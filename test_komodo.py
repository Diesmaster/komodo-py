import pytest
import requests
import json
import random
from ecpy.curves     import Curve,Point

from unittest.mock import patch, Mock
from explorer import Explorer  
from wallet import Wallet
from transaction import *


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

def test_ecG():
    obj = Wallet("hihi")
    cv_value = Curve.get_curve('secp256k1')
    
    # Call the ecG method
    point = obj.ecG(cv_value)
    
    # Assertions
    assert point.x == 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    assert point.y == 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

def test_serializePoint():
    wal = Wallet('hihi')

    # Assuming cv is set (either 'secp256k1' or an actual curve object)
    cv = Curve.get_curve('secp256k1')

    # Generate points
    p = wal.ecG(cv)
    points = [p, 2*p, 3*p, 4*p, 5*p]

    # Expected serialized outputs
    expected_outputs = [
        b'\x02y\xbef~\xf9\xdc\xbb\xacU\xa0b\x95\xce\x87\x0b\x07\x02\x9b\xfc\xdb-\xce(\xd9Y\xf2\x81[\x16\xf8\x17\x98',
        b'\x02\xc6\x04\x7f\x94A\xed}m0E@n\x95\xc0|\xd8\\w\x8eK\x8c\xef<\xa7\xab\xac\t\xb9\\p\x9e\xe5',
        b'\x02\xf90\x8a\x01\x92X\xc3\x10I4O\x85\xf8\x9dR)\xb51\xc8E\x83o\x99\xb0\x86\x01\xf1\x13\xbc\xe06\xf9',
        b'\x02\xe4\x93\xdb\xf1\xc1\r\x80\xf3X\x1eI\x04\x93\x0b\x14\x04\xccl\x13\x90\x0e\xe0u\x84t\xfa\x94\xab\xe8\xc4\xcd\x13'
    ]

    # Validate each point
    for point, expected_output in zip(points, expected_outputs):
        serialized = wal.serializePoint(point)
        assert serialized == expected_output



def test_base58Iguana():

    wal = Wallet('hihi')

    # Assuming cv is set (either 'secp256k1' or an actual curve object)
    cv = Curve.get_curve('secp256k1')

    # Generate a point
    p = wal.ecG(cv)

    # Serialize the point
    ret = wal.serializePoint(p)

    # Base58 encode using Iguana
    encoded_ret = wal.base58Iguana(ret)

    # Assert the result
    assert encoded_ret == "jesTu2BpszP8DKSoi1R5G6ggjHrsrVnboLdx6V47vkoR"

    # Generate a random bytestring
    random_bytestring = bytes([random.randint(0, 255) for _ in range(32)])

    # Base58 encode and then decode using Iguana
    encoded_random_str = wal.base58Iguana(random_bytestring)
    decoded_random_bytes = wal.base58DecodeIguana(encoded_random_str)  # Assuming you have implemented this function

    # Assert that the original and decoded bytestrings are the same
    assert random_bytestring == decoded_random_bytes


