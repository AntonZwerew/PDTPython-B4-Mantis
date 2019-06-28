from selenium import webdriver
from fixture.session import SessionHelper
from fixture.filler import FillerHelper
from fixture.navigation import NavigationHelper
from fixture.mantis_project import MantisProjectHelper


class Application:
    def __init__(self, browser, base_url, username, password):
        if browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "firefox":
            self.wd = webdriver.Firefox()
        else:
            raise ValueError("Unknown browser: %s" % browser)
        # self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.filler = FillerHelper(self)
        self.navigation = NavigationHelper(self)
        self.mantis_project = MantisProjectHelper(self)
        self.base_url = base_url
        self.username = username
        self.password = password

    def is_valid(self):
        try:
            self.wd.current_url
            self.session.ensure_login(username=self.username, password=self.password)
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()
