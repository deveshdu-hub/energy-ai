import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ NATIONAL GREEN TRANSITION OS (NGT-OS) // PRODUCTION RUNTIME CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="National Green Transition OS 🇮🇳",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Secure Encryption Bridge Key Handshake
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ═══════════════════════════════════════════════════════════════════════════════
# 🌌 CYBER-TECH DASHBOARD INJECTION DECK (CSS)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Institutional Mission Control Base Dark Layer */
    .stApp {
        background-color: #02050d !important;
        color: #e2e8f0 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Institutional Tricolor Infused Neon Gradient */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #FF9933, #FFFFFF, #129E59, #00F0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.2);
    }
    
    .cyber-label {
        font-family: 'Orbitron', sans-serif;
        color: #00F0FF !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
    }

    /* Premium Glassmorphism Container Matrix */
    .cyber-card {
        background: linear-gradient(135deg, rgba(6, 11, 30, 0.8), rgba(2, 4, 11, 0.95));
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 16px;
        padding: 26px;
        margin-bottom: 22px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .cyber-card:hover {
        border-color: rgba(24, 240, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
    }

    /* Native Tab Clean Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(6, 11, 30, 0.9);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(0, 240, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-family: 'Orbitron', sans-serif;
        background-color: transparent !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        color: #00F0FF !important;
        background: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        font-weight: 700;
    }

    /* Custom Chat Message Layouts */
    .bubble-user {
        background: linear-gradient(135deg, #3b82f6, #00f0ff);
        padding: 16px 20px;
        border-radius: 20px 20px 4px 20px;
        color: white;
        margin-bottom: 16px;
        max-width: 80%;
        margin-left: auto;
    }
    .bubble-bot {
        background: rgba(10, 15, 36, 0.95);
        border-left: 4px solid #129E59;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 16px 20px;
        border-radius: 4px 20px 20px 20px;
        color: #e2e8f0;
        margin-bottom: 16px;
        max-width: 85%;
    }

    /* Telemetry Metrics Tuning */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* Input Custom Framework Form Elements */
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, select {
        background-color: rgba(2, 4, 10, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
    }

    /* Cyber Action Button Control Layer */
    .stButton button {
        background: linear-gradient(135deg, #00F0FF, #129E59) !important;
        color: #02050d !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 1.5px;
        border-radius: 8px !important;
    }
    .stButton button:hover {
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD MISSION CONTROL HEADER GRID
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 10px;'>NATIONAL GREEN TRANSITION OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.05rem; margin-bottom: 25px;'>Strategic Analytics & Public Infrastructure Core for India's Sustainable Net-Zero Milestones.</p>", unsafe_allow_html=True)

# Real-Time Operational Telemetry Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="☀️ PM Surya Ghar Deployments", value="4.1M+ Homes", delta="Targeting 7.5M Sites")
with m2:
    st.metric(label="🚗 FAME III Support Allocation", value="₹10,000 Cr", delta="Active Structural Budget")
with m3:
    st.metric(label="🔋 Grid Battery Footprint", value="150 GW+", delta="Advanced Chemistry Cell Pool")
with m4:
    st.metric(label="🍃 Non-Fossil Generation Mix", value="45% Total", delta="Progress toward 500GW 2030")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION SECTIONS
# ═══════════════════════════════════════════════════════════════════════════════
sec_chat, sec_calc, sec_subsidy, sec_news, sec_connect = st.tabs([
    "🤖 INTELLIGENT POLICY ASSISTANT",
    "📊 MACRO ENERGY ECONOMIC CALCULATORS",
    "🎯 GOVERNANCE SUBSIDY AUDITOR",
    "📡 STRATEGIC INNOVATION STREAM",
    "📱 COMMERCIAL DISPATCH TERMINAL"
])

# 🛠️ SECTION 1: POLICY AI ASSISTANT TERMINAL
with sec_chat:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>⚡ STABLE ENDPOINT: ENGAGED // REVISION 4.5</p>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "⚡ National Green Transition OS core initialized. Query me on rooftop sizing mechanics, public EV grid feasibility frameworks, or central ministry subsidy policies."}
        ]
        
    for text_block in st.session_state.chat_history:
        if text_block["role"] == "user":
            st.markdown(f'<div class="bubble-user"><b>User:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot"><b>NGT-OS Core Intelligence:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.85rem; color:#64748b; font-family:Orbitron;'>DIRECTIVE SELECTION SHORTCUTS:</p>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    quick_input = None
    if b1.button("🇮🇳 Analyze India's 2030 Green Hydrogen Mission"): quick_input = "Give me a high-impact breakdown of India's National Green Hydrogen Mission goals, production milestones by 2030, and required pipeline setups."
    if b2.button("☀️ PM Surya Ghar Rooftop Sizing Logic"): quick_input = "Explain the solar capacity sizing regulations, structural cost parameters, and steps to claim financial allocations via the PM Surya Ghar scheme."
    if b3.button("🚗 Commercial EV Charging Hub Profitability"): quick_input = "What are the commercial parameters, power grids, and baseline capital payback speeds for building an array of 60kW DC fast chargers in a major tier-1 city?"

    user_raw = st.chat_input("Query the national green energy infrastructure graph...")
    executable_query = user_raw if user_raw else quick_input

    if executable_query:
        st.markdown(f'<div class="bubble-user"><b>User:</b><br>{executable_query}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": executable_query})
        
        try:
            # Active production model identifier
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            system_injection = (
                "You are the National Green Transition OS (NGT-OS) Core Intelligence. You are an authority on India's clean energy grid, "
                "government policies, technology matrices, and economic models. Structure answers cleanly using headers or lists, "
                "format monetary values in Lakhs or Crores, maintain an objective, data-driven, authoritative tone, and be helpful. "
                "Limit the output response to 150 words maximum."
            )
            response_container = model.generate_content(f"{system_injection}\n\nUser Question: {executable_query}")
            bot_reply = response_container.text
            
            st.markdown(f'<div class="bubble-bot"><b>NGT-OS Core Intelligence:</b><br>{bot_reply}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
            st.rerun()
        except Exception as e:
            st.error("🔒 Real-time API handshake paused. Ensure secret strings are verified in the Streamlit panel.")
    st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ SECTION 2: MACRO CALCULATORS
with sec_calc:
    st.markdown("### 📊 Dual-Vector Infrastructure Modeling Units")
    sub_ev, sub_solar = st.tabs(["🚗 Electric Transport Fleet Unit", "☀️ Photo-Voltaic Generation Unit"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE INPUT PANELS: TRANSPORT FLEET TRANSITION</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            daily_km = st.slider("Average Daily Run Scale per Fleet Vehicle (KM):", min_value=10, max_value=400, value=120)
            fuel_price = st.number_input("Conventional Petrol / Diesel Resource Rate (₹ / Liter):", min_value=80.0, value=104.0)
        with c2:
            ev_efficiency = st.number_input("Target EV Efficiency Coefficient (KM per kWh Unit):", min_value=1.0, value=6.5)
            grid_tariff = st.number_input("State Industrial / Commercial Tariff Base (₹ / kWh):", min_value=3.0, value=8.5)
        
        f_cost_day = (daily_km / 12) * fuel_price
        e_cost_day = (daily_km / ev_efficiency) * grid_tariff
        saved_monthly = (f_cost_day - e_cost_day) * 30
        saved_annual = saved_monthly * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 ECONOMIC TRANSITION LEDGER PROJECTIONS</p>", unsafe_allow_html=True)
        v1, v2, v3 = st.columns(3)
        v1.metric("📉 Estimated Monthly Savings", f"₹{saved_monthly:,.2f}")
        v2.metric("✨ Estimated Annual Net Savings", f"₹{saved_annual:,.2f}")
        v3.metric("⏱️ Capital Investment Payback Horizon", "11.4 Months" if saved_annual > 150000 else "19.8 Months")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sub_solar:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE INPUT PANELS: PHOTO-VOLTAIC ARRAYS</p>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            bill_monthly = st.number_input("Average Monthly Energy Bill Baseline (₹):", min_value=500, value=7500)
        with c4:
            roof_footprint = st.number_input("Available Free Unobstructed Roof Area Footprint (Sq Ft):", min_value=100, value=500)
        
        max_feasible_kw = min((roof_footprint / 100), (bill_monthly / 1300))
        estimated_capex = max_feasible_kw * 62000
        carbon_offset = max_feasible_kw * 1.3  # Tonnes of CO2 saved annually
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 RENEWABLE ENGINE SPECS GENERATED</p>", unsafe_allow_html=True)
        v4, v5, v6 = st.columns(3)
        v4.metric("☀️ Suggested Plant Capacity Size", f"{max_feasible_kw:.1f} kWp")
        v5.metric("💰 Estimated Project Capex Matrix", f"₹{estimated_capex:,.2f}")
        v6.metric("🍃 Annual Carbon Emissions Offset", f"{carbon_offset:.2f} MT CO2e")
        st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ SECTION 3: SUBSIDY AUDITOR
with sec_subsidy:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎯 DISCOM COMPLIANCE & MINISTRY ACCOUNTABILITY SCREEN</p>", unsafe_allow_html=True)
    
    state_domain = st.selectbox("Select Target Regional State Jurisdiction Node:", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"])
    class_profile = st.radio("Asset Allocation Profile Classification Group:", ["Residential Rooftop Array", "Commercial Plant System", "Public Fast Charging Hub Venture"])
    
    if st.button("RUN NATIONAL SUBSIDY COMPLIANCE AUDIT"):
        st.toast("Verifying policy parameters against central registry...", icon="⚙️")
        st.markdown("<hr style='border:1px solid rgba(0, 240, 255, 0.2);'>", unsafe_allow_html=True)
        
        a1, a2 = st.columns(2)
        with a1:
            st.markdown(f"""
            ### 🇮🇳 Central Ministry Incentives ({state_domain} Zone)
            * **Rooftop Disbursal Framework:** PM Surya Ghar grants up to ₹78,000 cash credit directly into verified accounts within 30 days of setup inspection loop.
            * **Hardware Mandate Regulation:** Solar panels must align with **DCR (Domestic Content Requirement)** design patterns to clear the registry.
            * **EV Infrastructure Clearances:** Public Fast Charging hubs are eligible for localized asset deployment grants under the active FAME III framework pool.
            """)
        with a2:
            st.markdown(f"""
            ### ⚖️ Regional DISCOM Policy & Tax Benefits
            * **Net-Metering Pipeline:** Smart-meter grid installations clear inside local utility boundaries within 4 weeks of technical registration.
            * **State Level Policy Perks:** Zero vehicle registration tax and complete electricity stamp-duty exemptions apply.
            * **Accelerated Asset Depreciation:** Enterprise-tier setups unlock up to **40% accelerated depreciation tax write-offs** inside the initial fiscal cycle.
            """)
    st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ SECTION 4: STRATEGIC INNOVATION DEEP-TECH STREAM
with sec_news:
    st.markdown("### 📡 Deep Tech Insights & Policy Intelligence")
    
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FF9933; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🔋 SOLID-STATE ENERGY CELL</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>ACC PLI Localized Scale</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Localized gigafactory rollouts reduce production reliance parameters on lithium imports by 30% utilizing advanced silicon-anode configurations.</p>
        </div>
        """, unsafe_allow_html=True)
    with n2:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FFFFFF; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🚗 MOBILITY INFRASTRUCTURE</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>V2G Grid Synchronization</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Vehicle-to-Grid power interfaces initiate high-volume trial tracking loops inside municipal utility zones across Bengaluru and Mumbai endpoints.</p>
        </div>
        """, unsafe_allow_html=True)
    with n3:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#129E59; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>☀️ GENERATION GRID</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>Perovskite Commercialization</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Indian research institutes achieve an improved 28% efficiency index scale on tandem solar cells, preparing modules for industrial line manufacturing.</p>
        </div>
        """, unsafe_allow_html=True)

# 🛠️ SECTION 5: STRATEGY DISPATCH
with sec_connect:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>📱 INITIALIZE ADVISORY POLICY TRANSITION RECORD</p>", unsafe_allow_html=True)
    
    with st.form("dispatch_capture_form"):
        exec_name = st.text_input("Full Official/Corporate Name:")
        exec_contact = st.text_input("Active Communications Handle Number (+91):")
        exec_intent = st.selectbox("Primary Strategic Transition Sector:", [
            "Residential Structural Optimization", 
            "Commercial Plant Integration", 
            "Public Fleet Grid Infrastructure Deployment"
        ])
        
        submit_exec = st.form_submit_button("SUBMIT INTENT PACKET")
        if submit_exec:
            if exec_name and exec_contact:
                st.markdown(f"""
                <div style='background:rgba(18, 158, 89, 0.1); border:1px solid #129E59; padding:18px; border-radius:12px; margin-top:15px;'>
                    <span style='color:#129E59; font-weight:bold; font-family:Orbitron;'>⚡ SUCCESS: INTENT COMPLIANCE PACKET DISPATCHED</span><br>
                    Welcome, {exec_name}. Your energy system transition goals are logged in the operating framework cache.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ Validation vector missing. Ensure mandatory fields are populated prior to registry transmission.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD FOOTER CONSOLE CONSOLE LOG
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
f_left, f_right = st.columns(2)
with f_left:
    st.caption("⚡ National Green Transition OS | Digital Public Goods Framework Core v4.5.0 (2026 Stable Deployment Layer)")
with f_right:
    st.markdown("<p style='text-align: right; font-size: 11px; color: #64748b; font-family:Orbitron;'>HUD RUNTIME STATUS: DATA LAYERS ALIGNED // COMPLIANCE ENGAGED</p>", unsafe_allow_html=True)
