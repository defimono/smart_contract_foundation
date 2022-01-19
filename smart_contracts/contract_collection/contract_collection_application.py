from pyteal import *


def contract_collection_application():
    """
        This option collection is intended to serve as a pseudo database for a user, to avoid backend database
        systems in traditional system architecture. This might still need to be approached again to enable further
        enhancements but for now this is sufficient.

        This allows a use to have up to 16 contracts open at any one time per wallet.
        It will record what they have open, and what they close in an atomic operation when called with another app.
        This will ensure it doesn't get out of sync with the real user state.
    """
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()

    # Make sure no rekey of smart contract
    no_rekey_address = Txn.rekey_to() == Global.zero_address()

    # Make sure no one forces a fee of like 5000 algos to blow account
    acceptable_fee = Txn.fee() <= Int(5000)

    on_init = Seq([
        # Allow everyone to opt into the application without restriction
        Return(Int(1))
    ])

    contract_id = GeneratedID(0)
    i = ScratchVar(TealType.uint64)

    add_contract = Seq([
        i.store(Int(0)),
        While(i.load() < Int(16)).Do(Seq([
            If(App.localGet(Txn.sender(), Itob(i.load())) == Int(0)).Then(
                Seq([
                    App.localPut(Txn.sender(), Itob(i.load()), contract_id),
                    Return(Int(1))
                ])
            ),
            i.store(i.load() + Int(1))
        ])),

        Return(Int(0))
    ])

    remove_contract = Seq([
        i.store(Int(0)),
        # 16 is max local-state items possible
        While(i.load() < Int(16)).Do(Seq([
            If(App.localGet(Txn.sender(), Itob(i.load())) == contract_id).Then(
                Seq([
                    App.localDel(Txn.sender(), Itob(i.load())),
                    Return(Int(1))
                ])
            ),
            i.store(i.load() + Int(1))
        ])),

        Return(Int(0))
    ])

    handle_noop = Cond(
        [And(
            no_rekey_address,
            no_close_out_address,
            acceptable_fee,
            Txn.application_args[0] == Bytes("append")
        ), add_contract],
        [And(
            no_rekey_address,
            no_close_out_address,
            acceptable_fee,
            Txn.application_args[0] == Bytes("remove")
        ), remove_contract],
    )

    handle_optin = Seq([
        Return(Int(1))
    ])

    handle_closeout = Seq([
        Assert(no_rekey_address),
        Assert(no_close_out_address),
        Assert(acceptable_fee),

        Return(Int(1))
    ])

    handle_update = Seq([
        Assert(no_rekey_address),
        Assert(no_close_out_address),
        Assert(acceptable_fee),

        Return(Int(1))
    ])

    handle_delete = Seq([
        Assert(no_rekey_address),
        Assert(no_close_out_address),
        Assert(acceptable_fee),

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
