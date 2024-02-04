from slickrpc import Proxy

class NodeRpc:
    def __init__(self, rpc_user, rpc_password, rpc_port, priv_key, node_ip):
        self.rpc_connection = self.rpc_connect(rpc_user, rpc_password, rpc_port, node_ip)
        self.import_priv_key(priv_key)

    def rpc_connect(self, rpc_user, rpc_password, rpc_port, node_ip):
        try:
            rpc_connection = Proxy(f"http://{rpc_user}:{rpc_password}@{node_ip}:{rpc_port}")
        except Exception as e:
            raise Exception(f"Connection error: {e}")
        return rpc_connection

    def import_priv_key(self, priv_key):
        try:
            self.rpc_connection.importprivkey(priv_key)
        except Exception as e:
            raise Exception(f"Error importing private key: {e}")


    def import_priv_key(self, priv_key):
        try:
            self.rpc_connection.importprivkey(priv_key)
        except Exception as e:
            raise Exception(f"Error importing private key: {e}")


    def get_balance(self, addr):
        try:
            balance = self.rpc_connection.getbalance()
        except Exception as e:
            raise Exception(f"Error getting balance: {e}")
        return balance

    def get_utxos(self, addr):
        try:
            utxos = self.rpc_connection.listunspent(1, 9999999, [addr])
        except Exception as e:
            raise Exception(f"Error getting UTXOs: {e}")
        return utxos

    def get_transaction(self, txid):
        try:
            transaction = self.rpc_connection.gettransaction(txid)
        except Exception as e:
            raise Exception(f"Error getting transaction: {e}")
        return transaction

    def get_network_status(self):
        try:
            info = self.rpc_connection.getinfo()
        except Exception as e:
            raise Exception(f"Error getting network status: {e}")
        return info

    def broadcast(self, signedtx):
        try:
            tx_id = self.rpc_connection.sendrawtransaction(signedtx)
        except Exception as e:
            raise Exception(f"Error broadcasting transaction: {e}")
        return tx_id

    def getinfo(self):
        try:
            info = self.rpc_connection.getinfo()
        except Exception as e:
            raise Exception(f"Error getting node info: {e}")
        return info
