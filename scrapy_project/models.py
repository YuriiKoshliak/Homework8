from mongoengine import Document, StringField, ListField, connect

connect('quotes_db', host='your_mongo_host', username='your_username', password='your_password')

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = StringField(required=True)
    quote = StringField(required=True)