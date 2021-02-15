# -*- coding: utf-8 -*-
import datetime


# Funkcja zwraca czas ostatniego zalogowania dla tokena (w przyszłości warto zmienić, żeby argumentem był user)
def redis_get_login_timestamp(redis, token):
    return redis.hget('last_login:', token).decode("utf-8")


# Zapisuje do Redisa czas wizyty użytkownika na forum
# i ucina, jeżeli jest więcej niż 3 rekordy w bazie
def redis_store_forum_login_timestamp(redis, user):
    # Czas musi być liczbą
    redis.zadd('forum_logins:', {user: datetime.datetime.now().timestamp()})
    # Top 3
    redis.zremrangebyrank('forum_logins:', 0, -3)
    return


# Wyciąga z Redisa wizyty użytkowników na forum
# naprawia sekundy na format daty
# zwraca odwróconą listę, bo dla Redisa więcej sekund - wyższy indeks
def redis_get_forum_login_timestamps(redis):
    zrange_with_floats = redis.zrange('forum_logins:', 0, -1, withscores='True')
    zrange_with_timestamps = [(user, datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')) for
                              (user, timestamp) in zrange_with_floats]
    return reversed(zrange_with_timestamps)


# Dodaje do redisa dla hashsetu "Cart:<EMAIL>" pozycje o kluczu ID produktu i wartości <NAZWA>|<CENA>|<LICZBA W KOSZYKU>
def redis_add_to_shopping_cart(redis, user, product_data, number):
    try:
        redis.hset('cart:' + user, product_data['p_id'],
                   '{}|{}|{}'.format(product_data['name'], product_data['price'], number))
    except:
        pass
    return


# Usuwa cały hashset użytkownika
def redis_clear_shopping_cart(redis, user):
    redis.delete('cart:' + user)
    return


# Usuwa wybrany produkt
def redis_remove_from_shopping_cart(redis, user, p_id):
    redis.hdel('cart:' + user, p_id)
    return


def redis_get_shopping_cart(redis, user):
    cart = redis.hgetall('cart:' + user)
    return cart


# Zwraca domyślny czas wygaśnięcia (w sekundach)
def redis_get_expire_ttl():
    return int(1*60)


# Zwraca nazwę zmiennej var_product, która przechowuje informacje o tym kto ostatni wyświetlił dany produkt
def redis_get_name_of_var_product(product_id):
    return 'product_' + product_id


# Ustawia kto jako ostatni wyświetlił dany produkt, zmienna usuwana jest po domyślnym czasie wygaśniecia
def redis_store_product_last_view(redis, product_id, user):
    var_product = redis_get_name_of_var_product(product_id)
    redis.setex(var_product, redis_get_expire_ttl(), user)
    return


# Pobiera kto jako ostatni wyświetlił dany produkt
def redis_get_product_last_view(redis, product_id):
    var_product = redis_get_name_of_var_product(product_id)
    if redis.exists(var_product):
        return {'user': redis.get(var_product).decode("utf-8"), 'time_ago': redis_get_expire_ttl()-redis.ttl(var_product)}
    else:
        return None
