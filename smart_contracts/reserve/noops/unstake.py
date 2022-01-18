from pyteal import *


def unstake():
    staked_state: App = App.localGet(Int(0), Bytes('staked'))
    contract_account: App = App.localGet(Int(0), Bytes('contract_account'))

    return Seq([
        # *assert_stake_guards(),
        Assert(Gtxn[1].sender() == contract_account),
        App.localPut(Int(0), Bytes("staked"), staked_state - Gtxn[1].amount()),

        Return(Int(1))
    ])
