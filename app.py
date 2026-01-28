import streamlit as st
import pandas as pd
import plotly.express as px
from src import queries
from src.db import initialize_database

# =========================================================
# SAFE DATABASE INIT (RUN ONCE)
# =========================================================
if "db_initialized" not in st.session_state:
    initialize_database()
    st.session_state.db_initialized = True

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

# =========================================================
# GLOBAL STYLING
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }

h1, h2, h3 {
    color: #0f172a;
    font-weight: 700;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    border-left: 6px solid #22c55e;
}

.stButton > button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border-radius: 14px;
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #16a34a, #15803d);
}

footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "user" not in st.session_state:
    st.session_state.user = None

if "mode" not in st.session_state:
    st.session_state.mode = "home"

# =========================================================
# AUTHENTICATION
# =========================================================
if st.session_state.user is None:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png" width="70"/>
        <h1>Local Food Wastage Management System</h1>
    </div>
    """, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = queries.authenticate_user(username, password)
            if user:
                st.session_state.user = {
                    "user_id": user[0],
                    "username": user[1]
                }
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with signup_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if queries.create_user(new_user, new_pass):
                st.success("Account created. Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# =========================================================
# TOP BAR
# =========================================================
l, r = st.columns([6, 1])
with l:
    st.markdown(f"👋 **Welcome, {st.session_state.user['username']}**")
with r:
    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.mode = "home"
        st.rerun()

# =========================================================
# HOME DASHBOARD
# =========================================================
if st.session_state.mode == "home":
    st.markdown("""
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:30px;">
        <img src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png" width="90"/>
        <div>
            <h1>Local Food Wastage Management System</h1>
            <p style="color:#475569;font-size:1.1rem;">
                Connecting surplus food with people in need using data & technology
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_food = queries.total_food_available()
    food_types = queries.most_common_food_types()
    claim_status = queries.claim_status_percentage()

    c1, c2, c3 = st.columns(3)
    c1.metric("🍱 Total Food Available", total_food)
    c2.metric("🍽 Food Types", len(food_types))
    c3.metric("📦 Claim Status Types", len(claim_status))

    st.markdown("### 📊 Dashboard Insights")
    col1, col2 = st.columns(2)

    if food_types:
        df_food = pd.DataFrame(food_types, columns=["Food Type", "Count"])
        col1.plotly_chart(
            px.bar(
                df_food,
                x="Food Type",
                y="Count",
                color="Food Type",
                color_discrete_sequence=px.colors.qualitative.Set2,
                title="Food Type Distribution"
            ),
            use_container_width=True
        )

    if claim_status:
        df_claim = pd.DataFrame(claim_status, columns=["Status", "Percentage"])
        col2.plotly_chart(
            px.pie(
                df_claim,
                names="Status",
                values="Percentage",
                color="Status",
                color_discrete_map={
                    "Completed": "#22c55e",
                    "Pending": "#facc15",
                    "Cancelled": "#ef4444"
                },
                title="Claim Status Distribution"
            ),
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    top_recv = queries.top_receivers_by_claims()
    if top_recv:
        df_top = pd.DataFrame(top_recv, columns=["Receiver", "Claims"])
        col3.plotly_chart(
            px.bar(
                df_top,
                x="Receiver",
                y="Claims",
                color_discrete_sequence=["#2563eb"],
                title="Top Receivers"
            ),
            use_container_width=True
        )

    trend = queries.claims_over_time()
    if trend:
        df_trend = pd.DataFrame(trend, columns=["Date", "Claims"])
        col4.plotly_chart(
            px.line(
                df_trend,
                x="Date",
                y="Claims",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["#0ea5e9"],
                title="Claims Over Time"
            ),
            use_container_width=True
        )

    a1, a2 = st.columns(2)
    if a1.button("🍱 Provide Food"):
        st.session_state.mode = "provider"
        st.rerun()
    if a2.button("🤝 Receive Food"):
        st.session_state.mode = "receiver"
        st.rerun()

# =========================================================
# PROVIDER MODE
# =========================================================
elif st.session_state.mode == "provider":
    st.markdown("### 🍱 Provide Food")

    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1)
    expiry = st.date_input("Expiry Date")
    city = st.text_input("City")

    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])

    if st.button("Submit Food"):
        if not food_name or not city:
            st.warning("Please fill all fields")
        else:
            queries.create_food_listing(
                food_name, quantity, str(expiry),
                st.session_state.user["user_id"],
                "Individual", city, food_type, meal_type
            )
            st.success("Food listing added successfully")
            st.session_state.mode = "home"
            st.rerun()

    if st.button("⬅ Back to Home"):
        st.session_state.mode = "home"
        st.rerun()

# =========================================================
# RECEIVER MODE
# =========================================================
elif st.session_state.mode == "receiver":
    st.markdown("### 👤 Receiver Profile")

    receiver = queries.get_receiver_by_user(st.session_state.user["user_id"])

    name = st.text_input("Name", receiver[1] if receiver else "")
    city = st.text_input("City", receiver[2] if receiver else "")
    contact = st.text_input("Contact", receiver[3] if receiver else "")

    if st.button("Save Profile"):
        if receiver:
            queries.update_receiver(receiver[0], name, city, contact)
        else:
            queries.create_receiver(st.session_state.user["user_id"], name, city, contact)
        st.success("Profile saved")
        st.rerun()

    if not receiver:
        st.info("Save profile to view available food")
        st.stop()

    st.markdown("### 📍 Available Food Near You")

    food = queries.get_food_by_city(city)
    if not food:
        st.info("No food available in your city")
    else:
        df = pd.DataFrame(food, columns=[
            "Food ID", "Food", "Qty", "Expiry",
            "Provider ID", "City", "Food Type", "Meal Type"
        ])
        st.dataframe(df, use_container_width=True)

        ids = df[df["Qty"] > 0]["Food ID"].tolist()
        if ids:
            fid = st.selectbox("Select Food ID to Claim", ids)
            if st.button("Claim Food"):
                queries.create_claim(fid, receiver[0])
                st.success("Food claimed successfully")
                st.session_state.mode = "home"
                st.rerun()

    if st.button("⬅ Back to Home"):
        st.session_state.mode = "home"
        st.rerun()
