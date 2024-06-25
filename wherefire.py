import numpy as np
import pandas as pd
import openai
import os
import streamlit as st
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()

# Streamlit - Where FIRE Calculator

st.markdown("<h1 style='color: #F39373; padding-bottom: 30px;'>🌏 Where FIRE Calculator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #F8F6F4; padding: 10px; border-radius: 5px;'>
        <p style='color: #000000; font-size: 16px; font-weight: bold;'>Use this very simple calculator to find out which city in Southeast Asia you can achieve financial independence and retire early (FIRE) based on your current savings and lifestyle. This app was created by Sherry from the Peek team (<a href='https://peek.money' style='color: #F39373;'>peek.money</a>)</p>
    </div>
""", unsafe_allow_html=True)

# User Inputs
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #F39373;'>Enter Your Details</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    current_savings = st.number_input("Current Savings ($)", value=500000, format="%d", help="Enter your current savings in USD")
with col2:
    lifestyle = st.selectbox("Lifestyle", ["Budget", "Moderate", "Luxury"], help="Select your desired lifestyle")


def get_where_fire(current_savings, lifestyle):
    prompt = (
        f"Based on the current savings of the user and their stated lifestyle, help them figure out which city in Southeast Asia they could comfortably live in, based on a withdrawal rate of 4%. Provide a list that includes the name of the city and the cost of living.\n"
        f"Current Savings: {current_savings}\n"
        f"Lifestyle: {lifestyle}\n\n"
        ""
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial analyst. Your job is to help me figure out my financial plan. You will be given the current savings and lifestyle, and you will need to output the name of the city I could comfortably live in, based on a withdrawal rate of 4%. In the output, please use simple math and language and avoid showing brackets and code"
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

st.subheader("Find out where you can FIRE in Southeast Asia")

# Initialize session state for suggestions
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = ""

if st.button("Get Suggestion"):
    st.session_state.suggestions = get_where_fire(current_savings, lifestyle)

if st.session_state.suggestions:
    st.write(f"Suggested Cities: {st.session_state.suggestions}")
