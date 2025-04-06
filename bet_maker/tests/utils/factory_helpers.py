import random
import string


def generate_random_string(length: int = 8) -> str:
    """
    Generate a random string of a given length.

    :param length: Length of the string to generate (default is 8).
    :return: A random string of the specified length.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
