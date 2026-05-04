# A09:2025 - Security Logging and Alerting Failures Evidence Case

This example demonstrates security logging and alerting failures, which occur when applications don't properly log security-relevant events or fail to generate timely alerts.

## Scenario

A web application handles authentication, payment processing, and sensitive operations but fails to log important security events. There's no alerting system in place, so attacks go undetected. When a breach occurs, there's no audit trail to investigate what happened.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5009](http://localhost:5009) in your browser.

## Evidence Case: Logging and Alerting Failures

- Visit `/login` and try multiple failed login attempts - no logs are generated.
- Check `/transfer` to make a fund transfer - no audit trail is created.
- Try `/admin` access as a regular user - no alert is triggered.
- Visit `/logs` to see that only basic access logs exist (not security-focused).
- Compare with `/secure-logging` to see proper security logging practices.

### Example Attack

- An attacker can perform brute-force attacks without detection.
- Multiple failed login attempts don't trigger any alerts.
- Suspicious activities (like accessing admin pages) go unnoticed.
- When a breach occurs, there's no audit trail to determine what happened.
- Attackers have unlimited time to explore and exploit the system.

## Why is this a Logging and Alerting Failure?

- The application doesn't log security-critical events (logins, failures, access attempts).
- No alerting mechanism exists for suspicious activities.
- Logs don't include sufficient detail (timestamps, source IP, user context).
- Log entries don't use a consistent, parseable format.
- No monitoring or SIEM integration is in place.
- Sensitive data might be logged (like passwords or tokens).

## How to Prevent

- Log all security-relevant events: login success/failure, access control failures, input validation failures.
- Use a consistent, structured log format (JSON) that can be easily parsed.
- Include contextual information: timestamps, source IP, user ID, session ID.
- Implement real-time alerting for suspicious patterns (multiple failures, privilege escalation).
- Ensure logs are stored securely and cannot be tampered with by attackers.
- Never log sensitive data (passwords, tokens, PII).
- Regularly review and test logging and alerting effectiveness.
- Integrate with SIEM or centralized logging solutions.
- Set up dashboards and alerts for security metrics.

## Example Attack Scenarios

**Scenario #1:** An attacker performs a brute-force attack against user accounts. Without proper logging and alerting, the attack goes unnoticed for days, allowing the attacker to compromise multiple accounts.

**Scenario #2:** An application doesn't log failed access attempts to admin panels. An attacker uses directory traversal or privilege escalation techniques, and the security team has no visibility into these attempts.

**Scenario #3:** A breach occurs, but the application only logs basic access logs without security context. The incident response team cannot determine what data was accessed, which accounts were compromised, or how the attacker moved through the system.

**Scenario #4:** An application logs sensitive information like passwords or session tokens in plaintext. An attacker who gains access to the logs can use this information to further compromise the system.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
