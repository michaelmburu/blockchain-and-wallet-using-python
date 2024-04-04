import uuid
import time
import copy

class Transaction():

    def __init__(self, senderPublicKey, receiverPublicKey, tokenAmount, transactionType):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.tokenAmount = tokenAmount
        self.transactionType = transactionType
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    # Parse Object to Json
    def toJson(self):
        return self.__dict__

    #Sign transaction
    def sign(self, signature):
        self.signature = signature

    #Get consistent representation of the json even if it is signed outside of the wallet
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    # Check if a transaction already exists
    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False
