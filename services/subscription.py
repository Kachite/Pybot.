class SubscriptionManager:
    def __init__(self):
        self.subscribed_users = set()  # Use a database in production

    def subscribe_user(self, user_id):
        self.subscribed_users.add(user_id)

    def unsubscribe_user(self, user_id):
        self.subscribed_users.discard(user_id)

    def get_subscribed_users(self):
        return list(self.subscribed_users)