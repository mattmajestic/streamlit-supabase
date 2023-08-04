from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Fetch Supabase URL and key from environment variables
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = supabase.Client(supabase_url, supabase_key)

def create_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/signup'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    return response.json()

def login_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/token'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    return response.json()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    response = create_user(email, password)
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    response = login_user(email, password)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
