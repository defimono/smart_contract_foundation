from pyteal import *


def reserve_contract_account(reserve_app_id):
    """
    asset transfers are a separate transaction type to an algorand payment transaction. pay != axfer
    :param reserve_app_id: The reserve application ID. Only approve transactions grouped with it.
    :return: Compiled TEAL of contract account
    """
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()
    no_rekey_address = Txn.rekey_to() == Global.zero_address()
    acceptable_fee = Txn.fee() <= Int(5000)

    """
    Control flow logic for when users stake/unstake. The only accepted asset is USDC.
    First transaction is to the application, second is to the contract account.
    
    # For stake/unstake:
    txn 0 must be app call noop
    txn 0 must be reserve app id
    txn 1 must be type asset transfer
    txn 1 must be asset id 31566704
    
    """
    # Contract call 1 app verification
    is_app_call = Gtxn[0].type_enum() == TxnType.ApplicationCall
    linked_reserve_app_id = Gtxn[0].application_id() == Int(reserve_app_id)

    # Contract call 2, a.k.a. this contract. 31566704 is the USDC asset ID.
    is_asset_transfer = Gtxn[1].type_enum() == TxnType.AssetTransfer
    is_usdc = Gtxn[1].xfer_asset() == Int(31566704)
    correct_receiver = Gtxn[1].receiver() == GeneratedID(1)

    stake_conditions = And(
        no_close_out_address,
        no_rekey_address,
        acceptable_fee,
        is_app_call,
        linked_reserve_app_id,
        is_asset_transfer,
        correct_receiver,
        is_usdc
    )

    return compileTeal(stake_conditions, Mode.Signature, version=5)
