from flask import Flask, render_template_string, request, jsonify, abort
import os
import logging
import uuid

app = Flask(__name__)

# Configure logging for internal error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <h1>Secure Error Handling Demo</h1>
    <ul>
        <li><a href="/divide?a=10&b=2">Divide Numbers (Secure)</a></li>
        <li><a href="/api/users">API with Error Handling</a></li>
        <li><a href="/secure-errors">Secure Error Handling Practices</a></li>
    </ul>
    ''')

@app.route('/divide')
def divide():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        if b == 0:
            return render_template_string('''
            <h1>Error</h1>
            <p>Cannot divide by zero. Please provide a non-zero value for b.</p>
            <a href="/">Back</a>
            '''), 400
        result = a / b
        return f"Result: {result}"
    except ValueError:
        return render_template_string('''
        <h1>Invalid Input</h1>
        <p>Please provide valid numbers for a and b.</p>
        <a href="/">Back</a>
        '''), 400
    except Exception as e:
        logger.error(f"Unexpected error in divide: {str(e)}")
        return render_template_string('''
        <h1>An Error Occurred</h1>
        <p>Please try again later.</p>
        <a href="/">Back</a>
        '''), 500

@app.route('/file-read')
def file_read():
    filename = request.args.get('file', '')
    if not filename or '..' in filename or filename.startswith('/'):
        return render_template_string('''
        <h1>Invalid Request</h1>
        <p>The requested file cannot be accessed.</p>
        <a href="/">Back</a>
        '''), 400
    try:
        safe_path = os.path.join(os.getcwd(), 'safe_files', filename)
        if not os.path.dirname(safe_path).endswith('safe_files'):
            abort(400)
        if not os.path.isfile(safe_path):
            return render_template_string('''
            <h1>File Not Found</h1>
            <p>The requested file does not exist.</p>
            <a href="/">Back</a>
            '''), 404
        with open(safe_path, 'r') as f:
            content = f.read()
        return f"File content: {content}"
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        return render_template_string('''
        <h1>An Error Occurred</h1>
        <p>Unable to read the requested file.</p>
        <a href="/">Back</a>
        '''), 500

@app.route('/api/users')
def api_users():
    try:
        user_id = request.args.get('id')
        if not user_id:
            return jsonify({"error": "Missing user ID", "code": "INVALID_REQUEST"}), 400
        # Simulate database query
        if user_id == 'crash':
            logger.error(f"Simulated database error for user_id: {user_id}")
            return jsonify({"error": "An error occurred", "code": "INTERNAL_ERROR", "request_id": str(uuid.uuid4())}), 500
        return jsonify({"id": user_id, "name": "John Doe"})
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({"error": "An error occurred", "code": "INTERNAL_ERROR", "request_id": str(uuid.uuid4())}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template_string('''
                <h1>Error</h1>
                <p>No file provided.</p>
                <a href="/">Back</a>
                '''), 400
            file = request.files['file']
            if file.content_length and file.content_length > 5000000:
                return render_template_string('''
                <h1>File Too Large</h1>
                <p>Maximum file size is 5MB.</p>
                <a href="/">Back</a>
                '''), 400
            return "File uploaded successfully"
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return render_template_string('''
            <h1>Upload Failed</h1>
            <p>Unable to process the file. Please try again.</p>
            <a href="/">Back</a>
            '''), 500
    return render_template_string('''
    <h1>File Upload</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <p><small>Maximum file size: 5MB.</small></p>
    ''')

@app.route('/process')
def process():
    data = request.args.get('data', '')
    try:
        if not data:
            return render_template_string('''
            <h1>Invalid Input</h1>
            <p>No data provided for processing.</p>
            <a href="/">Back</a>
            '''), 400
        if len(data) > 1000:
            return render_template_string('''
            <h1>Input Too Large</h1>
            <p>Data exceeds maximum allowed size.</p>
            <a href="/">Back</a>
            '''), 400
        result = f"Processed: {data}"
        return result
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return render_template_string('''
        <h1>Processing Error</h1>
        <p>Unable to process the data. Please try again.</p>
        <a href="/">Back</a>
        '''), 500

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
    <a href="/">Back</a>
    ''')

if __name__ == '__main__':
    app.run(debug=False, port=5010)
