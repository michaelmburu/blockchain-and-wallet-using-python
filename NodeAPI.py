from flask_classful import FlaskView, route
from flask import Flask, jsonify,request
from Utils import Utils

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)
    
    # Start Flask API
    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port = apiPort)
    
    #inject node object to our API
    def injectNode(self, injectedNode):
        global node
        node = injectedNode
    
    # Create info route
    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communication to the Nodes in the Blockchain', 200
    
    # Create blockchain route
    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200
    
    # Create a transaction pool route
    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    # Create a transactions route to issue transaction
    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = Utils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}   
        return jsonify(response), 201 

