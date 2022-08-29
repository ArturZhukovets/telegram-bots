import sqlite3
from datetime import date
import json


CURRENT_TIME = (date.today())


def ensure_connection(func):

    def inner(*args, **kwargs):
        """Открываем входящую функцию с помощью 'with open'."""
        with sqlite3.connect('sqlite_storage.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner

@ensure_connection
def init_db(conn, force=False):
    """Init db. IF force=True - delete the table and create new"""

    cur = conn.cursor()

    # Сообщения от пользователей и информация о них
    if force:
        cur.execute("""DROP TABLE IF EXISTS user_storage;""")
        cur.execute("""DROP TABLE IF EXISTS user_feedback;""")
    cur.execute("""
            CREATE TABLE IF NOT EXISTS user_storage( 
            user_id         INTEGER PRIMARY KEY,
            username        TEXT,
            user_password   INTEGER UNIQUE,
            user_firstname  TEXT
             );""")
    cur.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback(
            user_id INT NOT NULL,
            feedback TEXT,
            feedback_date TEXT,
            FOREIGN KEY (user_id) REFERENCES user_storage (user_id) ON DELETE CASCADE
            );
            """)

    # Сохранение изменений
    conn.commit()

@ensure_connection
def add_user(user_id:int, username:str, conn, user_firstname=None):
    """ТЕСТ. РАБОТАЕТ"""

    cur = conn.cursor()
    cur.execute("""INSERT INTO user_storage (user_id, username, user_firstname) VALUES (?, ?, ?) """, (user_id, username, user_firstname))

    conn.commit()

@ensure_connection
def add_password(user_id, user_password, conn):
    """ТЕСТ. РАБОТАЕТ"""

    cur = conn.cursor()

    cur.execute("""
        UPDATE user_storage
        SET user_password = ?  
        WHERE user_id = ?;
                """, (user_password, user_id))

    conn.commit()

@ensure_connection
def add_feedback(user_id, feedback, conn,  feedback_date=CURRENT_TIME,):
    """ТЕСТ. РАБОТАЕТ"""

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO user_feedback (user_id, feedback, feedback_date) VALUES
    (?, ?, ?);
    """, (user_id, feedback, feedback_date))

    conn.commit()


@ensure_connection
def get_last_message(user_id, conn=None) -> str:
    """Возращает последнее сообщение пользователя"""

    cur = conn.cursor()

    cur.execute("""
    SELECT feedback
    FROM user_feedback
    WHERE user_id = ?
    ORDER BY rowid DESC
    LIMIT 1;""", (user_id, ))
    (obj, ) = cur.fetchone()
    return obj


@ensure_connection
def get_list_message(user_id, number=10, conn=None) -> list:
    """Возращает список сообщений определенного пользователя
    По умолчанию - 10 сообщений"""

    cur = conn.cursor()

    cur.execute("""
    SELECT feedback
    FROM user_feedback
    WHERE user_id = ?
    ORDER BY rowid DESC
    LIMIT ?;
    """, (user_id, number))
    obj_list = cur.fetchall()
    return obj_list




# ------------------- Работа с хранилищем JSON ------------------- #

def content_from_json(path_to_fail) -> dict:
    """return data from json in dict format"""
    with open(path_to_fail, 'r', encoding='utf-8') as f_obj:
        dict_obj = json.load(f_obj)
    return dict_obj


def from_json_to_sqlite(obj_from_json:dict):
    """Receives data from json and loads in sqlite using cycle"""
    # Get data
    users_id = [key for key in obj_from_json]
    users_username = [obj_from_json[u_n].get('username', None) for u_n in users_id]
    users_firstname = [obj_from_json[u_fn].get('firstname', None) for u_fn in users_id]
    users_password = [obj_from_json[u_p].get('password', None) for u_p in users_id]
    users_feedback = [obj_from_json[u_fb].get('feedback', None) for u_fb in users_id]
    x = 0
    # Load data to sqlite
    for i in range(len(users_id)):
        add_user(user_id=users_id[i], username=users_username[i], user_firstname=users_firstname[i])
        add_password(users_id[i], users_password[i])
        number_of_feedbacks = len(users_feedback[i])
        # Т.к у каждого пользователя может быть несколько сообщений, необходимо загружать по одному сообщению за запрос sql
        for j in range(number_of_feedbacks):
            add_feedback(users_id[i], feedback=users_feedback[i][j])


# ------------------- Набор функций для загрузки в sql сразу из сообщения тг ------------------- #



if __name__ == '__main__':
    init_db(force=True)
    cont = content_from_json('json_data.json')
    from_json_to_sqlite(cont)






    # add_password(3, user_password="asdqweqtrqTEST_PASSWORDasdasdqweasd")
    # add_feedback(3, feedback="ДОЛЖЕН ВЫЙТИ ЭТОТ ФИДБЕК!")
    # print(get_last_message(1))