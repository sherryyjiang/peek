# Imports
import streamlit as st

# Heading
st.markdown("<h1 style='color: #F39373; padding-bottom: 30px;'>🔥 FIRE (Financial Independence, Retire Early) Calculator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #F8F6F4; padding: 10px; border-radius: 5px; margin-bottom: 40px;'>
        <p style='color: #000000; font-size: 16px; font-weight: bold;'>Welcome to Sherry's FIRE Calculator</p>
        <p style='color: #000000;'>
            Use this tool to estimate how much you need to save to achieve financial independence and retire early. Simply input your annual expenses, current savings, expected annual return on investments, annual income, and savings rate.
            <br><br>
            There are many other FIRE calculators out there, but what makes this one a bit different is it gives you:
            <br>
            a) More granular options for specific asset classes
            <br>
            b) FREE simulation of potential outcomes (using Monte Carlo method)
            <br>
            c) Better lens for the "Barbell FIRE" method
            <br><br>
            What is Barbell FIRE            
            <br><br>
            Barbell FIRE is a school of thought within FIRE that balances low-risk, stable investments with high-risk, high-reward investments. The idea is to divide your portfolio into two main parts: stable assets (ETFs, bonds, etc.) and growth assets (e.g., individual tech stocks, crypto, angel investing). In the best case top 10-20% scenarios, you might be able to reach your goal sooner. In the bottom 10% of the scenarios, your stable assets still ground your portfolio.
            <br><br>
            For any questions or feedback, don't hesitate to reach out to sherry@peek.money!
            <br><br>
            This product was created by Sherry from the Peek team. If you like what you see, and want more of it, check out peek.money!
    </div>
""", unsafe_allow_html=True)
# Streamlit: Input fields
st.markdown("<h2 style='color: #F39373; padding-bottom: 40px;'>Basic Inputs</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Current Age", min_value=0.0, value=35.0, step=0.1, format="%.1f")
    annual_expenses = st.number_input("Annual Expenses at Retirement ($)", min_value=0, value=80000, step=1000)
    current_savings = st.number_input("Current Savings ($)", min_value=0, value=500000, step=1000)
    annual_income = st.number_input("Annual Income ($) - assumed 3% growth rate", min_value=0, value=80000, step=1000)
with col2:
    desired_fire_age = st.number_input("Desired FIRE Age", min_value=0.0, value=55.0, step=0.1, format="%.1f")
    savings_rate = st.number_input("Savings Rate (%)", min_value=0.0, value=40.0, step=0.1)
    inflation_rate = st.number_input("Inflation Rate (%)", min_value=0.0, value=3.0, step=0.1)
    

# Streamlit: Advanced options for Expected Annual Return on Investments (%)
with st.sidebar:
    st.markdown("<h2 style='color: #F39373; padding-bottom: 40px;'>Expected Annual Return on Investments (%)</h2>", unsafe_allow_html=True)
    equities_percentage = st.number_input("% of Equities", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    fixed_income_percentage = st.number_input("% of Fixed Income", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
    cash_percentage = st.number_input("% of Cash", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    cash_equivalents_percentage = st.number_input("% of Cash Equivalents", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    commodities_percentage = st.number_input("% of Commodities", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    real_estate_percentage = st.number_input("% of Real Estate", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cryptocurrency_percentage = st.number_input("% of Cryptocurrency", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    reits_percentage = st.number_input("% of REITs", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    alternatives_percentage = st.number_input("% of Alternatives", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cpf_percentage = st.number_input("% of CPF or Retirement", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

    st.markdown("<h4 style='color: #F39373; padding-top: 20px; padding-bottom: 20px;'>Adjust Default Growth Rates for Each Asset Type</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: medium; font-style: italic;'>Adjust these growth rate estimates if you would like to use different assumptions</p>", unsafe_allow_html=True)
    with st.expander("Adjust Growth Rates for Each Asset Type"):
        equities_growth_rate = st.slider("Equities Growth Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        fixed_income_growth_rate = st.slider("Fixed Income Growth Rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.1)
        cash_growth_rate = st.slider("Cash Growth Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        cash_equivalents_growth_rate = st.slider("Cash Equivalents Growth Rate (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
        real_estate_growth_rate = st.slider("Real Estate Growth Rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.1)
        cryptocurrency_growth_rate = st.slider("Cryptocurrency Growth Rate (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.1)
        commodities_growth_rate = st.slider("Commodities Growth Rate (%)", min_value=0.0, max_value=100.0, value=3.0, step=0.1)
        reits_growth_rate = st.slider("REITs Growth Rate (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.1)
        alternatives_growth_rate = st.slider("Alternatives Growth Rate (%)", min_value=0.0, max_value=100.0, value=8.0, step=0.1)
        cpf_growth_rate = st.slider("CPF Growth Rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.1)

# Ensure the total percentage is 100%
total_percentage = (
    equities_percentage + fixed_income_percentage + cash_percentage +
    cash_equivalents_percentage + real_estate_percentage + cryptocurrency_percentage +
    commodities_percentage + reits_percentage + alternatives_percentage + cpf_percentage
)
if total_percentage != 100.0:
    st.error("The total percentage of all asset types must equal 100%. Please adjust the values.")

# Custom asset fields
with st.sidebar:
    st.markdown("<h2 style='color: #F39373;'>Add Custom Assets</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: medium; font-style: italic;'>Add specific assets here for more granular assumptions. For instance, if you hold 10% of your portfolio in Apple stock. Or hold 5% of your portfolio in Solana.</p>", unsafe_allow_html=True)
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

st.markdown(f"""
<div style='padding-top: 10px; text-align: left;'>
    <h4 style='color: gray;'>Annual Return on Investments: {blended_annual_return:.2f}% 
        <span style='cursor: pointer;' title='The return is calculated based on a blended average'>ℹ️</span>
    </h4>
    <p style='font-size: 16px; color: gray;'>This calculation is based on expected annual return on investments. You can adjust the assumptions from the default values provided on the left side panel.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
