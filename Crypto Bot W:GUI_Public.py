#!/usr/bin/env python
# coding: utf-8

# Coinbase Pro Sandbox API with functional GUI

import pandas as pd
import cbpro
import PySimpleGUI as sg   
import requests
import json

api_secret = ''
api_key =  ''
api_pass = ''


#websocket
class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url           = 'wss://ws-feed-public.sandbox.pro.coinbase.com'  #connection endpoint
        self.message_count = 0
    
    def on_message(self,msg):   # creates message for onscreen
        self.message_count += 1
        msg_type = msg.get('type',None)
        if msg_type == 'ticker':
            # returns a dict of keys&values.
            # we then select the ones we want- 'time','price',ect
            time_val   = msg.get('time',('-'*27))
            price_val  = msg.get('price',None)
            if price_val is not None:
                price_val = float(price_val)
            product_id = msg.get('product_id',None)
            
            print(f"{time_val:40} {price_val:.3f} {product_id}\tchannel type: {msg_type}")
    
    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")
        
        # Could add these output prices to a database



# Closes after n messages or when loses connection
stream = TextWebsocketClient(products=['ETH-BTC'],channels=['ticker'])
stream.start()


#stream.close()
print ("Stream closed")



# creates client object
url='https://api-public.sandbox.pro.coinbase.com'

client = cbpro.AuthenticatedClient(
    api_key,
    api_secret,
    api_pass,
    api_url=url)




#Placing a BUY market order
def buy():
    client.place_market_order(product_id='ETH-BTC',side='buy',funds=0.00010)
    return "Buy Complete"


def sell():
    client.place_market_order(product_id='ETH-BTC',side='sell',funds=0.00003)
    return "Sell Complete"

# AVERAGE PRCIE
def average_price():

    
    buy_data = 'https://api.coinbase.com/v2/accounts/:account_id/buys/:buy_id'
    
    price = (buy_data['subtotal']['amount'] / buy_data['amount']['amount'])

    
    return price

# Displaying the price
def price():
    ticker = requests.get('https://api.pro.coinbase.com/products/ETH-USD/ticker').json()

    return ticker['ask'] # return the asking price 




# Gets the account history
accounts = client.get_accounts()

for acc in accounts:
    currency = acc.get('currency')
    if currency=='ETH':
        acc_id = acc.get('id')
    
acc_history = client.get_account_history(acc_id)



def percentage_change():

    url = 'https://api.pro.coinbase.com/products/ETH-USD/stats'

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    response = response.json()
    
    # conver to floats
    openval= float(response['open'])
    highval = float(response['high'])
    lowval = float(response['low'])
    lastval = float(response['last'])
    
    percent = (((lastval - openval ) / openval *100 ))  # percent math
    
    return float(round(percent, 2))  # returns percent with 2 decimal places


# GUI--------------------------------------
theme_name_list = sg.theme('DarkGreen')
sg.set_options(font=("Courier New", 20))

#Buttons
layout = [ 
            [sg.Text("Welcome to your\nCrypto Command Center!\n\nSelect a command...")],
            [sg.Button('Buy')],
            [sg.Button('Sell')],
            [sg.Button('Current Price')],
            [sg.Button('24 hr percent change')],
            [sg.Button('Exit')]
         ]

# Name and sizing
window = sg.Window('Crypto Buy/Sell Launch Pad', layout, size = (400, 400)) # title of window

# saves the actions(clicks) and the inputted values
while True:
    event, values = window.read()
    print(event, values)
    if event is None or event == "Exit":
        break
    
    if event == "Buy":   # Connected to Buy Function
        buy()
    if event == 'Sell':
        sell()
    if event == 'Current Price':
        sg.popup(price(), keep_on_top=True)
    if event == '24 hr percent change':
        sg.popup(percentage_change(), keep_on_top=True)
    
window.close()
