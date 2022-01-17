import requests

from config.logger import logger


def get_asset_price(asset):
    """
    Query public API for ALGO price information. Will query, parse, and return a float representation pegged to USD.
    :return: float representation of price
    """
    url = "https://api.coinbase.com/v2/prices/{}-USD/buy".format(asset)

    raw_response = requests.get(url)

    price_data = raw_response.json()

    real_price = price_data.get('data').get('amount')

    parsed_price = float(real_price)

    logger.info("Got {} price from coinbase: ${}".format(asset, parsed_price))

    return parsed_price
