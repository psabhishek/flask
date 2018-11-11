import hashlib
import peewee
from playhouse.signals import pre_save
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
    isadmin = peewee.TextField(default=False)

@pre_save(sender=User)
def user_pre_save(sender,instance,created):
    if created:
        instance.password = hashlib.md5(str(instance.password).encode()).hexdigest()


class Movies(BaseModel):
    popularity  = peewee.DecimalField()
    director = peewee.TextField()
    genre = peewee.TextField()
    imdb_score = peewee.DecimalField()
    name = peewee.TextField()