def calculate_fire_plan(age, desired_fire_age, annual_expenses, current_savings, annual_return, annual_income, savings_rate, inflation_rate):
    # Calculate FIRE number
    fire_number = 25 * annual_expenses
    
    # Calculate real rate of return
    real_rate_of_return = (annual_return - inflation_rate) / 100
    
    # Calculate current savings growth
    current_savings_growth = current_savings * (1 + real_rate_of_return) ** (desired_fire_age - age)
    
    # Calculate annual savings amount
    annual_savings = annual_income * (savings_rate / 100)
    
    # Calculate annual savings growth using future value of an annuity formula
    n = desired_fire_age - age
    annual_savings_growth = annual_savings * (((1 + real_rate_of_return) ** n - 1) / real_rate_of_return)
    
    # Calculate actual savings at desired FIRE age
    actual_savings_at_desired_fire_age = current_savings_growth + annual_savings_growth
    
    # Compare actual savings to FIRE number
    if actual_savings_at_desired_fire_age >= fire_number:
        can_retire = True
        gap = 0
        additional_years_needed = 0
    else:
        can_retire = False
        gap = fire_number - actual_savings_at_desired_fire_age
        additional_years_needed = 0
        while actual_savings_at_desired_fire_age < fire_number:
            additional_years_needed += 1
            actual_savings_at_desired_fire_age += annual_savings * (1 + real_rate_of_return) ** additional_years_needed
        # Reset actual_savings_at_desired_fire_age to the correct value for printing
        actual_savings_at_desired_fire_age = current_savings_growth + annual_savings_growth
    

    st.markdown("<h2 style='color: #F39373;'>Results</h2>", unsafe_allow_html=True)
    
    # Prepare the scratchpad
    scratchpad = f"""
    <scratchpad style='font-size: 18px;'>
    FIRE number: ${fire_number:,.2f}<br>
    Actual savings at desired FIRE age: ${actual_savings_at_desired_fire_age:,.2f}<br>
    </scratchpad>
    """
    scratchpad += "<br><br>"
    
    return scratchpad, actual_savings_at_desired_fire_age, fire_number, can_retire, current_savings_growth, annual_savings_growth, real_rate_of_return, annual_savings

# Example usage with Streamlit inputs
scratchpad_and_answer, actual_savings_at_desired_fire_age, fire_number, can_retire, current_savings_growth, annual_savings_growth, real_rate_of_return, annual_savings = calculate_fire_plan(
    age, desired_fire_age, annual_expenses, current_savings, 
    blended_annual_return, annual_income, savings_rate, inflation_rate
)
st.markdown(scratchpad_and_answer, unsafe_allow_html=True)

