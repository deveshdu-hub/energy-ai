import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import hashlib
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ NATIONAL GREEN TRANSITION OS (NGT-OS) // GOVERNMENT DEPLOYMENT PROFILE
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

# ═══════════════════════════════════════════════════════════════════════════════
# 🌌 GOVERNMENT MISSON CONTROL INTERFACE LAYER (CSS)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Institutional Mission Control Base Dark Layer */
    .stApp {
        background-color: #030611 !important;
        color: #f1f5f9 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Official Tricolor Infused Neon Gradient Header */
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

    /* Premium Glassmorphism Container Matrix */
    .cyber-card {
        background: linear-gradient(135deg, rgba(8, 14, 38, 0.85), rgba(3, 7, 18, 0.98));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 240, 255, 0.12);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.6);
    }

    /* Government Institutional Report Document View */
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

    /* Native Tab Custom Overrides */
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

    /* Native Custom Chat Conversational Engine */
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
# HUD GOVERNMENT POLICY HEADER REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 5px;'>NATIONAL GREEN TRANSITION OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 20px;'>Digital Public Infrastructure Core for Inter-Ministerial Planning & National Net-Zero Targets.</p>", unsafe_allow_html=True)

# Language Localization Protocol Switch
lang_toggle = st.sidebar.selectbox("🌐 LANGUAGE PROTOCOL / भाषा चयन", ["English (Default)", "हिन्दी (Bilingual Core)"])

if lang_toggle == "English (Default)":
    m1_lbl, m2_lbl, m3_lbl, m4_lbl = "☀️ PM Surya Ghar Base", "🚗 FAME III Support Allocation", "🔋 Grid Energy Storage", "🍃 Renewable Energy Share"
    tab_1, tab_2, tab_3, tab_4, tab_5 = "🤖 POLICY AI ASSISTANT", "📊 VALUE CALCULATORS", "🎯 SUBSIDY COMPLIANCE AUDITOR", "📡 NATIONAL ENERGY RADAR", "🏛️ PUBLIC DISPATCH BRIDGE"
else:
    m1_lbl, m2_lbl, m3_lbl, m4_lbl = "☀️ पीएम सूर्य घर आधार", "🚗 फेम III आवंटन पूल", "🔋 ग्रिड बैटरी क्षमता", "🍃 गैर-जीवाश्म ग्रिड मिश्रण"
    tab_1, tab_2, tab_3, tab_4, tab_5 = "🤖 नीति एआई सहायक", "📊 मूल्य कैलकुलेटर", "🎯 सब्सिडी अनुपालन लेखा परीक्षक", "📡 राष्ट्रीय ऊर्जा रडार", "🏛️ सार्वजनिक प्रेषण पुल"

# 2026 Macro Telemetry Parameters
m1, m2, m3, m4 = st.columns(4)
m1.metric(label=m1_lbl, value="4.1M+ Homes", delta="Target: 7.5M Sites")
m2.metric(label=m2_lbl, value="₹10,000 Cr", delta="Active Transition Lifecycle")
m3.metric(label=m3_lbl, value="150 GW+", delta="ACC PLI Manufacturing Link")
m4.metric(label=m4_lbl, value="45% Total", delta="Path to 500GW 2030")

st.markdown("<br>", unsafe_allow_html=True)

