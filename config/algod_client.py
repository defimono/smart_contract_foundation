import os

from algosdk.v2client import algod


def initialize_algod_client():
    algod_address = os.environ['ALGOD_ADDRESS']
    algod_token = os.environ['ALGOD_KEY']

    headers = {
        "X-API-Key": algod_token,
    }

    return algod.AlgodClient(algod_token, algod_address, headers)


algod_client = initialize_algod_client()
