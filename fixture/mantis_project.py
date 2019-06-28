class MantisProjectHelper:
    def __init__(self, app):
        self.app = app

    def add_project(self, project):
        wd = self.app.wd
        self.app.navigation.open_manage_projects_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.app.filler.fill_input_field(element="name", text=project.name)
        self.app.filler.fill_dropdown_list(element="status", text=project.status)
        if not project.global_categories:
            self.app.filler.fill_checkbox(element="inherit_global", state=project.global_categories)
        self.app.filler.fill_dropdown_list(element="view_state", text=project.view_status)
        self.app.filler.fill_input_field(element="description", text=project.description)
        wd.find_element_by_css_selector("[value='Add Project']").click()

    def delete_project(self, project):
        wd = self.app.wd
        wd.find_element_by_link_text(project.name).click()  # id нельзя взять из свойств, а имя должно быть уникальным
        wd.find_element_by_css_selector("[value='Delete Project']").click()
        wd.find_element_by_css_selector("[value='Delete Project']").click()


