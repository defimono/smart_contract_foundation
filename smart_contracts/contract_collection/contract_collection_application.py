from pyteal import *


def contract_collection_application():
    # Generated ID for the to be created put option, the 2 is the txn index
    option_contract_id = GeneratedID(2)

    i = ScratchVar(TealType.uint64)

    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()

    # Make sure no rekey of smart contract
    no_rekey_address = Txn.rekey_to() == Global.zero_address()

    # Make sure no one forces a fee of like 100000 algos to blow account
    acceptable_fee = Txn.fee() <= Int(10000)

    add_contract = Seq([
        i.store(Int(0)),
        While(i.load() < Int(16)).Do(Seq([
            If(App.localGet(Txn.sender(), Itob(i.load())) == Int(0)).Then(
                Seq([
                    App.localPut(
                        Txn.sender(), Itob(
                            i.load()), option_contract_id),
                    Return(Int(1))
                    # Break()
                ])
            ),
            i.store(i.load() + Int(1))
        ])),

        Return(Int(0))
    ])

    remove_contract = Seq([
        i.store(Int(0)),
        While(i.load() < Int(16)).Do(Seq([
            If(App.localGet(Txn.sender(), Itob(i.load())) == option_contract_id).Then(
                Seq([
                    App.localDel(Txn.sender(), Itob(i.load())),
                    Return(Int(1))
                ])
            ),
            i.store(i.load() + Int(1))
        ])),

        Return(Int(0))
    ])

    on_init = Seq([
        Return(Int(1))
    ])

    handle_noop = Cond(
        [And(
            no_rekey_address,
            no_close_out_address,
            acceptable_fee,
            Txn.application_args[0] == Bytes("add_contract")
        ), add_contract],
        [And(
            no_rekey_address,
            no_close_out_address,
            acceptable_fee,
            Txn.application_args[0] == Bytes("remove_contract")
        ), remove_contract],
    )

    handle_optin = Seq([
        Return(Int(1))
    ])

    handle_closeout = Seq([
        Return(Int(1))
    ])

    handle_update = Seq([
        Return(Int(1))
    ])

    handle_delete = Seq([
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_init],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete]
    )

    return compileTeal(program, Mode.Application, version=5)