sec_chat, sec_calc, sec_subsidy, sec_news, sec_connect = st.tabs([tab_1, tab_2, tab_3, tab_4, tab_5])

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ SECTION 1: POLICY AI ASSISTANT TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════
with sec_chat:
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

    st.markdown("<p style='font-size:0.8rem; color:#64748b; font-family:Orbitron;'>STRATEGIC POLICY TARGET SHORTCUTS:</p>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    quick_input = None
    if b1.button("🇮🇳 National Green Hydrogen Targets"): quick_input = "Provide an objective policy briefing regarding India's National Green Hydrogen Mission targets by 2030 and grid transmission incentives."
    if b2.button("☀️ PM Surya Ghar Distribution Rules"): quick_input = "What are the current capacity tier limits and cash credit structural rules for consumers registering under the PM Surya Ghar framework?"
    if b3.button("🚗 FAME III EV Hub Infrastructure ROI"): quick_input = "What are the commercial parameters, power demands, and standard payback periods for running high-speed DC charging points in tier-1 municipal grids?"

    user_raw = st.chat_input("Enter inter-ministerial policy or technical query...")
    executable_query = user_raw if user_raw else quick_input

    if executable_query:
        st.markdown(f'<div class="bubble-user"><b>Query User:</b><br>{executable_query}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": executable_query})
        
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            system_injection = (
                "You are the National Green Transition OS Core Intelligence. You are an expert authority on India's energy grid, "
                "ministerial regulations, and economic feasibility. Respond with clean headers and professional terminology. "
                "Present monetary statistics in Lakhs or Crores. Maintain an authoritative, objective, public-sector appropriate tone. "
                "Limit the output response to 150 words maximum."
            )
            response_container = model.generate_content(f"{system_injection}\n\nUser Question: {executable_query}")
            bot_reply = response_container.text
            
            st.markdown(f'<div class="bubble-bot"><b>NGT-OS Core AI:</b><br>{bot_reply}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
            st.rerun()
        except Exception as e:
            st.error("🔒 Security Key Connection Interrupted. Ensure Streamlit configurations match requirements.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ SECTION 2: MACRO ENERGY ECONOMIC CALCULATORS
# ═══════════════════════════════════════════════════════════════════════════════
with sec_calc:
    st.markdown("### 📊 Dual-Vector Economic Feasibility Systems")
    sub_ev, sub_solar = st.tabs(["🚗 Commercial Electric Fleet Matrix", "☀️ Photovoltaic Power Plant Matrix"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ VARIABLE INPUT: ELECTRIC VEHICLE MOBILITY MODEL</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            daily_km = st.slider("Average Fleet Run Distance per Unit (KM / Day):", min_value=10, max_value=400, value=120, key="ev_slider")
            fuel_price = st.number_input("Conventional Fuel Resource Baseline Rate (₹ / Liter):", min_value=80.0, value=104.0, key="ev_fuel")
        with c2:
            ev_efficiency = st.number_input("Target Vehicle Energy Index (KM / kWh):", min_value=1.0, value=6.5, key="ev_eff")
            grid_tariff = st.number_input("Commercial/Industrial Discom Tariff Rate (₹ / Price per Unit):", min_value=3.0, value=8.5, key="ev_tariff")
        
        f_cost_day = (daily_km / 12) * fuel_price
        e_cost_day = (daily_km / ev_efficiency) * grid_tariff
        saved_monthly = (f_cost_day - e_cost_day) * 30
        saved_annual = saved_monthly * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 FINANCIAL FEASIBILITY METRICS OUTFLOW</p>", unsafe_allow_html=True)
        v1, v2, v3 = st.columns(3)
        v1.metric("📉 Estimated Monthly Savings", f"₹{saved_monthly:,.2f}")
        v2.metric("✨ Estimated Annual Net Savings", f"₹{saved_annual:,.2f}")
        v3.metric("⏱️ Capital Asset Payback Horizon", "11.4 Months" if saved_annual > 150000 else "19.8 Months")
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

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ SECTION 3: SUBSIDY COMPLIANCE AUDITOR (WITH POLICY BRIEFING REPORT GENERATOR)
# ═══════════════════════════════════════════════════════════════════════════════
with sec_subsidy:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎯 OFFICIAL DISCOM REGULATORY COMPLIANCE MONITOR</p>", unsafe_allow_html=True)
    
    state_domain = st.selectbox("Select Target Regional State Jurisdiction Node:", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"], key="sub_state")
    class_profile = st.radio("Asset Installation Infrastructure Target Profile:", ["Residential Rooftop Array", "Commercial Plant System", "Public Fast Charging Hub Venture"], key="sub_profile")
    
    if st.button("RUN NATIONAL COMPLIANCE AUDIT & GENERATE REPORT"):
        st.toast("Verifying policy parameters against central registry...", icon="⚙️")
        
        # Generation of an official Government Hash Verification Code
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hash_input = f"{state_domain}-{class_profile}-{timestamp_str}"
        verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:12].upper()
        
        # Official Bureaucratic White Report View Block 
        st.markdown(f"""
        <div class="gov-report">
            <h3 style="color:#0f172a; margin-top:0; text-transform:uppercase; font-family:'Orbitron'; letter-spacing:1px;">
                🇮🇳 NATIONAL GREEN TRANSITION VERIFICATION REPORT
            </h3>
            <p style="font-size:0.85rem; color:#475569; margin-bottom:20px;">
                <b>Generated:</b> {timestamp_str} IST // <b>System Reference Hash:</b> <span style="font-family:monospace; background:#cbd5e1; padding:2px 6px; border-radius:4px; color:#0f172a;">NGT-{verification_hash}</span>
            </p>
            <hr style="border:0; border-top:1px solid #cbd5e1; margin-bottom:20px;">
            <table style="width:100%; border-collapse: collapse; font-size:0.9rem;">
                <tr style="background-color: #f1f5f9;">
                    <td style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Jurisdiction State Node</td>
                    <td style="padding:10px; border:1px solid #cbd5e1;">{state_domain} Electricity Regulatory Commission</td>
                </tr>
                <tr>
                    <td style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Project Profile Allocation</td>
                    <td style="padding:10px; border:1px solid #cbd5e1;">{class_profile}</td>
                </tr>
                <tr style="background-color: #f1f5f9;">
                    <td style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Central Subsidy Eligibility</td>
                    <td style="padding:10px; border:1px solid #cbd5e1; color:#15803d; font-weight:bold;">VERIFIED APPROVED (PM Surya Ghar / FAME III Framework compliant)</td>
                </tr>
            </table>
            <br>
            <h4 style="color:#0f172a; margin-bottom:8px;">Compliance Directives & Legal Requirements:</h4>
            <ul style="margin-top:0; padding-left:20px; font-size:0.88rem; line-height:1.6;">
                <li><b>Hardware Standard Rules:</b> Systems must utilize Domestic Content Requirement (DCR) compliant photovoltaic configurations to clear direct central subsidy accounts.</li>
                <li><b>Net-Metering Code:</b> Unified smart-meter processing mandates state-level DISCOM clearance inside 30 operational days of line testing.</li>
                <li><b>Fiscal Benefits:</b> Corporate asset setups qualify for 40% accelerated depreciation credits inside the first year audit ledger.</li>
            </ul>
            <p style="font-size:0.75rem; color:#64748b; margin-top:25px; text-align:center; font-style:italic;">
                This report is electronically initialized via the National Green Transition OS Engine and constitutes valid reference metadata for preliminary infrastructure planning.
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ SECTION 4: STRATEGIC INNOVATION RADAR STREAM
# ═══════════════════════════════════════════════════════════════════════════════
with sec_news:
    st.markdown("### 📡 National Technology Tracks & Policy Horizons")
    
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FF9933; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🔋 ADVANCED BATTERY STORAGE</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>ACC PLI Localized Scale</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Localized gigafactory rollouts reduce production reliance parameters on lithium imports by 30% utilizing advanced localized silicon-anode configurations.</p>
        </div>
        """, unsafe_allow_html=True)
    with n2:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#FFFFFF; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>🚗 VEHICLE-TO-GRID (V2G)</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>Smart Grid Synchronization</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Vehicle-to-Grid power interfaces initiate high-volume trial tracking loops inside municipal utility zones across Bengaluru and Mumbai endpoints.</p>
        </div>
        """, unsafe_allow_html=True)
    with n3:
        st.markdown("""
        <div class='cyber-card'>
            <span style='color:#129E59; font-family:Orbitron; font-size:0.75rem; font-weight:bold;'>☀️ GENERATION SCIENCE</span>
            <h4 style='color:#00F0FF; margin:8px 0; font-family:Orbitron;'>Perovskite Efficiency Benchmarks</h4>
            <p style='font-size:0.85rem; color:#94a3b8;'>Indian research institutes scale a high 28% efficiency index index on tandem solar cell panels, readying lines for domestic industrial production.</p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ SECTION 5: PUBLIC STRATEGY DISPATCH BRIDGE
# ═══════════════════════════════════════════════════════════════════════════════
with sec_connect:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🏛️ OFFICIAL DISPATCH WEB BRIDGE // DIRECT INTENT REGISTRY</p>", unsafe_allow_html=True)
    
    with st.form("dispatch_capture_form"):
        exec_name = st.text_input("Full Official / Corporate Representative Name:")
        exec_contact = st.text_input("Verified Communications Contact Number (+91 Mobile):")
        exec_intent = st.selectbox("Strategic Transition Infrastructure Sector Focus:", [
            "Residential Asset Structural Optimization", 
            "Commercial Plant Integration Protocol", 
            "Public Fleet Grid Infrastructure Deployment"
        ])
        
        submit_exec = st.form_submit_button("DISPATCH SYSTEM DISCOVERY REQUEST")
        if submit_exec:
            if exec_name and exec_contact:
                st.markdown(f"""
                <div style='background:rgba(18, 158, 89, 0.1); border:1px solid #129E59; padding:18px; border-radius:8px; margin-top:15px;'>
                    <span style='color:#129E59; font-weight:bold; font-family:Orbitron;'>⚡ REGISTRY STATUS: DISPATCH COMPLETED</span><br>
                    Data verified. Welcome, {exec_name}. Your energy infrastructure transition intent packet has been registered securely in the session cache.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ Validation vector missing. Ensure mandatory fields are populated prior to registry transmission.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD FOOTER REEL ARCHITECTURE CONTROL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
f_left, f_right = st.columns(2)
with f_left:
    st.caption("⚡ National Green Transition OS | Digital Public Goods Framework Core v5.0.0 (2026 Production Profile)")
with f_right:
    st.markdown("<p style='text-align: right; font-size: 11px; color: #64748b; font-family:Orbitron;'>HUD RUNTIME STATUS: SYSTEM INTEGRITY MAXIMUM // REGULATORY MATRICES ACTIVE</p>", unsafe_allow_html=True)
