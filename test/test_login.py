import allure


def test_login(app):
    with allure.step("Logging in:"):
        app.session.ensure_logout()
        app.session.login(username=app.username, password=app.password)
    with allure.step("Check login correct:"):
        assert app.session.is_logged_in_as(app.username)
