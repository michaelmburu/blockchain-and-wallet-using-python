import pprint
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from Utils import Utils
from AccountModel import AccountModel
from Node import Node
import sys

if __name__ == '__main__':

	#Provide ip and port as arguments via the command line.
	ip = sys.argv[1]
	port = int(sys.argv[2])
	apiPort = int(sys.argv[3])
	keyFile = None
	if len(sys.argv) > 4:
		keyFile = sys.argv[4]

	node  = Node(ip, port, keyFile)
	node.startP2P()
	node.startAPI(apiPort)
	
	


	