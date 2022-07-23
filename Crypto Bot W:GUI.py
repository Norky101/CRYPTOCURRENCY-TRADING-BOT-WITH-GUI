#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import cbpro
import PySimpleGUI as sg   
import requests
import json

api_secret = ''
api_key =  ''
api_pass = ''


# In[3]:


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


# In[4]:


# Closes after n messages or when loses connection
stream = TextWebsocketClient(products=['ETH-BTC'],channels=['ticker'])
stream.start()


# In[5]:


#stream.close()
print ("Stream closed")


# In[6]:


# creates client variable
url='https://api-public.sandbox.pro.coinbase.com'

client = cbpro.AuthenticatedClient(
    api_key,
    api_secret,
    api_pass,
    api_url=url
)


# In[7]:


#Placing a BUY market order
def buy():
    client.place_market_order(product_id='ETH-BTC',side='buy',funds=0.00010)
    return "Buy Complete"


# In[8]:


def sell():
    client.place_market_order(product_id='ETH-BTC',side='sell',funds=0.00003)
    return "Sell Complete"


# In[9]:


# AVERAGE PRCIE
# https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-transactions
def average_price():
    #average = requests.get("https://api.coinbase.com/v2/accounts/:account_id/transactions").json()
    # OR
    
    buy_data = 'https://api.coinbase.com/v2/accounts/:account_id/buys/:buy_id'
    
    
    price = (buy_data['subtotal']['amount'] / buy_data['amount']['amount'])
    
    # OR
    
    #txs = client.get_transactions('2bbf394c-193b-5b2a-9155-3b4732659ede')
    
    return price
average_price()


# https://api.pro.coinbase.com/transfers?type=deposit

# That is not my trades but the whole coinbase user base active trades


# In[ ]:


# Displaying the price
def price():
    ticker = requests.get('https://api.pro.coinbase.com/products/ETH-USD/ticker').json()

    return ticker['ask'] # return the asking price 


# In[ ]:


# Gets the account history

accounts = client.get_accounts()

for acc in accounts:
    currency = acc.get('currency')
    if currency=='ETH':
        acc_id = acc.get('id')
    
acc_history = client.get_account_history(acc_id)


# In[ ]:


# Should return a list of stats for 24hr, I will need to Parse this and then calculate perccent
# https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductstats

# (data.last - data.open)/data.open*100  # Calculates percent change

def percentage_change():

    url = 'https://api.pro.coinbase.com/products/ETH-USD/stats'

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    response = response.json()
    #print(response)  # Prints the stats
   # print("-----------------\n")
    
    # conver to floats
    openval= float(response['open'])
    highval = float(response['high'])
    lowval = float(response['low'])
    lastval = float(response['last'])
    
    percent = (((lastval - openval ) / openval *100 ))  # percent math
    
    return float(round(percent, 2))  # returns percent with 2 decimal places

percentage_change()


# In[10]:


# GUI 
theme_name_list = sg.theme('DarkGreen')
sg.set_options(font=("Courier New", 20))

#Buttons
layout = [ 
            [sg.Text("Welcome to your\nCrypto Command Launch Pad!\n\nSelect a command...")],
            [sg.Button('Buy')],
            [sg.Button('Sell')],
            [sg.Button('Current Price')],
            [sg.Button('24 hr percent change')],
            [sg.Button('Profit/Loss')],
            [sg.Button('Exit')]
         ]
            
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



# In[ ]:





# In[ ]:




