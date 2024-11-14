from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="📝 Создать лобби", callback_data="generate_lobby"),
     InlineKeyboardButton(text="🔎 Войти в лобби", callback_data="find_lobby")],
    [InlineKeyboardButton(text="💎 Статистика", callback_data="statistics")]
]
menu_kb = InlineKeyboardMarkup(inline_keyboard=menu)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Отмена", callback_data="menu")]])
