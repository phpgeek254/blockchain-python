#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 23:00:31 2021

@author: maundaalex
"""

from flask import Flask, jsonify, request

from blockchain import Blockchain
from uuid import uuid4
import requests
app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an instance of the blockchain class
blockchain = Blockchain()

# Create an address for the node on port 5000
node_address = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender= node_address, receiver= 'Maunda Alex', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations you have successfully mined a new block',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions' : block['transactions']
    }
    return jsonify(response), 200


# get full block chain
@app.route('/chain', methods=['GET'])
def get_chain():
    #update the chain here.
    is_chain_replaced = blockchain.replace_chain()
    response = {
        'is_chain_replaced': is_chain_replaced,
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/validate-chain')
def chain_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    resp = {
        'chain_validity': is_valid,
        'message': 'Chain check completed successfully'
    }
    return jsonify(resp), 200

@app.route('/add-transaction', methods = ['POST'])
def add_transaction():
    # 1. validate the vars 2. Add transaction to the blockchain 3. anounce this.
    req = request.get_json()
    keys = ['sender', 'receiver', 'amount']
    
    if not all (key in req for key in keys):
        # Error out
        return 'There are some keys missing', 400
    
    index = blockchain.add_transaction(
            req['sender'], 
            req['receiver'], 
            req['amount']
            )
    resp = {
            'message': f'Transaction successful, added to Block {index}'
            }
    return jsonify(resp), 201

# Connect to the network -> Connect the  node.
@app.route('/connect', methods = ['POST'])
def connect():
    req = request.get_json()
    nodes = req.get('nodes')
    if nodes is None:
        return "Nodes not found", 400
    for node in nodes:
        blockchain.add_node(node)
    resp = {'message': 'Connection successful', 'nodes': list(blockchain.nodes)}
    return jsonify(resp), 200

@app.route('/replace-chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    # Handle chain replacement
    if is_chain_replaced is True:
        resp = {
                'message': 'The chain was replaced by the longest chain in the network',
                'chain': blockchain.chain
                }
    else:
        resp = {
                'message': 'This is the longest chain the network.',
                'chain': blockchain.chain
                }
        
    return jsonify(resp), 200

app.run(host='0.0.0.0', port=5003)
