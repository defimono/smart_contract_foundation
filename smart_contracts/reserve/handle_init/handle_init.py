from pyteal import *


def handle_init():
    return Seq([
        App.globalPut(Bytes("admin"), Txn.sender()),
        App.globalPut(Bytes("total_risk"), Int(0)),

        Return(Int(1))
    ])
