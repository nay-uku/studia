# -*- coding: utf-8 -*-
import json
import os
import uuid
import pytz
from cassandra.cluster import Cluster
from cassandra.util import datetime_from_uuid1
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify, flash
from flask_pymongo import PyMongo
from flask_jwt_extended import decode_token, JWTManager, jwt_required, jwt_optional, create_access_token, \
    set_access_cookies, set_refresh_cookies, create_refresh_token, \
    get_jwt_identity, jwt_refresh_token_required, unset_jwt_cookies
from flask_socketio import SocketIO
import bcrypt
import redis
import datetime
from jwt import decode
from kafka import KafkaProducer
from config import Config
import helpers
from search import *
from bson.objectid import ObjectId

# REDIS funkcje własne
from _redis import redis_get_login_timestamp, redis_store_forum_login_timestamp, redis_get_forum_login_timestamps, \
    redis_add_to_shopping_cart, redis_clear_shopping_cart, redis_get_shopping_cart, redis_remove_from_shopping_cart, redis_store_product_last_view, redis_get_product_last_view

app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.globals.update(redis_remove_from_shopping_cart=redis_remove_from_shopping_cart)

socketIO = SocketIO(app)

# Ustawienie timezone
tz = pytz.timezone('Europe/Warsaw')

# CASSANDRA #
cass_cluster = Cluster([Config.CLUSTER_IP])
cass_session = cass_cluster.connect('cassandra_nosql')

# ELASTICSEARCH #
es = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

# KAFKA #
kafka_producer = KafkaProducer(bootstrap_servers=Config.CLUSTER_IP + ":9092",
                               value_serializer=lambda m: json.dumps(m, default=datetime_converter).encode('ascii'))

# MONGO #
app.config['MONGO_DBNAME'] = 'TEST'
app.config['MONGO_URI'] = 'mongodb://' + Config.CLUSTER_IP + ':27017/TEST'
mongo = PyMongo(app)

# JWT #
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# JWT auth okres ważności
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)
# JWT refresh okres ważności
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/login'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config["JWT_SECRET_KEY"] = "SECRET_KEY"
jwt = JWTManager(app)

# REDIS #
# pool = redis.ConnectionPool(host='192.168.56.56', port=6379)
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
pool = redis.ConnectionPool(host=Config.CLUSTER_IP, port=6379)
redis = redis.Redis(connection_pool=pool)


# JWT-Extended dziwnie się konfiguruje dla stron, które mają nie wymagać JWT, stąd ta funkcja - na podstawie cookie
# zwraca identity usera
def get_identity_from_jwt(cookie):
    if cookie:
        try:
            dict = decode(cookie, app.config.get("JWT_SECRET_KEY"), algorithms='HS256')
            return dict.get('identity')
        except:
            pass
    return None


@app.route('/')
def index(user=None):
    if request.cookies.get("access_token_cookie"):
        user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    # Uzupełnienie elastica przykładowymi danymi
    # try:
    import_products_from_csv('game')
    # except:
    #    pass
    return render_template("home.html", user=user)


@app.route('/landing')
@jwt_required
def landing(user=None, timestamp=None):
    user = get_jwt_identity()
    return render_template("home.html", user=user,
                           timestamp=redis_get_login_timestamp(redis, request.cookies.get("access_token_cookie")))


# Przeglądarka nie robi tego automatycznie - jeżeli auth straci ważność, urywa sesję
# w aktualnej wersji nie jest wykorzystywane
@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, 200


