from pyteal import *


def update_escrow():
    return Seq([
        App.globalPut(Bytes("contract_account"), Txn.application_args[1]),

        Return(Int(1))
    ])
