# komodo-py

from wallet import WalletInterface

this gives access to the following functions:

## def get_address( self ):

This function returns the address of the wallet, so you can send funds to this wallet.


## def make_address_transaction( self, to_address, amount ):
@params: to_address:	array of address if you want a send many
					 	or string if you want to send to 1 address
		 amount:		array of amounts if you want a send many
		 				or a int if you want to send to 1
		 Number is always in full coins not in sats
		 to_address and to amount need to be of the same type

this functions returns a signed raw transaction to the addresses  


## def send_tx( self, to_address, amount ):
@params: to_address:	array of address if you want a send many
					 	or string if you want to send to 1 address
		 amount:		array of amounts if you want a send many
		 				or a int if you want to send to 1
		 Number is always in full coins not in sats
		 to_address and to amount need to be of the same type
this functions returns a txid if it sucsesfully broadcasted the transaction or raise a exception if there were issues.

## def send_tx_force( self, to_address, amount ):
@params: to_address:	array of address if you want a send many
					 	or string if you want to send to 1 address
		 amount:		array of amounts if you want a send many
		 				or a int if you want to send to 1
		 Number is always in full coins not in sats
		 to_address and to amount need to be of the same type
this functions returns a txid when it sucsesfully broadcasted the transaction, untill it broadcasted the transaction it will loop over all the utxos in the wallet to try them 1 by 1.