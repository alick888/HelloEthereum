import json
import time

from web3 import Web3

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

def print(request):
    return render(request, 'index.html')

#Ropsten Account
public_key="0xce193b95348b3F53E2a346FBa46b9de7A102A29d"
private_key="2b5bff1514cd738d3a772ec03f51f30d555e21f8bec9e2b0eb59649b21bcb78d"

#connecting to Infura
# url = 'https://ropsten.infura.io/v3/0178c83df5254ba8a084515d97a7fc9e'

#connecting to Ganache
url = 'HTTP://127.0.0.1:7545'

#Initiating Web3
web3 = Web3(Web3.HTTPProvider(url))

#Contract's Address and ABI
# Ropsten
# contract_address = "0xfB73F1ca027c48aB468D516524d6c2ECC43546C7"
# Ganache
contract_address = "0xf582B1b60Be61FE8F500D61d6c39B060d47a4a24"
address = web3.toChecksumAddress(contract_address)
abi = json.loads('''
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			},
			{
				"name": "usd_invested",
				"type": "uint256"
			}
		],
		"name": "buy_alicoins",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			},
			{
				"name": "alicoins_sold",
				"type": "uint256"
			}
		],
		"name": "sell_alicoins",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			}
		],
		"name": "equity_in_alicoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			}
		],
		"name": "equity_in_usd",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "max_alicoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "total_alicoins_bought",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "usd_to_alicoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]''')

#Creating a Contract Instance
contract = web3.eth.contract(address=address,abi=abi)
account_address = web3.toChecksumAddress(public_key)

def buy_alicoins(request):
    nonce = web3.eth.getTransactionCount(account_address)
    investor = account_address
    usd_invested = 10
    # tx = contract.functions.buy_alicoins(investor,usd_invested).buildTransaction({
    #     'gas': 2000000,
    #     'gasPrice': web3.toWei('40', 'gwei'),
    #     'nonce': nonce,
    #     'chainId': 3
    # })
    buy_alicoins_funct = contract.get_function_by_signature('buy_alicoins(address,uint256)')
    tx = buy_alicoins_funct(investor,usd_invested).buildTransaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
        'chainId': 3
    })

    signed_tx = web3.eth.account.signTransaction(tx,private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
        count += 1