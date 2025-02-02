import streamlit as st
import streamlit.components.v1 as components

# Your Firebase configuration (from your provided credentials)
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

# Create an HTML snippet that initializes Firebase and triggers Google sign-in
html_code = f"""
<!DOCTYPE html>
<html>
  <head>
    <!-- Load Firebase SDKs -->
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js"></script>
    <script>
      // Initialize Firebase with your config
      const firebaseConfig = {firebase_config};
      firebase.initializeApp(firebaseConfig);
      
      // Function to trigger Google sign-in
      function googleSignIn() {{
          var provider = new firebase.auth.GoogleAuthProvider();
          firebase.auth().signInWithPopup(provider)
            .then((result) => {{
                // Retrieve the Google access token
                var token = result.credential.accessToken;
                // For demonstration, display the token in the page
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

# Embed the HTML/JS code into your Streamlit app
components.html(html_code, height=500)
