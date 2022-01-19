from pyteal import *

from smart_contracts.reserve.security.stake import assert_stake_guards


@Subroutine(TealType.anytype)
def global_must_get(key: TealType.bytes) -> Expr:
    """Returns the result of a global storage MaybeValue if it exists, else Assert and fail the program"""
    maybe = App.globalGetEx(Int(0), key)
    return Seq(maybe, Assert(maybe.hasValue()), maybe.value())


def stake():
    global_staked_state: App = App.globalGet(Bytes('total_staked'))
    local_staked_state: App = App.localGet(Int(0), Bytes('staked'))

    contract_account = global_must_get(Bytes('contract_account'))

    return Seq([
        *assert_stake_guards(),
        # Assert(Gtxn[1].receiver() == App.globalGet(Bytes('contract_account'))),
        App.globalPut(Bytes("total_staked"), global_staked_state + Gtxn[1].asset_amount()),
        App.localPut(Int(0), Bytes("staked"), local_staked_state + Gtxn[1].asset_amount()),

        Return(Int(1))
    ])
