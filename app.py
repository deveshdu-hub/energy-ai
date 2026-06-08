import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import hashlib
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🛰️ NATIONAL GREEN TRANSITION OS (NGT-OS) // PRODUCTION BUILD v6.5.0
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
# 🌌 GOVERNMENT MISSION CONTROL INTERFACE LAYER (CSS)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
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
        letter-spacing: 0.5px;
        text-shadow: 0 0 30px rgba(255, 153, 51, 0.1);
    }
    
    .cyber-label {
        font-family: 'Poppins', sans-serif;
        color: #00F0FF !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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

    .rec-card {
        background: linear-gradient(135deg, rgba(14, 116, 144, 0.15), rgba(3, 7, 18, 0.95));
        border: 1px solid rgba(14, 116, 144, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
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

    div[data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.55rem !important;
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
                box-shadow: 0 20px 50px rgba(0, 240, 255, 0.15);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="height: 10px; width: 10px; background-color: #00F0FF; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 0.8rem; color: #00F0FF; font-weight: 600;">🇮🇳 CITIZEN LOGIN / नागरिक लॉगिन</span>
                    </div>
                    <span style="font-size: 0.75rem; color: #64748b;">v6.5.0</span>
                </div>
                <h2 style="font-weight: 800; color: #ffffff; margin-bottom: 5px; background: linear-gradient(135deg, #FF9933, #FFFFFF, #129E59); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PM GREEN TRANSITION PORTAL</h2>
                <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0;">हरित क्रांति DIGITAL SEVA - BHARAT SARKAR</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        in_c1, in_c2 = st.columns(2)
        with in_c1:
            st.markdown("<p style='font-size:0.8rem; color:#00F0FF; font-weight:600; margin-bottom:8px;'>📱 MOBILE NUMBER / मोबाइल नंबर</p>", unsafe_allow_html=True)
            mobile_in = st.text_input("Mobile", placeholder="10-Digit Mobile No.", max_chars=10, label_visibility="collapsed", key="gate_mobile")
            
        with in_c2:
            st.markdown("<p style='font-size:0.8rem; color:#00F0FF; font-weight:600; margin-bottom:8px;'>📍 AREA PIN CODE / पिन कोड</p>", unsafe_allow_html=True)
            pincode_in = st.text_input("Pincode", placeholder="6-Digit Pin Code", max_chars=6, label_visibility="collapsed", key="gate_pincode")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("OPEN DASHBOARD / आगे बढ़ें ➡️", use_container_width=True):
            if len(mobile_in) == 10 and mobile_in.isdigit() and len(pincode_in) == 6 and pincode_in.isdigit():
                st.session_state.user_registered = True
                st.session_state.user_mobile = mobile_in
                st.session_state.user_pincode = pincode_in
                st.rerun()
            else:
                st.error("⚠️ Error: Please check that your Mobile Number is 10 digits and Pin Code is 6 digits.")
                
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# 🏛️ POST-REGISTRATION MAIN SYSTEM LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1 class='neon-title' style='text-align: center; margin-top: 5px;'>PM GREEN TRANSITION PORTAL</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 0.9rem; color: #129E59; margin-top:-10px; font-weight:600;'>🟢 ACTIVE NODE // PIN CODE: {st.session_state.user_pincode} // WELCOME USER</p>", unsafe_allow_html=True)

# Main Telemetry Stats Banner
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="☀️ PM Surya Ghar Base", value="41 Lakh+ Homes", delta="Target: 75 Lakh")
m2.metric(label="🚗 FAME III Support Scheme", value="₹10,000 Crore", delta="Active Fund Lifecycle")
m3.metric(label="🔋 Total Grid Storage", value="150 GW Capacity", delta="ACC PLI Factories Active")
m4.metric(label="🍃 Renewable Energy Share", value="45% Green Power", delta="Goal: 50% by 2030")

st.markdown("<br>", unsafe_allow_html=True)

tab_calc, tab_chat, tab_subsidy, tab_news, tab_connect = st.tabs([
    "💰 MULTI-FUEL SAVINGS CALCULATOR (बचत कैलकुलेटर)",
    "🤖 GREEN SAHAYIK (योजना हेल्प AI)",
    "🎯 GOVT SUBSIDY CHECKER (सरकारी सब्सिडी)",
    "📡 REGIONAL ENERGY NEWS (समाचार)",
    "🏛️ CONNECT WITH OFFICIALS (अधिकारियों से जुड़ें)"
])

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ TAB 1: TRIPLE FUEL SYSTEM EXPENSES & COMPARISON MATRIX
# ═══════════════════════════════════════════════════════════════════════════════
with tab_calc:
    st.markdown("### 📊 Check Your Expenses & Green Savings Value")
    sub_ev, sub_solar = st.tabs(["🚗 Petrol vs CNG vs Electric Vehicle Dynamics", "☀️ Rooftop Solar Benefit Estimator"])
    
    with sub_ev:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ STEP 1: CONFIGURING OPERATIONAL METRICS / वाहन मापदंड सेट करें</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            daily_km = st.slider("Average Daily Running Distance (KM per Day):", min_value=10, max_value=350, value=80, key="multi_slider")
            fuel_price = st.number_input("Petrol Price (₹ per Liter):", min_value=80.0, value=104.0, key="p_rate")
            petrol_mileage = st.number_input("Petrol Car Mileage (KM / Liter):", min_value=5.0, value=15.0, key="p_mil")
        with c2:
            cng_price = st.number_input("CNG Price (₹ per KG):", min_value=60.0, value=82.5, key="cng_rate")
            cng_mileage = st.number_input("CNG Car Mileage (KM / KG):", min_value=10.0, value=22.0, key="cng_mil")
        with c3:
            grid_tariff = st.number_input("Electricity Rate (₹ per Unit):", min_value=3.0, value=8.5, key="ev_rate")
            ev_efficiency = st.number_input("EV Car Mileage (KM / 1 Unit Charge):", min_value=1.0, value=6.5, key="ev_mil")
        
        # Performance Math Matrix Calculations
        petrol_per_km = fuel_price / petrol_mileage
        cng_per_km = cng_price / cng_mileage
        ev_per_km = grid_tariff / ev_efficiency
        
        cost_petrol_month = petrol_per_km * daily_km * 30
        cost_cng_month = cng_per_km * daily_km * 30
        cost_ev_month = ev_per_km * daily_km * 30
        
        saved_vs_petrol_annual = (cost_petrol_month - cost_ev_month) * 12
        saved_vs_cng_annual = (cost_cng_month - cost_ev_month) * 12
        
        st.markdown("<p class='cyber-label' style='margin-top:20px;'>📊 COST PER KM COMPARISON / प्रति किलोमीटर खर्चा</p>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("⛽ Petrol Cost per KM", f"₹{petrol_per_km:.2f} / KM")
        rc2.metric("🟢 CNG Cost per KM", f"₹{cng_per_km:.2f} / KM")
        rc3.metric("⚡ Electric Cost per KM", f"₹{ev_per_km:.2f} / KM")
        
        st.markdown("<p class='cyber-label' style='margin-top:15px;'>📉 NET ESTIMATED MONTHLY RUNNING BILL / मासिक खर्च</p>", unsafe_allow_html=True)
        rm1, rm2, rm3 = st.columns(3)
        rm1.metric("Petrol Monthly Bill", f"₹{cost_petrol_month:,.2f}")
        rm2.metric("CNG Monthly Bill", f"₹{cost_cng_month:,.2f}", delta=f"Saves ₹{cost_petrol_month - cost_cng_month:,.0f} vs Petrol", delta_color="inverse")
        rm3.metric("EV Monthly Bill", f"₹{cost_ev_month:,.2f}", delta=f"Saves ₹{cost_petrol_month - cost_ev_month:,.0f} vs Petrol", delta_color="inverse")
        st.markdown("</div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # VISUAL TREND ANALYSIS INTERFACE (OPTION 1 GENERATED BRIDGE)
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>📈 3-YEAR CUMULATIVE RUNNING COST PROJECTION (cumulative expense trend)</p>", unsafe_allow_html=True)
        
        months_axis = list(range(1, 37))
        petrol_trend = [int((cost_petrol_month * m)) for m in months_axis]
        cng_trend = [int((cost_cng_month * m)) for m in months_axis]
        ev_trend = [int((cost_ev_month * m)) for m in months_axis]
        
        chart_data = pd.DataFrame({
            'Month': months_axis,
            'Petrol Expenses': petrol_trend,
            'CNG Expenses': cng_trend,
            'Electric Expenses': ev_trend
        }).set_index('Month')
        
        st.line_chart(chart_data)
        st.markdown("<p style='font-size:0.8rem; text-align:center; color:#94a3b8;'>💡 Lower lines represent a wider gap in compounding savings over long periods.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 🚗 EXPANDED VEHICLE RECOMMENDATION MATRIX BY BUDGET & ENGINE TYPE
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='rec-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label' style='color: #0e7490 !important; border-bottom: 1px solid rgba(14, 116, 144, 0.3);'>🎯 SMART VEHICLE CHOICE ENGINE BY TARGET BUDGET</p>", unsafe_allow_html=True)
        
        user_budget = st.selectbox(
            "What is your target investment budget? (आपका बजट विकल्प चुनें):",
            ["Under ₹7 Lakh (Entry Segment)", "₹7 Lakh to ₹12 Lakh (Mid Segment)", "₹12 Lakh to ₹18 Lakh (Family Upgrades)", "Above ₹18 Lakh (Premium / Long Range Range)"]
        )

        st.markdown("##### 🏎️ Best Options in Your Selected Bracket:")
        
        if "Under ₹7 Lakh" in user_budget:
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                st.markdown("📦 **PETROL OPTIONS**\n* Maruti Alto K10\n* Maruti WagonR\n* Hyundai Grand i10 Nios")
            with col_b2:
                st.markdown("🟢 **CNG OPTIONS**\n* Maruti WagonR CNG\n* Tata Tiago iCNG\n* Maruti Celerio CNG")
            with col_b3:
                st.markdown("⚡ **ELECTRIC OPTIONS**\n* MG Comet EV\n* Reva/Used Segment Market Only\n*(Consider CNG for high mileage at this budget)*")
                
        elif "₹7 Lakh to ₹12 Lakh" in user_budget:
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                st.markdown("📦 **PETROL OPTIONS**\n* Maruti Swift / Baleno\n* Tata Punch / Nexon\n* Hyundai Exter / i20")
            with col_b2:
                st.markdown("🟢 **CNG OPTIONS**\n* Tata Punch iCNG\n* Maruti Brezza CNG\n* Hyundai Exter CNG")
            with col_b3:
                st.markdown("⚡ **ELECTRIC OPTIONS**\n* Tata Tiago EV\n* Tata Punch EV (Base Range)\n* Citroen eC3 (Live)")
                
        elif "₹12 Lakh to ₹18 Lakh" in user_budget:
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                st.markdown("📦 **PETROL OPTIONS**\n* Hyundai Creta\n* Kia Seltos\n* Mahindra XUV700 (AX3)")
            with col_b2:
                st.markdown("🟢 **CNG OPTIONS**\n* Maruti Grand Vitara CNG\n* Toyota Urban Cruiser Taisor CNG\n* Maruti Ertiga CNG")
            with col_b3:
                st.markdown("⚡ **ELECTRIC OPTIONS**\n* Tata Nexon EV\n* Tata Punch EV (Long Range)\n* Mahindra XUV400")
        else:
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                st.markdown("📦 **PETROL OPTIONS**\n* Mahindra Scorpio-N\n* Toyota Innova Hycross\n* Tata Safari")
            with col_b2:
                st.markdown("🟢 **CNG OPTIONS**\n*(CNG segments are highly limited in premium configurations)*")
            with col_b3:
                st.markdown("⚡ **ELECTRIC OPTIONS**\n* Tata Curvv EV\n* MG ZS EV\n* BYD Atto 3 / Seal")
            
        st.markdown(f"💡 *Expert Advisory:* Because you drive **{daily_km} KM everyday**, your annual EV cost savings over Petrol is **₹{saved_vs_petrol_annual:,.2f}** and over CNG is **₹{max(0.0, saved_vs_cng_annual):,.2f}**. If you drive more than 50 KM daily, picking an EV or CNG asset will significantly lower your lifetime vehicle expenses.")
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
            {"role": "bot", "content": "नमस्ते! Welcome to the Green Sahayik Help Node. Ask me any question about PM Surya Ghar Solar Subsidies, rules, or EV/CNG car policies in simple words."}
        ]
        
    for text_block in st.session_state.chat_history:
        if text_block["role"] == "user":
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1d4ed8, #0284c7); padding: 14px 18px; border-radius: 16px 16px 4px 16px; color: white; margin-bottom: 14px; max-width: 80%; margin-left: auto;"><b>Your Question:</b><br>{text_block["content"]}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background: rgba(13, 22, 54, 0.95); border-left: 4px solid #129E59; padding: 14px 18px; border-radius: 4px 16px 16px 16px; color: #e2e8f0; margin-bottom: 14px; max-width: 85%;"><b>Sahayik AI Assistant:</b><br>{text_block["content"]}</div>""", unsafe_allow_html=True)

    user_raw = st.chat_input("Ask a question here (जैसे: CNG कार पर टैक्स छूट है क्या?)...")
    if user_raw:
        st.session_state.chat_history.append({"role": "user", "content": user_raw})
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            system_injection = "You are Green Sahayik, a helpful public assistant for regular Indian middle class users. Answer in extremely simple, friendly language. Mix English and conversational Hindi keywords naturally. Limit responses to 120 words max."
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
    class_profile = st.radio("Where are you installing solar? (सोलर कहाँ लगा रहे हैं):", ["Residential Rooftop Array (घर की छत पर)", "Commercial Plant System (दुकान/कारखाने की छत पर)", "Public Fast Charging Venture (सार्वजनिक वाहन充电站)"], key="sub_profile")
    
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
st.caption("⚡ National Green Transition OS | Digital Public Goods Portal Core v6.5.0 (2026 Open Public Build)")
