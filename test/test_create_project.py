from generator.project_generator import random_project


def test_create_correct_project(app, orm):
    app.session.open_main_page()
    app.session.ensure_login(username=app.username, password=app.password)
    app.navigation.open_manage_projects_page()
    projects_before = orm.get_all_projects()
    while True:
        project = random_project()
        if project.name not in (p.name for p in projects_before):
            break
    # в ходе теста встретил invalid security token error, не жо конца понял как появляется и как избежать
    # Возможно, это истекший срок годности токена, например если включить отладчик после логина и оставить на время
    # Т.к. других причин появления не вижу, обрабатывать не стал - специфичный случай, в тестах встретиться не должен
    app.mantis_project.add_project(project)
    projects_after = orm.get_all_projects()
    projects_before.append(project)
    assert projects_before == projects_after
    # assert app.soap.get_all_projects(app.username, app.password) == projects_before

