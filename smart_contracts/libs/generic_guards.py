from pyteal import *


def generic_guards():
    # security guards
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()

    # Make sure no rekey of smart contract
    no_rekey_address = Txn.rekey_to() == Global.zero_address()

    # Make sure no one forces a fee of like 100000 algos to blow account
    acceptable_fee = Txn.fee() <= Int(5000)

    return [
        no_close_out_address,
        no_rekey_address,
        acceptable_fee,
    ]
