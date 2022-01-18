import os

from algosdk.future import transaction
from dotenv import load_dotenv

from config.algod_client import algod_client

load_dotenv()


def test_reserve_stake_algorands():
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

    pass

# Test random asa deposit
# Test usd deposit
