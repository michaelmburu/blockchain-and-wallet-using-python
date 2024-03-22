from Crypto.PublicKey import RSA
from Utils import Utils
from Crypto.Signature import PKCS1_v1_5
from Transaction import Transaction

class Wallet:

    def __init__(self):
        self.keyPair = RSA.generate(2048)

    # Sign transactions
    def sign(self, data):
        dataHash = Utils.hash(data)
        signaturesSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signaturesSchemeObject.sign(dataHash)
        return signature.hex()

    # Validate signatures: Detect invalid signatures
    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature) 
        dataHash = Utils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signaturesSchemeObject = PKCS1_v1_5.new(publicKey)
        #Check if signature corresponds to dataHash based on the knowledge of the public key
        signatureValid = signaturesSchemeObject.verify(dataHash, signature)
        return signatureValid
    
    # Get public key string
    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey("PEM").decode('utf-8')
        return publicKeyString
    
    #Create & sign Transactions on the wallet
    def createTransaction(self, receiverPublicKey, tokenAmount, transactionType):
        transaction = Transaction(self.publicKeyString(), receiverPublicKey, tokenAmount, transactionType)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

