import hashlib
import peewee
from playhouse.signals import pre_save,Model
from settings import SUPERUSERMASTER
database = peewee.SqliteDatabase(database="databas")
database.connect()


class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    name = peewee.TextField(unique=True)
    email = peewee.TextField()
    username = peewee.TextField()
    password = peewee.TextField()
    isadmin = peewee.BooleanField(default=False)

@pre_save(sender=User)
def user_pre_save(sender,instance,created):
    print(str(instance.password))
    instance.password = hashlib.md5(str(instance.password).encode()).hexdigest()


class Movies(BaseModel):
    popularity  = peewee.DecimalField()
    director = peewee.TextField()
    genre = peewee.TextField()
    imdb_score = peewee.DecimalField()
    name = peewee.TextField()




def create_tables():
    with database:
        database.create_tables([User, Movies])

def initialize_database():
    # doesnt matter if 1st time or everytime
    create_tables()
    # creating superuser
    try:
        password = SUPERUSERMASTER['password']
        del SUPERUSERMASTER['password']
        master,created = User.get_or_create(**SUPERUSERMASTER)
        if created:
            master.password = password
            master.save()
    except Exception as e:
        print(e)
        raise e
initialize_database()



