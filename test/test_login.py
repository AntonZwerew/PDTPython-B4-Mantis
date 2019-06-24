def test_login(app):
    app.session.ensure_logout()
    app.session.login(username=app.username, password=app.password)
    assert app.session.is_logged_in_as(app.username)
