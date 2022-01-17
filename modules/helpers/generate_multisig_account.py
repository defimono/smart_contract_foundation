from algosdk.future.transaction import Multisig

from config.logger import logger


def generate_multisig_account(admin_address, user_address):
    # 1 is the version, 2 is the minimum requirement and array is the addresses. This means 2 of 2 required and hash
    # will vary depending on the order of the addresses, hence the lib.
    logger.debug("Generate multisig account for {} and {}".format(admin_address, user_address))

    multisig_account = Multisig(1, 2, [admin_address, user_address])

    multisig_address = multisig_account.address()

    logger.debug("Multisig Address: {}".format(multisig_address))

    return multisig_account
