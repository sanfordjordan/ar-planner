class Clothing:
    def __init__(self,
                 head=None,
                 body=None,
                 hand=None,
                 legs=None,
                 feet=None):
        # Initialize to empty list if not provided
        self.head = head if head is not None else []
        self.body = body if body is not None else []
        self.hand = hand if hand is not None else []
        self.legs = legs if legs is not None else []
        self.feet = feet if feet is not None else []