import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests

FMP_API_KEY = "XYlUcgrSf3yRbKcXbGQ4QPnGDFOcEajs"


def get_etf_data(ticker):
    etf = yf.Ticker(ticker)
    info = etf.info
    history = etf.history(period="5y")
    return info, history


def get_etf_holdings(ticker):
    url = f"https://financialmodelingprep.com/api/v3/etf-holder/{ticker}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        holdings = response.json()
        if isinstance(holdings, list) and len(holdings) > 0:
            df = pd.DataFrame(holdings)
            df['weightPercentage'] = df['weightPercentage'].astype(float)
            return df.sort_values('weightPercentage', ascending=False).reset_index(drop=True)
        else:
            st.warning(f"No holdings data available for {ticker}.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching holdings data: {e}")
        return None

def calculate_annualized_return(history):
    total_return = (history['Close'].iloc[-1] / history['Close'].iloc[0]) - 1
    years = len(history) / 252  # Assuming 252 trading days per year
    annualized_return = (1 + total_return) ** (1 / years) - 1
    return annualized_return

st.title("ETF Comparison Tool")

st.markdown("""
**Welcome to Sherry's ETF Comparison Tool**  
Use this tool to compare different ETFs based on ticker, to see the returns and overlapping holdings in each. There will be some ETFs that are missing in the tool based on our existing dataset.

For any questions or feedback or would like us to add more ETFs, don't hesitate to reach out to [sherry@peek.money](mailto:sherry@peek.money)!

This product was created by Sherry from the Peek team. If you would like to automatically connect your ETF holdings to understand overlaps, sign up for the waitlist for Peek at [peek.money](https://peek.money).
""")

st.markdown("<br>", unsafe_allow_html=True)



etf1 = st.text_input('Enter the first ETF ticker:')
etf2 = st.text_input('Enter the second ETF ticker:')

if etf1 and etf2:
    with st.spinner('Fetching ETF data...'):
        try:
            info1, history1 = get_etf_data(etf1)
            info2, history2 = get_etf_data(etf2)
            holdings1 = get_etf_holdings(etf1)
            holdings2 = get_etf_holdings(etf2)

            st.header(f'Comparison: {etf1} vs {etf2}')

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(etf1)
                st.write(f"Name: {info1.get('longName', 'N/A')}")
                if not history1.empty:
                    annualized_return1 = calculate_annualized_return(history1)
                    st.write(f"5-Year Annualized Return: {annualized_return1:.2%}")
                else:
                    st.write("5-Year Annualized Return: N/A")

            with col2:
                st.subheader(etf2)
                st.write(f"Name: {info2.get('longName', 'N/A')}")
                if not history2.empty:
                    annualized_return2 = calculate_annualized_return(history2)
                    st.write(f"5-Year Annualized Return: {annualized_return2:.2%}")
                else:
                    st.write("5-Year Annualized Return: N/A")
            if not history1.empty and not history2.empty:
                st.header('Performance Comparison (Last 12 Months)')
                
                # Resample data to ensure matching dates and remove duplicates
                history1_resampled = history1['Close'].last('12M').resample('D').last().dropna()
                history1_resampled = history1_resampled.loc[~history1_resampled.index.duplicated(keep='first')]
                
                history2_resampled = history2['Close'].last('12M').resample('D').last().dropna()
                history2_resampled = history2_resampled.loc[~history2_resampled.index.duplicated(keep='first')]
                
                # Align the two series and forward fill any missing values
                combined_history = pd.concat([history1_resampled, history2_resampled], axis=1, join='outer').fillna(method='ffill')
                combined_history.columns = [etf1, etf2]

                # Calculate percentage change
                combined_history = combined_history.pct_change().add(1).cumprod()
                st.line_chart(combined_history)
            else:
                st.warning("Unable to generate performance comparison due to missing historical data.")

            st.header('Holdings Comparison')
            if holdings1 is not None and holdings2 is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f'{etf1} Top 10 Holdings')
                    st.dataframe(holdings1.head(10)[['asset', 'weightPercentage']].set_index('asset'))
                with col2:
                    st.subheader(f'{etf2} Top 10 Holdings')
                    st.dataframe(holdings2.head(10)[['asset', 'weightPercentage']].set_index('asset'))

            st.subheader('Common Holdings Comparison')
            
            if holdings1 is not None and holdings2 is not None:
                common_holdings = set(holdings1['asset']) & set(holdings2['asset'])
                
                if len(common_holdings) > 0:
                    common_holdings_list = []
                    for holding in common_holdings:
                        weight1 = holdings1[holdings1['asset'] == holding]['weightPercentage'].values[0]
                        weight2 = holdings2[holdings2['asset'] == holding]['weightPercentage'].values[0]
                        min_weight = min(weight1, weight2)
                        common_holdings_list.append((holding, min_weight))
                    
                    # Sort by the largest common holding
                    common_holdings_list.sort(key=lambda x: x[1], reverse=True)
                    
                    total_common_weight = sum(weight for _, weight in common_holdings_list)
                    st.write(f"Total weight of all common holdings: {total_common_weight:.2f}%")
                    
                    st.write("Top 10 common holdings sorted by minimum percentage:")
                    for idx, (holding, min_weight) in enumerate(common_holdings_list[:10], start=1):
                        st.write(f"{idx}. {holding}: {min_weight:.2f}%")
                    
                else:
                    st.write("No common holdings found.")
            else:
                st.warning("Unable to fetch holdings data for one or both of the ETFs.")
        except Exception as e:
            st.error(f"An error occurred while processing the ETF data: {str(e)}")
else:
    st.write('Please enter both ETF tickers to compare.')

