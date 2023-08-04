import streamlit as st
import requests

supabase_url = "https://your-supabase-url.supabase.co"
supabase_key = "your-supabase-api-key"

@st.cache(allow_output_mutation=True)
def get_auth_headers():
    return {
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
    }

def signup_user(email, password):
    url = f"{supabase_url}/auth/v1/signup"
    data = {
        "email": email,
        "password": password,
    }
    response = requests.post(url, json=data, headers=get_auth_headers())
    return response

def login_user(email, password):
    url = f"{supabase_url}/auth/v1/token"
    data = {
        "grant_type": "password",
        "email": email,
        "password": password,
    }
    response = requests.post(url, data=data, headers=get_auth_headers())
    return response

def logout_user(token):
    url = f"{supabase_url}/auth/v1/logout"
    headers = {
        **get_auth_headers(),
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(url, headers=headers)
    return response

def main():
    st.title("Supabase Authentication")

    st.subheader("Sign Up")
    email_signup = st.text_input("Email")
    password_signup = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        response = signup_user(email_signup, password_signup)
        if response.status_code == 200:
            st.success("Sign up successful!")
        else:
            st.error("Sign up failed. Please try again.")

    st.subheader("Log In")
    email_login = st.text_input("Email")
    password_login = st.text_input("Password", type="password")
    if st.button("Log In"):
        response = login_user(email_login, password_login)
        if response.status_code == 200:
            st.success("Log in successful!")
        else:
            st.error("Log in failed. Please check your credentials.")

    st.subheader("Log Out")
    token = st.text_input("Token")
    if st.button("Log Out"):
        response = logout_user(token)
        if response.status_code == 200:
            st.success("Log out successful!")
        else:
            st.error("Log out failed. Please check your token.")

if __name__ == "__main__":
    main()
