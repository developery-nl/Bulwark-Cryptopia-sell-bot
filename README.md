# Bulwark-Cryptopia-sell-bot
The development repository for the Bulwark to Cryptopia transfer and sell bot

## Purpose

The Bulwark-Cryptopia-sell-bot lets you automatically transfer coins from your Bulwark wallet to Cryptopia. Coins that you e.g. earned with staking or with masternode rewards can now be send and sold at fixed time intervals. When your Cryptopia balance is sufficient, at regular time intervals a sell order will be place. The transfer amount, order amount, time interval, and sell order rate, can be set by the user.

Advantages:
* instead of e.g. doing a large weekly manual deposit to Cryptopia and 'dump' your coins at once, the bot takes care of many small sell orders daily or even hourly. Maybe a positive price impact?
* all is done automatically without the need to logging into Cryptopia, or make transaction in your wallet
* in case you have multisend enabled in your wallet, you can disable the transfer function for the bot and only use the sell functionality
* the bot is able to create the sell order rate relative to the 'live' market conditions

The bot is not developed to re-evaluate trading decisions in case a sell order is not filled after a certain time. It is your responsibility to decide what to do with these orders. By changing the sell order parameters in the config file it is possible to sell at market price in case you want all your orders to be filled as quick as possible.

## Prerequisites

The python bot requires Python 2.7 and:
* should run on the computer where the wallet is located
* a 24/7 open, (manually) unlocked, Bulwark wallet (such as a local pc wallet, or a SHN) with coins, preferably in multiple inputs
* a Cryptopia account, a BWK deposit address, and the API keys of your account

Also, it is needed to enable RPC settings in the bulwark.conf file:

```
rpcuser=userblablaname
rpcpassword=blablasecretrpcpass
rpcport=52541
server=1
```

## Installing

The python bot code depends on some modules, which probably have to be imported.
Apply these steps (for linux you may add 'sudo' before the commands)

```
pip install python-bitcoinrpc
pip install requests
pip install configparser
```

The bot can be started with

```
python cryptopia-trade.py mysettings.ini
```

where 'mysettings.ini' is the filename of a configuration file to be used with user specific settings. 

## Setting up configuration file

Copy the 'tradesettings.ini' file, rename it to e.g. 'mysettings.ini' and fill in the appropriate values. A detailed explanation of the configuration file with the parameters is shown below.  

```
[BWK]
# Specify your rpc credentials to communicate with your Bulwark Wallet
# Should be the same as specified in your bulwark.conf file
# notice: also check you have a line with: server=1 and a line with: rpcport=52541 in your bulwark.conf file
# otherwise python can not connect correctly with your wallet
rpcuser: rpcuserblabla
rpcpassword: rpcpassblabla

# Specify your wallet address from which you will send coins at regular time intervals
bwkaddress_from: bQMSWiV9jr2UszXKsenvfPuLFoFDummy

# Specify your Cryptopia deposit address
bwkaddress_to: bHMSWiV9jr2UszXKsenvfPuLFoF70Dummy

# In case you want to use the bot to transfer coins from wallet to Cryptopia, set to true
# when you want to use the bot only to sell orders at regular intervals, set to false
transfer_mode: true

# Specify the amount (float) to be transferred from your Bulwark wallet address to Cryptopia at <transfer_interval>
# notice: minimum requirement to place a sell order on Cryptopia is coin value of at least 0.005 btc , thus about 5 bwk
transfer_amount: 20.1

# Specify the amount (float) to be used as order size
# notice: in case your Cryptopia balance is not enough no order will be placed. For anonomity a random correction +/-10% is applied on order size
order_amount: 5.1

# Specify the interval time in minutes (integer) to check your balance on Cryptopia and initiate a sell order. 
# A value of 60 means once per hour
# In case sufficient balance is available on Cryptopia, a sell order will be created with size <order_amount>
order_interval : 60

# Specify the interval time in minutes (integer) to make transfers from wallet to Cryptopia. A value of 1440 means once a day
# A value of <transfer_amount> will be subtracted from your smallest available spendable input and then send.
transfer_interval : 720

# Set [wallet_manually_unlocked_mode : true]
# in case you take care to unlock the wallet yourself before starting the python bot.
# Since the python bot makes transactions, the wallet needs to be unlocked, which can be done manually
# using the wallet QT interface or using the bulwark-cli command line
wallet_manually_unlocked_mode : false

# In case [wallet_manually_unlocked_mode : false]
# then the python bot requires that you specify your walletphrase in this config file
# As you will understand, this is a risk if someone has access to your computer !!
walletpassphrase : yourWalletpass

[Cryptopia]
# Specify your public and secret api Cryptopia key
api_key: 87c2c7b2981840818a263dummy2839
api_secret: Nb8/rj+Ik1HfMznfLp4L9VqvRwHwUQ/+dummy

# Specify sell rate calculation parameters. (sell_rate = parameter_highest_bid * highest_bid_smoothed + parameter_lowest_ask*lowest_ask_smoothed + parameter_delt)
# thus values 0.5 and 0.5 means a sell rate around the center of spread
parameter_lowest_ask: 0.5
parameter_highest_bid: 0.5
parameter_delta: 0.0000001

# Specify the lowest price you are willing to sell your coins
# So your order will be placed, but never below the rate specified here
lowest_accepted_sell_rate: 0.0001126
```
## Example running bot
Below a screenshot of the bot running within a linux console. The interval for checking possible sell orders on Cryptopia was at 15 minutes in this example. Since the balance was enough to place an order this order was published at a rate of 0.0001136.

![screenshot bot in console](https://media.discordapp.net/attachments/384778076179136513/471421238623862814/unknown.png)

## Note

This python code was tested and developed on a raspberry pi SHN that is used for staking. So, yes it works on a SHN.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


