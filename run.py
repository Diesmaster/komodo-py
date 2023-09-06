
from transaction import Transaction
import transaction
from explorer import Explorer
from wallet import Wallet
from ecpy.curves     import Curve,Point

tx = Transaction( )
ex = Explorer("https://ofcmvp.explorer.batch.events/")

wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")
print(wal.create_wallet())

tx = transaction.make_address_transaction( ex, wal, "RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i", 1 )

## will need to use the transaction.py thing
## wal.sign_transaction( tx )

print( tx )

ex.broadcast_via_explorer( tx )