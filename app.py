import streamlit as st
import os
import supabase

# Fetch Supabase URL and key from environment variables
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = supabase.create_client(supabase_url, supabase_key)

def main():
    st.title('Supabase User Authentication')

    # Initialize session_state if not present
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Check if the user is authenticated
    user = st.session_state.user
    if user:
        st.write(f'Logged in as: {user["email"]}')
        st.button('Logout', on_click=logout)
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
    supabase_response = supabase_client.auth.sign_in(email, password)
    if not supabase_response['error']:
        st.session_state.user = supabase_response['user']
        st.experimental_rerun()

def signup(email, password):
    # Signup with email and password
    signup_data = {
        'email': email,
        'password': password
    }
    supabase_response = supabase_client.auth.sign_up(signup_data)
    if not supabase_response['error']:
        st.session_state.user = supabase_response['user']
        st.experimental_rerun()
        
def logout():
    # Logout user
    supabase_client.auth.sign_out()
    st.session_state.user = None
    st.experimental_rerun()

if __name__ == '__main__':
    main()
