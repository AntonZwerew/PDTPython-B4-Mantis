import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + '''string.punctuation''' + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(0, maxlen)])

