from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from flask import session as login_session
import hashlib

app = Flask(__name__)
app.secret_key = 'weak-secret-key-123'  # VULNERABLE: Hardcoded weak secret

# Insecure user store (in production, use a database)
USERS = {
    'admin': hashlib.md5('admin'.encode()).hexdigest(),  # VULNERABLE: MD5 hashing
    'alice': hashlib.md5('password123'.encode()).hexdigest(),
    'bob': hashlib.md5('123456'.encode()).hexdigest()
}

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template_string('''
    <h1>Authentication Failures Demo</h1>
    {% if logged_in %}
        <p>Welcome, {{ session.username }}!</p>
        <a href="/logout">Logout</a>
    {% else %}
        <ul>
            <li><a href="/login">Login (Insecure)</a></li>
            <li><a href="/register">Register (Insecure)</a></li>
            <li><a href="/forgot-password">Forgot Password</a></li>
            <li><a href="/brute-force">Brute Force Test</a></li>
            <li><a href="/secure-login">Login (Secure)</a></li>
        </ul>
    {% endif %}
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: Weak MD5 hashing, no rate limiting
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        if username in USERS and USERS[username] == password_hash:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template_string('''
            <h1>Login Failed</h1>
            <p>Invalid credentials. Try again.</p>
            <a href="/login">Back to Login</a>
            ''')
    
    return render_template_string('''
    <h1>Login (Insecure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p><small>No rate limiting - vulnerable to brute force!</small></p>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: No password complexity validation
        if username and password:
            USERS[username] = hashlib.md5(password.encode()).hexdigest()
            return render_template_string('<h1>Registered!</h1><a href="/login">Login</a>')
    
    return render_template_string('''
    <h1>Register (Insecure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Register">
    </form>
    <p><small>Accepts any password, even "123" or "password"!</small></p>
    ''')

@app.route('/forgot-password')
def forgot_password():
    return render_template_string('''
    <h1>Forgot Password (Insecure)</h1>
    <p>Enter your security question answer:</p>
    <form>
        Username: <input type="text" name="username"><br>
        Mother's maiden name: <input type="text" name="answer"><br>
        <input type="submit" value="Reset Password">
    </form>
    <p><small>VULNERABLE: Security questions are insecure!</small></p>
    ''')

@app.route('/brute-force')
def brute_force():
    return render_template_string('''
    <h1>Brute Force Test</h1>
    <p>Try common passwords: admin/admin, alice/password123, bob/123456</p>
    <p><strong>No rate limiting implemented!</strong></p>
    <a href="/login">Try Login</a>
    ''')

@app.route('/secure-login')
def secure_login_info():
    return render_template_string('''
    <h1>Secure Authentication (Best Practices)</h1>
    <ul>
        <li>Use strong password hashing (bcrypt, Argon2)</li>
        <li>Implement rate limiting and account lockout</li>
        <li>Enforce password complexity requirements</li>
        <li>Use multi-factor authentication (MFA)</li>
        <li>Generate secure random session tokens</li>
        <li>Use secure password recovery (time-limited tokens)</li>
    </ul>
    <p><strong>This is the secure approach!</strong></p>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5007)
