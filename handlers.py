from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import kb
import text
import utils
from states import *

router = Router()

from main import bot


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.menu_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    for message in utils.exit_game(msg.from_user.id):
        print(message)
        await bot.send_message(*message)

    await msg.answer(text.menu, reply_markup=kb.menu_kb)


@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    for message in utils.exit_game(clbck.from_user.id):
        print(message)
        await bot.send_message(*message)
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu_kb)


@router.callback_query(F.data == "generate_lobby")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Lobby.lobby)
    game = utils.Game()
    game.add_member(clbck.from_user.first_name, clbck.from_user.id)
    player = utils.Player()
    player.add_info(clbck.from_user.id, clbck.from_user.first_name, f'game_{game.game_info['token']}')
    await state.set_data({"game": game})
    game.create_json()
    player.create_json()
    await clbck.message.edit_text(text.start_lobby.format(tok=game.game_info['token']), reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "find_lobby")
async def menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Login.login_lobby)
    player = utils.Player()
    player.add_info(clbck.from_user.id, clbck.from_user.first_name, '')
    player.create_json()

    await clbck.message.edit_text(text.login_lobby, reply_markup=kb.iexit_kb)


@router.message(StateFilter(Login.login_lobby))
async def find_lobby(msg: Message):
    data_lb = utils.find_lobby(msg.text, data=1)
    data_pl = utils.find_player(msg.from_user.id)
    if data_lb:
        await msg.answer(text.lobby_successfully.format(name=list(data_lb['players'].keys())[0]))
        game = utils.Game(data_lb)
        game.add_member(msg.from_user.first_name, msg.from_user.id)
        game.create_json()
        player = utils.Player(data_pl)
        player.add_game(f'game_{data_lb['token']}')
        player.create_json()
    else:
        await msg.answer("Лобби не найдено")


@router.callback_query(F.data == "statistics")
async def statistic(clbck: CallbackQuery):
    await clbck.message.edit_text(text.statistics, reply_markup=kb.iexit_kb)
