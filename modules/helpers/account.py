from algosdk.account import generate_account

from config.logger import logger


def generate_keypair():
    """
    Generate and supply various information about your algorand account. Will give you the address of the wallet,
    hashed private key along with the mnemonic printed to the console.
    """
    private_key, address = generate_account()
    logger.info("My address: {}".format(address))
    logger.info("My private key: {}".format(private_key))

    return {
        "address": address,
        "private_key": private_key
    }
