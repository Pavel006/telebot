import config
import logging
from aiogram import Bot, Dispatcher, executor, types

import markups
import random
from db import BotD
import re
import time

BotDB = BotD('database.db')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if BotDB.get_users_one(message.from_user.id) == False:
        BotDB.add_user(message.from_user.id)
        await bot.send_message(865986613,
                               f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                               f"@{message.from_user.username}"
                               f"Зарегестрировался")
        await message.bot.send_message(message.from_user.id, "Добро пожаловать!\n "
                                                         "Вы зарегестрировались в Казино Боте\n"
                                                         "Ваш стартовый баланс: 25.000 фантиков")
        await message.bot.send_message(message.from_user.id, "Для того чтобы начать играть\n"
                                                             "Нажмите кнопку 'Начать играть'")
        await message.bot.send_message(message.from_user.id, "Основная информация: \n"
                                                             "Чтобы посмотреть свой баланс нажмите кнопку 'Баланс'.\n"
                                                             "Чтобы начать игру вам необходимо нажать кнопку 'Начать игру'.\n"
                                                             "После нажатия кнопки 'Начать игру', выберите сектор на который хотите поставить.\n"
                                                             "Для этого вам понадобиться ввести ' /sector *Название сектора* '.\n"
                                                             "Выбрав сектор, сделайте ставку.\n"
                                                             "Это делается с помощью команды ' /bet *Сумма ставки*'."
                                                             "Выполнив все выше описанные операции нажмите конпу 'Крутить рулетку'\n"
                                                             "Посмотреть основную информацию повторно можно будет с помощью команды ' /info '",
                                       reply_markup=markups.mainMenu)

    else:
        await bot.send_message(message.from_user.id, "С возврощением!!!\n"
                                                     "Если вы забыли как пользоваться ботом введите команду ' /info '", reply_markup=markups.mainMenu)

@dp.message_handler(commands=['info'])
async def gameInfo(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Основная информация: \n"
                                                         "Чтобы посмотреть свой баланс нажмите кнопку 'Баланс'.\n"
                                                         "Чтобы начать игру вам необходимо нажать кнопку 'Начать игру'.\n"
                                                         "После нажатия кнопки 'Начать игру', выберите сектор на который хотите поставить.\n"
                                                         "Для этого вам понадобиться ввести ' /sector *Название сектора* '.\n"
                                                         "Выбрав сектор, сделайте ставку.\n"
                                                         "Это делается с помощью команды ' /bet *Сумма ставки*'.\n"
                                                         "Выполнив все выше описанные операции нажмите конпу 'Крутить рулетку'\n"
                                                         "Если на вашем балансе мало средст или вы хотите сбросить свой баланс\n"
                                                         "Вы можете ввести комманду ' /give_coins ',\n"
                                                         "После чего вашь обнулиться до 25.000 фантиков\n"
                                                         "Обнуление произойдет не сразу.\n"
                                                         "Вы не сможете пользоваться ботом 2 часа.")
@dp.message_handler(commands=['getUsers'])
async def info(message: types.Message):
    i = 0
    if BotDB.user_exists(message.from_user.id) == False:
        await bot.send_message(message.from_user.id, "У вас нет прав администратора!!!")
    else:
        while i < len(BotDB.get_users()):
            await bot.send_message(message.from_user.id, f"ID пользователя: "
                                                         f"{BotDB.get_users()[i][0]}\n"
                                                         f"Баланс пользователя : "
                                                         f"{BotDB.get_users()[i][3]}\n")
            i += 1

@dp.message_handler(commands=['getAdmins'])
async def info(message: types.Message):
    i = 0
    if BotDB.user_exists(message.from_user.id) == False:
        await bot.send_message(message.from_user.id, "У вас нет прав администратора!!!")
    else:
        while i < len(BotDB.get_admins()) - 1:
            await bot.send_message(865986613, f"[INFO] Администратор  "
                                              f"'{message.from_user.first_name} {message.from_user.last_name}'\n"
                                              f"@{message.from_user.username}\n"
                                              f"Вызвал команду 'getAdmins'")
            await bot.send_message(message.from_user.id, f"ID администратора:"
                                                         f" {BotDB.get_users_one(BotDB.get_admins()[i][0])[i][0]}\n"
                                                         f"Баланс пользователя : "
                                                         f"{BotDB.get_users_one(BotDB.get_admins()[i][0])[i][3]}\n")
            i += 1

@dp.message_handler(commands=['sector'])
async def start(message: types.Message):
    BotDB.add_sector(message.from_user.id, message.text.strip("/sector "))
    if BotDB.get_bet(message.from_user.id) == 0:
        await bot.send_message(message.from_user.id, "Теперь введите сумму ставки")
    else:
        await bot.send_message(message.from_user.id, "Нажмите 'Крутить рулетку'")

    print(message.text.strip("/sector "), " @", message.from_user.username)

@dp.message_handler(commands=['get_coins'])
async def start(message: types.Message):
    if BotDB.user_exists(message.from_user.id) == False:
        await bot.send_message(message.from_user.id, "У вас нет прав администратора!!!")
    else:
        await bot.send_message(865986613,
                               f"[INFO] Администратор '{message.from_user.first_name} {message.from_user.last_name}'\n"
                               f"@{message.from_user.username}\n"
                               f"Вызвал команду 'get_coins'\n"
                               f"Изменив свой счет на {message.text.strip('/get_coins ')}")
        BotDB.get_coins(message.from_user.id, message.text.strip('/get_coins '))

