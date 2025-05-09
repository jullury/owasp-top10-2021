# A02:2021 - Cryptographic Failures Evidence Case

This example demonstrates cryptographic failures in web applications, which occur when sensitive data is exposed due to weak or missing encryption.

## Scenario
A web application stores and handles sensitive data (user credentials and social security numbers) insecurely. Instead of proper encryption, it uses insufficient protection methods like plaintext storage, encoding instead of encryption, and hardcoded cryptographic keys. These failures expose sensitive data to attackers.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Best Practice) Generate a secure Fernet key and set it in a `.env` file:
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   Copy the output and add it to your `.env` file as:
   ```
   FERNET_KEY="<your-generated-key>"
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Visit [http://localhost:5002](http://localhost:5002) in your browser.

## Evidence Case: Cryptographic Failures
- Visit the `/users` endpoint to see user data stored in plaintext, including passwords.
- Visit the `/encode` endpoint to see how SSNs are merely base64-encoded (not encrypted).
- Examine the `/decode` endpoint which allows anyone to decode the encoded data.
- For comparison, check the `/secure-users` endpoint to see properly encrypted data.

### Example Attack
- An attacker who gains access to the database can read all passwords directly since they're stored in plaintext.
- An attacker can use the `/decode` endpoint to convert encoded (not encrypted) data back to plaintext.
- If the application's source code is leaked, the hardcoded cryptographic key becomes known, compromising any data "protected" by it.

## Why is this a Cryptographic Failure?
- The flaw is in how sensitive data is protected (or not protected):
  - Passwords stored in plaintext instead of being hashed
  - SSNs encoded (reversible) instead of encrypted (requires key)
  - Cryptographic keys hardcoded in the application
  - Public endpoints for decoding sensitive data
- These failures violate basic security principles for protecting sensitive data at rest and in transit.
- Encoding (like base64) only obscures data but doesn't actually protect it cryptographically.

## How to Prevent
- Store sensitive data encrypted at rest and protect it in transit with secure protocols.
- Never store passwords in plain text; use strong adaptive hashing with salt (bcrypt, Argon2, PBKDF2).
- Use modern, strong encryption algorithms and protocols (AES-256, RSA, etc.).
- Generate, store, and manage keys securely; never hardcode them in source code.
- Use proper key rotation and management practices.
- Disable caching for responses containing sensitive data.
- Store passwords using strong adaptive and salted hashing functions.
- Apply appropriate security headers to prevent browser side caching.
- Verify independently the effectiveness of configurations and settings.

## Example Attack Scenarios
**Scenario #1:** An application encrypts credit card numbers in a database using automatic database encryption. However, this data is automatically decrypted when retrieved, allowing an SQL injection flaw to retrieve credit card numbers in clear text.

**Scenario #2:** A website doesn't use TLS for all authenticated pages, allowing an attacker to monitor network traffic, steal an authenticated user's session cookie, and hijack the user's session.

**Scenario #3:** A company's password database uses unsalted or simple hashes to store passwords. A file upload flaw allows an attacker to retrieve the password database. All unsalted hashes can be exposed with a rainbow table of pre-calculated hashes.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
