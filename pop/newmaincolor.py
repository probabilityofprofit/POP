import streamlit as st
import pandas as pd
import numpy as np
import multiprocessing
import poptions
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Custom CSS for coloring cells based on POP values */
.dataframe td {
    font-weight: bold;
}

/* Define CSS classes for background colors */
.low-pop {
    background-color: red;
    color: white; /* Add white text color for visibility on red background */
}

.medium-pop {
    background-color: yellow;
}

.high-pop {
    background-color: green;
    color: white; /* Add white text color for visibility on green background */
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

# Define a custom colormap for POP values
def custom_pop_colormap():
    # Define colors and their corresponding positions (from 0 to 1)
    colors = [(0.0, 'red'), (0.5, 'yellow'), (1.0, 'green')]
    
    # Create the custom colormap
    return LinearSegmentedColormap.from_list('custom_pop_colormap', colors)

# Streamlit UI
def main():
    try:
        st.title("Put Credit Spread")

        # Manual input of values
        underlying = st.number_input("Enter the underlying price:", value=0, placeholder="e.g. 347.47", min_value=0)
        sigma = st.number_input("Enter the sigma (volatility) as a percentage:", value=0, placeholder="e.g. 11.27", min_value=0)
        rate = st.number_input("Enter the interest rate as a percentage:", value=0, placeholder="e.g. 5.28", min_value=0)
        days_to_expiration = st.number_input("Enter the days to expiration:", value=0, placeholder="e.g. 9", min_value=0)
        percentage_array = np.arange(1, 101)
        trials = 2000

        # Dynamically generate the closing_days_array based on days_to_expiration
        closing_days_array = np.arange(1, days_to_expiration + 1)

        # Define the missing variables for manual input
        short_strike = st.number_input("Enter the short strike:", value=0, placeholder="e.g. 350", min_value=0)
        short_price = st.number_input("Enter the short price:", value=0, placeholder="e.g. 2.46", min_value=0)
        long_strike = st.number_input("Enter the long strike:", value=0, placeholder="e.g. 347.50", min_value=0)
        long_price = st.number_input("Enter the long price:", value=0, placeholder="e.g. 1.01", min_value=0)

        # Create an empty DataFrame to store results
        pop_results = pd.DataFrame(index=percentage_array, columns=closing_days_array)

        # Add a "Calculate" button to trigger the calculation
        if st.button("Calculate"):
            # Use st.spinner to display a loading spinner while calculating
            with st.spinner("Calculating..."):
                # Calculate POP values using multiprocessing
                results = []
                for percentage in percentage_array:
                    for closing_days in closing_days_array:
                        results.append((int(percentage), int(closing_days))

                pop_values = pool.starmap(calculate_pop, [(p, cd, underlying, sigma, rate, trials, days_to_expiration, short_strike, short_price, long_strike, long_price) for p, cd in results])
                pool.close()
                pool.join()

                # Fill the DataFrame with the calculated POP values
                for (percentage, closing_days), pop_value in zip(results, pop_values):
                    percentage_int = int(percentage)
                    closing_days_int = int(closing_days)
                    pop_results.at[percentage_int, closing_days_int] = pop_value

            # Display the calculated POP values in a table with cell background color
            st.write("Calculated POP Values:")
            st.dataframe(pop_results.style.applymap(color_pop_cells), height=800)

            # Create X and Y values for the scatter plot
            x_values = []
            y_values = []
            for (percentage, closing_days), pop_value in zip(results, pop_values):
                x_values.append(percentage)
                y_values.append(pop_value)

            # Convert y_values to numeric values
            y_values_numeric = pd.to_numeric(y_values, errors='coerce')

            # Create a scatter plot using Matplotlib with the custom colormap
            plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
            plt.scatter(x_values, y_values_numeric, c=y_values_numeric, cmap=custom_pop_colormap(), marker='o', edgecolor='k')
            plt.colorbar(label='POP Value')
            plt.xlabel('Percentage')
            plt.ylabel('POP Value')
            plt.title('Probability of Profit (POP) vs. Percentage')
            plt.grid(True)

            # Calculate the coefficients for the trendline
            degree = 1  # Linear regression
            coefficients = np.polyfit(x_values, y_values_numeric, degree)

            # Generate the trendline values
            trendline_x = np.array([min(x_values), max(x_values)])
            trendline_y = np.polyval(coefficients, trendline_x)

            # Plot the trendline
            plt.plot(trendline_x, trendline_y, color='#0031ff', linestyle='--', label='Trendline')

            plt.legend()  # Show the legend with the trendline label
            plt.tight_layout()
            st.pyplot(plt)

            # Calculate the coefficients for the trendline
            degree = 1  # Linear regression
            coefficients = np.polyfit(x_values, y_values_numeric, degree)

            # Generate the trendline values
            trendline_x = np.array([min(x_values), max(x_values)])
            trendline_y = np.polyval(coefficients, trendline_x)

            # Plot the trendline
            plt.plot(trendline_x, trendline_y, color='#0031ff', linestyle='--', label='Trendline')

            plt.legend()  # Show the legend with the trendline label
            plt.tight_layout()
            st.pyplot(plt)

            # Display the calculated values
            st.write(f"Sigma: {sigma:.2f}%")
            st.write(f"Days to Expiration: {days_to_expiration}")
            st.write(f"Rate: {rate:.2f}%")

            # Calculate the maximum profit
            def calculate_maximum_profit(short_strike, short_price, long_strike, long_price):
                net_credit_received = short_price * 100  # Multiply by 100 for standard option contract sizes
                initial_spread_cost = (short_price - long_price) * 100  # Multiply by 100 for standard option contract sizes
                return net_credit_received - initial_spread_cost

            net_credit_received = short_price * 100  # Multiply by 100 for standard option contract sizes
            initial_spread_cost = calculate_initial_spread_cost(short_strike, short_price, long_strike, long_price)
            maximum_profit = net_credit_received - initial_spread_cost

            st.write(f"Maximum Profit: ${maximum_profit:.2f}")

# Define a function to apply cell background color based on POP values
def color_pop_cells(pop_value):
    # Convert pop_value to a numeric value, handling non-numeric and NaN values
    pop_value_numeric = pd.to_numeric(pop_value, errors='coerce')

    if not pd.isna(pop_value_numeric):
        if pop_value_numeric <= 30:
            return 'background-color: red'
        elif pop_value_numeric <= 50:
            return 'background-color: yellow'
        else:
            return 'background-color: green'
    else:
        # Handle non-numeric or NaN values gracefully by returning an empty string
        return ''

if __name__ == "__main__":
    main()
