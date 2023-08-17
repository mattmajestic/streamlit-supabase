import streamlit as st
import os
from supabase import create_client, Client
from io import BytesIO

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def main():
    st.title('Supabase User Authentication and File Upload')

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

    # File Upload Section
    st.header('File Upload')
    file = st.file_uploader('Choose a file')

    if file is not None:
        bucket_files = supabase.storage.list_buckets()
        st.write(bucket_files)
        destination = file.name
        # Save the uploaded file temporarily
        with open(destination, 'wb') as f:
            f.write(file.read())
        
        res = supabase.storage.from_('streamlit-supabase').upload(destination, destination)
        st.write('File uploaded successfully!')
        
        # Remove the temporary file
        os.remove(destination)
            
def login(email, password):
    # Login with email and password
    data = supabase.auth.sign_in_with_password({"email": email, "password": password})

def signup(email, password):
    # Signup with email and password
    res = supabase.auth.sign_up({"email": email, "password": password})

if __name__ == '__main__':
    main()
