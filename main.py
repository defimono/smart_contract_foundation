from config.logger import logger
from modules.deployments.reserve import contract_account

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        contract_account.create()

    except Exception as error:
        logger.error('{}'.format(error))
