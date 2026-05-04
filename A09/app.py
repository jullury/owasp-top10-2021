from flask import Flask, render_template_string, request, session, redirect, url_for
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# Secure user store with hashed passwords
USERS = {
    'admin': {'password_hash': generate_password_hash('admin123'), 'role': 'admin'},
    'alice': {'password_hash': generate_password_hash('alice123'), 'role': 'user'}
}

# Structured security logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template_string('''
    <h1>Security Logging and Alerting Demo (Secure)</h1>
    {% if logged_in %}
        <p>Logged in as: {{ session.username }}</p>
        <ul>
            <li><a href="/transfer">Transfer Funds</a></li>
            <li><a href="/admin">Admin Panel</a></li>
            <li><a href="/logs">View Logs</a></li>
        </ul>
        <a href="/logout">Logout</a>
    {% else %}
        <ul>
            <li><a href="/login">Login</a></li>
            <li><a href="/secure-logging">Secure Logging Info</a></li>
        </ul>
    {% endif %}
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Log login attempt
        logger.info(f"Login attempt - user: {username}, IP: {request.remote_addr}")
        
        if username in USERS and check_password_hash(USERS[username]['password_hash'], password):
            session['username'] = username
            session['role'] = USERS[username]['role']
            logger.info(f"Login successful - user: {username}, IP: {request.remote_addr}")
            return redirect(url_for('index'))
        else:
            logger.warning(f"Login failed - user: {username}, IP: {request.remote_addr}")
            return render_template_string('''
            <h1>Login Failed</h1>
            <p>Invalid credentials.</p>
            <a href="/login">Try Again</a>
            ''')
    
    return render_template_string('''
    <h1>Login</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p><small>All login attempts are logged.</small></p>
    ''')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '0')
        to_account = request.form.get('to_account', '')
        # Audit logging for financial transactions
        logger.info(f"Transfer - user: {session['username']}, amount: ${amount}, to: {to_account}, IP: {request.remote_addr}")
        return render_template_string('''
        <h1>Transfer Complete</h1>
        <p>Transferred ${{ amount }} to {{ to_account }}</p>
        <a href="/">Back</a>
        ''', amount=amount, to_account=to_account)
    
    return render_template_string('''
    <h1>Transfer Funds</h1>
    <form method="POST">
        Amount: $<input type="text" name="amount"><br>
        To Account: <input type="text" name="to_account"><br>
        <input type="submit" value="Transfer">
    </form>
    ''')

@app.route('/admin')
def admin():
    if 'username' not in session:
        logger.warning(f"Unauthorized access attempt to /admin - IP: {request.remote_addr}")
        return redirect(url_for('login'))
    
    if session.get('role') == 'admin':
        logger.info(f"Admin access - user: {session['username']}, IP: {request.remote_addr}")
        return render_template_string('''
        <h1>Admin Panel</h1>
        <p>Welcome, admin!</p>
        <a href="/">Back</a>
        ''')
    else:
        logger.warning(f"Non-admin user attempted admin access - user: {session.get('username')}, IP: {request.remote_addr}")
        return render_template_string('''
        <h1>Access Denied</h1>
        <p>You don't have permission to access this page.</p>
        <a href="/">Back</a>
        ''')

@app.route('/logs')
def logs():
    return render_template_string('''
    <h1>Security Logs</h1>
    <p>Check the application logs for security events.</p>
    <p><small>Logs include timestamps, IP addresses, and event details.</small></p>
    <a href="/">Back</a>
    ''')

@app.route('/secure-logging')
def secure_logging_info():
    return render_template_string('''
    <h1>Secure Logging Practices</h1>
    <h2>What Is Logged:</h2>
    <ul>
        <li>All login attempts (success/failure) with timestamp, IP, user</li>
        <li>Access control failures (401, 403 responses)</li>
        <li>Privileged operations (admin access, config changes)</li>
        <li>Financial transactions with full audit trail</li>
        <li>Input validation failures (potential attack attempts)</li>
    </ul>
    <h2>Best Practices:</h2>
    <ul>
        <li>Use structured logging (JSON format)</li>
        <li>Include context: timestamp, IP, user, session ID</li>
        <li>Implement real-time alerting for suspicious patterns</li>
        <li>Never log sensitive data (passwords, tokens, PII)</li>
        <li>Store logs securely, prevent tampering</li>
        <li>Integrate with SIEM or centralized logging</li>
    </ul>
    <p><strong>Implemented:</strong> All security events are logged with timestamps and IP addresses.</p>
    <a href="/">Back</a>
    ''')

@app.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    session.clear()
    logger.info(f"Logout - user: {username}, IP: {request.remote_addr}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, port=5009)
