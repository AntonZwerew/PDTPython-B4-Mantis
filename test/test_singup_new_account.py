import allure
from generator import user_generator


def test_signup_new_account(app):
    with allure.step("Generate random account:"):
        username = user_generator.random_username()
        password = user_generator.random_password()
        email = username + "@localhost"
        app.james.ensure_user_exists(username, password)
    with allure.step("Sing up new user:"):
        app.signup.signup_new_user(username, email, password)
    with allure.step("Check user can login:"):
        assert app.soap.can_login(username, password)
