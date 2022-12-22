#!/usr/bin/python3
from brownie import SimpleCollectible, accounts, network, config, ZombieOwnership
from scripts.helpful_scripts import get_publish_source


def main():
    dev = accounts.from_mnemonic(config["wallets"]["from_mnemonic"])
    print(network.show_active())
    ZombieOwnership.deploy({"from": dev}, publish_source=get_publish_source())