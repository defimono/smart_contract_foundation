from config.load_app_config import app_config
from config.logger import logger
from modules.deployments.contract_collection import application as contract_collection_application
from modules.deployments.reserve import application as reserve_application, contract_account

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        # reserve_app_id = app_config.get("reserve_app_id")
        #
        # # generate_keypair()
        #
        # # Create/update the deployed stateful reserve app
        # # reserve_app_id = application.create()
        # update_result = reserve_application.update(reserve_app_id)
        # # delete_result = application.delete(reserve_app_id)
        #
        # # Create the stateless contract account to hold funds
        # created_contract_account = contract_account.create()
        #
        # # Extract address from response dict
        # contract_account_address = created_contract_account.get("escrow_address")
        # contract_account_program = created_contract_account.get("escrow_program")
        #
        # # Update the original stateful app with the smart contract address
        # # As part of this, opt into the usdc asset
        # update_contract_account_result = reserve_application.update_contract_account(
        #     reserve_app_id,
        #     contract_account_address,
        #     contract_account_program)

        contract_collection_app_id = contract_collection_application.create()

    except Exception as error:
        logger.error('{}'.format(error))
