
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    payment = None
    error = None
    total_interest = None
    total_paid = None

    if request.args:
        try:
            price = float(request.args.get("price", 0))
            down = float(request.args.get("down", 0))
            rate = float(request.args.get("rate", 0))
            years = int(request.args.get("years", 0))

            if price <= 0 or down < 0 or down >= price or rate < 0 or years <= 0:
                raise ValueError("Invalid mortgage values")

            principal = price - down
            months = years * 12
            monthly_rate = rate / 100 / 12

            if monthly_rate == 0:
                payment = principal / months
            else:
                payment = principal * (
                    monthly_rate * (1 + monthly_rate) ** months
                ) / ((1 + monthly_rate) ** months - 1)

            total_paid = payment * months
            total_interest = total_paid - principal

        except ValueError:
            error = "Please enter valid mortgage information."

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mortgage Calculator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 60px auto;
                padding: 20px;
                background: #f4f6f8;
            }
            input, button {
                display: block;
                width: 100%;
                box-sizing: border-box;
                padding: 10px;
                margin: 10px 0;
            }
            button {
                background: #2563eb;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Mortgage Calculator</h1>

        <form method="GET">

            <label>Home Price ($)</label>
            <input type="number" name="price" min="1" step="any"
                value="{{ request.args.get('price', '') }}" required>

            <label>Down Payment ($)</label>
            <input type="number" name="down" min="0" step="any"
                value="{{ request.args.get('down', '') }}" required>

            <label>Annual Interest Rate (%)</label>
            <input type="number" name="rate" min="0" step="any"
                value="{{ request.args.get('rate', '') }}" required>

            <label>Loan Term (Years)</label>
            <input type="number" name="years" min="1"
                value="{{ request.args.get('years', '') }}" required>


            <button type="submit">Calculate Payment</button>
        </form>

        {% if payment is not none %}
            <h2>Monthly Payment: ${{ "%.2f"|format(payment) }}</h2>
            <p>Total Interest: ${{ "%.2f"|format(total_interest) }}</p>
            <p>Total Loan Payments: ${{ "%.2f"|format(total_paid) }}</p>
            <p>Principal and interest only.</p>
        {% endif %}

        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}
    </body>
    </html>
    """, payment=payment, error=error,
     total_interest=total_interest, total_paid=total_paid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
