# HelloEthereum
Sample IPFS and Smart Contract manipulations in Django

Ethereum:
sample contains access to both Ropsten and Ganache, just fill in the url of the respective server in HelloEthereum/view.py
(This sample used a smart contract in my gist: https://gist.github.com/alick888/2eb6e9024cbedc8de9ee63ecbc8f31b6)
It is assumed that the smart contract is created in the respective server (Ropsten or Ganache) and fill in the contract address, public_key and private_key in HelloEthereum/view.py
Infura is required to access the smart contract using web3

Infura:
Create an account in Infura
Create a project in Infura and copy the url from settings of the project for Ropsten

IPFS:
Sample using ipfs.infura.io for IPFS API
