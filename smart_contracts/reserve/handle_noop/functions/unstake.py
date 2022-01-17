from pyteal import *


def unstake():
    staked_state: App = App.localGet(Int(0), Bytes('staked'))

    return Seq([
        App.localPut(Int(0), Bytes("staked"), staked_state - Gtxn[1].amount()),

        Return(Int(1))
    ])
