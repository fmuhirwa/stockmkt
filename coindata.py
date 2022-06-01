from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from requests import Request, Session
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'limit':201,
    'convert':'USD',
    'sort_dir':'desc'
}

headers = {
    'Accepts':'application/json',
    'X-CMC_Pro_API_KEY': '0563239d-ff13-4d07-b193-8473cc5792b6'
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)

data = response.json()

df = pd.DataFrame.from_dict(data['data'])

key = [value for key, value in df['quote'].items()]
details = [each['USD'] for each in key]

i=0
pli = []
pc90li = []
mcli = []
while i < len(df.index):
    pli.append(details[i]['price'])
    pc90li.append(details[i]['percent_change_90d'])
    mcli.append(details[i]['market_cap'])
    i += 1

df['price'] = pli
df['% change 90d'] = pc90li
df['market cap'] = mcli
df = df.drop(columns='id')
df = df.drop(columns='slug')
df = df.drop(columns='num_market_pairs')
df = df.drop(columns='tags')
df = df.drop(columns='platform')
df = df.drop(columns='self_reported_circulating_supply')
df = df.drop(columns='self_reported_market_cap')
df = df.drop(columns='total_supply')
df = df.drop(columns='quote')
df['date_added'] = pd.to_datetime(df['date_added'])
df['last_updated'] = pd.to_datetime(df['last_updated'])
df['date_added'] = df['date_added'].dt.strftime('%d-%m-%Y')
df['last_updated'] = df['last_updated'].dt.strftime('%d-%m-%Y')

df = df.iloc[:, [5,2,0,1,7,8,9,4,3,6]]

st.title('Top 200 Cryptos By Market Cap')
st.subheader('Dataset')
st.dataframe(df)

#df.to_csv(f'{dt.now()}.csv')
