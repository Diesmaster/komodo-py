import hashlib
import time
import json
import binascii

from pyblake2 import blake2b
import ecdsa

# Class for Transaction Inputs
class TxIn:
    def __init__(self, prev_tx_id, amount, vout, script_pubkey):
        self.prev_tx_id = prev_tx_id
        self.amount = int(amount*1e8)
        self.vout = int(vout)
        self.script_pubkey = script_pubkey
        self.pub_key = ""
        self.signature = ""

# Class for Transaction Outputs
class TxOut:
    def __init__(self, value, pub_key):
        self.value = int(value*1e8)
        self.pub_key = pub_key

    def __str__( self ):

        # Fetching attributes and their values as a dictionary
        attrs = vars(self)
        # Formatting the dictionary into string form
        return ',\n'.join(f"{key} = {value}" for key, value in attrs.items())

# Class for Transaction
class Transaction:
    def __init__(self, script_pubkey=""):
        self.version="04000080"
        self.version_group_id="85202f89"
        self.sapling_branch_id = "76b809bb"
        self.list_unspend=0
        self.end_marking="ffffffff"
        self.sequences = "ffffffff"
        self.script_pubkey = script_pubkey
        date = int(time.time())
        self.locktime = -1
        self.tx_outs = []
        self.tx_ins = []
        self.rawtx = ""
        self.overwintered = True

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

        sig = ""
        pub = ""
        if not self.tx_ins[0].signature == "":
            if len(self.tx_ins[0].signature) == 140:
                sig = "6a47" + self.tx_ins[0].signature
            else:
                sig = "6b48" + self.tx_ins[0].signature
            pub = "0121" + self.tx_ins[0].pub_key    

        #start raw tx
        rawtx= self.version + self.version_group_id # tx version
        #rawtx= rawtx +  #version group id
        # number of inputs (1, as we take one utxo from explorer listunspent)
        rawtx = rawtx + "01"
        rawtx= rawtx + rev_txid + rev_vout + sig + pub + self.end_marking

        return rawtx

    def serialize_input_sign( self ):

        #txid
        reversed_bytes = bytes.fromhex(self.tx_ins[0].prev_tx_id)[::-1]
        rev_txid = reversed_bytes.hex()

        #vout
        vout_hex = format(self.tx_ins[0].vout, '08x')
        rev_vout = bytes.fromhex(vout_hex)[::-1].hex()

        return rev_txid + rev_vout



    def serialize_outputs(self):
        rawtx = ""
        n_outputs = len(self.tx_outs)

        if n_outputs < 252:
            outputCount = format(n_outputs + 1, '02x')
            rawtx += outputCount
            total_amount = 0



            for tx_out in self.tx_outs:
                amount = bytes.fromhex(format(tx_out.value, '016x'))[::-1].hex()
                rawtx += f"{amount}1976a914{tx_out.pub_key}88ac"
                total_amount += tx_out.value

            change = self.get_ins_total() - total_amount
            change_value = bytes.fromhex(format(change, '016x'))[::-1].hex()
            rawtx += change_value

            rawtx += f"1976a914{self.script_pubkey}88ac"

        return rawtx

    def serialize_end_sign( self ):
        rawtx = ""
        n_outputs = len(self.tx_outs)

        if n_outputs < 252:
            #outputCount = format(n_outputs + 1, '02x')
            #rawtx += outputCount
            total_amount = 0



            for tx_out in self.tx_outs:
                amount = bytes.fromhex(format(tx_out.value, '016x'))[::-1].hex()
                rawtx += f"{amount}1976a914{tx_out.pub_key}88ac"
                total_amount += tx_out.value

            change = self.get_ins_total() - total_amount
            change_value = bytes.fromhex(format(change, '016x'))[::-1].hex()
            rawtx += change_value

            rawtx += f"1976a914{self.script_pubkey}88ac"

        return rawtx

    def serialize_end( self ):
        date = int(time.time())
        nlocktime = bytes.fromhex(format(date, '08x'))[::-1].hex()
        self.locktime = nlocktime
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

    def get_script_code( self ):
        return "76a914" + self.tx_ins[0].script_pubkey + "88ac"

    def var_int(self, i):
        # https://en.bitcoin.it/wiki/Protocol_specification#Variable_length_integer
        if i<0xfd:
            return bytes.fromhex(format(i, '08x'))[::-1].hex()[:2]
        elif i<=0xffff:
            return "fd"+bytes.fromhex(format(i, '08x'))[::-1].hex()[:2]
        elif i<=0xffffffff:
            return "fe"+bytes.fromhex(format(i, '08x'))[::-1].hex()[:4]
        else:
            return "ff"+bytes.fromhex(format(i, '08x'))[::-1].hex()[:8]


    def serialize_sign_precurser( self ):
        #TODO replace hard coded strings with the names of the op_codes
        
        nVersion = self.version #bytes.fromhex(format(self.version, '016x'))[::-1].hex()
        nHashType = bytes.fromhex(format(1, '016x'))[::-1].hex()[:8]
        nVersionGroupId = self.version_group_id
        nLocktime = self.locktime #bytes.fromhex(format(self.locktime, '016x'))[::-1].hex()
        
        txins = self.serialize_inputs()
        txouts = self.serialize_outputs()

        if self.overwintered == True:
            hashJoinSplits = '00'*32
            hashShieldedSpends = '00'*32
            hashShieldedOutputs = '00'*32

            txins = self.serialize_input_sign()
            txouts = self.serialize_end_sign()


            hashPrevouts = blake2b(bytes.fromhex(txins), digest_size=32, person=b'ZcashPrevoutHash').hexdigest()
            hashSequance = blake2b(bytes.fromhex(self.sequences), digest_size=32, person=b'ZcashSequencHash').hexdigest()
            hashOutputs = blake2b(bytes.fromhex(txouts), digest_size=32, person=b'ZcashOutputsHash').hexdigest()

            nExpiryHeight = "00000000"
            nValueBalance = "0000000000000000"

            #TODO: op codes still attached to pubkey
            preimage_script = self.tx_ins[0].script_pubkey

            #length = bytes.fromhex(format(len(preimage_script)  // 2, '08x'))[::-1].hex()
            scriptCode = str(self.var_int( len(preimage_script) // 2 )) + preimage_script

            #final amount
            val = self.get_ins_total()
            val = hex(val)[2:].rstrip('L')
            val = "0"*(2*8 - len(val)) + val


            val = bytes.fromhex(val)[::-1].hex()

            preimage = nVersion + nVersionGroupId + hashPrevouts + hashSequance + hashOutputs + hashJoinSplits + hashShieldedSpends + hashShieldedOutputs + nLocktime + nExpiryHeight + nValueBalance + nHashType + txins + scriptCode + val +  self.sequences

        else:
            # Check if transaction is overwintered
            

            # Construct the preimage for non-overwintered transactions
            preimage = nVersion + txins + txouts + nLocktime + nHashType

        return preimage

    def signtx( self, sig_key, pub_key ):
        preimage = self.serialize_sign_precurser()

        if self.overwintered == True:
            data = bytes.fromhex(preimage)
            person = b'ZcashSigHash' + bytes.fromhex(self.sapling_branch_id)[::-1] #.to_bytes(4, 'little')
            pre_hash = blake2b(data, digest_size=32, person=person).digest()


        print("#### IETS GEBEURT HIER")

        print(binascii.hexlify(pre_hash).decode('ascii'))
                
        sig = sig_key.sign_digest_deterministic(pre_hash, hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_der_canonize)
        sig = binascii.hexlify(sig).decode('ascii')

        print(sig)

        print("### END")

        self.tx_ins[0].signature = sig
        self.tx_ins[0].pub_key = pub_key
        return sig    


def find_utxo( utxos, amount ):
    for utxo in utxos:
        if utxo['amount'] > amount and utxo['confirmations']:
            return utxo


def make_address_transaction( ex, wal, to_address, amount ):
    if isinstance(to_address, list) and not isinstance(amount, list):
        return "needs to be the same type"

    address = wal.get_address()


    from_scriptpubkey = wal.get_scriptpubkkey()

    tx = Transaction(from_scriptpubkey)

    if isinstance(to_address, list) == True:
        print(" ### test ### ")
        for x in range(0, len(to_address)):
            print(to_address[x])
            to_scriptpubkey = wal.base58DecodeIguana(to_address[x]).hex()[2:-8]
            tx.add_output( amount[x], to_scriptpubkey )

        for out in tx.tx_outs:
            print(out)
    else:
        print("### not list? ### ")
        to_scriptpubkey = wal.base58DecodeIguana(to_address).hex()[2:-8]
        tx.add_output( amount, to_scriptpubkey )

    utxos = json.loads(ex.get_utxos( address ))
    utxo = find_utxo( utxos, 1 )


    tx.add_input( utxo['txid'], utxo['amount'], utxo['vout'], utxo['scriptPubKey'])

    ser_tx = tx.serialize()


    sig_key = wal.get_sign_key()
    pub_key = wal.get_public_key()
    tx.signtx(sig_key, pub_key)

    ser_tx = tx.serialize()

    return ser_tx
