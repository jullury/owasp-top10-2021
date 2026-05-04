from flask import Flask, render_template_string, jsonify, request
import requests
import subprocess
import json

app = Flask(__name__)

# Vulnerable dependency list (some with known CVEs)
DEPENDENCIES = [
    {"name": "flask", "version": "2.3.2", "vulnerable": False},
    {"name": "requests", "version": "2.28.1", "vulnerable": False},
    {"name": "numpy", "version": "1.23.0", "vulnerable": True, "cve": "CVE-2021-41495"},
    {"name": "django", "version": "3.2.0", "vulnerable": True, "cve": "CVE-2021-28699"}
]

@app.route('/')
def index():
    return render_template_string('''
    <h1>Software Supply Chain Failures Demo</h1>
    <ul>
        <li><a href="/dependencies">View All Dependencies</a></li>
        <li><a href="/vulnerable-deps">View Vulnerable Dependencies</a></li>
        <li><a href="/integrity-check">Check Package Integrity</a></li>
        <li><a href="/install-package">Install Package (Insecure)</a></li>
        <li><a href="/secure-deps">Secure Dependency Management</a></li>
    </ul>
    ''')

@app.route('/dependencies')
def dependencies():
    return render_template_string('''
    <h1>Application Dependencies</h1>
    <table border="1">
        <tr><th>Package</th><th>Version</th><th>Status</th></tr>
        {% for dep in deps %}
        <tr>
            <td>{{ dep.name }}</td>
            <td>{{ dep.version }}</td>
            <td>{% if dep.vulnerable %}<span style="color:red">Vulnerable</span>{% else %}<span style="color:green">Safe</span>{% endif %}</td>
        </tr>
        {% endfor %}
    </table>
    <br>
    <a href="/">Back to Home</a>
    ''', deps=DEPENDENCIES)

@app.route('/vulnerable-deps')
def vulnerable_deps():
    vuln_deps = [d for d in DEPENDENCIES if d.get('vulnerable')]
    return render_template_string('''
    <h1>Vulnerable Dependencies</h1>
    <p>These dependencies have known CVEs:</p>
    <ul>
        {% for dep in vuln_deps %}
        <li>{{ dep.name }} v{{ dep.version }} - {{ dep.cve }}</li>
        {% endfor %}
    </ul>
    <p><strong>Risk:</strong> Attackers can exploit these known vulnerabilities!</p>
    <a href="/">Back to Home</a>
    ''')

@app.route('/integrity-check')
def integrity_check():
    return render_template_string('''
    <h1>Package Integrity Check (Insecure)</h1>
    <p>This application does not verify package integrity!</p>
    <p>Packages are installed without checking hashes or signatures.</p>
    <p><strong>Risk:</strong> Compromised packages can be injected into the supply chain.</p>
    <a href="/">Back to Home</a>
    ''')

@app.route('/install-package')
def install_package():
    package = request.args.get('package', 'requests')
    # VULNERABLE: Directly installing package without verification
    try:
        result = subprocess.run(['pip', 'install', package], capture_output=True, text=True)
        return render_template_string('''
        <h1>Package Installation</h1>
        <p>Installing: {{ package }}</p>
        <pre>{{ output }}</pre>
        <p><strong>Warning:</strong> No integrity verification performed!</p>
        <a href="/">Back to Home</a>
        ''', package=package, output=result.stdout)
    except Exception as e:
        return str(e)

@app.route('/secure-deps')
def secure_deps():
    return render_template_string('''
    <h1>Secure Dependency Management</h1>
    <h2>Best Practices:</h2>
    <ul>
        <li>Pin exact versions in requirements.txt</li>
        <li>Use hash verification (pip install --hash)</li>
        <li>Maintain SBOM (Software Bill of Materials)</li>
        <li>Regularly scan for vulnerabilities</li>
        <li>Use private repositories for internal packages</li>
        <li>Implement CI/CD security checks</li>
    </ul>
    <p><strong>This is the secure approach!</strong></p>
    <a href="/">Back to Home</a>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5003)
