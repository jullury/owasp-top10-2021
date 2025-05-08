# A02: Cryptographic Failures

This example demonstrates both vulnerable and best practice implementations of cryptographic handling in web applications, as described in the [OWASP Top 10 A02:2021](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/).

- Vulnerable and secure routes are available side by side for comparison.
- The app runs by default on port 5002.

## Vulnerabilities Demonstrated

- **Plaintext storage of sensitive data**: User passwords and SSNs are stored in plaintext.
- **Hardcoded, weak secret key**: The application uses a hardcoded, weak key for demonstration.
- **Insecure encoding instead of encryption**: Sensitive data (SSN) is only base64-encoded, not encrypted.
- **Decoding endpoint**: Anyone can decode sensitive data via the `/decode` endpoint.

## How to Run

1. Install requirements:

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

4. Visit [http://localhost:5000](http://localhost:5000) and follow the links to see the vulnerabilities in action.

## How to Fix

- Never store sensitive data in plaintext; always use strong encryption and hashing (e.g., bcrypt for passwords).
- Never use hardcoded or weak cryptographic keys.
- Do not use encoding (like base64) as a substitute for encryption.
- Restrict access to sensitive data and decoding endpoints.
