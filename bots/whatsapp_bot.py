from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from fuzzywuzzy import process

app = Flask(__name__)

faq = {
    "how to open a bank account": "To open a bank account with Tinkoff, you can download our app or visit our website and follow the steps provided.",
    "how to order a card": "To order a card, simply log into the Tinkoff app, go to the 'Cards' section, and follow the instructions to choose and order a card.",
    "how to make a transfer": "To make a transfer, open the Tinkoff app, go to the 'Transfers' section, select the recipient, and enter the amount you want to send.",
    "how to check balance": "You can check your balance directly in the Tinkoff app, or by logging into your account on our website.",
    "how to contact customer support": "To contact customer support, you can use the in-app chat, call us at 8-800-555-77-44, or email support@tinkoff.ru.",
    "how to change my personal information": "To change your personal information, log into the Tinkoff app, go to 'Profile', and select 'Edit Personal Info'.",
    "how to reset my password": "To reset your password, open the Tinkoff app, go to 'Settings', select 'Security', and follow the steps to reset your password.",
    "thank you": "You're welcome! 😊",
    "okay": "If you have further questions, feel free to ask."
}

subscribed_users = set()

def get_faq_answer(query):
    query_lower = query.lower()
    best_match, score = process.extractOne(query_lower, faq.keys())
    if score > 60:
        return faq[best_match]
    return "❓ Sorry, I couldn't find an answer. Try asking something like 'How to contact customer support'."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")

    print("📩 Received message:", incoming_msg)
    print("📱 From:", from_number)

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower() in ["start", "hello", "hi"]:
        reply = (
            "👋 Hello! I can answer your questions about Tinkoff services.\n\n"
            "Type:\n"
            "- *Subscribe* to receive updates\n"
            "- *Unsubscribe* to stop updates"
        )
    elif incoming_msg.lower() == "subscribe":
        subscribed_users.add(from_number)
        reply = "✅ You've subscribed to automated updates!"
    elif incoming_msg.lower() == "unsubscribe":
        subscribed_users.discard(from_number)
        reply = "❌ You've unsubscribed from updates."
    else:
        reply = get_faq_answer(incoming_msg)

    msg.body(reply)
    return Response(str(resp), mimetype="application/xml")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
