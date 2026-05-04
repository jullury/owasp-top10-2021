# A08:2025 - Software or Data Integrity Failures Evidence Case

This example demonstrates software or data integrity failures, which occur when code and infrastructure don't protect against integrity violations. This includes things like insecure deserialization, reliance on untrusted software updates, and auto-update functionality without integrity verification.

## Scenario

A web application uses serialized objects for storing session data and implements an auto-update feature that downloads and executes updates without proper signature verification. Attackers can exploit these integrity failures to execute arbitrary code or manipulate application data.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5008](http://localhost:5008) in your browser.

## Evidence Case: Integrity Failures

- Visit `/serialize` to see how user data is serialized insecurely.
- Try `/deserialize` with crafted payloads to exploit insecure deserialization.
- Check `/auto-update` which downloads updates without signature verification.
- Test `/insecure-cicd` to see how compromised CI/CD pipelines can inject malicious code.
- Compare with `/secure-integrity` for best practices.

### Example Attack

- **Insecure Deserialization:** An attacker crafts a malicious serialized object that, when deserialized, executes arbitrary code on the server.
- **Unverified Updates:** An attacker performs a man-in-the-middle attack and serves a malicious update that gets executed by the application.
- **CI/CD Injection:** Attackers compromise the build pipeline and inject malicious code that gets distributed to all users.

## Why is this an Integrity Failure?

- The application deserializes data from untrusted sources without validation.
- Auto-update functionality doesn't verify digital signatures of updates.
- No integrity checks are performed on critical data or code.
- CI/CD pipelines lack proper security controls and access restrictions.
- The application trusts external data and code without verification.

## How to Prevent

- Avoid serializing untrusted data; use safe formats like JSON with schema validation.
- If serialization is necessary, use signed and encrypted serialization formats.
- Verify digital signatures on all software updates and third-party components.
- Implement strict CI/CD security: signed commits, reviewed code, protected branches.
- Use checksums and hashes to verify integrity of critical files and data.
- Implement allowlisting for permitted classes during deserialization.
- Use secure update mechanisms with rollback capabilities.

## Example Attack Scenarios

**Scenario #1:** A Java application uses native serialization. An attacker creates a malicious serialized object (using tools like ysoserial) and sends it to the application. When deserialized, it executes arbitrary commands on the server.

**Scenario #2:** An application has an auto-update feature that downloads updates from a server via HTTP. An attacker performs a MITM attack and replaces the legitimate update with malware, which is then executed with application privileges.

**Scenario #3:** A CI/CD pipeline has weak access controls. An attacker gains access and modifies the build script to include malicious code. The compromised build is then deployed to production, affecting all users.

**Scenario #4:** A web application stores session data in cookies using insecure serialization. An attacker modifies the cookie content to escalate privileges or inject malicious payloads that execute upon deserialization.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
