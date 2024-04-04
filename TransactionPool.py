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

    # Remove transaction from pool
    def removeFromPool(self, transactions):
        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False
            if insert  == True:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions
    
    # Check if the threshold of transactions in the pool is reached and select validators to forge a new block
    def forgerRequired(self):
        if len(self.transactions) >= 1:
            return True
        else:
            return False
    

    