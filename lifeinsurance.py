#Life Insurance Calculator

import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt

st.title("Do I Need Life Insurance?")


st.markdown("### Insurance Premium Assumptions")


# Data for males
data_males = {
    "Age": [30, 35, 40, 45],
    "Singlife": [568, 731, 976, 1278],
    "Etiqa": [765, 930, 1218, 1527],
    "Tokio Marine": [771, 945, 1213, 1608],
    "FWD": [576, 847, 985, 1451],
    "Manulife": [820, 863, 1053, 1479],
    "Prudential": [802, 1047, 1387, 1877],
    "AIA": [882, 1253, 1526, 1967],
    "Great Eastern Life": [771, 920, 1155, 1529],
    "HSBC Life": [615, 845, 997, 1272],
    "Income": [590, 822, 1032, 1348],
    "Singlife MINDEF/MHA Group Term Life": [300, 300, 300, 300]
}

# Data for females
data_females = {
    "Age": [30, 35, 40, 45],
    "Singlife": [451, 574, 722, 981],
    "Etiqa": [581, 678, 923, 1120],
    "Tokio Marine": [564, 685, 906, 1221],
    "FWD": [499, 626, 749, 1035],
    "Manulife": [583, 667, 832, 1098],
    "Prudential": [592, 762, 979, 1258],
    "AIA": [707, 854, 1057, 1428],
    "Great Eastern Life": [566, 679, 905, 1215],
    "HSBC Life": [454, 596, 723, 878],
    "Income": [504, 600, 778, 1109],
    "Singlife MINDEF/MHA Group Term Life": [300, 300, 300, 300]
}

st.markdown("**Source:** The data for these charts is sourced from MoneyOwl.")
st.markdown("**Note:** These are estimates for term life insurance coverage for $1M.")


# Create dataframes
df_males = pd.DataFrame(data_males)
df_females = pd.DataFrame(data_females)

# Plotting the data using Streamlit
st.markdown("### Annual Premiums for Males (Aged 30-45)")
st.line_chart(df_males.set_index("Age"))

st.markdown("### Annual Premiums for Females (Aged 30-45)")
st.line_chart(df_females.set_index("Age"))




# Basic Inputs
col1, col2 = st.columns(2)

with col1:
    current_age = st.number_input("Current Age", min_value=18, max_value=100, value=32)
    current_savings = st.number_input("Current Savings ($)", min_value=0.0, value=500000.0, step=1000.0)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    savings_rate = st.number_input("Savings Rate (%)", min_value=0.0, max_value=100.0, value=23.0, step=0.1)
    annual_income = st.number_input("Annual Income ($)", min_value=0.0, value=100000.0, step=1000.0)

investment_return = 4.5 / 100

# Current Situation Options
st.markdown("### Select Your Current Situation")
situation = st.radio(
    "Choose one:",
    ("a) I have dependents and debts", 
     "b) I have dependents but no debts", 
     "c) I have no dependents but have debts", 
     "d) I have no dependents and no debts currently, but might have in the future", 
     "e) I am not sure")
)

if situation == "e) I am not sure":
    st.markdown("Life insurance might not be necessary for you, but you could still consider it if you want to be conservative in case you have more financial obligations in the future.")

elif situation in ["a) I have dependents and debts", "b) I have dependents but no debts", "c) I have no dependents but have debts"]:
    st.markdown("### Enter Details for Dependents and Debts")
    number_of_dependents = st.number_input("Number of Dependents", min_value=0, value=1, step=1)
    cost_per_dependent = st.number_input("Cost per Dependent ($)", min_value=0.0, value=300000.0, step=1000.0)
    dependents_cost = number_of_dependents * cost_per_dependent
    debts_cost = st.number_input("Total Cost for Debts ($)", min_value=0.0, value=500000.0, step=1000.0)
    
    total_cost_of_dependents = cost_per_dependent * number_of_dependents
    total_coverage_needs = total_cost_of_dependents + debts_cost
    
    st.markdown(f"Total Cost of Dependents: ${total_cost_of_dependents:,.2f}")
    st.markdown(f"Total Cost of Coverage: ${total_coverage_needs:,.2f}")
    
    future_financial_obligations = dependents_cost + debts_cost
    coverage_gap = total_coverage_needs - current_savings

    if coverage_gap > 0:
        st.markdown(f"You need to cover ${coverage_gap:,.2f} with life insurance.")
    else:
        st.markdown("Your current savings sufficiently cover your obligations.")
    
    # New section for current life insurance details
    st.markdown("### Current Life Insurance Details")
    has_life_insurance = st.radio("Do you currently have life insurance?", ("Yes", "No"))
    
    if has_life_insurance == "Yes":
        current_term_life_coverage = st.number_input("Current Term Life Coverage ($)", min_value=0.0, value=0.0, step=1000.0)
        
        if current_term_life_coverage > total_coverage_needs:
            over_insured_amount = current_term_life_coverage - total_coverage_needs
            st.markdown(f"You are over-insured by ${over_insured_amount:,.2f}.")
        elif current_term_life_coverage < total_coverage_needs:
            under_insured_amount = total_coverage_needs - current_term_life_coverage
            st.markdown(f"You are under-insured by ${under_insured_amount:,.2f}.")
        else:
            st.markdown("Your current life insurance coverage matches your needs.")

