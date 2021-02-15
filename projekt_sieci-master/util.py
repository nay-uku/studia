import csv
import random
import sys
from time import strptime, strftime

import tweepy
import json
import re
import os

from gexf import Gexf
from tqdm import tqdm

from unidecode import unidecode

from statistics import stdev, mean


# czytanie ich w forze linia po linii działało mi o dziwo znacznie szybciej
def read_tweets(start, end):
    with open('./twity_08.04_nowy.csv', encoding="latin1") as csvDataFile:
        reader = csv.reader(csvDataFile)
        tweets = []
        i = 0
        for i, row in enumerate(reader):
            if i < start:
                continue
            tweets.append({
                "id": row[0],
                # Usuwa emoji i nadmiarowe znaki nowej linii
                "text": (re.sub(r"<U+.*?>", '', row[1])).replace('\n', ' ').strip(),
                "time": row[2],
                "user_id": row[3],
                "tweet_id": row[4],
                "ret": row[5],
                "quoted": row[6],
                "retweet_id": row[7]
            })
            if i >= end:
                return tweets
    return tweets


def twitter_auth():
    auth = tweepy.OAuthHandler("KYGW9PINfIJH9ezrtF4iqBWgm",
                               "yWexC4rOvQdT7DvoE8EOrevhT7GU6rynFo494MSLS2ryELibex")
    auth.set_access_token("1257714832641572864-edCQ0GIKnofeYkFZbgEyy68fgBermN",
                          "vLdAJBYzSApCkwHkZdeSN1j9jjy8NZzx6Kb7HEpcJz0OV")
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api


# min, max tylko potrzebne do nazwy pliku
def get_location_and_save(tweets, start, end):
    api = twitter_auth()
    with open('miasta.csv', 'r', encoding="utf-8") as f1, open('woj.csv', 'r', encoding="utf-8") as f2:
        wojewodztwa_lines = [line.strip() for line in f2]

        woj = {line.split(';')[0]: line.split(';')[1] for line in wojewodztwa_lines}

        miasta_lines = [line.strip() for line in f1]

        miasta_wojewodztwa = {line.split(';')[2]: woj.get(line.split(';')[1]) for line in miasta_lines}

    i = 0
    for tweet in tweets:
        if i % 100 == 0:
            print("Tweet: " + tweet["id"])
        i += 1

        try:
            location = api.get_user(tweet["user_id"]).location
            tweet["location"] = location
        except:
            tweet["location"] = ""

        if location.split(',')[0] in miasta_wojewodztwa.keys():
            tweet["woj"] = miasta_wojewodztwa.get(location.split(',')[0])
        else:
            tweet["woj"] = ""

    # Opcja tekstowa
    # with open('tweets_loc_{}_{}.txt'.format(start, end), 'w', newline='', encoding='utf-8') as file:
    #     for tweet in tweets:
    #         file.write("{}\n".format('|~|'.join(tweet.values())))
    # Opcja JSON
    with open('tweets_woj_{}_{}.json'.format(start, end), 'w', encoding='utf-8') as file:
        file.write(json.dumps(tweets, indent=4, sort_keys=True, ensure_ascii=False))

    return


