from fuzzywuzzy import process

class FAQHandler:
    def __init__(self):
        self.faq = {
            "how to open a bank account": "To open a bank account with Tinkoff, download our app or visit our website.",
            "how to order a card": "Log into the Tinkoff app, go to 'Cards', and follow the instructions.",
            "how to make a transfer": "Open the app, go to 'Transfers', select the recipient, and enter the amount.",
            "how to check balance": "Check your balance in the app or on the website.",
            "how to contact customer support": "Use in-app chat, call 8-800-555-77-44, or email support@tinkoff.ru.",
            "how to change my personal information": "Go to 'Profile' in the app and edit your info.",
            "how to reset my password": "Go to 'Settings', select 'Security', and reset your password."
        }

    def get_faq_answer(self, query):
        best_match, score = process.extractOne(query.lower(), self.faq.keys())
        if score > 50:
            return self.faq[best_match]
        return "Sorry, I couldn't find an answer to your question."