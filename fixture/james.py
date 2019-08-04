from telnetlib import Telnet


class JamesHelper:
    def __init__(self, app):
        self.app = app

    class Session:
        def __init__(self, host, port, username, password, timeout=5):
            self.telnet = Telnet(host, port, timeout)
            self.read_until("Login id:")
            self.write(username)
            self.read_until("Password:")
            self.write(password)
            self.read_until("Welcome %s. HELP for a list of commands" % username)

        def read_until(self, text, timeout=5):
            self.telnet.read_until(text.encode("ascii"), timeout)

        def write(self, text):
            self.telnet.write((text + "\n").encode("ascii"))

        def is_user_exist(self, username):
            self.write("verify %s" % username)
            result = self.telnet.expect([b"exists", b"does not exist"])
            return result[0] == 0

        def create_user(self, username, password, timeout=5):
            self.write("adduser %s %s" % (username, password))
            self.read_until("User %s added" % username)

        def reset_password(self, username, password, timeout=5):
            self.write("setpassword %s %s" % (username, password))
            self.read_until("Password for %s reset" % username)

        def quit(self):
            self.write("quit")

    def ensure_user_exists(self, username, password):
        config = self.app.config["james"]
        session = JamesHelper.Session(config["host"], config["port"], config["username"], config["password"])
        if session.is_user_exist(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

