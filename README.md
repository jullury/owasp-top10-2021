# OWASP Top 10:2025 Demonstration Project

This repository contains demonstration code and examples for the [OWASP Top 10:2025](https://owasp.org/Top10/2025/) security vulnerabilities. Each subdirectory corresponds to a specific OWASP Top 10:2025 vulnerability, with code, documentation, and examples to help you understand and mitigate these common security risks.

## OWASP Top 10:2025 List

1. **A01:2025 - Broken Access Control**
2. **A02:2025 - Security Misconfiguration**
3. **A03:2025 - Software Supply Chain Failures**
4. **A04:2025 - Cryptographic Failures**
5. **A05:2025 - Injection**
6. **A06:2025 - Insecure Design**
7. **A07:2025 - Authentication Failures**
8. **A08:2025 - Software or Data Integrity Failures**
9. **A09:2025 - Security Logging and Alerting Failures**
10. **A10:2025 - Mishandling of Exceptional Conditions**

## Structure

- `A01/`: Demonstrates **Broken Access Control** (vulnerable and best practice routes)
- `A02/`: Demonstrates **Security Misconfiguration** - Directory listing and sensitive file exposure:
    - `/browse/` : Directory listing showing misconfigured server
    - `/download-and-decompile` : Shows how attackers can extract sensitive information from exposed compiled code
    - Includes Docker setup for testing with Apache .htaccess configurations
- `A03/`: Demonstrates **Software Supply Chain Failures** - Vulnerable dependencies and supply chain attacks
- `A04/`: Demonstrates **Cryptographic Failures** (vulnerable and best practice routes)
- `A05/`: Demonstrates **Injection** (classic SQL injection, ORM-based injection, and command injection, both vulnerable and safe endpoints):
    - `/login` : Vulnerable SQL Injection
    - `/login/safe` : Safe SQL (parameterized)
    - `/login/orm_vuln` : Vulnerable ORM Injection
    - `/login/orm_safe` : Safe ORM (parameterized)
    - `/cmd_injection` : View File (Command Injection Demo, vulnerable to command injection)
    - `/safe_view_file` : Safe File Viewer (prevents command injection by validating input and not using the shell)
- `A06/`: Demonstrates **Insecure Design** - Cinema booking system with flawed business logic allowing group size limit bypass
    - `/book` : Group ticket booking system that demonstrates insecure design flaws
- `A07/`: Demonstrates **Authentication Failures** - Weak authentication mechanisms and session management issues
- `A08/`: Demonstrates **Software or Data Integrity Failures** - Unverified software updates and insecure deserialization
- `A09/`: Demonstrates **Security Logging and Alerting Failures** - Insufficient logging and monitoring
- `A10/`: Demonstrates **Mishandling of Exceptional Conditions** - Improper error handling and exception management

## How to Use

1. Navigate to the subdirectory for the vulnerability you want to explore (e.g., `A01/`).
2. Follow the README in each subdirectory for setup and usage instructions.
3. Run the example applications to see vulnerabilities in action and learn how to fix them.

## Requirements

- Python 3.x (for most examples)
- See each subdirectory's `requirements.txt` for dependencies

## Contributing

Contributions are welcome! Please open issues or submit pull requests to improve the examples or documentation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
