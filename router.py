import streamlit as st
from dashboard import show_dashboard
from Login import show_login
from main import show_main
from register import show_register



st.set_page_config(page_title="FitFeast", layout="wide")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = 0

login_pg = st.Page("Login.py", title="Login")
dash = st.Page("dashboard.py", title="Dashboard")
register = st.Page("register.py", title="Register")
main_pg = st.Page("main.py", title="Main")

if st.session_state.logged_in == 0:
    show_dashboard()
if st.session_state.logged_in == 1:
    show_login()
if st.session_state.logged_in == 2:
    show_register()
if st.session_state.logged_in == 3:
    show_main()