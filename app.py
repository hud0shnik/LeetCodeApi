#!flask/bin/python
from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

class User:
    def __init__(self, username):
        self.username = username
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@app.route('/user/<string:id>', methods=['GET'])
def get_tasks(id):
    result = User(id)
    file = open("sample.html", "w")
    file.write(requests.get('http://leetcode.com/'+id).text)
    file.close()
    return result.toJSON()

if __name__ == '__main__':
    app.run()