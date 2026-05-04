"""
A04:2021 - Insecure Design Evidence Case
This Flask app demonstrates an insecure design flaw based on OWASP Scenario #2:

'A cinema chain allows group booking discounts and has a maximum of fifteen attendees before requiring a deposit. 
Attackers could threat model this flow and test if they could book six hundred seats and all cinemas at once in a few requests, 
causing a massive loss of income.'

This is a classic insecure design issue, where the individual validation checks appear secure 
but the overall workflow and business logic contain critical flaws.
"""
from flask import Flask, request, abort, escape
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# List of cinemas for the demo
CINEMAS = ['Cinema 1', 'Cinema 2', 'Cinema 3'] 
MAX_GROUP_SIZE = 15  # Group bookings over this size require deposit per business rules
MAX_CINEMA_SEATS = 100  # Each cinema has 100 seats total

# In-memory state: track bookings per cinema
bookings = {cinema: 0 for cinema in CINEMAS}
deposits = {cinema: False for cinema in CINEMAS}  # Track if deposits have been made

@app.route('/')
def index():
    return '''
    <h2>A04: Insecure Design Demo - Cinema Booking System</h2>
    <ul>
        <li><a href="/book">Book Group Tickets (Insecure Design)</a></li>
        <li><a href="/secure-design">Secure Design Practices</a></li>
    </ul>
    <p>This demo shows a cinema booking system with insecure design flaws in its business logic validation.</p>
    <p>According to business rules, groups larger than 15 require a deposit, but the system architecture allows this to be bypassed.</p>
    '''

@app.route('/book', methods=['GET', 'POST'])
def book():
    message = ''
    business_rule_note = ''
    deposit_warning = ''
    
    # Get current status
    available_seats = {cinema: MAX_CINEMA_SEATS - bookings[cinema] for cinema in CINEMAS}
    
    if request.method == 'POST':
        cinema = request.form.get('cinema', '')
        deposit_provided = request.form.get('deposit') == 'on'
        
        # Input validation
        if cinema not in CINEMAS:
            return abort(400, "Invalid cinema selection.")
        
        try:
            num_seats = int(request.form.get('num_seats', '0'))
        except ValueError:
            return abort(400, "Invalid number of seats.")
            
        # Individual validations look secure, but the architecture allows bypassing business rules
        if num_seats <= 0:
            message = "Number of seats must be positive."
        elif num_seats > MAX_CINEMA_SEATS:
            message = f"Cannot book {num_seats} seats at once. Maximum is {MAX_CINEMA_SEATS}."
        elif num_seats > MAX_GROUP_SIZE and not deposit_provided:
            deposit_warning = f"<p style='color:orange'>Groups larger than {MAX_GROUP_SIZE} require a deposit.</p>"
        else:
            bookings[cinema] += num_seats
            message = f"Booked {num_seats} seats at {escape(cinema)}! (Total now: {bookings[cinema]})"
            
            if bookings[cinema] > MAX_CINEMA_SEATS:
                business_rule_note = f"<p style='color:red;'><b>BUSINESS RULE VIOLATED:</b> Cinema overbooked by {bookings[cinema] - MAX_CINEMA_SEATS} seats!</p>"
    
    cinema_options = ''.join(f'<option value="{escape(c)}">{escape(c)}</option>' for c in CINEMAS)
    return f'''
        <h3>Book Group Tickets (Insecure Design)</h3>
        
        <div style="border:1px solid #ddd; padding:10px; margin-bottom:20px; background-color:#f8f8f8">
            <h4>Business Rules:</h4>
            <ul>
                <li>Each cinema has {MAX_CINEMA_SEATS} seats total</li>
                <li>Group bookings larger than {MAX_GROUP_SIZE} people require a deposit</li>
            </ul>
        </div>
        
        <form method="post">
            Cinema: <select name="cinema">{cinema_options}</select><br>
            Number of seats: <input name="num_seats" type="number" min="1" max="{MAX_CINEMA_SEATS}"><br>
            <input type="checkbox" name="deposit" id="deposit"> <label for="deposit">Pay deposit</label><br>
            <input type="submit" value="Book">
        </form>
        
        {deposit_warning}
        <p>{message}</p>
        {business_rule_note}
        
        <h4>Current Bookings:</h4>
        <ul>
            {''.join(f'<li>{escape(cinema)}: {bookings[cinema]}/{MAX_CINEMA_SEATS} seats booked</li>' for cinema in CINEMAS)}
        </ul>
    '''

@app.route('/secure-design')
def secure_design():
    return '''
        <h2>Secure Design Practices</h2>
        <ul>
            <li>Implement threat modeling during design phase</li>
            <li>Use centralized validation and business logic controls</li>
            <li>Implement rate limiting and request throttling</li>
            <li>Add aggregate limits across multiple requests</li>
            <li>Use secure design patterns and architecture reviews</li>
        </ul>
        <a href="/">Back</a>
    '''

if __name__ == '__main__':
    app.run(port=5004, debug=False)
