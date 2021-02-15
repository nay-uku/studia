import operator
import os
import string
import argparse
from cassandra.cluster import Cluster
from config import CASSANDRA_IP
from datetime import datetime
from datetime import timedelta
from map_reduce import *
from graphs import *

cass_cluster = Cluster([CASSANDRA_IP])
cass_session = cass_cluster.connect('statistics')

parser = argparse.ArgumentParser()
parser.add_argument("action", help="available: service, user, hashtag")
parser.add_argument("-sd", "--startdate", help="start date - format %%Y%%m%%d (if left empty, data from today is returned")
parser.add_argument("-ed", "--enddate", help="end date - format %%Y%%m%%d (usable alongside start date only)")
parser.add_argument("-t", "--top", type=int, help="top X users or top X hashtags")
parser.add_argument("-s", "--source", help="available: twitter, discord (default: twitter)")

args = parser.parse_args()

today = datetime.today()
today_msg_day = today.strftime("%Y%m%d")


if args.action == "service":

    if args.startdate:
        if args.enddate:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            end_date = datetime.strptime(args.enddate, "%Y%m%d")
            numdays = (end_date - start_date).days
            msg_day_list = tuple([(end_date - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays + 1)])
            stmt = cass_session.prepare(
                'select count(*) from messages where msg_day in ? and source = ?;')
            qry = stmt.bind([msg_day_list, 'twitter'])
            twitter_rows = cass_session.execute(qry)
            stmt = cass_session.prepare(
                'select count(*) from messages where msg_day in ? and source = ?;')
            qry = stmt.bind([msg_day_list, 'discord'])
            discord_rows = cass_session.execute(qry)
            print(f"TWITTER:\t{tuple(twitter_rows[0])[0]}\nDISCORD:\t{tuple(discord_rows[0])[0]}")
            bar_graph_save(['twitter', 'discord'], [tuple(twitter_rows[0])[0], tuple(discord_rows[0])[0]], f'Messages from each service ({start_date} - {end_date})')
        else:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            numdays = (today - start_date).days
            msg_day_list = tuple([(today - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays+1)])
            stmt = cass_session.prepare(
                'select count(*) from messages where msg_day in ? and source = ?;')
            qry = stmt.bind([msg_day_list, 'twitter'])
            twitter_rows = cass_session.execute(qry)
            stmt = cass_session.prepare(
                'select count(*) from messages where msg_day in ? and source = ?;')
            qry = stmt.bind([msg_day_list, 'discord'])
            discord_rows = cass_session.execute(qry)
            print(f"TWITTER:\t{tuple(twitter_rows[0])[0]}\nDISCORD:\t{tuple(discord_rows[0])[0]}")
            bar_graph_save(['twitter', 'discord'], [tuple(twitter_rows[0])[0], tuple(discord_rows[0])[0]],
                           f"Messages from each service ({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")

    else:
        stmt = cass_session.prepare('select count(*) from messages where msg_day = ? and source = ?;')
        qry = stmt.bind([today_msg_day, 'twitter'])
        twitter_rows = cass_session.execute(qry)
        stmt = cass_session.prepare(
            'select count(*) from messages where msg_day = ? and source = ?;')
        qry = stmt.bind([today_msg_day, 'discord'])
        discord_rows = cass_session.execute(qry)
        print(f"TWITTER:\t{tuple(twitter_rows[0])[0]}\nDISCORD:\t{tuple(discord_rows[0])[0]}")
        bar_graph_save(['twitter', 'discord'], [tuple(twitter_rows[0])[0], tuple(discord_rows[0])[0]],
                       f"Messages from each service - {today.strftime('%Y-%m-%d %H:%M:%S')}")

