import pytest
from brownie import network, convert, chain, ZombieFactory, ZombieFeeding, ZombieHelper, ZombieAttack, accounts, ZombieOwnership

import brownie 

# def test_can_create_simple_collectible():
#     if network.show_active() not in ["development"] or "fork" in network.show_active():
#         pytest.skip("Only for local testing")
#     simple_collectible = SimpleCollectible.deploy(
#         {"from": get_account(), "gas_price": chain.base_fee}
#     )
#     simple_collectible.createCollectible(
#         "None", {"from": get_account(), "gas_price": chain.base_fee}
#     )
#     assert simple_collectible.ownerOf(0) == get_account()

@pytest.fixture
def test_create_zombie():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")

    return ZombieOwnership.deploy(
        {"from": accounts[0]}
    )

def test_zombie_factory(test_create_zombie):
 
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    assert (tx.events[0]['zombieId'] == 0 and tx.events[0]['name'] == 'None')

def test_zombie_feeding(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[0]})
    zombieId = tx.events[0]['zombieId']
    test_create_zombie.setKittyContractAddress('0x06012c8cf97BEaD5deAe237070F9587f8E7A266d', {"from": accounts[0]})
    txx = test_create_zombie.feedOnKitty(zombieId, 95, {"from": accounts[0]})
    assert(txx.events[0]['dna'] % 100 == 99)

# def test_zombie_feeding_feedAndMultiply(test_create_zombie):
#     myZombie = test_create_zombie.createRandomZombie("MyZombie", {"from": accounts[0]})
#     targetZombie = test_create_zombie.createRandomZombie("EnemyZombie", {"from": accounts[1]})
#     myZombieId = myZombie.events[0]['zombieId']
#     myZombieDna = myZombie.events[0]['dna']
#     targetZombieDna = targetZombie.events[0]['dna']
#     # with brownie.reverts():
#     tx = test_create_zombie.feedAndMultiply(myZombieId, targetZombieDna, "zombie", {"from": accounts[0]})
#     assert(tx.events[0]['dna'] == (myZombieDna + targetZombieDna) / 2)

def test_zombie_helper_withdraw(test_create_zombie):
    acc0_initial_balance = accounts[0].balance()
    
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    # print(zombieId)
    levelUp_fee = test_create_zombie.levelUpFee.call()
    
    test_create_zombie.levelUp(zombieId, {"from": accounts[1], "value": levelUp_fee})
    test_create_zombie.withdraw({"from": accounts[0]})
    new_balance = acc0_initial_balance + levelUp_fee
    # print(new_balance)

    # tx = test_create_zombie.withdraw()
    assert(accounts[0].balance() == new_balance)

def test_zombie_helper_setLevelUpFee(test_create_zombie):
    new_levelUpFee = 100
    test_create_zombie.setLevelUpFee(new_levelUpFee, {"from": accounts[0]})
    changed_levelUpFee = test_create_zombie.levelUpFee.call()
    assert(new_levelUpFee == changed_levelUpFee)

def test_zombie_helper_levelUp(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    initial_level = test_create_zombie.zombies(0)[2]
    levelUp_fee = test_create_zombie.levelUpFee.call()
    test_create_zombie.levelUp(zombieId, {"from": accounts[1], "value": levelUp_fee})
    new_level = test_create_zombie.zombies(0)[2]
    assert(new_level == initial_level + 1)

def test_zombie_helper_changeName(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    levelUp_fee = test_create_zombie.levelUpFee.call()
    test_create_zombie.levelUp(zombieId, {"from": accounts[1], "value": levelUp_fee})
    test_create_zombie.changeName(zombieId, "MyNewZombieName", {"from" : accounts[1]})
    assert(test_create_zombie.zombies(0)[0] == "MyNewZombieName")

# changed abovelevel to 2, instead of 20
def test_zombie_helper_changeDna(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    levelUp_fee = test_create_zombie.levelUpFee.call()
    test_create_zombie.levelUp(zombieId, {"from": accounts[1], "value": levelUp_fee})
    test_create_zombie.changeDna(zombieId, 6038148195197117, {"from" : accounts[1]})
    assert(test_create_zombie.zombies(0)[1] == 6038148195197117)

def test_zombie_helper_getZombiesByOwner(test_create_zombie):
    initial_zombie_count = test_create_zombie.ownerZombieCount.call(accounts[1])
    test_create_zombie.createRandomZombie("None", {"from": accounts[1]})
    test_create_zombie.getZombiesByOwner(
        accounts[1], {"from": accounts[1]}
    )
    new_zombie_count = test_create_zombie.ownerZombieCount.call(accounts[1])
    assert(initial_zombie_count + 1 == new_zombie_count)

def test_zombie_attack(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("None", {"from": accounts[0]})
    tx2 = test_create_zombie.createRandomZombie("None2", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    targetId = tx2.events[0]['zombieId']
    txx = test_create_zombie.attack(zombieId, targetId, {"from": accounts[0]})
    assert(test_create_zombie.zombies(0)[4] == 1 or test_create_zombie.zombies(1)[4] == 1)

def test_zombie_ownership_balanceof(test_create_zombie):
    test_create_zombie.createRandomZombie("MyZombie", {"from": accounts[0]})
    assert(test_create_zombie.balanceOf(accounts[0]) == 1)

def test_zombie_ownership_ownerOf(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("MyZombie", {"from": accounts[1]})
    zombieId = tx.events[0]['zombieId']
    assert(test_create_zombie.ownerOf(zombieId) == accounts[1])

def test_zombie_ownership_transfer(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("MyZombie", {"from": accounts[0]})
    zombieId = tx.events[0]['zombieId']
    test_create_zombie.transferFrom(accounts[0], accounts[1], zombieId, {"from": accounts[0]})
    assert(test_create_zombie.balanceOf(accounts[0]) == test_create_zombie.balanceOf(accounts[1]) - 1 )

def test_zombie_ownership_approve(test_create_zombie):
    tx = test_create_zombie.createRandomZombie("MyZombie", {"from": accounts[0]})
    zombieId = tx.events[0]['zombieId']
    tx2 = test_create_zombie.approve(accounts[1], zombieId, {"from": accounts[0]})
    assert(tx2.events[0]['_owner'] == accounts[0] and tx2.events[0]['_approved'] == accounts[1] and tx2.events[0]['_tokenId'] == zombieId)

