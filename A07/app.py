from flask import Flask, render_template_string, request, session, redirect, url_for
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# Secure user store with hashed passwords
USERS = {
    'admin': generate_password_hash('admin'),
    'alice': generate_password_hash('password123'),
    'bob': generate_password_hash('123456')
}

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template_string('''
    <h1>Authentication Failures Demo (Secure)</h1>
    {% if logged_in %}
        <p>Welcome, {{ session.username }}!</p>
        <a href="/logout">Logout</a>
    {% else %}
        <ul>
            <li><a href="/login">Login (Secure)</a></li>
            <li><a href="/register">Register (Secure)</a></li>
            <li><a href="/secure-practices">Security Practices</a></li>
        </ul>
    {% endif %}
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template_string('''
            <h1>Login Failed</h1>
            <p>Invalid credentials. Try again.</p>
            <a href="/login">Back to Login</a>
            ''')
    
    return render_template_string('''
    <h1>Login (Secure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p><small>Uses strong password hashing (no MD5).</small></p>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username and password and len(password) >= 8:
            USERS[username] = generate_password_hash(password)
            return render_template_string('<h1>Registered!</h1><a href="/login">Login</a>')
        else:
            return render_template_string('<h1>Error</h1><p>Password must be at least 8 characters.</p><a href="/register">Back</a>')
    
    return render_template_string('''
    <h1>Register (Secure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Register">
    </form>
    <p><small>Password must be at least 8 characters.</small></p>
    ''')

@app.route('/secure-practices')
def secure_practices():
    return render_template_string('''
    <h1>Secure Authentication Practices</h1>
    <ul>
        <li>Use strong password hashing (bcrypt, Argon2, or Werkzeug's default)</li>
        <li>Implement rate limiting and account lockout</li>
        <li>Enforce password complexity requirements</li>
        <li>Use multi-factor authentication (MFA)</li>
        <li>Generate secure random session tokens</li>
        <li>Use secure password recovery (time-limited tokens)</li>
    </ul>
    <p><strong>Security improvements made:</strong></p>
    <ul>
        <li>MD5 replaced with Werkzeug's secure hashing</li>
        <li>Secret key is no longer hardcoded</li>
        <li>Password minimum length enforced</li>
    </ul>
    <a href="/">Back</a>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, port=5007)
