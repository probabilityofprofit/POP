import streamlit as st
import poptions
from streamlit_option_menu import option_menu

def home():
    st.title("Home Page")
    # Add content for the Home page here

def projects():
    st.title("Projects Page")
    # Add content for the Projects page here

def contact():
    st.title("Contact Page")
    # Add content for the Contact page here

def calculator():
    st.title("Option Strategy Probability Calculator")

    underlying = st.number_input("Current Underlying Price", value=39.84)
    short_strike = st.number_input("Short Strike Price", value=38.5)
    short_price = st.number_input("Short Call Price", value=1.67)
    long_strike = st.number_input("Long Strike Price", value=41)
    long_price = st.number_input("Long Call Price", value=0.39)
    rate = st.number_input("Annualized Risk-free Rate (%)", value=5.35)
    sigma = st.number_input("Implied Volatility (%)", value=38.86)
    days_to_expiration = st.number_input("Days to Expiration", value=9)
    percentage_array = st.multiselect("Percentage of Maximum Profit to Close", [1, 8, 15, 20, 25, 30, 35, 41, 45], [1, 8, 15, 20, 25, 30, 35, 41, 45])
    closing_days_array = st.multiselect("Days Passed to Close", [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9])
    trials = st.number_input("Number of Trials", value=4000)

    if st.button("Calculate"):
        result = poptions.callCreditSpread(
            underlying, sigma, rate / 100, trials, days_to_expiration,
            closing_days_array, percentage_array, short_strike,
            short_price, long_strike, long_price
        )
        st.write("Call Credit Spread Probability:", result)

# Sidebar navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Projects", "Contact", "Calculator"],
    icons=["house", "book", "envelope", "calculator"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

# Main content based on the selected navigation option
if selected == "Home":
    home()
elif selected == "Projects":
    projects()
elif selected == "Contact":
    contact()
elif selected == "Calculator":
    calculator()

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #e5e5f7;
opacity: 1;
background-image: linear-gradient(45deg, #ffffff 50%, #e5e5f7 50%);
background-size: 4px 4px;
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}

[data-testid="stToolbar"] {
right: 2rem;
}

[data-testid="stVerticalBlock"] {
background-color: #00bbff;
opacity: 1;
background-image: linear-gradient(225deg, #e5e5f7 90%, #00bbff 50%);
background-size: 4px 4px;
border-radius: 0px;
box-shadow: 0px 2px 10px rgba(0, 0, 0, 1);
}

[data-testid="stDecoration"] {
background-color: #00bbff;
opacity: 1;
background-image: linear-gradient(45deg, #ffffff 50%, #00bbff 50%);
background-size: 4px 4px;
}

[data-testid="stMarkdownContainer"] {
margin: 10px;
}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
