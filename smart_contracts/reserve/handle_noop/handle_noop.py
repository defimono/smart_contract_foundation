from pyteal import *

from smart_contracts.libs.generic_guards import generic_guards
from smart_contracts.libs.is_admin import is_admin
from smart_contracts.reserve.handle_noop.functions.expire import expire
from smart_contracts.reserve.handle_noop.functions.insure import insure
from smart_contracts.reserve.handle_noop.functions.stake import stake
from smart_contracts.reserve.handle_noop.functions.unstake import unstake
from smart_contracts.reserve.handle_noop.functions.update_escrow import update_escrow


def handle_noop():
    """
    Stake/Unstake
    This will allow users who have opted-in to have a localstate item set, this counts how much of an asset they
    have staked into the pool, and discount this when they unstake it.
    :return: PyTeal Cond statement supporting various noop function calls
    """
    return Cond(
        [And(
            is_admin(),
            *generic_guards(),
            Txn.application_args[0] == Bytes("update_contract_account")
        ), update_escrow()],
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("stake")
        ), stake()],
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("unstake")
        ), unstake()],
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("insure")
        ), insure()],
        [And(
            *generic_guards(),
            Txn.application_args[0] == Bytes("expire")
        ), expire()],
        [And(
            is_admin()
        ), Return(Int(1))]
    )
