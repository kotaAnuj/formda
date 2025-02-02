import streamlit as st
import html

# Your Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyCadZIoYzIc_QhEkGjv86G4rjFwMASd5ig",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:3bd80618f9aff1a4dc8eee",
    "measurementId": "G-XSVGL2M8LL"
}

# Create the HTML code that loads Firebase and provides a Google sign‑in button.
html_code = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Firebase Google Sign-In</title>
    <!-- Load Firebase SDKs using compat versions for namespaced API -->
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js"></script>
    <script>
      // Initialize Firebase with your configuration
      const firebaseConfig = {firebase_config};
      firebase.initializeApp(firebaseConfig);
      
      // Function to trigger Google sign-in
      function googleSignIn() {{
          var provider = new firebase.auth.GoogleAuthProvider();
          firebase.auth().signInWithPopup(provider)
            .then((result) => {{
                // Retrieve the Google access token
                var token = result.credential.accessToken;
                // Display the token on the page
                document.getElementById('token').innerText = 'Access Token: ' + token;
            }})
            .catch((error) => {{
                console.error('Error during sign-in:', error);
                document.getElementById('token').innerText = 'Error: ' + error.message;
            }});
      }}
    </script>
  </head>
  <body>
    <h3>Auto Login with Google</h3>
    <!-- Button to trigger Google sign-in -->
    <button onclick="googleSignIn()">Login with Google</button>
    <p id="token">Not logged in</p>
  </body>
</html>
"""

# Escape the HTML code so it can safely be included in the srcdoc attribute.
encoded_html = html.escape(html_code, quote=True)

# Create an iframe with a sandbox attribute that allows scripts and same-origin access.
iframe_code = f'''
<iframe sandbox="allow-scripts allow-same-origin" style="width:100%; height:600px; border:none;" srcdoc="{encoded_html}"></iframe>
'''

# Render the iframe using st.markdown
st.markdown(iframe_code, unsafe_allow_html=True)
