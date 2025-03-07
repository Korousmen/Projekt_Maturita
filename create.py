import psycopg2

def create():
    conn = psycopg2.connect(
        dbname='projekt',
        user='postgres',
        password='heslo',
        host='localhost',
        port='5432'
        )

    cur = conn.cursor()
    cur.execute('''CREATE TABLE uziv(
            ID serial,
            username TEXT,
            email TEXT,
            password TEXT,
            pocet_her INT DEFAULT 0  ,
            pocet_vyher INT  DEFAULT 0 
                    )''')
    
    conn.commit()
    conn.close()

create()