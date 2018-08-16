from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from urllib2 import Request, urlopen, URLError
from requests.exceptions import ConnectionError
from time import sleep
import configparser  #pip install configparser
import requests
import random
import datetime
import calendar
import time
import json
import sys
import decimal
from cryptopia_api import Api

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

class MyOrderObject(object):

    @property
    def orderid(self):
       return self._orderid

    @property
    def ordertype(self):
       return self._ordertype

    @property
    def rate(self):
       return self._rate

    @property
    def rem_amount(self):
       return self._rem_amount

    def __init__(self, orderid, rate, ordertype, remaining_amount):
       self._orderid = orderid
       self._rate = rate
       self._ordertype = ordertype
       self._rem_amount = remaining_amount


def getmarketorders():
        ##    Returns the open buy and sell orders for the specified trade pair.
        ##    Param: market (Required) (TradePairId or MarketName)
        ##    GET https://www.cryptopia.co.nz/api/GetMarketOrders/100
        ##    GET https://www.cryptopia.co.nz/api/GetMarketOrders/DOT_BTC
        ##    Param: orderCount (optional, default: 100)
        ##    GET https://www.cryptopia.co.nz/api/GetMarketOrders/100/50
        ##    GET https://www.cryptopia.co.nz/api/GetMarketOrders/DOT_BTC/50
        url = 'https://www.cryptopia.co.nz/api/GetMarketOrders/BWK_BTC/100'
        highest_bid_weighted = 0
        lowest_ask_weighted = 0
        try:
            sleep(2)
            result = requests.get(url, headers=headers)

            json_ans = result.content.decode()
            j_obj = json.loads(json_ans)
            #print j_obj
            #print "----buy----"
            if 'Data' in j_obj:
                if 'Buy' in j_obj["Data"]:
                    result = j_obj["Data"]["Buy"]
                    sumvolume=0
                    sumweightedprice=0

                    for eenorder in result:
                        #print eenorder["Price"] , eenorder["Volume"]

                        if sumvolume< min_volume_forweightedprice:
                                sumvolume=sumvolume+eenorder["Volume"]
                                sumweightedprice=sumweightedprice + eenorder["Volume"] * eenorder["Price"]
                    
                    highest_bid_weighted=  sumweightedprice /  sumvolume
                    #print highest_bid_weighted
            #print "----sell----"
            if 'Data' in j_obj:
                if 'Sell' in j_obj["Data"]:
                    result = j_obj["Data"]["Sell"]
                    sumvolume=0
                    sumweightedprice=0

                    for eenorder in result:
                        #print eenorder["Price"] , eenorder["Volume"]

                        if sumvolume< min_volume_forweightedprice:
                                sumvolume=sumvolume+eenorder["Volume"]
                                sumweightedprice=sumweightedprice + eenorder["Volume"] * eenorder["Price"]
                    lowest_ask_weighted=  sumweightedprice /  sumvolume

            return highest_bid_weighted, lowest_ask_weighted 

        except ValueError:
            print 'No good api'
            return 0 , 0
        except ConnectionError as e:
            print 'No good  Got an error code:', e
            return 0  , 0
        except URLError, e:
            print 'No good . Got an error code:', e
            return 0 ,  0
    

def get_balance(coinname):
        bal=0.0
        try:
            result, error = api_wrapper.get_balance(coinname)
            if error is not None:
                #handle error
                print 'ERROR: %s' % error
            else:
                
                #print result
                j_obj = result
                bal = j_obj["Available"]
                print "         | balance available", bal , "( unconfirmed", j_obj["Unconfirmed"],")"
                #print 'Request successfull. Balance in BTC = %f' % balance
        except ValueError:
            print 'No good api'
            return 0.0
        except ConnectionError as e:
            print 'No good  Got an error code:', e
            return 0.0
        except URLError, e:
            print 'No good . Got an error code:', e
            return 0.0
        return bal


