import json

from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation, AssetTransferTxn

from config.algod_client import algod_client
from config.load_app_config import app_config
from config.logger import logger
from modules.helpers.compile import compile_smart_signature
from smart_contracts.reserve.contract_account import contract_account


#   Utility function u
#   sed to print asset holding for account and assetid
def print_asset_holding(account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are
    # looking for
    account_info = algod_client.account_info(account)
    for scrutinized_asset in account_info['assets']:
        if scrutinized_asset['asset-id'] == assetid:
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def create():
    logger.info("Creating reserve contract account...")
    reserve_app_id = app_config.get("reserve_app_id")
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")
    usdc_asset_id = 10458941

    stateless_program_teal = contract_account(int(reserve_app_id))

    initial_escrow_result, initial_escrow_address = compile_smart_signature(
        stateless_program_teal)
    # Populate and deploy.py the smart sig on the testnet
    # 300,000 = .3 algos
    initial_amount = 1000000

    params = algod_client.suggested_params()

    unsigned_txn = transaction.PaymentTxn(
        admin_address, params, initial_escrow_address, initial_amount)

    signed = unsigned_txn.sign(admin_private_key)

    transaction_id = algod_client.send_transaction(signed)

    payment_transaction = wait_for_confirmation(
        algod_client, transaction_id, 10)

    logger.info("Contract account created")

    response = {
        "escrow_program": initial_escrow_result,
        "escrow_address": initial_escrow_address,
        "payment_transaction": payment_transaction
    }

    logger.info(response)

    # We must ensure the contract account is opted into the USDC asset before
    # it can receive it
    account_info = algod_client.account_info(initial_escrow_address)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if scrutinized_asset['asset-id'] == usdc_asset_id:
            holding = True
            break

    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=admin_address,
            sp=params,
            receiver=initial_escrow_address,
            amt=0,
            index=usdc_asset_id)
        stxn = txn.sign(admin_private_key)
        txid = algod_client.send_transaction(stxn)

        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(initial_escrow_address, usdc_asset_id)

    return response
