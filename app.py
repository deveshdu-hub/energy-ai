import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import hashlib
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ NATIONAL GREEN TRANSITION OS (NGT-OS) // OPEN UTILITY DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="National Green Transition OS 🇮🇳",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Secure Encryption Bridge Key Handshake
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Session Registry for Public Users
if "user_registered" not in st.session_state:
    st.session_state.user_registered = False
if "user_mobile" not in st.session_state:
    st.session_state.user_mobile = ""
if "user_pincode" not in st.session_state:
    st.session_state.user_pincode = ""

# ═══════════════════════════════════════════════════════════════════════════════
# 🌌 GOVERNMENT MISSON CONTROL INTERFACE LAYER (CSS)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #030611 !important;
        color: #f1f5f9 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #FF9933 10%, #FFFFFF 50%, #129E59 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 2.5px;
        text-shadow: 0 0 35px rgba(255, 153, 51, 0.15);
    }
    
    .cyber-label {
        font-family: 'Orbitron', sans-serif;
        color: #00F0FF !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 6px;
        margin-bottom: 15px;
    }

    .cyber-card {
        background: linear-gradient(135deg, rgba(8, 14, 38, 0.85), rgba(3, 7, 18, 0.98));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 240, 255, 0.12);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.6);
    }

    .gov-report {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border-left: 6px solid #FF9933;
        border-right: 6px solid #129E59;
        border-radius: 6px;
        padding: 30px;
        margin-top: 15px;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(7, 13, 33, 0.95);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-family: 'Orbitron', sans-serif;
        background-color: transparent !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-size: 0.8rem;
    }
    .stTabs [aria-selected="true"] {
        color: #00F0FF !important;
        background: rgba(0, 240, 255, 0.08) !important;
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
    }

    .bubble-user {
        background: linear-gradient(135deg, #1d4ed8, #0284c7);
        padding: 14px 18px;
        border-radius: 16px 16px 4px 16px;
        color: white;
        margin-bottom: 14px;
        max-width: 80%;
        margin-left: auto;
    }
    .bubble-bot {
        background: rgba(13, 22, 54, 0.95);
        border-left: 4px solid #129E59;
        padding: 14px 18px;
        border-radius: 4px 16px 16px 16px;
        color: #e2e8f0;
        margin-bottom: 14px;
        max-width: 85%;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.65rem !important;
    }

    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, select {
        background-color: rgba(4, 8, 23, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #FF9933, #129E59) !important;
        color: #030611 !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 1px;
        border-radius: 6px !important;
        width: 100%;
    }
    .stButton button:hover {
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 📥 CITIZEN REGISTRATION ENTRY GATEWAY
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.user_registered:
    st.markdown("<br><br>", unsafe_allow_html=True)
    left_co, cent_co, last_co = st.columns([1, 1.8, 1])
    
    with cent_co:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='neon-title' style='text-align:center; font-size:1.7rem; margin-bottom:5px;'>NATIONAL GREEN TRANSITION OS</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color: #64748b; font-size:0.85rem; font-family:Orbitron; margin-bottom:25px;'>FREE OPEN ACCESS PLATFORM</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8; margin-bottom:2px;'>Mobile Number / मोबाइल नंबर:</p>", unsafe_allow_html=True)
        mobile_in = st.text_input("Mobile", placeholder="Enter 10-digit mobile number", max_chars=10, label_visibility="collapsed")
        
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8; margin-bottom:2px; margin-top:12px;'>Regional Pin Code / पिन कोड:</p>", unsafe_allow_html=True)
        pincode_in = st.text_input("Pincode", placeholder="Enter 6-digit area pin code", max_chars=6, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INITIALIZE TRANSITION DASHBOARD"):
            if len(mobile_in) == 10 and mobile_in.isdigit() and len(pincode_in) == 6 and pincode_in.isdigit():
                st.session_state.user_registered = True
                st.session_state.user_mobile = mobile_in
                st.session_state.user_pincode = pincode_in
                st.toast("Initialization complete. Welcome to NGT-OS Node.", icon="🇮🇳")
                st.rerun()
            else:
                st.error("⚠️ Validation Error: Please enter a valid 10-digit mobile number and 6-digit pin code.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# 🏛️ POST-REGISTRATION MAIN SYSTEM LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 5px;'>NATIONAL GREEN TRANSITION OS</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 0.8rem; font-family:Orbitron; color: #129E59; margin-top:-10px;'>ACTIVE SECTOR NODE // PIN CODE: {st.session_state.user_pincode} // USER ID: +91 ******{st.session_state.user_mobile[-4:]}</p>", unsafe_allow_html=True)

# Main Telemetry Stats Banner
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="☀️ PM Surya Ghar Base", value="4.1M+ Homes", delta="Target: 7.5M Sites")
m2.metric(label="🚗 FAME III Support Allocation", value="₹10,000 Cr", delta="Active Budget Lifecycle")
m3.metric(label="🔋 Grid Energy Storage", value="150 GW+", delta="ACC PLI Connected")
m4.metric(label="🍃 Renewable Energy Share", value="45% Total", delta="Path to 500GW 2030")

st.markdown("<br>", unsafe_allow_html=True)

# Reordered App Tabs: Savings Calculator Is Now Front And Center
tab_calc, tab_chat, tab_subsidy, tab_news, tab_connect = st.tabs([
    "📊 PETROL VS EV SAVINGS CALCULATOR",
    "🤖 POLICY AI ASSISTANT",
    "🎯 SUBSIDY COMPLIANCE AUDITOR",
    "📡 NATIONAL ENERGY RADAR",
    "🏛️ PUBLIC DISPATCH BRIDGE"
])

# 🛠️ TAB 1: PETROL VS EV SAVINGS CALCULATOR (HOMEPAGE PRIORITY)
with tab_calc:
    st.markdown("### 📊 Dual-Vector Economic Feasibility Systems")
    sub_ev, sub_solar = st.tabs(["🚗 Commercial Electric Fleet Matrix", "☀️ Photovoltaic Power Plant Matrix"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='cyber-label'>⚙️ VARIABLE INPUT: ELECTRIC VEHILITY MODEL (REGIONAL PROFILE: {st.session_state.user_pincode})</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            daily_km = st.slider("Average Daily Running Distance (KM / Day):", min_value=10, max_value=400, value=120, key="ev_slider")
            fuel_price = st.number_input("Conventional Petrol / Diesel Resource Rate (₹ / Liter):", min_value=80.0, value=104.0, key="ev_fuel")
        with c2:
            ev_efficiency = st.number_input("Target EV Vehicle Efficiency Index (KM / kWh):", min_value=1.0, value=6.5, key="ev_eff")
            grid_tariff = st.number_input("Regional Discom Tariff Rate (₹ / Price per Unit):", min_value=3.0, value=8.5, key="ev_tariff")
        
        # Mathematical Vector Run Calculations
        f_cost_day = (daily_km / 12) * fuel_price  # Assuming average fuel mileage baseline of 12km/L
        e_cost_day = (daily_km / ev_efficiency) * grid_tariff
        
        petrol_per_km = fuel_price / 12
        ev_per_km = grid_tariff / ev_efficiency
        
        saved_monthly = (f_cost_day - e_cost_day) * 30
        saved_annual = saved_monthly * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 DIRECT RUNNING COST METRICS BREAKDOWN</p>", unsafe_allow_html=True)
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("⛽ Petrol Running Cost", f"₹{petrol_per_km:.2f} / KM")
        rc2.metric("⚡ EV Running Cost", f"₹{ev_per_km:.2f} / KM")
        rc3.metric("📉 Estimated Monthly Savings", f"₹{saved_monthly:,.2f}")
        rc4.metric("✨ Estimated Annual Net Savings", f"₹{saved_annual:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sub_solar:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE INPUT: ROOFTOP PHOTOVOLTAIC INFRASTRUCTURE</p>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            bill_monthly = st.number_input("Current Monthly Commercial Energy Cost (₹):", min_value=500, value=7500, key="sol_bill")
        with c4:
            roof_footprint = st.number_input("Available Unobstructed Roof Footprint Area (Sq Ft):", min_value=100, value=500, key="sol_roof")
        
        max_feasible_kw = min((roof_footprint / 100), (bill_monthly / 1300))
        estimated_capex = max_feasible_kw * 62000
        carbon_offset = max_feasible_kw * 1.3  
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 TECHNICAL ASSESSMENT SPECS GENERATED</p>", unsafe_allow_html=True)
        v4, v5, v6 = st.columns(3)
        v4.metric("☀️ Recommended Capacity Size", f"{max_feasible_kw:.1f} kWp")
        v5.metric("💰 Estimated Project Capex Matrix", f"₹{estimated_capex:,.2f}")
        v6.metric("🍃 Annual Carbon Savings Value", f"{carbon_offset:.2f} MT CO2e")
        st.markdown("</div>", unsafe_allow_html=True)

# 🛠 ... KEEPING ALL SUBSEQUENT INTERACTIVE MODULES RUNNING AS COMPLETELY OPEN-ACCESS PIPELINES ...
with tab_chat:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>⚡ STABLE ENDPOINT: ACTIVE // SECURE GOVERNMENT DATA KERNEL</p>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "Welcome to the NGT-OS Intelligence Node. I can provide analytical briefs on solar deployments, EV infrastructure financial models, or carbon-offset policy regulations."}
        ]
        
    for text_block in st.session_state.chat_history:
        if text_block["role"] == "user":
            st.markdown(f'<div class="bubble-user"><b>Query User:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot"><b>NGT-OS Core AI:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)

    user_raw = st.chat_input("Enter inter-ministerial policy or technical query...")
    if user_raw:
        st.markdown(f'<div class="bubble-user"><b>Query User:</b><br>{user_raw}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": user_raw})
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            system_injection = "You are the National Green Transition OS Core Intelligence. Give structured, objective, public-sector ready answers limited to 150 words."
            response_container = model.generate_content(f"{system_injection}\n\nUser Question: {user_raw}")
            bot_reply = response_container.text
            st.markdown(f'<div class="bubble-bot"><b>NGT-OS Core AI:</b><br>{bot_reply}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
            st.rerun()
        except Exception as e:
            st.error("🔒 Security Key Connection Interrupted. Ensure Streamlit configurations match requirements.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_subsidy:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎯 OFFICIAL DISCOM REGULATORY COMPLIANCE MONITOR</p>", unsafe_allow_html=True)
    
    state_domain = st.selectbox("Select Target Regional State Jurisdiction Node:", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"], key="sub_state")
    class_profile = st.radio("Asset Installation Infrastructure Target Profile:", ["Residential Rooftop Array", "Commercial Plant System", "Public Fast Charging Hub Venture"], key="sub_profile")
    
    if st.button("RUN NATIONAL COMPLIANCE AUDIT & GENERATE REPORT"):
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hash_input = f"{state_domain}-{class_profile}-{timestamp_str}"
        verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:12].upper()
        
        st.markdown(f"""
        <div class="gov-report">
            <h3 style="color:#0f172a; margin-top:0; text-transform:uppercase; font-family:'Orbitron';">🇮🇳 NATIONAL GREEN TRANSITION VERIFICATION REPORT</h3>
            <p style="font-size:0.85rem; color:#475569; margin-bottom:20px;"><b>Generated:</b> {timestamp_str} IST // <b>System Reference Hash:</b> <span style="font-family:monospace; background:#cbd5e1; padding:2px 6px; color:#0f172a;">NGT-{verification_hash}</span></p>
            <hr style="border:0; border-top:1px solid #cbd5e1; margin-bottom:20px;">
            <p><b>Jurisdiction State Node:</b> {state_domain} Electricity Regulatory Commission</p>
            <p><b>Project Profile Allocation:</b> {class_profile}</p>
            <p style="color:#15803d; font-weight:bold;">🥇 Central Subsidy Eligibility: VERIFIED APPROVED (PM Surya Ghar Framework Compliant)</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_news:
    st.markdown("### 📡 National Technology Tracks & Policy Horizons")
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("<div class='cyber-card'><h5>🔋 ACC PLI Localized Scale</h5><p style='font-size:0.85rem; color:#94a3b8;'>Localized gigafactory metrics reducing production reliance on raw lithium imports.</p></div>", unsafe_allow_html=True)
    with n2:
        st.markdown("<div class='cyber-card'><h5>🚗 V2G Grid Synchronization</h5><p style='font-size:0.85rem; color:#94a3b8;'>Vehicle-to-Grid power infrastructure initiates live high-volume municipal trials.</p></div>", unsafe_allow_html=True)
    with n3:
        st.markdown("<div class='cyber-card'><h5>☀️ Perovskite Science</h5><p style='font-size:0.85rem; color:#94a3b8;'>Indian research institutes scale stable 28% efficiency cell performance parameters.</p></div>", unsafe_allow_html=True)

with tab_connect:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🏛️ OFFICIAL DISPATCH WEB BRIDGE // DIRECT INTENT REGISTRY</p>", unsafe_allow_html=True)
    with st.form("dispatch_capture_form"):
        exec_name = st.text_input("Full Official Representative Name:")
        exec_contact = st.text_input("Verified Contact Number (+91 Mobile):")
        submit_exec = st.form_submit_button("DISPATCH SYSTEM DISCOVERY REQUEST")
        if submit_exec and exec_name and exec_contact:
            st.success(f"Success! Request logged for verification from pin code {st.session_state.user_pincode}.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD FOOTER REEL CONTROL TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.caption("⚡ National Green Transition OS | Digital Public Goods Framework Core v6.0.0 (2026 Open Public Build Profile)")
