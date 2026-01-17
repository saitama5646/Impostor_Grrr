
import random

class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = {}
        self.impostors = []
        self.word = ""
        self.active = False

    def add_player(self, user_id, name):
        if not self.active:
            self.players[user_id] = name

    def can_start(self):
        return len(self.players) >= 3

    def start_game(self, words):
        self.active = True
        category = random.choice(list(words.keys()))
        self.word = random.choice(words[category])
        impostor_count = 2 if len(self.players) >= 8 else 1
        self.impostors = random.sample(list(self.players.keys()), impostor_count)
        return self.word, self.impostors
