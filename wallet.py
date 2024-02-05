#from sympy import Point, Integer
from ecpy.curves     import Curve,Point
import ecdsa

#from ecdsa.ecdh

import hashlib
import math
from Crypto.Hash import RIPEMD160
from .transaction import TxInterface
from .explorer import Explorer

## utils
def r160( data ):
    sha256_hash = hashlib.sha256(data).digest()
    ripemd160_hash = RIPEMD160.new(sha256_hash).digest()
    return ripemd160_hash

def s256( data ):
    return hashlib.sha256(data).digest()


## wallet class
class Wallet:
	def __init__( self, seed ):
		## const curve point
		self.startx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
		self.starty = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

		self.point_min_length = 32

		## const iguana
		self.base = 58
		self.alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

		## const general
		self.byte_order = 'big'

		## make the wallet
		self.seed = seed
		wallet = self.create_wallet()

		self.wif = wallet['wif']
		self.pub_key = wallet['pubkey']
		self.priv_key = wallet['privkey']
		self.address = wallet['address']


	def __str__( self ):

		# Fetching attributes and their values as a dictionary
		attrs = vars(self)
		# Formatting the dictionary into string form
		return ',\n'.join(f"{key} = {value}" for key, value in attrs.items())

	def create_wallet( self ):
		"""
		// A private key must be a whole number from 1 to
		//     0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140,
		// one less than the order of the base point (or "generator point") G.
		// See:
		//     https://en.bitcoin.it/wiki/Private_key//Range_of_valid_ECDSA_private_keys
		"""

		versionByte = bytes([0x3C])
		privKeyVersionByte = bytes([0xBC])

		passString = self.seed
		hashByte = hashlib.sha256(passString.encode()).digest()

		#print("hashByte: " + str(hashByte))

		"""
			// The following is the method used by iguana password hashing algorigthm, as shown in existing seed to address/WIF generate examples of PHP and JavaScript
		// See:
		//		https://github.com/pbca26/komodolib-js/blob/master/src/keys.js#L94
		//		https://github.com/DeckerSU/komodo_scripts/blob/master/genkomodo.php#L136
		"""

		hashByte = bytearray(hashByte)

		hashByte[0] &= 248
		hashByte[31] &= 127
		hashByte[31] |= 64

		privKey  = int.from_bytes(hashByte, byteorder=self.byte_order)

		#returned private key
		rPrivKey = hashByte.hex()


		#ec arithmatic to generate the public key
		cv = Curve.get_curve('secp256k1')
		startPoint = self.ecG(cv)
		publicPoint = privKey*startPoint
		publicPointSerialized = self.serializePoint(publicPoint)

		#returned publickey
		rPubKey = publicPointSerialized.hex()


		#modiciations to make it an address
		hashpubkey = r160(publicPointSerialized)
		versionPlusHash = versionByte + hashpubkey

		checksum = s256(s256(versionPlusHash))[:4]
		total = versionPlusHash + checksum

		address = self.base58Iguana(total)

		#returned address
		rAddress = str(address)


		#create the uncompressed wif not returned
		versionPrivkey = privKeyVersionByte + hashByte
		checksum = s256(s256(versionPrivkey))[:4]
		privKeyChecksum = versionPrivkey + checksum
		uwif = self.base58Iguana(privKeyChecksum)


		#create the compressed wif
		byteone = bytes([0x01])
		privkeyVerByte = versionPrivkey + byteone
		privKeyChecksumComp = s256(s256(privkeyVerByte))[:4]
		privByteCheck = privkeyVerByte + privKeyChecksumComp
		cwif = self.base58Iguana(privByteCheck)

		#returned wif
		rwif = cwif

		return {'wif':rwif, 'address':rAddress, 'pubkey':rPubKey, 'privkey':rPrivKey}

	def ecG( self, cv ):
		G = Point( self.startx, 
		           self.starty, cv)

		return G

	def serializePoint( self, point ):
		b = point.x.to_bytes((point.x.bit_length() + 7) // 8, byteorder=self.byte_order)

		if len(b) < self.point_min_length:
			length = self.point_min_length - len(b)
			addbytes = bytes(length)
			b = addbytes + b

		if point.y % 2 == 0:
			a = b'\x02' + b
			return a

		a = b'\x03' + b
		return a

	def base58Iguana( self, completeArray ):

		x = int.from_bytes(completeArray, byteorder=self.byte_order)  # Convert bytes to integer
		output_string = ""  # To store base58 converted value

		while x > 0:
		    x, remainder = divmod(x, self.base)
		    output_string = self.alphabet[remainder] + output_string
		    

		for byte in completeArray:
			if byte == 0:
				output_string = self.alphabet[0] + output_string
			else:
				break

		return output_string

	def base58DecodeIguana(self, input_string):
		x = 0

		for char in input_string:
			x = x * self.base + self.alphabet.index(char)

		completeArray = bytearray()
		while x > 0:
			x, remainder = divmod(x, 256)
			completeArray.insert(0, remainder)

		for char in input_string:
			if char == self.alphabet[0]:
				completeArray.insert(0, 0)
			else:
				break

		return completeArray

	def get_address( self ):
		return self.address

	def get_scriptpubkkey( self ):
		return self.base58DecodeIguana(self.address)[1:-4].hex()

	def get_sign_key( self ):
		return ecdsa.SigningKey.from_string(bytes.fromhex(self.priv_key), curve=ecdsa.SECP256k1)

	def get_public_key( self ):
		return self.pub_key


class WalletInterface:
	def __init__(self, query, seed):
		self.query = query
		self.wal = Wallet(seed)

	def get_address( self ):
		return self.wal.get_address()

	def make_address_transaction( self, to_address, amount ):
		tx_in = TxInterface(self.query, self.wal)
		res = tx_in.make_address_transaction( to_address, amount )
		return res

	def send_tx( self, to_address, amount ):
		tx_in = TxInterface(self.query, self.wal)
		res = tx_in.send_tx( to_address, amount )
		return res

	def send_tx_force( self, to_address, amount ):
		tx_in = TxInterface(self.query, self.wal)
		res = tx_in.send_tx_force( to_address, amount )
		return res

	def get_sign_key( self ):
 		return self.wal.get_sign_key()
	
	def get_utxos( self ):
		return self.query.get_utxos(self.wal.get_address())

	def get_balance( self ):
		return self.query.get_balance(self.wal.get_address())

	def get_public_key( self ):
		return self.wal.get_public_key()

	def send_tx_opreturn( self, to_address, data ):
		tx_in = TxInterface(self.query, self.wal)
		res = tx_in.send_tx_opreturn( to_address, data )
		return res

	 def oracles_create(self, name, description, data_type):
        return self.query.oracles_create(name, description, data_type)

    def oracles_fund(self, oracle_id):
        return self.query.oracles_fund(oracle_id)

    def oracles_register(self, oracle_id, data_fee):
        return self.query.oracles_register(oracle_id, data_fee)

    def oracles_subscribe(self, oracle_id, publisher_id, data_fee):
        return self.query.oracles_subscribe(oracle_id, publisher_id, data_fee)

    def oracles_info(self, oracle_id):
        return self.query.oracles_info(oracle_id)

    def oracles_data(self, oracle_id, hex_string):
        return self.query.oracles_data(oracle_id, hex_string)

    def oracles_list(self):
        return self.query.oracles_list()

    def oracles_samples(self, oracletxid, batonutxo, num):
        return self.query.oracles_samples(oracletxid, batonutxo, num)
