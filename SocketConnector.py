
# Create socket connections
class SocketConnector():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    # Check if this is an already existing connector
    def equals(self, connector):
        if connector.ip == self.ip and connector.port == self.port:
            return True
        else:
            return False
