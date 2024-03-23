import pprint
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils

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

    blockchain = Blockchain()

    #EXAMPLE 1: Check if transaction is unique
    pool = TransactionPool()
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    

    #EXAMPLE 2: #Check if signature is valid
    #signatureValid = Wallet.signatureValid(transaction.payload(), transaction.signature, fraudulentWallet.publicKeyString())

    #EXAMPLE 3: check whether signature is valid or not
    #signatureValid = Wallet.signatureValid(block.payload(), block.signature, wallet.publicKeyString())
    #pprint.pprint(signatureValid)
    #pprint.pprint(block.toJson())

    #EXAMPLE 4: get last block hash & blockcount
    # Change blockcount or lastHash below to add a wrong block to the blockchain and generate an error.
    lastHash = Utils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    block = wallet.createBlock(pool.transactions, lastHash, blockCount)

    if not blockchain.lastBlockHashValid(block):
        pprint.pprint("Last Block Hash is not valid")
    
    if not blockchain.blockCountValid(block):
        pprint.pprint("Last Block Count is not valid")
    
    # Add block to blockchain
    if blockchain.lastBlockHashValid(block) and blockchain.blockCountValid(block):
        blockchain.addBlock(block)

    pprint.pprint(blockchain.toJson())
  
   