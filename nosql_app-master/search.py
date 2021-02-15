from main import es
from helpers import Product


# Operacje na Elasticu
# jeżeli id indeksu istnieje to wartości zastępowane - czyli dodawnie nowych/modyfikacja istniejących
# index ~ table name
def add_to_index(index, doc_type, model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, doc_type=doc_type, id=model.id, body=payload)


def remove_from_index(index, id):
    es.delete(index=index, id=id)


# wyszukiwarka produktów
def query_index(index, doc_type, query=None):
    # multimatch: * - szukaj po wszystkich polach - name i description
    # fuziness - ile literówek można zrobić 1,2,..,AUTO - wylicza proporcjonalnie do długości query
    if query is not None:
        search = es.search(index=index, doc_type=doc_type,
                           body={'query':
                                     {'multi_match':
                                          {'query': query,
                                           'fields': ['*'],
                                           'fuzziness': 'AUTO'}
                                      }
                                 }
                           )
    else:
        search = es.search(index=index, doc_type=doc_type)
    # names = [hit['_source']['name'] for hit in search['hits']['hits']]
    # descriptions = [hit['_source']['description'] for hit in search['hits']['hits']]
    #records = [[int(hit['_id']), hit['_source']['name'], hit['_source']['description']] for hit in
               # search['hits']['hits']]
    #num_of_hits = search['hits']['total']['value']

    return search


def search_p_by_id(doc_type, id):
    try:
        search = es.get(index='products',doc_type=doc_type, id=id)
        name = search['_source']['name']
        description = search['_source']['description']
        price = search['_source']['price']
    except:
        return None
    return {'name': name, 'description': description, 'price': price}


def get_ids(index, doc_type):
    search = es.search(index=index, doc_type=doc_type)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids


def import_products_from_csv(doc_type):
    with open('./data/products.csv', encoding='utf-8') as lines:
        for line in lines:
            line = line.split(';')
            add_to_index('products', doc_type, Product(line[0], line[1], line[2], line[3]))
    pass
