import json
import time

from web3 import Web3
from eth_account import Account

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

# ipfs
import ipfshttpclient

#Ropsten Account
local_account=None

#connecting to Infura
url = 'https://ropsten.infura.io/v3/0178c83df5254ba8a084515d97a7fc9e'

#connecting to Ganache
# url = 'HTTP://127.0.0.1:7545'

#Initiating Web3
web3 = Web3(Web3.HTTPProvider(url))

#Contract's Address and ABI
# Ropsten
contract_address = "0x061323998Ebcdd42cf1330f7409B62cF38cD733D"
# Ganache
# contract_address = "0x4c5e02dad6e82D572d9d3049E77E6e5C8bB3B201"
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
account_address = None

def import_key(request):
    global local_account, account_address
    local_account = Account.from_key(request.GET.get('private_key'))
    account_address = web3.toChecksumAddress(local_account.address)

    return HttpResponse("Account import successful")

def buy_alicoins(request):
    nonce = web3.eth.getTransactionCount(account_address)
    investor_str = request.GET.get('investor', local_account.address)
    investor = web3.toChecksumAddress(investor_str)
    usd_invested = int(request.GET.get('usd_invested', '1'))
    tx = contract.functions.buy_alicoins(investor,usd_invested).buildTransaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
        'chainId': 1337
    })
    # tx = buy_alicoins_funct(investor,usd_invested).buildTransaction({
    #     'gas': 2000000,
    #     'gasPrice': web3.toWei('40', 'gwei'),
    #     'nonce': nonce,
    #     'chainId': 1337
    # })

    signed_tx = web3.eth.account.signTransaction(tx,local_account.key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
        count += 1

    return HttpResponse("Alicoin Purchase Successful! %s" % tx_receipt)

def ipfs_test (request):
    client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
    hash = client.add('test2.txt')['Hash']
    # return HttpResponse(client.cat(res['Hash']))
    # to retrieve content:https://gateway.ipfs.io/ipfs/QmXgTePLYuU9yUaZedxgxJV2Xh5hangCL8nqAZyWihUpMJ
    return HttpResponse(hash)