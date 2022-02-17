from pyteal import *


def contract_account(
        reserve_app_id,
        authorized_address
):
    """
    The contract account is the reserve escrow wallet.
    The Algos are the rewards to be paid to stakers.
    The USDC is the central reserve, from which collateral is pulled into escrow service accounts 1-1 to strategies.





    :param reserve_app_id: The reserve application ID. Only approve transactions grouped with it.
    :return: Compiled TEAL of contract account
    """
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()
    no_rekey_address = Txn.rekey_to() == Global.zero_address()
    acceptable_fee = Txn.fee() <= Int(5000)

    """
    Control flow logic for when users stake/unstake. The only accepted asset is USDC.
    """

    # Contract call 1 app verification. We *should* be txn 1 not 0...
    is_app_call = Gtxn[0].type_enum() == TxnType.ApplicationCall
    linked_reserve_app_id = Gtxn[0].application_id() == Int(reserve_app_id)

    # Contract call 2, a.k.a. this contract. 10458941 is the USDC asset ID
    is_asset_transfer = Txn.type_enum() == TxnType.AssetTransfer
    is_usdc = Txn.xfer_asset() == Int(10458941)

    stake_conditions = And(
        no_close_out_address,
        no_rekey_address,
        acceptable_fee,
        is_app_call,
        linked_reserve_app_id,
        is_asset_transfer,
        is_usdc
    )

    return compileTeal(stake_conditions, Mode.Signature, version=5)
