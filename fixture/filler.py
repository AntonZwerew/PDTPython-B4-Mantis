from selenium.webdriver.support.ui import Select


class FillerHelper:

    def __init__(self, app):
        self.app = app

    def fill_input_field(self, element, text):
        wd = self.app.wd
        wd.find_element_by_name(element).click()
        wd.find_element_by_name(element).clear()
        wd.find_element_by_name(element).send_keys(text)

    def fill_photo_field(self, element, text):
        # закомментировал клик, т.к. если их оставить - тест падает, по идее оставшееся эквивалентно перетаскиванию
        wd = self.app.wd
        wd.find_element_by_name(element).clear()
        wd.find_element_by_name(element).send_keys(text)

    def fill_dropdown_list(self, element, text):
        wd = self.app.wd
        wd.find_element_by_name(element).click()
        Select(wd.find_element_by_name(element)).select_by_visible_text(text)
