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

    ### oracle functions
    def oracles_create(self, name, description, data_type):
        try:
            oracles_hex = self.rpc_connection.oraclescreate(name, description, data_type)
        except Exception as e:
            raise Exception(f"Error in oracles_create: {e}")
        return oracles_hex

    def oracles_fund(self, oracle_id):
        try:
            oracles_fund_hex = self.rpc_connection.oraclesfund(oracle_id)
        except Exception as e:
            raise Exception(f"Error in oracles_fund: {e}")
        return oracles_fund_hex

    def oracles_register(self, oracle_id, data_fee):
        try:
            oracles_register_hex = self.rpc_connection.oraclesregister(oracle_id, data_fee)
        except Exception as e:
            raise Exception(f"Error in oracles_register: {e}")
        return oracles_register_hex

    def oracles_subscribe(self, oracle_id, publisher_id, data_fee):
        try:
            oracles_subscribe_hex = self.rpc_connection.oraclessubscribe(oracle_id, publisher_id, data_fee)
        except Exception as e:
            raise Exception(f"Error in oracles_subscribe: {e}")
        return oracles_subscribe_hex

    def oracles_info(self, oracle_id):
        try:
            oracles_info = self.rpc_connection.oraclesinfo(oracle_id)
        except Exception as e:
            raise Exception(f"Error in oracles_info: {e}")
        return oracles_info

    def oracles_data(self, oracle_id, hex_string):
        try:
            oracles_data = self.rpc_connection.oraclesdata(oracle_id, hex_string)
        except Exception as e:
            raise Exception(f"Error in oracles_data: {e}")
        return oracles_data

    def oracles_list(self):
        try:
            oracles_list = self.rpc_connection.oracleslist()
        except Exception as e:
            raise Exception(f"Error in oracles_list: {e}")
        return oracles_list

    def oracles_samples(self, oracletxid, batonutxo, num):
        try:
            oracles_sample = self.rpc_connection.oraclessamples(oracletxid, batonutxo, num)
        except Exception as e:
            raise Exception(f"Error in oracles_samples: {e}")
        return oracles_sample
