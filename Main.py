from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool

if __name__ == '__main__':
    sender = 'sender'
    receiver  = 'receiver'
    amount = 1
    type= 'TRANSFER'
    transaction = Transaction(sender, receiver, amount, type)

    wallet  = Wallet()
    
    #test fraudulent wallet by replacing wallet in the signature valid method
    fraudulentWallet = Wallet()

    transaction = wallet.createTransaction(receiver, amount, type)

    #Check if transaction is unique
    pool = TransactionPool()
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    
    #Check if signature is valid
    #signatureValid = Wallet.signatureValid(transaction.payload(), transaction.signature, fraudulentWallet.publicKeyString())

  
    print(pool.transactions)