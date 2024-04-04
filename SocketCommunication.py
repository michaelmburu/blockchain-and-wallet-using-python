import json
from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from Utils import Utils

class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)
    

    # Connect to the always online node, else send handshake if it's not 10001
    def connectToFirstNode(self):
        if self.socketConnector.port != 10001:
            self.connect_with_node('localhost', 10001)

    # Start socket communications & peer discovery handler
    def startSocketCommunication(self, node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()
    
    # Incoming messages & connections to the node
    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    # Outbound messages & connections from the node to other nodes
    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)
    
    # Print messages sent to the node
    def node_message(self, connected_node, message):
        message = Utils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.data.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockChainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain= message.data
            self.node.handleBlockChain(blockchain)
    
    # Send messages to the connected node
    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    # Send message to all nodes in the network
    def broadcast(self, message):
        self.send_to_nodes(message)