@app.route('/login', methods=['POST', 'GET'])
def login():
    # HTTP POST - proces logowania
    if request.method == 'POST':
        # Mongo - wyszukiwanie użytkownika
        users = mongo.db.users
        already_exists = users.find_one({'email': request.form['email']})

        # Mongo - użytkownik istnieje
        if already_exists:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), already_exists['password']):
                # Tworzenie i przydzielanie JWT auth + refresh
                access_token = create_access_token(identity=request.form['email'])
                refresh_token = create_refresh_token(identity=request.form['email'])
                response = redirect(url_for('landing'))
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                # Umieszczenie pary token : user oraz daty ostatniego logowania do bazy Redis
                redis.hset('login:', access_token, request.form['email'])
                redis.hset('last_login:', access_token, str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")))
                # Przesłanie notyfikacji o zalogowaniu się użytkownika do brokera
                log_day = get_current_day()
                kafka_producer.send('login-logs', {'log_day': log_day,
                                                   'user': request.form['email'],
                                                   'time': datetime.datetime.now(),
                                                   'msg': 'User has successfully logged in.'})
                return response

        # Mongo - brak użytkownika LUB niepoprawne hasło - zwraca error
        return render_template("login.html", error="failed_login")

    # HTTP GET - zwraca stronę logowania
    return render_template("login.html", error=None)


@app.route('/register', methods=['POST', 'GET'])
def register():
    # HTTP POST - proces rejestracji
    if request.method == 'POST':
        # Mongo - wyszukiwanie użytkownika
        users = mongo.db.users
        already_exists = users.find_one({'email': request.form['email']})

        # Mongo - użytkownik nie istnieje
        if not already_exists:
            users.insert({'email': request.form['email'],
                          'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())})
            # Przesłanie notyfikacji o zarejestrowaniu się użytkownika do brokera
            log_day = get_current_day()
            kafka_producer.send('registration-logs', {'log_day': log_day,
                                                      'user': request.form['email'],
                                                      'time': datetime.datetime.now(),
                                                      'msg': 'User has successfully registered.'})
            return redirect(url_for('index'))
        # Mongo - użytkownik istnieje
        # Do zmiany
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject), 500)

    # HTTP GET - zwraca stronę rejestracji
    return render_template("register.html")


@app.route('/logout', methods=['POST'])
def logout():
    response = redirect(url_for('index'))
    unset_jwt_cookies(response)
    return response


@app.route('/forum', methods=['GET'])
def forum(user=None, forum_users=None, forum_posts=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if user:
        redis_store_forum_login_timestamp(redis, user)

    forum_users = redis_get_forum_login_timestamps(redis)
    posts = mongo.db.posts
    forum_posts = [(cursor.get('title'), cursor.get('text'), cursor.get('author'), cursor.get('date_added'), cursor.get('_id')) for cursor
                   in posts.find({})]
    return render_template("forum.html", user=user, forum_users=forum_users, forum_posts=forum_posts)


@app.route('/forum/add_post', methods=['GET', 'POST'])
def add_post(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        posts = mongo.db.posts
        posts.insert({'title': request.form['title'],
                      'text': request.form['text'],
                      'author': user,
                      'date_added': str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
                      })
        return redirect(url_for('forum'))

    return render_template("add_post.html", user=user)

@app.route('/forum/post', methods=['GET'])
def post(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if not user:
        return redirect(url_for('login'))
    if not 'p' in request.args:
        return redirect(url_for('forum'))
    post_id = request.args['p']
    print(post_id)
    sanitized_post_id = post_id.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})

    post = mongo.db.posts.find_one({"_id": ObjectId(sanitized_post_id)})
    if not post:
        return redirect(url_for('forum'))

    return render_template("post.html", user=user, post=post)

@app.route('/forum/add_comment', methods=['POST'])
def add_comment(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if not user:
        return redirect(url_for('login'))
    if not 'p_id' or not 'comment' in request.form:
        return redirect(request.referrer)


    sanitized_post_id = request.form['p_id'].translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})

    comment = request.form['comment']

    # Do dodania - ochrona przed XSS
    sanitized_comment = comment

    mongo.db.posts.update(
        {"_id": ObjectId(sanitized_post_id)},
            {
                "$push":
                {
                    "comments":
                    {
                        "$each":
                        [
                            {
                                'author' : user,
                                'text' : sanitized_comment,
                                'date_added': str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
                             }

                        ],
                        "$sort":
                        {
                            "date_added" : 1
                        }

                    }

                }
            }
    )

    return redirect(request.referrer)



@app.route('/listings', methods=['GET', 'POST'])
def listings(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    search_form = helpers.SearchForm()
    # pokaż wszystkie produkty
    try:
        search_res = query_index('products', 'game')
        products = [[int(hit['_id']), hit['_source']['name'], hit['_source']['description']] for hit in
                    search_res['hits']['hits']]
    except:
        return render_template("home.html", user=user)  # gdy baza nie wczytana przenosi na główną
    return render_template("listings.html", user=user, products=products, search_form=search_form)


@app.route('/search', methods=['GET', 'POST'])
def search(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    search_form = helpers.SearchForm()
    # pokaż produkty zwrócone z query do elastcicSearch
    try:
        q = request.args.get('q')
        search_res = query_index('products', 'game', q)
        products = [[int(hit['_id']), hit['_source']['name'], hit['_source']['description']] for hit in
                    search_res['hits']['hits']]
    except:
        return render_template("home.html", user=user)
    return render_template("listings.html", user=user, products=products, search_form=search_form)


@app.route('/product', methods=['GET'])
def product(user=None, product_data=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    p_id = request.args.get('p')

    # sprawdzenie poprawności parametru
    if p_id is None or p_id == '' or not p_id.isdigit():
        return redirect(url_for('index'))
    ids = get_ids('products', 'game')
    if int(p_id) not in ids:
        return redirect(url_for('listings'))
    product_data = search_p_by_id('game', int(p_id))

    # to poniżej jest chyba niepotrzebne
    if not product_data:
        return redirect(url_for('listings'))

    product_data['p_id'] = p_id

    # pobranie i zapisanie kto ostatni wyświetlał produkt
    last_view = redis_get_product_last_view(redis, p_id)
    if user is None:
        redis_store_product_last_view(redis, p_id, "anonymous")
    else:
        redis_store_product_last_view(redis, p_id, user)
    return render_template("product.html", user=user, product_data=product_data, last_view=last_view)


def sanitize_number(parameter):
    return parameter if isinstance(parameter, int) else None


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart(user=None):
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.cookies.get("access_token_cookie"):
            user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
        if not user:
            return redirect(url_for('login'))

        p_id = request.form.get('p_id')
        number = request.form.get('number')
        if p_id.isdigit() and number.isdigit() and (0 < int(number) <= 500):
            product_data = search_p_by_id('game', p_id)

            # jeżeli taki produkt ma jakieś dane
            if product_data:
                product_data['p_id'] = p_id
                redis_add_to_shopping_cart(redis, user, product_data, number)
                return redirect(url_for('cart'))

    return redirect(url_for('listings'))


@app.route('/cart')
def cart(user=None, cart=None):
    if request.cookies.get("access_token_cookie"):
        user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if not user:
        return redirect(url_for('login'))

    # tu powinno wczytywać z redisa listę produktów z koszyka

    cart = redis_get_shopping_cart(redis, user)

    return render_template("cart.html", user=user, cart=cart, redis=redis)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart(user=None):
    if request.method == 'POST':
        if request.cookies.get("access_token_cookie"):
            user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
        if not user:
            return redirect(url_for('login'))

        if request.form['p_id'] and request.form['p_id'].isdigit():
            redis_remove_from_shopping_cart(redis, user, request.form['p_id'])

    return redirect(url_for('cart'))


@app.route('/chat', methods=['GET', 'POST'])
def chat(user=None):
    if request.cookies.get("access_token_cookie"):
        user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    if not user:
        return redirect(url_for('login'))
    msgs = get_messages()
    return render_template("chat.html", user=user, msgs=msgs)


@socketIO.on('connect_notice')
def handle_connect_notice_event(data):
    msg = data['user'] + " connected to the chat."
    app.logger.info(msg)
    socketIO.emit('add_message', msg, broadcast=True)


@socketIO.on('disconnect_notice')
def handle_disconnect_notice_event(data):
    msg = data['user'] + " disconnected from chat."
    app.logger.info(msg)
    socketIO.emit('add_message', msg, broadcast=True)


@socketIO.on('send_message')
def handle_send_message_event(data):
    app.logger.info(data['user'] + " send message: " + data['message'])
    # Ustawienie parametrów
    msg_day = get_current_day()
    ins_time = uuid.uuid1()
    local_time = utc_to_local_time(datetime_from_uuid1(ins_time))
    # Zapisanie wiadomości do bazy Cassandra
    stmt = cass_session.prepare("INSERT INTO chat_messages (msg_day, username, message, ins_time) VALUES (?,?,?,?)")
    qry = stmt.bind([msg_day, data['user'], data['message'], ins_time])
    cass_session.execute(qry)
    app.logger.info("Message saved in Cassandra.")
    # Przesłanie notyfikacji o wysłaniu przez użytkownika wiadomości do brokera
    log_day = get_current_day()
    kafka_producer.send('send-message-logs', {'log_day': log_day,
                                              'user': data['user'],
                                              'time': local_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                              'msg': data['message']})
    # Wysłanie wiadomości do wszystkich klientów
    msg = local_time.strftime('%Y-%m-%d %H:%M:%S') + " <b>" + data['user'] + ":&nbsp;</b> " + data['message']
    socketIO.emit('add_message', msg, broadcast=True)


def get_messages():
    msg_day = get_current_day()
    stmt = cass_session.prepare(
        "SELECT toTimestamp(ins_time) as time, username, message  FROM chat_messages WHERE msg_day = ? ORDER BY ins_time DESC;")
    qry = stmt.bind([msg_day])
    # Funkcja toTimestamp zwróci timestamp UTC, dlatego konwertuję msg['time'] do czasu lokalnego
    msgs = [{'time': utc_to_local_time(msg[0]).strftime('%Y-%m-%d %H:%M:%S'), 'username': msg[1], 'message': msg[2]} for
            msg in cass_session.execute(qry)]
    return msgs


def get_current_day():
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    return '{}{}{}'.format(year, month, day)


# Konwersja czasu UTC na lokalny
def utc_to_local_time(utc_time):
    return pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@app.route('/daily_logs', methods=['GET', 'POST'])
def daily_logs(user=None):
    user = get_identity_from_jwt(request.cookies.get("access_token_cookie"))
    login_logs = get_user_logs('login-logs')
    registration_logs = get_user_logs('registration-logs')
    send_message_logs = get_user_logs('send-message-logs')
    return render_template("user_logs.html", login_logs=login_logs, registration_logs=registration_logs,
                           send_message_logs=send_message_logs, user=user)


def get_user_logs(topic):
    log_day = get_current_day()
    stmt = cass_session.prepare("SELECT * FROM user_logs WHERE log_day = ? AND topic = ? ORDER BY time DESC;")
    qry = stmt.bind([log_day, topic])
    return cass_session.execute(qry)


if __name__ == "__main__":
    socketIO.run(app, debug=True, port=int(os.getenv('PORT', 4444)))
