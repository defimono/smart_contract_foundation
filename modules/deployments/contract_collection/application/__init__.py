from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation

from config.algod_client import algod_client
from config.load_app_config import app_config
from config.logger import logger
from modules.helpers.compile import compile_program
from modules.helpers.configure_state_params import configure_state_params
from smart_contracts.clear_state_program import clear_state_program
from smart_contracts.contract_collection.contract_collection_application import contract_collection_application


def create():
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    global_schema, local_schema = configure_state_params(
        local_ints=16,
        local_bytes=0,
        global_ints=0,
        global_bytes=1
    )

    application_approval_teal = contract_collection_application()

    application_clear_teal = clear_state_program()

    # compile program to binary
    approval_program_compiled = compile_program(application_approval_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(application_clear_teal)

    logger.info("Deploying Contract collection smart contract...")

    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = algod_client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        admin_address,
        params,
        on_complete,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema
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

    logger.info(
        "Deployed stateful contract collection contract with app_id: {}".format(app_id))

    return app_id


def delete(app_id):
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    logger.info("Deleting stateful contract collection smart contract...")

    # get node suggested parameters
    params = algod_client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(
        admin_address,
        params,
        app_id,
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

    logger.info(
        "Deleted stateful contract collection contract with app_id: {}".format(app_id))

    return transaction_response


def update(app_id):
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    application_approval_teal = contract_collection_application()

    application_clear_teal = clear_state_program()

    # compile program to binary
    approval_program_compiled = compile_program(application_approval_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(application_clear_teal)

    logger.info("Updating stateful contract collection smart contract...")

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

    logger.info(
        "Updated stateful contract collection contract with app_id: {}".format(app_id))

    return transaction_response
