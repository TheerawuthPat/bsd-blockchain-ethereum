import datetime
import json
import hashlib
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        # store block
        self.chain = []
        self.transaction = 0
        self.create_block(nonce=1, previous_hash=0)

    # method for createing a block
    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "data": self.transaction,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # POW implementation
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False

        # randomize nonce
        while check_proof is False:
            # any method to change nonce
            hash_tmp = hashlib.sha256(
                str(new_nonce**4 - previous_nonce**4).encode()
            ).hexdigest()
            if hash_tmp[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # validation
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"]
            current_nonce = block["nonce"]
            hash_tmp = hashlib.sha256(
                str(current_nonce**4 - previous_nonce**4).encode()).hexdigest()
            if hash_tmp[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True


# webserver
app = Flask(__name__)
# rounting


@app.route('/')
def hello():
    return "<h1>Hello Python</h1>"


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "lenght": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route("/mining", methods=["GET"])
def mining_block():
    # PoW
    amount = 100000
    blockchain.transaction += amount
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    current_nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(current_nonce, previous_hash)

    response = {
        "message": "Mining Successful",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            "message": "Chain Valid"
        }
    else:
        response = {
            "message": "Chain Invalid"
        }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run()

blockchain = Blockchain()


print(blockchain.hash(blockchain.chain[0]))
