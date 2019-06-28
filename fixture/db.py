import mysql.connector


class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password,
                                                  autocommit=True, buffered=True)
        # без buffered запрос всех данных контакта выдает Unread Result

    def destroy(self):
        self.connection.close()

