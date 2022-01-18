from algosdk import mnemonic

from config.load_app_config import app_config
from config.logger import logger
from modules.deployments.reserve import application, contract_account

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        reserve_app_id = app_config.get("reserve_app_id")
        key = mnemonic.from_private_key(
            "ZlHHOREN1BtC8YqLPcmKEcM3HDDopM9+N12PxyUrh+MUH6UkVYXCUIr7HaqAiVnXzcLo7B3oH7LWZBLs+dmZmg==")
        logger.info(key)

        # Create/update the deployed stateful reserve app
        update_result = application.update(reserve_app_id)

        # Create the stateless contract account to hold funds
        created_contract_account = contract_account.create()

        # Extract address from response dict
        contract_account_address = created_contract_account.get("escrow_address")

        # Update the original stateful app with the smart contract address
        update_contract_account_result = application.update_contract_account(reserve_app_id, contract_account_address)

    except Exception as error:
        logger.error('{}'.format(error))
