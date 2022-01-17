from pyteal import *

from modules.contracts.foundation.reserve.handle_init.handle_init import handle_init
from modules.contracts.foundation.reserve.handle_noop.handle_noop import handle_noop
from modules.contracts.shared.security_guards.is_admin import is_admin


def reserve():
    """
    Requirements
        Allow anyone to send to the account
            - Done by default as apps have a wallet address anyone can send to
        Allow admin account to move funds in and out of account, and create contracts external to this one.
        Allow anyone to withdraw only their amount, anytime. Won't get back the same exact algo blocks, but amount\

    This is potentially vulnerable to a run on the bank, but only at the beginning until we accrue enough funds
    to build the foundation. Reserve will be an external account that will be the size so even in the event
    of a run on the bank, users can get back 100% funds, even if value is locked in ongoing contracts.

    The initial setup for this Application (stateful smart contract, no one was kind enough to say it's both to me)

    1. Deploy the application and gets its’ application ID
    2. Hardcode the application ID into the escrow stateless smart contract and compile it to get the escrow address
    3. Store the escrow address in the application global state
    """
    handle_optin = Seq([
        App.localPut(Txn.sender(), Bytes("Deposited"), Int(0)),

        Return(Int(1))
    ])

    handle_closeout = Seq([
        Return(Int(0))
    ])

    handle_update = Seq([
        Assert(is_admin()),
        Return(Int(1))
    ])

    handle_delete = Seq([
        Assert(is_admin()),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), handle_init()],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop()],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete]
    )

    return compileTeal(program, Mode.Application, version=5)
