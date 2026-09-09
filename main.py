import streamlit as st
from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
import os
import base64
@st.cache_data
def load_recipes():
    import pandas as pd
    df = pd.read_excel("cleaned_recipes_dataset.xlsx", sheet_name="recipes-with-nutrition")
    return df
load_dotenv()

def get_image_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def show_main():
    api_key = st.secrets["GROQ_API_KEY"]
    username = st.session_state.get("username", "User")
    bg_b64 = get_image_b64("bgimage.jpg")
    bg_css = f'url("data:image/jpeg;base64,{bg_b64}")' if bg_b64 else "none"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Caveat:wght@400;700&display=swap');

        .stApp {{
            background-image: {bg_css};
            background-attachment: fixed;
            background-size: cover;
        }}

        .block-container {{
            padding-top: 0px !important;
        }}

        /* Style the logout button (first button on the page) */
        div[data-testid="stButton"]:first-of-type > button {{
            background-color: #e74c3c !important;
            color: white !important;
            border: none !important;
            font-family: 'Caveat', cursive !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            padding: 6px 18px !important;
            position: relative;
            z-index: 200 !important;
            margin-top: 8px;
            margin-left: 8px;
        }}
        div[data-testid="stButton"]:first-of-type > button:hover {{
            background-color: #c0392b !important;
        }}

        /* Cards */
        .glass-card {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            padding: 22px 20px 18px 20px;
            text-align: center;
            height: 295px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .glass-card:hover {{
            background: rgba(255, 255, 255, 0.45);
            transform: scale(1.03);
            box-shadow: 0 8px 30px rgba(0,0,0,0.18);
        }}
        .card-title {{
            font-family: 'Caveat', cursive;
            font-size: 25px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}
        .card-subtitle {{
            font-family: 'Caveat', cursive;
            font-size: 17px;
            color: #333;
            line-height: 1.55;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
        }}
        .tdee-strip {{
            background: linear-gradient(135deg, rgba(0,0,0,0.78), rgba(40,40,40,0.82));
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 16px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 24px;
            border: 1px solid rgba(255,255,255,0.15);
        }}
        .tdee-strip-text {{
            font-family: 'Caveat', cursive;
            font-size: 21px;
            color: #fff;
            font-weight: 700;
        }}

        .spectrum-outer {{ margin: 14px 0 4px 0; }}
        .spectrum-bar {{
            width: 100%;
            height: 16px;
            border-radius: 10px;
            background: linear-gradient(to right, #3498db 0%, #2ecc71 25%, #f1c40f 50%, #e67e22 75%, #e74c3c 100%);
            box-shadow: 0 2px 8px rgba(0,0,0,0.18);
        }}
        .spectrum-labels {{
            display: flex;
            justify-content: space-between;
            font-family: 'Caveat', cursive;
            font-size: 13px;
            color: #3a3a3a;
            margin-top: 5px;
            font-weight: 700;
        }}

        .tdee-note {{
            font-family: 'Caveat', cursive;
            font-size: 17px;
            color: #555;
            text-align: center;
            margin: 10px 0 4px 0;
        }}

        .section-header {{
            font-family: 'Caveat', cursive;
            font-size: 26px;
            color: #2d2d2d;
            margin-bottom: 4px;
            font-weight: 700;
        }}

        .tdee-page-header {{
            font-family: 'Pacifico', cursive;
            font-size: 28px;
            color: #2d2d2d;
            text-align: center;
            margin-bottom: 6px;
        }}
        .tdee-page-sub {{
            font-family: 'Caveat', cursive;
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }}
        .tdee-result-box {{
            background: rgba(255,255,255,0.35);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 20px 28px;
            margin-top: 16px;
            border: 1px solid rgba(255,255,255,0.5);
        }}
        .tdee-result-title {{
            font-family: 'Caveat', cursive;
            font-size: 21px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}
        .tdee-result-value {{
            font-family: 'Pacifico', cursive;
            font-size: 38px;
            color: #e67e22;
            margin: 4px 0;
        }}
        .tdee-result-label {{
            font-family: 'Caveat', cursive;
            font-size: 16px;
            color: #555;
        }}
        .bmi-line {{
            font-family: 'Caveat', cursive;
            font-size: 20px;
            font-weight: 700;
            color: #2d2d2d;
            margin-top: 12px;
        }}
        </style>
    """, unsafe_allow_html=True)

    if "section" not in st.session_state:
        st.session_state.section = 0

    # ─── SECTION 0: Landing ───
    if st.session_state.section == 0:

        # ── Real functional logout button — rendered BEFORE banner ──
        

        # ── Banner with title + hello overlaid inside it ──
        banner_b64 = get_image_b64("headingbanner.jpg")
        if banner_b64:
            st.markdown(f"""
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
                .banner-container {{
                    position: relative;
                    width: 100vw;
                    left: 50%;
                    margin-left: -50vw;
                    height: 120px;
                    border-top: 3px solid #1a1a1a;
                    border-bottom: 3px solid #1a1a1a;
                    overflow: hidden;
                    margin-top: -58px;
                    z-index: 0;
                }}
                .banner-img {{
                    display: block;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transform: scale(1.38);
                    position: relative;

                }}
                .banner-topbar {{
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 40px 0 160px;
                    z-index: 10;
                    pointer-events: none;
                }}
                .banner-title {{
                    font-family: 'Fredoka One', sans-serif;
                    font-size: 30px;
                    color: #fff;
                    -webkit-text-stroke: 2px #000;
                    text-align: center;
                    flex: 1;
                    position: absolute;
                    top: 60%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(0, 0, 0, 0.6);
                    padding: 3px 4px;
                    border-radius: 10px;
                }}
                .banner-hello {{
                    font-family: 'Caveat', cursive;
                    font-size: 20px;
                    font-weight: 700;
                    color: #fff;
                    text-shadow: 0 1px 6px rgba(0,0,0,0.6);
                    white-space: nowrap;
                }}
                </style>
                <div class="banner-container">
                    <img src="data:image/jpeg;base64,{banner_b64}" class="banner-img"/>
                    <div class="banner-topbar">
                        <div style="width:60px;"></div>
                        <div class="banner-title">Ways to find your perfect meal 🍽️</div>
                        <div class="banner-hello">👋 Hello, {username}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        else:
            st.markdown(f"""
                <div style="position:relative; width:100%; height:80px;
                background:rgba(0,0,0,0.6); border-radius:10px; display:flex;
                align-items:center; justify-content:center; margin-bottom:10px;">
                    <span style="font-family:'Pacifico',cursive; font-size:26px; color:#fff;">
                        Ways to find your perfect meal 🍽️
                    </span>
                    <span style="position:absolute; right:20px; font-family:'Caveat',cursive;
                    font-size:18px; color:#fff;">👋 Hello, {username}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3 Cards ──
        col1, col2, col3 = st.columns(3, gap="large")


        with col1:
            st.markdown("""
                <div class="glass-card">
                    <div class="card-title">🔥 Calorie-Based Meals</div>
                    <div class="card-subtitle">
                        How many calories do you want to eat?<br><br>
                        • Enter your calorie goal<br>
                        • Specify nutritional values like protein, carbs or fat
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Explore →", key="sec1", use_container_width=True):
                st.session_state.section = 1
                st.rerun()

        with col2:
            st.markdown("""
                <div class="glass-card">
                    <div class="card-title">🥗 Pick Your Culinary Genre</div>
                    <div class="card-subtitle">
                        Find dishes based on your mood and dietary choices<br><br>
                        • Select cuisine, dish, or meal type<br>
                        • Add dietary preferences
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Explore →", key="sec2", use_container_width=True):
                st.session_state.section = 2
                st.rerun()

        with col3:
            st.markdown("""
                <div class="glass-card">
                    <div class="card-title">🧑‍🍳 Cook With What You Have</div>
                    <div class="card-subtitle">
                        Find dishes based on the ingredients in your kitchen<br><br>
                        • No grocery run needed<br>
                        • Smart recipes from whatever's available
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Explore →", key="sec3", use_container_width=True):
                st.session_state.section = 3
                st.rerun()

        # ── TDEE strip ──
        st.markdown("""
            <div class="tdee-strip">
                <div class="tdee-strip-text">📊 How much should you eat today?&nbsp;&nbsp;Calculate your TDEE in seconds</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Calculate Now  →", key="tdee_go", use_container_width=True):
            st.session_state.section = 4
            st.rerun()

        # ── BMI Spectrum ──
        st.markdown("""
            <div class="spectrum-outer">
                <div class="spectrum-bar"></div>
                <div class="spectrum-labels">
                    <span>Underweight</span>
                    <span>Normal</span>
                    <span>Overweight</span>
                    <span>Obese</span>
                    <span>Severely Obese</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="tdee-note">
                Your TDEE is how many calories your body needs daily to maintain, lose, or gain weight — based on your lifestyle.
            </div>
        """, unsafe_allow_html=True)

    # ─── SECTION 1: Calorie-Based ───
    elif st.session_state.section == 1:
        st.markdown('<p class="section-header">🔥 Calorie-Based Meal Finder</p>', unsafe_allow_html=True)
        st.write("             ")
        if st.button("← Back", key="back1"):
            st.session_state.section = 0
            st.rerun()
        with st.container(border=True):
            calories = st.text_input("How many calories do you want to eat?", placeholder="e.g. 400")
            protein  = st.text_input("Protein target in grams (optional)", placeholder="e.g. 20")
            carbs    = st.text_input("Carbs target in grams (optional)", placeholder="e.g. 30")
            fat      = st.text_input("Fat target in grams (optional)", placeholder="e.g. 10")
            fiber    = st.text_input("Fiber target in grams (optional)", placeholder="e.g. 5")

            if st.button("Find Meals!", key="find_cal"):
                if not calories:
                    st.error("Please enter a calorie target!")
                    st.stop()

                import pickle
                import numpy as np
                import pandas as pd

                # Load model files — these must be in the same folder as main.py
                with open(r"scaler.pkl", "rb") as f:   scaler  = pickle.load(f)
                with open(r"knn_model_cal.pkl", "rb") as f: knn = pickle.load(f)
                with open(r"content.pkl", "rb") as f:  content = pickle.load(f)
                with open(r"recipe.pkl", "rb") as f:   recipe  = pickle.load(f)

                # Median defaults for optional fields
                med_protein = float(content["protein/serve"].median())
                med_carbs   = float(content["carbs/serve"].median())
                med_fat     = float(content["fat/serve"].median())
                med_fiber   = float(content["fiber/serve"].median())

                # Use user input if provided, else use median
                p  = float(protein) if protein  else med_protein
                c  = float(carbs)   if carbs    else med_carbs
                fa = float(fat)     if fat      else med_fat
                fi = float(fiber)   if fiber    else med_fiber
                cal_val = float(calories)

                # Build input in same column order as training
                user_input = pd.DataFrame([[p, c, fa, fi, cal_val]],
                    columns=["protein/serve", "carbs/serve", "fat/serve", "fiber/serve", "Cal/Ser"])

                # Apply same transforms as training
                user_input_log    = np.log1p(user_input)
                user_input_scaled = scaler.transform(user_input_log)

                # Get top 5 nearest dishes
                dist, idx = knn.kneighbors(user_input_scaled)

                dishes = []
                for i in idx[0]:
                    row = content.iloc[i]
                    dishes.append({
                        "name":     recipe.iloc[i],
                        "calories": round(row["Cal/Ser"], 1),
                        "protein":  round(row["protein/serve"], 1),
                        "carbs":    round(row["carbs/serve"], 1),
                        "fat":      round(row["fat/serve"], 1),
                        "fiber":    round(row["fiber/serve"], 1),
                    })

                # Format dish list for agent
                dish_text = "\n".join([
                    f"{i+1}. {d['name']} — {d['calories']} cal | protein: {d['protein']}g | carbs: {d['carbs']}g | fat: {d['fat']}g | fiber: {d['fiber']}g"
                    for i, d in enumerate(dishes)
                ])
                
                # Agent presents them nicely
                llm = LLM(model="groq/openai/gpt-oss-120b", api_key=api_key)

                obtainer = Agent(
                    role = 'Ingredient Extractor',
                    goal = 'Extract a clean, structured list of ingredients for each recommended dish.',
                    backstory='You are expert at reading recipe data and pulling out exactly the ingredients used, with no extra commentary.',
                    llm = llm, verbose = False
                )

                researcher = Agent(
                    role = ' Nutrition Researcher',
                    goal = 'Research the nutritional and health relevance of each ingredient.',
                    backstory = 'You are a food science researcher who explains what each ingredient contributes nutritionally and why it matters for the user goal.',
                    llm = llm, verbose = False
                )
                writer = Agent(
                    role='Nutritionist',
                    goal=f'Present these meal recommendations clearly and engagingly.',
                    backstory='You are a friendly nutritionist who explains meals in a warm, simple way.',
                    llm=llm, verbose=False
                )

                obtainer_task = Task(
                    description=f'''Here are the top matched dishes:
                    {dish_text}
                    For each dish, extract a clean list of its ingredients.''',
                    expected_output='A list of dishes, each with a clean bullet list of ingredients.',
                    agent=obtainer
                )

                research_task = Task(
                    description=f'''Using the ingredient lists from the previous step, research each dish's ingredients
                    in the context of the user's target of {cal_val} calories. Note key nutritional contributions
                    (macros, notable micronutrients, why it fits or doesn't fit the calorie/macro goal).''',
                    expected_output='For each dish, a short nutritional breakdown of its ingredients.',
                    agent=researcher,
                    context=[obtainer_task]
                )

                task = Task(
                    description=f'''The user wants meals around {cal_val} calories.
                    Our recommendation system found these top matches:
                    {dish_text}
                    Present each dish with its name, why it fits the user's calorie/macro goal, and a one-line description of what the dish is. 
                    Keep it friendly and simple.''',
                    expected_output='5 meal suggestions presented in a friendly, readable format',
                    agent=writer
                )
                crew_group = Crew(
                    agents=[obtainer, researcher,writer],
                    tasks=[obtainer_task, research_task, task],
                    process=Process.sequential,
                    verbose=False
                )

                with st.spinner('Finding the perfect meals for you...'):
                    result = crew_group.kickoff()

                st.success("Here are your meal suggestions!")
                st.markdown(f'<div style="font-family: Caveat, cursive; font-size: 20px; color: #1a1a1a;">{result.raw}</div>', unsafe_allow_html=True)

    # ─── SECTION 2: Pick your Culinary Genre ───
    elif st.session_state.section == 2:
        

        st.markdown('<p class="section-header">🥗 Pick your Culinary Genre</p>', unsafe_allow_html=True)
        st.write("             ")
        if st.button("← Back", key="back1"):
            st.session_state.section = 0
            st.rerun()
        df_recipes = load_recipes()

        # Build dropdown options from the actual dataset values
        cuisine_options = ["Any"] + sorted(df_recipes["cuisine_type"].dropna().str.title().unique().tolist())
        meal_options    = ["Any"] + sorted(df_recipes["meal_type"].dropna().unique().tolist())
        dish_options    = ["Any"] + sorted(df_recipes["dish_type"].dropna().unique().tolist())

        with st.container(border=True):
            cuisine_type = st.selectbox("Choose a cuisine", cuisine_options)
            meal_type    = st.selectbox("Meal type", meal_options)
            dish_type    = st.selectbox("Dish type", dish_options)

            if st.button("Find Recipes!", key="find_diet"):

                # ── Filter dataset ──
                filtered = df_recipes.copy()

                if cuisine_type != "Any":
                    filtered = filtered[
                        filtered["cuisine_type"].str.contains(cuisine_type, case=False, na=False)
                    ]
                if meal_type != "Any":
                    filtered = filtered[
                        filtered["meal_type"].str.contains(meal_type, case=False, na=False)
                    ]
                if dish_type != "Any":
                    filtered = filtered[
                        filtered["dish_type"].str.contains(dish_type, case=False, na=False)
                    ]

                if filtered.empty:
                    st.warning("No recipes found for that combination. Try relaxing one of the filters.")
                    st.stop()

                # Pick up to 10 random matches, send 5 to Groq
                sample = filtered.sample(min(10, len(filtered)), random_state=42)
                top5   = sample.head(5)

                dish_text = "\n".join([
                    f"{i+1}. {row['recipe_name']} ({row['dish_type']}, {row['cuisine_type']}) — {round(row['Cal/Ser'])} cal/serving"
                    for i, (_, row) in enumerate(top5.iterrows())
                ])

                # ── Groq just formats the output ──
                #groq/llama-3.3-70b-versatile
                llm = LLM(model="groq/openai/gpt-oss-120b", api_key=api_key)
                obtainer = Agent(
                    role='Ingredient Extractor',
                    goal='Extract a clean, structured list of ingredients for each recommended dish.',
                    backstory='You are expert at reading recipe data and pulling out exactly the ingredients used, with no extra commentary.',
                    llm=llm, verbose=False
                )

                researcher = Agent(
                    role=' Nutrition Researcher',
                    goal='Research the nutritional and health relevance of each ingredient.',
                    backstory='You are a food science researcher who explains what each ingredient contributes nutritionally and why it matters for the user goal.',
                    llm=llm, verbose=False
                )
                writer = Agent(
                    role='Nutritionist',
                    goal=f'Present these meal recommendations clearly and engagingly.',
                    backstory='You are a friendly nutritionist who explains meals in a warm, simple way.',
                    llm=llm, verbose=False
                )

                obtainer_task = Task(
                    description=f'''Here are the top matched dishes:
                                    {dish_text}
                                    For each dish, extract a clean list of its ingredients.''',
                    expected_output='A list of dishes, each with a clean bullet list of ingredients.',
                    agent=obtainer
                )

                research_task = Task(
                    description=f'''Using the ingredient lists from the previous step, research each dish's ingredients
                                    in the context of calories. Note key nutritional contributions
                                    (macros, notable micronutrients, why it fits or doesn't fit the calorie/macro goal).''',
                    expected_output='For each dish, a short nutritional breakdown of its ingredients.',
                    agent=researcher,
                    context=[obtainer_task]
                )

                task = Task(
                    description=f'''The user wants meals of {cuisine_type} cuisine type for {meal_type} which includes {dish_type} .
                                    Our recommendation system found these top matches:
                                    {dish_text}
                                    Present each dish with its name, why it fits the user's preferences, and a one-line description of what the dish is. 
                                    Also mention what makes this dish special, and healthy.
                                    Keep it friendly and simple.''',
                    expected_output='5 meal suggestions presented in a friendly, readable format',
                    agent=writer
                )
                crew_group = Crew(
                    agents=[obtainer, researcher, writer],
                    tasks=[obtainer_task, research_task, task],
                    process=Process.sequential,
                    verbose=False
                )

                with st.spinner('Finding your perfect dishes...'):
                    result = crew_group.kickoff()

                st.success(f"Found {len(filtered)} matching recipes — here are 5!")
                st.markdown(
                    f'<div style="font-family: Caveat, cursive; font-size: 20px; color: #1a1a1a;">{result.raw}</div>',
                    unsafe_allow_html=True
                )
    # ─── SECTION 3: Cook with what you have ───
    elif st.session_state.section == 3:
        

        st.markdown('<p class="section-header">🧑‍🍳 Cook with what you have</p>', unsafe_allow_html=True)
        st.write("             ")
        if st.button("← Back", key="back1"):
            st.session_state.section = 0
            st.rerun()
        with st.container(border=True):
            ingredients = st.text_area("What ingredients do you have?", placeholder="e.g. eggs, tomatoes, cheese, onion, bread...")

            if st.button("Find Recipes!", key="find_ingr"):
                if not ingredients:
                    st.error("Please enter at least a few ingredients!")
                    st.stop()

                import pickle

                with open("knn_model.pkl", "rb") as f: knn  = pickle.load(f)
                with open("vect.pkl",      "rb") as f: vect = pickle.load(f)
                with open("df.pkl",        "rb") as f: df   = pickle.load(f)

                # Feed ingredients into TF-IDF + KNN model
                user_text = ingredients.lower().strip()
                user_vect = vect.transform([user_text])
                A = knn.kneighbors(user_vect, n_neighbors=5)

                dishes = []
                for i in range(len(A[1][0])):
                    idx = A[1][0][i]
                    dishes.append({
                        "name":        df["recipe_name"].iloc[idx],
                        "ingredients": df["ingredient_text"].iloc[idx]
                    })
                # Format for agent
                dish_text = "\n".join([
                    f"{i+1}. {d['name']} — uses: {d['ingredients'][:100]}"
                    for i, d in enumerate(dishes)
                ])


                llm = LLM(model="groq/openai/gpt-oss-120b", api_key=api_key)
                obtainer = Agent(
                    role='Ingredient Extractor',
                    goal='Extract a clean, structured list of ingredients for each recommended dish.',
                    backstory='You are expert at reading recipe data and pulling out exactly the ingredients used, with no extra commentary.',
                    llm=llm, verbose=False
                )

                researcher = Agent(
                    role=' Nutrition Researcher',
                    goal='Research the nutritional and health relevance of each ingredient.',
                    backstory='You are a food science researcher who explains what each ingredient contributes nutritionally and why it matters for the user goal.',
                    llm=llm, verbose=False
                )
                writer = Agent(
                    role='Nutritionist',
                    goal=f'Present these meal recommendations clearly and engagingly.',
                    backstory='You are a friendly nutritionist who explains meals in a warm, simple way.',
                    llm=llm, verbose=False
                )

                obtainer_task = Task(
                    description=f'''Here are the top matched dishes:
                                    {dish_text}
                                    For each dish, extract a clean list of its ingredients.''',
                    expected_output='A list of dishes, each with a clean bullet list of ingredients.',
                    agent=obtainer
                )

                research_task = Task(
                    description=f'''Using the ingredient lists from the previous step, research each dish's ingredients
                                    and find if the dish ingredients actually match the user's ingredients: {ingredients}.
                                    If the user's ingredients does not match with the ingredients in the {dish_text}, tell what ingredients are missing, to make the {dish_text}
                                    Basically, compare {ingredients} and {dish_text} and tell how many ingredients will be needed in the {ingredients} to make {dish_text}''',
                    expected_output='For each dish, a short nutritional breakdown of its ingredients.',
                    agent=researcher,
                    context=[obtainer_task]
                )

                task = Task(
                    description=f'''The user wants meal suggestions from the ingredients the user has. .
                                    Our recommendation system found these top matches:
                                    {dish_text}. 
                                    But the user might have to add a few ingredients based on the previous response.
                                    Present each dish with its name, tell user if he/she has to add any more ingredients to make the {dish_text} 
                                    , and a one-line description of what the dish is. 
                                    Keep it friendly and simple.''',
                    expected_output='5 meal suggestions presented in a friendly, readable format',
                    agent=writer,
                    context =[research_task]
                )
                crew_group = Crew(
                    agents=[obtainer, researcher, writer],
                    tasks=[obtainer_task, research_task, task],
                    process=Process.sequential,
                    verbose=False
                )

                with st.spinner('Finding recipes from your kitchen...'):
                    result = crew_group.kickoff()

                st.success("Here are your recipes!")
                st.markdown(f'<div style="font-family: Caveat, cursive; font-size: 20px; color: #1a1a1a;">{result.raw}</div>', unsafe_allow_html=True)

    # ─── SECTION 4: TDEE Calculator ───
    elif st.session_state.section == 4:
        
        st.write("             ")
        st.write("             ")
        st.write("             ")
        if st.button("← Back", key="back1"):
            st.session_state.section = 0
            st.rerun()
        st.markdown('<div class="tdee-page-header">📊 TDEE Calculator</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tdee-page-sub">How to Calculate TDEE for Weight Loss and Healthy Living</div>', unsafe_allow_html=True)

        with st.container(border=True):
            col_a, col_b = st.columns(2)
            with col_a:
                age      = st.number_input("Age (years)",  min_value=10,  max_value=100, value=25,  step=1)
                height   = st.number_input("Height (cm)",  min_value=100, max_value=250, value=170, step=1)
                activity = st.selectbox("Activity Level", [
                    "Sedentary (little/no exercise)",
                    "Lightly active (1–3 days/week)",
                    "Moderately active (3–5 days/week)",
                    "Very active (6–7 days/week)",
                    "Extra active (physical job or 2x training)"
                ])
            with col_b:
                gender = st.selectbox("Gender", ["Male", "Female"])
                weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70, step=1)

            calculate = st.button("Calculate 🔥", key="calc_tdee", use_container_width=True)

        if calculate:
            if gender == "Male":
                bmr_mifflin = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr_mifflin = 10 * weight + 6.25 * height - 5 * age - 161

            if gender == "Male":
                bmr_pavlidou = 9.65 * weight + 573 * (height / 100) - 5.08 * age + 260
            else:
                bmr_pavlidou = 7.38 * weight + 607 * (height / 100) - 2.31 * age + 43

            raw_diff          = bmr_pavlidou - bmr_mifflin
            capped_adjustment = max(-100, min(100, raw_diff))
            bmr               = bmr_mifflin + capped_adjustment

            multipliers = {
                "Sedentary (little/no exercise)":             1.2,
                "Lightly active (1–3 days/week)":             1.375,
                "Moderately active (3–5 days/week)":          1.55,
                "Very active (6–7 days/week)":                1.725,
                "Extra active (physical job or 2x training)": 1.9
            }
            tdee = bmr * multipliers[activity]

            bmi = weight / ((height / 100) ** 2)
            if bmi < 18.5:
                bmi_cat    = "Underweight"
                bmi_color  = "#3498db"
                marker_pct = max(0, (bmi / 18.5) * 20)
            elif bmi < 25:
                bmi_cat    = "Normal"
                bmi_color  = "#2ecc71"
                marker_pct = 20 + ((bmi - 18.5) / 6.5) * 25
            elif bmi < 30:
                bmi_cat    = "Overweight"
                bmi_color  = "#f1c40f"
                marker_pct = 45 + ((bmi - 25) / 5) * 25
            elif bmi < 35:
                bmi_cat    = "Obese"
                bmi_color  = "#e67e22"
                marker_pct = 70 + ((bmi - 30) / 5) * 15
            else:
                bmi_cat    = "Severely Obese"
                bmi_color  = "#e74c3c"
                marker_pct = min(95, 85 + ((bmi - 35) / 5) * 10)

            marker_pct = round(marker_pct, 1)

            col_res1, col_res2, col_res3 = st.columns(3)

            with col_res1:
                st.markdown(f"""
                    <div class="tdee-result-box" style="text-align:center;">
                        <div class="tdee-result-title">🔥 Your TDEE</div>
                        <div class="tdee-result-value">{int(tdee)}</div>
                        <div class="tdee-result-label">calories / day</div>
                    </div>
                """, unsafe_allow_html=True)

            with col_res2:
                st.markdown(f"""
                    <div class="tdee-result-box" style="text-align:center;">
                        <div class="tdee-result-title">⚖️ To Lose Weight</div>
                        <div class="tdee-result-value" style="font-size:30px; color:#e74c3c;">{int(tdee - 500)}</div>
                        <div class="tdee-result-label">cal/day (−500 deficit)</div>
                    </div>
                """, unsafe_allow_html=True)

            with col_res3:
                st.markdown(f"""
                    <div class="tdee-result-box" style="text-align:center;">
                        <div class="tdee-result-title">💪 To Gain Weight</div>
                        <div class="tdee-result-value" style="font-size:30px; color:#2ecc71;">{int(tdee + 500)}</div>
                        <div class="tdee-result-label">cal/day (+500 surplus)</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="bmi-line">
                    BMI Score: {bmi:.1f} kg/m²
                    <span style="color:{bmi_color}; background:rgba(255,255,255,0.3);
                    border-radius:6px; padding:2px 10px; margin-left:8px;">
                    {bmi_cat}</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="spectrum-outer">
                    <div style="position:relative;">
                        <div class="spectrum-bar"></div>
                        <div style="position:absolute; top:-8px; left:{marker_pct}%;
                            transform:translateX(-50%); font-size:20px; line-height:1;">▼</div>
                    </div>
                    <div class="spectrum-labels">
                        <span>Underweight</span>
                        <span>Normal</span>
                        <span>Overweight</span>
                        <span>Obese</span>
                        <span>Severely Obese</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
