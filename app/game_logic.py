# Game Logic for Language Learning
# TODO: Implement Level class and game mechanics

class GameLevel:
    def __init__(self, level_number, language_target):
        self.level_number = level_number
        self.language_target = language_target
        self.conversation_history = []
        self.score = 0
    
    def add_message(self, sender, message):
        """Add a message to conversation history"""
        self.conversation_history.append({
            'sender': sender,
            'message': message
        })
    
    def evaluate_response(self, user_response):
        """Evaluate user response and return score"""
        # TODO: Implement evaluation logic
        pass
    
    def get_conversation(self):
        """Return conversation history"""
        return self.conversation_history
