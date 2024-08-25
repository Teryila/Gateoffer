from flask import Flask, request, jsonify, render_template
import stripe
import logging

app = Flask(__name__)

# Set your secret key: remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_51PjSaNRx4xZPU7wWD6DToXDOjTpbGfHhJcNESDvpVQlmdRWp4QUGfPDTKLQJNhubbNv1AepSw2ML7KBvGpWKauq4001TT3tEYY"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    try:
        data = request.get_json()
        logging.info(f"Received payment data: {data}")

        amount = float(data['amount'])
        currency = data['currency']
        bank = data['bank']
        receiver_account = data['receiver_account']
        source_token = data['source_token']

        # Convert amount to lowest currency unit
        converted_amount = amount
        logging.info(f"Converted amount: {converted_amount}")

        # Create the charge on Stripe's servers
        charge = stripe.Charge.create(
            amount=int(converted_amount * 100),  # amount in cents
            currency=currency,
            source=source_token,  # obtained with Stripe.js
            description=f'Payment Charge to {receiver_account} via {bank}'
        )
        return jsonify({"status": "success", "charge_id": charge.id})

    except stripe.error.CardError as e:
        logging.error(f"CardError: {e.user_message}")
        return jsonify({"status": "error", "message": e.user_message}), 400
    except stripe.error.StripeError as e:
        logging.error(f"StripeError: {str(e)}")
        return jsonify({"status": "error", "message": "A Stripe error occurred"}), 400
    except Exception as e:
        logging.error(f"A serious error occurred: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)
