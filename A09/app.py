from flask import Flask, render_template_string, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'some-secret-key'

# Insecure "database"
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'alice': {'password': 'alice123', 'role': 'user'}
}

# VULNERABLE: No proper security logging
ACCESS_LOG = []

@app.route('/')
def index():
    return render_template_string('''
    <h1>Security Logging and Alerting Failures Demo</h1>
    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/transfer">Transfer Funds</a></li>
        <li><a href="/admin">Admin Panel</a></li>
        <li><a href="/logs">View Logs (Insecure)</a></li>
        <li><a href="/secure-logging">Secure Logging Info</a></li>
    </ul>
    ''' + ('<p>Logged in as: ' + session.get('username', 'Not logged in') + '</p>' if 'username' in session else ''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: No logging of login attempts
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            # No success logging!
            return redirect(url_for('index'))
        else:
            # VULNERABLE: No failed login logging
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
    <p><small>No logging of attempts - attacks go undetected!</small></p>
    ''')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '0')
        to_account = request.form.get('to_account', '')
        # VULNERABLE: No audit logging for financial transactions
        return render_template_string('''
        <h1>Transfer Complete</h1>
        <p>Transferred $''' + amount + ''' to ''' + to_account + '''</p>
        <a href="/">Back</a>
        <p><small>No audit trail created!</small></p>
        ''')
    
    return render_template_string('''
    <h1>Transfer Funds</h1>
    <form method="POST">
        Amount: $<input type="text" name="amount"><br>
        To Account: <input type="text" name="to_account"><br>
        <input type="submit" value="Transfer">
    </form>
    <p><small>No logging of financial transactions!</small></p>
    ''')

@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # VULNERABLE: No logging of privileged access attempts
    if session.get('role') == 'admin':
        return render_template_string('''
        <h1>Admin Panel</h1>
        <p>Welcome, admin!</p>
        <a href="/">Back</a>
        ''')
    else:
        # VULNERABLE: No alert for unauthorized admin access attempt
        return render_template_string('''
        <h1>Access Denied</h1>
        <p>You don't have permission to access this page.</p>
        <a href="/">Back</a>
        <p><small>No alert triggered for access violation!</small></p>
        ''')

@app.route('/logs')
def logs():
    # VULNERABLE: Basic access log only, no security context
    return render_template_string('''
    <h1>Access Logs (Insecure)</h1>
    <pre>''' + '\n'.join(ACCESS_LOG) + '''</pre>
    <p><small>Only basic access logged - no security events!</small></p>
    <a href="/">Back</a>
    ''', ACCESS_LOG=ACCESS_LOG)

@app.route('/secure-logging')
def secure_logging_info():
    return render_template_string('''
    <h1>Secure Logging Practices</h1>
    <h2>What Should Be Logged:</h2>
    <ul>
        <li>All login attempts (success/failure) with timestamp, IP, user</li>
        <li>Access control failures (401, 403 responses)</li>
        <li>Privileged operations (admin access, config changes)</li>
        <li>Financial transactions with full audit trail</li>
        <li>Input validation failures (potential attack attempts)</li>
        <li>System errors and exceptions with context</li>
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
    <p><strong>This is the secure approach!</strong></p>
    <a href="/">Back</a>
    ''')

@app.before_request
def log_request():
    # VULNERABLE: Only basic access logging, no security context
    ACCESS_LOG.append(f"{datetime.now()}: {request.remote_addr} accessed {request.path}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5009)
