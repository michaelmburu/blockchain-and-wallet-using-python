from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from Utils import Utils
import copy

class Node():

    def __init__(self, ip , port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.fromKey(key)
    
    # Start P2P Socket Communication On The Node
    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)
    
    # Start API Communication
    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)
    
    # Handle transactions
    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        transactionExist = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        # If transaction is not in pool and not in the current block and signature is valid
        if not transactionExist and not transactionInBlock and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = Utils.encode(message)
            self.p2p.broadcast(encodedMessage)
            #Check if its time to generate a new block and select a forger
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired:
                self.forge()
    
    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        #Check if block count & hash are valid
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)

        #Check if last block hash, forger and transactions are valid
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)

        #If blockcount is not valid, ask peers the current state of the blockchain
        if not blockCountValid:
            self.requestChain()

        # If all checks are valid, add block to the block chain
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid and blockCountValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = Utils.encode(message)
            self.p2p.broadcast(encodedMessage)

    # Request uptodate chain
    def requestChain(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        encodedMessage = Utils.encode(message)
        self.p2p.broadcast(encodedMessage)
    
    # Handle Blockchain Status Request
    def handleBlockChainRequest(self, requestingNode):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)
        encodedMessage = Utils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)
    
    # Iterate the new blockchain and add valid blocks from the peers to get the current blockchain
    def handleBlockChain(self, blockchain):
        localBlockChainCopy = copy.deepcopy(self.blockchain)
        localBlockCount  = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)
        if localBlockCount < receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockChainCopy

    # Hands over to blockchain class to forge a new block      
    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print('I am the next forger')
            block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = Utils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print('I am not the next forger')
    

        