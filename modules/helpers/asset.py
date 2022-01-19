from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation

from config.algod_client import algod_client
from config.logger import logger


def user_opt_in(address, private_key, app_id):
    params = algod_client.suggested_params()

    opt_in_transaction = transaction.ApplicationOptInTxn(
        address,
        params,
        app_id
    )

    signed_opt_in = opt_in_transaction.sign(private_key)

    tx_id = signed_opt_in.get_txid()

    # send transaction
    algod_client.send_transactions([signed_opt_in])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)

    # display results
    transaction_response = algod_client.pending_transaction_info(tx_id)

    logger.info(transaction_response)


def user_opt_out(address, private_key, app_id):
    params = algod_client.suggested_params()

    opt_in_transaction = transaction.ApplicationClearStateTxn(
        address,
        params,
        app_id
    )

    signed_opt_in = opt_in_transaction.sign(private_key)

    tx_id = signed_opt_in.get_txid()

    # send transaction
    algod_client.send_transactions([signed_opt_in])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)

    # display results
    transaction_response = algod_client.pending_transaction_info(tx_id)

    logger.info(transaction_response)

    return transaction_response