# jsony w jeden
# wynik: "tweets_woj_merged.json" wszystko w jednym
# wynik: "tweets_woj_merged_onlyloc.json" wszystko w jednym, ale tylko jeżeli lokalizacja nie jest pusta
def merge_jsons():
    # sortowanie po pierwszej liczbie
    jsons_sorted = sorted(os.listdir("woj"), key=lambda x: int(x.split('_')[2]))

    with open(f"woj/{jsons_sorted[0]}", 'r', encoding="utf8") as f:
        json_dict = json.load(f, encoding='utf8')

    for filename in jsons_sorted[1:]:
        with open(f"woj/{filename}", 'r', encoding="utf8") as f:
            json_dict.extend(json.load(f, encoding='utf8'))

    with open("tweets_woj_merged.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(json_dict, indent=4, sort_keys="id", ensure_ascii=False))

    with open("tweets_woj_merged_onlyloc.json", 'w', encoding='utf8') as f:
        only_loc = list(filter(lambda sample: sample.get("location") != "", json_dict))
        f.write(json.dumps(only_loc, indent=4, sort_keys="id", ensure_ascii=False))


# Funkcja wypisuje liczbę kompletnych tweetów
# Funkcja tworzy plik "set_nieprzypisanych_lokalizacji.txt", który ma zestaw nieprzypisanych lokalizacji
def list_nonassigned_locations(file):
    with open(file, 'r', encoding="utf8") as f:
        json_dict = json.load(f, encoding='utf8')

        json_dict_nonassigned = [tweet for tweet in json_dict if not tweet.get("woj")]

        print(
            f"Complete tweets: {len(json_dict) - len(json_dict_nonassigned)} Non-assigned tweets: {len(json_dict_nonassigned)} Total tweets: {len(json_dict)}")

        location_set = set([tweet.get("location") for tweet in json_dict_nonassigned])

    with open("set_nieprzypisanych_lokalizacji.txt", 'w', encoding='utf-8') as f:
        f.write("\n".join(location_set))


# Funkcja naprawia tweety bez województwa w pliku źrodłowym
# Funkcja zapisuje poprawiony plik jako "tweets_woj_merged_onlyloc_currentfix.json"
# Funkcja wypisuje liczbę poprawionych tweetów
def fix_nonassigned_locations(file):
    # Odczytanie słownika miast i województw
    with open('miasta.csv', 'r', encoding="utf-8") as f1, open('woj.csv', 'r', encoding="utf-8") as f2:
        wojewodztwa_lines = [line.strip() for line in f2]

        woj = {line.split(';')[0]: line.split(';')[1] for line in wojewodztwa_lines}

        miasta_lines = [line.strip() for line in f1]

        miasta_wojewodztwa = {unidecode(line.split(';')[2].lower()): woj.get(line.split(';')[1]) for line in
                              miasta_lines}

    # Odczytanie pliku źródłowego
    with open(file, 'r', encoding="utf8") as f:
        json_dict = json.load(f, encoding='utf8')

    # Licznik
    fixed_counter = 0

    for tweet in json_dict:
        if not tweet.get("woj"):
            split_words = [unidecode(word.strip()) for word in re.split('[#-/|,;(]', re.sub(
                "gmina|poland|\spolska|polonia|🇵🇱|\spl\s|🇪🇺|^polska|polen", "", tweet.get("location").lower()))]
            matched_city = list(set(split_words) & set(miasta_wojewodztwa.keys()))

            if matched_city:
                tweet["woj"] = miasta_wojewodztwa.get(matched_city[0])
                fixed_counter += 1

    # Zapis
    with open("tweets_woj_merged_onlyloc_currentfix.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(json_dict, indent=4, ensure_ascii=False))

    print(f"Fixed tweets: {fixed_counter}")


def categorization(file='./tweets_woj_merged_onlyloc_currentfix.json'):
    # Załadowanie słowników
    is_domestic_dict = read_dict('./isDomestic_dict.csv')
    is_political_dict = read_dict('./isPolitical_dict.csv')

    # Odczyt tweet-ów
    with open(file, 'r', encoding="utf8") as tweets_file:
        tweets = json.load(tweets_file, encoding='utf8')

    with open('hashtags_categorized.json', 'r') as f:
        hashtags = json.load(f, encoding='utf8')

    with open('domestic_keywords.txt', 'r') as f:
        domestic_keywords = [unidecode(line.strip()) for line in f]

    hashtags_categorized = [(h, c) for h, c in hashtags.items() if
                            c["domestic"] != "unknown" or c["political"] != "unknown"]
    total_length = len(tweets)
    domestic_unknowns = 0
    political_unknowns = 0
    # Przypisanie każdemu tweet-u kategorii
    for tweet in tqdm(tweets):
        tweet["is_domestic"] = False if classify(tweet['text'], is_domestic_dict) else "unknown"
        tweet["is_political"] = classify(tweet['text'], is_political_dict) or "unknown"

        if any(keyword in tweet["text"] for keyword in domestic_keywords):
            tweet["is_domestic"] = True

        tweet_hashtags = [hashtag.strip() for hashtag in tweet["text"].split() if hashtag.startswith('#')]
        for hashtag, categories in hashtags_categorized:
            if tweet["is_domestic"] != "unknown" and tweet["is_political"] != "unknown":
                break
            if hashtag in tweet_hashtags:
                if categories["domestic"] != "unknown":
                    tweet["is_domestic"] = categories["domestic"]
                if categories["political"] != "unknown":
                    tweet["is_political"] = categories["political"]

        if tweet["is_domestic"] == "unknown":
            domestic_unknowns += 1
        if tweet["is_political"] == "unknown":
            political_unknowns += 1

    print("TOTAL TWEETS: {} DOMESTIC: {} POLITICAL: {}".format(total_length, total_length - domestic_unknowns,
                                                               total_length - political_unknowns))
    # Zapis do pliku
    with open("tweets_categorized.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(tweets, indent=4, ensure_ascii=False))
    return 0


def read_dict(filename):
    with open(filename, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        dictionary = []
        for i, row in enumerate(reader):
            dictionary.append({
                "id": row[0],
                "value": row[1]
            })
    return dictionary


def classify(text, dictionary):
    for entry in dictionary:
        if entry["value"] in text:
            return True
    return False


def json_to_csv(json_in, csv_out):
    with open(json_in) as f:
        data = json.load(f)

    with open(csv_out, "w") as f:
        output = csv.writer(f)
        output.writerow(data[0].keys())
        for row in data:
            output.writerow(row.values())


def categorize_hashtags(file='hashtags.json'):
    with open(file, 'r', encoding="utf8") as f:
        hashtags = json.load(f, encoding='utf8')

    with open('isDomestic_dict.csv', 'r') as f:
        international_hashtags = [line.split(';')[1].strip() for line in f if line.split(';')[1].startswith('#')]
    with open('isPolitical_dict.csv', 'r') as f:
        political_hashtags = [line.split(';')[1].strip() for line in f if line.split(';')[1].startswith('#')]
    with open('miasta.csv', 'r') as f:
        cities = [unidecode(line.split(';')[2].lower().strip()) for line in f]
    with open('kraje.csv', 'r') as f:
        countries = [unidecode(line.lower().strip()) for line in f]
    with open('hashtags_political_keywords.txt', 'r') as f:
        political_keywords = [unidecode(line.lower().strip()) for line in f]
    with open('hashtags_domestic_keywords.txt', 'r') as f:
        domestic_keywords = [unidecode(line.lower().strip()) for line in f]

    for hashtag, categories in hashtags.items():
        # Hashtagi polityczne ze słownika
        if hashtag in political_hashtags:
            categories["political"] = True
            categories["domestic"] = True
        # Hashtagi międzynarodowe ze słownika
        if hashtag in international_hashtags:
            categories["domestic"] = False

        # Polityczne słowa kluczowe
        if any(keyword in unidecode(hashtag.strip('.@#;').lower()) for keyword in political_keywords):
            categories["political"] = True
        # Krajowe słowa kluczowe
        if any(keyword in unidecode(hashtag.strip('.@#;').lower()) for keyword in domestic_keywords):
            categories["domestic"] = True

        # Krajowe hashtagi
        if any(city in unidecode(hashtag.strip('.@#;').lower()) for city in cities):
            categories["domestic"] = True
        if any(country in unidecode(hashtag.strip('.@#;').lower()) for country in countries):
            categories["domestic"] = False

    total_domestic = [_ for _ in hashtags.values() if _["domestic"] != "unknown"]
    total_political = [_ for _ in hashtags.values() if _["political"] != "unknown"]
    print(f"Total hashtags: {len(hashtags)}\n")
    print(f"Total domestic: {len(total_domestic)}\n")
    print(f"Total political: {len(total_political)}\n")

    with open("hashtags_categorized.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(hashtags, indent=4, ensure_ascii=False))

    return


def create_graph(json_in='tweets_categorized.json', gexf_out='graph.gexf'):
    gexf = Gexf('MiASZ - podgrupa 4', '22-06-2020')
    graph = gexf.addGraph('undirected', 'dynamic', 'MIASZ - podgrupa 4')

    node_id = 0
    edge_id = 0

    print("Dodawanie wojewodztw")
    provinces_nodes = []
    # Dodanie województw
    with open('woj.csv', 'r', encoding="utf-8") as f_woj:
        reader = csv.reader(f_woj)
        for row in enumerate(reader):
            woj_name = row[1][0].split(';')[1]
            graph.addNode(node_id, woj_name, r="255", g="0", b="0")
            provinces_nodes.append({
                "id": node_id,
                "woj_name": woj_name
            })
            node_id += 1

    print("Dodawanie uzytkownikow")
    users_nodes = []
    # Dodanie użytkowników
    with open(json_in, 'r', encoding="utf8") as f_tweets:
        data = json.load(f_tweets, encoding='utf8')
        users = []
        for row in data:
            if row["user_id"] not in users:
                user_id = row["user_id"]
                users.append(user_id)
                time = strftime('%Y-%m-%d', strptime(row["time"], '%Y-%m-%d %H:%M:%S'))
                graph.addNode(node_id, '', start=time, r="0", g="255", b="0")
                print(time)
                users_nodes.append({
                    "id": node_id,
                    "user_id": user_id
                })
                # Dodanie gałęzi lives_in
                if len(row["woj"]) > 0:
                    woj = row["woj"]
                else:
                    woj = 'unknown'
                print("user_id: " + user_id + " lives in " + woj)
                for province in provinces_nodes:
                    if province["woj_name"] == woj:
                        graph.addEdge(edge_id, node_id, province["id"])
                        edge_id += 1
                # Inkrementacja node_id
                node_id += 1

    tweets_nodes = []
    # Dodanie tweetów
    with open(json_in, 'r', encoding="utf8") as f_tweets:
        data = json.load(f_tweets, encoding='utf8')
        for row in data:
            tweet_id = row["tweet_id"]
            text = row["text"]
            time = strftime('%Y-%m-%d', strptime(row["time"], '%Y-%m-%d %H:%M:%S'))
            graph.addNode(node_id, '', start=time, end=time, r="0", g="0", b="255")
            tweets_nodes.append({
                "id": node_id,
                "label": text
            })
            # Dodanie gałęzi tweeted
            user_id = row["user_id"]
            print("user_id: " + user_id + " tweeted: " + tweet_id)
            for user in users_nodes:
                if user["user_id"] == user_id:
                    graph.addEdge(edge_id, node_id, user["id"])
                    edge_id += 1
            # Inkrementacja node_id
            node_id += 1
    print("Koniec")
    f_out = open(gexf_out, 'wb')
    gexf.write(f_out)


def create_graph_optimized(json_in='tweets_categorized.json', gexf_out='graph.gexf'):
    gexf = Gexf('MiASZ - podgrupa 4', '22-06-2020')
    graph = gexf.addGraph('undirected', 'dynamic', 'MIASZ - podgrupa 4')

    node_id = 0
    edge_id = 0

    print("Dodawanie wojewodztw:")
    provinces_nodes = []
    # Dodanie województw #
    with open('woj.csv', 'r', encoding="utf-8") as f_woj:
        reader = csv.reader(f_woj)
        for row in enumerate(reader):
            woj_name = row[1][0].split(';')[1]
            graph.addNode(node_id, woj_name, r="255", g="0", b="0")
            print("Dodano wojewodztwo; node_id: " + str(node_id))
            provinces_nodes.append({
                "id": node_id,
                "woj_name": woj_name
            })
            node_id += 1

    print("Dodawanie uzytkownikow:")
    # Dodanie użytkowników oraz tweet-ów #
    with open(json_in, 'r', encoding="utf8") as f_tweets:
        data = json.load(f_tweets, encoding='utf8')
        for row in data:
            user_node_id = node_id
            time = strftime('%Y-%m-%d', strptime(row["time"], '%Y-%m-%d %H:%M:%S'))
            # Dodanie użytkownika #
            graph.addNode(node_id, 'u', start=time, end=time, r="0", g="255", b="0")
            node_id += 1
            print("Dodano użytkownika; node_id: " + str(user_node_id))
            # Dodanie gałęzi lives_in
            if len(row["woj"]) > 0:
                woj = row["woj"]
            else:
                woj = 'unknown'
            for province in provinces_nodes:
                if province["woj_name"] == woj:
                    graph.addEdge(edge_id, user_node_id, province["id"])
                    print("Utworzono gałęź lives_in; edge_id: " + str(edge_id))
                    edge_id += 1
                    break
            print("Utworzono gałęź lives_in; edge_id: " + str(edge_id))

            # Dodanie tweetu #
            tweet_node_id = node_id
            graph.addNode(node_id, 't', start=time, end=time, r="0", g="0", b="255")
            node_id += 1
            print("Dodano tweet; node_id: " + str(tweet_node_id))
            # Dodanie gałęzi tweeted
            graph.addEdge(edge_id, tweet_node_id, user_node_id)
            print("Utworzono gałęź tweeted; edge_id: " + str(edge_id))
            edge_id += 1

    print("Zapisywanie grafu do plku:")
    f_out = open(gexf_out, 'wb')
    gexf.write(f_out)
    print("Graf zapisano do pliku.")
    print("Koniec.")


def create_graph_for_province(province, json_in='tweets_categorized.json'):
    gexf_out = province + '.gexf'
    gexf = Gexf('MiASZ - podgrupa 4; ' + province, '22-06-2020')
    graph = gexf.addGraph('undirected', 'dynamic', 'MIASZ - podgrupa 4')

    node_id = 0
    edge_id = 0

    print("Dodawanie wojewodztw:")
    # Dodanie województwa #
    graph.addNode(node_id, province, r="255", g="0", b="0")
    print("Dodano wojewodztwo; node_id: " + str(node_id))
    province_id = node_id
    node_id += 1

    print("Dodawanie uzytkownikow:")
    # Dodanie użytkowników oraz tweet-ów #
    with open(json_in, 'r', encoding="utf8") as f_tweets:
        data = json.load(f_tweets, encoding='utf8')
        for row in data:
            if (len(row["woj"]) > 0) and (row["woj"] == province):
                user_node_id = node_id
                time = strftime('%Y-%m-%d', strptime(row["time"], '%Y-%m-%d %H:%M:%S'))
                # Dodanie użytkownika #
                graph.addNode(node_id, 'u', start=time, end=time, r="0", g="255", b="0")
                node_id += 1
                print("Dodano użytkownika; node_id: " + str(user_node_id))
                # Dodanie gałęzi lives_in
                graph.addEdge(edge_id, user_node_id, province_id)
                edge_id += 1
                print("Utworzono gałęź lives_in; edge_id: " + str(edge_id))

                # Dodanie tweetu #
                tweet_node_id = node_id
                graph.addNode(node_id, 't', start=time, end=time, r="0", g="0", b="255")
                node_id += 1
                print("Dodano tweet; node_id: " + str(tweet_node_id))
                # Dodanie gałęzi tweeted
                graph.addEdge(edge_id, tweet_node_id, user_node_id)
                print("Utworzono gałęź tweeted; edge_id: " + str(edge_id))
                edge_id += 1
        print("Dodano wszystkie wierzchołki oraz gałęzie.")

    print("Zapisywanie grafu do plku:")
    f_out = open(gexf_out, 'wb')
    gexf.write(f_out)
    print("Graf zapisano do pliku.")
    print("Koniec.")


def analyze_tweets(file='tweets_categorized.json'):
    with open(file, 'r', encoding="utf8") as f:
        tweets = json.load(f, encoding='utf8')

    TOTAL_TWEETS = len(tweets)
    TOTAL_TWEETS_WITH_WOJ = len([tweet for tweet in tweets if tweet["woj"]])

    with open('woj.csv', 'r', encoding="utf8") as f:
        woj_stats = {line.split(';')[1].strip(): {} for line in f}

    woj_stats.pop("unknown", None)
    woj_stats.__setitem__("", {})

    for woj, stats in woj_stats.items():
        woj_tweets = len([tweet for tweet in tweets if tweet["woj"] == woj])
        political_tweets = len([tweet for tweet in tweets if tweet["woj"] == woj and tweet["is_political"] == True])
        domestic_tweets = len([tweet for tweet in tweets if tweet["woj"] == woj and tweet["is_domestic"] == True])
        stats["liczba tweetów"] = woj_tweets
        if woj:
            stats["% tweetów z przypisanymi województwami"] = round(100 * woj_tweets / TOTAL_TWEETS_WITH_WOJ, 2)
        if not woj:
            stats["% wszystkich tweetów"] = round(100 * woj_tweets / TOTAL_TWEETS, 2)

        stats["liczba politycznych tweetów"] = political_tweets
        stats["% politycznych tweetów w województwie"] = round(100 * political_tweets / woj_tweets, 2)
        stats["liczba krajowych tweetów"] = domestic_tweets
        stats["% krajowych tweetów w województwie"] = round(100 * domestic_tweets / woj_tweets, 2)

    general = {
        "najwięcej tweetów (top 3)": sorted(
            [{"woj": woj, "liczba": stats["liczba tweetów"]} for woj, stats in woj_stats.items()],
            key=lambda k: k["liczba"], reverse=True)[1:4:],
        "najwięcej politycznych tweetów (top 3)": sorted(
            [{"woj": woj, "liczba": stats["liczba politycznych tweetów"]} for woj, stats in woj_stats.items()],
            key=lambda k: k["liczba"], reverse=True)[1:4:],
        "najwięcej krajowych tweetów (top 3)": sorted(
            [{"woj": woj, "liczba": stats["liczba krajowych tweetów"]} for woj, stats in woj_stats.items()],
            key=lambda k: k["liczba"], reverse=True)[1:4:],
        "największy procent politycznych tweetów (top 3)": sorted(
            [{"woj": woj, "liczba": stats["% politycznych tweetów w województwie"]} for woj, stats in
             woj_stats.items()], key=lambda k: k["liczba"], reverse=True)[:3],
        "największy procent krajowych tweetów (top 3)": sorted(
            [{"woj": woj, "liczba": stats["% krajowych tweetów w województwie"]} for woj, stats in woj_stats.items()],
            key=lambda k: k["liczba"], reverse=True)[:3],
        "średni % politycznych tweetów": mean(
            [stats["% politycznych tweetów w województwie"] for woj, stats in woj_stats.items() if woj]),
        "średni % krajowych tweetów": mean(
            [stats["% krajowych tweetów w województwie"] for woj, stats in woj_stats.items() if woj]),
    }

    woj_stats.__setitem__("general", general)

    with open("statystyki_wojewodztw.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(woj_stats, indent=4, ensure_ascii=False))


def csv_to_neo4j_datatype():
    # datetime w neo potrzebuje w napisie znaku "T" między datą i czasem zamiast spacji
    r = csv.reader(open('tweets.csv'))
    lines = list(r)
    for l in lines:
        l[6] = l[6].replace(' ', 'T')
    print(lines[2])
    writer = csv.writer(open('tweets_to_neo.csv', 'w'))
    writer.writerows(lines)
    pass


def rand100k_tweets():
    # losowanie 100k linii bez powtórzeń z csv i zapis do innego pliku csv
    r = csv.reader(open('tweets.csv'))
    lines = list(r)
    a = lines[0]
    lines = random.sample(lines[1:-1], 100000)
    lines[0] = a
    writer = csv.writer(open('100k.csv', 'w'))
    writer.writerows(lines)
    pass
