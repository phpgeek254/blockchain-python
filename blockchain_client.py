#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 23:00:31 2021

@author: maundaalex
"""

from flask import Flask, jsonify

from blockchain import Blockchain

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an instance of the blockchain class
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations you have successfully mined a new block',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


# get full block chain
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
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


app.run(host='0.0.0.0', port=5000)
