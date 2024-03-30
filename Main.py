import pprint
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils
from AccountModel import AccountModel

if __name__ == '__main__':

  blockChain = Blockchain()
  pool = TransactionPool()

  alice = Wallet()
  bob = Wallet()
  exchange = Wallet()
  forger = Wallet()

  exchangeTransaction = exchange.createTransaction(alice.publicKeyString(), 10, 'EXCHANGE')

  if not pool.transactionExists(exchangeTransaction):
    pool.addTransaction(exchangeTransaction)

  coveredTransaction = blockChain.getCoveredTransactions(pool.transactions)
  lastHash = Utils.hash(blockChain.blocks[-1].payload()).hexdigest()
  blockCount = blockChain.blocks[-1].blockCount + 1
  blockOne = forger.createBlock(coveredTransaction, lastHash, blockCount)
  blockChain.addBlock(blockOne)

  #Alice wants to send 5 tokens to bob
  transaction = alice.createTransaction(bob.publicKeyString(), 5, 'TRANSFER')

  if not pool.transactionExists(transaction):
    pool.addTransaction(transaction)

  coveredTransaction = blockChain.getCoveredTransactions(pool.transactions)
  lastHash = Utils.hash(blockChain.blocks[-1].payload()).hexdigest()
  blockCount = blockChain.blocks[-1].blockCount + 1
  blockTwo = forger.createBlock(coveredTransaction, lastHash, blockCount)
  blockChain.addBlock(blockTwo)


  pprint.pprint(blockChain.toJson())
  

