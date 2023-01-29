import random
import util
import math
from math import log
from line import Line

class TLB:
    def __init__(self):
        self.page_number = []
        self.block_number = []

class Cache:
    # Replacement policies
    LRU = "LRU"
    LFU = "LFU"
    FIFO = "FIFO"

    virtual_address_bit = 24
    physical_address_bit = 16

    def __init__(self, size, mem_size, block_size, mapping_pol, replace_pol,
                 write_pol):
        self._lines = [Line(block_size) for i in range(size // block_size)]

        self._mapping_pol = mapping_pol  # Mapping policy
        self._replace_pol = replace_pol  # Replacement policy
        self._write_pol = write_pol  # Write policy

        self._size = size  # Cache size
        self._mem_size = mem_size  # Memory size
        self._block_size = block_size  # Block size

        # Bit offset of cache line tag
        self._tag_shift = int(log(self._size // (self._mapping_pol*block_size), 2))
        # Bit offset of cache line set
        self._set_shift = int(log(self._block_size, 2))
        self.tlb = TLB()

    def read(self, address):
        """Read a block of memory from the cache.
        """
        tag = self._get_tag(address)  # Tag of cache line
        set = self._get_set(address)  # Set of cache lines
        line = None

        # Search for cache line within set
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Update use bits of cache line
        if line:
            if (self._replace_pol == Cache.LRU or
                self._replace_pol == Cache.LFU):
                self._update_use(line, set)

        return line.data if line else line

    def load(self, block, address, data):
        """Load a block of memory into the cache.
        """
        tag = self._get_tag(block)  # Tag of cache line
        set = self._get_set(address)  # Set of cache lines
        victim_info = None

        # choose the victim to replace

        victim = set[0]

        for index in range(len(set)):
            if set[index].use < victim.use:
                victim = set[index]

        victim.use = 0

        if self._replace_pol == Cache.FIFO:
            self._update_use(victim, set)


        # Store victim info if modified
        if victim.modified:
            victim_info = (index, victim.data)

        # Replace victim
        victim.modified = 0
        victim.valid = 1
        victim.tag = tag
        victim.data = data

        return victim_info

    def write(self, address, byte):
        """Write a byte to cache.
        """
        tag = self._get_tag(address)  # Tag of cache line
        set = self._get_set(address)  # Set of cache lines
        line = None

        # Search for cache line within set
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Update data of cache line
        if line:
            line.data[self.get_offset(address)] = byte
            line.modified = 1

            if (self._replace_pol == Cache.LRU or
                self._replace_pol == Cache.LFU):
                self._update_use(line, set)

        return True if line else False

    def print_section(self, start, amount):
        """Print a section of the cache.
        """
        line_len = len(str(self._size // self._block_size - 1))
        use_len = max([len(str(i.use)) for i in self._lines])
        tag_len = int(log(self._mapping_pol * self._mem_size // self._size, 2))
        address_len = int(log(self._mem_size, 2))

        if start < 0 or (start + amount) > (self._size // self._block_size):
            raise IndexError

        print("\n" + " " * line_len + " " * use_len + " U M V T" +
              " " * tag_len + "<DATA @ ADDRESS>")

        for i in range(start, start + amount):
            print(util.dec_str(i, line_len) + ": " +
                  util.dec_str(self._lines[i].use, use_len) + " " +
                  util.bin_str(self._lines[i].modified, 1) + " " +
                  util.bin_str(self._lines[i].valid, 1) + " " +
                  util.bin_str(self._lines[i].tag, tag_len) + " <" +
                  " ".join([util.hex_str(i, 2) for i in self._lines[i].data]) + " @ " +
                  util.bin_str(self.get_physical_address(i), address_len) + ">")
        print()

    def get_physical_address(self, index):
        """Get the physical address of the cache line at index.
        """
        set_num = index // self._mapping_pol

        return ((self._lines[index].tag << self._tag_shift) +
                (set_num << self._set_shift))

    def get_offset(self, address):
        """Get the offset from within a set from a physical address.
        """
        return address & (self._block_size - 1)

    def _get_tag(self, address):
        """Get the cache line tag from a physical address.
        """
        return address >> self._tag_shift

    def _get_set(self, address):
        """Get a set of cache lines from a physical address.
        """
        index = address * self._mapping_pol
        return self._lines[index:index + self._mapping_pol]

    def _update_use(self, line, set):
        """Update the use bits of a cache line.
        """
        if (self._replace_pol == Cache.LRU or
            self._replace_pol == Cache.FIFO):
            use = line.use

            if line.use < self._mapping_pol:
                line.use = self._mapping_pol
                for other in set:
                    if other is not line and other.use > use:
                        other.use -= 1
        elif self._replace_pol == Cache.LFU:
                line.use += 1

    def find_page(self, page_number):
        if page_number in self.tlb.page_number:
            data = self.tlb.block_number[self.tlb.page_number.index(page_number)]
            return True, data
        else:
            print('Fail to find page number in TLB')
            return False, None

    def update_tlb(self, page_number, memory_page_number):
        self.tlb.page_number.append(page_number)
        self.tlb.block_number.append(memory_page_number)

    def load_page(self, start_block, block_num, data):
        """Load a page of memory into the cache.
        """
        start_index = 0
        for block in range(start_block, start_block+block_num):
            width = Cache.physical_address_bit - int(math.log2(self._block_size))
            bi_block = util.bin_str(block, width)  # block address in binary form
            cache_block_res = int(math.log2(self._size // (self._mapping_pol * self._block_size)))

            address = int(bi_block[(width - cache_block_res):], 2)  # block address in cache
            self.load(block, address, data[start_index:start_index+self._block_size])
            start_index += self._block_size
        return

    def load_toy(self, block, address, data):
        """Load a block of memory into the cache.
        """
        tag = self._get_tag(block)  # Tag of cache line
        set = self._get_set(address)  # Set of cache lines
        victim_info = None

        # choose the victim to replace

        victim = set[0]

        for index in range(len(set)):
            if set[index].use < victim.use:
                pass

        victim.use = 0

        # Store victim info if modified
        if victim.modified:
            victim_info = (index, victim.data)

        # Replace victim
        victim.modified = 0
        victim.valid = 1
        victim.tag = tag
        victim.data = data

        return victim_info