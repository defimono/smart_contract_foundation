import os

import pytest
from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation
from dotenv import load_dotenv

from config.algod_client import algod_client

load_dotenv()


def test_reserve_stake_algorands_fails():
    with pytest.raises(Exception):
        # Test algorand deposit
        test_address = os.environ["TEST_ADDRESS"]
        test_private_key = os.environ["TEST_PRIVATE_KEY"]
        reserve_address = os.environ["RESERVE_ADDRESS"]
        reserve_program = os.environ["RESERVE_PROGRAM"]
        reserve_app_id = int(os.environ["RESERVE_APP_ID"])

        # Build stake transaction
        # Involves a 2 transaction group, first is the noop the second is the stake

        params = algod_client.suggested_params()

        app_args = ["stake"]

        amount = 100000

        application_transaction = transaction.ApplicationNoOpTxn(
            test_address,
            params,
            reserve_app_id,
            app_args
        )

        payment_transaction = transaction.PaymentTxn(
            test_address,
            params,
            reserve_address,
            amount
        )

        # Build atomic group
        group_id = transaction.calculate_group_id([
            application_transaction,
            payment_transaction
        ])

        # Group transactions and assign their id
        application_transaction.group = group_id
        payment_transaction.group = group_id

        # Sign transaction group
        signed_application_transaction = application_transaction.sign(test_private_key)
        signed_payment_transaction = payment_transaction.sign(test_private_key)

        transaction_group = [
            signed_application_transaction,
            signed_payment_transaction
        ]

        tx_id = application_transaction.get_txid()

        # send transaction
        algod_client.send_transactions(transaction_group)

        # await confirmation
        wait_for_confirmation(algod_client, tx_id, 30)


def test_reserve_stake_algorands_usdc():
    # Test algorand deposit
    test_address = os.environ["TEST_ADDRESS"]
    test_private_key = os.environ["TEST_PRIVATE_KEY"]
    reserve_address = os.environ["RESERVE_ADDRESS"]
    reserve_app_id = int(os.environ["RESERVE_APP_ID"])
    usdc_asset_id = 10458941

    params = algod_client.suggested_params()

    app_args = ["stake"]

    amount = 100000

    application_transaction = transaction.ApplicationNoOpTxn(
        test_address,
        params,
        reserve_app_id,
        app_args
    )

    payment_transaction = transaction.AssetTransferTxn(
        test_address,
        params,
        reserve_address,
        amount,
        usdc_asset_id
    )

    # Build atomic group
    group_id = transaction.calculate_group_id([
        application_transaction,
        payment_transaction
    ])

    # Group transactions and assign their id
    application_transaction.group = group_id
    payment_transaction.group = group_id

    # Sign transaction group
    signed_application_transaction = application_transaction.sign(test_private_key)
    signed_payment_transaction = payment_transaction.sign(test_private_key)

    transaction_group = [
        signed_application_transaction,
        signed_payment_transaction
    ]

    tx_id = application_transaction.get_txid()

    # send transaction
    algod_client.send_transactions(transaction_group)

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)
