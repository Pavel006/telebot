from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('Главное меню')

# ---- Firs Registration ----


# ---- Main Menu ----
btnStartGame = KeyboardButton('Начать игру')
btnStatistic = KeyboardButton('Баланс')
btnRolle = KeyboardButton('Крутить рулетку')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnStartGame, btnStatistic, btnRolle)