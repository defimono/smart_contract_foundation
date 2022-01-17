from pyteal import *


def premiums(
        admin_address,
):
    """
    Premiums paid to the platform. Only the admin can withdraw.
    """
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()
    no_rekey_address = Txn.rekey_to() == Global.zero_address()
    acceptable_fee = Txn.fee() <= Int(10000)
    correct_withdraw_address = Txn.sender() == Addr(admin_address)

    conditions = And(
        no_close_out_address,
        no_rekey_address,
        acceptable_fee,
        correct_withdraw_address
    )

    return compileTeal(conditions, Mode.Signature, version=5)
