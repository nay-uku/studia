rm -f nohup.out
nohup python3 /root/cassandra_statistics/cassandra_statistics_consumer.py &
echo "To get statistics info type: 'python3 /root/cassandra_statistics/cassandra_api.py'"