def get_openorders():
        ##[  
        ##   {  
        ##      u'OrderId':543587989,
        ##      u'TimeStamp':      u'2018-04-06T21:56:33.3503359      ', u'      TradePairId':5883,
        ##      u'Rate':0.00073188,
        ##      u'Amount':0.9,
        ##      u'Total':0.00065869,
        ##      u'Type':u'Sell',
        ##      u'Remaining':0.9,
        ##      u'Market':u'POLIS/BTC'
        ##   },
        ##   {  
        ##      u'OrderId':543586127,
        ##      u'TimeStamp':      u'2018-04-06T21:55:44.9364209      ', u'      TradePairId':5883,
        ##      u'Rate':0.0005188,
        ##      u'Amount':1.0,
        ##      u'Total':0.0005188,
        ##      u'Type':u'Buy',
        ##      u'Remaining':1.0,
        ##      u'Market':u'POLIS/BTC'
        ##   }
        ##]

        try:
            result, error = api_wrapper.get_openorders('BWK/BTC')
            if error is not None:
                #handle error
                print 'ERROR: %s' % error
            else:
                #ok
                
                if len(result) == 0:
                    print("         | no open orders")
                else:
                    
                    j_obj = result

                    for eenorder in result:
                           #print "         | ", eenorder["OrderId"], eenorder["Type"], eenorder["Rate"], eenorder["Remaining"], eenorder["TimeStamp"]
                           ordertimestamp = datetime.datetime.strptime( eenorder["TimeStamp"][:-5], "%Y-%m-%dT%H:%M:%S.%f" )
                           nowtimestamp = datetime.datetime.utcnow()
                           #print  nowtimestamp , ordertimestamp
                           c=nowtimestamp - ordertimestamp
                           diftimeobj = divmod(c.days * 86400 + c.seconds, 60)  #(minutes, seconds)

                           if eenorder["Type"]=="Buy" and not(eenorder["OrderId"] in buy_orders_dict):
                                   #print "         | new order buy entry"
                                   orderobject = MyOrderObject(eenorder["OrderId"], eenorder["Rate"], eenorder["Type"], eenorder["Remaining"])
                                   #buy_orders_dict[ eenorder["OrderId"] ] = orderobject

                           if eenorder["Type"]=="Sell" and not(eenorder["OrderId"] in sell_orders_dict):
                                   #print "         | new order sell entry"
                                   orderobject = MyOrderObject(eenorder["OrderId"], eenorder["Rate"], eenorder["Type"], eenorder["Remaining"])
                                   #sell_orders_dict[ eenorder["OrderId"] ] = orderobject

                           if eenorder["Type"]=="Sell" and diftimeobj[0]>order_cancel_interval:
                                print "         | orderId",eenorder["OrderId"]," is",  diftimeobj[0], "minutes old and will be cancelled (setting=",order_cancel_interval,")"
                                cancel_trade(eenorder["OrderId"])
        except ValueError:
            print 'No good api'
        except ConnectionError as e:
            print 'No good  Got an error code:', e
        except URLError, e:
            print 'No good . Got an error code:', e


def submit_trade(rate, ordersize):
        ##Submits a new trade order
        ##URI: https://www.cryptopia.co.nz/api/SubmitTrade
        ## 
        ##Input:
        ##Market: The market symbol of the trade e.g. 'DOT/BTC' (not required if 'TradePairId' supplied)
        ##TradePairId: The Cryptopia tradepair identifier of trade e.g. '100' (not required if 'Market' supplied)
        ##Type: the type of trade e.g. 'Buy' or 'Sell'
        ##Rate: the rate or price to pay for the coins e.g. 0.00000034
        ##Amount: the amount of coins to buy e.g. 123.00000000
        rate_str=str(rate)
        amount_str=str(ordersize)
        try:
            sleep(1)
            result, error = api_wrapper.submit_trade('BWK/BTC','Sell',rate_str,amount_str)
            if error is not None:
                #handle error
                print 'ERROR: %s' % error
            else:
                #ok
                print "         | sell order created ",result, " size",ordersize
        except ValueError:
            print 'No good api'
        except ConnectionError as e:
            print 'No good  Got an error code:', e
        except URLError, e:
            print 'No good . Got an error code:', e



