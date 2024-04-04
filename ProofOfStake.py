from Lot import Lot
from Utils import Utils

class ProofOfStake():

    def __init__(self):
        self.stakers = {}
        self.setGenesisNodeStake()
    
    # Set genesis node staker public key
    def setGenesisNodeStake(self):
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        self.stakers[genesisPublicKey] = 1
        

    # Update and keep track list of public keys that are staking
    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake
        else:
            self.stakers[publicKeyString] = stake
    
    # Get a publicKeyString that is staking.
    def get(self, publicKeyString):
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None

    # Generate lots for a validator
    def validatorLots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake + 1, seed))
        return lots
    
    # Select lot winner who is the next forger
    def winnerLot(self, lots, seed):
        winnerLot = None
        leastOffset = None
        referenceHashIntValue = int(Utils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offSet = abs(lotIntValue - referenceHashIntValue)
            if leastOffset is None or offSet < leastOffset:
                leastOffset = offSet
                winnerLot = lot
        return winnerLot

    # Select the forger from the validator lots who will forge the next block
    def forger(self, lastBlockHash):
        lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(lots, lastBlockHash)
        return winnerLot.publicKey
    
