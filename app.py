from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_path = "example.db"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT,
        email TEXT UNIQUE
    )
    ''')

    conn.commit()
    conn.close()


# ---------- FUNCTIONS ----------
def get_users():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def add_user(first_name, last_name, gender, phone, email):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (first_name, last_name, gender, phone, email)
    VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, gender, phone, email))

    conn.commit()
    conn.close()


def update_user(id, first_name, last_name, gender, phone, email):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE users
    SET first_name=?, last_name=?, gender=?, phone=?, email=?
    WHERE id=?
    ''', (first_name, last_name, gender, phone, email, id))

    conn.commit()
    conn.close()


def delete_user(id):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()


# ---------- ROUTES ----------
@app.route('/')
def index():
    init_db()  # 🔥 ensures table exists
    users = get_users()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if not first_name or not last_name:
        return "Missing data!"

    add_user(first_name, last_name, gender, phone, email)
    return redirect(url_for('index'))


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user_route(id):

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not first_name or not last_name:
            return "First and Last name required!"

        update_user(id, first_name, last_name, gender, phone, email)
        return redirect(url_for('index'))

    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (id,))
    user = cursor.fetchone()
    conn.close()

    return render_template('update_user.html', user=user)


@app.route('/delete_user/<int:id>')
def delete_user_route(id):
    delete_user(id)
    return redirect(url_for('index'))


# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)