import streamlit as st
import pandas as pd
import numpy as np
import multiprocessing
import poptions
import pyautogui

# Define the style to hide Streamlit elements
hide_streamlit_style = """
<style>
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
#MainMenu,
header,
footer {
    visibility: hidden;
    height: 0%;
    position: fixed;
}
</style>
"""

# Your additional CSS style block
custom_css = """
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
</style>
"""
st.markdown("""
    <style>
    /* Hide the link button */
    .stApp a:first-child {
        display: none;
    }
    
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)

# Combine the Streamlit styles and your custom styles
combined_styles = hide_streamlit_style + custom_css

st.markdown(combined_styles, unsafe_allow_html=True)

# Function to calculate POP for a specific combination of percentage and closing days
def calculate_pop(percentage, closing_days, underlying, sigma, rate, trials, days_to_expiration, short_strike, short_price, long_strike, long_price):
    return poptions.putCreditSpread(
        underlying, sigma, rate, trials, days_to_expiration,
        [closing_days], [percentage], short_strike,
        short_price, long_strike, long_price
    )

# Streamlit UI
def main():
    st.title("Options Calculator")

    # Manual input of values
    underlying = st.number_input("Enter the underlying price:")
    sigma = st.number_input("Enter the sigma (volatility) as a percentage:")
    rate = st.number_input("Enter the interest rate as a percentage:")
    days_to_expiration = st.number_input("Enter the days to expiration:")
    percentage_array = np.arange(1, 101)
    trials = 2000

    # Dynamically generate the closing_days_array based on days_to_expiration
    closing_days_array = np.arange(1, days_to_expiration + 1)

    # Define the missing variables for manual input
    short_strike = st.number_input("Enter the short strike:")
    short_price = st.number_input("Enter the short price:")
    long_strike = st.number_input("Enter the long strike:")
    long_price = st.number_input("Enter the long price:")

    # Create an empty DataFrame to store results
    pop_results = pd.DataFrame(index=percentage_array, columns=closing_days_array)

    # Add a "Calculate" button to trigger the calculation
    if st.button("Calculate"):
        # Use st.spinner to display a loading spinner while calculating
        with st.spinner("Calculating..."):
            # Create a multiprocessing pool with the number of processes you want to use
            num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
            pool = multiprocessing.Pool(processes=num_processes)

            # Calculate POP values using multiprocessing
            results = []
            for percentage in percentage_array:
                for closing_days in closing_days_array:
                    results.append((int(percentage), int(closing_days)))

            pop_values = pool.starmap(calculate_pop, [(p, cd, underlying, sigma, rate, trials, days_to_expiration, short_strike, short_price, long_strike, long_price) for p, cd in results])
            pool.close()
            pool.join()

            # Fill the DataFrame with the calculated POP values
            for (percentage, closing_days), pop_value in zip(results, pop_values):
                percentage_int = int(percentage)
                closing_days_int = int(closing_days)
                pop_results.at[percentage_int, closing_days_int] = pop_value

        # Display the calculated POP values in a table
        st.write("Calculated POP Values:")
        st.write(pop_results)

        # You can also export the results to an Excel file here if needed
        # excel_filename = "pop_results.xlsx"
        # pop_results.to_excel(excel_filename, index_label="Percentage", sheet_name="POP Results")
        # st.write(f"Results exported to {excel_filename}")

        # Display the calculated values
        st.write(f"Sigma: {sigma:.2f}%")
        st.write(f"Days to Expiration: {days_to_expiration}")
        st.write(f"Rate: {rate:.2f}%")
    
    # Add a "Start Over" button to reset the inputs
    if st.button("Start Over"):
        pyautogui.hotkey("ctrl","F5")

if __name__ == "__main__":
    main()
