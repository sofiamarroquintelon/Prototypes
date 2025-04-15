import streamlit as st
import pandas as pd
import cohere
import os
from dotenv import load_dotenv
import plotly.express as px
import difflib

st.set_page_config(page_title="Cruz Verde Pharmacy Assistant", layout="wide")

st.markdown("""
<style>
body {
    background-color: #f6f8f9;
    font-family: 'Segoe UI', sans-serif;
}

/* Chat bubbles */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.user-message {
    align-self: flex-end;
    background-color: #DCF8C6;
    padding: 0.6em 1em;
    border-radius: 1rem 1rem 0 1rem;
    max-width: 70%;
    color: #333;
    font-size: 15px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

.bot-message {
    align-self: flex-start;
    background-color: #F1F0F0;
    padding: 0.6em 1em;
    border-radius: 1rem 1rem 1rem 0;
    max-width: 70%;
    color: #333;
    font-size: 15px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

/* Title and section headers */
h1, h2, h3, .stTabs [data-baseweb="tab"] {
    color: #00695c;
}

/* Tabs */
.stTabs [role="tab"] {
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    border: 1px solid #00695c;
    border-radius: 8px 8px 0 0;
    margin-right: 4px;
    background-color: #e0f2f1;
}

.stTabs [aria-selected="true"] {
    background-color: #b2dfdb;
    color: black;
}

/* Buttons */
button[kind="primary"] {
    background-color: #009688 !important;
    color: white !important;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    border: none;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

/* Expander */
details > summary {
    font-weight: bold;
    color: #00796B;
    margin-bottom: 5px;
}

/* Container style */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Inputs */
textarea, input[type="text"] {
    border-radius: 6px;
    border: 1px solid #ccc;
    padding: 10px;
    background-color: #ffffff;
}

/* Info boxes */
.stAlert {
    border-radius: 6px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# Welcome header
with st.container():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAe1BMVEX///8BmjT///0DmTQAnDQAkST6/////v7E6NMjoEUUnT0Ajx/N7Nio2Lc6nlsAlDCi0rA/nl8AkBwAkCUAmC07oFrq9vGn2LSr1rjE5NoAhQAAix1UqGseokUepkYVmTsAmSoylVUAjhTb6+HL69yi3rbO89zP6NoqlE5Yq3iWAAACw0lEQVR4nO3c23LaMBRAUVvGCEJqiiGXJiXphZb+/xcWx3WHzGQaHVcenSP2fmB4SGyvSBG5CBcFERERERERERERERERERFR7FzqC5g6Z07oZR/u7AmL27u7D0Hdd9kbQ1d8elgFtt0+lhaFi7oMrSqvUl+vPIQI9YcQof7EwvxfDxGqCyFC/SFEqD+ECPWHEKH+ECLUH0KE+kOIUH8IEeoPIUL9IUSoP4QI9YcQof4QItRf/sKiWGwFwqdRpxDulv9H889LYfv9/qmqwoXVXnqG5fL5PhqwmDfr4PEYmpXBwJHVH+MJi81sdrpmUTKg7Nh9cYVr8YCEz9GxxRTORwinL65w+hGRF1mYmvNG+Qu3MYWNRmHUMcxfqHKWtgjNC/Ofpaw0MuEuNeeN4r4eahTmP4b5C/OfpfxcKhLm/3qIMEkIEb4S5r+WIkwSQoQI04cQIcL0IUR4aUKNf4maRtjtOpE8mhFudn98AqBU2O/CCX8eWfjl7wnKqgp9FAKFX5G4wq/f6rrubjXarlZ10GPbhm9N7LZP9Yc/fWZdD0/fe/4QUei+H66FHY4/wvcmlrOrn9cL6RkOtxGF8m2OvjgKBnE25q6C3kfbkno6VHcsJ6nwB+F9E0WHH86SMC/aI3waw36e9NfsnH8pJeDdxEJ/IcKXutmXoXBYzdz5MTQ3XujOjqG5/5mlwyEyE5p7vwVChPobK9S9upw3Uqh8/TxvEL76rTzLMRQKL2AM7XQSroL/9mJXWCI0Lsz/FX8b/i5Zo8I6e2H+34dt9sL8x5C11L6QtdS+kLXUvpC11L6QtdS+kLXUvpC11L6QtdS+kLXUvpC11L6QtdS+sN1dwH/XQmepxTu0erd4XIdnUnj81TQ3N01Ym+RbfsV55+aCuiG0BeyExq5YXvbAy03B+wgmDiERERERERERERERERGR2n4DIHtg5AVT+fIAAAAASUVORK5CYII=", width=100)
    with col2:
        st.title("Welcome to Cruz Verde Pharmacy Virtual Assistant")
        st.markdown("""
        This assistant helps you to:
        - Get recommendations based on your symptoms
        - Review interactions between medications
        - Search prices and alternatives available in our database
        """)

st.divider()

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

@st.cache_data
def load_data():
    df = pd.read_csv("Medicines_with_Simulated_Prices.csv")
    df.dropna(subset=["Composition"], inplace=True)
    return df

df = load_data()

tab1, tab2, tab3 = st.tabs(["Symptom Checker", "Upload Prescription", "Price Comparison"])

if "step" not in st.session_state:
    st.session_state.step = "start"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "meds" not in st.session_state:
    st.session_state.meds = []

with tab1:
    st.title("Conversational Assistant")

    if not st.session_state.chat_history:
        st.session_state.chat_history.append({
            "role": "bot",
            "content": "Let’s talk! Describe your symptoms and I’ll recommend something for you."
        })

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        css_class = "user-message" if message["role"] == "user" else "bot-message"
        st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    def add_user_message(text):
        st.session_state.chat_history.append({"role": "user", "content": text})

    if st.session_state.step == "start":
        user_input = st.chat_input("Describe how you're feeling:")
        if user_input:
            st.session_state.user_data["symptoms"] = user_input
            add_user_message(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": "Thanks. How old are you?"})
            st.session_state.step = "age"
            st.rerun()

    elif st.session_state.step == "age":
        user_input = st.chat_input("Your age:")
        if user_input:
            st.session_state.user_data["age"] = user_input
            add_user_message(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": "Great. What’s your weight in kg?"})
            st.session_state.step = "weight"
            st.rerun()

    elif st.session_state.step == "weight":
        user_input = st.chat_input("Your weight (kg):")
        if user_input:
            st.session_state.user_data["weight"] = user_input
            add_user_message(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": "And finally, what’s your gender?"})
            st.session_state.step = "gender"
            st.rerun()

    elif st.session_state.step == "gender":
        user_input = st.chat_input("Your gender:")
        if user_input:
            st.session_state.user_data["gender"] = user_input
            add_user_message(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": "Thanks! Let me analyze your symptoms and recommend something."})
            st.session_state.step = "generate"
            st.rerun()

    elif st.session_state.step == "generate":
        with st.spinner("Analyzing your symptoms..."):
            data = st.session_state.user_data
            conversation = ""
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    conversation += f"User: {message['content']}\n"
                else:
                    conversation += f"Pharmacist: {message['content']}\n"

            prompt = f"""
            You are a helpful and smart virtual pharmacist having a conversation with a user.

            {conversation}

            Pharmacist: Based on the user’s symptoms, age, weight, and gender, suggest 2–3 **appropriate and commonly used** active ingredients for treatment. Be accurate and avoid recommending medications for unrelated conditions. Only return the active ingredient names, comma-separated. No explanation.
            """

            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=50,
                temperature=0.7
            )
            meds = [m.strip() for m in response.generations[0].text.split(",") if m.strip()]
            suggestion_text = f"Based on what you told me, I recommend: `{', '.join(meds)}`."
            st.session_state.chat_history.append({"role": "bot", "content": suggestion_text})
            st.session_state.meds = meds
            st.session_state.step = "done"
            st.rerun()

    elif st.session_state.step == "done":

        st.markdown("### Suggested Medicines in Our Pharmacy")

        results = pd.DataFrame()
        for med in st.session_state.meds:
            match = df[df["Composition"].str.contains(med, case=False, na=False)]
            results = pd.concat([results, match])

        top3 = results.drop_duplicates(subset="Medicine Name").head(3)

        if top3.empty:
            st.warning("No matching medicines found in the database.")
        else:
            for _, row in top3.iterrows():
                with st.container():
                    st.markdown('<div class="medicine-block">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if pd.notna(row["Image URL"]):
                            st.image(row["Image URL"], width=150)
                    with col2:
                        st.markdown(f"**{row['Medicine Name']}**")
                        st.markdown(f"- **Use:** {row['Uses']}")
                        st.markdown(f"- **Manufacturer:** {row['Manufacturer']}")
                        st.markdown(f"- **Price:** `${row['Price ($)']}`")
                        with st.expander("Buy now"):
                            st.markdown("### Place your order by WhatsApp")
                            whatsapp_logo_url = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
                            st.markdown(
                                f"""
                                <a href="https://wa.me/50237148100" target="_blank" style="text-decoration: none;">
                                    <div style="display: flex; align-items: center; justify-content: center;
                                                background-color: #00C853; color: white; padding: 0.6em 1.2em;
                                                border-radius: 6px; font-weight: bold; font-size: 16px; width: fit-content;">
                                        <img src="{whatsapp_logo_url}" alt="WhatsApp" style="height: 24px; margin-right: 10px;">
                                        Order via WhatsApp
                                    </div>
                                </a>
                                """,
                                unsafe_allow_html=True
                            )

        st.markdown("---")
        if st.button("Start new conversation"):
            st.session_state.step = "start"
            st.session_state.chat_history = []
            st.session_state.user_data = {}
            st.session_state.meds = []
            st.rerun()

with tab2:
    st.title("Upload Prescription")
    st.markdown("Paste your prescription or list of medicines below. We'll check availability and interactions.")

    user_input = st.text_area("Enter your prescribed medicines (comma-separated):", placeholder="e.g. Eptoin, Flucort, Augmentin")

    if st.button("Search Prescription", key="prescription_button"):
        if not user_input.strip():
            st.warning("Please enter at least one medicine name.")
        else:
            meds = [m.strip() for m in user_input.split(",") if m.strip()]
            corrected_meds = []
            not_found = []

            for med in meds:
                close = difflib.get_close_matches(med, df["Medicine Name"], n=1)
                name = close[0] if close else med
                match = df[df["Medicine Name"].str.contains(name, case=False, na=False)]
                if match.empty:
                    not_found.append(med)
                    continue
                corrected_meds.append(name)
                row = match.drop_duplicates("Medicine Name").iloc[0]
                with st.container():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if pd.notna(row["Image URL"]):
                            st.image(row["Image URL"], width=150)
                    with col2:
                        st.markdown(f"**{row['Medicine Name']}**")
                        st.markdown(f"- **Use:** {row['Uses']}")
                        st.markdown(f"- **Manufacturer:** {row['Manufacturer']}")
                        st.markdown(f"- **Price:** `${row['Price ($)']}`")
                        with st.expander("Buy now"):
                            whatsapp_logo_url = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
                            st.markdown(
                                f"""
                                <a href="https://wa.me/50237148100" target="_blank" style="text-decoration: none;">
                                    <div style="display: flex; align-items: center; justify-content: center;
                                                background-color: #00C853; color: white; padding: 0.6em 1.2em;
                                                border-radius: 6px; font-weight: bold; font-size: 16px; width: fit-content;">
                                        <img src="{whatsapp_logo_url}" alt="WhatsApp" style="height: 24px; margin-right: 10px;">
                                        Order via WhatsApp
                                    </div>
                                </a>
                                """,
                                unsafe_allow_html=True
                            )

            if corrected_meds and len(corrected_meds) > 1:
                prompt = f"Do any of these medicines have interactions or contraindications? {', '.join(corrected_meds)}."
                response = co.generate(model="command-r-plus", prompt=prompt, max_tokens=500)
                st.info(f"Interaction check: {response.generations[0].text.strip()}")

            if not_found:
                st.warning(f"Sorry, we couldn't find: {', '.join(not_found)}")

with tab3:
    st.title("Price Comparison")
    st.markdown("Enter an active ingredient to compare available products and their prices.")
    ingredient_input = st.text_input("Enter ingredient name (e.g. Paracetamol):")
    price_range = st.slider("Select price range:", float(df["Price ($)"].min()), float(df["Price ($)"].max()), (float(df["Price ($)"].min()), float(df["Price ($)"].max())), step=1.0)

    if st.button("Compare Prices"):
        if not ingredient_input.strip():
            st.warning("Please enter an ingredient to search.")
        else:
            filtered = df[df["Composition"].str.contains(ingredient_input, case=False, na=False) & df["Price ($)"].between(price_range[0], price_range[1])]
            if filtered.empty:
                st.warning(f"No medicines found for '{ingredient_input}' in the selected range.")
            else:
                fig = px.bar(filtered.drop_duplicates("Medicine Name").sort_values("Price ($)"), x="Price ($)", y="Medicine Name", orientation="h")
                fig.update_layout(height=600, plot_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)

