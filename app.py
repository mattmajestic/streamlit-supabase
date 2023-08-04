import streamlit as st
import os
from supabase import create_client, Client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def main():
    st.title('Supabase User Authentication')

    # Initialize session_state if not present
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Check if the user is authenticated
    user = st.session_state.user
    if user:
        st.write(f'Logged in as: {user["email"]}')
    else:
        # Show login form
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        login_btn = st.button('Login', on_click=login, args=(email, password))

        # Show signup form
        if not login_btn:
            st.text('Or')
            new_email = st.text_input('New Email')
            new_password = st.text_input('New Password', type='password')
            signup_btn = st.button('Signup', on_click=signup, args=(new_email, new_password))

def login(email, password):
    # Login with email and password
    data = supabase.auth.sign_in_with_password({"email": email, "password": password})

def signup(email, password):
    # Signup with email and password
    res = supabase.auth.sign_up({"email": email, "password": password})

if __name__ == '__main__':
    main()