if actual_savings_at_desired_fire_age >= fire_number:
    st.markdown(f"<h3 style='color: green;'>Congratulations! You will be able to FIRE by {desired_fire_age}.</h3>", unsafe_allow_html=True)
else:
    gap = fire_number - actual_savings_at_desired_fire_age
    st.markdown(f"<h3 style='color: red;'>You currently have a gap of ${gap:,.2f} to reach your FIRE number.</h3>", unsafe_allow_html=True)

if not can_retire:
    additional_years_needed = 0
    while actual_savings_at_desired_fire_age < fire_number:
        additional_years_needed += 1
        actual_savings_at_desired_fire_age += annual_savings * (1 + real_rate_of_return) ** additional_years_needed
    fire_age = age + additional_years_needed
    # st.markdown(f"<h3 style='color: red;'>You will need an additional {additional_years_needed} years to reach your FIRE number. You will be {fire_age} years old when you reach FIRE.</h3>", unsafe_allow_html=True)


#Add in some basic charts

import altair as alt
import pandas as pd

# Create a DataFrame for the actual savings trajectory
actual_savings_data = {
    'Age': list(range(int(age), int(desired_fire_age) + 1)),
    'Savings': [
        current_savings * (1 + real_rate_of_return) ** i + 
        annual_savings * (((1 + real_rate_of_return) ** i - 1) / real_rate_of_return)
        for i in range(int(desired_fire_age) - int(age) + 1)
    ]
}
actual_savings_df = pd.DataFrame(actual_savings_data)

# Calculate the required growth rate to hit the FIRE number by the desired FIRE age
required_growth_rate = (fire_number / current_savings) ** (1 / (desired_fire_age - age)) - 1

# Create a DataFrame for the required savings trajectory
required_savings_data = {
    'Age': list(range(int(age), int(desired_fire_age) + 1)),
    'Savings': [current_savings * (1 + required_growth_rate) ** i for i in range(int(desired_fire_age) - int(age) + 1)]
}

required_savings_df = pd.DataFrame(required_savings_data)

# Create the actual savings chart
# Ensure the 'Age' field is treated as an ordinal scale to avoid gaps for odd-numbered years
actual_savings_chart = alt.Chart(actual_savings_df).mark_line(color='blue').encode(
    x=alt.X('Age:O', title='Age'),  # Treat 'Age' as an ordinal scale
    y=alt.Y('Savings', scale=alt.Scale(domain=[current_savings, max(actual_savings_df['Savings'].max(), required_savings_df['Savings'].max())]))
).properties(
    title='Actual Savings Trajectory'
)

# Create the required savings chart
required_savings_chart = alt.Chart(required_savings_df).mark_line(color='red', strokeDash=[5, 5]).encode(
    x=alt.X('Age:O', title='Age'),  # Treat 'Age' as an ordinal scale
    y='Savings'
).properties(
    title='Required Savings Trajectory to Reach FIRE Number'
)

# Combine both charts
combined_chart = alt.layer(actual_savings_chart, required_savings_chart).resolve_scale(
    y='shared'
)

# Display the chart in Streamlit with padding
st.markdown("<div style='padding-top: 40px;'></div>", unsafe_allow_html=True)
st.altair_chart(combined_chart, use_container_width=True)


# Sensitivity Analysis Heading
st.markdown("<h2 style='color: #F39373; padding-top: 20px;'>What If Scenarios</h2>", unsafe_allow_html=True)
st.markdown("""
    <p style='color: #000000; font-size: 16px;'>
        The charts below show how your savings at your desired FIRE age changes with different savings rate % and different annual return rates. 
        They are meant to help you figure out what potential adjustments you could make.
    </p>
""", unsafe_allow_html=True)

# Create a DataFrame to store the savings at desired FIRE age for different savings rates
savings_rates = list(range(10, 85, 5))
savings_at_fire_age = []

for rate in savings_rates:
    annual_savings_rate = rate / 100 * annual_income
    savings = current_savings
    for i in range(int(desired_fire_age) - int(age) + 1):
        savings = savings * (1 + real_rate_of_return) + annual_savings_rate
    savings_at_fire_age.append(savings)

