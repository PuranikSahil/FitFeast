import streamlit as st
def show_dashboard():
    st.set_page_config("Dashboard")
    with st.sidebar:
        st.subheader('A post grad project by: ')
        st.text('Sahil Puranik | 256534')
        st.text('Aditya Gaikwad | 256501')
        st.text('Tejas Sawant | (roll_no)')
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
                    <h1 style="color: black; font-size: 60px; font-family: 'Pacifico', cursive; margin-top: 50px;">Fit Feast</h1>
                """, unsafe_allow_html=True)
    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
                    </style>
                    <h2 style="color: black; font-size: 30px; font-family: 'Caveat', cursive; ">Cook smarter. Eat better. Live fuller</h2>
                """, unsafe_allow_html=True)


    with st.container(border=True):
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
            </style>
            <h3 style="color: black; font-size: 35px ;font-family: 'Caveat', cursive; margin-bottom: 2px;">What is FitFeast..?</h3>
            """, unsafe_allow_html=True)
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
            </style>
            <h3 style="color: black; font-size: 30px ;font-family: 'Caveat', cursive; ">
            FitFeast is your AI-powered kitchen companion that turns whatever's in your fridge into delicious meals instantly.
             Just add your ingredients, and let our smart recipe engine do the rest.
            </h3>
            """, unsafe_allow_html=True)

    col1, col2, col3 ,col4 = st.columns(4)
    with col1:
        login = st.button("Visiting Again..Login!")
        if login:
            st.session_state.logged_in = 1
            st.rerun()
    with col2:
        register = st.button("First Time..Register now!")
        if register:
            st.session_state.logged_in = 2
            st.rerun()
    with col3:
        admin = st.button("Admin")
        if admin:
            st.error("You..Admin..srsly? ..Sorry")
            st.session_state.logged_in = 0












