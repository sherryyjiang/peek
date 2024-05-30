#debtrepayment 

import streamlit as st

st.title("Debt Repayment Calculator")

# Basic Inputs
col1, col2 = st.columns(2)

with col1:
    total_debt = st.number_input("Total Debt ($)", min_value=0.0, value=50000.0, step=1000.0)
    annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    investment_return_rate = st.number_input("Annual Investment Return Rate (%)", min_value=0.0, max_value=100.0, value=7.0, step=0.1)

with col2:
    monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, value=1000.0, step=100.0)

# Calculate the number of months to repay the debt
if monthly_payment > 0 and annual_interest_rate > 0:
    monthly_interest_rate = annual_interest_rate / 12 / 100
    months_to_repay = -1 * (total_debt / monthly_payment) / (1 - (1 + monthly_interest_rate) ** (-1 * (total_debt / monthly_payment)))
    months_to_repay = int(months_to_repay)
else:
    months_to_repay = 0

# Calculate the opportunity cost
if investment_return_rate > 0 and months_to_repay > 0:
    total_paid = monthly_payment * months_to_repay
    opportunity_cost = total_paid * ((1 + investment_return_rate / 100) ** (months_to_repay / 12) - 1)
else:
    opportunity_cost = 0

# Display the result
if months_to_repay > 0:
    st.markdown(f"### You will repay your debt in approximately {months_to_repay} months.")
    st.markdown(f"### The opportunity cost of not investing this money is approximately ${opportunity_cost:,.2f}.")
else:
    st.markdown("### Please enter a valid monthly payment and interest rate to calculate the repayment period.")

