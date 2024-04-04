from Utils import Utils

class Lot():
    def __init__(self, publicKeyString, iteration, lastBlockHash):
        self.publicKey = str(publicKeyString)
        self.iteration = iteration
        self.lastBlockHash = lastBlockHash
    
    # Generate a single hash from the lot data
    def lotHash(self):
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.iteration):
            hashData = Utils.hash(hashData).hexdigest()
        return hashData

    
    