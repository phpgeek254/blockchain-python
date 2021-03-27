#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 22:08:19 2021

@author: maundaalex
"""

import datetime
import hashlib
import json


# Building the block chain

def hash(block):
    # Change the chain to a string
    encoded_block = json.dumps(block, sort_keys=True).encode()
    # Hash the block
    return hashlib.sha256(encoded_block).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def is_chain_valid(self, chain):
        # Check all the blocks in the chain
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]

            # Check the validity of the chain
            if current_block['previous_hash'] != hash(previous_block):
                return False

            # Check the validity of the proof of work
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        return True
