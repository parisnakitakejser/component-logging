from mongoengine import Document, StringField, DateTimeField, BooleanField


class Authentication(Document):
    identifier = StringField(required=True, max_length=32)
    environment = StringField(required=True, max_length=32)

    secret_key = StringField(required=True, max_length=64)
    available = BooleanField(default=True)

    created_at = DateTimeField()

    meta = {
        'indexes': [{
            'fields': ['identifier', 'environment', 'secret_key']
        }]
    }
