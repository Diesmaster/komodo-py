import time

##TODO: make it into a real object -> obj oracle represents 1 oracle


class Oracles:
    def __init__(self, query):
        self.query = query
        self.addresses = {}
        self.number_of_samples = "100000"

    def check_balance(self, address):

        balance = self.query.get_balance(address)
        if balance == 0:
            return None
        else:
            return f"Balance is enough: {balance}"

    def list_oracles(self):
        return self.query.oracles_list()

    def create_oracle(self, name, description, data_type):
        return self.query.oracle_create(name, description, data_type)

    def samples_oracle(self, oracle_txid):
        res = self.get_oracle_info(oracle_txid)
        batton_addr = res['registered'][0]['baton']
        res = self.query.oracles_samples(oracle_txid, batton_addr, self.number_of_samples)
        return res

    def get_oracle_last_data(self, oracle_txid):
        res = self.get_oracle_info(oracle_txid)
        batton_addr = res['registered'][0]['baton']
        res = self.query.oracles_samples(oracle_txid, batton_addr, 1)
        return res


    def send_oracle_creation_tx(self, hex_value):
        res = self.query.sendrawtxwrapper(hex_value)
        if not res.get('result') == 'success':
            error_message = res.get('error', 'Unknown error')
            print(f"Oracle creation failed: {error_message}")
            raise Exception(f"Oracle creation failed: {error_message}")

        return res


    def fund_oracle(self, oracle_txid):
        res = self.query.oracles_fund(oracle_txid)
        # Check if the creation was successful
        if not res.get('result') == 'success':
            error_message = res.get('error', 'Unknown error')
            print(f"Oracle fund failed: {error_message}")
            raise Exception(f"Oracle fund failed: {error_message}")

        return res

    def register_as_publisher(self, oracle_txid, data_fee):

        print("register")
        print(oracle_txid)
        print(data_fee)

        res = self.query.oracles_register(oracle_txid, data_fee)

        print(res)

        if not res.get('result') == 'success':
            error_message = res.get('error', 'Unknown error')
            print(f"Oracle register as publisher failed: {error_message}")
            raise Exception(f"Oracle register as publisher failed: {error_message}")

        return res

    def subscribe_to_oracle(self, oracle_txid, publisher_id, fee):
        res = self.query.oracles_subscribe(oracle_txid, publisher_id, fee)
        if not res.get('result') == 'success':
            error_message = res.get('error', 'Unknown error')
            print(f"Oracle subscribe failed: {error_message}")
            raise Exception(f"Oracle subscribe failed: {error_message}")

        return res

    def publish_data_string_to_oracle(self, oracle_txid, data_string, max_retry=3, retry_interval=30):

        print(data_string)

        # Convert the string to UTF-8 bytes and then to a hex string
        hex_data = data_string.encode('utf-8').hex()

        # Get the length of the original data string
        data_length = len(data_string)

        # Convert the length to a hex string
        length_hex = format(data_length, 'x')

        print(length_hex)

        if length_hex == 4:
            length_hex[1] + length_hex[0] + length_hex[3] + length_hex[2]

        if len(length_hex) < 2:
            length_hex = "0"+length_hex+"00" 

        if len(length_hex) < 3:
            length_hex = length_hex +"00"

        if len(length_hex) < 4:
            length_hex = length_hex[1] + length_hex[2] + "0"+length_hex[0]




        print(hex_data)
        print(length_hex)

        # Concatenate the length in hex and the data hex string
        final_hex_data = length_hex + hex_data

        # Send the data to the oracle
        res = self.query.oracles_data(oracle_txid, final_hex_data)

        x = 0

        while res.get('result') == 'error' and x < max_retry:
            print("Error encountered. Trying again... " + str(res))
            ret = self.subscribe_oracle_total(oracle_txid, "1")
            print(ret)
            time.sleep(retry_interval)
            res = self.query.oracles_data(oracle_txid, final_hex_data)
            x += 1

        print(res)

        pub_txid = self.query.broadcast(res['hex'])

        self.subscribe_oracle_total(oracle_txid, "1")

        return pub_txid

    def get_oracle_info(self, oracle_txid, retry_interval=30):
        res = self.query.oracles_info(oracle_txid)

        return res

    def get_oracle_info_while(self, oracle_txid, retry_interval=30):
        res = self.query.oracles_info(oracle_txid)

        # Keep checking until at least one publisher is registered
        while len(res.get('registered', [])) == 0:
            print("No publishers registered yet. Let's try again...")
            time.sleep(retry_interval)
            res = self.query.oracles_info(oracle_txid)

        return res

    def subscribe_oracle_total(self, oracle_txid, data_fee):
        res = self.get_oracle_info_while(oracle_txid)

        publisherid = res['registered'][0]['publisher']

        res = {}

        while not res.get('result'):
            res = self.subscribe_to_oracle(oracle_txid, publisherid, data_fee)
            # Check if the creation was successful
            print(res)
            if not res.get('result') == 'success':
                error_message = res.get('error', 'Unknown error')
                print(f"Oracle fund failed: {error_message}")
                raise Exception(f"Oracle fund failed: {error_message}")

        sub_txid = self.query.broadcast(res['hex'])

        print(sub_txid)

        return sub_txid

    def create_string_oracle(self, name, description, data_fee):
        # Call the oracle_create method from the wallet object

        print(data_fee)

        res = self.query.oracles_create(name, description, "S")
        
        print(res)

        oracle_txid = self.query.broadcast(res['hex'])

        print("oracle_txid")
        print(oracle_txid)

        res = self.fund_oracle(oracle_txid)

        print("fund res")
        print(res)

        fund_txid = self.query.broadcast(res['hex'])

        #print("fund tx id")
        #print(fund_txid)

        res = self.register_as_publisher(oracle_txid, data_fee)

        register_txid = self.query.broadcast(res['hex'])

        for i in range(0,10):
            try:
                res = self.subscribe_oracle_total(oracle_txid, data_fee)
                print(res)
            except BaseException as e:
                print(e)

            time.sleep(5)

        return oracle_txid