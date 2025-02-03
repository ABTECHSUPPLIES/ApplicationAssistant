from flask import Flask, request, jsonify

app = Flask(__name__)

# Example iPhone prices in ZAR
IPHONE_PRICES = {
    "iPhone XS": 7500,
    "iPhone 11 Pro": 9500,
    "iPhone 12 Pro": 11500,
    "iPhone 13 Pro": 13500,
    "iPhone 14 Pro": 15500,
    "iPhone 15 Pro": 17500,
    "iPhone 16 Pro Max": 19500
}

# Interest rates based on repayment period
INTEREST_RATES = {
    3: 0.05,   # 5%
    6: 0.08,   # 8%
    12: 0.12,  # 12%
    24: 0.15   # 15%
}

@app.route('/calculate_installment', methods=['POST'])
def calculate_installment():
    data = request.json
    model = data.get("model")
    deposit = data.get("deposit", 750)
    months = data.get("months", 12)
    
    if model not in IPHONE_PRICES:
        return jsonify({"error": "Invalid iPhone model."}), 400
    if months not in INTEREST_RATES:
        return jsonify({"error": "Invalid repayment period. Choose from 3, 6, 12, or 24 months."}), 400
    if deposit < 750:
        return jsonify({"error": "Minimum deposit is R750."}), 400
    
    price = IPHONE_PRICES[model]
    interest_rate = INTEREST_RATES[months]
    amount_financed = price - deposit
    total_payable = amount_financed * (1 + interest_rate)
    monthly_payment = total_payable / months
    
    return jsonify({
        "model": model,
        "price": price,
        "deposit": deposit,
        "months": months,
        "interest_rate": f"{interest_rate * 100}%",
        "total_payable": round(total_payable, 2),
        "monthly_payment": round(monthly_payment, 2)
    })

@app.route('/eligibility_requirements', methods=['GET'])
def eligibility_requirements():
    return jsonify({
        "requirements": [
            "Proof of income",
            "Valid ID",
            "Proof of residence"
        ]
    })

@app.route('/payment_methods', methods=['GET'])
def payment_methods():
    return jsonify({
        "methods": [
            "EFT (Electronic Funds Transfer)",
            "Cash Send",
            "COD (Cash on Delivery, for orders above R10,000)"
        ]
    })

@app.route('/order_tracking', methods=['GET'])
def order_tracking():
    return jsonify({
        "message": "To track your order, please contact ANB Tech Supplies with your order reference number."
    })

@app.route('/iphone_images', methods=['GET'])
def iphone_images():
    return jsonify({"url": "https://abtechsupplies.github.io/Pictures/"})

if __name__ == '__main__':
    app.run(debug=True)
