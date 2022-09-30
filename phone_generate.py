import random

from functools import partial


def gen_phone_numb():
    a = partial(random.randint, 0, 9)
    gen = lambda: "+7-{}{}{}-{}{}{}-{}{}{}{}".format(a(), a(), a(), a(), a(), a(), a(), a(), a(), a())
    phone_num = gen()
    return phone_num


if __name__ == "__main__":
    gen_phone_numb()