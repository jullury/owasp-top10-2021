from flask import Flask, session, redirect, url_for, request, render_template_string

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Insecure for demo purposes only

users = {
    'alice': {'password': 'userpass', 'role': 'user'},
    'bob': {'password': 'adminpass', 'role': 'admin'}
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
        if user and user['password'] == password:
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
    # BROKEN ACCESS CONTROL: No role check!
    if 'username' in session:
        return f"Welcome to the admin page, {session['username']}! (role: {session['role']})"
    return redirect(url_for('login'))


@app.route('/admin/secure')
def admin_secure():
    if 'username' in session and session['role'] == 'admin':
        return f"Welcome to the admin page, {session['username']}! (role: {session['role']})"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
