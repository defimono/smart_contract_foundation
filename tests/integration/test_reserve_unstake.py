import base64
import os

import pytest
from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation, LogicSig, LogicSigTransaction

from config.algod_client import algod_client


def test_reserve_unstake_minimum_usdc():
    test_address = os.environ["TEST_ADDRESS"]
    test_private_key = os.environ["TEST_PRIVATE_KEY"]
    reserve_address = os.environ["RESERVE_ADDRESS"]
    reserve_program = os.environ["RESERVE_PROGRAM"]
    reserve_app_id = int(os.environ["RESERVE_APP_ID"])
    usdc_asset_id = 10458941

    params = algod_client.suggested_params()

    app_args = ["unstake"]

    amount = 10000

    application_transaction = transaction.ApplicationNoOpTxn(
        test_address,
        params,
        reserve_app_id,
        app_args
    )

    asset_transfer_transaction = transaction.AssetTransferTxn(
        reserve_address,
        params,
        test_address,
        amount,
        usdc_asset_id
    )

    # Build atomic group
    group_id = transaction.calculate_group_id([
        application_transaction,
        asset_transfer_transaction
    ])

    # Group transactions and assign their id
    application_transaction.group = group_id
    asset_transfer_transaction.group = group_id

    # Sign transaction group
    signed_application_transaction = application_transaction.sign(
        test_private_key)

    # Create logic sig
    encoded_program = reserve_program.encode()
    program = base64.decodebytes(encoded_program)
    logic_signature = LogicSig(program)
    logic_signed_asset_transfer_transaction = LogicSigTransaction(
        asset_transfer_transaction, logic_signature)
    transaction_group = [
        signed_application_transaction,
        logic_signed_asset_transfer_transaction
    ]

    tx_id = application_transaction.get_txid()

    # send transaction
    algod_client.send_transactions(transaction_group)

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)


def test_reserve_unstake_too_much_usdc_fails():
    with pytest.raises(Exception):
        test_address = os.environ["TEST_ADDRESS"]
        test_private_key = os.environ["TEST_PRIVATE_KEY"]
        reserve_address = os.environ["RESERVE_ADDRESS"]
        reserve_program = os.environ["RESERVE_PROGRAM"]
        reserve_app_id = int(os.environ["RESERVE_APP_ID"])
        usdc_asset_id = 10458941

        params = algod_client.suggested_params()

        app_args = ["unstake"]

        amount = 1000000

        application_transaction = transaction.ApplicationNoOpTxn(
            test_address,
            params,
            reserve_app_id,
            app_args
        )

        asset_transfer_transaction = transaction.AssetTransferTxn(
            reserve_address,
            params,
            test_address,
            amount,
            usdc_asset_id
        )

        # Build atomic group
        group_id = transaction.calculate_group_id([
            application_transaction,
            asset_transfer_transaction
        ])

        # Group transactions and assign their id
        application_transaction.group = group_id
        asset_transfer_transaction.group = group_id

        # Sign transaction group
        signed_application_transaction = application_transaction.sign(
            test_private_key)

        # Create logic sig
        encoded_program = reserve_program.encode()
        program = base64.decodebytes(encoded_program)
        logic_signature = LogicSig(program)
        logic_signed_asset_transfer_transaction = LogicSigTransaction(
            asset_transfer_transaction, logic_signature)
        transaction_group = [
            signed_application_transaction,
            logic_signed_asset_transfer_transaction
        ]

        tx_id = application_transaction.get_txid()

        # send transaction
        algod_client.send_transactions(transaction_group)

        # await confirmation
        wait_for_confirmation(algod_client, tx_id, 30)
