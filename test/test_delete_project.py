from model import mantis_project
import allure


def delete_random_project(app, project):
    app.mantis_project.delete_project(project)


def test_delete_project(app, orm):
    with allure.step("Open projects page:"):
        app.session.open_main_page()
        app.session.ensure_login(username=app.username, password=app.password)
        app.navigation.open_manage_projects_page()
        projects_before = orm.get_all_projects()
    with allure.step("Delete random project:"):
        project = orm.get_random_project()
        delete_random_project(app=app, project=project)
        projects_after = orm.get_all_projects()
        projects_before.remove(project)
    with allure.step("Check project removing correctly:"):
        assert sorted(projects_before, key=mantis_project.id_or_max) == \
               sorted(projects_after, key=mantis_project.id_or_max)
        assert sorted(app.soap.get_all_projects(app.username, app.password), key=mantis_project.id_or_max) == \
               sorted(projects_before, key=mantis_project.id_or_max)

