import math
from enum import Enum
import globalVariables


class MagicNumbers(Enum):
    TAGS = 0
    BLOCK = 1
    VALID = 2
    COUNTER = 3
    ADDRESS = 4


class Cache:
    def __init__(self, blockSize, cacheSize, associativity, accessLatency, level):
        # all memory sizes in bytes
        self.blockSize = blockSize
        self.cacheSize = cacheSize
        self.associativity = associativity
        self.accessLatency = accessLatency
        self.level = level

        self.numBlocks = self.cacheSize//self.blockSize
        self.numSets = self.numBlocks//self.associativity

        self.block = [None for _ in range(self.blockSize)]
        self.valid = 0
        self.tag = 0
        self.counter = 0
        self.address = "0"*globalVariables.ADDRESS_BITS
        self.cache = [[[self.tag, self.block, self.valid, self.counter, self.address]
                       for _ in range(self.associativity)] for _ in range(self.numSets)]

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
                self.updateCounter(index, blockIndex)
                return theSet[blockIndex][MagicNumbers.BLOCK.value][offset]
            return False
        except ValueError:
            return False

    def updateCache(self, address, blockIndex):
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
        self.cache[index][blockIndex][MagicNumbers.TAGS.value] = tag
        self.cache[index][blockIndex][MagicNumbers.BLOCK.value] = self.getBlock(
            address)
        self.cache[index][blockIndex][MagicNumbers.VALID.value] = 1
        self.cache[index][blockIndex][MagicNumbers.ADDRESS.value] = address

        self.updateCounter(index, blockIndex)

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

    def isFull(self, index):
        '''
        description:
            returns true if the set at the given index is full
        paramters:
            index: (int) set number
        returns:
            (bool)
        '''
        count = 0
        for b in self.cache[index]:
            count += b[MagicNumbers.VALID.value]
        return count == self.associativity

    def updateCounter(self, index, blockIndex):
        temp = self.cache[index][blockIndex][MagicNumbers.COUNTER.value]
        for b in self.cache[index]:
            if b[MagicNumbers.COUNTER.value] > temp:
                b[MagicNumbers.COUNTER.value] -= 1
        self.cache[index][blockIndex][MagicNumbers.COUNTER.value] = self.associativity - 1

    def LeastRecentlyUsed(self, address):
        '''
        description:
            updates the cache with the new block at the given address using
            the LRU policy
        parameters:
            address: (str) address of the block in binary
        returns:
            None
        '''
        tag, index, offset = self.getLocation(address)
        ## if the block is not in the cache
        if not self.search(address):
            if self.isFull(index):
            ## if the block is full, find the least recently used one
            ## and replace it
                minIndex = 0
                for b in range(len(self.cache[index])):
                    if self.cache[index][b][MagicNumbers.COUNTER.value] == 0:
                        minIndex = b
                        break

                # write back the value in self.cache[minIndex] to main memory
                writeBackAddress = int(
                    self.cache[index][minIndex][MagicNumbers.ADDRESS.value], base=2)
                globalVariables.memory[writeBackAddress:writeBackAddress+self.blockSize *
                                       4:4] = self.cache[index][minIndex][MagicNumbers.BLOCK.value]

                self.cache[index][minIndex] = [
                    tag, self.getBlock(address), 1, 0]
            else:
                ## find the block that is empty and fill it
                emptyBlock = 0
                for b in range(len(self.cache[index])):
                    if not self.cache[index][b][MagicNumbers.VALID.value]:
                        emptyBlock = b
                self.updateCache(address, emptyBlock)
        else:
            ## find the blockIndex and update its counter
            blockIndex = 0
            for b in range(len(self.cache[index])):
                if self.cache[index][b][MagicNumbers.TAGS.value] == tag:
                    blockIndex = b
            self.updateCounter(index, blockIndex)


if __name__ == "__main__":
    l1 = Cache(4, 256, 4, 2, 1)
## [1, 2, 3, 4]
## [1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0]
