from pyteal import *


def assert_stake_guards():
    asserted = []

    for guard in stake_guards():
        asserted.append(Assert(guard))

    return asserted


def stake_guards():
    # The noop must be in position 1 in the group and of type app call
    is_app_call = Txn.type_enum() == TxnType.ApplicationCall

    # Contract call 2, a.k.a. the statekess escrow payment. 31566704 is the
    # USDC asset ID.
    is_asset_transfer = Gtxn[1].type_enum() == TxnType.AssetTransfer
    is_usdc = Gtxn[1].xfer_asset() == Int(10458941)

    return [
        is_app_call,
        is_asset_transfer,
        is_usdc
    ]
