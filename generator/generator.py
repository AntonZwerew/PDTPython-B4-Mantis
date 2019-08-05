import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + '''string.punctuation''' + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(0, maxlen)])


def random_string_only_letters(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(0, maxlen)])
