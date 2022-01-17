from pyteal import *


def expire():
    risk_state = App.globalGet(Bytes("total_risk"))

    # Remote asset price is 2 point fixed point, meaning it is already 10**2
    # Gtxn[2] == put
    # asset_price = App.globalGetEx(GeneratedID(2), Bytes("asset_price"))
    # amount_insured = App.globalGetEx(GeneratedID(2), Bytes("amount_insured"))
    # new_risk = Mul(Div(amount_insured, Int(100)), asset_price)

    # Risk for now as we only can support algos is 100% reimbursement of lost funds. This will change however with the
    # intro usdc peg
    # raw_amount_insured = App.globalGetEx(GeneratedID(1), Bytes("amount_insured"))
    # amount_insured = Seq([
    #     raw_amount_insured,
    #     raw_amount_insured.value()
    # ])

    return Seq([
        # When we insure an item against the central reserve, we need to record MAX risk for payout
        # total risk = total risk + max current risk is amount insured * price per asset
        # App.globalPut(Bytes("total_risk"), risk_state - amount_insured),

        Return(Int(1))
    ])
