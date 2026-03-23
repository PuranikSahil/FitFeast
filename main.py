import streamlit as st
from crewai import Agent, Task, Crew , LLM, Process


#"""_____________________
#    The Agent systems depend on the LLMs for the core thinking and decision making.
#    CrewAI uses the lite LLMs to access the LLM, so anything available to LiteLLM is available
#    to use within the CrewAI frameworks.
#
#    Here I am using GPT-4o, therefore it obviously needs an API key.
#    syntax:
#   llm = LLM(
#            model = 'openai/gpt-4o',
#           api_key = 'API KEY'
#            )
#_________________________"""

def show_main():
    api_key = st.secrets["GROQ_API_KEY"]
    st.markdown(
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
    st.set_page_config("First Gen")
    st.markdown("""
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
                </style>
                <h2 style="color: black; font-size: 30px; font-family: 'Caveat', cursive; ">Hi, I'm FirstGen ... Your Nutritional Chatbot</h2>
                """,
                unsafe_allow_html=True)
    output_container = st.container(border=True)

    with st.sidebar:
        st.title("HI! ITS FIRST GEN!")



        food_item = st.text_input("Which food item do you want to search about?")

        if st.button("Start!"):
            if not food_item:
                st.error("Please input your food item!")
                st.stop()

            llm = LLM(
                    model="groq/openai/gpt-oss-120b",
                    api_key=api_key,
                )
                # AGENTS:
            writer = Agent(
                role='Nutritionist',
                goal='Write an engaging article about the {} in 500 number of words. And also how to make it at home. '.format(food_item),
                backstory='You are a professional nutritionist with over 20+ years of experience and knows how to cook delicious food',
                llm=llm,
                verbose=True
                )
            editor = Agent(
                role='Senior editor',
                goal='Edit the drafted article for clarity, grammar for common people.',
                backstory='You are an editor who simplifies things and tells how something is going to help while ensuring very friendly tone',
                llm=llm,
                verbose=False
                )
                # TASKS:
            write_task = Task(
                description='Draft an article about whether {food_item} is healthy for a person or not or explain how healthy it is, while focusing on the nutritional values gained from it.'.format(
                    food_item=food_item),
                expected_output='A text article',
                agent=writer
            )
            edit_task = Task(
                description='Review the draft, fix the errors and improve structure',
                expected_output='A final polished article which clearly tells about nutritional values and its advantages',
                agent=editor
            )

                #Groups Agents:
            crew_group = Crew(
                agents=[writer, editor],
                tasks=[write_task, edit_task],
                process=Process.sequential,
                verbose=True
            )

                #start
            with st.spinner('Wait for it...'):
                result = crew_group.kickoff()
            with output_container:
                st.subheader('Here we go!')
                st.markdown("""
                                <style>
                                @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap');
                                </style>
                            """, unsafe_allow_html=True)
                st.markdown(
                    f'<h2 style="color: black; font-size: 25px; font-family: Caveat, cursive;">{result.raw}</h2>',
                    unsafe_allow_html=True
                )

