from flask import Flask, request, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
DB_PATH = 'test.db'

# Setup: Create a simple users table if it doesn't exist
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)')
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('alice', generate_password_hash('wonderland')))
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('bob', generate_password_hash('builder')))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h2>A03: Injection - Secure Demo</h2>
        <a href="/login/safe">Safe Login (Parameterized)</a><br>
        <a href="/login/orm_safe">Safe ORM Login</a><br>
        <a href="/safe_view_file">Safe File Viewer</a><br>
        <a href="/security-info">Security Practices</a><br>
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
        c.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password))
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
        <p>Uses parameterized queries to prevent SQL injection.</p>
    '''

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

# Ensure the ORM table exists and insert demo users if not present
with app.app_context():
    db.create_all()
    # Insert demo users if not already present
    if not User.query.filter_by(username='alice').first():
        db.session.add(User(username='alice', password_hash=generate_password_hash('wonderland')))
    if not User.query.filter_by(username='bob').first():
        db.session.add(User(username='bob', password_hash=generate_password_hash('builder')))
    db.session.commit()

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
        <p>Uses ORM filter_by() which parameterizes queries.</p>
    '''

# Safe File Viewer Demo (prevents command injection)
@app.route('/safe_view_file', methods=['GET', 'POST'])
def safe_view_file():
    from flask import request, abort
    import os
    output = ''
    safe_dir = os.path.abspath('.')
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
        <p><b>Allowed filenames (alphanumeric only):</b></p>
        <ul>
            <li><code>testdb</code> (allowed, shows contents if present)</li>
        </ul>
        <form method="post">
            Filename: <input name="filename" type="text"><br>
            <input type="submit" value="View">
        </form>
        {output}
        <p>This demo prevents command injection by validating input and not using the shell.</p>
    '''

@app.route('/security-info')
def security_info():
    return render_template_string('''
    <h2>Security Practices Implemented</h2>
    <ul>
        <li>SQL queries use parameterized statements (no string formatting)</li>
        <li>ORM queries use filter_by() (not raw string interpolation)</li>
        <li>File viewing validates input and avoids shell commands</li>
        <li>Passwords are hashed (not stored in plaintext)</li>
        <li>Debug mode is disabled</li>
    </ul>
    <a href="/">Back</a>
    ''')

if __name__ == '__main__':
    app.run(port=5003, debug=False)
