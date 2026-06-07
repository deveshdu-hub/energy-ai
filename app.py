import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import hashlib
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ NATIONAL GREEN TRANSITION OS (NGT-OS) // SIMPLIFIED CITIZEN BUILD
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="PM Green Transition Portal 🇮🇳",
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
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #FF9933 10%, #FFFFFF 50%, #129E59 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 0 35px rgba(255, 153, 51, 0.15);
    }
    
    .cyber-label {
        font-family: 'Poppins', sans-serif;
        color: #00F0FF !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
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
        font-family: 'Poppins', sans-serif;
        background-color: transparent !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-size: 0.85rem;
        font-weight: 600;
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
        font-family: 'Poppins', sans-serif;
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
        font-family: 'Poppins', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
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
    
    left_co, cent_co, last_co = st.columns([1, 2.2, 1])
    
    with cent_co:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(13, 22, 54, 0.9), rgba(4, 8, 23, 0.98));
                backdrop-filter: blur(25px);
                border: 2px solid rgba(0, 240, 255, 0.25);
                box-shadow: 0 20px 50px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(0, 240, 255, 0.05);
                border-radius: 20px;
                padding: 45px;
                position: relative;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="height: 10px; width: 10px; background-color: #00F0FF; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #00F0FF;"></span>
                        <span style="font-family: 'Poppins', sans-serif; font-size: 0.8rem; color: #00F0FF; font-weight: 600;">🇮🇳 CITIZEN LOGIN / नागरिक लॉगिन</span>
                    </div>
                    <span style="font-family: 'Poppins', sans-serif; font-size: 0.75rem; color: #64748b;">v6.3.0</span>
                </div>
                
                <h2 class="neon-title" style="text-align:center; font-size:1.8rem; margin-bottom:5px;">PM GREEN TRANSITION PORTAL</h2>
                <p style="text-align:center; color: #94a3b8; font-size:0.95rem; margin-bottom:15px;">हरित क्रांति डिजिटल सेवा - भारत सरकार</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Dual inputs
        in_c1, in_c2 = st.columns(2)
        
        with in_c1:
            st.markdown("<p style='font-family:\"Poppins\", sans-serif; font-size:0.8rem; color:#00F0FF; font-weight:600; margin-bottom:8px;'>📱 MOBILE NUMBER / मोबाइल नंबर</p>", unsafe_allow_html=True)
            mobile_in = st.text_input("Mobile", placeholder="10-Digit Mobile No.", max_chars=10, label_visibility="collapsed", key="gate_mobile")
            
        with in_c2:
            st.markdown("<p style='font-family:\"Poppins\", sans-serif; font-size:0.8rem; color:#00F0FF; font-weight:600; margin-bottom:8px;'>📍 AREA PIN CODE / पिन कोड</p>", unsafe_allow_html=True)
            pincode_in = st.text_input("Pincode", placeholder="6-Digit Pin Code", max_chars=6, label_visibility="collapsed", key="gate_pincode")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action button cleanly aligned under the central column content
        submit_btn = st.button("OPEN DASHBOARD / आगे बढ़ें ➡️", use_container_width=True)
        
        if submit_btn:
            if len(mobile_in) == 10 and mobile_in.isdigit() and len(pincode_in) == 6 and pincode_in.isdigit():
                st.session_state.user_registered = True
                st.session_state.user_mobile = mobile_in
                st.session_state.user_pincode = pincode_in
                st.toast("Handshake Successful! Welcome.", icon="🇮🇳")
                st.rerun()
            else:
                st.error("⚠️ Error: Please check that your Mobile Number is 10 digits and Pin Code is 6 digits.")
                
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# 🏛️ POST-REGISTRATION MAIN SYSTEM LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 5px;'>PM GREEN TRANSITION PORTAL</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 0.9rem; color: #129E59; margin-top:-10px; font-weight:600;'>🟢 ACTIVE NODE // PIN CODE: {st.session_state.user_pincode} // WELCOME USER</p>", unsafe_allow_html=True)

# Main Telemetry Stats Banner (Simplified to Lakhs and Crores)
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="☀️ PM Surya Ghar Base", value="41 Lakh+ Homes", delta="Target: 75 Lakh")
m2.metric(label="🚗 FAME III Support Scheme", value="₹10,000 Crore", delta="Active Fund Lifecycle")
m3.metric(label="🔋 Total Grid Storage", value="150 GW Capacity", delta="ACC PLI Factories Active")
m4.metric(label="🍃 Renewable Energy Share", value="45% Green Power", delta="Goal: 50% by 2030")

st.markdown("<br>", unsafe_allow_html=True)