elif situation == "d) I have no dependents and no debts currently, but might have in the future":
    st.markdown("Calculating your life insurance needs is more complicated and requires estimating probabilities of future events.")

#Projected savings
# Create a DataFrame to hold the savings growth data
    annual_savings = annual_income * (savings_rate / 100)
    years = list(range(current_age, current_age + 11))
    savings = [current_savings * (1 + investment_return) ** (year - current_age) + 
               annual_savings * (((1 + investment_return) ** (year - current_age) - 1) / investment_return) 
               for year in years]

    savings_data = pd.DataFrame({
        'Year': years,
        'Savings': savings
    })

    # Create the Altair chart
    savings_chart = alt.Chart(savings_data).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Savings:Q', title='Savings ($)', scale=alt.Scale(domain=[0, max(savings)])),
        tooltip=['Year', 'Savings']
    ).properties(
        title='Projected Savings Growth Over 10 Years'
    )

    # Display the chart
    st.altair_chart(savings_chart, use_container_width=True)

    # Calculate savings at coverage age
    coverage_age = current_age + 10
    current_savings_growth = current_savings * (1 + investment_return) ** 10
    annual_savings_growth = annual_savings * (((1 + investment_return) ** 10 - 1) / investment_return)
    savings_at_coverage_age = current_savings_growth + annual_savings_growth

    st.markdown(f"### Savings at Age {current_age + 10}")
    st.markdown(f"At age {current_age + 10}, your projected savings will be ${savings_at_coverage_age:,.2f}.")

    
    # Calculate savings at coverage age
    coverage_age = current_age + 10
    current_savings_growth = current_savings * (1 + investment_return) ** 10
    annual_savings_growth = annual_savings * (((1 + investment_return) ** 10 - 1) / investment_return)
    savings_at_coverage_age = current_savings_growth + annual_savings_growth
    
    st.markdown("### Enter Details for Potential Future Dependents and Debts")
    future_number_of_dependents = st.number_input("Number of Future Dependents", min_value=0, value=1, step=1)
    future_cost_per_dependent = st.number_input("Cost per Future Dependent ($)", min_value=0.0, value=300000.0, step=1000.0)
    future_dependents_cost = future_number_of_dependents * future_cost_per_dependent
    future_debts_cost = st.number_input("Total Cost for Future Debts ($)", min_value=0.0, value=500000.0, step=1000.0)
    
    future_financial_obligations = future_dependents_cost + future_debts_cost

    st.markdown("### Future Financial Obligations")
    st.markdown(f"Your future financial obligations are estimated to be ${future_financial_obligations:,.2f}.")

    if savings_at_coverage_age >= future_financial_obligations:
        st.markdown(f"Your savings of ${savings_at_coverage_age:,.2f} sufficiently cover your potential obligations.")
        coverage_gap = 0  # No gap if savings are sufficient
    else:
        coverage_gap = future_financial_obligations - savings_at_coverage_age
        st.markdown(f"Your savings are ${savings_at_coverage_age:,.2f}, which means you have a coverage gap of ${coverage_gap:,.2f}.")



    st.markdown("### Enter Probabilities for Future Events")
    probability_dependent = st.number_input("Probability of Having a Dependent (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1) / 100
    probability_debt = st.number_input("Probability of Taking on Debt (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1) / 100
    
    probability_dependent_or_debt = probability_dependent + probability_debt - (probability_dependent * probability_debt)
    
    # Annual premiums data (example values)
    annual_premiums = {
        "Male": {age: premium for age, premium in zip(
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
            [365.84, 410.16, 454.48, 498.80, 543.12, 587.44, 631.76, 676.08, 720.40, 764.72, 809.04, 853.36, 897.68, 942.00, 986.32, 1030.64, 1074.96, 1119.28, 1163.60, 1207.92, 1252.24, 1296.60, 1340.92, 1385.24, 1429.56, 1252.27, 1296.60, 1340.92, 1385.24, 1429.56, 1473.88, 1518.20, 1562.52, 1606.84, 1651.16, 1695.48, 1739.80, 1784.12, 1828.44, 1872.76, 1917.08, 1961.40, 2005.72, 2050.04, 2094.36, 2138.68, 2183.00, 2227.32, 2271.64, 2315.96]
        )},
        "Female": {age: premium for age, premium in zip(
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
            [286.50, 318.75, 351.00, 383.25, 415.50, 447.75, 480.00, 512.25, 544.50, 576.75, 609.00, 641.25, 673.50, 705.75, 738.00, 770.25, 802.50, 834.75, 867.00, 899.25, 931.50, 963.74, 995.99, 1028.24, 1060.49, 931.49, 963.74, 995.99, 1028.24, 1060.49, 1092.74, 1124.99, 1157.24, 1189.49, 1221.74, 1253.99, 1286.24, 1318.49, 1350.74, 1382.99, 1415.24, 1447.49, 1479.74, 1511.99, 1544.24, 1576.49, 1608.74, 1640.99, 1673.24, 1705.49, 1737.74]
        )}
    }
    life_insurance_current_age_cost = annual_premiums[gender][current_age] * 30
    life_insurance_coverage_age_cost = annual_premiums[gender][coverage_age] * 20
    expected_value_life_insurance_coverage_age_cost = probability_dependent_or_debt * life_insurance_coverage_age_cost

    st.markdown("### Life Insurance Cost Analysis")

    st.markdown("### Customize Premiums")

    # Default premiums based on the dictionary
    default_premium_current_age = annual_premiums[gender][current_age]
    default_premium_coverage_age = annual_premiums[gender][coverage_age]

    # Input fields for premiums
    premium_current_age = st.number_input(
        "Premium at Current Age ($)", 
        min_value=0.0, 
        value=default_premium_current_age, 
        step=10.0
    )
    premium_coverage_age = st.number_input(
        "Premium at Current Age + 10 ($)", 
        min_value=0.0, 
        value=default_premium_coverage_age, 
        step=10.0
    )

    # Update the costs based on user input
    life_insurance_current_age_cost = premium_current_age * 30
    
    # Calculate the present value of the life insurance cost at coverage age
    discount_rate = 0.03
    years_until_coverage_age = 10
    present_value_factor = (1 + discount_rate) ** years_until_coverage_age
    life_insurance_coverage_age_cost = (premium_coverage_age * 20) / present_value_factor
    
    expected_value_life_insurance_coverage_age_cost = probability_dependent_or_debt * life_insurance_coverage_age_cost

    st.markdown("#### Life insurance cost if you buy now:")
    st.markdown(f"- Annual Premium: ${annual_premiums[gender][current_age]:,.2f}")
    st.markdown(f"- Total Cost over 30 years: ${life_insurance_current_age_cost:,.2f}")

    st.markdown("#### Life insurance cost if you buy 10 years later:")
    st.markdown(f"- Annual Premium: ${annual_premiums[gender][coverage_age]:,.2f}")
    st.markdown(f"- Total Cost over 20 years (discounted to present value): ${life_insurance_coverage_age_cost:,.2f}")
    st.markdown(f"- Total Cost over 20 years (without discount): ${premium_coverage_age * 20:,.2f}")
    st.markdown(f"Expected Value of Life Insurance Cost at Coverage Age: ${expected_value_life_insurance_coverage_age_cost:,.2f}")

    
    if life_insurance_current_age_cost < expected_value_life_insurance_coverage_age_cost:
        recommendation = "You should buy life insurance now."
        savings = expected_value_life_insurance_coverage_age_cost - life_insurance_current_age_cost
        reasoning = f"Buying life insurance now will save you ${savings:,.2f} compared to buying it later."
    else:
        recommendation = "You can consider buying life insurance later."
        savings = life_insurance_current_age_cost - expected_value_life_insurance_coverage_age_cost
        reasoning = (f"The expected value of life insurance cost in the future is ${savings:,.2f} less than the cost to pay for it today. "
                     "Therefore, it might be more economical to wait until later to buy it.")
    st.markdown(f"<reasoning>{reasoning}</reasoning>", unsafe_allow_html=True)
    
    # st.markdown("<h3>Recommendation</h3>", unsafe_allow_html=True)
    # st.markdown(f"<recommendation>{recommendation}</recommendation>", unsafe_allow_html=True)
    
    # st.markdown("<h3>Step-by-Step Calculations</h3>", unsafe_allow_html=True)
    # st.markdown(f"""
    # <calculations>
    # - Savings at Coverage Age: ${savings_at_coverage_age:,.2f}
    # - Future Coverage Needs: ${future_financial_obligations:,.2f}
    # - Coverage Gap: ${coverage_gap:,.2f}
    # - Probability of Dependent or Debt: {probability_dependent_or_debt:.2%}
    # - Life Insurance Cost Now: ${life_insurance_current_age_cost:,.2f}
    # - Expected Value of Life Insurance Cost at Coverage Age: ${expected_value_life_insurance_coverage_age_cost:,.2f}
    # </calculations>
    # """, unsafe_allow_html=True)
