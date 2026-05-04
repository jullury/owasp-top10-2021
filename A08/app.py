import json
import base64
import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <h1>Software or Data Integrity Failures Demo (Secure)</h1>
    <ul>
        <li><a href="/serialize">Secure Serialization (JSON)</a></li>
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
        # SECURE: Using JSON for serialization (not pickle)
        json_data = json.dumps(user_data)
        encoded = base64.b64encode(json_data.encode()).decode()
        return render_template_string('''
        <h1>Serialized Data (Secure)</h1>
        <p>User data serialized using JSON (safe):</p>
        <textarea rows="10" cols="80">{{ data }}</textarea>
        <p><strong>Secure:</strong> JSON serialization is safe for untrusted data.</p>
        <a href="/">Back</a>
        ''', data=encoded)
    return render_template_string('''
    <h1>Serialize Data (Secure)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Role: <input type="text" name="role"><br>
        <input type="submit" value="Serialize">
    </form>
    <p><small>Uses JSON - safe alternative to pickle.</small></p>
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
    <p><strong>Security improvements made:</strong></p>
    <ul>
        <li>Pickle replaced with JSON serialization</li>
        <li>exec() removed - no dynamic code execution</li>
        <li>Vulnerable CI/CD demo route removed</li>
    </ul>
    <p><strong>This is the secure approach!</strong></p>
    <a href="/">Back</a>
    ''')

if __name__ == '__main__':
    app.run(debug=False, port=5008)