@dp.message_handler(commands=['bet'])
async def start(message: types.Message):
    BotDB.add_bet(message.from_user.id, message.text.strip("/bet "))
    if BotDB.get_bet(message.from_user.id) == 0:
        await bot.send_message(message.from_user.id, "Теперь ввдите сектор")
    else:
        await bot.send_message(message.from_user.id, "Нажмите 'Крутить рулетку'")
    print(message.text.strip("/bet "), " @", message.from_user.username)

@dp.message_handler(commands=['give_coins'])
async def give_coins(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы захотели обнулить счет\n"
                                                 "и теперь вы не можете пользоваться ботом 2 часа.\n"
                                                 "По истечению этого времени на вашем балансе будет 25.000 фантиков.")
    i = 1
    while i <= 4:
        time.sleep(10)
        if i == 1:
            await bot.send_message(message.from_user.id, "Остался 1 час 30 минут")
        elif i == 2:
            await bot.send_message(message.from_user.id, "Остался 1 час")
        elif i == 3:
            await bot.send_message(message.from_user.id, "Остался 30 минут")
        i += 1
    BotDB.giv_coins(message.from_user.id)
    await bot.send_message(message.from_user.id, "Поздравляю, на вашем счету 25.000 фантиков.")

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == 'Баланс':
        await bot.send_message(message.from_user.id, f"Ваш баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
    if message.text == 'Начать игру':
        photo = open('C:/Users/79877/PycharmProjects/pythonProject/img/Table.png', 'rb')
        await bot.send_photo(message.from_user.id, photo)

    if message.text == "Крутить рулетку":
        await bot.send_message(message.from_user.id, "Рулетка крутиться")
        time.sleep(1)
        await bot.send_message(message.from_user.id, "Результа через...")
        i = 1
        while i <= random.randint(4 , 15):
            await bot.send_message(message.from_user.id, str(i))
            i += 1
            time.sleep(1)
        randomNumber = int(random.randint(0, 36))
        userAnswer1 = str(BotDB.get_sector(message.from_user.id))
        userAnswer = userAnswer1.strip("( ' , )")
        userBalance = float(BotDB.get_user_balance(message.from_user.id)) - BotDB.get_bet(message.from_user.id)
        BotDB.add_balance(message.from_user.id, userBalance)

        await bot.send_message(message.from_user.id, "Выпало число: " + str(randomNumber))

        if userAnswer == randomNumber:
            revard = BotDB.get_bet(message.from_user.id) * 35
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")

        elif (userAnswer == "1ST12" and randomNumber >= 1 and randomNumber <= 12):
            revard = BotDB.get_bet(message.from_user.id) * 2
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
        elif (userAnswer == "2ND12" and randomNumber >= 13 and randomNumber <= 24):
            revard = BotDB.get_bet(message.from_user.id) * 2
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
        elif (userAnswer == "3RD12" and randomNumber >= 25 and randomNumber <= 36):
            revard = BotDB.get_bet(message.from_user.id) * 2
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")

        elif (userAnswer == "1TO18" and randomNumber >= 1 and randomNumber <= 18):
            revard = BotDB.get_bet(message.from_user.id) * 1.6
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
        elif (userAnswer == "19TO36" and randomNumber >= 19 and randomNumber <= 36):
            revard = BotDB.get_bet(message.from_user.id) * 1.6
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")

        elif (userAnswer == "RED" or userAnswer == "BLACK"):
            if(randomNumber % 2 == 0 and userAnswer == "RED"):
                revard = BotDB.get_bet(message.from_user.id) * 1.6
                userBalance = BotDB.get_user_balance(message.from_user.id)
                BotDB.add_balance(message.from_user.id, userBalance + revard)
                await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
                await bot.send_message(865986613,
                                    f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                    f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
            elif(randomNumber % 2 != 0 and userAnswer == "BLACK"):
                revard = BotDB.get_bet(message.from_user.id) * 1.6
                userBalance = BotDB.get_user_balance(message.from_user.id)
                BotDB.add_balance(message.from_user.id, userBalance + revard)
                await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
                await bot.send_message(865986613,
                                    f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                    f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
            else:
                await bot.send_message(message.from_user.id, "Вы проиграли")

        elif (userAnswer == "EVEN" and randomNumber % 2 == 0):
            revard = BotDB.get_bet(message.from_user.id) * 1.6
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")
        elif (userAnswer == "ODD" and randomNumber % 2 != 0):
            revard = BotDB.get_bet(message.from_user.id) * 1.6
            userBalance = BotDB.get_user_balance(message.from_user.id)
            BotDB.add_balance(message.from_user.id, userBalance + revard)
            await bot.send_message(message.from_user.id, "Вы выйграли: " + str(revard) + " фантиков")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Выйграл: {revard} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")

        else:
            await bot.send_message(message.from_user.id, "Вы проиграли")
            await bot.send_message(865986613,
                                   f"[INFO] Пользователь  '{message.from_user.first_name} {message.from_user.last_name}'\n"
                                   f"@{message.from_user.username}\n"
                                   f"Проиграл: {BotDB.get_bet(message.from_user.id)} фантиков\n"
                                   f"Баланс: {BotDB.get_users_one(message.from_user.id)[0][3]} фантиков")

        BotDB.add_sector(message.from_user.id, "0")
        BotDB.add_bet(message.from_user.id, 0)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