if args.action == "user":
    if args.source:
        source = args.source
    else:
        source = 'twitter'
    if args.startdate:
        if args.enddate:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            end_date = datetime.strptime(args.enddate, "%Y%m%d")
            numdays = (end_date - start_date).days
            msg_day_list = tuple([(end_date - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays + 1)])

            stmt = cass_session.prepare(
                "SELECT author, count(*) FROM messages WHERE msg_day in ? AND source = ? GROUP BY msg_day, source, author;")
            qry = stmt.bind([msg_day_list, source])
            twitter_rows = cass_session.execute(qry)
            sorted_users = sorted([tuple(row) for row in list(twitter_rows)], key=lambda x: x[1], reverse=True)

            if args.top:
                print(sorted_users[:args.top])
                if sorted_users:
                    users, counts = zip(*sorted_users[:args.top])
                    pie_chart_save(users, counts, f"Most active {source} users - ({start_date} - {end_date})")
            else:
                print(sorted_users[:5])
                if sorted_users:
                    users, counts = zip(*sorted_users[:5])
                    pie_chart_save(users, counts, f"Most active {source} users - ({start_date} - {end_date})")

        else:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            numdays = (today - start_date).days
            msg_day_list = tuple([(today - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays + 1)])

            stmt = cass_session.prepare(
                "SELECT author, count(*) FROM messages WHERE msg_day in ? AND source = ? GROUP BY msg_day, source, author;")
            qry = stmt.bind([msg_day_list, source])
            twitter_rows = cass_session.execute(qry)
            sorted_users = sorted([tuple(row) for row in list(twitter_rows)], key=lambda x: x[1], reverse=True)
            if args.top:
                print(sorted_users[:args.top])
                if sorted_users:
                    users, counts = zip(*sorted_users[:args.top])
                    pie_chart_save(users, counts, f"Most active {source} users\n({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print(sorted_users[:5])
                if sorted_users:
                    users, counts = zip(*sorted_users[:5])
                    pie_chart_save(users, counts, f"Most active {source} users\n({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")

    else:
        stmt = cass_session.prepare(
            "SELECT author, count(*) FROM messages WHERE msg_day = ? AND source = ? GROUP BY msg_day, source, author;")
        qry = stmt.bind([today_msg_day, source])
        twitter_rows = cass_session.execute(qry)
        sorted_users = sorted([tuple(row) for row in list(twitter_rows)], key=lambda x: x[1], reverse=True)
        if args.top:
            print(sorted_users[:args.top])
            if sorted_users:
                users, counts = zip(*sorted_users[:args.top])
                pie_chart_save(users, counts, f"Most active {source} users today\n{today.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(sorted_users[:5])
            if sorted_users:
                users, counts = zip(*sorted_users[:5])
                pie_chart_save(users, counts, f"Most active {source} users today\n{today.strftime('%Y-%m-%d %H:%M:%S')}")


def hashtag_mapper(msg_text):
    hashtag_list = []
    for part in msg_text.split():
        if part.startswith('#'):
            hashtag_list.append((part[1:], 1))
    return hashtag_list


def hashtag_reducer(item):
    word, occurrences = item
    return word, sum(occurrences)


if args.action == "hashtag":
    source = 'twitter'
    if args.startdate:
        if args.enddate:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            end_date = datetime.strptime(args.enddate, "%Y%m%d")
            numdays = (end_date - start_date).days
            msg_day_list = tuple([(end_date - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays + 1)])

            stmt = cass_session.prepare(
                "SELECT msg_data FROM messages WHERE msg_day in ? AND source = ?;")
            qry = stmt.bind([msg_day_list, source])
            twitter_rows = cass_session.execute(qry)
            message_texts = [row[0] for row in twitter_rows]
            mapper = MapReduce(hashtag_mapper, hashtag_reducer, 3)
            hashtag_counts = mapper(message_texts)
            hashtag_counts.sort(key=operator.itemgetter(1))
            hashtag_counts.reverse()
            if args.top:
                print(hashtag_counts[:args.top])
                if hashtag_counts:
                    hashtags, counts = zip(*hashtag_counts[:args.top])
                    pie_chart_save(hashtags, counts,
                                   f"Most popular hashtags\n({start_date} - {end_date})")
            else:
                print(hashtag_counts[:5])
                if hashtag_counts:
                    hashtags, counts = zip(*hashtag_counts[:5])
                    pie_chart_save(hashtags, counts,
                                   f"Most popular hashtags\n({start_date} - {end_date})")
        else:
            start_date = datetime.strptime(args.startdate, "%Y%m%d")
            numdays = (today - start_date).days
            msg_day_list = tuple([(today - timedelta(days=x)).strftime("%Y%m%d") for x in range(numdays + 1)])

            stmt = cass_session.prepare(
                "SELECT msg_data FROM messages WHERE msg_day in ? AND source = ?;")
            qry = stmt.bind([msg_day_list, source])
            twitter_rows = cass_session.execute(qry)
            message_texts = [row[0] for row in twitter_rows]
            mapper = MapReduce(hashtag_mapper, hashtag_reducer, 3)
            hashtag_counts = mapper(message_texts)
            hashtag_counts.sort(key=operator.itemgetter(1))
            hashtag_counts.reverse()
            if args.top:
                print(hashtag_counts[:args.top])
                if hashtag_counts:
                    hashtags, counts = zip(*hashtag_counts[:args.top])
                    pie_chart_save(hashtags, counts,
                                   f"Most popular hashtags\n({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print(hashtag_counts[:5])
                if hashtag_counts:
                    hashtags, counts = zip(*hashtag_counts[:5])
                    pie_chart_save(hashtags, counts, f"Most popular hashtags\n({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")

    else:
        stmt = cass_session.prepare(
            "SELECT msg_data FROM messages WHERE msg_day = ? AND source = ?;")
        qry = stmt.bind([today_msg_day, source])
        twitter_rows = cass_session.execute(qry)
        message_texts = [row[0] for row in twitter_rows]
        mapper = MapReduce(hashtag_mapper, hashtag_reducer, 3)
        hashtag_counts = mapper(message_texts)
        hashtag_counts.sort(key=operator.itemgetter(1))
        hashtag_counts.reverse()
        if args.top:
            print(hashtag_counts[:args.top])
            if hashtag_counts:
                hashtags, counts = zip(*hashtag_counts[:args.top])
                pie_chart_save(hashtags, counts, f"Most popular hashtags today\n{today.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(hashtag_counts[:5])
            if hashtag_counts:
                hashtags, counts = zip(*hashtag_counts[:5])
                pie_chart_save(hashtags, counts, f"Most popular hashtags today\n{today.strftime('%Y-%m-%d %H:%M:%S')}")
