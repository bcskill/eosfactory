

import os

import eosfactory.core.utils as utils
from eosfactory.eosf import *

import pathlib
from termcolor import colored

import eosfactory.core.config as config

contract_dir = None

while True:
    map = config.config_map()
    EOSIO_CONTRACTS = "EOSIO_CONTRACTS"
    prompt_color = "green"
    error_path_color = "red"
    eosio_contracts_src_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "contracts/eosio.contracts")
    eosio_build_contracts_src_sub_dir = "build/contracts"
    eosio_bios_contracts_src_sub_dir = os.path.join(eosio_build_contracts_src_sub_dir, "eosio.bios")

    def ok(con_dir):
        is_ok = con_dir and os.path.exists(
                    os.path.join(con_dir, eosio_bios_contracts_src_sub_dir))
        if is_ok:
            global contract_dir
            contract_dir = os.path.join(con_dir, eosio_build_contracts_src_sub_dir)
        return is_ok

    if ok(eosio_contracts_src_dir):
        break

    if EOSIO_CONTRACTS in map:
        eosio_contracts_src_dir = map[EOSIO_CONTRACTS]
        if ok(eosio_contracts_src_dir):
            break

    eosio_contracts_src_dir = input(colored(utils.heredoc('''
        Where is 'eosio.contracts` repository located on your machine?
        Input an existing directory path:
        ''') + "\n", prompt_color))

    eosio_contracts_src_dir.replace("~", str(pathlib.Path.home()))

    if ok(eosio_contracts_src_dir):
        map[EOSIO_CONTRACTS] = eosio_contracts_src_dir
        config.write_config_map(map)
        print()
        break

    print("\n" + utils.heredoc('''
    The path you entered:
    {}
    doesn't seem to be correct!
    directory --
    {} 
    -- does not exist.
    ''').format(
        colored(eosio_contracts_src_dir, error_path_color),
        colored(os.path.join(eosio_contracts_src_dir, eosio_bios), error_path_color)
        ) + "\n")

INFO(contract_dir)


reset()
COMMENT('''Create important system accounts''')
eosio = new_master_account()
eosio_token = new_account(eosio, "eosio.token", is_sys_create=False)
eosio_ram = new_account(eosio, "eosio.ram", is_sys_create=False)
eosio_ramfee = new_account(eosio, "eosio.ramfee", is_sys_create=False)
eosio_stake = new_account(eosio, "eosio.stake", is_sys_create=False)
eosio_bpay = new_account(eosio, "eosio.bpay", is_sys_create=False)
eosio_vpay = new_account(eosio, "eosio.vpay", is_sys_create=False)
eosio_msig = new_account(eosio, "eosio.msig", is_sys_create=False)
eosio_names = new_account(eosio, "eosio.names", is_sys_create=False)
eosio_saving = new_account(eosio, "eosio.saving", is_sys_create=False)
eosio_rex = new_account(eosio, "eosio.rex", is_sys_create=False)

COMMENT('''Install the eosio.token contract''')
contract = "eosio.token"
contract_object = Contract(
    eosio_token,
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"
    )
contract_object.deploy()

COMMENT('''Set the eosio.msig contract''')

contract = "eosio.msig"
contract_object = Contract(
    eosio_msig,
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"
    )
contract_object.deploy()

COMMENT('''Create and allocate the EOS currency''')

eosio_token.push_action(
    "create",
    [eosio, "10000000000.0000 EOS"],
    (eosio_token, Permission.ACTIVE))

eosio_token.push_action(
    "issue",
    [eosio, "1000000000.0000 EOS", "memo"],
    (eosio, Permission.ACTIVE))

COMMENT('''Set the eosio.system contract''')

contract = "eosio.system"
contract_object = Contract(
    eosio,
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"
    )

contract_object.deploy()

COMMENT('''Init the eosio.system contract''')
cleos.PushAction(
    eosio,
    "init",
    '[0, "4,EOS"]',
    (eosio, Permission.ACTIVE))