# Ensure the savings calculated at the FIRE age match with the calculations above
savings_at_fire_age_corrected = [
    current_savings * (1 + real_rate_of_return) ** (desired_fire_age - age) + 
    (rate / 100 * annual_income) * (((1 + real_rate_of_return) ** (desired_fire_age - age) - 1) / real_rate_of_return)
    for rate in savings_rates
]

savings_rate_data = {
    'Savings Rate (%)': [f"{rate}%" for rate in savings_rates],
    'Savings at FIRE Age': [f"${savings:,.0f}" for savings in savings_at_fire_age_corrected]
}

savings_rate_df = pd.DataFrame(savings_rate_data)

# Display the table in Streamlit
st.markdown("**<h4>Savings Based on Savings Rate</h3>**", unsafe_allow_html=True)
st.dataframe(savings_rate_df.style.set_properties(**{'font-size': '14pt', 'text-align': 'left'}), height=400, width=600)  # Set width to 3/4 of 800

# Create a range of annual returns from 3.0% to 12.0%, incrementing by 0.5%
annual_return_rates = [round(x * 0.5, 1) for x in range(6, 25)]

# Initialize lists to store the results
adjusted_annual_returns = []
savings_at_fire_age = []

# Pull the inflation_rate from the inputs above
inflation_rate = st.session_state.get('inflation_rate', 3.0)

# Calculate the savings projections for each annual return rate
for annual_return in annual_return_rates:
    adjusted_annual_return = annual_return - inflation_rate
    current_savings_growth = current_savings * ((1 + adjusted_annual_return / 100) ** (desired_fire_age - age))
    
    # Avoid division by zero by checking if adjusted_annual_return is zero
    if adjusted_annual_return != 0:
        annual_savings_growth = annual_savings * (((1 + adjusted_annual_return / 100) ** (desired_fire_age - age) - 1) / (adjusted_annual_return / 100))
    else:
        annual_savings_growth = annual_savings * (desired_fire_age - age)  # Simple linear growth if return is zero
    
    total_savings_at_fire_age = round(current_savings_growth + annual_savings_growth)
    
    savings_at_fire_age.append(total_savings_at_fire_age)

# Create a DataFrame to store the results
sensitivity_data = {
    'Annual Return Rate (%)': [f"{rate:.1f}" for rate in annual_return_rates],  # Show 1 decimal place
    'Savings at FIRE Age ($)': [f"${savings:,.0f}" for savings in savings_at_fire_age]  # Format with commas and $ sign
}
sensitivity_df = pd.DataFrame(sensitivity_data)

# Display the table in Streamlit
st.markdown("**<h4>Savings Based on Annual Return Rate</h4>**", unsafe_allow_html=True)
st.dataframe(sensitivity_df.style.set_properties(**{'font-size': '14pt', 'text-align': 'left'}), height=400, width=600)  # Set width to 3/4 of 800
# Provide suggestions based on risk tolerance
st.markdown("### Suggestions Based on Risk Tolerance")

st.markdown("""
If you are **risk-averse**, a better approach would be to manage to a certain savings rate to maintain your FIRE goal or reach your FIRE goal. This means focusing on consistent savings and possibly opting for more stable, lower-risk investments. This could be suitable for people who really want to get more certainty around their FIRE plan.

<div style='height: 25px;'></div>

If you are **risk-tolerant**, you could consider a blend of managing a savings rate percentage and looking at higher growth investments. This approach might involve investing in assets with higher potential returns but also higher risks. Just make sure to do your own research and understand the risks in the market.

This strategy could also be suitable for people who want to attempt FIRE earlier in their life with more aggressive investments, but are okay if they are not able to hit their goal with 100% certainty, and have more years of adjusting financial choices and employment to make up for any variance in the market.
""", unsafe_allow_html=True)

# Add a divider
st.markdown("<hr>", unsafe_allow_html=True)


#Monte Carlo simulations
st.markdown("<h2 style='color: #F39373;'>Optional: Simulations</h2>", unsafe_allow_html=True)

st.markdown("""
Monte Carlo simulations are like running thousands of different possible future scenarios to see how your savings and investments might grow or shrink over time. It's like trying out lots of different "what if" stories to see how likely it is that you'll reach your financial goals and be able to retire early.

<br>

This calculator allows you to also simulate outcomes where you add additional inputs of stable assets and growth assets with different risk and return profiles. For example, if you are following the Barbell FIRE strategy, you could see the different range of outcomes.

<br>
""", unsafe_allow_html=True)


