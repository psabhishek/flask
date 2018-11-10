import peewee
database = peewee.SqliteDatabase(database="databas")
database.connect()

class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    name = peewee.TextField(unique=True)
    email = peewee.TextField()
    username = peewee.TextField()
    password = peewee.TextField()
    isadmin = peewee.TextField()

class Movies(BaseModel):
    popularity  = peewee.DecimalField()
    director = peewee.TextField()
    genre = peewee.TextField()
    imdb_score = peewee.DecimalField()
    name = peewee.TextField()






def create_tables():
    with database:
        database.create_tables([User, Movies])

# create_tables()