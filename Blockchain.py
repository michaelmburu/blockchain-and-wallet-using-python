from Block import Block
from Utils import Utils
from AccountModel import AccountModel

class Blockchain():

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()


    # Add a block to the blockchain
    def addBlock(self, block):
        self.executeTransactions(block.transactions)
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
    
    # Get all covered transactions
    def getCoveredTransactions(self, transactions):
        converedTransactions = []
        for transaction in transactions:
            if self.TransactionCovered(transaction):
                converedTransactions.append(transaction)
            else:
                print("Transaction is not covered")
        return converedTransactions

    
    # Is this a covered transaction?
    def TransactionCovered(self, transaction):
        if transaction.transactionType == 'EXCHANGE':
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.tokenAmount:
            return True
        else:
            return False
        
    
    # is the executed transaction a covered transaction
    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)


    # execute covered transactions
    def executeTransaction(self, transaction):
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.tokenAmount
        self.accountModel.updateBalance(sender, -amount)
        self.accountModel.updateBalance(receiver, amount)