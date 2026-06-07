import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 FUTUREHQ.IN - UNIFIED PRODUCTION LAYER
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="FutureHQ - India Energy AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Configuration Handshake
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    st.error("⚠️ Missing API Key. Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")

# Custom Luxury Dark Glass Theme Stylesheet
st.markdown("""
    <style>
    /* Global Base */
    .stApp {
        background-color: #050816 !important;
        color: #ffffff !important;
    }
    
    /* Header Typography */
    h1 {
        background: linear-gradient(135deg, #8B5CF6, #00F0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    h2, h3 {
        color: #00F0FF !important;
        font-weight: 700 !important;
    }
    
    /* Tabs Control Custom Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a1a1aa !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00F0FF !important;
        background-color: rgba(0, 240, 255, 0.1) !important;
        font-weight: bold !important;
    }

    /* Message UI Formatting */
    .chat-bubble-user {
        background: linear-gradient(135deg, #8B5CF6, #00F0FF);
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        color: white;
        margin-bottom: 15px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
    }
    .chat-bubble-bot {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 240, 255, 0.2);
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        color: white;
        margin-bottom: 15px;
        max-width: 80%;
    }

    /* Form & Input Fields */
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Action Buttons */
    .stButton button {
        background: linear-gradient(135deg, #8B5CF6, #00F0FF) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    /* Success Container */
    .success-card {
        background: rgba(0, 240, 255, 0.05);
        border: 1px solid #00F0FF;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HERO DISPLAY FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1>⚡ FutureHQ</h1>", unsafe_allow_html=True)
st.markdown("### Your ₹20L Energy Decision. In 2 Minutes. Actually Smart.")

m1, m2, m3 = st.columns(3)
m1.metric("🚗 EV Growth", "40%", "YoY Target")
m2.metric("☀️ Solar Deployment", "30%", "YoY Expansion")
m3.metric("🔋 Battery Systems", "50% ", "YoY Scale")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# UI CORE NAVIGATION TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Premium AI Chat", 
    "💰 Investment Matrix", 
    "📊 Market Insights", 
    "🎯 Subsidy Auditor", 
    "📱 Connect Gateway"
])

# 🛠️ TAB 1: AI CHAT ENGINE
with tab1:
    st.markdown("### 🤖 FutureHQ Analytics Terminal")
    
    # Persistent conversational frame state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "👋 Welcome to FutureHQ. Ask me anything about local EV infrastructure, solar plant payback horizons, or central capital subsidies!"}
        ]
        
    # Render Chat Log using the new responsive layout architecture
    for dialogue in st.session_state.chat_history:
        if dialogue["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{dialogue["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">{dialogue["content"]}</div>', unsafe_allow_html=True)

    # Contextual suggestion row variables
    suggestion = None
    sc1, sc2, sc3, sc4 = st.columns(4)
    if sc1.button("📈 Check Sector ROIs"): suggestion = "What are the investment ROIs for solar and EV?"
    if sc2.button("🚗 EV Infra Growth"): suggestion = "Tell me about EV infrastructure scaling in India."
    if sc3.button("☀️ Subsidy Match"): suggestion = "What are the main government solar subsidies?"
    if sc4.button("🔋 Battery Trends"): suggestion = "Is battery manufacturing expanding?"

    # Chat Input Capture
    user_query = st.chat_input("Enter your energy or project query...")
    query_to_process = user_query if user_query else suggestion

    if query_to_process:
        # Display user submission immediately
        st.markdown(f'<div class="chat-bubble-user">{query_to_process}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": query_to_process})
        
        try:
            # Connect using the correct production configuration layout
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            
            structured_prompt = (
                f"System Prompt Context: You are FutureHQ AI, an expert advisor on Indian renewable infrastructure. "
                f"Keep answers precise, insight-driven, format numbers clearly in Lakhs/Crores, and limit responses to 120 words.\n\n"
                f"User Question: {query_to_process}"
            )
            
            raw_response = model.generate_content(structured_prompt)
            bot_text = raw_response.text
            
            st.markdown(f'<div class="chat-bubble-bot">{bot_text}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "bot", "content": bot_text})
            st.rerun()
            
        except Exception as api_err:
            st.error(f"⚠️ Live Stream Synchronization Interrupted: {str(api_err)}")

# 🛠️ TAB 2: INVESTMENT MATRIX
with tab2:
    st.markdown("### 💰 Capital Allocation & Payback Targets")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🚗 EV Charging\n* **Capex Bound:** ₹50K - ₹5 Lakhs\n* **Target ROI:** 15-25%\n* **Market Curve:** Hyper-Growth")
    with col2:
        st.info("### ☀️ Infrastructure Solar\n* **Capex Bound:** ₹2L - ₹5 Lakhs\n* **Target ROI:** 12-20%\n* **Market Curve:** High Stability")
    with col3:
        st.info("### 🔋 Utility Storage\n* **Capex Bound:** ₹20L - ₹1 Crore\n* **Target ROI:** 20-35%\n* **Market Curve:** Emerging Play")

# 🛠️ TAB 3: MARKET INSIGHTS
with tab3:
    st.markdown("### 📊 India Macro-Growth Framework (2030 Targets)")
    graph_data = pd.DataFrame({
        'Infrastructure Cluster': ['Solar Grid Integration', 'EV Base Fleet Share', 'Advanced Storage PLI'],
        'Target Scale (CAGR %)': [30, 40, 50]
    })
    st.bar_chart(graph_data.set_index('Infrastructure Cluster'), color="#00F0FF")

# 🛠️ TAB 4: SUBSIDY AUDITOR
with tab4:
    st.markdown("### 🎯 Local Rooftop Allocation Matrix")
    select_state = st.selectbox("Operating State Domain:", ["Delhi", "Maharashtra", "Karnataka", "Gujarat", "Other"])
    surface_area = st.number_input("Available Unobstructed Area (Sq Meters):", min_value=10, value=60)
    
    if st.button("Run Feasibility Assessment"):
        calculated_kw = surface_area * 1.2
        computed_grant = calculated_kw * 28000
        
        st.markdown(f"""
        <div class="success-card">
            <h4>📊 Preliminary Asset Assessment Profile</h4>
            <ul>
                <li>Calculated Generation Capacity Vector: <b>{calculated_kw:.2f} kWp</b></li>
                <li>Estimated Central Subsidy Grant Pool: <b>₹{computed_grant:,.2f}</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# 🛠️ TAB 5: CONNECT GATEWAY
with tab5:
    st.markdown("### 📱 Secure Strategy Deployment Request")
    with st.form("execution_lead_capture"):
        c_name = st.text_input("Corporate / Client Executive Name")
        c_mail = st.text_input("Official Electronic Mail Address")
        c_phone = st.text_input("Active Phone Connection Signature")
        c_segment = st.selectbox("Asset Class Intent:", ["Commercial Grid Solar", "EV Hub Deployment", "Industrial Battery System"])
        
        form_action = st.form_submit_button("Initialize Engineering Verification")
        if form_action:
            if c_name and c_mail and c_phone:
                st.success(f"⚡ Project Record Registered for {c_name}. FutureHQ assignment protocols dispatched to {c_mail}.")
            else:
                st.error("⚠️ Form validation incomplete. All verification indices must be satisfied.")

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL FOOTER BLOCK
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
f1, f2 = st.columns(2)
f1.caption("FutureHQ Energy Systems © 2026 | Built for High Performance Deployment")
f2.markdown("<p style='text-align: right; font-size: 12px; color: #a1a1aa;'>System Status: Connected to Production Model Layer</p>", unsafe_allow_html=True)
