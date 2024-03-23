from Block import Block
from Utils import Utils

class Blockchain():

    def __init__(self):
        self.blocks = [Block.genesis()]
    
    # Add a block to the blockchain
    def addBlock(self, block):
        self.blocks.append(block)

    # Allow pprint to json representation of the object
    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data
    
    # BELOW ARE VALIDATION METHODS THAT MAKE SURE WE ARE ADDING A VALID BLOCK TO THE BLOCKCHAIN

    # Check if the blockcount is valid
    def blockCountValid(self, block):
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False
    # Check if the last BlockHash is Valid
    def lastBlockHashValid(self, block):
        latestBlockChainHash = Utils.hash(self.blocks[-1].payload()).hexdigest()
        if latestBlockChainHash == block.lastHash:
            return True
        else:
            return False

