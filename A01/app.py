from flask import Flask, session, redirect, url_for, request, render_template_string
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

users = {
    'alice': {'password_hash': generate_password_hash('userpass'), 'role': 'user'},
    'bob': {'password_hash': generate_password_hash('adminpass'), 'role': 'admin'}
}

@app.route('/')
def home():
    if 'username' in session:
        return f"Logged in as {session['username']} ({session['role']}) <a href='/logout'>Logout</a><br><a href='/admin'>Admin Page</a>"
    return "<a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('home'))
        return '''Invalid credentials<br><a href='/login'>Try again</a>'''
    
    return '''
        <form method='post'>
            Username: <input name='username'><br>
            Password: <input name='password' type='password'><br>
            <input type='submit' value='Login'>
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if 'username' in session and session.get('role') == 'admin':
        return f"Welcome to the admin page, {session['username']}! (role: {session['role']})"
    return redirect(url_for('login'))


@app.route('/admin/secure')
def admin_secure():
    if 'username' in session and session['role'] == 'admin':
        return f"Welcome to the admin page, {session['username']}! (role: {session['role']})"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5001, debug=False)
