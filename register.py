import streamlit as st
from Database import enter_user


def show_register():
    st.set_page_config("Register user")
    with st.sidebar:
        st.subheader('A post grad project by: ')
        st.text('Sahil Puranik | 256534')
        st.text('Aditya Gaikwad | 256501')
        st.text('Tejas Sawant | 256550')
        st.divider()
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

    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
                    .block-container {
                    padding-top: 80px;
                    }
                    </style>
                    <h1 style="color: black; font-size: 60px; font-family: 'Pacifico', cursive; margin-top: 50px;">Register for FitFeast</h1>
                """, unsafe_allow_html=True)


    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
                    </style>
                    <h2 style="color: black; font-size: 30px; font-family: 'Caveat', cursive; ">Cook smarter. Eat better. Live fuller</h2>
                """, unsafe_allow_html=True)



## REGISTERING THE USER
    with st.container(border=True):
        name = st.text_input("Enter your name")
        username = st.text_input("Enter your username")
        age = st.text_input("Enter your age")
        if age:
            if not age.isdigit():
                st.error("Please enter an integer")
        password = st.text_input("Enter your password",type ="password")
        if password:
            if len(password) < 5:
                st.error("Please enter a password of at least 5 characters")
        weight = st.text_input("Enter your weight (kg)")
        if weight:
            try:
                weight = float(weight)
            except ValueError:
                st.error("Please enter a valid number")

        height = st.text_input("Enter your height (cm)")
        if height:
            try:
                height = float(height)
            except ValueError:
                st.error("Please enter a valid number")

        register = st.button("Register")
        back_button = st.button("Back")
        if back_button:
            st.session_state.logged_in == 0
        if register and name and password and username and age and height and weight:
            enter_user(name,username,password,int(age),float(weight),float(height))
            st.success("You have successfully registered")
            st.session_state.logged_in = 1
            st.rerun()
        else:
            st.error("Enter the essential information")
