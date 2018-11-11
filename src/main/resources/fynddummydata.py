
import json
import hashlib
import requests

a = []
import pdb;pdb.set_trace()

if __name__ == '__main__':
    for ele in a:
        abc = hashlib.md5(str(ele).encode()).hexdigest()
        res = requests.put(url = "http://lodalhost:9200/fynd/movies/{}".format(abc),data = json.dumps(ele))

