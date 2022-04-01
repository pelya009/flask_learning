import random
import uuid


def generate_name(pref: str = 'auto'):
    return pref + str(uuid.uuid4())[:8]


def rand_float():
    return round(random.uniform(0, 1000), 2)
