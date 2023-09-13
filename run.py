
from transaction import TxInterface
import transaction
from explorer import Explorer
from wallet import Wallet
from ecpy.curves     import Curve,Point


ex = Explorer("https://ofcmvp.explorer.batch.events/")

wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")
print(wal.create_wallet())


tx_in = TxInterface(ex, wal)

for n in range(0, 1000):
	rawtx = tx_in.send_tx_force( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] )

print(rawtx)

#res = ex.broadcast_via_explorer( rawtx )
#print(res)