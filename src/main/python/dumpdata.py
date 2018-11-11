from utility.toolbox import Toolbox

import requests
from flask import Flask, request, Response

import json
import hashlib

app = Flask(__name__)



@app.route('/add_movies', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data_element = request.get_json()
        if isinstance(data_element,list):
            for ele in data_element:
                j_ele = json.dumps(ele)
                element_id = hashlib.md5( str(j_ele).encode())
                req = requests.put(Toolbox.elastic_search_insert_url(element_id), data=j_ele)
        if isinstance(data_element,dict):
            j_ele = json.dumps(data_element)
            element_id = hashlib.md5(str(j_ele).encode())
            req = requests.put(Toolbox.elastic_search_insert_url(element_id), data=j_ele)
    return Response('True')



@app.route('/delete_movies', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        data_element = request.get_json()
        if isinstance(data_element,list):
            for ele in data_element:
                j_ele = json.dumps(ele)
                element_id = hashlib.md5( str(j_ele).encode())
                req = requests.delete(Toolbox.elastic_search_insert_url(element_id))
        if isinstance(data_element,dict):
            j_ele = json.dumps(data_element)
            element_id = hashlib.md5(str(j_ele).encode())
            req = requests.delete(Toolbox.elastic_search_insert_url(element_id))
    return Response('True')


@app.route("/search", method=["GET" , "POST"])
def search():
    if request.method == "POST":
        data_element = request.get_json()
        element = data_element["serch_key"]
        try:
            element = float(element)


            search_body =  {
                "from": 0,
                "size": 1000,
                "query": {
                    "bool":{
                        "should": [
                                    { "match" : { "popularity" : element } },
                                    {"match": {"imdb_score": element }}
                        ]
                }
                    }
            }
        except:
            search_body = {
                "from": 0,
                "size": 1000,
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"director": element}},
                            {"match": {"genre": element}},
                            {"match": {"name": element}}
                        ]
                    }
                }
            }


        req = requests.get(
            "http://localhost:9200/fynd/movies/_search", data=json.dumps(search_body))
        return req.text




if __name__ == '__main__':
    app.run(host= "0.0.0.0" ,port= 5001)