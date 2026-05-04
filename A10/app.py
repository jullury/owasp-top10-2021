from flask import Flask, render_template_string, request, jsonify
import os
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <h1>Mishandling of Exceptional Conditions Demo</h1>
    <ul>
        <li><a href="/divide?a=10&b=0">Divide by Zero (Insecure)</a></li>
        <li><a href="/file-read?file=nonexistent.txt">Read Non-existent File</a></li>
        <li><a href="/api/users">API with Malformed Requests</a></li>
        <li><a href="/upload">Upload (Crash-prone)</a></li>
        <li><a href="/process?data=test">Process Data (Insecure)</a></li>
        <li><a href="/secure-errors">Secure Error Handling</a></li>
    </ul>
    ''')

@app.route('/divide')
def divide():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        result = a / b
        return f"Result: {result}"
    except Exception as e:
        # VULNERABLE: Exposing full traceback to user
        return render_template_string('''
        <h1>Error Occurred!</h1>
        <h2>Exception Details:</h2>
        <pre>{{ error }}</pre>
        <h2>Traceback:</h2>
        <pre>{{ traceback }}</pre>
        <p><strong>VULNERABLE:</strong> Full error details exposed!</p>
        ''', error=str(e), traceback=traceback.format_exc())

@app.route('/file-read')
def file_read():
    filename = request.args.get('file', '')
    try:
        # VULNERABLE: No input validation, path traversal possible
        with open(filename, 'r') as f:
            content = f.read()
        return f"File content: {content}"
    except Exception as e:
        # VULNERABLE: Reveals file paths and OS details
        return render_template_string('''
        <h1>File Read Error!</h1>
        <p>Failed to read file: {{ filename }}</p>
        <h2>Error:</h2>
        <pre>{{ error }}</pre>
        <h2>Current working directory:</h2>
        <p>{{ cwd }}</p>
        <p><strong>VULNERABLE:</strong> Exposing file system details!</p>
        ''', filename=filename, error=str(e), cwd=os.getcwd())

@app.route('/api/users')
def api_users():
    try:
        # VULNERABLE: No input validation
        user_id = request.args.get('id')
        # Simulate database query that can fail
        if user_id == 'crash':
            raise ValueError("Simulated database connection failed at line 123 in user_service.py")
        return jsonify({"id": user_id, "name": "John Doe"})
    except Exception as e:
        # VULNERABLE: Full exception details in API response
        return render_template_string('''
        <h1>API Error</h1>
        <h2>Exception:</h2>
        <pre>{{ error }}</pre>
        <h2>Stack Trace:</h2>
        <pre>{{ traceback }}</pre>
        <p><strong>VULNERABLE:</strong> API exposing internal details!</p>
        ''', error=str(e), traceback=traceback.format_exc())

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            # VULNERABLE: No file size limit, no proper error handling
            file = request.files['file']
            # Simulate processing that can crash
            if len(file.read()) > 1000000:
                raise MemoryError("File too large, cannot process")
            return "File uploaded successfully"
        except MemoryError as e:
            # VULNERABLE: Exposing internal error details
            return f"Memory Error: {str(e)}\nApplication may be unstable now."
        except Exception as e:
            return f"Unexpected error: {traceback.format_exc()}"
    return render_template_string('''
    <h1>File Upload (Insecure)</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <p><small>No file size limits or proper error handling!</small></p>
    ''')

@app.route('/process')
def process():
    data = request.args.get('data', '')
    try:
        # VULNERABLE: No input validation, can crash on special input
        if data == 'crash':
            raise Exception("Processing failed: invalid state in DataProcessor.process() at line 456")
        result = f"Processed: {data}"
        return result
    except Exception as e:
        # VULNERABLE: Exposing internal processing details
        return render_template_string('''
        <h1>Processing Error</h1>
        <p>Failed to process data.</p>
        <h2>Internal Error Details:</h2>
        <pre>{{ error }}</pre>
        <p><strong>VULNERABLE:</strong> Revealing internal implementation!</p>
        ''', error=str(e))

@app.route('/secure-errors')
def secure_errors():
    return render_template_string('''
    <h1>Secure Error Handling (Best Practices)</h1>
    <h2>What to Do:</h2>
    <ul>
        <li>Show generic error pages (no details to users)</li>
        <li>Log full errors internally for debugging</li>
        <li>Use proper try-catch with graceful fallbacks</li>
        <li>Validate input before processing</li>
        <li>Return appropriate HTTP status codes</li>
        <li>Never expose stack traces to users</li>
        <li>Implement rate limiting for error-prone endpoints</li>
        <li>Test edge cases and failure scenarios</li>
    </ul>
    <h2>Example Secure Error Response:</h2>
    <pre>
    {
        "error": "An error occurred",
        "code": "INTERNAL_ERROR",
        "request_id": "abc-123-def"
    }
    </pre>
    <p><strong>This is the secure approach!</strong></p>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5010)
