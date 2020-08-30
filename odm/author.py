from mongoengine import EmbeddedDocument, StringField


class Author(EmbeddedDocument):
    name = StringField(required=True)
    identifier = StringField()
    ipv4 = StringField()
    ipv6 = StringField()