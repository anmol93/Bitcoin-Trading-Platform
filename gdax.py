'''
The service I created is the first function you see below. It takes an object called "input_object" as
input which provides the values - action, base_currency, quote_currency and amount. The gax_web_service
function checks if the base and quote currency pair exists in the gdax order book and calls function
get_quote if they do, calls get_quote2 if they exist inversely or return object containing the error message
if the currencies cannot be traded. Functions get_quote and get_quote2 call functions buyorsell and
buyorsell2 respectively. Functions buyorsell and buyorsell2 compute the aggregated orders to provide the
the best value and returns them to get_quote and get_quote2 respectively, which return them back to
gdax_web_service.

Instead of creating a class of these functions, I decided to create separate file for storing
the functions.

'''

import requests
import json

def gdax_web_service(input_object):
    action = input_object['action']
    bc = input_object['base_currency']
    qc = input_object['quote_currency']
    amount = input_object['amount']
    if amount.isdigit():
        amount = float(amount)
        if amount > 0:
            url1 = "https://api.gdax.com/products"
            data1 = requests.get(url1).json()
            quote = 0
            for ex in data1:  # To iterate through every currency pair in the list found on url1
                if bc == ex['base_currency'] and qc == ex['quote_currency']:
                    quote = get_quote(action, bc, qc, amount)  # Then called the get_quote function that returns the json_quote object
                elif bc == ex['quote_currency'] and qc == ex['base_currency']:
                    quote = get_quote2(action, bc, qc, amount)  # Inverse currency pairs with reference to the GDAX trading pairs go to this separate function
                else:
                    pass
            if quote != 0:
                return(quote)  # Finally printed the quote
            else:
                err = {'error': 'These currencies cannot be traded'}
                return(err['error'])
        else:
            err = {'error': 'This amount cannot be traded'}
            return (err['error'])
    else:
        err = {'error': 'This amount cannot be traded'}
        return (err['error'])

def get_quote(action, bc, qc, amount):
    url2 = "https://api.gdax.com/products/" + bc + "-" + qc + "/book?level=2"
    #Created the url to access the order book through the api.
    data2 = requests.get(url2).json()
    if action == "buy":
        list = data2["asks"]    #List of the top 50 asks
        return(buyorsell(list, qc, amount))     #Called the function that aggregates orders from the order book and returns the quote object
    if action == "sell":
        list = data2["bids"]    #list of the top 50 bids
        return(buyorsell(list, qc, amount))

def get_quote2(action, bc, qc, amount):
    url3 = "https://api.gdax.com/products/" + qc + "-" + bc + "/book?level=2"
    #Switched the quote currency and base currency to put in the link to retrieve the order book
    data2 = requests.get(url3).json()
    if action == "buy":
        list = data2["asks"]
        return(buyorsell2(list, qc, amount))
        #A separate function to aggregate orders for currency pairs that are inverse of GDAX trading pairs
    if action == "sell":
        list = data2["bids"]
        return(buyorsell2(list, qc, amount))

def buyorsell(list, qc, amount):
    #print(list)
    pa = amount
    val = 0
    for item in list:   #To iterate through each of the top 50 bids or asks
        if amount != 0:     #The amount that we need to aggregate from multiple orders to get the best price/value
            count = item[2]     #Count stored the "num-orders" value from entries in the oder book
            while count != 0:
                if float(item[1])>amount:   #Compares the quote currency's size(quantity) with the amount remaining to be aggregated
                    val = val + (float(item[0]) * amount)
                    amount = 0
                if float(item[1])<=amount:
                    val = val + (float(item[0])*float(item[1]))
                    #Calculates the best value- max for sell orders and min for buy orders
                    amount = amount - float(item[1])
                    count = count - 1
                if amount == 0:
                    break
    if amount != 0:
        err = {'error':'This is too big of an order to complete at the moment.\nThe best we could do right now for you is ' + str(pa-amount)}
        return(err['error'])
        exit()
    total = val
    price = '%f' % float(val / pa)
    currency = qc
    dict = {"total":total, "price":price, "currency":currency}
    json_dict = json.dumps(dict)
    return(json_dict)

def buyorsell2(list, qc, amount):   #Does essentially the same job as 'buyorsell' but for inverse currency pairs in reference to GDAX trading pairs.
    #print(list)
    pa = amount
    val = 0
    for item in list:
        if amount != 0:
            count = item[2]
            while count != 0:
                if (float(item[0])*float(item[1]))>amount:
                    val = val + amount/float(item[0])
                    amount = 0
                if (float(item[0])*float(item[1]))<=amount:
                    val = val + float(item[1])
                    amount = amount - (float(item[0])*float(item[1]))
                    count = count - 1
                if amount == 0:
                    break
    if amount != 0:
        err = {'error':'This is too big of an order to complete at the moment.\nThe best we could do right now for you is ' + str(pa-amount)}
        return(err['error'])
        exit()
    total = val
    price = '%f' % float(val/pa)
    currency = qc
    dict = {"total": total, "price": price, "currency": currency}
    json_dict = json.dumps(dict)
    return (json_dict)

