from neomodel import StructuredNode, StringProperty, Relationship, config

NEO4J_CLUSTER_IP = "10.7.38.68"
config.DATABASE_URL = f'bolt://:@{NEO4J_CLUSTER_IP}:7687'


class Word(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    next_words = Relationship('Word', 'NEXT')
