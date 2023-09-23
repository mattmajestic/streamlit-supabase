import streamlit as st
import streamlit.components.v1 as components
import os
from supabase import create_client
import pandas as pd
import requests
import docker
import subprocess
import platform
import distro
import uuid
from datetime import datetime

# Supabase setup
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

r = requests.get(f'https://docs.google.com/spreadsheet/ccc?key=1ORu0GIhEBfyEtUr9GGFtSg_0QaxB2LuHEvxSpgSaZQs&output=csv')
open('dataset.csv', 'wb').write(r.content)
feedback_df = pd.read_csv('dataset.csv')

def show_user_info(user):
    with st.expander('User Information'):
        st.success(f'🎉 Logged in as: {user["email"]}')
        if 'full_name' in user.get("user_metadata", {}):
            st.write(f'Username: {user["user_metadata"]["full_name"]}')

def is_docker_installed():
    try:
        subprocess.check_output(["docker", "--version"])
        return True
    except FileNotFoundError:
        return False

def show_login_signup_forms():
    col1, col2 = st.columns(2)
    with col1:
        with st.expander('Login 🔒'):
            email = st.text_input('Email', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')
            login_btn = st.button('Login', on_click=login, args=(email, password))
    with col2:
        with st.expander('Sign Up 📝'):
            new_email = st.text_input('Email', key='signup_email')
            new_password = st.text_input('Password', type='password', key='signup_password')
            signup_btn = st.button('Sign Up', on_click=signup, args=(new_email, new_password))

def upload_file():
    file = st.file_uploader('Choose a file')
    if file is not None:
        destination = file.name
        with open(destination, 'wb') as f:
            f.write(file.read())
        
        res = supabase.storage.from_('streamlit-supabase').upload(destination, destination)
        st.success('🚀 File uploaded successfully!')
        
        os.remove(destination)

def streamlit_supabase_session():
    new_id = str(uuid.uuid4())
    time_now = datetime.now().isoformat()
    response = supabase.table("streamlit_supabase_session").insert([{"id": new_id, "created_at": time_now}]).execute()

def login(email, password):
    data = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if 'user' in data:
        st.session_state.user = data['user']
        show_user_info(data['user'])
        st.success("🎉 Login successful!")
    else:
        st.warning("Login failed. Please check your credentials.")

def signup(email, password):
    res = supabase.auth.sign_up({"email": email, "password": password})
    if res['user']:
        st.success("🎉 Signup successful!")
    else:
        st.warning("Signup failed. Please try again.")

# Set page title and favicon to an emoji
st.set_page_config(page_title="Streamlit Supabase", page_icon="🔒")

def main():
    st.title('Streamlit Supabase 🔒')

    # Store Session Info in Supabase
    streamlit_supabase_session()

    # README Documentation Expander
    with st.expander("README Documentation 📝"):
        with open("README.md", "r") as readme_file:
            readme_content = readme_file.read()
        st.write("")
        st.markdown(readme_content)
        os_platform = platform.system()
        distribution_info = distro.linux_distribution(full_distribution_name=False)
        if is_docker_installed():
            st.write(f"The operating system is: {os_platform} of distribution: {distribution_info[0]} {distribution_info[1]} with Docker installed 🐳")
        else:
            st.write(f"The operating system is: {os_platform} of distribution: {distribution_info[0]} {distribution_info[1]} without Docker installed 🐳")

        # Initialize session_state if not present
    if 'user' not in st.session_state:
        st.session_state.user = {}
    # Check if the user is authenticated
    user = st.session_state.user
    if user and 'email' in user:
        show_user_info(user)
    else:
        show_login_signup_forms()
    # File Upload Section
    st.header('File Upload 📂')
    upload_file()

    # Show the supabase content
    supabase_expander = st.expander("Supabase Backend 🚄 ")
    with supabase_expander:
        st.balloons()
        # Replace with supabase fetch
        st_db = supabase.table('streamlit_supabase_session').select("*").execute()
        st_df = pd.DataFrame(st_db.data)
        st.write("streamlit table hosted in Supabase ")
        st.dataframe(st_df)
        
    # Show the author content
    author_expander = st.expander("Author's Gthub Projects 🌏")
    with author_expander:
        url = "https://raw.githubusercontent.com/mattmajestic/mattmajestic/main/README.md"
        response = requests.get(url)
        readme_content = response.text if response.status_code == 200 else ""
        iframe_html = f'<iframe srcdoc="{readme_content}</iframe>'
        st.markdown(iframe_html, unsafe_allow_html=True)

        # Show the BTC Pay Server
    btc_expander = st.expander("Donate BTC 💸")
    with btc_expander:
        url = "https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC"
        link='Pay wit BTC [via this link](https://mainnet.demo.btcpayserver.org/api/v1/invoices?storeId=4r8DKKKMkxGPVKcW9TXB2eta7PTVzzs192TWM3KuY52e&price=100&currency=USD&defaultPaymentMethod=BTC)'
        st.markdown(link,unsafe_allow_html=True)
        components.iframe(url,width = 300,height = 500, scrolling=True)
    feedback_expander = st.expander("Give Feedback 🤝")
    with feedback_expander:
        st.dataframe(feedback_df)
        st.markdown('''<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfkcEBiOklswShRGok5hjJQ1UTuGcT-ZB-6gBx6ehLCjlrRIQ/viewform?embedded=true" width="640" height="2197" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>''', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
