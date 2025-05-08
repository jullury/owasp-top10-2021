# A03: Injection

This example demonstrates SQL Injection vulnerabilities and how to prevent them, as described in the [OWASP Top 10 A03:2021 - Injection](https://owasp.org/Top10/A03_2021-Injection/).

- Vulnerable and secure login forms are available side by side for comparison.
- The app runs by default on port 5003.

## How it works
- The app uses a SQLite database with two users: `alice` and `bob`.
- The `/login` route is vulnerable to SQL injection.
- The `/login/safe` route uses parameterized queries to prevent injection.
- The `/login/orm_vuln` route demonstrates ORM-based injection (vulnerable).
- The `/login/orm_safe` route demonstrates safe ORM-based querying (parameterized).
- The `/cmd_injection` route demonstrates a realistic command injection vulnerability via a 'View File' feature that unsafely passes user input to a shell command.
- The `/safe_view_file` route demonstrates a safe file viewer that prevents command injection by validating input and not using the shell.

## How to use
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Try logging in with normal and malicious input on all four login forms:
   - `/login` : Vulnerable SQL Injection (classic)
   - `/login/safe` : Safe SQL (parameterized)
   - `/login/orm_vuln` : Vulnerable ORM Injection
   - `/login/orm_safe` : Safe ORM (parameterized)
   - `/cmd_injection` : View File (Command Injection Demo, vulnerable)
    - Example command injection: filename = `test.db; whoami` or `test.db; rm -rf /tmp`
   - `/safe_view_file` : Safe File Viewer (prevents command injection)
    - Example safe usage: filename = `testdb` (must be alphanumeric and in the current directory)
   - Example SQL injection: username = `alice' --` , password = anything
   - Example ORM injection: username = `' OR '1'='1`

## Vulnerability
The `/login` route directly interpolates user input into SQL queries, allowing attackers to bypass authentication with crafted input.

## How to Fix
- Always use parameterized queries or ORM methods to interact with databases.
- Never concatenate or interpolate user input directly into SQL statements.
- Validate and sanitize user input as an additional precaution.

### Preventing Command Injection
- **Never use user input directly in system commands.**
- Use built-in APIs (like Python's file I/O) instead of shell commands for operations like file reading.
- If you must use user input, strictly validate it (e.g., allow only alphanumeric filenames).
- **Safe Example:** See `/safe_view_file` endpoint for a secure implementation.

## When is an Application Vulnerable to Injection?
An application is vulnerable to injection attacks when:

- **User-supplied data is not validated, filtered, or sanitized by the application.**
  - Example: Accepting user input and passing it directly to the database or command line.
- **Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter.**
  - Example: Building SQL queries using string concatenation with user input.
- **Hostile data is used within object-relational mapping (ORM) search parameters to extract additional, sensitive records.**
  - Example: Passing user input directly to ORM filter methods without validation.
    This can lead to injection if the ORM does not parameterize the query internally or if raw SQL is used.
- **Hostile data is directly used or concatenated. The SQL or command contains the structure and malicious data in dynamic queries, commands, or stored procedures.**
  - Example: Using user input in system commands or stored procedures without sanitization.

    ```python
    import os
    user_input = request.args.get('filename')
    # DANGEROUS: user_input could be something like 'foo.txt; rm -rf /'
    os.system(f"cat {user_input}")
    ```
    This can allow attackers to execute arbitrary system commands if input is not sanitized.
