import os

from algosdk import account
from dotenv import load_dotenv

load_dotenv()


def load_app_config():
    """
    Need this, allows safer value loading, defaults, safe panicking, keeps code dry, etc.
    """
    config = dict()

    config["admin_private_key"] = os.environ["ADMIN_PRIVATE_KEY"]
    config["admin_address"] = account.address_from_private_key(
        config["admin_private_key"])

    config["reserve_address"] = os.environ['RESERVE_ADDRESS']
    config["reserve_program"] = os.environ['RESERVE_PROGRAM']

    # Managed globally static app id's from foundation
    config["oracle_app_id"] = int(os.environ['ORACLE_APP_ID'])
    config["reserve_app_id"] = int(os.environ['RESERVE_APP_ID'])

    # Config for algo sdk client blockchain connection
    config["algod_address"] = os.environ['ALGOD_ADDRESS']
    config["algod_token"] = os.environ['ALGOD_KEY']

    return config


app_config = load_app_config()
