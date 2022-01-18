from algosdk.future import transaction

from config.algod_client import algod_client
from config.load_app_config import app_config
from config.logger import logger
from modules.helpers.compile import compile_program
from smart_contracts.clear_state_program import clear_state_program
from smart_contracts.reserve.app import reserve


def update_stateful_contract(app_id):
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    application_approval_teal = reserve()

    application_clear_teal = clear_state_program()

    # compile program to binary
    approval_program_compiled = compile_program(application_approval_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(application_clear_teal)

    logger.info("Updating stateful reserve smart contract...")

    # get node suggested parameters
    params = algod_client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationUpdateTxn(
        admin_address,
        params,
        app_id,
        approval_program_compiled,
        clear_state_program_compiled,
    )

    # sign transaction
    signed_txn = txn.sign(admin_private_key)

    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)

    # display results
    transaction_response = algod_client.pending_transaction_info(tx_id)

    app_id = transaction_response['application-index']

    logger.info("Updated stateful reserve contract with app_id: {}".format(app_id))

    return app_id
