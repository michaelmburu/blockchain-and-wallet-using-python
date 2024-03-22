# Pool unique transactions before submitting to a block
class  TransactionPool():

    def __init__(self):
        self.transactions = []

    # Add a transaction to the pool
    def addTransaction(self, transaction):
        self.transactions.append(transaction)
    
    # check if transaction is unique
    def transactionExists(self, transaction):
        #check if transaction exists
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

    