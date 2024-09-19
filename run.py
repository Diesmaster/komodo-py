
from transaction import TxInterface
from explorer import Explorer
from wallet import WalletInterface
from ecpy.curves     import Curve,Point


exp = Explorer("https://blockchain-explorer.occs.openfoodchain.org/")

wal_in = WalletInterface(exp, "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

print("privkey:")
print(wal_in.get_priv_key_dev())

print("pubkey")
print(wal_in.get_public_key())

print("wif:")
print(wal_in.get_wif())

utxos = wal_in.get_utxos()

#utxo = utxos[9]

for utxo_ex in utxos:
	if utxo_ex['amount'] > 2:
		utxo = utxo_ex

wal = wal_in.get_wal_dev()


tx = TxInterface(exp, wal)

rawtx = tx.make_address_transaction("RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i", utxo['amount']-1)

print(rawtx)

res = exp.broadcast(rawtx)

print(res)

#print(wal_in.send_tx_force( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] ))


"""tx_in = TxInterface(ex, wal)

for n in range(0, 1000):
	rawtx = tx_in.send_tx_force( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] )

print(rawtx)

#res = ex.broadcast_via_explorer( rawtx )
#print(res)
"""