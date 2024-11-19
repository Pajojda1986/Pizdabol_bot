from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="📝 Создать лобби", callback_data="generate_lobby"),
     InlineKeyboardButton(text="🔎 Войти в лобби", callback_data="find_lobby")],
    [InlineKeyboardButton(text="💎 Статистика", callback_data="statistics")]
]

exit_kb_raw = InlineKeyboardButton(text="◀️ Отмена", callback_data="menu")


start_game_raw = [
    [InlineKeyboardButton(text="🎮 Начать игру", callback_data="start_game"),
     exit_kb_raw]
]

menu_kb = InlineKeyboardMarkup(inline_keyboard=menu)

exit_kb = InlineKeyboardMarkup(inline_keyboard=[[exit_kb_raw]])

start_game_kb = InlineKeyboardMarkup(inline_keyboard=start_game_raw)
