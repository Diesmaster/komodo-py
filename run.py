
from transaction import Transaction
import transaction
from explorer import Explorer
from wallet import Wallet
from ecpy.curves     import Curve,Point

tx = Transaction( )
ex = Explorer("https://ofcmvp.explorer.batch.events/")

wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")
print(wal.create_wallet())

rawtx = transaction.make_address_transaction( ex, wal, ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] )

print(tx)

res = ex.broadcast_via_explorer( rawtx )
print(res)