BLOCK_SIZE = 32
CACHE_SIZE = 1024*16
ASSOCIATIVITY = 4

numBlocks = CACHE_SIZE//BLOCK_SIZE
numSets = numBlocks//ASSOCIATIVITY


## cache -> array of sets each of which contains a block
block = [None for _ in range(BLOCK_SIZE)]
mySet = [block for _ in range(ASSOCIATIVITY)]
cache = [mySet for _ in range(numSets)]