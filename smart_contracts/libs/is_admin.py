from pyteal import *


def is_admin():
    return Txn.sender() == App.globalGet(Bytes("admin"))
