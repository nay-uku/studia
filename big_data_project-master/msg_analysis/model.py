import pytz
from datetime import datetime
from neomodel import StructuredNode, StructuredRel, DateTimeProperty, StringProperty, RelationshipFrom, RelationshipTo, \
    config, One, OneOrMore, ZeroOrMore

NEO4J_CLUSTER_IP = "10.7.38.69"
config.DATABASE_URL = f'bolt://:@{NEO4J_CLUSTER_IP}:7687'


class AuthorRel(StructuredRel):
    timestamp = DateTimeProperty(default=lambda: datetime.now(pytz.utc))


class User(StructuredNode):
    nick = StringProperty(required=True)
    service = StringProperty(required=True)
    messages = RelationshipTo('Message', 'AUTHOR', cardinality=ZeroOrMore, model=AuthorRel)
    location = RelationshipTo('Location', 'LIVES', cardinality=OneOrMore)


class Message(StructuredNode):
    text = StringProperty(required=True)
    language = StringProperty(required=True)
    author = RelationshipFrom('User', 'AUTHOR', cardinality=One, model=AuthorRel)


class Location(StructuredNode):
    name = StringProperty(required=True)
    users = RelationshipFrom('Location', 'LIVES', cardinality=ZeroOrMore)
