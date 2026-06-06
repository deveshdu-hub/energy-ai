import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 FUTUREHQ.IN - STREAMLIT APP (GEMINI 100% FREE TIER READY)
# Deployment ready for share.streamlit.io
# ═══════════════════════════════════════════════════════════════════════════════

# Configure Streamlit
st.set_page_config(
    page_title="FutureHQ - India Energy AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
    <style>
    /* Main Theme */
    :root {
        --purple: #8B5CF6;
        --cyan: #00F0FF;
        --saffron: #FF6B35;
        --navy: #0F172A;
        --lime: #32FF00;
    }
    
    /* Dark Theme */
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
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(0, 240, 255, 0.1));
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Input Styling */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(139, 92, 246, 0.1) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border: 2px solid #00F0FF !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    /* Success/Error Messages */
    .success-box {
        background-color: rgba(50, 255, 0, 0.1);
        border: 1px solid #32FF00;
        border-radius: 8px;
        padding: 15px;
        color: #32FF00;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: rgba(255, 107, 53, 0.1);
        border: 1px solid #FF6B35;
        border-radius: 8px;
        padding: 15px;
        color: #FF6B35;
        margin: 10px 0;
    }
    
    /* Data Highlight */
    .data-highlight {
        color: #32FF00;
        font-weight: 700;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Securely configure the free Gemini API using Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "chat_initialized" not in st.session_state:
    st.session_state.chat_initialized = False

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
# MAIN INTERFACE - TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 AI Chat",
    "💰 Investment Guide",
    "📊 Market Data",
    "🎯 Subsidy Checker",
    "📱 Contact"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: AI CHATBOT (POWERED BY GEMINI FREE TIER)
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.subheader("🤖 Ask Anything About Energy")
    
    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input("Ask about EV, Solar, Battery, or subsidies...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    # Construct system prompt context
                    system_context = """You are FutureHQ, an AI expert on India's energy sector.
                        
                    You provide guidance on:
                    - EV Infrastructure (growing 40% YoY)
                    - Solar Energy (growing 30% YoY)  
                    - Battery Technology (growing 50% YoY)
                    - Government subsidies and schemes
                    - Investment ROI calculations
                    - Clean energy opportunities

                    Be conversational, authentic, and helpful. Use Indian context and numbers.
                    Provide specific data when possible. Keep responses under 200 words."""

                    # Initialize model with system instruction
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=system_context
                    )
                    
                    # Convert internal message format to Gemini's expected role structure
                    gemini_history = []
                    for msg in st.session_state.messages[:-1]:
                        # Map roles cleanly ('user' remains 'user', 'assistant' becomes 'model')
                        g_role = "user" if msg["role"] == "user" else "model"
                        gemini_history.append({"role": g_role, "parts": [msg["content"]]})
                    
                    # Start chat session with built history framework
                    chat = model.start_chat(history=gemini_history)
                    response = chat.send_message(user_input)
                    
                    assistant_message = response.text
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    st.markdown(assistant_message)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: INVESTMENT GUIDE
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.subheader("💰 Energy Investment Opportunities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚗 EV Charging
        
        **Investment:** ₹50K - ₹5L  
        **ROI:** 15-25% annually  
        **Growth:** 40% YoY
        
        **Why:**
        - Government support
        - Increasing demand
        - Long-term contracts
        
        **Risks:**
        - Infrastructure scattered
        - Tech changes fast
        """)
    
    with col2:
        st.markdown("""
        ### ☀️ Solar Energy
        
        **Investment:** ₹2 - ₹5L (residential)  
        **ROI:** 12-20% annually  
        **Growth:** 30% YoY
        
        **Why:**
        - Subsidies available
        - 25-year lifespan
        - Govt schemes
        
        **Risks:**
        - Weather dependent
        - Installation costs
        """)
    
    with col3:
        st.markdown("""
        ### 🔋 Battery Tech
        
        **Investment:** ₹20L - ₹1Cr  
        **ROI:** 20-35% annually  
        **Growth:** 50% YoY
        
        **Why:**
        - Fastest growing segment
        - Manufacturing boost
        - New tech
        
        **Risks:**
        - High capital needed
        - Tech evolution
        """)
    
    st.markdown("---")
    
    # ROI Calculator
    st.subheader("📈 Quick ROI Calculator")
    
    investment_type = st.selectbox(
        "Select investment type:",
        ["EV Charging", "Solar", "Battery Storage"]
    )
    
    amount = st.slider(
        "Investment Amount (₹)",
        min_value=50000,
        max_value=10000000,
        step=50000,
        value=500000
    )
    
    years = st.slider(
        "Investment Period (Years)",
        min_value=1,
        max_value=25,
        value=5
    )
    
    # ROI calculations
    roi_rates = {
        "EV Charging": 0.20,  # 20% average
        "Solar": 0.16,        # 16% average
        "Battery Storage": 0.27  # 27% average
    }
    
    roi_rate = roi_rates[investment_type]
    final_amount = amount * ((1 + roi_rate) ** years)
    profit = final_amount - amount
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Initial Investment", f"₹{amount:,.0f}")
    col2.metric("After {0} Years".format(years), f"₹{final_amount:,.0f}")
    col3.metric("Total Profit", f"₹{profit:,.0f}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: MARKET DATA
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.subheader("📊 India Energy Market Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## 🇮🇳 Market Overview
        
        **EV Segment:**
        - Growth: 40% YoY
        - Sales: 1.4M+ units
        - Target: 30% of vehicles by 2030
        - Market Size: ₹2+ Trillion
        
        **Solar Energy:**
        - Growth: 30% YoY
        - Current: 70+ GW operational
        - Target: 500 GW by 2030
        - Subsidy: Substantial support available per roof
        
        **Renewable Energy:**
        - Growth: 35% YoY
        - Current: 180+ GW
        - Goal: 500 GW by 2030
        - Investment: $500B+ expected
        """)
    
    with col2:
        st.markdown("""
        ## 🎯 Government Schemes
        
        **PM Gati Shakti Infrastructure**
        - Focus: Transport & charging
        - Budget: ₹100K Cr
        - Timeline: 2023-2030
        
        **National Green Hydrogen Mission**
        - Focus: Clean fuel
        - Budget: ₹19,744 Cr
        - Target: 5M tonnes/year
        
        **PLI Scheme**
        - Focus: EV manufacturing
        - Budget: ₹10,000 Cr
        - Target: 5M vehicles
        
        **Solar Subsidies**
        - Residential: Significant financial implementation aid
        - Process: Accessible via National Online portal
        """)
    
    # Growth chart
    st.markdown("---")
    st.subheader("📈 Sector Growth Comparison")
    
    import pandas as pd
    
    data = {
        'Sector': ['EV', 'Solar', 'Renewables', 'Battery'],
        'Growth %': [40, 30, 35, 50],
        '2030 Value (Trillion ₹)': [2.5, 1.8, 3.2, 1.5]
    }
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(df.set_index('Sector')['Growth %'], color='#00F0FF')
        st.caption("Annual Growth Rate (%)")
    
    with col2:
        st.bar_chart(df.set_index('Sector')['2030 Value (Trillion ₹)'], color='#8B5CF6')
        st.caption("Estimated 2030 Market Value (₹ Trillion)")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: SUBSIDY CHECKER
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.subheader("🎯 Check Your Subsidy Eligibility")
    
    st.markdown("""
    ### Solar Rooftop Subsidy Calculator
    
    Enter your details to check eligibility and estimate subsidy.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox(
            "Select Your State:",
            ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Kolkata", 
             "Chennai", "Pune", "Ahmedabad", "Jaipur", "Other"]
        )
        
        roof_area = st.number_input(
            "Roof Area (sq meters):",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
    
    with col2:
        roof_type = st.selectbox(
            "Roof Type:",
            ["Concrete", "Metal", "Asbestos", "Tile", "Other"]
        ) FB cc c 
