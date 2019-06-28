from model import mantis_project


def delete_random_project(app, project):
    app.mantis_project.delete_project(project)


def test_delete_project(app, orm):
    app.session.open_main_page()
    app.session.ensure_login(username=app.username, password=app.password)
    app.navigation.open_manage_projects_page()
    projects_before = orm.get_all_projects()
    project = orm.get_random_project()
    delete_random_project(app=app, project=project)
    projects_after = orm.get_all_projects()
    projects_before.remove(project)
    assert sorted(projects_before, key=mantis_project.id_or_max) == sorted(projects_after, key=mantis_project.id_or_max)

