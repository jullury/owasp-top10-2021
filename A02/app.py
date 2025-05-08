from flask import Flask, request, render_template_string
import base64

app = Flask(__name__)

# BAD PRACTICE: Hardcoded secret key and storing sensitive data in plaintext
SECRET_KEY = '12345'  # Weak, hardcoded key

users = {
    'alice': {
        'password': 'password123',  # BAD: Plaintext password
        'ssn': '123-45-6789',      # Sensitive data
    }
}

from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os

@app.route('/')
def index():
    return '''
        <a href="/bad_profile?user=alice">View Alice Profile (Vulnerable)</a><br>
        <a href="/good_profile?user=alice">View Alice Profile (Best Practice)</a>
    '''

@app.route('/bad_profile')
def bad_profile():
    username = request.args.get('user')
    user = users.get(username)
    if not user:
        return 'User not found', 404
    # BAD: Encode sensitive data with base64 instead of encryption
    encoded_ssn = base64.b64encode(user['ssn'].encode()).decode()
    return render_template_string('''
        <h2>Profile for {{username}}</h2>
        <p>Password: {{password}}</p>
        <p>SSN (base64-encoded): {{encoded_ssn}}</p>
        <br><a href="/decode?data={{encoded_ssn}}">Decode SSN</a>
    ''', username=username, password=user['password'], encoded_ssn=encoded_ssn)

# Best Practice Example
FERNET_KEY = os.environ.get('FERNET_KEY')
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)
users_good = {
    'alice': {
        'password_hash': generate_password_hash('password123'),
        'ssn_encrypted': fernet.encrypt(b'123-45-6789'),
    }
}

@app.route('/good_profile')
def good_profile():
    username = request.args.get('user')
    user = users_good.get(username)
    if not user:
        return 'User not found', 404
    ssn_encrypted_b64 = user['ssn_encrypted'].decode()
    return render_template_string('''
        <h2>Profile for {{username}}</h2>
        <p>Password Hash: {{password_hash}}</p>
        <p>SSN (encrypted): {{ssn_encrypted_b64}}</p>
    ''', username=username, password_hash=user['password_hash'], ssn_encrypted_b64=ssn_encrypted_b64)

@app.route('/decode')
def decode():
    data = request.args.get('data')
    # BAD: Anyone can decode sensitive data
    try:
        decoded = base64.b64decode(data).decode()
    except Exception:
        decoded = 'Invalid data.'
    return f"Decoded SSN: {decoded}"

if __name__ == '__main__':
    app.run(port=5002, debug=True)
