import pytest
import requests
import json

from unittest.mock import patch, Mock
from explorer import Explorer  

@pytest.fixture
def mock_response():
    return {
        'info': {
            'version': 70200,
            'protocolversion': 170011,
            'blocks': 572080,
            'timeoffset': 0,
            'connections': 20,
            'proxy': '',
            'difficulty': 1851.978976535526,
            'testnet': False,
            'relayfee': 1e-06,
            'errors': '',
            'notarized': 0,
            'network': 'livenet',
            'lastNotarizedBlockhash': '0000000000000000000000000000000000000000000000000000000000000000'
        }
    }

@pytest.fixture
def mock_integer_response():
    return "1000"

@pytest.fixture
def mock_utxos_response():
    return json.dumps([
        {
            "address": "RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB",
            "txid": "d062912291ced3990af0393ec4887fb4aaf86869c31569702b87dfd6471ced39",
            "vout": 0,
            "scriptPubKey": "2102acd3058603f6fcb30daa487c19fcebd393a1af088a7985717479677935e05e44ac",
            "amount": 25,
            "satoshis": 2500000000,
            "height": 572076,
            "confirmations": 32
        }
    ])

@pytest.fixture
def mock_transaction_response():
    return json.dumps({
        "txid": "d062912291ced3990af0393ec4887fb4aaf86869c31569702b87dfd6471ced39",
        "version": 4,
        "locktime": 1693420841,
        "confirmations": 49,
        "notarized": False,
        "height": 572076,
        "lastNotarizedHeight": 0,
        "vin": [{"coinbase": "03acba080101", "sequence": 4294967295, "n": 0}],
        "vout": [{
            "value": "25.00000000",
            "n": 0,
            "scriptPubKey": {
                "hex": "2102acd3058603f6fcb30daa487c19fcebd393a1af088a7985717479677935e05e44ac",
                "asm": "02acd3058603f6fcb30daa487c19fcebd393a1af088a7985717479677935e05e44 OP_CHECKSIG",
                "addresses": ["RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB"],
                "type": "pubkeyhash"
            },
            "spentTxId": None,
            "spentIndex": None,
            "spentHeight": None
        }],
        "vjoinsplit": [],
        "blockhash": "03802ecf4ba9251c38c88960ae9d2b77c574f297e5fe0b3541ef0603bb322878",
        "blockheight": 572076,
        "time": 1693420828,
        "blocktime": 1693420828,
        "isCoinBase": True,
        "valueOut": 25,
        "size": 120,
        "fOverwintered": True,
        "nVersionGroupId": 2301567109,
        "nExpiryHeight": 0,
        "valueBalance": 0,
        "spendDescs": [],
        "outputDescs": []
    })

def test_get_network_status(mock_response):
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.json.return_value = mock_response

        ex = Explorer("https://ofcmvp.explorer.batch.events/")  # Initialize your class

        result = ex.get_network_status()

        print("##### mock #####")
        print(mock_response)
        print("##### resp #####")
        print(result)

        assert result == mock_response


def test_get_balance(mock_integer_response):
    with patch('requests.get') as mocked_get:
        mocked_get.return_value = Mock()
        mocked_get.return_value.text = mock_integer_response

        ex = Explorer("https://ofcmvp.explorer.batch.events/")  # Initialize your class

        test_address = 'RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB'
        result = ex.get_balance(test_address)

        assert result == int(mock_integer_response)


def test_get_utxos(mock_utxos_response):
    with patch('requests.get') as mocked_get:
        mocked_get.return_value = Mock()
        mocked_get.return_value.text = mock_utxos_response

        ex = Explorer("https://ofcmvp.explorer.batch.events/")  # Initialize your class
        test_address = 'RGkJwsapuVx4yCR4ktaLm2P7Q2i83cznKB'

        result = ex.get_utxos(test_address)

        assert result == mock_utxos_response

def test_get_transaction(mock_transaction_response):
    with patch('requests.get') as mocked_get:
        mocked_get.return_value = Mock()
        mocked_get.return_value.text = mock_transaction_response

        ex = Explorer("https://ofcmvp.explorer.batch.events/")  # Initialize your class
        test_txid = 'd062912291ced3990af0393ec4887fb4aaf86869c31569702b87dfd6471ced39'
        result = ex.get_transaction(test_txid)

        assert result == mock_transaction_response