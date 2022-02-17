from config.load_app_config import app_config
from config.logger import logger
from modules.deployments.reserve import application as reserve_application, contract_account, application

if __name__ == "__main__":
    """
    Work in progress in foundational repo. This script is intended to be called via CI/CD automation and local dev
    and is how we use the ci pipeline to deploy and update existing applications
    """
    try:
        # reserve_app_id = app_config.get("reserve_app_id")
        # contract_collection_app_id = app_config.get(
        #     "contract_collection_app_id")
        # 
        # update_result = reserve_application.update(reserve_app_id)
        # delete_result = application.delete(reserve_app_id)
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
        # contract_collection_application.create()
        # contract_collection_application.update(contract_collection_app_id)

        pass

    except Exception as error:
        logger.error('{}'.format(error))