@pytest.mark.parametrize("seed, expected", [
    ("This is a test string hahaha", {'wif': 'UrRj8cUwadaGcbbgTm8xZbnP7PbkakoUpXvddyR5vydMkRuyCVWz', 'address': 'RHhezrNf5u87gNexawSn1bj7fUKuX1kn94', 'pubkey': '03b0a780e5d9a8a7adb6c8dbc357bd28799172666fc3f2c1b8d5310024a62edf38', 'privkey': '481d9e62898116cf9a7aa2d286b4bddde312057bd077bdc858b463f617e53f44'}),
    ("This is not a test string", {'wif': 'UuvhVqMuEv343WP9oJW2M16HtyHdgWjpXf3x22aW9hM9RggK7uD4', 'address': 'RMsHcBWu5C6Uuq9VKrbggMHhzPcP686xpo', 'pubkey': '02f60c752ab2c73d86780cfdabc6b9ffb2196c5500f7be0d8739d33d6636991708', 'privkey': 'b08837323b995d7d1b055de66dfb07b805fac947afd807cc29edc0632942ff63'}),
    ("I love komdo", {'wif': 'UtaZYRFbSzXMBk4KjLfut6DzE9ypTco1L3jEHPYvj9dDQWS2soWq', 'address': 'RT89DMeAo1HVaCxGdJPCf56kiJn3boQpXC', 'pubkey': '02457e4746fa51259ec6e6a43f7251e60af86282799ed885741fe315ea970f0966', 'privkey': '8855db3b114d566b036ca7ba775bfa1438493b97745ea0fb2649f03c85a15849'}),
    ("I love python", {'wif': 'UvjgQCyd2PqJyq9t37yCM5SLQGeNDbyDR1qFqx9niPuCJ3eL8CMn', 'address': 'RWiFJ5nchpP76B8PAX4Ma2yEvadCZU2wa5', 'pubkey': '02acd7fe6e80563a5425eb4cf3382f60e9446cffa6c7d05615b4e7cecc6b0dc528', 'privkey': 'c8b370f0419ff4e3a8b57f2a26ee861849936a64a4b8dbf7b2ad50894d94007b'}),
])
def test_create_wallet(seed, expected):
    wallet = Wallet(seed)
    result = wallet.create_wallet()
    assert result == expected


def test_serialize_outputs( ):
    tx = Transaction( )
    ex = Explorer("https://ofcmvp.explorer.batch.events/")

    wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

    to_address =  "RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i" 
    amount = 1

    address = wal.get_address()


    from_scriptpubkey = wal.get_scriptpubkkey()

    tx = Transaction(from_scriptpubkey)

    if isinstance(to_address, list) == True:
        for x in range(0, len(to_address)):
            print(to_address[x])
            to_scriptpubkey = wal.base58DecodeIguana(to_address[x]).hex()[2:-8]
            tx.add_output( amount[x], to_scriptpubkey )

        for out in tx.tx_outs:
            print(out)
    else:
        to_scriptpubkey = wal.base58DecodeIguana(to_address).hex()[2:-8]
        tx.add_output( amount, to_scriptpubkey )

    utxos = json.loads(ex.get_utxos( address ))
    utxo = find_utxo( utxos, 1 )


    tx.add_input( utxo['txid'], utxo['amount'], utxo['vout'], utxo['scriptPubKey'])

    ser_tx = tx.serialize_outputs()
    print(ser_tx)

    n_outputs = integer_value = int(ser_tx[:2], 16)
    ser_tx = ser_tx[2:]

    assert n_outputs < 252

    for n in range(0, n_outputs):
        amount = ser_tx[:16]
        ser_tx = ser_tx[16:]

        script = ser_tx[:8]
        ser_tx = ser_tx[8:]
        assert script == "1976a914"

        key = ser_tx[:40]
        ser_tx = ser_tx[40:]
        assert key == wal.get_scriptpubkkey()


        script_key_script = ser_tx[:4]
        ser_tx = ser_tx[4:]
        assert script_key_script == "88ac"    


