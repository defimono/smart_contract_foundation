from pyteal import *


def update_contract_account():
    contract_account = Txn.application_args[1]

    return Seq([
        App.globalPut(Bytes("contract_account"), contract_account),

        Return(Int(1))
    ])
