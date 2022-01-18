from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation

from config.algod_client import algod_client
from config.load_app_config import app_config
from config.logger import logger
from modules.helpers.compile import compile_smart_signature
from smart_contracts.reserve.contract_account import contract_account


def create():
    logger.info("Creating reserve contract account...")
    reserve_app_id = app_config.get("reserve_app_id")
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    stateless_program_teal = contract_account(int(reserve_app_id))

    initial_escrow_result, initial_escrow_address = compile_smart_signature(stateless_program_teal)
    # Populate and deploy.py the smart sig on the testnet
    # 300,000 = .3 algos
    initial_amount = 1000000

    params = algod_client.suggested_params()

    unsigned_txn = transaction.PaymentTxn(admin_address, params, initial_escrow_address, initial_amount)

    signed = unsigned_txn.sign(admin_private_key)

    transaction_id = algod_client.send_transaction(signed)

    payment_transaction = wait_for_confirmation(algod_client, transaction_id, 10)

    logger.info("Contract account created")

    response = {
        "escrow_program": initial_escrow_result,
        "escrow_address": initial_escrow_address,
        "payment_transaction": payment_transaction
    }

    logger.info(response)

    return response
