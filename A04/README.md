# A04:2021 - Insecure Design Evidence Case

This example demonstrates an insecure design flaw in a cinema booking system, based on OWASP's Example Attack Scenario #2.

## Scenario
A cinema chain booking system has a business rule that group bookings larger than 15 attendees require a deposit. However, the system's design fails to enforce this rule effectively, allowing attackers to book hundreds of seats across multiple smaller transactions without paying any deposit, potentially causing significant business impact.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [http://localhost:5004](http://localhost:5004) in your browser.

## Evidence Case: Cinema Booking Insecure Design
- Go to `/book`.
- Notice that the business rules state groups larger than 15 require a deposit.
- Try booking 16 seats and observe that the system asks for a deposit.
- **The insecure design flaw:** Make multiple smaller bookings (e.g., 10 seats at a time) that each stay under the limit but collectively bypass the deposit requirement.
- You can also book more seats than the cinema's capacity by making multiple requests.

### Example Attack
- An attacker could book hundreds of seats across multiple small transactions without any deposit.
- The application has individual validation checks but fails to implement centralized business logic controls.
- There's no rate limiting, global validation, or transaction history checks.

## Why is this Insecure Design?
- The flaw is in the architecture: individual validations exist but are ineffective due to the fragmented business logic.
- Input validation alone cannot fix this - the entire workflow and system architecture need redesign.
- The application failed to consider proper threat modeling for the specific business domain.
- The design doesn't account for how individual valid actions could collectively cause system-wide issues.

## How to Prevent
- Establish and use a secure development lifecycle with AppSec professionals to help evaluate and design security and privacy-related controls.
- Establish and use a library of secure design patterns or paved road ready-to-use components.
- Use threat modeling for critical authentication, access control, business logic, and key flows.
- Integrate security language and controls into user stories.
- Integrate plausibility checks at each tier of your application (from frontend to backend).
- Write unit and integration tests to validate that all critical flows are resistant to the threat model. Compile use-cases and misuse-cases for each tier of your application.
- Segregate tier layers on the system and network layers depending on the exposure and protection needs.
- Segregate tenants robustly by design throughout all tiers.
- Limit resource consumption by user or service.
- Require authentication before allowing password resets.
- Use secure, time-limited reset tokens sent to the user's registered email.
- Ensure that only the owner of the account can reset their password.

## Example Attack Scenarios
**Scenario #1:** A credential recovery workflow might include “questions and answers,” which is prohibited by NIST 800-63b, the OWASP ASVS, and the OWASP Top 10. Questions and answers cannot be trusted as evidence of identity as more than one person can know the answers, which is why they are prohibited. Such code should be removed and replaced with a more secure design.

**Scenario #2:** A cinema chain allows group booking discounts and has a maximum of fifteen attendees before requiring a deposit. Attackers could threat model this flow and test if they could book six hundred seats and all cinemas at once in a few requests, causing a massive loss of income.

**Scenario #3:** A retail chain’s e-commerce website does not have protection against bots run by scalpers buying high-end video cards to resell auction websites. This creates terrible publicity for the video card makers and retail chain owners and enduring bad blood with enthusiasts who cannot obtain these cards at any price. Careful anti-bot design and domain logic rules, such as purchases made within a few seconds of availability, might identify inauthentic purchases and reject such transactions.

---

**This is for educational purposes only. Never use such insecure patterns in production!**
