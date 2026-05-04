# A07:2025 - Authentication Failures Evidence Case

This example demonstrates authentication failures, which occur when application functions related to authentication and session management are implemented incorrectly.

## Scenario

A web application implements authentication with weak password policies, insecure session management, and insufficient brute-force protection. Attackers can exploit these weaknesses to gain unauthorized access to user accounts.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5007](http://localhost:5007) in your browser.

## Evidence Case: Authentication Failures

- Visit `/login` and try logging in with weak credentials (e.g., username: `admin`, password: `admin`)
- Check `/register` to see that weak passwords are accepted without validation.
- Try the `/forgot-password` endpoint which uses insecure recovery mechanisms (security questions).
- Test `/brute-force` which has no rate limiting, allowing unlimited login attempts.
- Compare with the secure version at `/secure-login` which implements proper authentication.

### Example Attack

- An attacker can brute-force passwords due to lack of rate limiting or account lockout.
- Weak password policies allow users to set easily guessable passwords.
- Session tokens are predictable or don't expire properly.
- Credential stuffing attacks succeed because there's no protection against reused passwords.

## Why is this an Authentication Failure?

- The application allows weak passwords without enforcing complexity requirements.
- No multi-factor authentication (MFA) is implemented.
- Session management is flawed (predictable tokens, long-lived sessions).
- No protection against automated attacks (brute-force, credential stuffing).
- Password recovery uses insecure methods (security questions, cleartext emails).

## How to Prevent

- Implement multi-factor authentication (MFA) for all users, especially for admin accounts.
- Enforce strong password policies (complexity, length, avoid common passwords).
- Use secure session management with properly generated random session IDs.
- Implement rate limiting and account lockout after failed attempts.
- Store passwords using strong adaptive hashing algorithms (bcrypt, Argon2, PBKDF2).
- Use secure password recovery mechanisms (time-limited tokens, no security questions).
- Monitor and log authentication failures to detect attack patterns.
- Implement CAPTCHA or similar mechanisms after several failed attempts.

## Example Attack Scenarios

**Scenario #1:** A credential stuffing attack uses a list of known passwords. Without rate limiting or MFA, attackers can gain access to many accounts by trying common passwords.

**Scenario #2:** An application allows users to set passwords like "password123" or "admin". An attacker guesses these weak credentials through manual attempts or automated tools.

**Scenario #3:** Session IDs are generated using a predictable pattern (e.g., incrementing numbers). An attacker can guess valid session tokens and hijack active user sessions.

**Scenario #4:** The password recovery process uses security questions like "Mother's maiden name" which can be researched or guessed. Attackers use this to reset passwords and take over accounts.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
