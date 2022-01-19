from config.load_app_config import app_config
from config.logger import logger
from modules.deployments.reserve import application, contract_account

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        reserve_app_id = app_config.get("reserve_app_id")

        # generate_keypair()

        # Create/update the deployed stateful reserve app
        # update_result = application.create()
        update_result = application.update(reserve_app_id)

        # Create the stateless contract account to hold funds
        created_contract_account = contract_account.create()

        # Extract address from response dict
        contract_account_address = created_contract_account.get("escrow_address")
        contract_account_program = created_contract_account.get("escrow_program")

        # Update the original stateful app with the smart contract address
        # As part of this, opt into the usdc asset
        update_contract_account_result = application.update_contract_account(
            reserve_app_id,
            contract_account_address,
            contract_account_program)

    except Exception as error:
        logger.error('{}'.format(error))
