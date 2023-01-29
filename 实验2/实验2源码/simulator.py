import math
import util
from cache import Cache
from memory import Memory

def write(address, byte, memory, cache, mode='WB'):
    """Write a byte to cache."""
    written = cache.write(address, byte)

    if written:
        global hits
        hits += 1
    else:
        global misses
        misses += 1

    if mode == Cache.WRITE_THROUGH:
        # Write block to memory
        block = memory.get_block(address)
        block[cache.get_offset(address)] = byte
        memory.set_block(address, block)
    elif mode == Cache.WRITE_BACK:
        if not written:
            # Write block to cache
            block = memory.get_block(address)
            cache.load(address, block)
            cache.write((address, block))
    else:
        print('No such mode')

def find_page(cache, memory, page_number):
    exist_tlb, data = cache.find_page(page_number)
    if exist_tlb:
        global hits
        hits += 1
        print('Find Page in TLB!')
        return data
    else:
        global misses
        misses += 1

    exist, memory_page_number, mem_data = memory.find_page(page_number)
    if exist:
        cache.update_tlb(page_number, memory_page_number)
        start_block = memory_page_number *  (memory._page_size // cache._block_size)
        cache.load_page(start_block, (memory._page_size // cache._block_size), mem_data)
    else:
        data_from_disk = [255 for i in range(memory._page_size)]
        print('Loading from disk')
        memory.set_page(page_number, data_from_disk)

mem_size = 2 ** 16
cache_size = 2 ** 14
block_size = 2 ** 4
page_size = 2 ** 12
mapping = 2 ** 1
virtual_address_bit = 24
physical_address_bit = 16

cache_total_block_num = cache_size // (mapping * block_size)
hits = 0
misses = 0

memory = Memory(mem_size, block_size, page_size)
cache = Cache(cache_size, mem_size, block_size,
              mapping, "LRU", "WB")

mapping_str = "2^{0}-way associative".format(int(math.log2(mapping)))

print("\nMemory size: " + str(mem_size) +
      " bytes (" + str(mem_size // block_size) + " blocks)")
print("Cache size: " + str(cache_size) +
      " bytes (" + str(cache_size // block_size) + " lines)")
print("Block size: " + str(block_size) + " bytes")
print("Mapping policy: " + ("direct" if mapping == 1 else mapping_str) + "\n")


print("="*20, 'Problem 1', "="*20)
print()
print('FIRST 5 BLOCK FROM MEMORY:')
memory.print_section(0, 5)

print('FIRST BYTE FROM BLOCK 28:')
memory.print_first_byte(28)
print('FIRST BYTE FROM BLOCK 29:')
memory.print_first_byte(29)

print("="*20, 'Problem 2', "="*20)
print()
memory._data = [util.rand_byte() for i in range(memory._size)] # or random data
block = 2022 # input block
block_data = memory.get_block(block*block_size) # corresponding data from memory
width = physical_address_bit - int(math.log2(block_size))
bi_block = util.bin_str(block, width) # block address in binary form
cache_block_res = int(math.log2(cache_total_block_num))
tag = bi_block[0:(width-cache_block_res)] # Result of tag of cache

address = int(bi_block[(width-cache_block_res):], 2) # block address in cache
cache.load(block, address, block_data) # load data into cache
print("Corresponding Cache Block Number: ", address)
print("Result of H: ", tag)
print()

print("="*20, 'Problem 3', "="*20)
print()
good_page = 0
bad_page = 5
print('Scenario 1: Find Page Successfully')
find_page(cache, memory, good_page) # find page successfully
print()
print('Scenario 2: Fail to find Page')
find_page(cache, memory, bad_page) # fail to find page
print()

print("="*20, 'Problem 4', "="*20)
print()
address = 256
cache.write(address, 0xFF)
print('Now We need to replace the modified data block.')
sub_block = [0xFF for _ in range(cache._block_size)]

_, modified_data = cache.load_toy(address, address, sub_block)
print(modified_data)
memory.set_block(address*cache._block_size, modified_data)
print()

print("="*20, 'Hit/Miss', "="*20)
print()
ratio = (hits / ((hits + misses) if misses else 1)) * 100

print("\nHits: {0} | Misses: {1}".format(hits, misses))
print("Hit/Miss Ratio: {0:.2f}%".format(ratio) + "\n")

# read again
find_page(cache, memory, good_page)
ratio = (hits / ((hits + misses) if misses else 1)) * 100

print("\nHits: {0} | Misses: {1}".format(hits, misses))
print("Hit/Miss Ratio: {0:.2f}%".format(ratio) + "\n")
