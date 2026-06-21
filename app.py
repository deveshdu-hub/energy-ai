"""
BHARAT HARIT KRANTI PORTAL v8.0.1
FutureHQ.in | Business & Revenue Focused
- Removed Tax Engine
- Enhanced EV Charging Guide (cost, subsidies, ROI, vendor leads)
- New "Business Marketplace" tab (lead gen for solar & EV vendors)
- Auto-upgrade marker included (# AUTO-UPGRADE-AREA)
"""

import streamlit as st
import pandas as pd
import datetime
import hashlib
import os
import logging
from io import BytesIO

# Optional AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
class Config:
    APP_NAME = "Bharat Harit Kranti Portal"
    APP_VERSION = "8.0.1"
    COMPANY = "FutureHQ.in"
    SESSION_KEYS = {
        'user_registered': False,
        'user_mobile': "",
        'user_pincode': "",
        'chat_history': [{"role": "bot", "content": "नमस्ते! I'm Green Sahayik. Ask me about solar, EVs, or subsidies!"}],
    }
    MOBILE_LENGTH = 10
    PINCODE_LENGTH = 6
    SOLAR_COST_PER_KW = 62000
    SOLAR_AREA_PER_KW = 100
    BILL_TO_KW_RATIO = 1300
    SUBSIDY_PERCENTAGE = 0.60
    GRID_SELL_RATE = 4.50
    GRID_GENERATION_PER_KW = 4
    PUMP_CONFIGS = {
        "3 HP Pump": {"diesel_per_hour": 0.8, "solar_kw": 3.0, "setup_cost": 185000},
        "5 HP Pump": {"diesel_per_hour": 1.2, "solar_kw": 5.0, "setup_cost": 260000},
        "7.5 HP Pump": {"diesel_per_hour": 1.8, "solar_kw": 7.5, "setup_cost": 390000},
        "10 HP Pump": {"diesel_per_hour": 2.4, "solar_kw": 10.0, "setup_cost": 510000}
    }

# ─── SESSION INIT ──────────────────────────────────────────────────────────
def init_session_state():
    for key, default in Config.SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default

# ─── VALIDATION ────────────────────────────────────────────────────────────
def validate_mobile(mobile: str) -> bool:
    return mobile and len(mobile) == 10 and mobile.isdigit()
def validate_pincode(pincode: str) -> bool:
    return pincode and len(pincode) == 6 and pincode.isdigit()

# ─── GEMINI AI ────────────────────────────────────────────────────────────
def get_gemini_response(prompt: str) -> str:
    if not GENAI_AVAILABLE:
        return "🔧 AI not configured."
    try:
        api_key = None
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ API key missing."
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        sys_prompt = "You are Green Sahayik, an Indian green energy assistant. Respond in simple Hinglish. Keep answers under 120 words."
        response = model.generate_content(f"{sys_prompt}\n\nUser: {prompt}")
        return response.text if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "🤖 AI service temporarily unavailable."

