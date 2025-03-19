from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import bcrypt
import mysql.connector

app = Flask(__name__, template_folder='templates')
app.secret_key = "tajny_klic"

# Připojení k databázi
def get_db_connection():
    return mysql.connector.connect(
        host='dbs.spskladno.cz',
        port=3306,
        user='student8',
        password='spsnet',
        database='vyuka8'
    )

# Funkce pro získání hashovaného hesla
def get_hash_from_database(username):
    """ Získá hash hesla z databáze na základě uživatelského jména. """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = '''SELECT password FROM uziv WHERE username=%s'''
        cur.execute(query, (username,))
        user_hash_password = cur.fetchone()
        conn.close()

        if user_hash_password and user_hash_password[0]:  # ✅ Ověření, že máme nějaký výsledek
            return bytes.fromhex(user_hash_password[0])  # Převádíme HEX zpět na bytes
        else:
            print("⚠️ Uživatel nenalezen nebo nemá heslo v databázi!")
            return None  # Uživatel nebyl nalezen

    except mysql.connector.Error as e:
        print(f'❌ Chyba databáze: {e}')
        return None
    except Exception as e:
        print(f'❌ Obecná chyba: {e}')
        return None
# Hlavní stránka
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

# Login stránka
@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

# Ověření přihlášení
@app.route('/login_validation', methods=['POST'])
def login():
    """ Zpracování přihlášení """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template("login.html", error="Chybí uživatelské jméno nebo heslo!")

        # Získání hashe z databáze
        hash = get_hash_from_database(username)

        if hash and bcrypt.checkpw(password.encode('utf-8'), hash):
            session['user'] = username  # Uložení uživatele do session
            return redirect(url_for('users_page'))  # Přesměrování na stránku s uživateli
        else:
            return render_template("login.html", error="Neplatné přihlašovací údaje!")

    return render_template("login.html")  # Pro GET request

@app.route('/users')
def users_page():
    """ Stránka se seznamem uživatelů """
    if 'user' not in session:
        return redirect(url_for('login'))  # Pokud není přihlášený, přesměrovat na login
    
    try:
        connection = get_db_connection()
        cur = connection.cursor(dictionary=True)

        # Získání informací o přihlášeném uživateli
        cur.execute("SELECT user_type_id FROM uziv WHERE username=%s", (session['user'],))
        user_info = cur.fetchone()
        is_admin = user_info and user_info['user_type_id'] == 1  # Admin má user_type_id = 1

        # Získání všech uživatelů
        cur.execute("SELECT ID, username, pocet_her, pocet_vyher FROM uziv")
        users = cur.fetchall()
        connection.close()
    except mysql.connector.Error as e:
        users = []
        print(f'Chyba databáze: {e}')
        is_admin = False

    return render_template("users.html", users=users, is_admin=is_admin)

@app.route('/update_user', methods=['POST'])
def update_user():
    """ Změní uživatelské jméno (pouze pro admina) """
    if 'user' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    cur = connection.cursor(dictionary=True)
    cur.execute("SELECT user_type_id FROM uziv WHERE username=%s", (session['user'],))
    user_info = cur.fetchone()

    if not user_info or user_info['user_type_id'] != 1:
        return "Nemáte oprávnění", 403

    user_id = request.form.get('user_id')  # Získání z form
    new_username = request.form.get('new_username')

    if not user_id or not new_username:
        return "Neplatné údaje", 400

    try:
        cur.execute("UPDATE uziv SET username=%s WHERE ID=%s", (new_username, user_id))
        connection.commit()
        return redirect(url_for('users_page'))  # Po změně se vrátit na users
    except mysql.connector.Error as e:
        return f"Chyba databáze: {e}", 500
    finally:
        connection.close()

@app.route('/delete_user', methods=['POST'])
def delete_user():
    """ Smaže uživatele (pouze admin) """
    if 'user' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    cur = connection.cursor(dictionary=True)
    cur.execute("SELECT user_type_id FROM uziv WHERE username=%s", (session['user'],))
    user_info = cur.fetchone()

    if not user_info or user_info['user_type_id'] != 1:
        return "Nemáte oprávnění", 403

    user_id = request.form.get('user_id')

    if not user_id:
        return "Neplatné údaje", 400

    try:
        cur.execute("DELETE FROM uziv WHERE ID=%s", (user_id,))
        connection.commit()
        return redirect(url_for('users_page'))  # Po smazání se vrátit na users
    except mysql.connector.Error as e:
        return f"Chyba databáze: {e}", 500
    finally:
        connection.close()

# Registrace uživatele
@app.route('/register', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not user_name or not email or not password:
            return "Všechna pole musí být vyplněna!", 400  # Chybová zpráva

        # Hashování hesla
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).hex()

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO uziv (username, email, password, user_type_id) VALUES (%s, %s, %s, %s)", 
                        (user_name, email, hashed_password, 2))  # 2 = běžný uživatel
            conn.commit()
            conn.close()

            print("✅ Registrace úspěšná! Přesměrování na login...")
            return redirect(url_for('login'))  # Přesměrování na login stránku
        except Exception as e:
            print(f'❌ Chyba při registraci: {e}')
            return f'Chyba při registraci: {e}', 500

    return render_template("register.html")
# Odhlášení
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
