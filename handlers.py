from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
from states import *

import text
import kb

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.menu_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_kb)


@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu_kb)


@router.callback_query(F.data == "generate_lobby")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Lobby.lobby)
    game = utils.Game()
    game.add_member(clbck.from_user.username, clbck.from_user.id)
    await state.set_data({"game": game})
    game.create_json()
    print(game.game_info)
    await clbck.message.edit_text(text.start_lobby.format(tok=game.game_info['token']), reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "find_lobby")
async def menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Login.login_lobby)
    await clbck.message.edit_text(text.login_lobby, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "statistics")
async def statistic(clbck: CallbackQuery):
    await clbck.message.edit_text(text.statistics, reply_markup=kb.iexit_kb)
