from config.load_app_config import app_config
from config.logger import logger
from modules.deployments.reserve import application

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        reserve_app_id = app_config.get("reserve_app_id")

        update_result = application.update(reserve_app_id)
        # created_contract_account = contract_account.create()

    except Exception as error:
        logger.error('{}'.format(error))
