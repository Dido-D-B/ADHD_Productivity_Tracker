import streamlit as st
import copy
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import pandas as pd
import bcrypt
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Safely load credentials from secrets into editable dictionaries
credentials = {
    "usernames": {
        user: {
            "name": st.secrets["credentials"]["usernames"][user]["name"],
            "password": st.secrets["credentials"]["usernames"][user]["password"]
        }
        for user in st.secrets["credentials"]["usernames"]
    }
}

cookie = {
    "name": st.secrets["cookie"]["name"],
    "key": st.secrets["cookie"]["key"],
    "expiry_days": st.secrets["cookie"]["expiry_days"]
}

preauthorized = st.secrets.get("preauthorized", {})

config = {
    "credentials": credentials,
    "cookie": cookie,
    "preauthorized": preauthorized,
}

# Set page title and icon
st.set_page_config(page_title="ADHD Tracker", page_icon="icon.ico")

# WARNING: Registration will not persist without config.yaml.
# When using st.secrets for configuration, user registration is best handled in a separate interface.
with st.expander("Register New User"):
    new_name = st.text_input("Full Name")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Register"):
        if new_username in config['credentials']['usernames']:
            st.warning("Username already exists.")
        elif not new_name or not new_password:
            st.warning("Please fill out all fields.")
        else:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'password': hashed_pw
            }
            st.success("User registered successfully! You can now log in.")

# Authentication
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(fields={'Form name': 'Login'})

if authentication_status:
    st.sidebar.success(f"Welcome, {name}!")
    authenticator.logout('Logout', 'sidebar')

    st.title("ADHD Productivity Tracker")

    if not username:
        st.warning("No username detected. Please try logging in again.")
        st.stop()

    # Connect to Supabase
    load_dotenv()

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.success("Connected to Supabase database.")

    with st.container():
        st.subheader("Log Your Focus Session")

        date = st.date_input("Date", value=datetime.today())
        time_block = st.text_input("Time Block (e.g. 10:00 - 10:30)")
        activity = st.text_input("What were you doing?")
        productivity = st.selectbox("How productive were you?", ["Productive", "Neutral", "Distracted"])
        mood = st.selectbox("Mood", ["Low", "Okay", "Good", "Great"])
        energy = st.slider("Energy Level", 1, 10, 5)
        notes = st.text_area("Extra notes (optional)")


        if st.button("✅ Log Entry"):
            timestamp = datetime.now().isoformat()

            try:
                response = supabase.table("logs").insert({
                    "username": username,
                    "date": date.strftime("%Y-%m-%d"),
                    "time_block": time_block,
                    "activity": activity,
                    "productivity": productivity,
                    "mood": mood,
                    "energy": energy,
                    "notes": notes,
                    "timestamp": timestamp
                }).execute()

                if response.data:
                    st.success("Entry logged successfully!")
                else:
                    st.error(f"Insert failed. Raw response: {response}")
            except Exception as e:
                st.error(f"Failed to insert entry: {e}")

    # Show user previous logs
    st.markdown("### Your Recent Entries")
    try:
        response = supabase.table("logs").select("*").eq("username", username).order("timestamp", desc=True).limit(10).execute()
        df = pd.DataFrame(response.data)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to fetch entries: {e}")

elif authentication_status is False:
    st.error("Username or password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")