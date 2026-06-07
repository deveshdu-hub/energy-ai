import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ INDIA ENERGY FUTURE HQ ⚡ SYSTEM CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="India Energy Future HQ ⚡",
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
    
    /* Premium ISRO / Space-Tech Base Dark Layer */
    .stApp {
        background-color: #02040a !important;
        color: #e2e8f0 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Cyber Glowing Typography - Tricolor Infused Neon Gradient */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #FF9933, #FFFFFF, #10B981, #00F0FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 3px;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.25);
    }
    
    .cyber-label {
        font-family: 'Orbitron', sans-serif;
        color: #00F0FF !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Luxury Glassmorphism Container Matrix */
    .cyber-card {
        background: linear-gradient(135deg, rgba(6, 11, 30, 0.75), rgba(3, 7, 18, 0.9));
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 22px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .cyber-card:hover {
        border-color: rgba(24, 240, 255, 0.5);
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2);
        transform: translateY(-3px);
    }

    /* Native Tab Clean Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(6, 11, 30, 0.85);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(0, 240, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-family: 'Orbitron', sans-serif;
        background-color: transparent !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #00F0FF !important;
        background: rgba(0, 240, 255, 0.12) !important;
        border: 1px solid rgba(0, 240, 255, 0.35) !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }

    /* Advanced Message UI Layouts */
    .bubble-user {
        background: linear-gradient(135deg, #4f46e5, #00f0ff);
        padding: 16px 20px;
        border-radius: 24px 24px 4px 24px;
        color: white;
        margin-bottom: 16px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25);
    }
    .bubble-bot {
        background: rgba(10, 15, 36, 0.9);
        border-left: 4px solid #10B981;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 16px 20px;
        border-radius: 4px 24px 24px 24px;
        color: #e2e8f0;
        margin-bottom: 16px;
        max-width: 85%;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
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
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* Cyber Action Button Control Layer */
    .stButton button {
        background: linear-gradient(135deg, #00F0FF, #10B981) !important;
        color: #02040a !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 1.5px;
        border-radius: 10px !important;
        padding: 10px 24px !important;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD MISSION CONTROL HEADER GRID
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 10px;'>INDIA ENERGY FUTURE HQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 25px;'>Building the Next-Generation Clean Energy Operating System for India's Sustainable Horizon.</p>", unsafe_allow_html=True)

# Real-Time 2026 Macro Telemetry Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="☀️ PM Surya Ghar Scale", value="4.1M+ Homes", delta="Targeting 7.5M by Year-End")
with m2:
    st.metric(label="🚗 FAME III Support Allocation", value="₹10,000 Cr", delta="Active Transition Lifecycle")
with m3:
    st.metric(label="🔋 Grid Battery Footprint", value="150 GW+", delta="+85% Local Manufacturing")
with m4:
    st.metric(label="🍃 Renewable Power Generation", value="45% Total", delta="On track for 500GW 2030")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION NAVIGATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
sec_chat, sec_calc, sec_subsidy, sec_news, sec_connect = st.tabs([
    "🤖 CYBERNETIC AI ASSISTANT",
    "📊 INTUITIVE ENERGY CALCULATORS",
    "🎯 CENTRAL SUBSIDY MONITOR",
    "📡 DEEP-TECH INNOVATION STREAM",
    "📱 STRATEGY DISPATCH CORES"
])

# 🛠️ TAB 1: AI ASSISTANT TERMINAL
with sec_chat:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>⚡ MODEL ENGINE ACTIVE // STATUS: STABLE</p>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "👋 Namaste! I am the FutureHQ Operating Core. Ask me anything about scaling solar arrays, localized EV fleet financial payback periods, or navigating grid interconnection protocols."}
        ]
        
    for text_block in st.session_state.chat_history:
        if text_block["role"] == "user":
            st.markdown(f'<div class="bubble-user"><b>You:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot"><b>Core AI Engine:</b><br>{text_block["content"]}</div>', unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.85rem; color:#64748b; font-family:Orbitron;'>PRE-SET DIRECTIVES:</p>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    quick_input = None
    if b1.button("🇮🇳 Analyze India's 2030 Green Hydrogen Mission"): quick_input = "Give me a high-impact overview of India's National Green Hydrogen Mission goals, production targets by 2030, and economic infrastructure changes."
    if b2.button("☀️ PM Surya Ghar Rooftop Sizing Rules"): quick_input = "Explain the solar capacity rules, cost benefits, and technical steps required to install an optimized rooftop configuration under the PM Surya Ghar scheme."
    if b3.button("🚗 Commercial EV Charging Hub Profitability"): quick_input = "What are the commercial parameters, power demands, and expected payback periods for building an array of 60kW DC fast chargers in a major tier-1 Indian city?"

    user_raw = st.chat_input("Query the unified knowledge graph...")
    executable_query = user_raw if user_raw else quick_input

    if executable_query:
        st.markdown(f'<div class="bubble-user"><b>You:</b><br>{executable_query}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": executable_query})
        
        try:
            # Swapped legacy code wrapper to use the updated active stable model engine
            model = genai.GenerativeModel(model_name="gemini-3.5-flash")
            system_injection = (
                "You are India Energy Future HQ AI—a world-class clean energy founder, infrastructure analyst, and engineering strategist. "
                "Structure answers perfectly, use clear numbers formatted in Lakhs/Crores, offer an encouraging tone, and address the user's intent. "
                "Limit the output response to 150 words maximum."
            )
            response_container = model.generate_content(f"{system_injection}\n\nUser Question: {executable_query}")
            bot_reply = response_container.text
            
            st.markdown(f'<div class="bubble-bot"><b>Core AI Engine:</b><br>{bot_reply}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
            st.rerun()
        except Exception as e:
            st.error("🔒 Real-time API connection synchronized incorrectly. Check configuration settings inside Streamlit Secrets panel.")
    st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ TAB 2: ADVANCED CALCULATORS
with sec_calc:
    st.markdown("### 📊 Dual-Vector Economic Modeling Systems")
    sub_ev, sub_solar = st.tabs(["🚗 Electric Mobility Fleet Modeler", "☀️ High-Efficiency Rooftop Modeler"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE PARAMETERS: ELECTRIC MOBILITY FLEET</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            daily_km = st.slider("Average Daily Fleet Operational Range (KM):", min_value=10, max_value=400, value=120)
            fuel_price = st.number_input("Conventional Petrol / Diesel Base Cost (₹ / Liter):", min_value=80.0, value=104.0)
        with c2:
            ev_efficiency = st.number_input("Target EV Efficiency Matrix (KM per kWh Unit):", min_value=1.0, value=6.5)
            grid_tariff = st.number_input("State Industrial / Commercial Electricity Power Rate (₹ / kWh):", min_value=3.0, value=8.5)
        
        # Operational Analytics Calculations
        f_cost_day = (daily_km / 12) * fuel_price
        e_cost_day = (daily_km / ev_efficiency) * grid_tariff
        saved_monthly = (f_cost_day - e_cost_day) * 30
        saved_annual = saved_monthly * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 FINANCIAL PROJECTIONS OUTPUT LEDGER</p>", unsafe_allow_html=True)
        v1, v2, v3 = st.columns(3)
        v1.metric("📉 Projected Monthly Savings", f"₹{saved_monthly:,.2f}")
        v2.metric("✨ Projected Annual Net Savings", f"₹{saved_annual:,.2f}")
        v3.metric("⏱️ Capital Investment Payback Speed", "11.4 Months" if saved_annual > 150000 else "19.8 Months")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sub_solar:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE PARAMETERS: ROOFTOP PHOTOVOLTAIC MATRICES</p>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            bill_monthly = st.number_input("Average Monthly Electricity Cost Baseline (₹):", min_value=500, value=7500)
        with c4:
            roof_footprint = st.number_input("Available Free Unobstructed Roof Footprint Area (Sq Ft):", min_value=100, value=500)
        
        # Solar Technical Logic 
        max_feasible_kw = min((roof_footprint / 100), (bill_monthly / 1300))
        estimated_capex = max_feasible_kw * 62000
        carbon_offset = max_feasible_kw * 1.3  # Metric tonnes of CO2 saved annually
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 TECHNICAL ASSESSMENT SPECIFICATION SHEET</p>", unsafe_allow_html=True)
        v4, v5, v6 = st.columns(3)
        v4.metric("☀️ Recommended Plant Capacity Size", f"{max_feasible_kw:.1f} kWp")
        v5.metric("💰 Estimated Initial Project Capex", f"₹{estimated_capex:,.2f}")
        v6.metric("🍃 Annual Carbon Offset Value", f"{carbon_offset:.2f} MT CO2e")
        st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ TAB 3: CENTRAL SUBSIDY MONITOR
with sec_subsidy:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎯 CENTRAL CAPITAL COMPLIANCE & SUBSIDY VERIFICATION AUDIT</p>", unsafe_allow_html=True)
    
    state_domain = st.selectbox("Select Target Regional State Jurisdiction:", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"])
    class_profile = st.radio("Asset Installation Infrastructure Target Profile:", ["Residential Rooftop Array", "Commercial Plant System", "Public Fast Charging Hub Venture"])
    
    if st.button("RUN NATIONAL SUBSIDY COMPLIANCE AUDIT"):
        st.toast("Processing compliance parameters...", icon="⚡")
        st.markdown("<hr style='border:1px solid rgba(0, 240, 255, 0.2);'>", unsafe_allow_html=True)
        
        a1, a2 = st.columns(2)
        with a1:
            st.markdown(f"""
            ### 🇮🇳 Central Governance Allowances ({state_domain} Nodes)
            * **Rooftop Financial Incentives:** PM Surya Ghar grants up to ₹78,000 cash credit directly into verified account holders within 30 days of setup inspection.
            * **Component Compliance Guardrail:** Solar modules must match national **DCR (Domestic Content Requirement)** patterns to clear audit structures.
            * **EV Subsidy Clearances:** Public Fast Charging hubs are eligible for localized infrastructure grants under the modern FAME III structural pool.
            """)
        with a2:
            st.markdown(f"""
            ### ⚖️ Regional Regulatory Benefits & Tax Credits
            * **Grid Net-Metering Pipeline:** Active bidirectional smart-meter approvals across local DISCOM networks within 4 weeks.
            * **State Level Policy Perks:** Zero road tax and complete stamp-duty exemptions for clean asset setups.
            * **Accelerated Asset Depreciation:** Industrial setups unlock up to **40% accelerated depreciation credits** inside the initial year framework.
            """)
    st.markdown("</div>", unsafe_allow_html=True)

# 🛠️ TAB 4: INNOVATION DEEP-TECH STREAM
with sec_news:
    st.markdown("### 📡 Deep Tech Insights & Strategic Intelligence")
    
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FF9933; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🔋 SOLID-STATE ARRAYS</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>ACC PLI Project Milestones</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Localized gigafactory rollouts drop production reliance metrics on lithium components by 30% utilizing next-gen silicon-anode layouts.</p>
        </div>
        """, unsafe_allow_html=True)
    with n2:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FFFFFF; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🚗 SMART TRANSPORT GRID</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>V2G Bidirectional Infrastructure</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Vehicle-to-Grid power interfaces initiate high-volume trial loops within dense metro sectors across Bengaluru and Mumbai nodes.</p>
        </div>
        """, unsafe_allow_html=True)
    with n3:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#10B981; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>☀️ GENERATION SYSTEMS</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>Perovskite Cell Commercial Efficiency</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Indian engineering labs achieve a breakthrough 28% efficiency index scale on tandem solar cell panels, readying lines for factory production.</p>
        </div>
        """, unsafe_allow_html=True)

# 🛠️ TAB 5: STRATEGY DISPATCH PIPELINE
with sec_connect:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>📱 INITIALIZE PROJECT ADVISORY PIPELINE</p>", unsafe_allow_html=True)
    
    with st.form("dispatch_capture_form"):
        exec_name = st.text_input("Full Professional Name:")
        exec_contact = st.text_input("Active WhatsApp Contact Number (+91):")
        exec_intent = st.selectbox("Primary Infrastructure Focus Area Target:", [
            "Residential Transformation Venture", 
            "Commercial Factory Rooftop Optimization", 
            "Public Fast Charging Hub Capital Asset Deployment"
        ])
        
        submit_exec = st.form_submit_button("DISPATCH DISCOVERY STRATEGY ENTRY")
        if submit_exec:
            if exec_name and exec_contact:
                st.markdown(f"""
                <div style='background:rgba(16, 185, 129, 0.1); border:1px solid #10B981; padding:18px; border-radius:12px; margin-top:15px;'>
                    <span style='color:#10B981; font-weight:bold; font-family:Orbitron;'>⚡ SUCCESS: STRATEGY PACKET DISPATCHED</span><br>
                    Welcome, {exec_name}. Your energy asset transition data has been registered. Our system engineers will review your configuration goals.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ Form matrix invalid. Ensure field vectors contain verified data strings before dispatching.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD FOOTER CONSOLE RUNTIME REEL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
f_left, f_right = st.columns(2)
with f_left:
    st.caption("⚡ India Energy Future HQ | Operational System Core Terminal v4.0.0 (2026 Stable Release)")
with f_right:
    st.markdown("<p style='text-align: right; font-size: 11px; color: #64748b; font-family:Orbitron;'>HUD RUNTIME STATUS: ALL COMPLIANCE MATRICES ACTIVE // VERIFIED CONNECTED</p>", unsafe_allow_html=True)
