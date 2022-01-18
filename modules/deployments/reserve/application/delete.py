def delete(app_id):
    admin_address = app_config.get("admin_address")
    admin_private_key = app_config.get("admin_private_key")

    logger.info("Deleting stateful reserve smart contract...")

    # get node suggested parameters
    params = algod_client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(
        admin_address,
        params,
        app_id,
    )

    # sign transaction
    signed_txn = txn.sign(admin_private_key)

    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 30)

    # display results
    transaction_response = algod_client.pending_transaction_info(tx_id)

    logger.info("Deleted stateful reserve contract with app_id: {}".format(app_id))

    return transaction_response