import numpy as np
import altair as alt

# Gather user inputs
col1, col2 = st.columns(2)

with col1:
    stable_assets_percentage = st.number_input("% of Stable Assets", min_value=0.0, max_value=100.0, value=85.0, step=0.1, key="stable_assets_percentage")
    stable_annual_return = st.number_input("Stable Assets Annual Return (%)", min_value=0.0, value=7.0, step=0.1, key="stable_annual_return")
    stable_standard_deviation = st.number_input("Stable Assets Standard Deviation (%)", min_value=0.0, value=10.0, step=0.1, key="stable_standard_deviation")
    current_age = age
    current_savings = current_savings

with col2:
    growth_assets_percentage = st.number_input("% of Growth Assets", min_value=0.0, max_value=100.0, value=15.0, step=0.1, key="growth_assets_percentage")
    growth_annual_return = st.number_input("Growth Assets Annual Return (%)", min_value=0.0, value=15.0, step=0.1, key="growth_annual_return")
    growth_standard_deviation = st.number_input("Growth Assets Standard Deviation (%)", min_value=0.0, value=30.0, step=0.1, key="growth_standard_deviation")
    annual_savings = annual_income * (savings_rate / 100)
 
# Add line breaks for better spacing
st.markdown("<br><br>", unsafe_allow_html=True)



# Monte Carlo simulation parameters
num_trials = 1000
years = int(desired_fire_age - current_age)
inflation_rate = inflation_rate / 100

# Print the number of years until desired FIRE age in Streamlit
st.markdown(f"<h3 style='font-size: 18px;'>Years until desired FIRE age: {years}</h3>", unsafe_allow_html=True)


# Run Monte Carlo simulation
results = []

for _ in range(num_trials):
    total_savings = current_savings
    savings_over_time = []

    for year in range(years):
        stable_return = np.random.normal(stable_annual_return / 100, stable_standard_deviation / 100)
        growth_return = np.random.normal(growth_annual_return / 100, growth_standard_deviation / 100)
        adjusted_annual_return = (stable_assets_percentage / 100 * stable_return) + (growth_assets_percentage / 100 * growth_return) - inflation_rate
        total_savings = total_savings * (1 + adjusted_annual_return) + annual_savings
        savings_over_time.append(total_savings)

    results.append(savings_over_time)

# Calculate percentiles
results = np.array(results)
percentiles = np.percentile(results, [10, 50, 90], axis=0)

# Create DataFrame for plotting

years_range = list(range(int(current_age) + 1, int(desired_fire_age) + 1))
percentile_df = pd.DataFrame({
    'Year': years_range * 3,
    'Total Savings': np.concatenate([percentiles[0], percentiles[1], percentiles[2]]),
    'Percentile': ['10th'] * years + ['50th'] * years + ['90th'] * years
})

# Plot the results using Altair
chart = alt.Chart(percentile_df).mark_line().encode(
    x=alt.X('Year', title='Year', scale=alt.Scale(domain=[int(current_age) + 1, int(desired_fire_age)])),
    y=alt.Y('Total Savings', title='Total Savings'),
    color=alt.Color('Percentile', legend=alt.Legend(orient='bottom'))
).properties(
    title='Monte Carlo Simulation of Retirement Savings',
    width=800,  # Increase the width of the chart
    height=400  # Increase the height of the chart
)

st.altair_chart(chart, use_container_width=True)

# Display final savings percentiles at desired FIRE age
st.markdown(f"<h3 style='font-size: 18px;'>Projected Savings at Age {desired_fire_age}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 18px;'>10th Percentile: ${percentiles[0, -1]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 18px;'>50th Percentile (Median): ${percentiles[1, -1]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 18px;'>90th Percentile: ${percentiles[2, -1]:,.2f}</p>", unsafe_allow_html=True)
st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)

# Reflection
st.markdown(f"""
<p style='font-size: 16px;'>The range of outcomes between the 10th and 90th percentiles shows the level of uncertainty in the projections, given the asset allocation and assumptions provided.</p>
<ul style='font-size: 16px;'>
    <li>The 10th percentile outcome represents a more worst-case scenario, where returns are lower than average.</li>
    <li>The 90th percentile outcome represents a more best-case scenario, where returns are higher than average.</li>
</ul>
""", unsafe_allow_html=True)