import hashlib
import time
import json

# Class for Transaction Inputs
class TxIn:
    def __init__(self, prev_tx_id, amount, vout, script_pubkey):
        self.prev_tx_id = prev_tx_id
        self.amount = int(amount*1e8)
        self.vout = int(vout)
        self.script_pubkey = script_pubkey

# Class for Transaction Outputs
class TxOut:
    def __init__(self, value, pub_key):
        self.value = int(value*1e8)
        self.pub_key = pub_key

# Class for Transaction
class Transaction:
    def __init__(self, script_pubkey=""):
        self.version="04000080"
        self.version_group_id="85202f89"
        self.list_unspend=0
        self.end_marking="00ffffffff"
        self.script_pubkey = script_pubkey
        date = int(time.time())
        self.nlocktime = bytes.fromhex(format(date, '08x'))[::-1].hex()
        self.tx_outs = []
        self.tx_ins = []

    def __str__(self):
        # Fetching attributes and their values as a dictionary
        attrs = vars(self)
        # Formatting the dictionary into string form
        return ', '.join(f"{key}={value}" for key, value in attrs.items())

    def get_ins_total( self ):
        amount = 0
        for tx_in in self.tx_ins:
            amount += tx_in.amount

        return amount

    def serialize_inputs( self ):
        reversed_bytes = bytes.fromhex(self.tx_ins[0].prev_tx_id)[::-1]
        rev_txid = reversed_bytes.hex()

        #rev vout
        # Convert vout to a hexadecimal string with 8 digits
        vout_hex = format(self.tx_ins[0].vout, '08x')

        # Reverse byte order
        rev_vout = bytes.fromhex(vout_hex)[::-1].hex()
        #print("Reversed vout_hex:", rev_vout)
    
        #start raw tx
        rawtx= self.version + self.version_group_id # tx version
        #rawtx= rawtx +  #version group id
        # number of inputs (1, as we take one utxo from explorer listunspent)
        rawtx = rawtx + "01"
        rawtx= rawtx + rev_txid + rev_vout + self.end_marking

        return rawtx

    def serialize_inputs_sign( self ):
        reversed_bytes = bytes.fromhex(self.tx_ins[0].prev_tx_id)[::-1]
        rev_txid = reversed_bytes.hex()

        #rev vout
        # Convert vout to a hexadecimal string with 8 digits
        vout_hex = format(self.tx_ins[0].vout, '08x')

        # Reverse byte order
        rev_vout = bytes.fromhex(vout_hex)[::-1].hex()

        scriptkey = self.tx_ins[0].script_pubkey
    
        #start raw tx
        rawtx= self.version #+ self.version_group_id # tx version

        rawtx = rawtx + "01" #amount of inputs is 1
        rawtx= rawtx + rev_txid + rev_vout + len(scriptkey)//2 + scriptkey + self.end_marking

        return rawtx

    def serialize_outputs(self):
        rawtx = ""
        n_outputs = len(self.tx_outs)

        if n_outputs < 252:
            outputCount = format(n_outputs + 1, '02x')
            rawtx += outputCount
            total_amount = 0



            for tx_out in self.tx_outs:
                print("val: " + str(tx_out.value))
                amount = bytes.fromhex(format(tx_out.value, '016x'))[::-1].hex()
                print(tx_out.pub_key)
                rawtx += f"{amount}1976a914{tx_out.pub_key}88ac"
                total_amount += tx_out.value

            change = self.get_ins_total() - total_amount
            print(f"change: {change}")
            change_value = bytes.fromhex(format(change, '016x'))[::-1].hex()
            rawtx += change_value

            rawtx += f"1976a914{self.script_pubkey}88ac"

        return rawtx

    def serialize_outputs_sign( self ):
        rawtx = ""
        n_outputs = len(self.tx_outs)

        if n_outputs < 252:
            outputCount = format(n_outputs + 1, '02x')
            rawtx += outputCount
            total_amount = 0

            for tx_out in self.tx_outs:
                amount = bytes.fromhex(format(tx_out.value, '016x'))[::-1].hex()
                rawtx += f"{amount}2321{tx_out.pub_key}ac"
                total_amount += tx_out.value

            change = self.get_ins_total() - total_amount
            print(f"change: {change}")
            change_value = bytes.fromhex(format(change, '016x'))[::-1].hex()
            rawtx += change_value

            rawtx += f"1976a914{self.script_pubkey}88ac"

        return rawtx

    def serialize_end( self ):
        date = int(time.time())
        nlocktime = bytes.fromhex(format(date, '08x'))[::-1].hex()
        rawtx = nlocktime
        rawtx = rawtx + "000000000000000000000000000000"
        return rawtx

    # Method to serialize the transaction for hashing only single input output now supported
    def serialize(self):
        # Serialize the transaction here
        # You'll need to convert each field to bytes and concatenate them

        rawtx = self.serialize_inputs()
        rawtx = rawtx + self.serialize_outputs()
        rawtx = rawtx + self.serialize_end()
        return rawtx

    # Method to compute the transaction ID
    def txid(self):
        serialized_tx = self.serialize()
        double_hash = hashlib.sha256(hashlib.sha256(serialized_tx).digest()).digest()
        return double_hash[::-1].hex()

    # Method to add an input transaction
    def add_input(self, prev_tx_id, amount, vout, script_pubkey):
        tx = TxIn( prev_tx_id, amount, vout, script_pubkey )
        self.tx_ins.append(tx)
        self.list_unspend += 1

    # Method to add an output transaction
    def add_output( self, value, to_scriptpubkey ):
        tx = TxOut(value, to_scriptpubkey)
        self.tx_outs.append(tx)

