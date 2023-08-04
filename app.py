import streamlit as st
import requests
import os
import base64
import supabase

# Fetch Supabase URL and key from environment variables
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = supabase.Client(supabase_url, supabase_key)

def main():
    st.title("Supabase Auth and Bucket Storage Demo")

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

    st.header("Bucket Storage")

    file_upload = st.file_uploader("Choose a file to upload")

    if file_upload:
        # Encode the file to base64
        file_data = file_upload.read()
        file_data_encoded = base64.b64encode(file_data).decode()

        # Upload the file to Supabase bucket
        file_name = os.path.basename(file_upload.name)
        file_extension = os.path.splitext(file_name)[1]
        file_url = f"{supabase_url}/storage/v1/object/public/{file_name}"
        file_metadata = {
            "name": file_name,
            "file_extension": file_extension,
            "data": file_data_encoded
        }
        supabase_response = supabase_client.storage.from_url(file_url).upload(file_metadata)

        # Display the download URL
        if supabase_response["data"]:
            download_url = supabase_response["data"]["url"]
            st.success("File uploaded successfully!")
            st.markdown(f"**Download URL:** [Download]({download_url})")
        else:
            st.error("Error uploading file.")

if __name__ == "__main__":
    main()
