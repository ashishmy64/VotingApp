import streamlit as st
import json
import os

# File paths
users_file = "users.json"
votes_file = "votes.json"

# Fixed voting title
VOTING_TITLE = "Voting for Class CR"

# Initialize data files
def initialize_files():
    if not os.path.exists(users_file):
        with open(users_file, "w") as file:
            json.dump({}, file)
    if not os.path.exists(votes_file):
        with open(votes_file, "w") as file:
            json.dump({"Ashish": 0, "Sourabh": 0, "Darshan": 0}, file)

# Load user data
def load_users():
    with open(users_file, "r") as file:
        return json.load(file)

# Save user data
def save_users(users):
    with open(users_file, "w") as file:
        json.dump(users, file)

# Load votes
def load_votes():
    with open(votes_file, "r") as file:
        return json.load(file)

# Save votes
def save_votes(votes):
    with open(votes_file, "w") as file:
        json.dump(votes, file)

# Initialize files
initialize_files()
users = load_users()
votes = load_votes()

# App starts here
st.title("Simple Voting System")

# Authentication system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.voted = False

if not st.session_state.logged_in:
    st.subheader("Login / Sign Up")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

    with tab2:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            if new_username in users:
                st.error("Username already exists.")
            elif len(new_username) < 3 or len(new_password) < 3:
                st.error("Username and password must be at least 3 characters long.")
            else:
                users[new_username] = new_password
                save_users(users)
                st.success("Account created successfully! Please log in.")

else:
    st.subheader(f"Welcome, {st.session_state.username}!")

    # Voting Section
    if not st.session_state.voted:
        st.header(VOTING_TITLE)

        for person in votes.keys():
            if st.button(f"Vote for {person}"):
                votes[person] += 1
                save_votes(votes)
                st.session_state.voted = True
                st.success("Thanks for voting! You can log out below.")

    else:
        st.success("Thanks for voting! You can log out below.")

    # Logout Option
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.voted = False
        st.session_state.username = None
        st.info("You have logged out.")
