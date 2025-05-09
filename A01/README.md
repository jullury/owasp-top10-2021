# A01:2021 - Broken Access Control Evidence Case

This example demonstrates broken access control, which occurs when restrictions on what authenticated users are allowed to do are not properly enforced.

## Scenario
An admin interface is implemented with a missing authorization check that allows any authenticated user (not just administrators) to access sensitive functionality. This is a classic broken access control flaw, as the application fails to verify if the user has the appropriate privileges.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5001](http://localhost:5001) in your browser.

## Evidence Case: Broken Admin Access
- Log in as `alice` (password: `userpass`) - a regular user with no admin privileges.
- Navigate to `/admin` - you should be able to access the admin page even though Alice is not an admin.
- For comparison, try the secure version at `/admin/secure` - access should be denied.
- Log in as `bob` (password: `adminpass`) - an admin user.
- Both `/admin` and `/admin/secure` routes should be accessible to Bob.

### Example Attack
- An attacker who has gained access to a regular user account can directly access administrative functions.
- Simply changing the URL to `/admin` bypasses authorization checks entirely.
- No special tools or techniques are needed - just knowledge of the endpoint's existence.

## Why is this Broken Access Control?
- The flaw is in missing authorization checks: the application authenticates users but fails to verify authorization.
- The code only checks if a user is logged in (`'username' in session`) but not their role or permissions.
- This violates the principle of least privilege, allowing users to perform actions beyond their intended permissions.
- Authentication (proving who you are) is implemented, but authorization (proving what you're allowed to do) is missing.

## How to Prevent
- Deny access by default, except for public resources.
- Implement proper access control checks for each sensitive function, method, and resource.
- Use role-based access control (RBAC) consistently across the application.
- Never rely solely on hiding URLs or API endpoints ("security by obscurity").
- Enforce record ownership - users should only be able to view/modify their own data.
- Disable directory listing and ensure metadata/backup files aren't accessible.
- Log access control failures and alert administrators when appropriate.
- Rate limit API access to minimize harm from automated attack tools.
- Session tokens should be invalidated on the server after logout.

## Example Attack Scenarios
**Scenario #1:** Application uses unverified data in a SQL call that is accessing account information:
```
pstmt = "SELECT * FROM accts WHERE account = ?" 
pstmt.setString(1, request.getParameter("acct"));
```
Attacker modifies the 'acct' parameter in the browser to send any account number they want.

**Scenario #2:** An application uses force browsing (like our example) to access admin endpoints:
```
https://example.com/app/getappinfo
https://example.com/app/admin_getappinfo
```
If unauthenticated users can access either page, it's a flaw. If non-admins can access the admin page, this is also a flaw.

**Scenario #3:** An API lacks proper controls and allows regular users to modify permissions:
```
https://api.example.com/user/423/update_role
```
An attacker could craft a request to this API endpoint to escalate their privileges.

---

**This is for educational purposes only. Never use such insecure patterns in production!**

