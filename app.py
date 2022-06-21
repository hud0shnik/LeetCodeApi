#!flask/bin/python
from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

class User:
    def __init__(self, username, activity_status):
        self.username = username
        self.activity_status = activity_status
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False)

def find(fullStr, substr, stopChar) -> str:
    i = fullStr.find(substr)
    fullStr = fullStr[i+len(substr):]
    return fullStr[:fullStr.find(stopChar)]

@app.route('/user/<string:id>', methods=['GET'])
def get_tasks(id):
    html = requests.get('https://vk.com/'+id).text
    result = User(
        id, 
        find(html, '<span class="pp_last_activity_text">', '<')
    )
    return result.toJSON()

if __name__ == '__main__':
    app.run()