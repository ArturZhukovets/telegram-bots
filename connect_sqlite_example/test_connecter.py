import sqlite3


with sqlite3.connect('example.db') as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS test""")
    cur.execute("""CREATE TABLE IF NOT EXISTS test
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,
                    user_id INT,
                    user_reg_date TEXT DEFAULT ''
                    );""")
    data = ('maria', '14', '2022.14.10')
    cur.execute("""INSERT INTO test (user_name, user_id, user_reg_date)
                    VALUES(
                    ?, ?, ?
                    )""", data)
    # cur.execute("""INSERT INTO test (user_name, user_id)
    #                 VALUES
    #                 ('Paren', 14),
    #                 ("devochka", 15);
    #                 """)

    cur.execute("SELECT * FROM test")
    result = cur.fetchall()

    print(result)
    con.commit()
