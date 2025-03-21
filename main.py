import bcrypt
import mysql.connector
from tkinter import *

def password_to_hash(plain_password):
    """ Hashování hesla pomocí bcrypt. """
    try: 
        password_bytes = plain_password.encode('utf-8')
        hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hash.hex()  # Ukládáme jako HEX řetězec, protože MySQL neumí přímo pracovat s byte-array
    except Exception as e:
        print(f'Error při hashování hesla: {e}')
        return None

def insert_regr_user(username, email, password):
    """ Vloží nového uživatele do databáze. """
    try:
        connection = mysql.connector.connect(
            host='dbs.spskladno.cz',
            port=3306,
            user='student8',
            password='spsnet',
            database='vyuka8'
        )
        cur = connection.cursor()
        query = '''INSERT INTO uziv(username, email, password) VALUES(%s, %s, %s)'''

        hash = password_to_hash(password)
        cur.execute(query, (username, email, hash))
        connection.commit()
        connection.close()
    except mysql.connector.Error as e:
        print(f'Error databáze: {e}')
    except Exception as e:
        print(f'Obecná chyba: {e}')
    else:
        print('Uživatel úspěšně zaregistrován')
        result_label['text'] = 'Registrace proběhla úspěšně'

def get_hash_from_database(username):
    """ Získá hash hesla z databáze na základě uživatelského jména. """
    try:
        connection = mysql.connector.connect(
            host='dbs.spskladno.cz',
            port=3306,
            user='student8',
            password='spsnet',
            database='vyuka8'
        )
        cur = connection.cursor()
        query = '''SELECT password FROM uziv WHERE username=%s'''
        cur.execute(query, (username,))
        user_hash_password = cur.fetchone()
        connection.close()

        if user_hash_password:
            return bytes.fromhex(user_hash_password[0])  # Převádíme HEX zpět na bytes
        else:
            return b''
    except mysql.connector.Error as e:
        print(f'Error databáze: {e}')
        return b''
    except Exception as e:
        print(f'Obecná chyba: {e}')
        return b''

def login_authentication(username, password):
    """ Ověří přihlašovací údaje uživatele. """
    try:
        hash = get_hash_from_database(username)
        password_byte = bytes(password, encoding='utf-8')

        if hash == b'':
            result_label['text'] = 'Neplatné'
        else:
            if bcrypt.checkpw(password_byte, hash):
                result_label['text'] = 'Úspěšné přihlášení'
                import pisk
                pisk.singed_user = username
                pisk.run()
            else:
                result_label['text'] = 'Neplatné'
    except Exception as e:
        result_label['text'] = 'Došlo k chybě při ověřování'
        print(f'Chyba při ověřování: {e}')


root = Tk()
root.title('Registrace a přihlášení')
root.geometry('300x300')
root.resizable(False,False)


registration_label = Label(text='Registrace')
registration_label.grid(row=0, column=1)

username_label = Label(text='Jméno: ')
username_label.grid(row=1, column=0)

username_entry = Entry()
username_entry.grid(row=1, column=1)

email_label = Label(text='Email: ')
email_label.grid(row=2, column=0)

email_entry = Entry()
email_entry.grid(row=2, column=1)

password_label = Label(text='Heslo: ')
password_label.grid(row=3, column=0)

password_entry = Entry(show='*')
password_entry.grid(row=3, column=1)

registration_button = Button(text='Zaregistrovat', command=lambda:insert_regr_user(username_entry.get(), email_entry.get(), password_entry.get()))
registration_button.grid(row=4, column=1)

login_label = Label(text='Přihlášení: ')
login_label.grid(row=5, column=1)

username_login_label = Label(text='Jméno: ')
username_login_label.grid(row=5, column=0)

username_login_entry = Entry()
username_login_entry.grid(row=5, column=1)


password_login_label = Label(text='Heslo: ')
password_login_label.grid(row=6, column=0)


password_login_entry = Entry(show='*')
password_login_entry.grid(row=6, column=1)

login_button = Button(text='Přihlásit se',
                      command=lambda: login_authentication(username_login_entry.get() ,password_login_entry.get()))
login_button.grid(row=8, column=1)

result_label = Label()
result_label.grid(row=9, column=1)

root.mainloop()