# ─── CSS ──────────────────────────────────────────────────────────────────
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        .stApp {
            background: linear-gradient(135deg, #030611 0%, #0a0f2a 100%) !important;
            color: #f1f5f9;
            font-family: 'Poppins', sans-serif;
        }
        .neon-title {
            background: linear-gradient(135deg, #FF9933, #FFFFFF, #129E59);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
        }
        .cyber-card, .farmer-card {
            background: rgba(8, 14, 38, 0.88);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .farmer-card { border-color: #129E59; }
        .cyber-label {
            color: #00F0FF;
            font-weight: 600;
            border-bottom: 1px solid rgba(0,240,255,0.3);
            margin-bottom: 15px;
        }
        .gov-report {
            background: white;
            color: #1e293b;
            border-left: 6px solid #FF9933;
            border-right: 6px solid #129E59;
            padding: 20px;
            border-radius: 8px;
        }
        .news-update-badge {
            background: linear-gradient(90deg, #FF9933 0%, #129E59 100%);
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        .highlight-box {
            background: rgba(255, 153, 51, 0.1);
            border-left: 4px solid #FF9933;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        .profit-badge {
            background: #FF9933;
            color: #030611;
            padding: 2px 12px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.75rem;
            display: inline-block;
            margin-left: 10px;
        }
        @media (max-width: 768px) {
            .cyber-card { padding: 12px; }
            .stTabs [data-baseweb="tab"] { font-size: 0.7rem; padding: 6px 10px !important; }
        }
        </style>
    """, unsafe_allow_html=True)

# ─── REGISTRATION ──────────────────────────────────────────────────────────
def registration_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(13,22,54,0.95); border-radius: 20px; padding: 40px; text-align: center; border: 1px solid #00F0FF;">
                <h2 style="color:white;">🇮🇳 BHARAT HARIT KRANTI</h2>
                <p style="color:#94a3b8;">Citizen Access Portal</p>
            </div>
        """, unsafe_allow_html=True)
        with st.form("reg_form"):
            mobile = st.text_input("📱 Mobile Number (10 digits)", max_chars=10)
            pincode = st.text_input("📍 Pin Code (6 digits)", max_chars=6)
            if st.form_submit_button("Enter Dashboard"):
                if validate_mobile(mobile) and validate_pincode(pincode):
                    st.session_state.user_registered = True
                    st.session_state.user_mobile = mobile
                    st.session_state.user_pincode = pincode
                    st.rerun()
                else:
                    st.error("Invalid mobile or pincode.")
    st.stop()

# ─── VEHICLE CALCULATOR ──────────────────────────────────────────────────
def vehicle_calculator():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ Vehicle Cost Comparison</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            daily_km = st.slider("Daily KM", 10, 350, 80)
            petrol_price = st.number_input("Petrol ₹/L", 80.0, 120.0, 104.0)
            petrol_mileage = st.number_input("Petrol km/L", 5.0, 25.0, 15.0)
        with c2:
            cng_price = st.number_input("CNG ₹/kg", 60.0, 100.0, 82.5)
            cng_mileage = st.number_input("CNG km/kg", 10.0, 30.0, 22.0)
        with c3:
            elec_rate = st.number_input("Electricity ₹/unit", 3.0, 12.0, 8.5)
            ev_mileage = st.number_input("EV km/unit", 3.0, 10.0, 6.5)
        petrol_cost_km = petrol_price / petrol_mileage
        cng_cost_km = cng_price / cng_mileage
        ev_cost_km = elec_rate / ev_mileage
        monthly_petrol = petrol_cost_km * daily_km * 30
        monthly_cng = cng_cost_km * daily_km * 30
        monthly_ev = ev_cost_km * daily_km * 30
        st.markdown("#### Cost per km")
        mc = st.columns(3)
        mc[0].metric("Petrol", f"₹{petrol_cost_km:.2f}")
        mc[1].metric("CNG", f"₹{cng_cost_km:.2f}")
        mc[2].metric("EV", f"₹{ev_cost_km:.2f}")
        st.markdown("#### Monthly Running Cost")
        mc2 = st.columns(3)
        mc2[0].metric("Petrol", f"₹{monthly_petrol:,.0f}")
        mc2[1].metric("CNG", f"₹{monthly_cng:,.0f}", delta=f"Save ₹{monthly_petrol - monthly_cng:.0f}")
        mc2[2].metric("EV", f"₹{monthly_ev:,.0f}", delta=f"Save ₹{monthly_petrol - monthly_ev:.0f}")
        months = list(range(1, 37))
        data = pd.DataFrame({
            'Month': months,
            'Petrol': [monthly_petrol * m for m in months],
            'CNG': [monthly_cng * m for m in months],
            'EV': [monthly_ev * m for m in months]
        }).set_index('Month')
        st.line_chart(data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── SOLAR CALCULATOR ────────────────────────────────────────────────────
def solar_calculator():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>☀️ Rooftop Solar Estimator</p>", unsafe_allow_html=True)
        bill = st.number_input("Avg Monthly Bill (₹)", 500, 50000, 7500)
        area = st.number_input("Roof Area (sq ft)", 100, 5000, 500)
        max_kw = min(area / Config.SOLAR_AREA_PER_KW, bill / Config.BILL_TO_KW_RATIO)
        cost = max_kw * Config.SOLAR_COST_PER_KW
        carbon = max_kw * 1.3
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Recommended Size", f"{max_kw:.1f} kW")
        col_b.metric("Estimated Cost", f"₹{cost:,.0f}")
        col_c.metric("CO₂ Saved/Year", f"{carbon:.1f} tons")
        if max_kw < 1:
            st.info("💡 For better savings, consider reducing energy consumption first.")
        st.markdown("</div>", unsafe_allow_html=True)

# ─── FARMER SOLAR ──────────────────────────────────────────────────────────
def farmer_solar_calculator():
    with st.container():
        st.markdown("<div class='farmer-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🚜 Kisan Solar Pump Calculator</p>", unsafe_allow_html=True)
        pump = st.selectbox("Pump HP", list(Config.PUMP_CONFIGS.keys()))
        hours = st.slider("Monthly operating hours", 10, 200, 60)
        diesel_price = st.number_input("Diesel ₹/L", 85.0, 120.0, 92.5)
        cfg = Config.PUMP_CONFIGS[pump]
        monthly_diesel = hours * cfg["diesel_per_hour"] * diesel_price
        yearly_diesel = monthly_diesel * 12
        subsidy = cfg["setup_cost"] * Config.SUBSIDY_PERCENTAGE
        payable = cfg["setup_cost"] - subsidy
        yearly_grid_income = (hours * cfg["solar_kw"] * Config.GRID_GENERATION_PER_KW * Config.GRID_SELL_RATE * 30) / 1000
        st.markdown("#### Financial Summary")
        f1, f2, f3 = st.columns(3)
        f1.metric("Yearly Diesel Cost", f"₹{yearly_diesel:,.0f}")
        f2.metric("Subsidy (60%)", f"₹{subsidy:,.0f}")
        f3.metric("Your Payment", f"₹{payable:,.0f}")
        payback = payable / yearly_diesel if yearly_diesel > 0 else 0
        st.success(f"""
        ✅ **Payback Period:** ~{payback:.1f} years  
        ✅ **Grid Sell Income:** ₹{yearly_grid_income:,.0f}/year  
        ✅ **Zero diesel cost after installation**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── AI CHATBOT ──────────────────────────────────────────────────────────
def ai_chatbot():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤖 Green Sahayik AI</p>", unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div style='background:#1d4ed8; padding:10px; border-radius:15px; margin:5px 0; text-align:right; color:white;'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:rgba(13,22,54,0.9); border-left:4px solid #129E59; padding:10px; border-radius:10px; margin:5px 0;'><b>🤖 Sahayik:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        user_input = st.chat_input("Ask about solar subsidy, EV, PM Surya Ghar...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                reply = get_gemini_response(user_input)
                st.session_state.chat_history.append({"role": "bot", "content": reply})
            st.rerun()
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = [{"role": "bot", "content": "नमस्ते! I'm Green Sahayik. Ask me anything about green energy."}]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ─── SUBSIDY CHECKER ────────────────────────────────────────────────────
def subsidy_checker():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🎯 Subsidy Eligibility</p>", unsafe_allow_html=True)
        state = st.selectbox("State", ["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh"])
        ptype = st.radio("Project Type", ["Residential Rooftop", "Agricultural Pump", "Commercial"])
        if st.button("Check Eligibility"):
            ref = hashlib.md5(f"{state}{ptype}".encode()).hexdigest()[:8]
            st.markdown(f"""
                <div class="gov-report">
                    <h4>✅ Eligible for Subsidy</h4>
                    <p><strong>State:</strong> {state}<br>
                    <strong>Project:</strong> {ptype}<br>
                    <strong>Reference ID:</strong> HRT-{ref}<br>
                    <strong>Next Step:</strong> Contact local DISCOM with this report.</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── NEWS SECTION ──────────────────────────────────────────────────────
def news_section():
    st.markdown("### 📡 PM SURYA GHAR MUFT BIJLI YOJANA HUB")
    st.markdown("""
        <div class='cyber-card' style="border-left: 5px solid #FF9933; background: rgba(255, 153, 51, 0.05);">
            <span class='news-update-badge'>🔥 CORE DIRECTIVE</span>
            <h4 style="color:#FF9933;">प्रधानमंत्री सूर्य घर मुफ्त बिजली योजना Framework</h4>
            <p>Launched with ₹75,021 Crores, aims to install rooftop solar across 1 Crore households. Eligible households receive up to 300 Units free electricity monthly.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("#### 📊 Official Subsidy Slab Structure")
    subsidy_data = pd.DataFrame({
        "System Capacity": ["1 kW", "2 kW", "3 kW or Higher", "Group Housing (per kW)"],
        "Subsidy": ["₹30,000", "₹60,000", "₹78,000 (Max)", "₹18,000"],
        "Suitable Load": ["Up to 150 units/mo", "150-300 units/mo", ">300 units/mo", "Common Area"]
    })
    st.table(subsidy_data)
    st.markdown(
        "<a href='https://pmsuryaghar.gov.in' target='_blank' style='display:block; text-align:center; background:#129E59; color:white; padding:12px; border-radius:8px; text-decoration:none; font-weight:bold;'>🌐 Apply on Official PM Surya Ghar Portal</a>",
        unsafe_allow_html=True
    )

# ─── COMMUNITY CONNECTOR (Vendor Leads) ────────────────────────────────
def community_connector():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤝 Connect with Local Vendors</p>", unsafe_allow_html=True)
        with st.form("vendor_form"):
            name = st.text_input("Full Name")
            contact = st.text_input("Mobile Number", max_chars=10)
            if st.form_submit_button("Submit"):
                if name and validate_mobile(contact):
                    st.success(f"✅ Local vendors in {st.session_state.user_pincode} will contact you soon.")
                else:
                    st.warning("Enter valid name and 10-digit mobile.")
        st.markdown("</div>", unsafe_allow_html=True)

# ─── ENHANCED EV CHARGING GUIDE ──────────────────────────────────────
def ev_charging_guide():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🔌 EV Charging Station – Complete Setup & Profit Guide</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:rgba(0,240,255,0.05); border-left:4px solid #00F0FF; padding:15px; border-radius:6px; margin-bottom:20px;">
            <b>🚗 Go Electric – Set Up Your Own Charging Point.</b><br>
            Charger types, installation steps, costs, subsidies, ROI, and how you can turn this into a business.
            <span class='profit-badge'>💰 Profit Opportunity</span>
        </div>
    """, unsafe_allow_html=True)

    charger_data = pd.DataFrame({
        "Type": ["Level 1 (AC)", "Level 2 (AC)", "DC Fast Charger"],
        "Voltage": ["230V (15A)", "230V (32A)", "480V (3-Phase)"],
        "Power": ["2.3–3.3 kW", "7–22 kW", "50–350 kW"],
        "Charging Time": ["8–12 hrs", "3–6 hrs", "20–40 min"],
        "Best For": ["Home (overnight)", "Home / Office", "Commercial / Public"],
        "Approx Cost (₹)": ["15,000–25,000", "40,000–80,000", "5,00,000+"],
        "Avg. ROI (Years)": ["2-3", "2-4", "3-5"],
        "Business Model": ["Personal Use", "Semi-Public", "Public Charging"]
    })
    st.dataframe(charger_data, use_container_width=True, hide_index=True)

    st.markdown("#### 📋 5-Step Installation & Profit Checklist")
    steps = [
        ("1. Site Assessment", "Check load capacity, parking space, and grid connection. Business: assess footfall for public charging."),
        ("2. Choose Charger", "Select Level 1 or 2 based on usage. Business: choose Level 2 or DC Fast for commercial."),
        ("3. Hire Licensed Electrician", "Install dedicated MCB, RCD, earthing. Business: get multiple quotes to reduce CAPEX."),
        ("4. Mount and Connect", "Wall-mount near parking. Business: consider branding and payment integration."),
        ("5. Test & Commission", "Test charging, register for net metering. Business: apply for FAME-II subsidy, set up payment gateway.")
    ]
    for step, desc in steps:
        st.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:10px; border-radius:6px; margin-bottom:8px;'><b>{step}</b><br>{desc}</div>", unsafe_allow_html=True)

    st.markdown("#### 💰 Installation Cost Estimator & ROI")
    col1, col2 = st.columns(2)
    with col1:
        charger_type = st.selectbox("Charger Type", ["Level 1 (3.3 kW)", "Level 2 (7 kW)", "Level 2 (22 kW)"])
        cable_length = st.slider("Cable length (m)", 5, 50, 15)
        labour = st.number_input("Labour & Misc (₹)", min_value=0, value=5000, step=1000)
    with col2:
        daily_users = st.number_input("Expected daily charging sessions (business)", min_value=0, value=10, step=5)
        charge_fee = st.number_input("Charge price per session (₹)", min_value=0, value=150, step=50)
    
    if st.button("Calculate Total Cost & Profit Potential"):
        base = {"Level 1 (3.3 kW)": 20000, "Level 2 (7 kW)": 50000, "Level 2 (22 kW)": 75000}
        total_cost = base[charger_type] + cable_length * 200 + labour
        daily_revenue = daily_users * charge_fee
        monthly_revenue = daily_revenue * 30
        yearly_revenue = monthly_revenue * 12
        payback_years = total_cost / yearly_revenue if yearly_revenue > 0 else 999
        
        st.success(f"**Estimated Total Cost:** ₹{total_cost:,.0f}")
        st.info(f"""
        **Revenue Projection (Business Model):**
        - Daily Revenue: ₹{daily_revenue:,.0f}
        - Monthly Revenue: ₹{monthly_revenue:,.0f}
        - Yearly Revenue: ₹{yearly_revenue:,.0f}
        - Payback Period: {payback_years:.1f} years
        """)
        if payback_years < 2:
            st.markdown("<span class='profit-badge'>🔥 Highly Profitable!</span>", unsafe_allow_html=True)

    st.markdown("#### 🏛️ Government Subsidies & Business Incentives")
    st.markdown("""
        - **FAME-II Scheme** – up to 60% subsidy on public charging infrastructure (CAPEX support).
        - **State EV Policies** – additional incentives (Delhi, Maharashtra, Karnataka offer land, electricity tariff discounts).
        - **Net Metering** – offset charging cost with solar, reducing OPEX.
        - **Business Loans** – Special EV infrastructure loans from PSU banks at 7-9% interest.
        - **GST** – 5% GST on EV charging services (input credit available).
    """)

    st.markdown("#### 💸 How This Tab Generates Revenue for Us")
    st.markdown("""
        - **Lead Generation:** Users submit their details to get quotes from installers – we charge ₹200-₹500 per lead to vendors.
        - **Affiliate Commissions:** Recommend specific charger brands (e.g., Tata Power, Servotech) – earn 5-10% on sales.
        - **Premium Listing:** Vendors can pay ₹2,500/month to be featured as preferred installers.
        - **Data Analytics:** Anonymized charging demand data can be sold to utility companies and urban planners.
    """)

    st.markdown("#### 🤝 Find a Local EV Charger Installer (Lead Generation)")
    with st.form("ev_vendor"):
        name = st.text_input("Full Name")
        contact = st.text_input("Mobile Number", max_chars=10)
        if st.form_submit_button("Connect with Installers"):
            if name and validate_mobile(contact):
                st.success(f"✅ Installers in {st.session_state.user_pincode} will contact you.")
            else:
                st.warning("Valid name & 10-digit mobile required.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ─── BUSINESS MARKETPLACE TAB ─────────────────────────────────────────
def business_marketplace():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🏪 Business Marketplace – Vendor & Partner Hub</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='highlight-box'>
            <b>Turn your green energy interest into a revenue stream.</b><br>
            We connect you with verified vendors for solar, EV charging, and energy efficiency products.
        </div>
    """, unsafe_allow_html=True)

    categories = ["Solar Installation", "EV Charger Installation", "Energy Auditing", "Green Loans & Financing"]
    selected_category = st.selectbox("Select Service Type", categories)
    
    vendors = pd.DataFrame({
        "Company Name": ["SolarMax India", "EVChargePro", "EcoPower Solutions"],
        "Rating": ["4.8 ⭐", "4.5 ⭐", "4.2 ⭐"],
        "Services": ["Rooftop Solar, Pump", "Level 2 & DC Fast Charger", "Solar + Storage"],
        "Coverage": ["Pan India", "Maharashtra, Gujarat", "Delhi NCR"],
        "Starting Price": ["₹50,000", "₹75,000", "₹1,20,000"]
    })
    st.dataframe(vendors, use_container_width=True, hide_index=True)

    with st.form("business_lead"):
        name = st.text_input("Your Full Name")
        mobile = st.text_input("Mobile Number", max_chars=10)
        project_desc = st.text_area("Describe your requirement")
        if st.form_submit_button("Request Quote"):
            if name and validate_mobile(mobile):
                st.success("✅ Your request has been sent to top vendors. You'll hear back within 24 hours.")
            else:
                st.warning("Please fill all fields correctly.")
    
    st.markdown("""
        <div style="background:rgba(255,153,51,0.1); padding:10px; border-radius:6px; margin-top:20px; border:1px solid #FF9933;">
            <b>💰 Revenue Generation:</b> Each lead is sold to vendors at ₹300-₹500. With 1000 leads/month, we earn ₹3-5 Lakhs.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# 🔁 AUTO-UPGRADE MARKER – daily_upgrade.py will inject new code here
# ═══════════════════════════════════════════════════════════════════════════
# AUTO-UPGRADE-AREA

# ─── MAIN ──────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Bharat Harit Kranti", page_icon="🌾", layout="wide")
    init_session_state()
    load_css()
    if not st.session_state.user_registered:
        registration_screen()
    st.markdown(f"<h1 class='neon-title'>{Config.APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>🟢 Pincode: {st.session_state.user_pincode} | Welcome Citizen</p>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("☀️ Rooftop Solar", "41 Lakh+", "Target 75 Lakh")
    m2.metric("🌾 Solar Pumps", "7.5 Lakh+", "60% Subsidy")
    m3.metric("🔋 Grid Storage", "150 GW", "Local Manufacturing")
    m4.metric("🍃 Green Share", "45%", "Goal 50%")
    
    tabs = st.tabs(["💰 Calculator", "🤖 AI Assistant", "🎯 Subsidy", "📡 News", "🤝 Connect", "🔌 EV Charging", "🏪 Marketplace"])
    with tabs[0]:
        sub_tabs = st.tabs(["🚗 Vehicle", "☀️ Solar", "🌾 Farmer"])
        with sub_tabs[0]: vehicle_calculator()
        with sub_tabs[1]: solar_calculator()
        with sub_tabs[2]: farmer_solar_calculator()
    with tabs[1]: ai_chatbot()
    with tabs[2]: subsidy_checker()
    with tabs[3]: news_section()
    with tabs[4]: community_connector()
    with tabs[5]: ev_charging_guide()
    with tabs[6]: business_marketplace()
    
    st.caption(f"⚡ {Config.APP_NAME} v{Config.APP_VERSION} | FutureHQ.in – Building Green Businesses")

if __name__ == "__main__":
    main()
```

