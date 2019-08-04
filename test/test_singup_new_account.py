def test_singup_new_account(app):
    username = "user1"
    password = "user1"
    app.james.ensure_user_exists(username, password)