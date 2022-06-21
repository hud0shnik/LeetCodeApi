#!flask/bin/python
from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

# Пользователь
class User:

    # Конструктор
    def __init__(self, username, activity_status = "", followers = "", posts = ""):
        self.username = username
        self.activity_status = activity_status
        self.followers = followers
        self.posts = posts

    # Функция конвертирования в json
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False)

# Ошибка
class Error:
    
    # Конструктор
    def __init__(self, title):
        self.title = title

    # Функция конвертирования в json
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False)

# Функция поиска значений
def find(fullStr, substr, stopChar) -> str:
    fullStr = fullStr[fullStr.find(substr)+len(substr):]
    return fullStr[:fullStr.find(stopChar)]

# Роут /user/
@app.route('/user/<string:id>', methods=['GET'])
def get_tasks(id):

    # Объект, в который будет вестись запись
    result = User(id)

    # Получение html файла странички
    html = requests.get('https://vk.com/'+id).text

    # Проверка на существование пользователя
    if html.find('<title>404 Not Found</title>') != -1:
        return Error("Not Found").toJSON()

    # Проверка на возможность обработки
    if html.find('<div class="service_msg service_msg_null">') != -1:
        return Error("Access Denied").toJSON()

    # Статус активности
    result.activity_status = find(html, '<span class="pp_last_activity_text">', '<')

    # Количество подписчиков
    result.followers = find(html, 'le="nonzero"/></g></g></g></svg></div></div><div class="OwnerInfo__rowCenter">', ' ')
    
    # Количество записей
    result.posts = find(html, 'class="slim_header slim_header_block_top">', ' ')
    
    
    return result.toJSON()

if __name__ == '__main__':
    app.run()