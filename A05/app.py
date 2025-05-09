"""
A05:2021 - Security Misconfiguration Evidence Case
This Flask app demonstrates a security misconfiguration vulnerability based on OWASP Scenario #2:

'Directory listing is not disabled on the server. An attacker discovers they can simply list directories. 
The attacker finds and downloads the compiled Java classes, which they decompile and reverse engineer 
to view the code. The attacker then finds a severe access control flaw in the application.'

This example simulates a misconfigured web server that allows directory listing,
exposing sensitive compiled files that shouldn't be accessible.
"""
from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for, abort, send_file
import os
import time
import datetime
import mimetypes

app = Flask(__name__)

# Configure static folder but we'll handle directory browsing manually
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.static_url_path = '/static'

# Path to the static directory with demo files
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
CLASSES_DIR = os.path.join(STATIC_DIR, 'classes')

# Ensure directories exist
os.makedirs(CLASSES_DIR, exist_ok=True)

# Path to compiled Java class file (already created externally)
COMPILED_JAVA_CLASS = os.path.join(CLASSES_DIR, 'AdminController.class')

# Path to "decompiled" Java source code (already created externally)
DECOMPILED_JAVA = os.path.join(STATIC_DIR, 'AdminController.java')

# Path to the sensitive configuration file (already created externally)
CONFIG_FILE = os.path.join(STATIC_DIR, 'config.properties')

# Path to the .htaccess file (already created externally)
HTACCESS_FILE = os.path.join(STATIC_DIR, '.htaccess')

