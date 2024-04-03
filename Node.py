from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from Utils import Utils

class Node():

    def __init__(self, ip , port):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
    
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
        if not transactionExist and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = Utils.encode(message)
            self.p2p.broadcast(encodedMessage)
        