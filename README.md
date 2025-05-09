# OWASP Top 10 Demonstration Project

This repository contains demonstration code and examples for the [OWASP Top 10](https://owasp.org/www-project-top-ten/) security vulnerabilities. Each subdirectory corresponds to a specific OWASP Top 10 vulnerability, with code, documentation, and examples to help you understand and mitigate these common security risks.

## Structure

- `A01/`: Demonstrates **Broken Access Control** (vulnerable and best practice routes)
- `A02/`: Demonstrates **Cryptographic Failures** (vulnerable and best practice routes)
- `A03/`: Demonstrates **Injection** (classic SQL injection, ORM-based injection, and command injection, both vulnerable and safe endpoints):
    - `/login` : Vulnerable SQL Injection
    - `/login/safe` : Safe SQL (parameterized)
    - `/login/orm_vuln` : Vulnerable ORM Injection
    - `/login/orm_safe` : Safe ORM (parameterized)
    - `/cmd_injection` : View File (Command Injection Demo, vulnerable to command injection)
    - `/safe_view_file` : Safe File Viewer (prevents command injection by validating input and not using the shell)
- `A04/`: Demonstrates **Insecure Design** - Cinema booking system with flawed business logic allowing group size limit bypass
    - `/book` : Group ticket booking system that demonstrates insecure design flaws
- (Add more directories for each OWASP Top 10 item as you implement them)

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
