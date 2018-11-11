import os


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
RESOURCE_PATH = ROOT_PATH + "/../resources/"
SUPERUSERMASTER={"name":'master',
                 "password":'masterpassword',
                 'email':'master@fynd.com',
                 'username':'masterfynd',
                 'isadmin':True}

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_SECRET_KEY = 'secret123'

ELASTIC_APP_HOST  = 'localhost'
ELASTIC_APP_PORT = 9200

