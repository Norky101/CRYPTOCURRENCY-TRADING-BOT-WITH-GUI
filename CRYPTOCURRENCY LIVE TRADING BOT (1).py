#!/usr/bin/env python
# coding: utf-8

# In[12]:


get_ipython().system('pip install cbpro')
# must also install Py 3.5.0 version as CBPro API is outdated
# Must run notebook in order
# May need to change Notebook Py version
# https://public.sandbox.pro.coinbase.com/
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')

import pandas as pd
import cbpro

from Creds import (api_secret, api_key, api_pass)



# In[13]:


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


# In[14]:


# Closes after n messages or when loses connection
stream = TextWebsocketClient(products=['BTC-USD'],channels=['ticker'])
stream.start()


# In[15]:


#stream.close()
print ("Stream closed")


# In[16]:


# creates client variable
url='https://api-public.sandbox.pro.coinbase.com'

client = cbpro.AuthenticatedClient(
    api_key,
    api_secret,
    api_pass,
    api_url=url
)


# In[17]:


#Placing a BUY market order
# funds = x amount in usd e.g Buy $100 of BTC
# size = x amount in BTC  e.g Buy 1 BTC
client.place_market_order(product_id='BTC-USD',side='buy',funds=100)


# In[18]:


# checks account history for specific dict 'keys'

accounts = client.get_accounts()


# In[19]:


for acc in accounts:
    currency = acc.get('currency')
    if currency=='BTC':
        acc_id = acc.get('id')


# In[20]:


acc_history = client.get_account_history(acc_id)


# In[21]:


import json

for hist in acc_history:
    print(json.dumps(hist,indent=1))


# In[ ]:




