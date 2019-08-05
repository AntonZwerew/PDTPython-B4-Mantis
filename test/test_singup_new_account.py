from generator import user_generator


def test_signup_new_account(app):
    username = user_generator.random_username()
    password = user_generator.random_password()
    email = username + "@localhost"
    app.james.ensure_user_exists(username, password)
    app.signup.signup_new_user(username, email, password)
    assert app.soap.can_login(username, password)
