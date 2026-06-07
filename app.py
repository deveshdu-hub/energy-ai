import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 FUTUREHQ.IN - STREAMLIT APP (STABLE PRODUCTION VERSION)
# ═══════════════════════════════════════════════════════════════════════════════

# Configure Streamlit (MUST BE FIRST STREAMLIT CALL)
st.set_page_config(
    page_title="FutureHQ - India Energy AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Securely configure the Gemini API using Streamlit Secrets or Local Env
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")

# CSS Styling for Premium Dark UI Layout
st.markdown("""
    <style>
    /* Main Theme */
    body {
        background-color: #0a0e27;
        color: #ffffff;
    }
    .main {
        background-color: #050816;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #8B5CF6, #00F0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 20px;
    }
    h2 {
        color: #00F0FF;
        font-size: 32px;
        font-weight: 700;
    }
    h3 {
        color: #8B5CF6;
        font-size: 24px;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #8B5CF6, #00F0FF);
        color: white;
        border: none;
        padding: 12px 32px;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
        transform: translateY(-2px);
    }
    
    /* Input Boxes */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(139, 92, 246, 0.1) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Custom Alerts */
    .success-box {
        background-color: rgba(50, 255, 0, 0.1);
        border: 1px solid #32FF00;
        border-radius: 8px;
        padding: 15px;
        color: #32FF00;
        margin: 10px 0;
    }
    .data-highlight {
        color: #32FF00;
        font-weight: 700;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

# ═══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("# ⚡ FutureHQ")
    st.markdown("## Your ₹20L Energy Decision. In 2 Minutes. Actually Smart.")
    st.markdown("""
    **Tired of making energy decisions BLIND?**
    
    AI-powered guidance for:
    - 🚗 EV Infrastructure (40% YoY growth)
    - ☀️ Solar Energy (30% YoY growth)  
    - 🔋 Battery & Clean Tech (50% YoY growth)
    """)

with col2:
    st.metric("EV Growth", "40%", "YoY")
    st.metric("Solar Growth", "30%", "YoY")
    st.metric("Battery Growth", "50%", "YoY")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 AI Chat",
    "💰 Investment Guide",
    "📊 Market Data",
    "🎯 Subsidy Checker",
    "📱 Contact"
])

# 🛠️ TAB 1: AI CHAT WINDOW
with tab1:
    st.subheader("🤖 Ask Anything About Energy")
    
    # Render chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User Input Field
    user_input = st.chat_input("Ask about EV, Solar, Battery, or subsidies...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("🤖 Processing energy insights..."):
                try:
                    system_context = (
                        "You are FutureHQ, an AI expert on India's energy sector. "
                        "Always use Indian context and format numbers in Lakhs/Crores. "
                        "Provide sharp, data-driven answers restricted to under 150 words."
                    )
                    
                    # Correct baseline configuration for stable endpoints
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=system_context
                    )
                    
                    response = model.generate_content(user_input)
                    assistant_message = response.text
                    
                    st.markdown(assistant_message)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                    
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")

# 🛠️ TAB 2: INVESTMENT GUIDE
with tab2:
    st.subheader("💰 Energy Investment Opportunities")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚗 EV Charging\n**Investment:** ₹50K - ₹5L\n**ROI:** 15-25% annually\n**Growth:** 40% YoY")
    with col2:
        st.markdown("### ☀️ Solar Energy\n**Investment:** ₹2 - ₹5L\n**ROI:** 12-20% annually\n**Growth:** 30% YoY")
    with col3:
        st.markdown("### 🔋 Battery Tech\n**Investment:** ₹20L - ₹1Cr\n**ROI:** 20-35% annually\n**Growth:** 50% YoY")
    
    st.markdown("---")
    st.subheader("📈 Quick ROI Estimator")
    inv_type = st.selectbox("Select Segment:", ["EV Charging", "Solar", "Battery Storage"])
    amount = st.slider("Investment Amount (₹)", 50000, 5000000, 500000, step=50000)
    years = st.slider("Horizon (Years)", 1, 15, 5)
    
    rates = {"EV Charging": 0.22, "Solar": 0.16, "Battery Storage": 0.28}
    final_val = amount * ((1 + rates[inv_type]) ** years)
    st.metric("Projected Value", f"₹{final_val:,.0f}", f"+₹{final_val-amount:,.0f} Net Profit")

# 🛠️ TAB 3: MARKET DATA
with tab3:
    st.subheader("📊 India Energy Market Matrix")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🇮🇳 Segment Targets (2030)\n- **EV Target:** 30% of total vehicle share\n- **Solar Target:** 500 GW base integration")
    with col2:
        st.markdown("### 🎯 Active Allocations\n- **National Green Hydrogen:** ₹19,744 Cr\n- **Manufacturing PLI:** ₹10,000 Cr")
        
    chart_data = pd.DataFrame({
        'Sector': ['EV', 'Solar', 'Renewables', 'Battery'],
        'Growth Rate (%)': [40, 30, 35, 50]
    })
    st.bar_chart(chart_data.set_index('Sector'), color='#00F0FF')

# 🛠️ TAB 4: SUBSIDY CHECKER
with tab4:
    st.subheader("🎯 Check Your Subsidy Eligibility")
    col1, col2 = st.columns(2)
    state = col1.selectbox("Select State:", ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Gujarat", "Other"])
    roof_area = col2.number_input("Available Roof Area (sq meters):", min_value=10, value=50)
    
    if st.button("Calculate Subsidies"):
        capacity = roof_area * 1.2
        est_subsidy = capacity * 1000 * 28
        st.markdown(f"""
        <div class="success-box">
        <h3>✅ Estimated Allocation Profile</h3>
        <ul>
            <li>System Capacity Potential: <span class="data-highlight">{capacity:.1f} kW</span></li>
            <li>Approximate Government Subsidy Wallet: <span class="data-highlight">₹{est_subsidy:,.0f}</span></li>
        </ul>
        <p>Apply via the National Solar Rooftop Portal using your verified electricity consumer number.</p>
        </div>
        """, unsafe_allow_html=True)

# 🛠️ TAB 5: LEAD CAPTURE CONTACT FORM
with tab5:
    st.subheader("📱 Request Professional Execution Plan")
    with st.form("lead_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        interest = st.selectbox("Primary Focus:", ["EV Infrastructure", "Commercial Solar", "Residential Solar", "Storage"])
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if name and email and phone:
                st.markdown(f"""
                <div class="success-box">
                🎉 Request logged for <b>{name}</b>! An energy specialist will reach out to <b>{email}</b> within 24 business hours.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please fill in all mandatory identity fields.")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns(3)
f_col1.markdown("### 🌍 FutureHQ\nIndia's Premium Energy Decision Platform")
f_col2.markdown("### 📞 Connect\n📧 iefuture108@gmail.com\n🌐 [@india_energy_future__ev_ai](https://instagram.com/india_energy_future__ev_ai)")
f_col3.markdown("### ⚡ Architecture\nEngineered with Gemini AI & Streamlit")

st.caption("FutureHQ © 2026 | Smart Energy Strategy Decisions for India")
