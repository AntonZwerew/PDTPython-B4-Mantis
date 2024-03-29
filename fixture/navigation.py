class NavigationHelper:

    def __init__(self, app):
        self.app = app

    def open_manage_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_overview_page.php"):
            wd.find_element_by_link_text("Manage").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            self.open_manage_page()
            wd.find_element_by_link_text("Manage Projects").click()

