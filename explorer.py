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
            print(f"Get balance for wallet: {addr}: {res.text}")
            

        except Exception as e:
            print("explorer_get_balance " + str(e))
            raise Exception(e)

        return int(res.text)


    def get_utxos( self, addr ):

        print("Get UTXO for wallet " + addr)

        if type(addr) is not str:
            print("Query wallet must be string")
            raise Exception("Query Wallet must be string")


        full_url = self.url + self.root + self.address + addr + self.utxo
        try:
            res = requests.get(full_url)
        
        except Exception as e:
            print("explorer_get_utxos " + str(e))
            raise Exception(e)
        

        return res.text

    def get_transaction( self, txid ):
        
        print("Get transaction " + txid)
        print("start explorer_get_transaction")

        if type(txid) is not str:
            print("TXID must be string")
            raise Exception("TXID must be string")
        print("Get transaction " + txid)

        full_url = self.url + self.root + self.transaction + txid

        try:
            res = requests.get(full_url)
            print("end explorer_get_transaction")
        except Exception as e:
            print("explorer_get_transaction " + str(e))
            raise Exception(e)
        return res.text

    def get_network_status( self ):
        
        print("Get network status")
        try:
            full_url = self.url + self.root + self.status    
            res = requests.get(full_url)
            print("Result network status : " + str(res.json()))
            return res.json()
    
        except Exception as e:
            raise Exception(e)

