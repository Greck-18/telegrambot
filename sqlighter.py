import sqlite3


class SQLighter:
    ''' класс базы данных для пользователей , со статусом подписки'''

    def __init__(self, database):
        # привязка к базе данных и создание курсора
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute("INSERT INTO subscribers(user_id,status) VALUES(?,?)", (user_id, status))

    def update_subscriber(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE subscribers SET status=? WHERE user_id=?", (status, user_id))

    def get_subscriptions(self, status=True):
        # выборка всех пользователей из бд , кто подписан
        with self.connection:
            return self.cursor.execute("SELECT * FROM subscribers WHERE status=?", (status,)).fetchall()

    def subscribers_exists(self, user_id):
        # проверка на подписку
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subscribers WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def close(self):
        # дисконект с базой данных
        self.connection.close()
