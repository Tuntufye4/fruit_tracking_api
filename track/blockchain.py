import hashlib
import json
import time


# ---------------------------------------------------
# BLOCK STRUCTURE
# ---------------------------------------------------
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()    

    def calculate_hash(self):
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
        ).encode()

        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


# ---------------------------------------------------
# BLOCKCHAIN
# ---------------------------------------------------
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # Genesis block (first block)
    def create_genesis_block(self):
        return Block(0, {"info": "Fruit Supply Chain Genesis"}, "0")

    # Add new block
    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block.hash  # 👈 return hash string for DB storage

    # Export full chain
    def to_list(self):
        return [block.to_dict() for block in self.chain]
               