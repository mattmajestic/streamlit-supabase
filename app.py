import streamlit as st
import os
from supabase import create_client

# Set page title and favicon to an emoji
st.set_page_config(page_title="Streamlit Supabase", page_icon="🔒")

# Supabase setup
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def show_user_info(user):
    with st.expander('User Information'):
        st.success(f'🎉 Logged in as: {user["email"]}')
        if 'full_name' in user.get("user_metadata", {}):
            st.write(f'Username: {user["user_metadata"]["full_name"]}')

def show_login_signup_forms():
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

def upload_file():
    file = st.file_uploader('Choose a file')
    if file is not None:
        destination = file.name
        with open(destination, 'wb') as f:
            f.write(file.read())
        
        res = supabase.storage.from_('streamlit-supabase').upload(destination, destination)
        st.success('🚀 File uploaded successfully!')
        
        os.remove(destination)

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

def main():
    st.title('Streamlit Supabase ')

    # Show the supabase content
    supabase_expander = st.expander("Supabase Backend 🚄 ")
    with supabase_expander:
        st.balloons()
        # Replace with supabase fetch
        st_db = supabase.table('streamlit').select("*").execute()
        st_df = pd.DataFrame(st_db.data)
        st.write("streamlit table hosted in Supabase ")
        st.dataframe(st_df)

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
    st.header('File Upload')
    upload_file()

    # README Documentation Expander
    with st.expander("README Documentation"):
        with open("README.md", "r") as readme_file:
            readme_content = readme_file.read()
        st.markdown(readme_content)

    # Show the author content
    author_expander = st.expander("Author's Gthub Projects 🌏")
    with author_expander:
        url = "https://raw.githubusercontent.com/mattmajestic/mattmajestic/main/README.md"
        response = requests.get(url)
        readme_content = response.text if response.status_code == 200 else ""
        iframe_html = f'<iframe srcdoc="{readme_content}</iframe>'
        st.markdown(iframe_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()