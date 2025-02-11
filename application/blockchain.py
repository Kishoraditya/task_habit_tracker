import os
import json
from web3 import Web3

# Connect to a blockchain node (for testing, use Ganache or Infura)
BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://127.0.0.1:7545")  # Default Ganache
web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
if not web3.isConnected():
    raise Exception("Blockchain node not connected.")

# Load contract ABI
with open("contracts/TaskManagerABI.json") as f:
    contract_abi = json.load(f)

# Set contract address from environment variable or directly here
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0xYourContractAddressHere")
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def create_list_on_chain(owner_private_key: str, name: str, description: str):
    account = web3.eth.account.privateKeyToAccount(owner_private_key)
    nonce = web3.eth.getTransactionCount(account.address)
    txn = contract.functions.createList(name, description).buildTransaction({
        'chainId': web3.eth.chain_id,
        'gas': 3000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
    })
    signed_txn = account.signTransaction(txn)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

def add_task_on_chain(owner_private_key: str, list_id: int, title: str, description: str):
    account = web3.eth.account.privateKeyToAccount(owner_private_key)
    nonce = web3.eth.getTransactionCount(account.address)
    txn = contract.functions.addTask(list_id, title, description).buildTransaction({
        'chainId': web3.eth.chain_id,
        'gas': 3000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
    })
    signed_txn = account.signTransaction(txn)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt
