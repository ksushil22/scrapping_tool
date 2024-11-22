class Notification:
    """
    Simple Notification class. Can be modified in the future if we make scrapping async and notify via email to the
    user.
    """
    @staticmethod
    def notify(message):
        print(message)
