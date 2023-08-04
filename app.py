import streamlit as st
import os
import base64
import requests
import supabase

# Fetch Supabase URL and key from environment variables
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = supabase.create_client(supabase_url, supabase_key)

def main():
    st.title('Supabase File Upload')

    # Get the file URLs or file uploads from the user
    uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            st.write(f'File name: {file.name}')

            # Read file content
            file_content = file.read()

            # Get the file name and extension
            file_name = file.name
            file_ext = file_name.split('.')[-1]

            # Encode file content in base64
            file_base64 = base64.b64encode(file_content).decode()

            # Upload file to Supabase
            file_metadata = {
                'name': file_name,
                'type': f'application/csv'  # You can change the content type based on the file type you are uploading
            }
            supabase_response = supabase_client.storage().upload(file_name, file_base64, file_metadata)
            if supabase_response['error']:
                st.error(f'File upload failed for {file.name}.')
            else:
                st.success(f'File {file.name} uploaded successfully.')

if __name__ == '__main__':
    main()
