import itertools
import string
import random


def get_variant_combination(*args):
    """
    This function generates the combinations for variants e.g
    args: ['black', 'green'], ['xl', 'l']

    returns: [('black', 'xl'), ('black', 'l'), ('blue', 'xl'), ('blue', 'l')]
    """
    return [p for p in itertools.product(*args)]


def generate_string_of_length(string_length: int = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=string_length))


