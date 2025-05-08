# A01: Broken Access Control

This example demonstrates both insecure and secure (best practice) implementations of access control in a Flask app.

- Vulnerable and secure routes are available side by side for comparison.
- The app runs by default on port 5001.

This simple Flask app demonstrates the OWASP Top 10 A01:2021 - Broken Access Control vulnerability.

## How it works
- There are two users: `alice` (user) and `bob` (admin).
- The `/admin` page should only be accessible to admins, but due to missing role checks, any logged-in user can access it.

## How to use
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Log in as `alice` (userpass) and try to access `/admin`.
4. Log in as `bob` (adminpass) and try to access `/admin`.

## Vulnerability
The app lacks proper access control checks on the `/admin` route. Any authenticated user can access the admin page, demonstrating Broken Access Control.

## Secure version
The app has proper access control checks on the `/admin/secure` route. Only admins can access the admin page, demonstrating Secure Access Control.

## How to Fix
- Always check the user's role or permissions before granting access to sensitive or administrative routes.
- Implement role-based access control (RBAC) in your application logic.
- Never rely solely on client-side checks; always enforce authorization on the server side.
- Regularly review and test your access control logic to ensure there are no bypasses.

