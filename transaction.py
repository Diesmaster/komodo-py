import hashlib
import time

# Class for Transaction Inputs
class TxIn:
    def __init__(self, prev_tx_id, prev_tx_out_index, script_pubkey, amount):
        self.prev_tx_id = prev_tx_id
        self.prev_tx_out_index = prev_tx_out_index
        self.amount = amount

# Class for Transaction Outputs
class TxOut:
    def __init__(self, value, pub_key):
        self.value = value
        self.pub_key = pub_key

# Class for Transaction
class Transaction:
    def __init__(self, script_pubkey=""):
        self.version="04000080"
        self.version_group_id="85202f89"
        self.list_unspend=0
        self.end_marking="00ffffffff"
        self.script_sig = script_pubkey
        date = int(time.time())
        self.nlocktime = bytes.fromhex(format(date, '08x'))[::-1].hex()

    def __str__(self):
        # Fetching attributes and their values as a dictionary
        attrs = vars(self)
        # Formatting the dictionary into string form
        return ', '.join(f"{key}={value}" for key, value in attrs.items())

    # Method to serialize the transaction for hashing
    def serialize(self):
        # Serialize the transaction here
        # You'll need to convert each field to bytes and concatenate them
        pass

    # Method to compute the transaction ID
    def txid(self):
        serialized_tx = self.serialize()
        double_hash = hashlib.sha256(hashlib.sha256(serialized_tx).digest()).digest()
        return double_hash[::-1].hex()

    # Method to add an input transaction
    def add_input(self, tx_in):
        self.tx_ins.append(tx_in)
        self.list_unspend += 1

    # Method to add an output transaction
    def add_output(self, tx_out):
        self.tx_outs.append(tx_out)