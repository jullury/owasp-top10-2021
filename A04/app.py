from flask import Flask, request, render_template_string
import os
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# Secure user store with hashed passwords and encrypted sensitive data
FERNET_KEY = os.environ.get('FERNET_KEY')
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

users = {
    'alice': {
        'password_hash': generate_password_hash('password123'),
        'ssn_encrypted': fernet.encrypt(b'123-45-6789'),
    }
}

@app.route('/')
def index():
    return '''
        <a href="/profile?user=alice">View Alice Profile (Secure)</a><br>
        <a href="/security-info">Security Practices</a>
    '''

@app.route('/profile')
def profile():
    username = request.args.get('user')
    user = users.get(username)
    if not user:
        return 'User not found', 404
    ssn_encrypted_b64 = user['ssn_encrypted'].decode()
    return render_template_string('''
        <h2>Profile for {{username}}</h2>
        <p>Password is securely hashed (not displayed)</p>
        <p>SSN is encrypted and not exposed to users</p>
        <p><small>Encrypted value (for demo): {{ssn_encrypted_b64}}</small></p>
    ''', username=username, ssn_encrypted_b64=ssn_encrypted_b64)

@app.route('/security-info')
def security_info():
    return render_template_string('''
    <h2>Security Practices Implemented</h2>
    <ul>
        <li>Passwords are hashed using werkzeug's generate_password_hash</li>
        <li>Sensitive data (SSN) is encrypted using Fernet symmetric encryption</li>
        <li>Secret key is loaded from environment variable or securely generated</li>
        <li>Debug mode is disabled</li>
    </ul>
    <a href="/">Back</a>
    ''')

if __name__ == '__main__':
    app.run(port=5002, debug=False)
