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

# Convert firebase_config to JSON string
firebase_config_json = json.dumps(firebase_config)

# Simple HTML with just login functionality
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firebase Auth</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6 text-center">
                <h2>Firebase Authentication</h2>
                <div id="loginStatus" class="mt-3"></div>
                <button id="loginButton" class="btn btn-primary mt-3">Login with Google</button>
                <button id="logoutButton" class="btn btn-danger mt-3 d-none">Logout</button>
            </div>
        </div>
    </div>

    <script type="module">
        // Import Firebase modules
        import {{ initializeApp }} from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js';
        import {{ 
            getAuth, 
            signInWithPopup, 
            GoogleAuthProvider,
            onAuthStateChanged,
            signOut 
        }} from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js';

        // Initialize Firebase
        const firebaseConfig = {firebase_config_json};
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const provider = new GoogleAuthProvider();

        // Get DOM elements
        const loginButton = document.getElementById('loginButton');
        const logoutButton = document.getElementById('logoutButton');
        const loginStatus = document.getElementById('loginStatus');

        // Login function
        loginButton.addEventListener('click', async () => {{
            try {{
                const result = await signInWithPopup(auth, provider);
                console.log('Login successful:', result.user.email);
            }} catch (error) {{
                console.error('Login error:', error);
                loginStatus.innerHTML = `<div class="alert alert-danger">Login failed: ${{error.message}}</div>`;
            }}
        }});

        // Logout function
        logoutButton.addEventListener('click', async () => {{
            try {{
                await signOut(auth);
                console.log('Logout successful');
            }} catch (error) {{
                console.error('Logout error:', error);
            }}
        }});

        // Auth state observer
        onAuthStateChanged(auth, (user) => {{
            if (user) {{
                loginStatus.innerHTML = `<div class="alert alert-success">Logged in as: ${{user.email}}</div>`;
                loginButton.classList.add('d-none');
                logoutButton.classList.remove('d-none');
            }} else {{
                loginStatus.innerHTML = '<div class="alert alert-warning">Not logged in</div>';
                loginButton.classList.remove('d-none');
                logoutButton.classList.add('d-none');
            }}
        }});
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Streamlit app
st.set_page_config(page_title="Firebase Auth", layout="centered")

# Convert HTML to base64
b64_html = base64.b64encode(html_code.encode()).decode()

# Create iframe with necessary permissions
iframe_code = f'''
    <iframe 
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        style="width:100%; height:400px; border:none;"
        src="data:text/html;base64,{b64_html}"
    ></iframe>
'''

# Hide Streamlit components
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Display the iframe
st.markdown(iframe_code, unsafe_allow_html=True)
