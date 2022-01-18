from pyteal import *


def assert_stake_guards():
    asserted = []

    for guard in stake_guards():
        asserted.append(Assert(guard))

    return asserted


def stake_guards():
    # The noop must be in position 1 in the group and of type app call
    is_app_call = Gtxn[0].type_enum() == TxnType.ApplicationCall
    linked_reserve_app_id = Gtxn[0].application_id() == GeneratedID(Int(0))

    # Contract call 2, a.k.a. this contract. 31566704 is the USDC asset ID.
    is_asset_transfer = Gtxn[1].type_enum() == TxnType.AssetTransfer
    is_usdc = Gtxn[1].xfer_asset() == Int(31566704)

    return [
        is_app_call,
        linked_reserve_app_id,
        is_asset_transfer,
        is_usdc
    ]
