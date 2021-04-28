import main
import math
from enum import Enum

class MagicNumbers(Enum):
    TAGS = 0
    BLOCK = 1
    VALID = 2

class Cache:
    def __init__(self, blockSize, cacheSize, associativity, accessLatency):
        # all memory sizes in bytes
        self.blockSize = blockSize
        self.cacheSize = cacheSize
        self.associativity = associativity
        self.accessLatency = accessLatency

        self.numBlocks = self.cacheSize//self.blockSize
        self.numSets = self.numBlocks//self.associativity

        self.block = [None for _ in range(self.blockSize)]
        self.tags = [None for _ in range(self.blockSize)]
        self.valid = [0 for _ in range(self.blockSize)]
        self.mySet = [[self.tags, self.block, self.valid] for _ in range(self.associativity)]
        self.cache = [self.mySet for _ in range(self.numSets)]

        self.offset = int(math.log2(self.blockSize))
        self.index = int(math.log2(self.numSets))
        self.address = int(math.log2(main.MEMORY_SIZE))
        self.tag = int(math.log2(main.MEMORY_SIZE)) - self.index - self.offset

    def search(self, address):
        '''
        description:
            searches for the given address in the cache
        returns:
            (any) the value if it is present in the cache
            else, returns False
        '''
        tag, index, offset = self.getLocation(address)
        theSet = self.cache[index]
        try:
            blockIndex = theSet[MagicNumbers.TAGS.value].index(tag)
            if theSet[blockIndex][MagicNumbers.VALID.value] == 1:
                return theSet[blockIndex][MagicNumbers.BLOCK.value][offset]
            return False
        except ValueError:
            return False

    def updateCache(self, address, blockNumber, newBlock):
        '''
        description:
            updates the cache at the given location with new information
        parameters:
            address: (str) address of the value in binary
            blockNumber: (int) index of the block in the set to be replaced with
            newBlock: (list) new block to be replaced with at the given location
        
        returns: None
        '''
        tag, index, offset = self.getLocation(address)
        self.cache[index][blockNumber][MagicNumbers.TAGS.value] = tag
        self.cache[index][blockNumber][MagicNumbers.BLOCK.value] = newBlock
        self.cache[index][blockNumber][MagicNumbers.VALID.value] = 1

    def getLocation(self, address):
        '''
        description:
            returns the tag, index and offset values for the given address
        parameters:
            address: (str) address in binary

        returns:
            (tuple) (tag, index, offset)
        '''
        tag = int(address[:self.tag], base=2)
        index = int(address[self.tag:self.tag+self.index], base=2)
        offset = int(address[-self.offset:], base=2)

        return (tag, index, offset)


if __name__ == "__main__":
    cache = Cache(4, 256, 4, 2)
    cache.updateCache("000000000000", 0, [1, 2, 3, 4])
    print(cache.search("000000000000"))
