from pyteal import *


def reserve(
        reserve_app_id,
):
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()
    no_rekey_address = Txn.rekey_to() == Global.zero_address()
    acceptable_fee = Txn.fee() <= Int(5000)
    is_app_call = Gtxn[0].type_enum() == TxnType.ApplicationCall
    # linked_reserve_app_id = Gtxn[0].application_id() == Int(reserve_app_id)

    conditions = And(
        no_close_out_address,
        is_app_call,
        no_rekey_address,
        acceptable_fee,
    )

    return compileTeal(conditions, Mode.Signature, version=5)
