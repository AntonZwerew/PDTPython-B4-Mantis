from generator import generator


def random_username():
    return generator.random_string_only_letters(prefix="user", maxlen=10)


def random_password():
    return generator.random_string_only_letters(prefix="pass", maxlen=10)


