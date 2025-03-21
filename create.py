import mysql.connector

def create():
    conn = mysql.connector.connect(
        host='dbs.spskladno.cz',
        port=3306,
        user='student8',
        password='spsnet',
        database='vyuka8'
    )

    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS uziv(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            username TEXT,
            email TEXT,
            password TEXT,
            user_type_id INT DEFAULT 2,
            pocet_her INT DEFAULT 0,
            pocet_vyher INT DEFAULT 0
        );'''
    )
    
    conn.commit()
    conn.close()

def create2():
    conn = mysql.connector.connect(
        host='dbs.spskladno.cz',
        port=3306,
        user='student8',
        password='spsnet',
        database='vyuka8'
    )

    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS uziv_type(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            user_type TEXT
        );'''
    )
    
    conn.commit()
    conn.close()


def insert_user_types():
    conn = mysql.connector.connect(
        host='dbs.spskladno.cz',
        port=3306,
        user='student8',
        password='spsnet',
        database='vyuka8'
    )
    cur = conn.cursor()
    
    cur.execute('''
            INSERT INTO uziv_type (ID, user_type)
            VALUES (%s, %s)
        ''', (1, 'admin'))
    cur.execute('''
            INSERT INTO uziv_type (ID, user_type)
            VALUES (%s, %s)
        ''', (2, 'hrac'))
    conn.commit()
    conn.close()


create()
create2()
insert_user_types()
