import streamlit as st
from Database import match_user_pwd
def show_login():
    st.markdown("""
                    """
                """
                <style>
                .stApp{
                background-image: url("https://t3.ftcdn.net/jpg/00/93/94/70/360_F_93947061_762RH5kKEGwEJNGSN6flzUOJaXkMVVAT.jpg");
                background-attachment: fixed;
                background-size: cover;
                }
                </style>
                """,
                unsafe_allow_html=True
                )
    container = st.container(border= True)

    with container:
        st.title('Welcome to Fit-Feast!')
        st.subheader('YOUR GO-TO ONLINE NUTRITIONIST')
        st.divider()
        st.title("Login")
        email = st.text_input("Enter your username")
        pwd = st.text_input("Enter your password",type="password")
        login = st.button("Login")
        if login:
            act_pwd = match_user_pwd(email,pwd)
            if pwd==act_pwd:
                st.session_state.logged_in = 3
                st.rerun()
            else:
                st.error("Please enter correct password")
                st.session_state.logged_in = 1
                st.rerun()

