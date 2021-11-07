from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network
import time


def deploy_lottery():
    acc = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed"),
        get_contract("vrf_coordinator").address,
        get_contract("link").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": acc},
        publish_source=config["networks"][network.show_active()].get("verify", False),

    )
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    start_tx = lottery.startLottery({"from": account})
    start_tx.wait(1)
    print("The Lottery has started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntryFee() + 1000000
    print(value)
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("Entered lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    end_tx = lottery.endLottery({"from": account, "gas_limit":1000000 })
    end_tx.wait(1)
    time.sleep(30)
    print(f"{lottery.recentWinner()} is the new winner")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
