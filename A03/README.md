# A03:2021 - Injection Evidence Case

This example demonstrates SQL and command injection vulnerabilities, which occur when untrusted data is sent to an interpreter as part of a command or query.

## Scenario
A web application implements login functionality using SQL and a file viewing feature using shell commands. In both cases, user input is directly incorporated into queries and commands without proper validation or parameterization, allowing attackers to manipulate the intended behavior.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5003](http://localhost:5003) in your browser.

## Evidence Case: SQL and Command Injection

### SQL Injection Demos
- Visit `/login` and attempt login with normal credentials: username=`alice`, password=`alice123`
- Try a SQL injection attack: username=`alice' --`, password=anything
- The attack bypasses authentication by commenting out the password check in SQL.
- For comparison, try the same attack on the secure version at `/login/safe`
- Similar examples are provided with ORM at `/login/orm_vuln` and `/login/orm_safe`

### Command Injection Demo
- Visit `/cmd_injection` to see a file viewer that uses shell commands.
- Enter normal input like `test.db` to view a file.
- Try command injection using `test.db; whoami` or `test.db; rm -rf /tmp`
- The attack executes arbitrary shell commands by abusing command concatenation.
- For comparison, try the secure version at `/safe_view_file` with the same inputs.

### Example Attack
- SQL Injection: An attacker can bypass authentication or extract sensitive data by manipulating the SQL query structure.
- Command Injection: An attacker can execute arbitrary system commands by breaking out of the intended command context.
- Both vulnerabilities arise from the same root cause: direct incorporation of user input into interpreted contexts.

## Why is this Injection?
- The flaw is in how user input is handled: it becomes part of the command/query syntax rather than being treated as data.
- The application fails to distinguish between trusted code and untrusted data.
- SQL injection exploits this by turning data into SQL syntax.
- Command injection exploits this by escaping the intended command to execute additional commands.
- These vulnerabilities can lead to data theft, modification, or destruction, and in the case of command injection, full system compromise.

## How to Prevent
- Use parameterized queries for database access instead of building dynamic queries:
  - Use prepared statements with bind variables
  - Use ORMs with proper parameterization
  - Avoid dynamic queries entirely where possible
- For command execution:
  - Avoid using shell commands with user input when possible
  - Use built-in language functions instead of shell commands
  - If shell commands are necessary, strictly validate and sanitize inputs
  - Consider allowlists for permitted values rather than trying to detect malicious input
- Input validation should be applied, but is not a complete defense on its own
- Apply the principle of least privilege to database accounts and system permissions

## Example Attack Scenarios
**Scenario #1:** An application uses untrusted data in an SQL call:
```sql
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```
An attacker can modify the 'id' parameter to bypass authentication or extract additional data.

**Scenario #2:** An application naively accepts file paths for a system command:
```python
import os
user_input = request.args.get('filename')
# DANGEROUS: user_input could be 'file.txt; rm -rf /'
os.system(f"cat {user_input}")
```
This allows attackers to execute arbitrary system commands by abusing command syntax.

**Scenario #3:** A web application uses an ORM but still allows raw SQL:
```python
query = "SELECT * FROM products WHERE category = '" + productCategory + "'";
```
Even with ORM usage, raw SQL queries can introduce injection vulnerabilities if not properly parameterized.

---

**This is for educational purposes only. Never use such insecure patterns in production!**

