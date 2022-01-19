from pyteal import *

from smart_contracts.reserve.security.stake import assert_stake_guards


def unstake():
    global_staked_state: App = App.globalGet(Bytes('total_staked'))
    local_staked_state: App = App.localGet(Int(0), Bytes('staked'))

    return Seq([
        *assert_stake_guards(),
        # Assert(Gtxn[1].sender() == contract_account),
        App.globalPut(Bytes("total_staked"), global_staked_state - Gtxn[1].asset_amount()),
        App.localPut(Int(0), Bytes("staked"), local_staked_state - Gtxn[1].asset_amount()),

        Return(Int(1))
    ])
