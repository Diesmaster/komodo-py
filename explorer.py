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
        #print("start broadcast_via_explorer")

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

        try:
            broadcast_res = requests.post(full_url, data=params)
            if len(broadcast_res.text) < 64: # TODO check if json, then if the json has a txid field and it is 64
                print("error")
                print(broadcast_res.text)
                raise Exception(broadcast_res.text)
            else:
                return json.loads(broadcast_res.text)

        except Exception as e:
            print(str(broadcast_res.__dict__))
            # log2discord(f"---\nThere is an exception during the broadcast: **{params}**\n Error: **{e}**\n---")
            print("rawtx: " + str(signedtx))
            # log2discord(rawtx_text)
            print("broadcast_via_explorer " + str(e))
            raise(e)

class QueryInterface:
    def __init__(self, url):
        # Initialize an Explorer object with the given URL
        self.query = Explorer(url)

    def get_balance(self, addr):
        if hasattr(self.query, 'get_balance'):
            return self.query.get_balance(addr)
        else:
            raise AttributeError("Explorer object has no method 'get_balance'")

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

    def get_network_status(self):
        if hasattr(self.query, 'get_network_status'):
            return self.query.get_network_status()
        else:
            raise AttributeError("Explorer object has no method 'get_network_status'")

    def broadcast(self, signedtx):
        if hasattr(self.query, 'broadcast_via_explorer'):
            return self.query.broadcast_via_explorer(signedtx)
        else:
            raise AttributeError("Explorer object has no method 'broadcast_via_explorer'")

