import pycurl
from io import BytesIO
import json

class NodeRpc:
    def __init__(self, rpc_user, rpc_password, rpc_port, priv_key, node_ip):
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.rpc_port = rpc_port
        self.node_ip = node_ip
        self.rpc_url = f"https://{node_ip}:{rpc_port}/"
        self.headers = ["Content-Type: application/json"]
        self.import_priv_key(priv_key)

    def rpc_call(self, method, params=[]):
        buffer = BytesIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, self.rpc_url)
        curl.setopt(curl.USERPWD, f"{self.rpc_user}:{self.rpc_password}")
        curl.setopt(curl.HTTPHEADER, self.headers)
        curl.setopt(curl.POST, 1)
        
        data = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": method,
            "params": params
        }
        post_data = json.dumps(data)
        curl.setopt(curl.POSTFIELDS, post_data)
        curl.setopt(curl.WRITEFUNCTION, buffer.write)
        
        try:
            curl.perform()
            curl.close()
        except pycurl.error as e:
            raise Exception(f"Curl error: {e}")

        response = buffer.getvalue().decode('utf-8')
        response_json = json.loads(response)
        
        if response_json.get("error"):
            raise Exception(f"RPC error: {response_json['error']}")
        
        return response_json["result"]

    def import_priv_key(self, priv_key):
        try:
            ret = self.rpc_call("importprivkey", [priv_key])
        except Exception as e:
            print(str(e))
            raise Exception(f"Error importing private key: {e}")

    def get_balance(self, addr=None):
        try:
            if addr:
                balance = self.rpc_call("getreceivedbyaddress", [addr])
            else:
                balance = self.rpc_call("getbalance")
        except Exception as e:
            raise Exception(f"Error getting balance: {e}")
        return balance

    def get_utxos(self, addr):
        try:
            utxos = self.rpc_call("listunspent", [1, 9999999, [addr]])
        except Exception as e:
            raise Exception(f"Error getting UTXOs: {e}")
        return utxos

    def get_mempool(self, addr):
        try:
            utxos = self.rpc_call("getaddressmempool", [{"addresses": [addr]}])
        except Exception as e:
            raise Exception(f"Error getting UTXOs: {e}")
        return utxos

    def get_transaction(self, txid):
        try:
            transaction = self.rpc_call("gettransaction", [txid])
        except Exception as e:
            raise Exception(f"Error getting transaction: {e}")
        return transaction

    def get_block(self, hash_or_height, verbose=True):
        try:
            block_info = self.rpc_call("getblock", [hash_or_height, verbose])
        except Exception as e:
            raise Exception(f"Error getting block: {e}")
        return block_info

    def get_blockcount(self):
        try:
            block_info = self.rpc_call("getblockcount")
        except Exception as e:
            raise Exception(f"Error getting block count: {e}")
        return block_info

    def get_network_status(self):
        try:
            info = self.rpc_call("getinfo")
        except Exception as e:
            raise Exception(f"Error getting network status: {e}")
        return info

    def broadcast(self, signedtx):
        try:
            print("broadcast node")
            tx_id = self.rpc_call("sendrawtransaction", [signedtx])
            print("res: " + str(tx_id))
        except Exception as e:
            print(str(e))
            print(signedtx)
            raise Exception(f"Error broadcasting transaction: {e}")
        return tx_id

    def getinfo(self):
        try:
            info = self.rpc_call("getinfo")
        except Exception as e:
            raise Exception(f"Error getting node info: {e}")
        return info

    def get_rawtransaction(self, txid):
        try:
            tx = self.rpc_call("getrawtransaction", [txid])
        except Exception as e:
            raise Exception(f"Error getting tx: {e}")
        return tx

    ### oracle functions
    def oracles_create(self, name, description, data_type):
        try:
            oracles_hex = self.rpc_call("oraclescreate", [name, description, data_type])
        except Exception as e:
            raise Exception(f"Error in oracles_create: {e}")
        return oracles_hex

    def oracles_fund(self, oracle_id):
        try:
            oracles_fund_hex = self.rpc_call("oraclesfund", [oracle_id])
        except Exception as e:
            raise Exception(f"Error in oracles_fund: {e}")
        return oracles_fund_hex

    def oracles_register(self, oracle_id, data_fee):
        try:
            oracles_register_hex = self.rpc_call("oraclesregister", [oracle_id, data_fee])
        except Exception as e:
            raise Exception(f"Error in oracles_register: {e}")
        return oracles_register_hex

    def oracles_subscribe(self, oracle_id, publisher_id, data_fee):
        try:
            oracles_subscribe_hex = self.rpc_call("oraclessubscribe", [oracle_id, publisher_id, data_fee])
        except Exception as e:
            raise Exception(f"Error in oracles_subscribe: {e}")
        return oracles_subscribe_hex

    def oracles_info(self, oracle_id):
        try:
            oracles_info = self.rpc_call("oraclesinfo", [oracle_id])
        except Exception as e:
            raise Exception(f"Error in oracles_info: {e}")
        return oracles_info

    def oracles_data(self, oracle_id, hex_string):
        try:
            oracles_data = self.rpc_call("oraclesdata", [oracle_id, hex_string])
        except Exception as e:
            raise Exception(f"Error in oracles_data: {e}")
        return oracles_data

    def oracles_list(self):
        try:
            oracles_list = self.rpc_call("oracleslist")
        except Exception as e:
            raise Exception(f"Error in oracles_list: {e}")
        return oracles_list

    def oracles_samples(self, oracletxid, batonutxo, num):
        try:
            oracles_sample = self.rpc_call("oraclessamples", [oracletxid, batonutxo, num])
        except Exception as e:
            raise Exception(f"Error in oracles_samples: {e}")
        return oracles_sample