# Function to format file size for display
def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <title>A05:2021 - Security Misconfiguration Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 5px; }
            h1 { color: #d9534f; }
            h2 { color: #333; }
            .warning { background-color: #fcf8e3; border-left: 4px solid #f0ad4e; padding: 10px; margin: 15px 0; }
            .danger { background-color: #f2dede; border-left: 4px solid #d9534f; padding: 10px; margin: 15px 0; }
            code { background-color: #f1f1f1; padding: 2px 4px; border-radius: 3px; }
            pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
            .button { display: inline-block; padding: 8px 16px; margin: 5px 0; background-color: #5bc0de; color: white; text-decoration: none; border-radius: 3px; }
            .button:hover { background-color: #46b8da; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>A05:2021 - Security Misconfiguration Evidence Case</h1>
            
            <div class="warning">
                <strong>Educational Purpose:</strong> This application demonstrates security misconfiguration vulnerabilities. DO NOT use these practices in production environments.
            </div>
            
            <h2>What is Security Misconfiguration?</h2>
            <p>
                Security Misconfiguration happens when security settings are not properly defined, implemented, or maintained.
                It can occur at any level of the application stack, including the network services, platform, web server, 
                application server, database, frameworks, custom code, and more.
            </p>
            
            <h2>Demo Scenario</h2>
            <p>
                This application demonstrates a common security misconfiguration: <strong>directory listing enabled on the server</strong>.
                When directory listing is enabled, attackers can browse the contents of directories on the server, potentially 
                discovering and accessing sensitive files.
            </p>
            
            <div class="danger">
                <strong>OWASP Scenario #2:</strong> Directory listing is not disabled on the server. An attacker discovers they can simply list directories. 
                The attacker finds and downloads the compiled Java classes, which they decompile and reverse engineer to view the code. 
                The attacker then finds a severe access control flaw in the application.
            </div>
            
            <h2>Try the Attack Yourself</h2>
            <p>
                <a href="/browse/" class="button">Browse Directory Listing</a>
            </p>
            <p>
                Notice how you can see all files in the directory, including:
                <ul>
                    <li>Compiled Java classes (that should never be publicly accessible)</li>
                    <li>Configuration files with sensitive information</li>
                    <li>Server configuration files like .htaccess</li>
                </ul>
            </p>
            
            <p>
                <a href="/download-and-decompile" class="button">Download Class File</a> - Simulates an attacker downloading and decompiling a Java class
            </p>
            
            <h2>The Security Flaws</h2>
            <p>This demo shows multiple security misconfigurations:</p>
            <ol>
                <li><strong>Directory Listing Enabled</strong> - Allows attackers to browse directory contents</li>
                <li><strong>Sensitive Files Exposed</strong> - Configuration files with credentials are accessible</li>
                <li><strong>Improper Access Controls</strong> - .htaccess file is misconfigured</li>
                <li><strong>Unsafe Defaults</strong> - The server uses unsafe default configurations</li>
            </ol>
            
            <h2>How to Fix</h2>
            <p>To fix these issues:</p>
            <ul>
                <li>Disable directory listing (Options -Indexes in Apache)</li>
                <li>Move sensitive files outside the web root</li>
                <li>Implement proper access controls</li>
                <li>Use web server security headers</li>
                <li>Configure proper file permissions</li>
                <li>Remove unnecessary files from production</li>
                <li>Implement a secure development lifecycle with proper hardening</li>
            </ul>
        </div>
    </body>
    </html>
    ''')

# Create a special route for browsing directories that overrides Flask's default behavior
@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse_directories(path=''):
    """
    This route intentionally allows directory listing, demonstrating a security misconfiguration.
    Instead of blocking directory browsing (which is the secure approach), it explicitly enables it.
    """
    # Map the path to the static directory
    if path:
        target_path = os.path.join(STATIC_DIR, path)
    else:
        target_path = STATIC_DIR
        
    print(f"Browsing path: '{path}'")
    print(f"Target directory: '{target_path}'")
    
    # Handle files - serve them directly
    if os.path.isfile(target_path):
        return send_file(target_path)
        
    # Handle directories - show listing (this is the security misconfiguration)
    if os.path.isdir(target_path):
        # Redirect to add trailing slash if missing (for consistent URLs)
        if not request.path.endswith('/') and path:
            return redirect(request.path + '/')
            
        try:
            items = os.listdir(target_path)
            items.sort()
        except Exception as e:
            return f"<h1>Error</h1><p>Could not access directory: {e}</p>", 500
            
        # Build parent directory link
        parent_link = ""
        if path:
            parent_parts = path.split('/')
            if len(parent_parts) > 1:
                parent_path = '/'.join(parent_parts[:-1])
                parent_link = f"<a href='/browse/{parent_path}/'>← Up to parent directory</a>"
            else:
                parent_link = f"<a href='/browse/'>← Back to root directory</a>"
                
        # Current path for display
        display_path = f"/static/{path}" if path else "/static"
        
        # Format the directory listing as HTML
        listing = f"""
        <html>
        <head>
            <title>Directory listing for {display_path}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                th {{ background-color: #f2f2f2; }}
                .back {{ margin-bottom: 20px; }}
                .warning {{ background-color: #ffe6e6; padding: 10px; border-left: 4px solid #ff5252; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="warning">
                <strong>Security Misconfiguration:</strong> Directory listing is enabled, allowing attackers to browse directory contents. This should be disabled in production.
            </div>
            
            <h2>Directory listing for: {display_path}</h2>
            
            <div class="back">
                <a href="/">← Back to main page</a>
                <br>{parent_link}
            </div>
            
            <table>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Size</th>
                    <th>Last Modified</th>
                </tr>
        """
        
        # Process directories first, then files
        directories = []
        files = []
        
        for item in items:
            item_path = os.path.join(target_path, item)
            
            # Create the URL path for the item
            if path:
                item_url = f"/browse/{path}/{item}" if not path.endswith('/') else f"/browse/{path}{item}"
            else:
                item_url = f"/browse/{item}"
            
            # Get file information
            stat = os.stat(item_path)
            size = format_size(stat.st_size)
            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Add to appropriate list based on type
            if os.path.isdir(item_path):
                directories.append(f"""
                <tr>
                    <td><a href="{item_url}/"><b>{item}/</b></a></td>
                    <td>Directory</td>
                    <td>-</td>
                    <td>{mod_time}</td>
                </tr>""")
            else:
                # Determine file type based on extension
                ext = os.path.splitext(item)[1].lower()
                if ext == '.class':
                    file_type = "Java Compiled Class"
                elif ext == '.java':
                    file_type = "Java Source"
                elif ext == '.properties':
                    file_type = "Properties Config"
                elif item.startswith('.ht'):
                    file_type = "Server Config"
                else:
                    file_type = "File"
                
                files.append(f"""
                <tr>
                    <td><a href="{item_url}">{item}</a></td>
                    <td>{file_type}</td>
                    <td>{size}</td>
                    <td>{mod_time}</td>
                </tr>""")
                
        # Combine everything
        listing += "".join(directories) + "".join(files)
        listing += """
            </table>
            
            <div style="margin-top: 20px; padding: 10px; background-color: #f8f8f8; border-left: 4px solid #5bc0de;">
                <h3>Security Note</h3>
                <p>This server has directory listing enabled, which is a security misconfiguration.</p>
                <p>In a properly secured server, this directory would not be accessible to users.</p>
            </div>
        </body>
        </html>
        """
        
        return listing
    
    # If path doesn't exist, return 404
    return f"<h1>404 Not Found</h1><p>The requested resource was not found on this server: {filename}</p>", 404

@app.route('/download-and-decompile')
def decompile_demo():
    """
    This route simulates an attacker downloading a compiled class file and decompiling it
    to discover security flaws in the code.
    """
    try:
        with open(DECOMPILED_JAVA, 'r') as f:
            decompiled_source = f.read()
    except Exception as e:
        return f"<h1>Error</h1><p>Could not read decompiled source: {e}</p>", 500
    
    return render_template_string('''
    <html>
    <head>
        <title>Class Decompilation - Security Misconfiguration</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 5px; }
            h1, h2 { color: #d9534f; }
            .alert { background-color: #f2dede; border-left: 4px solid #d9534f; padding: 10px; margin: 15px 0; }
            .steps { background-color: #dff0d8; border-left: 4px solid #5cb85c; padding: 10px; margin: 15px 0; }
            pre { background-color: #2d2d2d; color: #f9f9f9; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 14px; }
            .highlight { background-color: #ff6b6b; color: white; padding: 0 3px; }
            .button { display: inline-block; padding: 8px 16px; margin: 5px 0; background-color: #5bc0de; color: white; text-decoration: none; border-radius: 3px; }
            .button:hover { background-color: #46b8da; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Security Misconfiguration Exploit: Class Decompilation</h1>
            
            <div class="alert">
                <strong>Warning:</strong> This demonstrates how an attacker can exploit security misconfigurations to 
                discover application vulnerabilities. Do not use these practices in real applications.
            </div>
            
            <h2>Attack Scenario</h2>
            <div class="steps">
                <h3>Steps the Attacker Followed:</h3>
                <ol>
                    <li>Discovered that directory listing was enabled on the server</li>
                    <li>Found compiled Java class files in the <code>/static/classes</code> directory</li>
                    <li>Downloaded the <code>AdminController.class</code> file</li>
                    <li>Used a Java decompiler tool (like JAD, CFR, or Procyon) to decompile the class</li>
                    <li>Analyzed the decompiled source code and found severe security flaws</li>
                </ol>
            </div>
            
            <h2>Decompiled Source Code</h2>
            <p>Below is the decompiled Java source code that reveals significant security flaws:</p>
            
            <pre><code>{{ decompiled_source }}</code></pre>
            
            <h2>Security Flaws Exposed</h2>
            <p>The decompiled code reveals several critical security vulnerabilities:</p>
            <ul>
                <li><strong>Hardcoded credentials</strong> - Admin username and password are hardcoded in the source</li>
                <li><strong>Improper access control</strong> - <code>isAuthorized()</code> method only checks the role parameter without proper validation</li>
                <li><strong>Exposed API Keys</strong> - Sensitive API endpoints and keys are included in the code</li>
                <li><strong>Developer comments</strong> - TODO comments reveal sensitive information about the application architecture</li>
            </ul>
            
            <h2>Impact</h2>
            <p>
                With this information, an attacker could:
                <ul>
                    <li>Log in as an administrator using the hardcoded credentials</li>
                    <li>Bypass access control by manipulating the role parameter</li>
                    <li>Access internal API endpoints using the exposed keys</li>
                    <li>Gain deep understanding of the application's internal structure</li>
                </ul>
            </p>
            
            <p>
                <a href="/" class="button">Back to Home</a>
                <a href="/static" class="button">Back to Directory Listing</a>
            </p>
        </div>
    </body>
    </html>
    ''', decompiled_source=decompiled_source)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
