from pyteal import *

from smart_contracts.libs.is_admin import is_admin
from smart_contracts.reserve.handle_init.handle_init import handle_init
from smart_contracts.reserve.handle_noop.handle_noop import handle_noop


def reserve():
    """
    The reserve is the heart of the application with various functions built-in.
    """
    handle_optin = Seq([
        App.localPut(Txn.sender(), Bytes("staked"), Int(0)),

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
