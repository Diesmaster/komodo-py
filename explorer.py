import requests
import json

class Explorer:
    def __init__(self, url):

    	## url
        self.url = url

        ## root:
        self.root = "insight-api-komodo/"

        ## type: status, transaction, address
        self.status = "status/"
        self.transaction = "tx/"
        self.address = "addr/"

        ## options:
        self.utxo = "/utxo"
        self.balance = "/balance"
        self.send = "send"


    def __str__( self ):

        # Fetching attributes and their values as a dictionary
        attrs = vars(self)
        # Formatting the dictionary into string form
        return ', '.join(f"{key}={value}" for key, value in attrs.items())

    def get_balance( self, addr ):

        if type(addr) is not str:
            print("Query wallet must be string")
            raise Exception("Query wallet must be string")

        full_url = self.url + self.root + self.address + addr + self.balance

        try:
            res = requests.get(full_url)

        except Exception as e:
        
            print("explorer_get_balance " + str(e))
            raise Exception(e)

        return json.loads(res.text)


    def get_utxos( self, addr ):

        if type(addr) is not str:
            print("Query wallet must be string")
            raise Exception("Query Wallet must be string")


        full_url = self.url + self.root + self.address + addr + self.utxo
        try:
            res = requests.get(full_url)
        
        except Exception as e:
        
            print("explorer_get_utxos " + str(e))
            raise Exception(e)
        

        return json.loads(res.text)

    def get_transaction( self, txid ):
        
        if type(txid) is not str:
            print("TXID must be string")
            raise Exception("TXID must be string")
        
        full_url = self.url + self.root + self.transaction + txid

        try:
            res = requests.get(full_url)
        
        except Exception as e:
        
            print("explorer_get_transaction " + str(e))
            raise Exception(e)
        return json.loads(res.text)

    def get_network_status( self ):
        try:

            full_url = self.url + self.root + self.status    
            res = requests.get(full_url)
            
            return res.json()
    
        except Exception as e:
            raise Exception(e)


    def broadcast( self, signedtx ):
        print("start broadcast_via_explorer")

        if type(self.url) is not str:
            print("Explorer URL must be string")
            raise Exception("Explorer URL must be string")

        if type(signedtx) is not str:
            print("SignedTX must be string")
            raise Exception("SignedTX must be string")

        full_url = self.url + self.root + self.transaction + self.send
        params = {'rawtx': signedtx}
        #print("PARAMS: " + str(params))
        #print("Broadcast via " + full_url)

        broadcast_res = {}
        try:
            broadcast_res = requests.post(full_url, data=params, verify=False)

            print("BC RES:")
            print(broadcast_res)

            if len(broadcast_res.text) < 64: # TODO check if json, then if the json has a txid field and it is 64
                print("error")
                print(broadcast_res.text)
                raise Exception(broadcast_res.text)
            else:
                return json.loads(broadcast_res.text)

        except Exception as e:
            print(str(broadcast_res))
            # log2discord(f"---\nThere is an exception during the broadcast: **{params}**\n Error: **{e}**\n---")
            print("rawtx: " + str(signedtx))
            # log2discord(rawtx_text)
            print("broadcast_via_explorer " + str(e))
            raise(e)

class QueryInterface:
    def __init__(self, backend):
        # Initialize an Explorer object with the given URL
        self.query = backend

    def get_balance(self, addr):
        if hasattr(self.query, 'get_balance'):
            return self.query.get_balance(addr)
        else:
            raise AttributeError("Explorer object has no method 'get_balance'")

    def get_blockcount(self):
        if hasattr(self.query, 'get_balance'):
            return self.query.get_blockcount()
        else:
            raise AttributeError("Explorer object has no method 'blockcount'")

    def get_utxos(self, addr):
        if hasattr(self.query, 'get_utxos'):
            return self.query.get_utxos(addr)
        else:
            raise AttributeError("Explorer object has no method 'get_utxos'")

    def get_transaction(self, txid):
        if hasattr(self.query, 'get_transaction'):
            return self.query.get_transaction(txid)
        else:
            raise AttributeError("Explorer object has no method 'get_transaction'")

    def get_block(self, hash_or_height, verbose=True):
        if hasattr(self.query, 'get_block'):
            return self.query.get_block(hash_or_height, verbose)
        else:
            raise AttributeError("Explorer object has no method 'get_block'")

    def get_network_status(self):
        if hasattr(self.query, 'get_network_status'):
            return self.query.get_network_status()
        else:
            raise AttributeError("Explorer object has no method 'get_network_status'")

    def broadcast(self, signedtx):
        if hasattr(self.query, 'broadcast'):
            return self.query.broadcast(signedtx)
        else:
            raise AttributeError("Explorer object has no method 'broadcast_via_explorer'")

    def oracles_create(self, name, description, data_type):
        if hasattr(self.query, 'oracles_create'):
            return self.query.oracles_create(name, description, data_type)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_create'")

    def oracles_fund(self, oracle_id):
        if hasattr(self.query, 'oracles_fund'):
            return self.query.oracles_fund(oracle_id)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_fund'")

    def oracles_register(self, oracle_id, data_fee):
        if hasattr(self.query, 'oracles_register'):
            return self.query.oracles_register(oracle_id, data_fee)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_register'")

    def oracles_subscribe(self, oracle_id, publisher_id, data_fee):
        if hasattr(self.query, 'oracles_subscribe'):
            return self.query.oracles_subscribe(oracle_id, publisher_id, data_fee)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_subscribe'")

    def oracles_info(self, oracle_id):
        if hasattr(self.query, 'oracles_info'):
            return self.query.oracles_info(oracle_id)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_info'")

    def oracles_data(self, oracle_id, hex_string):
        if hasattr(self.query, 'oracles_data'):
            return self.query.oracles_data(oracle_id, hex_string)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_data'")

    def oracles_list(self):
        if hasattr(self.query, 'oracles_list'):
            return self.query.oracles_list()
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_list'")

    def oracles_samples(self, oracletxid, batonutxo, num):
        if hasattr(self.query, 'oracles_samples'):
            return self.query.oracles_samples(oracletxid, batonutxo, num)
        else:
            raise AttributeError("NodeRpc object has no method 'oracles_samples'")