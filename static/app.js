// Initialize Stripe
var stripe = Stripe('your-publishable-key-here');

// Create an instance of Elements
var elements = stripe.elements();

// Create an instance of the card Element
var card = elements.create('card');

// Add an instance of the card Element into the `card-element` div
card.mount('#card-element');

// Handle form submission
document.querySelector('#payment-form').addEventListener('submit', function(e) {
    e.preventDefault();

    stripe.createToken(card).then(function(result) {
        if (result.error) {
            // Inform the user if there was an error
            console.error(result.error.message);
        } else {
            // Send the token to your server
            fetch('/pay', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount: document.querySelector('#amount').value,
                    currency: document.querySelector('#currency').value,
                    bank: document.querySelector('#bank').value,
                    receiver_account: document.querySelector('#receiver_account').value,
                    source_token: result.token.id // Pass the token to the backend
                })
            }).then(function(response) {
                return response.json();
            }).then(function(responseJson) {
                console.log(responseJson);
                if (responseJson.status === "success") {
                    alert("Payment Successful!");
                } else {
                    alert("Payment Failed: " + responseJson.message);
                }
            });
        }
    });
});
