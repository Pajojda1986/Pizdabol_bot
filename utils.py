from PIL import Image
from random import randint
import json


async def cards():
    filename = 'table.jpg'
    with Image.open(filename) as table:
        table.load()

    with Image.open('cards/b/4b.png') as card:
        card.load()

    cords_of_cards = {}

    for i in range(0, 12):
        for k in range(0, 5):
            cords_of_cards[len(cords_of_cards) + 1] = (20 + i * 160, k * 170 + k * 30 + 60)


def register_token():
    token = randint(1000, 9999)
    return token


class Game:
    def __init__(self):
        self.game_info = {
            "table": [],
            "players": {},
            "token": register_token(),
        }

    def add_member(self, *args):
        self.game_info["players"][args[0]] = {
            "id": args[1],
            "cards": []
        }

    def create_json(self):
        with open(f'games/game_{self.game_info['token']}.json', 'w', encoding='utf-8') as file:
            json.dump(self.game_info, file, ensure_ascii=False, indent=4)
