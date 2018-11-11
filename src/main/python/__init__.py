from models import database, User, Movies
from settings import SUPERUSERMASTER


def create_tables():
    with database:
        database.create_tables([User, Movies])

def initialize_database():
    # doesnt matter if 1st time or everytime
    create_tables()
    # creating superuser
    try:
        import pdb;pdb.set_trace()
        master,created = User.get_or_create(**SUPERUSERMASTER)
    except Exception as e:
        print(e)
        raise e

initialize_database()