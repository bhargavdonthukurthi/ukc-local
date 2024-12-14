import streamlit as st
from streamlit_option_menu import option_menu

# Set the page configuration as the first Streamlit command
st.set_page_config(
    page_title="UKC",
    page_icon="./ukc_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": """
         This website was designed by UKC Backend for the purpose of accessing and analyzing data effectively and conveniently.
        """,
    },
)

# Other imports
from action_on_transaction import (
    get_transactions_data,
    display_total_debit,
    display_total_credit,
    display_total_debit_opex,
    display_total_credit_income,
    display_total_credit_investment,
    display_pareto_chart,
    display_debit_trend_with_classification_selection,
    display_credit_trend_income, display_net_profit_or_loss, display_transaction_trends
)
from action_on_recipe import get_recipe

# Predefined credentials for simplicity
USERS = {
    "admin": "admin123",
    "user1": "password1",
}

def login():
    #st.sidebar.title("Login")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.button("Login")

        if login_button:
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.sidebar.success("Logged in successfully!")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password")
    else:
        st.sidebar.title("Hi, Admin")
        logout_button = st.sidebar.button("Logout")
        if logout_button:
            st.session_state.logged_in = False
            st.rerun()


def main_app():
    # Apply custom CSS for dark theme
    st.markdown(
        """
        <style>
            .block-container {background-color: #1e1e1e; color: white;}
            .css-17eq0hr {background-color: #000000 !important; color: white !important;}
            .css-1v3fvcr a {color: white !important;}
            .css-1v3fvcr a:hover {background-color: #333333 !important;}
            .css-1v3fvcr .css-10trblm {background-color: #444444 !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a dark-themed icon-based sidebar menu
    with st.sidebar:
        tab = option_menu(
            "Navigation",
            ["Home", "Transaction", "Recipe"],
            icons=["house", "wallet2", "book"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#000000"},
                "icon": {"color": "#00c0f1", "font-size": "20px"},
                "nav-link": {
                    "font-size": "12px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#333333",
                    "color": "white",
                },
                "nav-link-selected": {"background-color": "#444444"},
            },
        )

    st.title("UKC Hygiene Foods")

    # Handle navigation
    if tab == "Transaction":
        get_transactions_data()

    elif tab == "Home":
        st.title("P&L")
        col1, col2 = st.columns(2)
        with col1:
            display_total_debit()
        with col2:
            display_total_credit()
        st.write("---")
        col3, col4 = st.columns(2)
        with col3:
            display_total_debit_opex()
        with col4:
            display_total_credit_income()
        st.write("---")
        col5, col6 = st.columns(2)
        with col5:
            display_total_credit_investment()
        with col6:
            display_net_profit_or_loss()
        st.write("---")
        display_transaction_trends()
        display_pareto_chart()
        display_debit_trend_with_classification_selection()
        display_credit_trend_income()

    elif tab == "Recipe":
        get_recipe()


if __name__ == "__main__":
    login()
    if st.session_state.logged_in:
        main_app()
    else:
        st.warning("Please log in to access the application.")
