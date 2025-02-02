import streamlit as st
import base64

# Firebase configuration (ensure these values match your Firebase project)


# Define the HTML content for the dashboard
html_code = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Priest Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
</head>

<body>
    <div id="login-screen" class="d-flex justify-content-center align-items-center vh-100 bg-light">
        <div class="card p-4 shadow-lg" style="width: 400px;">
            <h4 class="card-title text-center">Login</h4>
            <div class="card-body">
                <button id="login-button" class="btn btn-primary w-100">Login with Google</button>
            </div>
        </div>
    </div>

    <div id="dashboard" class="d-none">
        <div class="d-flex">
            <!-- Sidebar -->
            <div class="bg-light border-end" id="sidebar-wrapper">
                <div class="sidebar-heading text-center py-4 primary-text fs-4 fw-bold text-uppercase border-bottom">Priest Profile</div>
                <div class="list-group list-group-flush my-3">
                    <div class="text-center my-3">
                        <img id="priest-photo" src="" alt="Priest Photo" class="rounded-circle" width="100" height="100">
                        <h5 id="priest-name" class="mt-2">Name</h5>
                        <button id="edit-profile" class="btn btn-outline-primary btn-sm mt-2">Edit Profile</button>
                        <button id="logout-button" class="btn btn-danger btn-sm mt-2">Logout</button>
                    </div>
                </div>
            </div>

            <!-- Page Content -->
            <div id="page-content-wrapper" class="w-100">
                <nav class="navbar navbar-expand-lg navbar-light bg-light py-3 px-4">
                    <button class="btn btn-primary" id="menu-toggle">Toggle Menu</button>
                </nav>
                <div class="container-fluid px-4">
                    <h2 class="mt-4">Today’s Orders</h2>
                    <div id="orders-container" class="row mt-4"></div>
                    <h2 class="mt-4">Order History</h2>
                    <div id="history-container" class="row mt-4"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Profile Modal -->
    <div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="profileModalLabel">Edit Profile</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="profile-form">
                        <div class="mb-3">
                            <label for="profile-name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="profile-name" required>
                        </div>
                        <div class="mb-3">
                            <label for="profile-photo" class="form-label">Photo URL</label>
                            <input type="text" class="form-control" id="profile-photo">
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script type="module">
        import {{ initializeApp }} from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js';
        import {{ getAuth, signInWithPopup, signOut, GoogleAuthProvider, onAuthStateChanged }} from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js';
        import {{ getFirestore, doc, getDoc, setDoc, updateDoc, collection, query, where, onSnapshot }} from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-firestore.js';

        const firebaseConfig = {
            apiKey: "AIzaSyC6YllFBzRnUjFfIJhGjIkwMlGELuKs9YQ",
            authDomain: "nothing-d3af4.firebaseapp.com",
            databaseURL: "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "nothing-d3af4",
            storageBucket: "nothing-d3af4.firebasestorage.app",
            messagingSenderId: "7155955115",
            appId: "1:7155955115:web:62e7e9a543ba2f77dc8eee",
            measurementId: "G-JNLGNYK8DM"
        };


        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getFirestore(app);
        const provider = new GoogleAuthProvider();

        const loginScreen = document.getElementById('login-screen');
        const dashboard = document.getElementById('dashboard');
        const loginButton = document.getElementById('login-button');
        const logoutButton = document.getElementById('logout-button');
        const editProfileButton = document.getElementById('edit-profile');
        const priestPhoto = document.getElementById('priest-photo');
        const priestName = document.getElementById('priest-name');
        const profileModal = new bootstrap.Modal(document.getElementById('profileModal'));
        const profileForm = document.getElementById('profile-form');
        const profileNameInput = document.getElementById('profile-name');
        const profilePhotoInput = document.getElementById('profile-photo');
        const ordersContainer = document.getElementById('orders-container');
        const historyContainer = document.getElementById('history-container');

        let currentUser = null;

        loginButton.addEventListener('click', async () => {{
            try {{
                const result = await signInWithPopup(auth, provider);
                currentUser = result.user;
                await loadUserProfile(currentUser.uid);
            }} catch (error) {{
                console.error('Login Error:', error);
                Swal.fire('Login Failed', 'Unable to login. Please try again.', 'error');
            }}
        }});

        logoutButton.addEventListener('click', async () => {{
            try {{
                await signOut(auth);
                currentUser = null;
                switchToLoginScreen();
            }} catch (error) {{
                console.error('Logout Error:', error);
            }}
        }});

        editProfileButton.addEventListener('click', () => {{
            if (currentUser) {{
                profileNameInput.value = priestName.textContent;
                profilePhotoInput.value = priestPhoto.src;
                profileModal.show();
            }}
        }});

        profileForm.addEventListener('submit', async (event) => {{
            event.preventDefault();
            try {{
                const updatedName = profileNameInput.value;
                const updatedPhoto = profilePhotoInput.value;
                priestName.textContent = updatedName;
                priestPhoto.src = updatedPhoto;
                const userRef = doc(db, 'users', currentUser.uid);
                await updateDoc(userRef, {{ name: updatedName, photo: updatedPhoto }});
                profileModal.hide();
                Swal.fire('Profile Updated', 'Your profile has been updated successfully.', 'success');
            }} catch (error) {{
                console.error('Profile Update Error:', error);
                Swal.fire('Error', 'Failed to update profile.', 'error');
            }}
        }});

        onAuthStateChanged(auth, async (user) => {{
            if (user) {{
                currentUser = user;
                await loadUserProfile(user.uid);
                loadOrders();
                loadOrderHistory();
            }} else {{
                switchToLoginScreen();
            }}
        }});

        const loadUserProfile = async (uid) => {{
            try {{
                const userRef = doc(db, 'users', uid);
                const userDoc = await getDoc(userRef);
                if (userDoc.exists()) {{
                    const userData = userDoc.data();
                    priestName.textContent = userData.name;
                    priestPhoto.src = userData.photo;
                }} else {{
                    await setDoc(userRef, {{ name: currentUser.displayName, photo: currentUser.photoURL }});
                    priestName.textContent = currentUser.displayName;
                    priestPhoto.src = currentUser.photoURL;
                }}
                switchToDashboard();
            }} catch (error) {{
                console.error('Load User Profile Error:', error);
            }}
        }};

        const loadOrders = () => {{
            const bookingsRef = collection(db, 'bookings');

            onSnapshot(bookingsRef, (snapshot) => {{
                ordersContainer.innerHTML = '';
                snapshot.forEach((doc) => {{
                    const booking = doc.data();
                    const cartItems = booking.cartItems || [];

                    cartItems.forEach((item) => {{
                        if (!booking.accepted) {{
                            const col = document.createElement('div');
                            col.className = 'col-md-4 mb-4';
                            col.innerHTML = `
                                <div class="card p-3 shadow-sm">
                                    <img src="${{item.image || ''}}" alt="${{item.title || 'No title'}}" class="img-fluid mb-2">
                                    <h5>${{item.title || 'No title'}}</h5>
                                    <p>${{item.description || 'No description available'}}</p>
                                    <p><strong>Price:</strong> ${{item.price || 'N/A'}}</p>
                                    <p><strong>Date:</strong> ${{booking.date || 'N/A'}}</p>
                                    <p><strong>Time:</strong> ${{booking.time || 'N/A'}}</p>
                                    <p><strong>Location:</strong> ${{booking.location || 'N/A'}}</p>
                                    <p><strong>Contact:</strong> <em>Visible upon acceptance</em></p>
                                    <button class="btn btn-primary btn-sm" onclick="acceptOrder('${{doc.id}}')">Accept</button>
                                </div>
                            `;
                            ordersContainer.appendChild(col);
                        }}
                    }});
                }});
            }});
        }};

        const loadOrderHistory = () => {{
            const bookingsRef = collection(db, 'bookings');

            onSnapshot(bookingsRef, (snapshot) => {{
                historyContainer.innerHTML = '';
                snapshot.forEach((doc) => {{
                    const booking = doc.data();
                    const cartItems = booking.cartItems || [];

                    if (booking.accepted) {{
                        cartItems.forEach((item) => {{
                            const col = document.createElement('div');
                            col.className = 'col-md-4 mb-4';
                            col.innerHTML = `
                                <div class="card p-3 shadow-sm">
                                    <img src="${{item.image || ''}}" alt="${{item.title || 'No title'}}" class="img-fluid mb-2">
                                    <h5>${{item.title || 'No title'}}</h5>
                                    <p>${{item.description || 'No description available'}}</p>
                                    <p><strong>Price:</strong> ${{item.price || 'N/A'}}</p>
                                    <p><strong>Date:</strong> ${{booking.date || 'N/A'}}</p>
                                    <p><strong>Time:</strong> ${{booking.time || 'N/A'}}</p>
                                    <p><strong>Location:</strong> ${{booking.location || 'N/A'}}</p>
                                    <p><strong>Contact:</strong> ${{booking.contactNumber || 'N/A'}}</p>
                                </div>
                            `;
                            historyContainer.appendChild(col);
                        }});
                    }}
                }});
            }});
        }};

        const switchToLoginScreen = () => {{
            loginScreen.classList.remove('d-none');
            dashboard.classList.add('d-none');
        }};

        const switchToDashboard = () => {{
            loginScreen.classList.add('d-none');
            dashboard.classList.remove('d-none');
        }};

        window.acceptOrder = async (orderId) => {{
            try {{
                const orderRef = doc(db, 'bookings', orderId);
                await updateDoc(orderRef, {{ accepted: true }});
                Swal.fire('Accepted!', 'You have accepted the order.', 'success');
            }} catch (error) {{
                console.error('Accept Order Error:', error);
                Swal.fire('Error', 'Failed to accept the order.', 'error');
            }}
        }};

        window.rejectOrder = async (orderId) => {{
            try {{
                const orderRef = doc(db, 'bookings', orderId);
                await updateDoc(orderRef, {{ accepted: false }});
                Swal.fire('Rejected!', 'You have rejected the order.', 'info');
            }} catch (error) {{
                console.error('Reject Order Error:', error);
                Swal.fire('Error', 'Failed to reject the order.', 'error');
            }}
        }};
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
"""

# Encode the HTML content as a base64 string.
b64_html = base64.b64encode(html_code.encode()).decode()

# Create an iframe that loads the HTML from the base64 data URL.
iframe_code = f'''
<iframe sandbox="allow-scripts allow-same-origin allow-popups" 
        style="width:100%; height:100vh; border:none;" 
        src="data:text/html;base64,{b64_html}">
</iframe>
'''

# Render the iframe using st.markdown with unsafe_allow_html.
st.markdown(iframe_code, unsafe_allow_html=True)
