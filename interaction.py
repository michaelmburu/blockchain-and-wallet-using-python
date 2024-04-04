from Wallet import Wallet
from Utils import Utils
import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = 'http://localhost:5000/transaction'
    package = {'transaction': Utils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)

if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    exchange = Wallet()

    #forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(alice, alice, 100, 'STAKE') # Remeber to create a stake private key

    # forger alice
    postTransaction(alice, bob, 1, 'TRANSFER')