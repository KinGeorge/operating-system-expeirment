import util
import random
random.seed(10)

class Page:
    def __init__(self, page_number, valid_number=4):
        self.valid = [0 for i in range(page_number)]
        self._data = random.sample(range(0, page_number),page_number)
        for i in range(valid_number):
            # Only First [valid_number] of the Page Table is Valid
            self.valid[i] = 1


class Memory:

    def __init__(self, size, block_size, page_size):

        self._size = size  # Memory size
        self._block_size = block_size  # Block size
        self._page_size = page_size  # Page size

        iter = util.odd_even_mix_byte(0x55, 0xAA, block_size) # If use mix data
        self._data = [next(iter) for i in range(size)]

        self._page_mapping = Page(self._size//self._page_size)

    def print_section(self, start, amount):
        """Print a section of main memory.
        """
        address_len = len(str(self._size - 1))
        start = start - (start % self._block_size)
        amount *= self._block_size

        if start < 0 or (start + amount) > self._size:
            raise IndexError

        print()
        for i in range(start, start + amount, self._block_size):
            print(util.dec_str(i, address_len) + ": " +
                  " ".join([util.hex_str(i, 2) for i in self.get_block(i)]))
        print()


    def print_first_byte(self, start):
        """Print first byte of a memory block
        """
        amount = self._block_size
        address_len = len(str(self._size - 1))

        if start < 0 or (start + amount) > self._size:
            raise IndexError

        print()
        print('BLOCK ' + str(start) + ": " +
                  str(util.hex_str(self.get_block(start*self._block_size)[0], 2)))
        print()

    def get_block(self, address):
        """Get the block of main memory contains
        the byte at address.
        """
        start = address - (address % self._block_size)  # Start address
        end = start + self._block_size  # End address

        if start < 0 or end > self._size:
            raise IndexError

        return self._data[start:end]

    def set_block(self, address, data):
        """Set the block of main memory contains
        the byte at address.
        """
        start = address - (address % self._block_size)  # Start address
        end = start + self._block_size  # End address

        if start < 0 or end > self._size:
            raise IndexError

        self._data[start:end] = data

    def find_page(self, page_index):
        if self._page_mapping.valid[page_index] == 0:
            print('Fail to find page in memory')
            return False, None, None
        else:
            page = self._page_mapping._data[page_index]
            print('The Corresponding Page in Cache is: ', page)
            return True, page, self._data[page*self._page_size:(1+page)*self._page_size]

    def set_page(self, page_number, data):
        self._page_mapping.valid[page_number] = 1
        memory_page_number = self._page_mapping._data[page_number]
        address = memory_page_number * self._page_size
        start = address - (address % self._block_size)  # Start address
        end = start + self._page_size  # End address

        if start < 0 or end > self._size:
            raise IndexError
        self._data[start:end] = data