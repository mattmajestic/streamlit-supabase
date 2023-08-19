import streamlit as st
import os
from supabase import create_client, Client
from io import BytesIO

# Set page title and favicon to an emoji
st.set_page_config(page_title="🚀 Streamlit Supabase", page_icon="🔒")

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def main():
    st.title('Streamlit Supabase')

    # Initialize session_state if not present
    if 'user' not in st.session_state:
        st.session_state.user = {}

    # Check if the user is authenticated
    user = st.session_state.user
    if user and 'email' in user:
        with st.expander('User Information'):
            st.success(f'🎉 Logged in as: {user["email"]}')
            if 'full_name' in user.get("user_metadata", {}):
                st.write(f'Username: {user["user_metadata"]["full_name"]}')
    else:
        # Show login and signup forms side by side in two expanders
        col1, col2 = st.columns(2)
        with col1:
            with st.expander('Login'):
                email = st.text_input('Email', key='login_email')
                password = st.text_input('Password', type='password', key='login_password')
                login_btn = st.button('Login', on_click=login, args=(email, password))
        with col2:
            with st.expander('Sign Up'):
                new_email = st.text_input('Email', key='signup_email')
                new_password = st.text_input('Password', type='password', key='signup_password')
                signup_btn = st.button('Sign Up', on_click=signup, args=(new_email, new_password))

    # File Upload Section
    st.header('File Upload')
    file = st.file_uploader('Choose a file')

    if file is not None:
        destination = file.name
        # Save the uploaded file temporarily
        with open(destination, 'wb') as f:
            f.write(file.read())
        
        res = supabase.storage.from_('streamlit-supabase').upload(destination, destination)
        st.success('🚀 File uploaded successfully!')
        
        # Remove the temporary file
        os.remove(destination)

    # README Documentation Expander
    with st.expander("README Documentation"):
        with open("README.md", "r") as readme_file:
            readme_content = readme_file.read()
        st.markdown(readme_content)
            
def login(email, password):
    # Login with email and password
    data = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if 'user' in data:
        st.session_state.user = data['user']
    else:
        st.warning("Login failed. Please check your credentials.")

def signup(email, password):
    # Signup with email and password
    res = supabase.auth.sign_up({"email": email, "password": password})

if __name__ == '__main__':
    main()
