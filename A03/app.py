from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'test.db'

# Setup: Create a simple users table if it doesn't exist
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('alice', 'wonderland'))
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('bob', 'builder'))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h2>A03: Injection Demo</h2>
        <a href="/login">Vulnerable Login (SQL Injection)</a><br>
        <a href="/login/safe">Safe Login (Parameterized)</a><br>
        <a href="/login/orm_vuln">Vulnerable ORM Login</a><br>
        <a href="/login/orm_safe">Safe ORM Login</a><br>
        <a href="/cmd_injection">Command Injection</a><br>
        <a href="/safe_view_file">Safe File Viewer</a><br>
    '''

# Vulnerable to SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login_vuln():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # DANGEROUS: User input directly in SQL
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            return f"Welcome, {username}! (Vulnerable login)"
        return "Invalid credentials. Try again."
    return '''
        <h3>Vulnerable Login</h3>
        <form method='post'>
            Username: <input name='username'><br>
            Password: <input name='password' type='password'><br>
            <input type='submit' value='Login'>
        </form>
        <p>Try SQL Injection: username = alice' -- , password = anything</p>
    '''

# Safe from SQL Injection
@app.route('/login/safe', methods=['GET', 'POST'])
def login_safe():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # SAFE: Parameterized query
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            return f"Welcome, {username}! (Safe login)"
        return "Invalid credentials. Try again."
    return '''
        <h3>Safe Login</h3>
        <form method='post'>
            Username: <input name='username'><br>
            Password: <input name='password' type='password'><br>
            <input type='submit' value='Login'>
        </form>
    '''

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Ensure the ORM table exists and insert demo users if not present
with app.app_context():
    db.create_all()
    # Insert demo users if not already present
    if not User.query.filter_by(username='alice').first():
        db.session.add(User(username='alice', password='wonderland'))
    if not User.query.filter_by(username='bob').first():
        db.session.add(User(username='bob', password='builder'))
    db.session.commit()

@app.route('/login/orm_vuln', methods=['GET', 'POST'])
def orm_vuln():
    message = ''
    if request.method == 'POST':
        user_input = request.form.get('username', '')
        # DANGEROUS: Directly interpolating user input into ORM filter
        try:
            from sqlalchemy import text
            user = User.query.filter(text(f"username = '{user_input}'")).first()
            if user:
                message = f"Found user: {user.username}"
            else:
                message = "No user found."
        except Exception as e:
            message = f"Error: {e}"
    return f'''
        <h3>Vulnerable ORM Login</h3>
        <form method="post">
            Username: <input name="username"><br>
            <input type="submit" value="Lookup">
        </form>
        <p>{message}</p>
        <p>Try injection: <code>' OR '1'='1</code></p>
    '''

@app.route('/login/orm_safe', methods=['GET', 'POST'])
def orm_safe():
    message = ''
    if request.method == 'POST':
        user_input = request.form.get('username', '')
        # SAFE: Use parameterized ORM filtering
        user = User.query.filter_by(username=user_input).first()
        if user:
            message = f"Found user: {user.username}"
        else:
            message = "No user found."
    return f'''
        <h3>Safe ORM Login</h3>
        <form method="post">
            Username: <input name="username"><br>
            <input type="submit" value="Lookup">
        </form>
        <p>{message}</p>
    '''

# Command Injection Demo (DANGEROUS: for demonstration only)
@app.route('/cmd_injection', methods=['GET', 'POST'])
def cmd_injection():
    import subprocess
    from flask import request
    output = ''
    if request.method == 'POST':
        filename = request.form.get('filename', '')
        # DANGEROUS: vulnerable to command injection
        proc = subprocess.run(f"cat {filename}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            decoded = proc.stdout.decode('utf-8')
        except UnicodeDecodeError:
            decoded = proc.stdout.decode('utf-8', errors='replace')
        output = f"<pre>{decoded}</pre>"
    return f'''
        <h3>View File (Command Injection Demo)</h3>
        <p><b>Example payloads:</b></p>
        <ul>
            <li><code>test.db</code> (safe, shows contents of test.db)</li>
            <li><code>test.db; whoami</code> (unsafe, demonstrates command injection)</li>
            <li><code>test.db; rm -rf /tmp</code> (dangerous, demonstrates destructive command injection)</li>
        </ul>
        <form method="post">
            Filename: <input name="filename" type="text"><br>
            <input type="submit" value="View">
        </form>
        {output}
        <p>DANGEROUS: Never use user input in system commands!</p>
    '''

# Safe File Viewer Demo (prevents command injection)
@app.route('/safe_view_file', methods=['GET', 'POST'])
def safe_view_file():
    from flask import request, abort
    import os
    output = ''
    safe_dir = os.path.abspath('.')  # For demo, use current directory; in production, use a dedicated safe directory
    if request.method == 'POST':
        filename = request.form.get('filename', '')
        # Only allow alphanumeric filenames (no path traversal, no shell metacharacters)
        if not filename.isalnum():
            abort(400, "Invalid filename: only alphanumeric filenames allowed.")
        file_path = os.path.join(safe_dir, filename)
        # Ensure file is within the safe directory
        if not file_path.startswith(safe_dir):
            abort(400, "Invalid file path.")
        if not os.path.isfile(file_path):
            abort(404, "File not found.")
        with open(file_path, 'r') as f:
            content = f.read()
        output = f"<pre>{content}</pre>"
    return f'''
        <h3>Safe File Viewer (No Command Injection)</h3>
        <p><b>Example payloads:</b></p>
        <ul>
            <li><code>testdb</code> (allowed, shows contents of testdb if present)</li>
            <li><code>test.db</code> (blocked, not alphanumeric)</li>
            <li><code>test.db; whoami</code> (blocked, not alphanumeric)</li>
        </ul>
        <form method="post">
            Filename: <input name="filename" type="text"><br>
            <input type="submit" value="View">
        </form>
        {output}
        <p>This demo prevents command injection by validating input and not using the shell.</p>
        <p>Only alphanumeric filenames in the current directory are allowed.</p>
    '''

if __name__ == '__main__':
    app.run(port=5003, debug=True)
