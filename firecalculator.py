# Imports
import streamlit as st

# Heading
st.markdown("<h1 style='color: #F39373; padding-bottom: 30px;'>🔥 FIRE (Financial Independence, Retire Early) Calculator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #F8F6F4; padding: 10px; border-radius: 5px; margin-bottom: 40px;'>
        <p style='color: #000000; font-size: 16px; font-weight: bold;'>Welcome to the FIRE Calculator</p>
        <p style='color: #000000;'>
            Use this tool to estimate how much you need to save to achieve financial independence and retire early. Simply input your annual expenses, current savings, expected annual return on investments, annual income, and savings rate.
        </p>
    </div>
""", unsafe_allow_html=True)

# Streamlit: Input fields
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Current Age", min_value=0.0, value=32.0, step=0.1, format="%.1f")
with col2:
    desired_fire_age = st.number_input("Desired FIRE Age", min_value=0.0, value=50.0, step=0.1, format="%.1f")

col3, col4 = st.columns(2)
with col3:
    annual_expenses = st.number_input("Annual Expenses ($)", min_value=0, value=100000, step=1000)
with col4:
    current_savings = st.number_input("Current Savings ($)", min_value=0, value=1000000, step=1000)

col5, col6 = st.columns(2)
with col5:
    annual_return = st.number_input("Expected Annual Return on Investments (%)", min_value=0.0, value=9.0, step=0.1)
with col6:
    annual_income = st.number_input("Annual Income ($) - assumed 3% growth rate", min_value=0, value=90000, step=1000)

col7, col8 = st.columns(2)
with col7:
    savings_rate = st.number_input("Savings Rate (%)", min_value=0.0, value=30.0, step=0.1)
with col8:
    inflation_rate = st.number_input("Inflation Rate (%)", min_value=0.0, value=3.0, step=0.1)


# Streamlit: Advanced options for Expected Annual Return on Investments (%)
st.markdown("<h2 style='color: #F39373;'>Advanced Options for Expected Annual Return on Investments (%)</h2>", unsafe_allow_html=True)

col9, col10 = st.columns(2)
with col9:
    equities_percentage = st.number_input("% of Equities", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    fixed_income_percentage = st.number_input("% of Fixed Income", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
    cash_percentage = st.number_input("% of Cash", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    cash_equivalents_percentage = st.number_input("% of Cash Equivalents", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    commodities_percentage = st.number_input("% of Commodities", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
with col10:
    real_estate_percentage = st.number_input("% of Real Estate", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cryptocurrency_percentage = st.number_input("% of Cryptocurrency", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    reits_percentage = st.number_input("% of REITs", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    alternatives_percentage = st.number_input("% of Alternatives", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cpf_percentage = st.number_input("% of CPF or Retirement", min_value=0.0, max_value=100.0, value=0.0, step=0.1)


with st.expander("Tweak Growth Rates for Each Asset Type"):
    equities_growth_rate = st.number_input("Equities Growth Rate (%)", min_value=0.0, value=10.0, step=0.1)
    fixed_income_growth_rate = st.number_input("Fixed Income Growth Rate (%)", min_value=0.0, value=4.0, step=0.1)
    cash_growth_rate = st.number_input("Cash Growth Rate (%)", min_value=0.0, value=0.0, step=0.1)
    cash_equivalents_growth_rate = st.number_input("Cash Equivalents Growth Rate (%)", min_value=0.0, value=2.0, step=0.1)
    real_estate_growth_rate = st.number_input("Real Estate Growth Rate (%)", min_value=0.0, value=4.0, step=0.1)
    cryptocurrency_growth_rate = st.number_input("Cryptocurrency Growth Rate (%)", min_value=0.0, value=15.0, step=0.1)
    commodities_growth_rate = st.number_input("Commodities Growth Rate (%)", min_value=0.0, value=3.0, step=0.1)
    reits_growth_rate = st.number_input("REITs Growth Rate (%)", min_value=0.0, value=6.0, step=0.1)
    alternatives_growth_rate = st.number_input("Alternatives Growth Rate (%)", min_value=0.0, value=8.0, step=0.1)
    cpf_growth_rate = st.number_input("CPF Growth Rate (%)", min_value=0.0, value=4.0, step=0.1)

# Ensure the total percentage is 100%
total_percentage = (
    equities_percentage + fixed_income_percentage + cash_percentage +
    cash_equivalents_percentage + real_estate_percentage + cryptocurrency_percentage +
    commodities_percentage + reits_percentage + alternatives_percentage + cpf_percentage
)
if total_percentage != 100.0:
    st.error("The total percentage of all asset types must equal 100%. Please adjust the values.")

# Custom asset fields
st.markdown("<h2 style='color: #F39373;'>Add Custom Assets</h2>", unsafe_allow_html=True)
custom_assets = []

# Display initial 3 custom asset fields
for i in range(3):
    with st.expander(f"Custom Asset {i+1}"):
        asset_name = st.text_input(f"Name of Asset {i+1}", key=f"asset_name_{i}")
        asset_allocation = st.number_input(f"Allocation (%) for {asset_name}", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"asset_allocation_{i}")
        asset_growth_rate = st.number_input(f"Growth Rate (%) for {asset_name}", min_value=0.0, value=0.0, step=0.1, key=f"asset_growth_rate_{i}")
        if asset_name and asset_allocation > 0:
            custom_assets.append((asset_name, asset_allocation, asset_growth_rate))

# Button to add more custom asset fields
if 'custom_asset_count' not in st.session_state:
    st.session_state.custom_asset_count = 3

# Display additional custom asset fields if any
for i in range(3, st.session_state.custom_asset_count):
    with st.expander(f"Custom Asset {i+1}"):
        asset_name = st.text_input(f"Name of Asset {i+1}", key=f"asset_name_{i}")
        asset_allocation = st.number_input(f"Allocation (%) for {asset_name}", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"asset_allocation_{i}")
        asset_growth_rate = st.number_input(f"Growth Rate (%) for {asset_name}", min_value=0.0, value=0.0, step=0.1, key=f"asset_growth_rate_{i}")
        if asset_name and asset_allocation > 0:
            custom_assets.append((asset_name, asset_allocation, asset_growth_rate))

# Move the button to add more custom asset fields below the last custom asset
if st.button("Add Custom Asset"):
    st.session_state.custom_asset_count += 1
# Ensure the total percentage is 100%
total_percentage = (
    equities_percentage + fixed_income_percentage + cash_percentage +
    cash_equivalents_percentage + real_estate_percentage + cryptocurrency_percentage +
    commodities_percentage + reits_percentage + alternatives_percentage + cpf_percentage +
    sum(asset_allocation for _, asset_allocation, _ in custom_assets)
)
if total_percentage != 100.0:
    st.error("The total percentage of all asset types must equal 100%. Please adjust the values.")

# Calculate the blended annual return
blended_annual_return = (
    (equities_percentage * equities_growth_rate) +
    (fixed_income_percentage * fixed_income_growth_rate) +
    (cash_percentage * cash_growth_rate) +
    (cash_equivalents_percentage * cash_equivalents_growth_rate) +
    (real_estate_percentage * real_estate_growth_rate) +
    (cryptocurrency_percentage * cryptocurrency_growth_rate) +
    (commodities_percentage * commodities_growth_rate) +
    (reits_percentage * reits_growth_rate) +
    (alternatives_percentage * alternatives_growth_rate)
)

# Add custom assets to the blended annual return calculation
for asset_name, asset_allocation, asset_growth_rate in custom_assets:
    blended_annual_return += (asset_allocation * asset_growth_rate)

# Normalize the blended annual return by the total allocation
total_allocation = (
    equities_percentage + fixed_income_percentage + cash_percentage +
    cash_equivalents_percentage + real_estate_percentage + cryptocurrency_percentage +
    commodities_percentage + reits_percentage + alternatives_percentage +
    sum(asset_allocation for _, asset_allocation, _ in custom_assets)
)

if total_allocation > 0:
    blended_annual_return /= total_allocation
else:
    blended_annual_return = 0.0

st.markdown(f"<h3 style='color: #F39373;'>Blended Annual Return on Investments: {blended_annual_return:.2f}%</h3>", unsafe_allow_html=True)
#Calculations

# Calculate FIRE number
fire_number = annual_expenses * 25

# Calculate annual savings
annual_savings = (annual_income * (savings_rate / 100))

# Adjust annual return for inflation
adjusted_annual_return = ((1 + annual_return / 100) / (1 + inflation_rate / 100)) - 1

# Calculate years to FIRE
if adjusted_annual_return > 0:
    years_to_fire = (fire_number - current_savings) / (annual_savings + (current_savings * adjusted_annual_return))
else:
    years_to_fire = float('inf')


# Streamlit

# Display results
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #F39373;'>Your FIRE Number: ${fire_number:,.2f}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #F39373;'>Years to FIRE: {years_to_fire:.1f} years</h3>", unsafe_allow_html=True)

fire_age = age + years_to_fire
st.markdown(f"<h3 style='color: #F39373;'>FIRE Age: {fire_age:.1f}</h3>", unsafe_allow_html=True)

# Calculate net worth at desired FIRE age
net_worth_at_desired_fire_age = current_savings * ((1 + adjusted_annual_return) ** (desired_fire_age - age)) + annual_savings * (((1 + adjusted_annual_return) ** (desired_fire_age - age) - 1) / adjusted_annual_return)

# Adjust net worth for CPF if FIRE age is less than 65
if fire_age < 65:
    cpf_amount = (cpf_percentage / 100) * current_savings
    net_worth_at_desired_fire_age -= cpf_amount

# Display net worth at current age, FIRE age, and desired FIRE age
st.markdown(f"<h3 style='color: #F39373;'>Net Worth at Current Age: ${current_savings:,.2f}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #F39373;'>Net Worth at FIRE Age: ${fire_number:,.2f}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #F39373;'>Net Worth at Desired FIRE Age: ${net_worth_at_desired_fire_age:,.2f}</h3>", unsafe_allow_html=True)

if fire_age <= desired_fire_age:
    st.markdown(f"<h3 style='color: #F39373;'>Congratulations! You can reach FIRE at your desired age of {desired_fire_age}.</h3>", unsafe_allow_html=True)
else:
    gap = fire_number - (current_savings + annual_savings * (desired_fire_age - age))
    st.markdown(f"<h3 style='color: #F39373;'>You cannot reach FIRE at your desired age of {desired_fire_age}. You currently have a gap of ${gap:,.2f}.</h3>", unsafe_allow_html=True)

import altair as alt
import pandas as pd

# Calculate net worth over time using adjusted annual return
years = list(range(1, int(years_to_fire) + 1))
net_worth = [current_savings]

for year in years[1:]:
    net_worth.append(net_worth[-1] * (1 + adjusted_annual_return) + annual_savings)

# Create a DataFrame for the chart
data = pd.DataFrame({
    'Year': years,
    'Net Worth': net_worth
})

# Add Age to the DataFrame
data['Age'] = [age + year for year in years]

# Create the chart
chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Age', title='Age'),
    y=alt.Y('Net Worth', title='Net Worth ($)', scale=alt.Scale(domain=[0, max(net_worth)])),
    tooltip=['Age', 'Net Worth']
).properties(
    title='Net Worth Over Time'
).interactive()

# Display the chart
st.altair_chart(chart, use_container_width=True)

#Monte Carlo Simulation

import numpy as np

# Monte Carlo Simulation parameters
num_simulations = 10000
simulation_years = int(years_to_fire)
simulated_net_worths = []

# Run Monte Carlo Simulation
for _ in range(num_simulations):
    simulated_net_worth = current_savings
    for _ in range(simulation_years):
        annual_return = np.random.normal(loc=adjusted_annual_return, scale=0.1)  # Assuming 10% standard deviation
        simulated_net_worth = simulated_net_worth * (1 + annual_return) + annual_savings
    simulated_net_worths.append(simulated_net_worth)

# Calculate the probability of exceeding the FIRE number
successful_simulations = [nw for nw in simulated_net_worths if nw > fire_number]
success_rate = len(successful_simulations) / num_simulations

# Display the results
st.markdown(f"<h3 style='color: #F39373;'>Monte Carlo Simulation Results</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #646464;'>Based on {num_simulations} simulations, there is a <strong>{success_rate * 100:.2f}%</strong> chance of exceeding your FIRE goal of ${fire_number:,.2f}.</p>", unsafe_allow_html=True)

# Create a DataFrame for the simulation results
simulation_data = pd.DataFrame({
    'Simulation': range(1, num_simulations + 1),
    'Net Worth': simulated_net_worths
})

# Monte Carlo Simulation Chart
simulation_chart = alt.Chart(simulation_data).mark_bar(size=10).encode(
    x=alt.X('Net Worth:Q', bin=alt.Bin(maxbins=50), title='Net Worth ($)'),
    y=alt.Y('count()', title='Frequency'),
    color=alt.Color('Net Worth:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['Net Worth', 'count()']
).properties(
    title='Monte Carlo Simulation Results'
).interactive()

# Display the chart
st.altair_chart(simulation_chart, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(f"<h3 style='color: #F39373;'>AI Suggestions: ${fire_number:,.2f}</h3>", unsafe_allow_html=True)

st.markdown(f"<p style='color: #646464;'>Get suggestions around how to bridge the gap to your FIRE number if there is a gap.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #646464;'>Or get suggestions around how to de-risk yourself - you are already on a great path!</p>", unsafe_allow_html=True)

#AI Suggestions
if st.button("Get AI Suggestions to Bridge Gap"):
    if fire_age > desired_fire_age:
        st.markdown(f"<h3 style='color: #F39373;'>AI Suggestions to Bridge the Gap:</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #646464;'>1. Increase your annual savings by ${gap / (desired_fire_age - age):,.2f}.</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #646464;'>2. Consider investing in higher return assets to achieve an adjusted annual return higher than {adjusted_annual_return * 100:.2f}%.</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #646464;'>3. Reduce your current expenses to save more towards your FIRE goal.</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #646464;'>4. Explore additional income streams to boost your savings.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color: #F39373;'>No gap to bridge! You are on track to reach FIRE at your desired age of {desired_fire_age}.</h3>", unsafe_allow_html=True)

if st.button("Get AI Suggestions to De-Risk Portfolio"):
    st.markdown(f"<h3 style='color: #F39373;'>AI Suggestions to De-Risk Portfolio:</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #646464;'>1. Diversify your investments across different asset classes to reduce risk.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #646464;'>2. Consider shifting a portion of your portfolio to more stable, lower-risk investments such as bonds or index funds.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #646464;'>3. Regularly rebalance your portfolio to maintain your desired risk level.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #646464;'>4. Keep an emergency fund to cover unexpected expenses without needing to liquidate investments.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #646464;'>5. Stay informed about market trends and economic indicators to make timely adjustments to your portfolio.</p>", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)




#add in the LLM element where you could get suggestions


#additional chat below that basically runs GPT or another model where you could ask questions and the LLM will provide an answer back