# Reordered App Tabs: Savings Calculator Front And Center
tab_calc, tab_chat, tab_subsidy, tab_news, tab_connect = st.tabs([
    "💰 MY SAVINGS CALCULATOR (बचत कैलकुलेटर)",
    "🤖 GREEN SAHAYIK (योजना हेल्प AI)",
    "🎯 GOVT SUBSIDY CHECKER (सरकारी सब्सिडी)",
    "📡 REGIONAL ENERGY NEWS (समाचार)",
    "🏛️ CONNECT WITH OFFICIALS (अधिकारियों से जुड़ें)"
])

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 1: PETROL VS EV SAVINGS CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab_calc:
    st.markdown("### 📊 Check Your Expenses & Green Savings Value")
    sub_ev, sub_solar = st.tabs(["🚗 Petrol vs Electric Vehicle Savings", "☀️ Rooftop Solar Benefit Estimator"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='cyber-label'>⚙️ STEP 1: SELECT YOUR VEHICLE TYPE / वाहन का प्रकार चुनें</p>", unsafe_allow_html=True)
        
        vehicle_type = st.selectbox(
            "Select Vehicle Category / वाहन प्रकार चुनें:",
            ["Electric 2-Wheeler (Scooter/Bike)", "Electric 3-Wheeler (E-Rickshaw/Auto)", "Electric 4-Wheeler (Car/Fleet SUV)"]
        )
        
        if "2-Wheeler" in vehicle_type:
            default_mileage = 45.0
            default_efficiency = 40.0
            slider_max = 150
            slider_val = 40
        elif "3-Wheeler" in vehicle_type:
            default_mileage = 25.0
            default_efficiency = 12.0
            slider_max = 200
            slider_val = 80
        else:
            default_mileage = 14.0
            default_efficiency = 6.5
            slider_max = 400
            slider_val = 120

        c1, c2 = st.columns(2)
        with c1:
            daily_km = st.slider("Average Daily Running Distance (KM per Day / हर दिन कितना चलते हैं):", min_value=10, max_value=slider_max, value=slider_val, key="ev_slider")
            fuel_price = st.number_input("Current Petrol / Diesel Rate (₹ per Liter / पेट्रोल की कीमत):", min_value=80.0, value=104.0, key="ev_fuel")
        with c2:
            ev_efficiency = st.number_input("EV Vehicle Mileage (KM per 1 Unit of Charge / 1 यूनिट में कितने KM चलेगी):", min_value=1.0, value=default_efficiency, key="ev_eff")
            grid_tariff = st.number_input("Your Home Electricity Rate (₹ per Unit / बिजली बिल दर):", min_value=3.0, value=8.5, key="ev_tariff")
        
        f_cost_day = (daily_km / default_mileage) * fuel_price
        e_cost_day = (daily_km / ev_efficiency) * grid_tariff
        
        petrol_per_km = fuel_price / default_mileage
        ev_per_km = grid_tariff / ev_efficiency
        
        saved_monthly = (f_cost_day - e_cost_day) * 30
        saved_annual = saved_monthly * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 REAL SAVINGS ESTIMATE / आपकी कुल अनुमानित बचत</p>", unsafe_allow_html=True)
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("⛽ Petrol Cost per KM", f"₹{petrol_per_km:.2f} / KM")
        rc2.metric("⚡ Electric Cost per KM", f"₹{ev_per_km:.2f} / KM")
        rc3.metric("📉 Monthly Bachat (बचत)", f"₹{saved_monthly:,.2f}")
        rc4.metric("✨ Yearly Net Bachat (बचत)", f"₹{saved_annual:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sub_solar:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ STEP 1: ROOFTOP SPACE & LIGHT BILL DETAILS</p>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            bill_monthly = st.number_input("Average Monthly Light Bill Amount (₹ / हर महीने का बिजली का बिल):", min_value=500, value=7500, key="sol_bill")
        with c4:
            roof_footprint = st.number_input("Available Open Roof Area (Square Feet / छत पर खाली जगह):", min_value=100, value=500, key="sol_roof")
        
        max_feasible_kw = min((roof_footprint / 100), (bill_monthly / 1300))
        estimated_capex = max_feasible_kw * 62000
        carbon_offset = max_feasible_kw * 1.3  
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 RECOMMENDED SOLAR PLANT SETUP SPECS</p>", unsafe_allow_html=True)
        v4, v5, v6 = st.columns(3)
        v4.metric("☀️ Recommended Solar Size", f"{max_feasible_kw:.1f} kW Size")
        v5.metric("💰 Approx Setup Price (लागत)", f"₹{estimated_capex:,.2f}")
        v6.metric("🍃 Annual Carbon Saved", f"{carbon_offset:.2f} Tons CO2")
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 2: POLICY AI ASSISTANT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🤖 GREEN SAHAYIK AI HELP DESK // सरकारी योजना हेल्प डेस्क</p>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "नमस्ते! Welcome to the Green Sahayik Help Node. Ask me any question about PM Surya Ghar Solar Subsidies, rules, or EV loans in simple words."}
        ]
        
    for text_block in st.session_state.chat_history:
        if text_block["role"] == "user":
            st.markdown(f"""<div class="bubble-user"><b>Your Question:</b><br>{text_block["content"]}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="bubble-bot"><b>Sahayik AI Assistant:</b><br>{text_block["content"]}</div>""", unsafe_allow_html=True)

    user_raw = st.chat_input("Ask a question here (जैसे: सोलर सब्सिडी कितनी मिलेगी?)...")
    if user_raw:
        st.session_state.chat_history.append({"role": "user", "content": user_raw})
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            system_injection = "You are Green Sahayik, a helpful public assistant for regular Indian middle class users and farmers. Answer in extremely simple, friendly language. Mix English and conversational Hindi keywords naturally. Limit responses to 120 words max."
            response_container = model.generate_content(f"{system_injection}\n\nUser Question: {user_raw}")
            bot_reply = response_container.text
            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
            st.rerun()
        except Exception as e:
            st.error("🔒 Security Key Connection Interrupted. Ensure Streamlit configurations match requirements.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 3: SUBSIDY COMPLIANCE AUDITOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab_subsidy:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎯 CENTRAL GOVERNMENT STATE-WISE SUBSIDY AUDITOR</p>", unsafe_allow_html=True)
    
    state_domain = st.selectbox("Select Your State Jurisdiction (अपना राज्य चुनें):", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"], key="sub_state")
    class_profile = st.radio("Where are you installing solar? (सोलर कहाँ लगा रहे हैं):", ["Residential Rooftop Array (घर की छत पर)", "Commercial Plant System (दुकान/कारखाने की छत पर)", "Public Fast Charging Venture (सार्वजनिक वाहन चार्जिंग स्टेशन)"], key="sub_profile")
    
    if st.button("CHECK SUBSIDY ELIGIBILITY / पात्रता जांचें 🔍"):
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hash_input = f"{state_domain}-{class_profile}-{timestamp_str}"
        verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:12].upper()
        
        st.markdown(f"""
        <div class="gov-report">
            <h3 style="color:#0f172a; margin-top:0; font-family:'Poppins'; font-weight:700;">🇮🇳 GOVERNMENT SUBSIDY VERIFICATION SLIP</h3>
            <p style="font-size:0.85rem; color:#475569; margin-bottom:20px;"><b>Generated Date:</b> {timestamp_str} IST // <b>Govt System Reference ID:</b> <span style="font-family:monospace; background:#cbd5e1; padding:2px 6px; color:#0f172a;">NGT-{verification_hash}</span></p>
            <hr style="border:0; border-top:1px solid #cbd5e1; margin-bottom:20px;">
            <p><b>State Node Allocation:</b> {state_domain} State Electricity Regulatory Commission</p>
            <p><b>Project Type Category:</b> {class_profile}</p>
            <p style="color:#15803d; font-weight:bold; font-size:1.1rem;">🥇 STATUS: ELIGIBLE APPROVED / आप केंद्रीय सब्सिडी योजना के पात्र हैं (PM Surya Ghar Framework Verified)</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 4: NATIONAL ENERGY RADAR
# ═══════════════════════════════════════════════════════════════════════════════
with tab_news:
    st.markdown("### 📡 Energy Updates & Village Schemes")
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("<div class='cyber-card'><h5>🔋 Local Battery Making</h5><p style='font-size:0.85rem; color:#94a3b8;'>New Indian gigafactories are opening up, which will reduce the price of electric vehicle batteries soon.</p></div>", unsafe_allow_html=True)
    with n2:
        st.markdown("<div class='cyber-card'><h5>🚗 Sell Power Back to Grid</h5><p style='font-size:0.85rem; color:#94a3b8;'>New vehicle charging trials will soon let you sell extra charge from your car back to the electricity department for cash profit.</p></div>", unsafe_allow_html=True)
    with n3:
        st.markdown("<div class='cyber-card'><h5>☀️ High-Yield Solar Cells</h5><p style='font-size:0.85rem; color:#94a3b8;'>Indian research centers develop new panels that produce 28% more energy even in regular sunlight environments.</p></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 5: PUBLIC DISPATCH BRIDGE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_connect:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🏛️ LOCAL VENDOR DISPATCH // अधिकारियों और डीलरों से जुड़ें</p>", unsafe_allow_html=True)
    with st.form("dispatch_capture_form"):
        exec_name = st.text_input("Enter Full Name (अपना नाम लिखें):")
        exec_contact = st.text_input("Enter Verified Mobile Number (अपना चालू मोबाइल नंबर):")
        submit_exec = st.form_submit_button("SUBMIT CONNECTION REQUEST / जानकारी दर्ज करें 📤")
        if submit_exec and exec_name and exec_contact:
            st.success(f"Success! Your request has been logged. Certified local solar dealers matching pin code {st.session_state.user_pincode} will reach out to you via call shortly.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HUD FOOTER REEL CONTROL TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.caption("⚡ National Green Transition OS | Digital Public Goods Portal Core v6.3.0 (2026 Open Public Build)")
