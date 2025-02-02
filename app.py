import streamlit as st
import base64
import json

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyC6YllFBzRnUjFfIJhGjIkwMlGELuKs9YQ",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:62e7e9a543ba2f77dc8eee"
}

firebase_config_json = json.dumps(firebase_config)

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firebase Auth</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }}
        
        .auth-container {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }}
        
        .google-btn {{
            background-color: #4285f4;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
            transition: background-color 0.3s;
        }}
        
        .google-btn:hover {{
            background-color: #357abd;
        }}
        
        .status-message {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
        }}
        
        .info {{
            background-color: #e3f2fd;
            color: #1976d2;
        }}
        
        .success {{
            background-color: #e8f5e9;
            color: #2e7d32;
        }}
        
        .error {{
            background-color: #ffebee;
            color: #c62828;
        }}
    </style>
</head>
<body>
    <div class="auth-container">
        <h2>Firebase Authentication</h2>
        <div id="status-message" class="status-message info">Please log in</div>
        <button id="google-login" class="google-btn">
            Login with Google
        </button>
    </div>

    <!-- Firebase App (the core Firebase SDK) -->
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js"></script>
    <!-- Firebase Auth -->
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-auth-compat.js"></script>

    <script>
        // Initialize Firebase
        const firebaseConfig = {firebase_config_json};
        firebase.initializeApp(firebaseConfig);

        // Get DOM elements
        const loginButton = document.getElementById('google-login');
        const statusMessage = document.getElementById('status-message');

        // Set up Google Auth Provider
        const provider = new firebase.auth.GoogleAuthProvider();

        // Handle login
        loginButton.addEventListener('click', () => {{
            statusMessage.textContent = 'Initiating login...';
            statusMessage.className = 'status-message info';
            
            firebase.auth().signInWithPopup(provider)
                .then((result) => {{
                    const user = result.user;
                    statusMessage.textContent = `Welcome, ${{user.email}}!`;
                    statusMessage.className = 'status-message success';
                    loginButton.textContent = 'Logout';
                }})
                .catch((error) => {{
                    console.error('Auth Error:', error);
                    statusMessage.textContent = `Error: ${{error.message}}`;
                    statusMessage.className = 'status-message error';
                }});
        }});

        // Auth state observer
        firebase.auth().onAuthStateChanged((user) => {{
            if (user) {{
                statusMessage.textContent = `Logged in as: ${{user.email}}`;
                statusMessage.className = 'status-message success';
                loginButton.textContent = 'Logout';
            }} else {{
                statusMessage.textContent = 'Please log in';
                statusMessage.className = 'status-message info';
                loginButton.textContent = 'Login with Google';
            }}
        }});
    </script>
</body>
</html>
"""

# Set up Streamlit page
st.set_page_config(page_title="Firebase Auth", layout="wide")

# Convert HTML to base64
b64_html = base64.b64encode(html_code.encode()).decode()

# Create iframe with necessary permissions
iframe_code = f'''
    <iframe 
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-modals"
        style="width:100%; height:100vh; border:none;"
        src="data:text/html;base64,{b64_html}"
    ></iframe>
'''

# Hide Streamlit components
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            margin: 0;
            padding: 0;
        }
        iframe {
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Display the iframe
st.markdown(iframe_code, unsafe_allow_html=True)
