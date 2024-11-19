from aiogram.fsm.state import StatesGroup, State


class Lobby(StatesGroup):
    lobby = State()
    start_lobby = State()


class Login(StatesGroup):
    login_lobby = State()
    wait_start = State()


class Game(StatesGroup):
    game = State()
