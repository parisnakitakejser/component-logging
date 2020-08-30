from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, SequenceField, BooleanField, DateTimeField, ListField
from odm.author import Author


class LoggingData(EmbeddedDocument):
    summary = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(required=True)


class Logging(Document):
    number = SequenceField()
    identifier = StringField(required=True, max_length=32)
    environment = StringField(required=True, max_length=32)

    data = EmbeddedDocumentField(LoggingData)

    tags = ListField(StringField())
    binds = ListField(StringField(), required=True)

    author = EmbeddedDocumentField(Author)
    system = BooleanField(default=False)

    created_at = DateTimeField()
    deleted_at = DateTimeField()

    meta = {
        'auto_create_index': True,
        'index_background': True,
        'indexes': [{
            'fields': ['binds', 'identifier', 'environment']
        }]
    }
