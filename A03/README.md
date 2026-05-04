# A03:2025 - Software Supply Chain Failures Evidence Case

This example demonstrates software supply chain failures, which occur when applications use vulnerable dependencies, fail to verify integrity of components, or inherit weaknesses from third-party code.

## Scenario

A web application uses multiple third-party packages and dependencies without proper version pinning or integrity verification. Attackers can exploit known vulnerabilities in these dependencies or compromise the supply chain to inject malicious code into the application.

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

## Evidence Case: Supply Chain Vulnerabilities

- Visit `/dependencies` to see all application dependencies and their versions.
- Check `/vulnerable-deps` to see dependencies with known CVEs.
- Visit `/integrity-check` to see how the application handles package integrity verification (or lack thereof).
- Try the secure version at `/secure-deps` to see proper dependency management practices.

### Example Attack

- An attacker identifies a known vulnerability (CVE) in an application's dependency.
- They exploit the vulnerability to gain unauthorized access or execute malicious code.
- Without proper integrity checks, compromised packages can be silently injected into the supply chain.
- Dependency confusion attacks can trick the application into downloading malicious packages from public repositories.

## Why is this a Supply Chain Failure?

- The application doesn't pin dependency versions, allowing automatic updates to vulnerable versions.
- No integrity verification is performed on downloaded packages.
- Known vulnerable dependencies are used without compensating controls.
- The build pipeline may use compromised or untrusted components.
- No software bill of materials (SBOM) is maintained to track all components.

## How to Prevent

- Maintain an up-to-date inventory of all components (SBOM).
- Only use trusted repositories and verify package integrity with hashes/signatures.
- Pin dependency versions and use lockfiles to ensure reproducible builds.
- Regularly scan dependencies for known vulnerabilities (CVEs).
- Implement security checks in CI/CD pipelines for all third-party code.
- Use private package repositories with access controls for internal dependencies.
- Monitor security advisories for all used components.
- Have a patch management process for quickly updating vulnerable dependencies.

## Example Attack Scenarios

**Scenario #1:** An application uses an outdated version of a popular JavaScript library with a known XSS vulnerability. An attacker exploits this vulnerability to inject malicious scripts into the application, affecting all users.

**Scenario #2:** A build system downloads dependencies over an unencrypted connection. An attacker performs a man-in-the-middle attack and replaces a legitimate package with a malicious version that includes a backdoor.

**Scenario #3:** A company's internal package name is not registered on the public PyPI repository. An attacker publishes a malicious package with the same name, and the build system downloads the malicious version instead of the internal one (dependency confusion attack).

**Scenario #4:** A developer includes a development dependency (with known vulnerabilities) in the production build, exposing the application to attacks through the vulnerable component.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
