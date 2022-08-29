import json
from uuid import uuid4
from telebot.types import Message


def open_storage(path):
    with open(path, 'r', encoding='utf-8') as file_obj:
        data_from_json = json.load(file_obj)
    return data_from_json


def add_to_storage(path, message, data_from_json):
    """Добавляет в существующее хранилище json нового пользователя
    Если пользователь уже есть в хранилище - оповещает его об этом"""
    user_id = str(message.from_user.id)
    username = message.from_user.username
    firstname = message.from_user.first_name
    if user_id not in data_from_json:
        data_from_json[user_id] = {'username': username, 'firstname': firstname, 'feedback':[]}
        with open(path, 'w', encoding='utf-8') as file_obj:
            json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
        return True

    else:
        return False


def password_to_storage(path,message, password, data_from_json):
    try:
        data_from_json[str(message.from_user.id)]['password'] = password

    except:
        return False

    with open(path, 'w', encoding='utf-8') as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
    return password


def add_review(path, message:Message, data_from_json:dict):
    try:
        user_id = str(message.from_user.id)
        data_from_json[user_id]['feedback'].append(message.text)
    except:
        return False
    with open(path, 'w', encoding='utf-8') as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
    return True


