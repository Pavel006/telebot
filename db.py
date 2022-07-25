#import sqlite3

class BotD:

    def __init__(self, db_file):
        """Инициализация с БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, id_user):
        """Проверяем, есть ли пользователь в БД"""
        result = self.cursor.execute("SELECT `id_user` FROM `users` WHERE `id_user` = (?)", (id_user,))
        return bool(len(result.fetchall()))

    def get_user_balance(self, id_user):
        """Получаем баланс пользователя"""
        result = self.cursor.execute("SELECT `balance` FROM `users` WHERE `id_user` = (?)", (id_user,))
        return result.fetchone()[0]

    def add_user(self, id_user):
        """Добавляем пользователся в БД"""
        self.cursor.execute("INSERT INTO `users` (`id_user`, `balance`) VALUES (?,?)", (id_user, 25000))
        return self.conn.commit()

    def add_admin(self, id_user):
        """Добавляем администратора в БД"""
        self.cursor.execute("INSERT INTO `admins` (`id_admin`) VALUES (?)", (id_user,))
        return self.conn.commit()

    def add_sector(self, id_user, sector):
        """Добавляем сектор, на который поставил пользователь"""
        self.cursor.execute("UPDATE `users` SET `sector` = (?) WHERE `id_user` = (?)", (sector, id_user))
        return self.conn.commit()

    def add_bet(self, id_user, bet):
        """Добавляем сумму ставки, на который поставил пользователь"""
        self.cursor.execute("UPDATE `users` SET `bet` = (?) WHERE `id_user` = (?)", (bet, id_user))
        return self.conn.commit()

    def add_balance(self, id_user, balance):
        """Добавляем сумму ставки, на который поставил пользователь"""
        self.cursor.execute("UPDATE `users` SET `balance` = (?) WHERE `id_user` = (?)", (balance, id_user))
        return self.conn.commit()

    def user_exists(self, id_user):
        """Проверяем, наличие прав администратора"""
        result = self.cursor.execute("SELECT `id_admin` FROM `admins` WHERE `id_admin` = ?", (id_user,))
        return bool(len(result.fetchall()))

    def get_sector(self, id_user):
        """Получаем информацию о секторе"""
        result = self.cursor.execute("SELECT `sector` FROM `users` WHERE `id_user` = (?)", (id_user,))
        return result.fetchall()[0]

    def get_bet(self, id_user):
        """Получаем информацию о ставке"""
        result = self.cursor.execute("SELECT `bet` FROM `users`WHERE `id_user` = (?)", (id_user,))
        return result.fetchone()[0]

    def get_users(self):
        """Получаем информацию о всех пользователях"""
        result = self.cursor.execute("SELECT `id_user`, `bet`, `sector`, `balance`  FROM `users`")
        return result.fetchall()

    def get_users_one(self, id_user):
        """Получаем информацию об определенном пользователе"""
        result = self.cursor.execute("SELECT `id_user`, `bet`, `sector`, `balance` FROM `users` WHERE `id_user` = (?)",
                                     (id_user,))
        return result.fetchall()

    def get_admins(self):
        """Получаем информацию о всех администраторах"""
        result = self.cursor.execute("SELECT `id_admin` FROM `admins`")
        return result.fetchall()

    def get_coins(self, id_user, coins):
        """Добавляем сумму ставки, на который поставил пользователь"""
        self.cursor.execute("UPDATE `users` SET `balance` = (?) WHERE `id_user` = (?)", (coins, id_user))
        return self.conn.commit()

    def giv_coins(self, id_user):
        """Выдать фантики пользователю"""
        self.cursor.execute("UPDATE `users` SET `balance` = (?) WHERE `id_user` = (?)", (25000, id_user))

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
