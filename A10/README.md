# A10:2025 - Mishandling of Exceptional Conditions Evidence Case

This example demonstrates the mishandling of exceptional conditions, which occurs when applications don't properly handle errors, exceptions, and edge cases. This leads to information disclosure, instability, and security vulnerabilities.

## Scenario

A web application has poor exception handling practices. It displays detailed error messages to users, crashes on unexpected input, and doesn't handle edge cases gracefully. Attackers can exploit these behaviors to gather system information, cause denial of service, or trigger unexpected application states.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5010](http://localhost:5010) in your browser.

## Evidence Case: Exception Handling Failures

- Visit `/divide` and try dividing by zero - detailed error messages are shown.
- Check `/file-read` with non-existent files - reveals file system structure.
- Try `/api/users` with malformed requests - stack traces exposed.
- Test `/upload` with oversized files - application crashes without grace.
- Compare with `/secure-errors` to see proper error handling.

### Example Attack

- **Information Disclosure:** Detailed error messages reveal database structure, file paths, and internal logic.
- **Denial of Service:** Sending unexpected input causes the application to crash or hang.
- **System Fingerprinting:** Stack traces expose technology stack, versions, and internal architecture.
- **Bypass Security Controls:** Unhandled exceptions can leave the application in an inconsistent state.

## Why is this Mishandling of Exceptional Conditions?

- The application displays detailed error messages (stack traces, debug info) to users.
- Exceptions are not caught and handled gracefully.
- No generic error pages are implemented for unexpected conditions.
- Error messages reveal sensitive information (file paths, SQL queries, internal logic).
- The application crashes or behaves unpredictably with unexpected input.
- No logging of exceptions for monitoring and debugging (see also A09).

## How to Prevent

- Implement generic error pages that don't reveal sensitive information.
- Catch and handle exceptions gracefully with appropriate fallback behavior.
- Log exceptions with full detail internally, but show minimal info to users.
- Use try-catch blocks strategically around risky operations.
- Validate input thoroughly before processing to prevent many exceptions.
- Implement rate limiting and input constraints to prevent resource exhaustion.
- Return appropriate HTTP status codes with generic error messages.
- Test edge cases and failure scenarios during development.
- Never expose stack traces, debug information, or internal details to users.

## Example Attack Scenarios

**Scenario #1:** An application shows a detailed stack trace when a database connection fails. The error message reveals the database IP, username, query structure, and table names. An attacker uses this information to craft targeted attacks.

**Scenario #2:** A file upload feature doesn't handle oversized files gracefully. An attacker uploads a massive file that crashes the server or fills the disk space, causing denial of service for all users.

**Scenario #3:** An API endpoint doesn't validate input types properly. An attacker sends unexpected data types (e.g., sending an array where a string is expected), causing unhandled exceptions that expose internal application logic.

**Scenario #4:** A payment processing function doesn't handle timeout exceptions. When the payment gateway is slow to respond, the application hangs indefinitely, consuming resources and potentially leaving transactions in an inconsistent state.

**Scenario #5:** A search function crashes when given special characters or extremely long input. An attacker can repeatedly trigger these crashes to cause denial of service, while also learning about the application's internal search implementation from error messages.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
