from settings import ELASTIC_APP_HOST, ELASTIC_APP_PORT


class Toolbox(object):
    @staticmethod
    def elastic_search_insert_url(id):
        elastic_url = "http://"+ELASTIC_APP_HOST+":"+str(ELASTIC_APP_PORT)+'/fynd/movies'+str(id)
        return elastic_url