# A05:2021 - Security Misconfiguration Evidence Case

This example demonstrates a security misconfiguration vulnerability based on OWASP's Example Attack Scenario #2.

## Scenario
Directory listing is not disabled on the server. An attacker discovers they can simply list directories. The attacker finds and downloads the compiled Java classes, which they decompile and reverse engineer to view the code. The attacker then finds a severe access control flaw in the application.

## How to Run

### Option 1: Using Flask (Python)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5005](http://localhost:5005) in your browser.

### Option 2: Using Docker with Apache (for .htaccess testing)
1. Build the Docker image:
   ```bash
   cd A05
   docker build -t a05-apache .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8080:80 --name a05-apache-container a05-apache
   ```
3. Visit [http://localhost:8080](http://localhost:8080) in your browser.
4. When finished, stop the container:
   ```bash
   docker stop a05-apache-container
   docker rm a05-apache-container
   ```

## Evidence Case: Directory Listing Security Misconfiguration

### Flask Implementation
- Go to the application's main page
- Click on the "Browse Directory Listing" button or navigate to `/browse/` URL
- Notice that the server allows directory listing, exposing sensitive files
- You can see all files within the directory, including ones that should not be accessible:
  - `AdminController.java` - Source code with hard-coded credentials
  - `classes/` - Directory with compiled Java classes
  - `config.properties` - Configuration file with sensitive information
  - `.htaccess` - Misconfigured server settings
- Use the "Download and Decompile" link or navigate to `/download-and-decompile` to see how exposed compiled classes can be decompiled
- The decompiled code reveals security flaws like hard-coded credentials and internal API endpoints

### Apache Implementation (Docker)
- The Docker container sets up Apache with intentionally misconfigured `.htaccess`
- Navigate to http://localhost:8080 to see the directory listing due to `Options +Indexes` setting
- The `.htaccess` file incorrectly allows access to sensitive file types like `.class`, `.properties`, and `.conf`
- This demonstrates how improper server configurations can expose sensitive files

### Example Attack
- An attacker browses to different directories on the server
- The attacker discovers that directory listing is enabled
- They download compiled Java classes from an exposed directory
- By decompiling these classes, they extract sensitive information like:
  - Hard-coded credentials
  - Internal API endpoints
  - Access control implementation flaws

## Why is this a Security Misconfiguration?
- Directory listing should be disabled by default in production environments
- Sensitive files like compiled code should not be stored in publicly accessible locations
- The application exposes unnecessary information that helps attackers map the system
- Proper server hardening would prevent this type of information disclosure

## How to Prevent
- Implement a repeatable hardening process that makes it fast and easy to deploy properly locked down environments
- Deploy a minimal platform without unnecessary features, components, documentation, and samples
- Review and update configurations for all security notes, updates, and patches as part of the patch management process
- Use a segmented application architecture that provides effective and secure separation between components
- Send security directives to clients, such as Security Headers
- Automate verification of configurations across all environments
- Set up an automated process to verify effectiveness of configurations and settings in all environments
- Disable directory listing on web servers
- Store sensitive code and files outside web-accessible directories

## Example Attack Scenarios
**Scenario #1:** The application server comes with sample applications that are not removed from the production server. These sample applications have known security flaws attackers use to compromise the server. Suppose one of these applications is the admin console, and default accounts weren't changed. In that case, the attacker logs in with default passwords and takes over.

**Scenario #2:** Directory listing is not disabled on the server. An attacker discovers they can simply list directories. The attacker finds and downloads the compiled Java classes, which they decompile and reverse engineer to view the code. The attacker then finds a severe access control flaw in the application.

**Scenario #3:** The application server's configuration allows detailed error messages, e.g., stack traces, to be returned to users. This potentially exposes sensitive information or underlying flaws such as component versions that are known to be vulnerable.

**Scenario #4:** A cloud service provider has default sharing permissions open to the Internet by other CSP users. This allows sensitive data stored within cloud storage to be accessed.

---

**This is for educational purposes only. Never leave such insecure configurations in production!**
