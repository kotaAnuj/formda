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
        // Wait for DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', async () => {{
            try {{
                // Import Firebase modules
                const {{ initializeApp }} = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js');
                const {{ 
                    getAuth, 
                    signInWithPopup, 
                    GoogleAuthProvider,
                    onAuthStateChanged,
                    signOut 
                }} = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js');

                // Initialize Firebase
                const firebaseConfig = {firebase_config_json};
                const app = initializeApp(firebaseConfig);
                const auth = getAuth(app);
                const provider = new GoogleAuthProvider();

                // Get DOM elements
                const loginButton = document.getElementById('loginButton');
                const logoutButton = document.getElementById('logoutButton');
                const loginStatus = document.getElementById('loginStatus');

                let isAuthInProgress = false;

                // Login function with debounce
                loginButton.addEventListener('click', async () => {{
                    if (isAuthInProgress) return;
                    
                    try {{
                        isAuthInProgress = true;
                        loginStatus.innerHTML = '<div class="alert alert-info">Logging in...</div>';
                        loginButton.disabled = true;
                        
                        const result = await signInWithPopup(auth, provider);
                        console.log('Login successful:', result.user.email);
                    }} catch (error) {{
                        console.error('Login error:', error);
                        if (error.code === 'auth/cancelled-popup-request') {{
                            loginStatus.innerHTML = '<div class="alert alert-warning">Login cancelled. Please try again.</div>';
                        }} else if (error.code === 'auth/popup-blocked') {{
                            loginStatus.innerHTML = '<div class="alert alert-warning">Popup blocked. Please allow popups for this site.</div>';
                        }} else {{
                            loginStatus.innerHTML = `<div class="alert alert-danger">Login error: ${{error.message}}</div>`;
                        }}
                    }} finally {{
                        isAuthInProgress = false;
                        loginButton.disabled = false;
                    }}
                }});

                // Logout function
                logoutButton.addEventListener('click', async () => {{
                    try {{
                        await signOut(auth);
                        console.log('Logout successful');
                    }} catch (error) {{
                        console.error('Logout error:', error);
                        loginStatus.innerHTML = `<div class="alert alert-danger">Logout error: ${{error.message}}</div>`;
                    }}
                }});

                // Auth state observer
                onAuthStateChanged(auth, (user) => {{
                    if (user) {{
                        loginStatus.innerHTML = `
                            <div class="alert alert-success">
                                <img src="${{user.photoURL}}" alt="Profile" style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">
                                Logged in as: ${{user.email}}
                            </div>
                        `;
                        loginButton.classList.add('d-none');
                        logoutButton.classList.remove('d-none');
                    }} else {{
                        loginStatus.innerHTML = '<div class="alert alert-warning">Not logged in</div>';
                        loginButton.classList.remove('d-none');
                        logoutButton.classList.add('d-none');
                    }}
                }});

            }} catch (error) {{
                console.error('Firebase initialization error:', error);
                document.getElementById('loginStatus').innerHTML = 
                    '<div class="alert alert-danger">Failed to initialize Firebase. Please check your configuration.</div>';
            }}
        }});
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Streamlit app
st.set_page_config(page_title="Firebase Auth", layout="wide")

# Convert HTML to base64
b64_html = base64.b64encode(html_code.encode()).decode()

# Create iframe with necessary permissions
iframe_code = f'''
    <iframe 
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        style="width:100%; height:600px; border:none;"
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
    </style>
""", unsafe_allow_html=True)

# Display the iframe
st.markdown(iframe_code, unsafe_allow_html=True)
