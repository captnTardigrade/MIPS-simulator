import math
from enum import Enum
import globalVariables

class MagicNumbers(Enum):
    TAGS = 0
    BLOCK = 1
    VALID = 2
    COUNTER = 3


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
        self.valid = 0
        self.tag = 0
        self.counter = 0
        self.mySet = [[self.tag, self.block, self.valid, self.counter]
                      for _ in range(self.associativity)]
        self.cache = [self.mySet for _ in range(self.numSets)]

        self.offsetBits = int(math.log2(self.blockSize))
        self.indexBits = int(math.log2(self.numSets))
        self.address = globalVariables.ADDRESS_BITS
        self.tagBits = globalVariables.ADDRESS_BITS - \
            self.indexBits - self.offsetBits

    def search(self, address):
        '''
        description:
            searches for the given address in the cache
        returns:
            (any) the value if it is present in the cache
            else, returns False
        '''
        globalVariables.totalCacheAccesses += 1
        tag, index, offset = self.getLocation(address)
        theSet = self.cache[index]
        try:
            blockIndex = theSet[MagicNumbers.TAGS.value].index(tag)
            if theSet[blockIndex][MagicNumbers.VALID.value] == 1:
                globalVariables.numCacheHits += 1
                temp = theSet[blockIndex][MagicNumbers.COUNTER.value]
                theSet[blockIndex][MagicNumbers.COUNTER.value] = self.numBlocks - 1
                for b in theSet:
                    if b[MagicNumbers.COUNTER.value] > temp:
                        b[MagicNumbers.COUNTER.value] -= 1
                return theSet[blockIndex][MagicNumbers.BLOCK.value][offset]
            return False
        except ValueError:
            return False

    def updateCache(self, address, blockNumber):
        '''
        description:
            updates the cache at the given location with new information
        parameters:
            address: (str) address of the value in binary
            blockNumber: (int) index of the block in the set to be replaced with
            newBlock: (list) new block to be replaced with at the given location

        returns: None
        '''
        globalVariables.totalCacheAccesses += 1
        tag, index, offset = self.getLocation(address)
        self.cache[index][blockNumber][MagicNumbers.TAGS.value] = tag
        self.cache[index][blockNumber][MagicNumbers.BLOCK.value] = self.getBlock(address)
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
        tag = int(address[:self.tagBits], base=2)
        index = int(address[self.tagBits:self.tagBits+self.indexBits], base=2)
        offset = int(address[-self.offsetBits:], base=2)

        return (tag, index, offset)

    def getBlock(self, address):
        start = int(address, base=2)
        return globalVariables.memory[start:start+self.blockSize*4:4]

    def isFull(self):
        count = 0
        for s in self.cache:
            for b in s:
                count += b[MagicNumbers.VALID.value]
        return count == self.numBlocks


if __name__ == "__main__":
    cache = Cache(16, 256, 4, 2)
