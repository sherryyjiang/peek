# #rebalancing

import yfinance as yf
import numpy as np
import pandas as pd
import openai
import os
import streamlit as st
from pydantic import BaseModel
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()

############################################################################################################################################################

# Add a toggle for dark mode
dark_mode = st.checkbox("Enable Dark Mode")

# Apply dark mode settings if enabled
if dark_mode:
    st.markdown(
        """
        <style>
        .css-18e3th9 {
            background-color: #0e1117;
            color: #c9d1d9;
        }
        .css-1d391kg {
            background-color: #0e1117;
        }
        .css-1cpxqw2 {
            color: #c9d1d9;
        }
        .css-1v3fvcr {
            color: #c9d1d9;
        }
        .css-1v0mbdj {
            color: #c9d1d9;
        }
        .css-1aehpvj {
            color: #c9d1d9;
        }
        .css-1cpxqw2 a {
            color: #58a6ff;
        }
        .css-1cpxqw2 a:hover {
            color: #1f6feb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


############################################################################################################################################################

# Function to calculate portfolio metrics

def calculate_portfolio_metrics(portfolio):
    total_return = 0
    total_std_dev = 0
    total_weight = 0

    for asset, weight in portfolio.items():
        if asset in available_assets:
            data = yf.download(asset, start="2015-01-01", end="2024-01-01")['Adj Close']
            annual_returns = data.resample('YE').ffill().pct_change().dropna()
            geometric_return = (np.prod(1 + annual_returns) ** (1 / len(annual_returns)) - 1) * 100
            variance = np.var(annual_returns, ddof=1)
            std_dev_annual_return = np.sqrt(variance) * 100
        else:
            geometric_return = 10
            std_dev_annual_return = 10
        total_return += geometric_return * weight
        total_std_dev += std_dev_annual_return * weight
        total_weight += weight
    
    if total_weight == 0:
        return 0, 0, 0  # Avoid division by zero if total_weight is zero
    
    sharpe_ratio = (total_return - 5) / total_std_dev if total_std_dev != 0 else 0
    return total_return, total_std_dev, sharpe_ratio

# Streamlit app
st.title("Portfolio Rebalancing Simulator")

st.subheader("Introduction")
st.markdown("""
The portfolio rebalancing simulator tool is designed to help users optimize their investment portfolios by experimenting with different allocation percentages. Users input basic information such as net worth, risk appetite, and age, which guide the tool's allocation suggestions. They also input their current portfolio, which focuses on liquid or public assets with prices pulled from Yahoo! Finance.

The tool provides key portfolio health metrics, including annualized return, standard deviation, and Sharpe ratio, calculated since 2015. Based on this data, users receive AI-generated suggestions to adjust their portfolio for either de-risking or enhancing growth. Additionally, users can add new items with varying weights to visualize how these changes affect overall portfolio health.

This allows for dynamic experimentation, helping users make informed decisions to achieve their desired financial outcomes. Remember, past performance does not guarantee future results, but it could be used as an indicator. The information provided is for educational and informational purposes only and should not be construed as financial advice.

For any questions or feedback, don't hesitate to reach out to sherry@peek.money! This product was created by Sherry from the Peek team. If you like what you see, and want more of it, check out [peek.money](https://peek.money)! Tools like this can be directly integrated with real-time information around your portfolio so you don't have to manually enter each time.
""")


############################################################################################################################################################

def clean_data(value):
    """Remove non-numeric characters except for the decimal point."""
    if isinstance(value, str):
        cleaned_value = ''.join(char for char in value if char.isdigit() or char == '.')
        try:
            return float(cleaned_value)
        except ValueError:
            return None
    return value

############################################################################################################################################################


# Basic Information

st.header("Basic Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Net Worth")
    net_worth = st.number_input("Enter your estimated net worth:", min_value=0.0, step=1000.0, value=500000.0)

    st.subheader("User Information")
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1, value=35)

with col2:
    st.subheader("Risk Appetite")
    risk_appetite = st.selectbox(
        "Select your risk appetite:",
        ("Conservative (tolerate 0-10% loss)", "Moderate (tolerate 10% to 20% loss)", "Aggressive (tolerate 20%+ loss)"),
        index=1
    )
    st.subheader("Dependents")
    dependents = st.selectbox(
        "Do you have any dependents?",
        ("Yes", "No"),
        index=1
    )

############################################################################################################################################################

# Input current portfolio

st.header("Current Portfolio")

st.markdown("""
Add in estimations for your current portfolio in liquid assets with tickers. To simplify it farther, you can add just the largest holdings you recall off the top of your head. We are pulling the live and historical ticker price from Yahoo! Finance. Your private or illiquid assets like property or alternative assets will not be included in this calculation.
<br><br>
""", unsafe_allow_html=True)

############################################################################################################################################################



#OpenAI tickers suggestions

def get_ticker_suggestions(portfolio_description):
    prompt = (
        f"Only return the tickers based on the following portfolio description:\n"
        f"{portfolio_description}\n\n"
        "Format: TICKER1, TICKER2, TICKER3, ..."
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial analyst. Your task is to list out the tickers for the users easily based on the description of their investments. Only provide the tickers, separated by commas."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            model="gpt-4-turbo",
            temperature=0.5,
            max_tokens=1000
        )
        suggestions = chat_completion.choices[0].message.content
        return suggestions.strip()
    except Exception as e:
        return f"An error occurred while fetching the LLM suggestions: {e}"

st.subheader("Step 1: Get Ticker - AI widget")
portfolio_description = st.text_area("Enter your public market positions if you can't remember the tickers. Separate each entry by a comma. Only valid tickers will show up:")

# Use session state to persist the output
if "tickers" not in st.session_state:
    st.session_state.tickers = ""

if st.button("Get Ticker"):
    if portfolio_description:
        st.session_state.tickers = get_ticker_suggestions(portfolio_description)
    else:
        st.warning("Please provide the names of the assets in your portfolio.")

if st.session_state.tickers:
    st.write(f"Suggested Tickers: {st.session_state.tickers}")



############################################################################################################################################################

#Portfolio Table

st.subheader("Step 2: Add Your Current Portfolio")

st.markdown("""
Add in your current holdings and their respective % of your portfolio first in column 1 and 2. Leave "New % Holdings" blank for now until you know what % allocations you want to rebalance to.
<br><br>
""", unsafe_allow_html=True)

# Create an empty DataFrame with the specified columns
portfolio_df = pd.DataFrame(columns=["Stock Ticker", "% Holding", "New % Holding", "Annualized Returns", "Standard Deviation"])

# Display the DataFrame as an editable table
portfolio_df = st.data_editor(portfolio_df, num_rows="dynamic", column_config={
    "% Holding": st.column_config.NumberColumn(format="%.2f"),
    "New % Holding": st.column_config.NumberColumn(format="%.2f")
})


# Calculate the total for % Holding and New % Holding columns
total_row = pd.DataFrame(portfolio_df[["% Holding", "New % Holding"]].sum()).transpose()
total_row["Stock Ticker"] = "Total"
total_row["Annualized Returns"] = ""
total_row["Standard Deviation"] = ""
total_row["Notes"] = ""

# Check if the total % Holding is less than 100%
if total_row["% Holding"].iloc[0] < 100.0:
    st.warning("The total percentage of your current holdings is less than 100%. Please ensure your portfolio allocations sum up to 100%.")

# Check if the total % Holding is more than 100%
if total_row["% Holding"].iloc[0] > 100.0:
    st.warning("The total percentage of your current holdings is more than 100%. Please ensure your portfolio allocations sum up to 100%.")


def fetch_annualized_return_and_std(ticker):
    try:
        data = yf.download(ticker, start="2015-01-01", end="2024-01-01")
        data['Return'] = data['Open'].pct_change()
        annual_returns = data.resample('YE').ffill().pct_change().dropna()
        annualized_return = round((np.prod(1 + annual_returns) ** (1 / len(annual_returns)) - 1) * 100, 2)
        variance = np.var(annual_returns, ddof=1)
        std_dev = round(np.sqrt(variance) * 100, 2)
        return annualized_return, std_dev
    except Exception as e:
        st.warning(f"Could not fetch data for {ticker}. Using defaults of 10.00% return and 10.00% standard deviation.")
        return 10.00, 10.00


# Fetch annualized return and standard deviation for each ticker in the portfolio
for index, row in portfolio_df.iterrows():
    ticker = row["Stock Ticker"]
    if ticker:
        annualized_return, std_dev = fetch_annualized_return_and_std(ticker)
        portfolio_df.at[index, "Annualized Returns"] = str(annualized_return)[12:19]
        portfolio_df.at[index, "Standard Deviation"] = str(std_dev)[12:20]

# Check if the total % Holding is exactly 100%
if total_row["% Holding"].iloc[0] == 100.0 and portfolio_df["New % Holding"].sum() != 100.0:
    # st.success("See your initial portfolio review below")
    # Create a new DataFrame with the required columns
    initial_portfolio_df = portfolio_df[["Stock Ticker", "% Holding", "New % Holding", "Annualized Returns", "Standard Deviation"]]
    
    # Display the new DataFrame as a table
    st.write("Output - Portfolio Allocation, Annualized Return and Standard Deviation")
    st.dataframe(initial_portfolio_df)


if portfolio_df["New % Holding"].sum() == 100.0:
    st.success("See your rebalanced portfolio review below")
    initial_portfolio_df = portfolio_df[["Stock Ticker", "% Holding", "New % Holding", "Annualized Returns", "Standard Deviation"]]
    
    # Display the new DataFrame as a table
    st.write("Output - Portfolio Allocation, Annualized Return and Standard Deviation")
    st.dataframe(initial_portfolio_df)

# Calculate portfolio level annualized returns and standard deviation
portfolio_returns = []
portfolio_std_devs = []

for index, row in portfolio_df.iterrows():
    if row["Annualized Returns"] and row["Standard Deviation"]:
        weight = row["% Holding"]
        if weight is not None:
            weight /= 100
            annualized_return = clean_data(row["Annualized Returns"])
            std_dev = clean_data(row["Standard Deviation"])
            portfolio_returns.append(weight * annualized_return)
            portfolio_std_devs.append((weight * std_dev) ** 2)

# Calculate weighted average of annualized returns
portfolio_annualized_return = sum(portfolio_returns)

# Calculate portfolio standard deviation
portfolio_std_dev = np.sqrt(sum(portfolio_std_devs))

st.subheader("Initial Portfolio Review")


# Display portfolio level annualized returns and standard deviation only if % holdings add up to 100%
if total_row["% Holding"].iloc[0] == 100.0:
    st.write(f"Initial Portfolio Annualized Return: {portfolio_annualized_return:.2f}%")
    st.write(f"Initial Portfolio Standard Deviation: {portfolio_std_dev:.2f}%")

# Display expected range of outcomes based on return and standard deviation
if total_row["% Holding"].iloc[0] == 100.0:
    st.subheader("Expected Range of Outcomes")

    # Calculate the expected range of outcomes
    mean_return = portfolio_annualized_return / 100
    std_dev = portfolio_std_dev / 100

    # Assuming a normal distribution, calculate the range for 1, 2, and 3 standard deviations
    one_std_dev_range = (mean_return - std_dev, mean_return + std_dev)

    st.write(f"1 Standard Deviation Range: {one_std_dev_range[0] * 100:.2f}% to {one_std_dev_range[1] * 100:.2f}%")
    st.write(f"{one_std_dev_range[0] * 100:.2f}% is the amount that you could expect to lose in a bad year.")

############################################################################################################################################################

#Rebalancing Action

# Check if the total New % Holding is exactly 100%
if portfolio_df["New % Holding"].sum() == 100.0:
    new_portfolio_returns = []
    new_portfolio_std_devs = []

    for index, row in portfolio_df.iterrows():
        if row["Annualized Returns"] and row["Standard Deviation"]:
            new_weight = row["New % Holding"]
            if new_weight is not None:
                new_weight /= 100
                annualized_return = clean_data(row["Annualized Returns"])
                std_dev = clean_data(row["Standard Deviation"])
                new_portfolio_returns.append(new_weight * annualized_return)
                new_portfolio_std_devs.append((new_weight * std_dev) ** 2)

    # Calculate weighted average of annualized returns for new portfolio
    new_portfolio_annualized_return = sum(new_portfolio_returns)

    # Calculate portfolio standard deviation for new portfolio
    new_portfolio_std_dev = np.sqrt(sum(new_portfolio_std_devs))


    # Display new portfolio level annualized returns and standard deviation
    st.subheader("Rebalanced Portfolio Review")
    st.write(f"New Portfolio Annualized Return: {new_portfolio_annualized_return:.2f}%")
    st.write(f"New Portfolio Standard Deviation: {new_portfolio_std_dev:.2f}%")

else:
    if portfolio_df["New % Holding"].notna().sum() > 0:
        st.warning("The total New % Holding must add up to 100% to proceed with rebalancing.")

# Display expected range of outcomes based on return and standard deviation for the rebalanced portfolio
if portfolio_df["New % Holding"].sum() == 100.0:
    st.subheader("Expected Range of Outcomes for Rebalanced Portfolio")

    # Calculate the expected range of outcomes
    new_mean_return = new_portfolio_annualized_return / 100
    new_std_dev = new_portfolio_std_dev / 100

    # Assuming a normal distribution, calculate the range for 1 standard deviation
    new_one_std_dev_range = (new_mean_return - new_std_dev, new_mean_return + new_std_dev)

    st.write(f"1 Standard Deviation Range: {new_one_std_dev_range[0] * 100:.2f}% to {new_one_std_dev_range[1] * 100:.2f}%")
    st.write(f"{new_one_std_dev_range[0] * 100:.2f}% is the amount that you could expect to lose in a bad year.")



############################################################################################################################################################

#Rebalancing Charts

st.subheader("Differences in Initial and Rebalanced Portfolio")


# Calculate the difference in annualized return and standard deviation between the initial and the new portfolio
if total_row["% Holding"].iloc[0] == 100.0 and portfolio_df["New % Holding"].sum() == 100.0:
    return_difference = new_portfolio_annualized_return - portfolio_annualized_return
    std_dev_difference = new_portfolio_std_dev - portfolio_std_dev

    st.write(f"Difference in Annualized Return: {return_difference:.2f}%")
    st.write(f"Difference in Standard Deviation: {std_dev_difference:.2f}%")

# Show changes between % holdings and % new holdings
if total_row["% Holding"].iloc[0] == 100.0 and portfolio_df["New % Holding"].sum() == 100.0:
    st.subheader("Changes in Holdings")
    changes_df = portfolio_df.copy()
    changes_df["Change in % Holding"] = changes_df["New % Holding"] - changes_df["% Holding"]
    changes_df["Change in $ Amount"] = (changes_df["Change in % Holding"] / 100) * net_worth
    st.write(changes_df[["Stock Ticker", "% Holding", "New % Holding", "Change in % Holding", "Change in $ Amount"]])


############################################################################################################################################################

# Function to assess and rebalance the portfolio

def assess_and_rebalance_portfolio(portfolio_df, portfolio_annualized_return, portfolio_std_dev, risk_appetite, age, dependents):
    # Filter out assets with zero allocation
    non_zero_portfolio_df = portfolio_df[portfolio_df["% Holding"] != 0]

    prompt = (
        f"Step 1: Portfolio Assessment\n"
        f"Please assess the user's portfolio based on the following details:\n"
        f"- Current Annual Return: {portfolio_annualized_return}%\n"
        f"- Current Standard Deviation: {portfolio_std_dev}\n"
        f"- Asset allocation: {non_zero_portfolio_df}%\n"
        f"- Stated Risk Appetite: {risk_appetite}\n"
        f"- Stated Age: {age}\n"
        f"- Stated Dependents: {dependents}\n\n"
        f"Step 2: Recommendation\n"
        f"For instance, only recommend having more bonds of more than 10% if the user is older, has low risk appetite and has dependents. "
        f"For someone who is younger, risk-taking and has no dependents, a more equity-weighted portfolio is okay.\n"
        f"If the user is aggressive in their risk appetite, feel free to recommend them a much higher return higher standard deviation portfolio mix.\n"
        f"If the user is weighted more towards a certain sector, you can suggest for the user to diversify into ETFs in other sectors.\n\n"
        f"Step 3: Tell the user they could add in the recommended new allocations in the New % Holdings column in the table below \n"
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial analyst. Your task is to help the user understand the risks within their portfolio "
                        "and provide recommendations for rebalancing. You will assess the user's current portfolio, considering their "
                        "stated risk appetite, age, dependents, and provide an analysis and specific recommendations for adjustments. Your response should "
                        "include an assessment of asset allocation risk, concentration risk, and detailed suggestions for reducing exposure "
                        "to certain holdings. Additionally, you will recommend new assets to add to the portfolio, with exact percentages "
                        "for the new % holdings. Ensure that the percentages for % holdings and new % holdings are whole numbers. Provide the revised allocations in a table format so the user can easily copy and paste the table "
                        "Let the user know if they could copy/paste the table into the portfolio table above. If the user wants another suggested portfolio, inform them they can run the process again."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            model="gpt-4-turbo",
            temperature=0.7,
            max_tokens=1000
        )
        suggestions = chat_completion.choices[0].message.content
        return suggestions
    except Exception as e:
        return f"An error occurred while fetching the LLM suggestions: {e}"


# LLM suggestions for rebalancing
st.header("Get AI Rebalancing Suggestions")
if 'llm_suggestions' not in st.session_state:
    st.session_state.llm_suggestions = ""

if st.button("Get AI Rebalancing Suggestions"):
    with st.spinner('Fetching rebalancing suggestions...'):
        st.session_state.llm_suggestions = assess_and_rebalance_portfolio(portfolio_df, portfolio_annualized_return, portfolio_std_dev, risk_appetite, age, dependents)

st.write(st.session_state.llm_suggestions)