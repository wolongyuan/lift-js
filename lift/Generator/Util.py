import string
import random


generated = []


def rand_bytes(size=10, chars=string.ascii_uppercase + string.digits):
    while True:
        res = ''.join(random.choice(chars) for _ in range(size))
        if res not in generated:
            generated.append(res)
            return res