def test_serialize_sign_precursor( ):
    tx = Transaction( )
    ex = Explorer("https://ofcmvp.explorer.batch.events/")

    wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

    to_address =  "RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i" 
    amount = 1

    address = wal.get_address()


    from_scriptpubkey = wal.get_scriptpubkkey()

    tx = Transaction(from_scriptpubkey)

    if isinstance(to_address, list) == True:
        for x in range(0, len(to_address)):
            print(to_address[x])
            to_scriptpubkey = wal.base58DecodeIguana(to_address[x]).hex()[2:-8]
            tx.add_output( amount[x], to_scriptpubkey )

        for out in tx.tx_outs:
            print(out)
    else:
        to_scriptpubkey = wal.base58DecodeIguana(to_address).hex()[2:-8]
        tx.add_output( amount, to_scriptpubkey )

    utxos = json.loads(ex.get_utxos( address ))
    utxo = find_utxo( utxos, 1 )


    tx.add_input( utxo['txid'], utxo['amount'], utxo['vout'], utxo['scriptPubKey'])

    ser_tx = tx.serialize()

    ser_tx = tx.serialize_sign_precurser()    

    header = ser_tx[:16]
    ser_tx = ser_tx[16:]
    assert header == "0400008085202f89"

    hashes = ser_tx[:384]
    ser_tx = ser_tx[384:]

    locktime  = ser_tx[:8]
    ser_tx = ser_tx[8:]

    ex_hight_nvb = ser_tx[:24]
    ser_tx = ser_tx[24:]

    assert ex_hight_nvb == "000000000000000000000000"

    hashtype = ser_tx[:8]
    ser_tx = ser_tx[8:]
    assert hashtype == "01000000"


    txins_check = tx.serialize_input_sign()
    n = len(txins_check)
    txins = ser_tx[:n]
    ser_tx = ser_tx[n:]
    assert txins_check == txins

    script = ser_tx[:8]
    ser_tx = ser_tx[8:]
    assert script == "1976a914"

    key = ser_tx[:40]
    ser_tx = ser_tx[40:]
    assert key == wal.get_scriptpubkkey()
    
    script_key_script = ser_tx[:4]
    ser_tx = ser_tx[4:]
    assert script_key_script == "88ac" 

    val = ser_tx[:16]
    ser_tx = ser_tx[16:]
    val = bytes.fromhex(val)[::-1].hex()
    val = val.lstrip('0') # Removing the leading zeros
    val = int(val, 16)
    check_val = tx.get_ins_total()
    assert check_val == val

    assert ser_tx == "ffffffff"     

def test_serialize_inputs( ):
    tx = Transaction( )
    ex = Explorer("https://ofcmvp.explorer.batch.events/")

    wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

    to_address =  "RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i" 
    amount = 1

    address = wal.get_address()


    from_scriptpubkey = wal.get_scriptpubkkey()

    tx = Transaction(from_scriptpubkey)

    if isinstance(to_address, list) == True:
        for x in range(0, len(to_address)):
            print(to_address[x])
            to_scriptpubkey = wal.base58DecodeIguana(to_address[x]).hex()[2:-8]
            tx.add_output( amount[x], to_scriptpubkey )

        for out in tx.tx_outs:
            print(out)
    else:
        to_scriptpubkey = wal.base58DecodeIguana(to_address).hex()[2:-8]
        tx.add_output( amount, to_scriptpubkey )

    utxos = json.loads(ex.get_utxos( address ))
    utxo = find_utxo( utxos, 1 )


    tx.add_input( utxo['txid'], utxo['amount'], utxo['vout'], utxo['scriptPubKey'])

    ser_in = tx.serialize_inputs()

    assert ser_in[:18] == "0400008085202f8901"
    assert ser_in[-8:] == "ffffffff"
    assert len(ser_in) == 98

@pytest.mark.parametrize("amount", [1, 20, 300, 1000])
def test_find_utxo( amount):
    ex = Explorer("https://ofcmvp.explorer.batch.events/")  # Initialize your class
    test_address = 'RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i'

    result = ex.get_utxos(test_address)
    utxo = find_utxo(json.loads(result), amount)

    assert utxo['amount'] >= amount
    assert utxo['confirmations'] >= 1



@pytest.mark.parametrize("to_addie, amount", [
    ("RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i", 1),
    (["RGKg9LCmU5i9JL2PceLbhM9HenHmMzDU7i"], [1]),
    (["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1,1]),
])
def test_make_address_transaction( to_addie, amount ):
    tx = Transaction( )
    ex = Explorer("https://ofcmvp.explorer.batch.events/")

    wal = Wallet("pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

    tx_in = TxInterface(ex, wal)

    rawtx = tx_in.make_address_transaction( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] )

    try :
        res = ex.broadcast_via_explorer( rawtx )
        assert json.loads(res)['txid']


    except Exception as e:
        assert e == Exception('. Code:-25')
        #code 25 is that the explorer complains about spam