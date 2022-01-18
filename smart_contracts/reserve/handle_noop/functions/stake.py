from pyteal import *


def stake():
    staked_state: App = App.localGet(Int(0), Bytes('staked'))
    usdc_asset_id = Int(31566704)

    # get the balance of the sender for asset `Txn.assets[0]`
    # if the account is not opted into that asset, returns 0
    remote_sender_usdc_balance = AssetHolding.balance(Txn.sender(), usdc_asset_id)
    sender_usdc_balance = Seq([
        remote_sender_usdc_balance,
        remote_sender_usdc_balance.value()
    ])

    return Seq([
        App.localPut(Int(0), Bytes("staked"), staked_state + Gtxn[1].amount()),

        Return(Int(1))
    ])
