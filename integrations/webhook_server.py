from flask import Flask, request, jsonify
from core.agent import process_incoming_message
from config.config import WEBHOOK_VERIFY_TOKEN

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Security: Check for a secret token from Ngrok/Sender
    token = request.args.get('token') or request.headers.get('X-Verify-Token')
    if token != WEBHOOK_VERIFY_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    
    # NOTE: Adapt these keys based on your specific WhatsApp provider (Green-API, Twilio, etc.)
    # This is a generic structure.
    sender = data.get('sender') 
    message = data.get('message')
    
    if not sender or not message:
        return jsonify({"status": "ignored", "reason": "no_data"}), 200

    print(f"Received from {sender}: {message}")

    response_text = process_incoming_message(sender, message)
    
    if response_text:
        print(f"Replying: {response_text}")
        # Here you would add the code to POST the response back to WhatsApp/Teams
        return jsonify({"reply": response_text}), 200
    
    return jsonify({"status": "silent"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)