from pyteal import *

from modules.contracts.foundation.reserve.handle_noop.functions.expire import expire
from modules.contracts.foundation.reserve.handle_noop.functions.insure import insure
from modules.contracts.foundation.reserve.handle_noop.functions.stake import stake
from modules.contracts.foundation.reserve.handle_noop.functions.unstake import unstake
from modules.contracts.foundation.reserve.handle_noop.functions.update_escrow import update_escrow
from modules.contracts.shared.security_guards.general_guards import general_guards
from modules.contracts.shared.security_guards.is_admin import is_admin


def handle_noop():

    return Cond(
        [And(
            is_admin(),
            *general_guards(),
            Txn.application_args[0] == Bytes("update_escrow")
        ), update_escrow()],
        [And(
            *general_guards(),
            Txn.application_args[0] == Bytes("stake")
        ), stake()],
        [And(
            *general_guards(),
            Txn.application_args[0] == Bytes("unstake")
        ), unstake()],
        [And(
            *general_guards(),
            Txn.application_args[0] == Bytes("insure")
        ), insure()],
        [And(
            *general_guards(),
            Txn.application_args[0] == Bytes("expire")
        ), expire()],
        [And(
            is_admin()
        ), Return(Int(1))]
    )