def find_utxo( utxos, amount ):
    for utxo in utxos:
        if utxo['amount'] > amount and utxo['confirmations']:
            return utxo


def make_address_transaction( ex, wal, to_address, amount ):
    address = wal.get_address()
    to_scriptpubkey = wal.base58DecodeIguana(to_address).hex()[2:-8]

    print(to_scriptpubkey)

    from_scriptpubkey = wal.get_scriptpubkkey()

    tx = Transaction(from_scriptpubkey)
    tx.add_output( amount, to_scriptpubkey )

    utxos = json.loads(ex.get_utxos( address ))
    utxo = find_utxo( utxos, 1 )

    print(utxo)
    print(wal.get_scriptpubkkey())

    tx.add_input( utxo['txid'], utxo['amount'], utxo['vout'], utxo['scriptPubKey'])

    ser_tx = tx.serialize()
    return ser_tx

def serialize_sign_precurser( self ):
    # Check if transaction is overwintered
    overwintered = self.overwintered
    version = self.version

    # Create hash type and lock time in hexadecimal
    nHashType = int_to_hex(1, 4)
    nLocktime = int_to_hex(self.locktime, 4)

    # Serialize inputs and outputs
    inputs = self.inputs()
    outputs = self.outputs()
    txin = inputs[i]


    # deactivate overwintered support
    overwintered = False

    # Check for overwintered transactions RN no support
    if overwintered:
        # Prepare overwintered specific headers and version group ID
        nVersion = int_to_hex(0x80000000 | self.version, 4)
        nVersionGroupId = int_to_hex(self.version_group_id, 4)

        # Generate hash for previous outputs, sequences, and outputs
        s_prevouts = bfh(''.join(self.serialize_outpoint(txin) for txin in inputs))
        hashPrevouts = blake2b(s_prevouts, digest_size=32, person=b'ZcashPrevoutHash').hexdigest()
        s_sequences = bfh(''.join(int_to_hex(txin.get('sequence', 0xffffffff - 1), 4) for txin in inputs))
        hashSequence = blake2b(s_sequences, digest_size=32, person=b'ZcashSequencHash').hexdigest()
        s_outputs = bfh(''.join(self.serialize_output(o) for o in outputs))
        hashOutputs = blake2b(s_outputs, digest_size=32, person=b'ZcashOutputsHash').hexdigest()

        # Initialize joinSplits, hashShieldedSpends, and hashShieldedOutputs
        hashJoinSplits = '00'*32
        hashShieldedSpends = '00'*32
        hashShieldedOutputs = '00'*32

        # Prepare expiry height and value balance
        nExpiryHeight = int_to_hex(self.expiryHeight, 4)
        nValueBalance = int_to_hex(self.valueBalance, 8)

        # Get preimage script for the input
        preimage_script = self.get_preimage_script(txin)
        scriptCode = var_int(len(preimage_script) // 2) + preimage_script

        # Construct the preimage with all the components
        preimage = (
            nHeader + nVersionGroupId + hashPrevouts + hashSequence + hashOutputs
            + hashJoinSplits + hashShieldedSpends + hashShieldedOutputs + nLocktime
            + nExpiryHeight + nValueBalance + nHashType
            + self.serialize_outpoint(txin)
            + scriptCode
            + int_to_hex(txin['value'], 8)
            + int_to_hex(txin.get('sequence', 0xffffffff - 1), 4)
        )
    else:
        # Prepare headers for non-overwintered transactions
        nVersion = int_to_hex(self.version, 4)
        
        txins = var_int(len(inputs)) + ''.join(self.serialize_input(txin, self.get_preimage_script(txin) if i==k else '') for k, txin in enumerate(inputs))

        txouts = var_int(len(outputs)) + ''.join(self.serialize_output(o) for o in outputs)

        # Construct the preimage for non-overwintered transactions
        preimage = nVersion + txins + txouts + nLocktime + nHashType

    return preimage
