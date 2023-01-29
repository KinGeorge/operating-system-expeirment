import random
random.seed(10)


def rand_byte():
    """Get a random byte.
    """
    return random.randint(0, 0xFF)

def odd_even_mix_byte(odd_data, even_data, block_size):
  """ Get a odd and even specific byte.
  """
  while True:
    for _ in range(block_size):
        yield even_data
    for _ in range(block_size):
        yield odd_data

def dec_str(integer, width):
    """Get decimal formatted string representation of an integer.
    """
    return "{0:0>{1}}".format(integer, width)

def bin_str(integer, width):
    """Get binary formatted string representation of an integer.
    """
    return "{0:0>{1}b}".format(integer, width)

def hex_str(integer, width):
    """Get hexadecimal formatted string representation of an integer.
    """
    return "{0:0>{1}X}".format(integer, width)
