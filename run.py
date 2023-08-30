from transaction import Transaction
from explorer import Explorer

#tx = Transaction()
ex = Explorer("https://ofcmvp.explorer.batch.events/")

#print(tx)
print(ex)

print(ex.get_network_status())
print(ex.get_balance("RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB"))
print(ex.get_utxos("RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB"))
print(ex.get_transaction("d062912291ced3990af0393ec4887fb4aaf86869c31569702b87dfd6471ced39"))