def cancel_trade(orderid):
        ##Cancels a single order, all orders for a tradepair or all open orders
        ##URI: https://www.cryptopia.co.nz/api/CancelTrade
        ## 
        ##Input:
        ##Type: The type of cancellation, Valid Types: 'All',  'Trade', 'TradePair'
        ##OrderId: The order identifier of trade to cancel (required if type 'Trade')
        ##TradePairId: The Cryptopia tradepair identifier of trades to cancel e.g. '100' (required if type 'TradePair')
        try:
            result, error = api_wrapper.cancel_trade('Trade', orderid,99999) # cancels 1 order with specific id
            print "         | cancel orderid",result
        except ValueError:
            print 'No good api'
        except ConnectionError as e:
            print 'No good  Got an error code:', e
        except URLError, e:
            print 'No good . Got an error code:', e
        



def transfer_coins():
    success = False
    txid='0000'
    vout=0
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:52541"%(rpcuser, rpcpassword))

    # STEP 1. select best, smallest, txid to transfer    
    # bulwark-cli listunspent 70 9999999 '''["bRTwEvdihGjjCKRSiLM84xZaiwgfZCADFx"]'''
    addr= [bwkaddress_from]
    listunspent = rpc_connection.listunspent(70, 999999, addr)
    #print len(listunspent)
    smallestvalidamount=100000000.0
    for k in range (len(listunspent)):
        if listunspent[k]["amount"]>=transfer_amount and listunspent[k]["spendable"]:
        
            if listunspent[k]["amount"]<=smallestvalidamount:
                smallestvalidamount= listunspent[k]["amount"]
                txid = listunspent[k]["txid"]
                vout = listunspent[k]["vout"]

    if smallestvalidamount<10000000.0:
            print "         | valid txid found for sending", transfer_amount," :",listunspent[k]["txid"]," ", smallestvalidamount
            # STEP 2. create raw tx
            # format cli: bulwark-cli createrawtransaction '[{"txid" : "000000000...000","vout" : 1}]' '{"bRTw...adres": 101.0, "bGM....adres": 4.41}'
            change= decimal.Decimal(smallestvalidamount) - decimal.Decimal(transfer_amount) - decimal.Decimal(0.00001)
            json1=[{"txid": txid, "vout" : vout }]
            json2={ bwkaddress_from : float(change) , bwkaddress_to : float(transfer_amount) }
            #print(json.dumps(json1))
            rawtx_hex = rpc_connection.createrawtransaction(json1,json2)

            # STEP 3. unlock wallet
            if not wallet_manually_unlocked_mode:
                rpc_connection.walletpassphrase(walletpassphrase, 99999999, wallet_manually_unlocked_mode)


            # STEP 4. sign raw tx
            # format cli: bulwark-cli signrawtransaction 00000...ab23
            rawsigned = rpc_connection.signrawtransaction(rawtx_hex)


            # STEP 5. send raw tx
            # format cli: bulwark-cli sendrawtransaction 00000...gb23
            signed_hex = rawsigned["hex"]
            sendresult = rpc_connection.sendrawtransaction(signed_hex)
            if "{" not in sendresult: #in case error it gives a {..json error message }
                    success = True
                    print "         | done sending coins, blockchain txid will be ",sendresult
    return success


def get_latest_block():
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:52541"%(rpcuser, rpcpassword))
    blockcount = rpc_connection.getblockcount()
    return blockcount

