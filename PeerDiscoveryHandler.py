import time
import threading
from Utils import Utils
from Message import Message

# Manage Broadcasting of node connections to allow other nodes to connect to each other.
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node
    
    # Start the status and discovery methods
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()
    
    # print broadcast connections
    def status(self):
        while True:
            print('Current connections:')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(10)

    # send broadcast message out to the network for other nodes to hear which other connections the node has.
    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)
    
    # Track connection between two nodes & exchange of information
    def handshake(self, connect_node):
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)

    # Create handshake message of the connected nodes to send
    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = "DISCOVERY"
        message = Message(ownConnector, messageType, data)
        encodedMessage = Utils.encode(message)
        return encodedMessage
    
    # Handle incoming message connections & connect with peers in the peer list
    def handleMessage(self, message):
        peersSocketConnector = message.connector
        peersList = message.data
        newPeer = True
        for peer  in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer == True:
            self.socketCommunication.peers.append(peersSocketConnector)
        for peersPeer in peersList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)


    

