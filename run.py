
from transaction import Transaction
from explorer import Explorer
from wallet import Wallet
from ecpy.curves     import Curve,Point

#tx = Transaction()
ex = Explorer("https://ofcmvp.explorer.batch.events/")

#print(tx)
#print(ex)

#print(ex.get_network_status())
#print(ex.get_balance("RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB"))
#print(ex.get_utxos("RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB"))
#print(ex.get_transaction("d062912291ced3990af0393ec4887fb4aaf86869c31569702b87dfd6471ced39"))

wal = Wallet("This is a test string hahaha")

seed = "This is a test string hahaha"
print(wal.create_wallet( seed ))

seed = "This is not a test string"
print(wal.create_wallet( seed ))


seed = "I love komdo"
print(wal.create_wallet( seed ))

seed = "I love python"
print(wal.create_wallet( seed ))
#cv = Curve.get_curve('secp256k1')
#p = wal.ecG(cv)
#ret = wal.serializePoint(p)
#print(ret)
#ret = wal.base58Iguana(ret)
#print(ret)
#ret = wal.base58DecodeIguana(ret)
#print(str(ret))