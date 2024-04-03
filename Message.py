
#Messages to be sent by the connector(ip & Port)
class Message():

    def __init__(self, connector, messageType, data):
        self.connector = connector
        self.messageType = messageType
        self.data = data
    
