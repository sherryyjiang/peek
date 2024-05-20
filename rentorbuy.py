#Imports
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np  # Added this line
import seaborn as sns
import pandas as pd
import altair as alt


#Heading
st.markdown("<h1 style='color: #F39373; padding-bottom: 30px;'>🏠 Rent vs. Buy Calculator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #F8F6F4; padding: 10px; border-radius: 5px;'>
        <p style='color: #000000; font-size: 16px; font-weight: bold;'>Welcome to Sherry's no-frills Rent vs. Buy calculator</p>
        <p style='color: #000000;'>
            Use this FREE tool to figure out the total costs, including opportunity costs, between renting and buying property. Easy to input, easy to calculate. No numbers crunching or giant spreadsheet templates necessary.<br><br>
            You can calculate through two ways:
            <br>1. Simply upload your CSV file with the necessary data OR
            <br>2. Input the necessary data yourself</br></br>
            For CSV uploads, please make sure that the columns are labeled with the exact wording of the inputs below: "Home Price," "Monthly Rent," "Stay Duration," "Mortgage Rate," "Down Payment," "Mortgage Term.
            "
            <br><br>
            For any questions or feedback, don't hesitate to reach out to sherry@peek.money!
            <br><br>
            This product was created by Sherry from the Peek team. If you like what you see, and want more of it, check out <a href='https://peek.money' target='_blank'>peek.money</a>!
    </div>
""", unsafe_allow_html=True)


#Upload CSV File
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #F39373;'>Upload a CSV file</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        if data.empty:
            st.error("The uploaded CSV file is empty. Please upload a valid file.")
        else:
            st.success("CSV file uploaded successfully!")
            st.dataframe(data.style.set_properties(**{'background-color': '#F8F6F4', 'color': '#000000'}))
    except pd.errors.EmptyDataError:
        st.error("No columns to parse from file. Please upload a valid CSV file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

#Base calculations for rent vs. buy
def calculate_rent_vs_buy(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost):
    # Step 1: Calculate initial costs
    initial_rent_cost = monthly_rent
    initial_buy_cost = down_payment * home_price + cost_of_buying * home_price

    # Step 2: Calculate recurring costs
    annual_recurring_rent = monthly_rent * 12
    total_recurring_rent = annual_recurring_rent * ((1 - (1 + rental_growth_rate) ** stay_duration) / (1 - (1 + rental_growth_rate)))

    annual_mortgage_payment = (home_price * (1 - down_payment)) * (mortgage_rate / (1 - (1 + mortgage_rate) ** -mortgage_term))
    annual_maintenance_cost = maintenance_cost * home_price
    annual_recurring_buy = annual_mortgage_payment + annual_maintenance_cost
    total_recurring_buy = annual_recurring_buy * stay_duration

    # Step 3: Calculate opportunity costs
    future_value_rent = annual_recurring_rent * (((1 + investment_return) ** stay_duration - (1 + rental_growth_rate) ** stay_duration) / (investment_return - rental_growth_rate))
    future_value_buy_initial = initial_buy_cost * (1 + investment_return) ** stay_duration
    future_value_buy_recurring = (annual_mortgage_payment + annual_maintenance_cost) * (((1 + investment_return) ** stay_duration - 1) / investment_return)

    # Annualize opportunity costs
    annual_future_value_rent = future_value_rent / stay_duration
    annual_future_value_buy_recurring = future_value_buy_recurring / stay_duration

    # Step 4: Calculate net proceeds
    future_home_price = home_price * (1 + home_price_growth_rate) ** stay_duration
    net_proceeds = future_home_price - cost_of_selling * future_home_price

    # Step 5: Calculate total costs
    total_renting_cost = initial_rent_cost + total_recurring_rent + future_value_rent
    total_buying_cost = initial_buy_cost + total_recurring_buy + future_value_buy_initial + future_value_buy_recurring - net_proceeds

    return total_renting_cost, total_buying_cost, initial_rent_cost, initial_buy_cost, annual_future_value_rent, annual_future_value_buy_recurring, net_proceeds, annual_mortgage_payment, annual_maintenance_cost, annual_recurring_rent, total_recurring_rent, annual_recurring_buy, total_recurring_buy, future_value_buy_initial

# Streamlit - Manual Inputs

st.markdown("<h3 style='color: #F39373; padding-bottom: 40px;'>Enter Details Manually</h3>", unsafe_allow_html=True)

if uploaded_file is not None and not data.empty:
    # Extract values from CSV
    home_price = data['Home Price'].iloc[0]
    monthly_rent = data['Monthly Rent'].iloc[0]
    stay_duration = int(data['Stay Duration'].iloc[0])
    mortgage_rate = data['Mortgage Rate'].iloc[0] / 100
    down_payment = data['Down Payment'].iloc[0] / 100
    mortgage_term = int(data['Mortgage Term'].iloc[0])

else:
    col1, col2 = st.columns(2)
    with col1:
        home_price = st.number_input("Home Price", value=1150000, key="home_price", format="%d", help="Enter the home price")
    with col2:
        monthly_rent = st.number_input("Monthly Rent", value=4300, key="monthly_rent", format="%d", help="Enter the monthly rent")
    
    col3, col4 = st.columns(2)
    with col3:
        stay_duration = int(st.number_input("Stay Duration (years)", value=30, key="stay_duration", format="%d", help="Enter the stay duration in years"))
    with col4:
        mortgage_rate = st.number_input("Mortgage Rate (%)", value=4, key="mortgage_rate", format="%d", help="Enter the mortgage rate in percentage") / 100
    
    col5, col6 = st.columns(2)
    with col5:
        down_payment = st.number_input("Down Payment (%)", value=25, key="down_payment", format="%d", help="Enter the down payment in percentage") / 100
    with col6:
        mortgage_term = int(st.number_input("Mortgage Term (years)", value=30, key="mortgage_term", format="%d", help="Enter the mortgage term in years"))


# Constants
with st.expander("Adjust Other Default Assumptions", expanded=False):
    investment_return = st.slider('Investment Return (%)', 0.0, 20.0, 9.0) / 100
    home_price_growth_rate = st.slider('Home Price Growth Rate (%)', 0.0, 10.0, 4.0) / 100
    rental_growth_rate = st.slider('Rental Growth Rate (%)', 0.0, 10.0, 3.0) / 100
    cost_of_buying = st.slider('Cost of Buying (%)', 0.0, 10.0, 4.5) / 100
    cost_of_selling = st.slider('Cost of Selling (%)', 0.0, 10.0, 8.0) / 100
    maintenance_cost = st.slider('Maintenance Cost (inclusive of tax, insurance, servicing) (%)', 0.0, 10.0, 2.0) / 100

st.markdown("<hr>", unsafe_allow_html=True)

# Streamlit - Decision Calculator

st.markdown("<h3 style='color: #F39373; padding-bottom: 30px;'>Calculations</h3>", unsafe_allow_html=True)
st.markdown("""
After uploading or manually entering your details, feel free to tap each of the buttons below to calculate your results.

- **Calculate Decision**: Calculate total rent vs. buy costs, including opportunity cost
- **Calculate Cash Flow**: See the liquid cash flows out for each decision
- **Mortgage Rate - Breakeven**: See the mortgage % that you need in order for renting and buying to cost the same
- **Calculate Opportunity Cost Details**: Breakdown of how each year's costs contribute to overall opportunity cost. Keeping in mind the power of compounding.
""", unsafe_allow_html=True)
st.markdown("<div style='padding-bottom: 30px;'></div>", unsafe_allow_html=True)

if st.button("Calculate Decision"):
    results = calculate_rent_vs_buy(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost)
    total_renting_cost, total_buying_cost, initial_rent_cost, initial_buy_cost, annual_future_value_rent, annual_future_value_buy_recurring, net_proceeds, annual_mortgage_payment, annual_maintenance_cost, annual_recurring_rent, total_recurring_rent, annual_recurring_buy, total_recurring_buy, future_value_buy_initial = results
    
    st.write(f"<p style='color: #646464;'><b>Total Renting Cost: ${total_renting_cost:,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Total Buying Cost: ${total_buying_cost:,.2f}</b></p>", unsafe_allow_html=True)

    
    if total_renting_cost < total_buying_cost:
        savings = total_buying_cost - total_renting_cost
        st.write("<p style='color: #F39373; font-size: 18px;'><b>Renting is more cost-effective than buying.</b></p>", unsafe_allow_html=True)
        st.write(f"<p style='color: #F39373; font-size: 18px;'><b>You would save ${savings:,.2f} by renting.</b></p>", unsafe_allow_html=True)
    else:
        savings = total_renting_cost - total_buying_cost
        st.write("<p style='color: #F39373; font-size: 18px;'><b>Buying is more cost-effective than renting.</b></p>", unsafe_allow_html=True)
        st.write(f"<p style='color: #F39373; font-size: 18px;'><b>You would save ${savings:,.2f} by buying.</b></p>", unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)
    

    st.markdown("<h4 style='color: #646464; padding-bottom: 20px;'>Breakdown of Total Renting Cost</h4>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Initial Renting Cost: ${initial_rent_cost:,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Recurring Renting Cost: ${total_recurring_rent:,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Renting Opportunity Cost: ${annual_future_value_rent * stay_duration:,.2f}</b></p>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #646464; padding-bottom: 20px;'>Breakdown of Total Buying Cost</h4>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Initial Buying Cost: ${initial_buy_cost:,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Recurring Buying Cost: ${total_recurring_buy:,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464;'><b>Buying Opportunity Cost: ${(future_value_buy_initial + annual_future_value_buy_recurring * stay_duration):,.2f}</b></p>", unsafe_allow_html=True)
    st.write(f"<p style='color: #646464; padding-bottom: 40px;'><b>Buying Net Proceeds: ${net_proceeds * (-1):,.2f}</b> <i>(This is the amount you get when you sell the house at the end of {stay_duration} years, which you subtract out of the total cost for buying)</i></p>", unsafe_allow_html=True)

    # Line chart for annualized costs over time
    years = list(range(1, stay_duration + 1))
    rent_costs = []
    buy_costs = []
    
    annualized_rent_cost = total_renting_cost / stay_duration
    annualized_buy_cost = total_buying_cost / stay_duration
    
    for year in years:
        rent_cost = annualized_rent_cost * year
        buy_cost = annualized_buy_cost * year
        
        rent_costs.append(rent_cost)
        buy_costs.append(buy_cost)
    
    # Create a DataFrame for Altair
    data = pd.DataFrame({
        'Year': years,
        'Renting Cost': rent_costs,
        'Buying Cost': buy_costs
    })

    # Melt the DataFrame for Altair
    data_melted = data.melt('Year', var_name='Cost Type', value_name='Cost')

    # Create the line plot using Altair
    line_chart = alt.Chart(data_melted).mark_line(point=True).encode(
        x=alt.X('Year:Q', title='Years'),
        y=alt.Y('Cost:Q', title='Annualized Cost ($)'),
        color='Cost Type:N',
        tooltip=['Year:Q', 'Cost:Q', 'Cost Type:N']
    ).properties(
        title=alt.TitleParams(
            text='Annualized Rent vs. Buy Costs Over Time',
            fontSize=20,  # h3 size
            anchor='start'
        ),
        width=600,
        height=400
    )
    

    # Add data labels for every 5 years and the final year
    text_labels = alt.Chart(data_melted).mark_text(align='right', dx=-5, dy=-5).encode(
        x='Year:Q',
        y='Cost:Q',
        text=alt.Text('Cost:Q', format='$,.0f'),
        color='Cost Type:N'
    ).transform_filter(
        (alt.datum.Year % 5 == 0) | (alt.datum.Year == stay_duration)
    )

    # Combine the line chart and text labels
    final_chart = line_chart + text_labels

    st.altair_chart(final_chart, use_container_width=True)


# Breakeven

def mortgage_break_even(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost):
    low, high = 0, 0.2  # Searching within 0% to 20% mortgage rate
    while high - low > 0.0001:
        mid = (high + low) / 2
        total_renting_cost, total_buying_cost, *_ = calculate_rent_vs_buy(home_price, monthly_rent, stay_duration, mid, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost)  # Pass all arguments here
        if total_renting_cost > total_buying_cost:
            low = mid
        else:
            high = mid
    break_even_rate = (high + low) / 2
    return break_even_rate * 100  # Convert to percentage

def calculate_costs_over_mortgage_rates(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost):
    rates = np.linspace(0.005, 0.06, 100)  # Mortgage rates from 0.5% to 6%
    renting_costs = []
    buying_costs = []

    for rate in rates:
        total_renting_cost, total_buying_cost, *_ = calculate_rent_vs_buy(home_price, monthly_rent, stay_duration, rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost)  # Pass all arguments here
        renting_costs.append(total_renting_cost)
        buying_costs.append(total_buying_cost)

    return rates, renting_costs, buying_costs

if st.button("Mortgage Rate - Breakeven"):
    break_even_rate = mortgage_break_even(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost)  # Pass all arguments here
    st.write(f"<p style='color: #646464;'><b>Break-even Mortgage Rate: {break_even_rate:.2f}%</b></p>", unsafe_allow_html=True)
    st.write("That means you break even on your buying and renting cost at this mortgage rate.")
    st.write(f"Your current mortgage rate is {mortgage_rate*100:.2f}%")
    rates, renting_costs, buying_costs = calculate_costs_over_mortgage_rates(home_price, monthly_rent, stay_duration, mortgage_rate, down_payment, mortgage_term, investment_return, home_price_growth_rate, rental_growth_rate, cost_of_buying, cost_of_selling, maintenance_cost)  # Pass all arguments here
    
    data = pd.DataFrame({
        'Mortgage Rate (%)': rates * 100,  # Convert to percentage and update column name for clarity
        'Renting Cost ($)': renting_costs,  # Update column name for clarity
        'Buying Cost ($)': buying_costs  # Update column name for clarity
    }).melt('Mortgage Rate (%)', var_name='Cost Type', value_name='Total Cost ($)')  # Update parameters to match column name changes
    
    break_even_chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X('Mortgage Rate (%):Q', title='Mortgage Rate (%)'),  # Ensure axis title matches updated column name
        y=alt.Y('Total Cost ($):Q', title='Total Cost ($)'),  # Ensure axis title matches updated column name
        color=alt.Color('Cost Type:N', legend=alt.Legend(title="Cost Type")),  # Add legend title for clarity
        tooltip=['Mortgage Rate (%):Q', 'Total Cost ($):Q', 'Cost Type:N']  # Ensure tooltip labels match updated column names
    ).properties(
        title='Renting vs. Buying Costs Over Different Mortgage Rates',
        width=600,
        height=400
    )
    
    st.altair_chart(break_even_chart, use_container_width=True)