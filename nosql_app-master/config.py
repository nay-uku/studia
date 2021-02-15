# Ustawienienie całej konfiguracji przed włączeniem serwera
class Config(object):
    # Zmienna określająca adres IP klastra na którym znajdują się
    # CLUSTER_IP = 'localhost'
    CLUSTER_IP = '192.168.1.233'
    # CLUSTER_IP = '192.168.56.56'
    SECRET_KEY = 'debug'
    ELASTICSEARCH_URL = CLUSTER_IP + ':9200'
