from pyteal import *

from smart_contracts.libs.generic_guards import generic_guards
from smart_contracts.reserve.noops.expire import expire
from smart_contracts.reserve.noops.insure import insure
from smart_contracts.reserve.noops.stake import stake
from smart_contracts.reserve.noops.unstake import unstake
from smart_contracts.reserve.noops.update_contract_account import update_contract_account


def reserve_application():
    """
    The reserve is the heart of the application
    """
    is_admin = Txn.sender() == App.globalGet(Bytes("admin"))

    handle_init = Seq([
        # On init, lock the contract down to the admin only being able to interact with it, and other global states
        App.globalPut(Bytes("admin"), Txn.sender()),
        App.globalPut(Bytes("total_staked"), Int(0)),
        App.globalPut(Bytes("total_risk"), Int(0)),
        App.globalPut(Bytes("contract_account"), Global.zero_address()),

        Return(Int(1))
    ])

    handle_optin = Seq([
        # Allow anyone to opt into the contract, once opted set the local state staked amount.
        App.localPut(Txn.sender(), Bytes("staked"), Int(0)),

        Return(Int(1))
    ])

    handle_noop = Cond(
        [And(
            is_admin,
            *generic_guards(),
            Txn.application_args[0] == Bytes("update_contract_account")
        ), update_contract_account()],
        [And(
            *generic_guards(),
            Global.group_size() == Int(2),
            Txn.application_args[0] == Bytes("stake")
        ), stake()],
        [And(
            *generic_guards(),
            Global.group_size() == Int(2),
            Txn.application_args[0] == Bytes("unstake")
        ), unstake()],
        # TODO, we need to refine the logic here for insure/expire
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("insure")
        ), insure()],
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("expire")
        ), expire()],
        [And(
            is_admin
        ), Return(Int(1))]
    )

    handle_closeout = Seq([
        Return(Int(0))
    ])

    handle_update = Seq([
        Assert(is_admin),
        Return(Int(1))
    ])

    handle_delete = Seq([
        Assert(is_admin),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), handle_init],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete]
    )

    return compileTeal(program, Mode.Application, version=5)
