import time
import copy

class Block():

    def __init__(self, transactions, lastHash, forger, blockCount):
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ''
    
    # Create the genesis block
    @staticmethod
    def genesis():
        genesisBlock = Block([], 'genesisHash', 'genesisSignature', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    # Display object in json representation on pprint
    def toJson(self):
        data = {}
        data['lastHash'] = self.lastHash
        data['forger'] = self.forger
        data['blockCount'] = self.blockCount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        return data
    
    #Get consistent representation of the json even if it is signed outside of the wallet class
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    # Add signature to the block
    def sign(self, signature):
        self.signature = signature


