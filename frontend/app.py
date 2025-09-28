import streamlit as st
import requests

st.title("Stock Price Monte Carlo Simulator")

# User inputs
ticker = st.text_input("Enter stock ticker", "AAPL")
n_sim = st.number_input("Number of simulations", min_value=1, max_value=1000, value=10)

if st.button("Run Simulation"):
    try:
        # Call FastAPI backend
        response = requests.get(
            "http://127.0.0.1:8000/simulate",
            params={"ticker": ticker, "n": n_sim}
        )
        data = response.json()
        
        st.write("Raw simulation data:")
        st.json(data)
    except Exception as e:
        st.error(f"Error: {e}")
