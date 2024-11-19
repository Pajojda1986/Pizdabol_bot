from PIL import Image
from random import randint, shuffle
import json
from os import listdir, remove
from text import exit_player
from numpy import array_split


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


def shuffle_cards() -> list:
    cards_list = []
    all_games = listdir('cards')
    for suit in all_games:
        all_cards_of_suit = listdir('cards/' + suit)
        for card in all_cards_of_suit:
            cards_list.append(card[:-4])
    shuffle(cards_list)
    return cards_list


class Game:
    def __init__(self, data=None):
        if data is None:
            self.game_info = {
                "table": [],
                "players": {},
                "token": register_token()
            }
        else:
            self.game_info = {
                'table': data["table"],
                'players': data["players"],
                'token': data["token"]
            }

    def add_member(self, name: str, player_id: int):
        self.game_info["players"][name] = {
            "id": player_id,
            "cards": []
        }

    def dealing_cards(self):
        all_cards = shuffle_cards()
        print(all_cards)
        print(self.game_info['players'])
        count_of_players = len(self.game_info['players'])
        print(count_of_players)
        chunks = array_split(all_cards, count_of_players)
        for player, id_player in zip(self.game_info['players'], range(count_of_players + 1)):
            self.game_info['players'][player]['cards'] = chunks[id_player].tolist()

    def create_json(self):
        with open(f'games/game_{self.game_info['token']}.json', 'w', encoding='utf-8') as file:
            json.dump(self.game_info, file, ensure_ascii=False, indent=4)

        print(self.game_info)


class Player:

    def __init__(self, data=None):
        if data is None:
            self.player_info = {
                'id': 0,
                'player_name': '',
                'in_game': ''
            }
        else:
            self.player_info = {
                'id': data['id'],
                'player_name': data['player_name'],
                'in_game': data['in_game']
            }

    def add_statistic(self):
        pass

    def add_info(self, player_id: int, player_name: str, in_game: str):
        if player_id:
            self.player_info['id'] = player_id
        if player_name:
            self.player_info['player_name'] = player_name
        if in_game:
            self.player_info['in_game'] = in_game

    def add_game(self, in_game):
        self.player_info['in_game'] = in_game

    def create_json(self):
        with open(f'players/player_{self.player_info['id']}.json', 'w', encoding='utf-8') as file:
            json.dump(self.player_info, file, ensure_ascii=False, indent=4)
        print(self.player_info)


def find_lobby(lb_id: str, data=None, raw=None):
    all_lobbies = listdir('games')
    for lobby_id in all_lobbies:
        if f'game_{lb_id}.json' == lobby_id:
            with open(f'games/game_{lb_id}.json', 'r', encoding='utf-8') as file:
                if data:
                    return json.load(file)
                elif raw:
                    return file
    all_players = listdir('players')
    for player in all_players:
        print(player, f'player_{lb_id}.json')
        if f'player_{lb_id}.json' == player:
            with open(f'players/player_{lb_id}.json', 'r', encoding='utf-8') as file:
                player_data = json.load(file)
                for lobby_id in all_lobbies:
                    if f'{player_data['in_game']}.json' == lobby_id:
                        with open(f'games/{player_data['in_game']}.json', 'r', encoding='utf-8') as file_g:
                            if data:
                                return json.load(file_g)
                            elif raw:
                                return file
    return None


def find_player(player: int):
    all_players = listdir('players')
    for player_id in all_players:
        if f'player_{player}.json' == player_id:
            with open(f'players/player_{player}.json', 'r', encoding='utf-8') as file:
                return json.load(file)

    return None


def player_del_in_game(player):
    with open(f'players/{player}', 'r', encoding='utf-8') as file:
        data_player = json.load(file)
        data_player["in_game"] = ''
    with open(f'players/{player}', 'w', encoding='utf-8') as file:
        json.dump(data_player, file, ensure_ascii=False, indent=4)


def del_data_play():
    all_games = listdir('games')
    for games in all_games:
        remove(f'games/{games}')
    all_players = listdir('players')
    for player in all_players:
        player_del_in_game(player)


def exit_game(player_id: int):
    leave_message = []
    all_games = listdir('games')
    all_players = listdir('players')
    for player in all_players:
        if f"player_{player_id}.json" == player:
            with open(f'players/{player}', 'r', encoding='utf-8') as file:
                data_player = json.load(file)
                for game in all_games:
                    print(data_player["in_game"])
                    if game[:-5] == data_player["in_game"]:
                        with open(f'games/{game}', 'r', encoding='utf-8') as file_game:
                            game_data = json.load(file_game)
                            for player_d in list(game_data['players']):
                                data_leave = player_d
                                if game_data['players'][player_d]['id'] == data_player['id']:
                                    del game_data['players'][player_d]
                                    player_del_in_game(player)
                                    with open(f'games/{game}', 'w', encoding='utf-8') as file_g:
                                        json.dump(game_data, file_g, ensure_ascii=False, indent=4)
                                        for player_e in game_data['players']:
                                            leave_message.append([game_data['players'][player_e]['id'],
                                                                  exit_player.format(name=data_leave)])

                            if len(game_data['players']) == 0:
                                file_game.close()
                                remove(f'games/{game}')
    return leave_message


def get_all_id(player_id: int) -> list:
    players_id = []
    with open(f'players/player_{player_id}.json', 'r', encoding='utf-8') as file:
        player_game = json.load(file)
        with open(f'games/{player_game['in_game']}.json', 'r', encoding='utf-8') as file_g:
            data = json.load(file_g)
            for player_e in data['players']:
                players_id.append(data['players'][player_e]['id'])
    return players_id
