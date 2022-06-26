#!flask/bin/python

from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

# Пользователь
class User:

    # Конструктор
    def __init__(self, username, name = "", activity_status = "", 
                followers = "", posts = "", home = "", work=""):
        self.username = username
        self.name = name
        self.activity_status = activity_status
        self.followers = followers
        self.posts = posts
        self.home = home
        self.work = work

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
def find(fullStr, substr, stopChar, add_count = 0) -> str:
    if substr in fullStr:
        fullStr = fullStr[fullStr.find(substr)+len(substr)+add_count:]
        return fullStr[:fullStr.find(stopChar)]
    return ''
    

# Роут /user/
@app.route('/user/<string:id>', methods=['GET'])
def get_tasks(id):

    # Объект, в который будет вестись запись
    result = User(id)

    # Получение html файла странички
    html = requests.get('https://vk.com/'+id).text

    '''# Сохранение html'ки в файл (для тестов)
    file = open("sample.html", "w")
    file.write(html)
    file.close() '''

    # Проверка на существование пользователя
    if '<title>404 Not Found</title>' in html:
        return Error("Not Found").toJSON()

    # Проверка на возможность обработки
    if '<div class="service_msg service_msg_null">' in html:
        return Error("Access Denied").toJSON()

    # Удаление символов "-"
    html = html.replace('<span class="num_delim"> </span>', '')

    # Имя
    result.name = find(html, 'type="user">', '<')

    # Статус активности
    result.activity_status = find(html, '<span class="pp_last_activity_text">', '<')

    # Город
    result.home = find(html, 'id="home_outline_20__Icon-Color"', '<', 113)

    # Место работы
    result.work = find(html, 'id="work_outline_20__Icon-Color"', '</div>', 120)

    # Количество подписчиков
    result.followers = find(html, 'id="followers_outline_20__Icon-Color"', ' ', 106)

    # Количество записей
    result.posts = find(html, 'class="slim_header slim_header_block_top">', ' ')

    return result.toJSON()

