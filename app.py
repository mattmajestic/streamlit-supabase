import streamlit as st
import requests

def main():
    st.title("Supabase Auth Demo")

    st.header("Login")

    email_login = st.text_input("Email", key="email_login")
    password_login = st.text_input("Password", type="password", key="password_login")
    login_button = st.button("Login")

    if login_button:
        # Perform login logic here
        st.write(f"Logging in with email: {email_login}")

    st.header("Register")

    email_register = st.text_input("Email", key="email_register")
    password_register = st.text_input("Password", type="password", key="password_register")
    register_button = st.button("Register")

    if register_button:
        # Perform register logic here
        st.write(f"Registering with email: {email_register}")

if __name__ == "__main__":
    main()
