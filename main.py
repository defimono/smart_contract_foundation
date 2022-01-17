from config.logger import logger

if __name__ == "__main__":
    """
    Work in progress in foundational repo
    """
    try:
        logger.info("hello")

    except Exception as error:
        logger.error('{}'.format(error))