if __name__ == '__main__':

    buy_orders_dict = {}
    sell_orders_dict= {}

    last_highest_bid = 0
    last_lowest_ask = 0
    sell_rate= 0.0
    min_counter = 0
  
    # argument at startup specifies coin, should be equal to a value in .ini 
    if len(sys.argv) > 1:
        ini_arg= sys.argv[1]
        print  'Started python bot with settings file:',ini_arg,''
    else:
        print 'No argument observed, settings file tradesettings.ini will be used'
        ini_arg='tradesettings.ini'


    # settings file
    settings = configparser.ConfigParser()
    settings.read(ini_arg)
    coin_arg='BWK'

    # read settings
    rpcuser = settings.get(coin_arg,'rpcuser')
    rpcpassword = settings.get(coin_arg,'rpcpassword')
    bwkaddress_from = settings.get(coin_arg,'bwkaddress_from')
    bwkaddress_to = settings.get(coin_arg,'bwkaddress_to')
    transfer_mode = settings.getboolean(coin_arg,'transfer_mode')
    if transfer_mode:
        transfer_amount = settings.getfloat(coin_arg,'transfer_amount')
    order_amount_orig = settings.getfloat(coin_arg,'order_amount')
    order_interval = settings.getint(coin_arg,'order_interval')
    order_cancel_interval = settings.getint(coin_arg,'order_cancel_interval')

    transfer_interval = settings.getint(coin_arg,'transfer_interval')
    wallet_manually_unlocked_mode = settings.getboolean(coin_arg,'wallet_manually_unlocked_mode')
    if not wallet_manually_unlocked_mode:
        walletpassphrase = settings.get(coin_arg,'walletpassphrase')


    api_key= settings.get('Cryptopia','api_key')
    api_secret= settings.get('Cryptopia','api_secret')
    lowest_accepted_sell_rate = settings.getfloat('Cryptopia','lowest_accepted_sell_rate')

    parameter_lowest_ask = settings.getfloat('Cryptopia','parameter_lowest_ask')
    parameter_highest_bid = settings.getfloat('Cryptopia','parameter_highest_bid')
    parameter_delta = settings.getfloat('Cryptopia','parameter_delta')

    #limit = settings.getfloat(coin_arg,'nh_order_limit')
    #do_multi= settings.getboolean(coin_arg,'nh_do_multi')

    print "         | settings file processed"

    api_wrapper = Api(api_key, api_secret)
    min_volume_forweightedprice =50  # this approach neglect sell/buy orders with almost no volume. It weights average using upto cumulative sell/buy value

    # checks if RPC connection works
    get_latest_block()
    print "         | current Bulwark blockheight",get_latest_block()


    while True:
        order_amount = order_amount_orig + order_amount_orig * (random.randint(-5,5)/50.0)
        highest_bid_weighted, lowest_ask_weighted = getmarketorders()
        highest_bid_weighted = round(highest_bid_weighted,7)
        lowest_ask_weighted = round(lowest_ask_weighted,7)
        if  highest_bid_weighted>0 and lowest_ask_weighted>0:

                # initialize
                if last_highest_bid==0:
                        last_highest_bid = round(highest_bid_weighted, 7) 
                        last_lowest_ask =  round(lowest_ask_weighted, 7)

                # smooth to have a better estimate of trend, neglect sudden extremes
                highest_bid_smoothed = round(0.6 * last_highest_bid + 0.4 * highest_bid_weighted, 7)
                lowest_ask_smoothed = round(0.6 * last_lowest_ask + 0.4 * lowest_ask_weighted, 7)
                
                 

                # determine current good sell rate
                
                sell_rate = parameter_highest_bid * highest_bid_smoothed + parameter_lowest_ask*lowest_ask_smoothed + parameter_delta

                if sell_rate<lowest_accepted_sell_rate:
                   sell_rate = lowest_accepted_sell_rate 
                
                # show rates
                print datetime.datetime.now().time().replace(microsecond=0), "| highest bid @" , highest_bid_weighted, "/ lowest ask @", lowest_ask_weighted, "/ your sell rate will be @",sell_rate

                # update
                last_highest_bid = highest_bid_smoothed
                last_lowest_ask =  lowest_ask_smoothed                     
 
        # every minute, update minute counter / check if orders must be cancelled
        get_openorders()
        min_counter=min_counter+1;
        sleep(55)

        # every x minutes, check if we have a balance to be sold
        if min_counter%order_interval==0: #e.g. every 60 minutes
            print datetime.datetime.now().time().replace(microsecond=0), "| check Cryptopia for sufficient balance to place sell order "
            bal = get_balance('BWK')
            # sell orders only possible above approx 5 bwk (0.005 btc)           
            if bal >= order_amount:
                submit_trade(sell_rate,order_amount)

        # every y minutes, transfer coins from wallet to Cryptopia
        if min_counter==transfer_interval:  #e.g. every 1440 minutes
            min_counter=0
            if transfer_mode:
                print datetime.datetime.now().time().replace(microsecond=0), "| ****  initiate possible coin transfer from wallet to Cryptopia  ****"
                transfer_coins()
            


