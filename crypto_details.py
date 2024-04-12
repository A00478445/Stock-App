import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to fetch all available coins
def get_coin_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-V9bekAbwemrie8vxeQN1pZri"
}

    response = requests.get(url,headers=headers)
    if response.ok:
        return {coin['name']: coin['id'] for coin in response.json()}
    else:
        st.error(f"Failed to fetch data: HTTP Status Code {response.status_code}")
        return {}

# Function to fetch historical data for a given coin
def get_historical_data(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-V9bekAbwemrie8vxeQN1pZri"
    }
    response = requests.get(url, params=params,headers=headers)
    if response.ok:
        prices = response.json()['prices']       
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('date', inplace=True)
        return df
    else:
        st.error(f"Failed to fetch historical data: HTTP Status Code {response.status_code}")
        return pd.DataFrame()
# Function to fetch historical data of volumes
def get_volume_data(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-V9bekAbwemrie8vxeQN1pZri"
    }
    response = requests.get(url, params=params,headers=headers)
    if response.ok:
        total_volume = response.json()['total_volumes']
        v_df = pd.DataFrame(total_volume, columns=['timestamp', 'total_volumes'])
        v_df['date'] = pd.to_datetime(v_df['timestamp'], unit='ms')
        v_df.set_index('date', inplace=True)
        return v_df
    else:
        st.error(f"Failed to fetch historical data: HTTP Status Code {response.status_code}")
        return pd.DataFrame()


st.title('Cryptocurrency Details Viewer')

coin_list = get_coin_list()
coin_name = st.selectbox('Select a cryptocurrency:', list(coin_list.keys()))

if coin_name:
    coin_id = coin_list[coin_name]
    df = get_historical_data(coin_id)
    v_df = get_volume_data(coin_id)
    if not df.empty:
        st.plotly_chart(px.line(df, x=df.index, y='price', title=f'Price Trend for {coin_name} over the Last Year'))
        
        max_price = df['price'].max()
        min_price = df['price'].min()
        max_date = df['price'].idxmax()
        min_date = df['price'].idxmin()

        st.write(f"Maximum Price: ${max_price:.4f} on {max_date.strftime('%Y-%m-%d')}")
        st.write(f"Minimum Price: ${min_price:.4f} on {min_date.strftime('%Y-%m-%d')}")

        highest_volume = v_df['total_volumes'].max()
        lowest_volume = v_df['total_volumes'].min()
        highest_date = v_df['total_volumes'].idxmax()
        lowest_date = v_df['total_volumes'].idxmin()
        # Display the specific days for max and min prices
        st.write(f"The highest trading day was on {highest_date.strftime('%Y-%m-%d')} with a price of {highest_volume:.4f}.")
        st.write(f"The lowest trading day was on {lowest_date.strftime('%Y-%m-%d')} with a price of {lowest_volume:.4f}.")
