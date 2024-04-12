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

# UI Elements
st.title('Cryptocurrency Comparison Viewer')

# Fetching the list of coins
coin_list = get_coin_list()
choices = list(coin_list.keys())

# User selections
coin1_name = st.selectbox('Select the first cryptocurrency:', choices, index=choices.index('Bitcoin') if 'Bitcoin' in choices else 0)
coin2_name = st.selectbox('Select the second cryptocurrency:', choices, index=choices.index('Ethereum') if 'Ethereum' in choices else 0)
time_frame = st.selectbox('Select time frame:', options=['7', '30', '365', '1825'], index=2, format_func=lambda x: f"{int(x)/365:.1f} year(s)" if int(x) >= 365 else f"{x} day(s)")

# Convert time_frame to integer
days = int(time_frame)

# Fetching historical data based on user selections
if coin1_name and coin2_name:
    df1 = get_historical_data(coin_list[coin1_name], days)
    df2 = get_historical_data(coin_list[coin2_name], days)
    
    if not df1.empty and not df2.empty:
        # Merging dataframes for the plot
        df1 = df1.rename(columns={'price': f'price_{coin1_name}'})
        df2 = df2.rename(columns={'price': f'price_{coin2_name}'})
        df = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
        
        # Plotting the data
        fig = px.line(df, x=df.index, y=[f'price_{coin1_name}', f'price_{coin2_name}'],
                      title=f'Price Comparison of {coin1_name} vs {coin2_name} Over Selected Time Frame')
        st.plotly_chart(fig)
