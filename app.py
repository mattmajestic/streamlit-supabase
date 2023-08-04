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
    st.title('Supabase File Upload')

    # Get the file URL from user
    file_url = st.text_input('Enter file URL:')
    if file_url:
        st.write(f'File URL: {file_url}')

        # Fetch file content from the URL
        response = requests.get(file_url)
        file_content = response.content

        # Get the file name and extension from the URL
        file_name = file_url.split('/')[-1]
        file_ext = file_name.split('.')[-1]

        # Encode file content in base64
        file_base64 = base64.b64encode(file_content).decode()

        # Upload file to Supabase
        file_metadata = {
            'name': file_name,
            'type': f'image/{file_ext}'
        }
        supabase_response = supabase_client.storage().upload(file_name, file_base64, file_metadata)
        if supabase_response['error']:
            st.error('File upload failed.')
        else:
            st.success('File uploaded successfully.')

if __name__ == '__main__':
    main()
