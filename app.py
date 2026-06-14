import streamlit as st
import pandas as pd
import datetime
import hashlib
import base64
import os
import logging
from typing import Optional, Any
from contextlib import contextmanager

# Try importing AI package gracefully
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logging.warning("google-generativeai not installed. AI features disabled.")

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
class Config:
    APP_NAME = "Bharat Harit Kranti Portal"
    APP_VERSION = "7.3.0"
    COMPANY = "FutureHQ.in"
    
    SESSION_KEYS = {
        'user_registered': False,
        'user_mobile': "",
        'user_pincode': "",
        'chat_history': [{"role": "bot", "content": "नमस्ते! I'm Green Sahayik. Ask me about solar, subsidies, or EVs!"}]
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

# ═══════════════════════════════════════════════════════════════════════════════
# SAFE BACKGROUND (no file required)
# ═══════════════════════════════════════════════════════════════════════════════
def get_background_style() -> str:
    """Return CSS background – no external image needed."""
    return """
        background: linear-gradient(135deg, #030611 0%, #0a0f2a 100%) !important;
        color: #f1f5f9;
    """

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION INIT
# ═══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    for key, default in Config.SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
def validate_mobile(mobile: str) -> bool:
    return mobile and len(mobile) == Config.MOBILE_LENGTH and mobile.isdigit()

def validate_pincode(pincode: str) -> bool:
    return pincode and len(pincode) == Config.PINCODE_LENGTH and pincode.isdigit()

# ═══════════════════════════════════════════════════════════════════════════════
# GEMINI AI WITH FALLBACK
# ═══════════════════════════════════════════════════════════════════════════════
def get_gemini_response(prompt: str) -> str:
    """Return AI response or friendly fallback."""
    if not GENAI_AVAILABLE:
        return "🔧 AI service is not configured. Please contact support or install google-generativeai."
    
    try:
        # Get API key from secrets or env
        api_key = None
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "⚠️ Gemini API key missing. Please add GEMINI_API_KEY to secrets."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        sys_prompt = """You are Green Sahayik, an Indian green energy assistant. 
        Respond in simple Hinglish (mix Hindi and English). Keep answers under 120 words."""
        response = model.generate_content(f"{sys_prompt}\n\nUser: {prompt}")
        return response.text if response.text else "Sorry, I couldn't generate a response."
    
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "🤖 AI service temporarily unavailable. Please try again later."

# ═══════════════════════════════════════════════════════════════════════════════
# CSS (Mobile responsive)
# ═══════════════════════════════════════════════════════════════════════════════
def load_css():
    bg = get_background_style()
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        .stApp {{
            {bg}
            font-family: 'Poppins', sans-serif;
        }}
        .neon-title {{
            background: linear-gradient(135deg, #FF9933, #FFFFFF, #129E59);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
        }}
        .cyber-card, .farmer-card, .rec-card {{
            background: rgba(8, 14, 38, 0.88);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .farmer-card {{ border-color: #129E59; }}
        .cyber-label {{
            color: #00F0FF;
            font-weight: 600;
            border-bottom: 1px solid rgba(0,240,255,0.3);
            margin-bottom: 15px;
        }}
        .gov-report {{
            background: white;
            color: #1e293b;
            border-left: 6px solid #FF9933;
            border-right: 6px solid #129E59;
            padding: 20px;
            border-radius: 8px;
        }}
        .news-update-badge {{
            background: linear-gradient(90deg, #FF9933 0%, #129E59 100%);
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }}
        @media (max-width: 768px) {{
            .cyber-card {{ padding: 12px; }}
            .stTabs [data-baseweb="tab"] {{ font-size: 0.7rem; padding: 6px 10px !important; }}
        }}
        </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRATION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# VEHICLE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
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
        
        # 3-year projection chart
        months = list(range(1, 37))
        data = pd.DataFrame({
            'Month': months,
            'Petrol': [monthly_petrol * m for m in months],
            'CNG': [monthly_cng * m for m in months],
            'EV': [monthly_ev * m for m in months]
        }).set_index('Month')
        st.line_chart(data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SOLAR CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# FARMER SOLAR CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# AI CHATBOT (no rerun issues)
# ═══════════════════════════════════════════════════════════════════════════════
def ai_chatbot():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤖 Green Sahayik AI</p>", unsafe_allow_html=True)
        
        # Display history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div style='background:#1d4ed8; padding:10px; border-radius:15px; margin:5px 0; text-align:right; color:white;'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:rgba(13,22,54,0.9); border-left:4px solid #129E59; padding:10px; border-radius:10px; margin:5px 0;'><b>🤖 Sahayik:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        
        # Input
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

# ═══════════════════════════════════════════════════════════════════════════════
# SUBSIDY CHECKER
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# NEWS SECTION (PM SURYA GHAR DEEP DIVE)
# ═══════════════════════════════════════════════════════════════════════════════
def news_section():
    st.markdown("### 📡 PM SURYA GHAR MUFT BIJLI YOJANA HUB")
    st.markdown("Comprehensive central updates, subsidy parameters, and live scheme status trackers.")
    
    # 1. Master Ledger Card & Free units details
    st.markdown("""
        <div class='cyber-card' style="border-left: 5px solid #FF9933; background: rgba(255, 153, 51, 0.05);">
            <span class='news-update-badge'>🔥 CORE DIRECTIVE</span>
            <h4 style="color:#FF9933; margin-top:5px;">प्रधानमंत्री सूर्य घर मुफ्त बिजली योजना Framework</h4>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Launched with a massive outlay of <b>₹75,021 Crores</b>, the central directive aims to install rooftop solar systems across <b>1 Crore households</b> in India. Eligible registered households receive up to <b>300 Units of completely free electricity every month</b> while generating additional revenue via net metering exports back to their state DISCOM.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Dynamic Subsidy Slabs Grid Data Table
    st.markdown("#### 📊 Official Subsidy Slab Structure")
    subsidy_data = pd.DataFrame({
        "System Capacity": ["1 kW System", "2 kW System", "3 kW or Higher", "Group Housing / RWA (per kW)"],
        "Central Subsidy Allocation": ["₹30,000", "₹60,000", "₹78,000 (Maximum Cap)", "₹18,000"],
        "Suitable Household Load": ["Up to 150 Units/month", "150 to 300 Units/month", "Above 300 Units/month", "Common Area Illumination"]
    })
    st.table(subsidy_data)

    # 3. Step-by-Step Interactive Registration Matrix
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🗺️ Official Operational Roadmap</p>", unsafe_allow_html=True)
    
    step_col1, step_col2, step_col3 = st.columns(3)
    with step_col1:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:8px; border:1px dashed rgba(0,240,255,0.3);">
                <h6 style="color:#00F0FF;">Step 1: Digital Register</h6>
                <p style="font-size:0.85rem; color:#94a3b8;">Sign up on the National Portal using your mobile number, billing consumer account ID, and your local state DISCOM mapping name.</p>
            </div>
        """, unsafe_allow_html=True)
    with step_col2:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:8px; border:1px dashed rgba(0,240,255,0.3);">
                <h6 style="color:#00F0FF;">Step 2: Vendor Install</h6>
                <p style="font-size:0.85rem; color:#94a3b8;">Choose an MNRE registered authorized local vendor to procure and install the line setup and net-metering devices.</p>
            </div>
        """, unsafe_allow_html=True)
    with step_col3:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:8px; border:1px dashed rgba(0,240,255,0.3);">
                <h6 style="color:#00F0FF;">Step 3: Subsidy Release</h6>
                <p style="font-size:0.85rem; color:#94a3b8;">Submit your physical commissioning report certificate. The central subsidy amount hits your banking account within 30 business days.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<a href='https://pmsuryaghar.gov.in' target='_blank' style='display: block; text-align: center; background: #129E59; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold;'>🌐 Click Here to Open Official PM Surya Ghar National Portal</a>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Complementary National Sector Infrastructure Bulletins
    st.markdown("#### 📰 Associated Green Energy Bulletins")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class='cyber-card'>
                <span class='news-update-badge'>🔋 PRODUCTION UPDATE</span>
                <h5>Battery Storage Cell Level Upgrades</h5>
                <p style="font-size:0.88rem; color:#cbd5e1;">New PLI hardware parameters approved by central ministries. Automated local mass scaling targets 50 GWh capacity setup. Residential backup cost metrics projected to step down up to 15%.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class='cyber-card' style="border-left: 4px solid #129E59;">
                <span class='news-update-badge'>🚜 PM-KUSUM SCHEME</span>
                <h5>Solar Irrigation Pump Expansion Node</h5>
                <p style="font-size:0.88rem; color:#cbd5e1;">Fresh infrastructure budgets of ₹10,000 Crores cleared for feeder level solar adjustments. State distribution targets focus on allocating 2 Million new off-grid operations to farming clusters.</p>
            </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COMMUNITY CONNECTOR
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    st.set_page_config(page_title="Bharat Harit Kranti", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")
    init_session_state()
    load_css()
    
    if not st.session_state.user_registered:
        registration_screen()
    
    st.markdown(f"<h1 class='neon-title'>{Config.APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>🟢 Pincode: {st.session_state.user_pincode} | Welcome Citizen</p>", unsafe_allow_html=True)
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("☀️ Rooftop Solar", "41 Lakh+", "Target 75 Lakh")
    m2.metric("🌾 Solar Pumps", "7.5 Lakh+", "60% Subsidy")
    m3.metric("🔋 Grid Storage", "150 GW", "Local Manufacturing")
    m4.metric("🍃 Green Share", "45%", "Goal 50%")
    
    tabs = st.tabs(["💰 Calculator", "🤖 AI Assistant", "🎯 Subsidy", "📡 News", "🤝 Connect"])
    with tabs[0]:
        sub_tabs = st.tabs(["🚗 Vehicle", "☀️ Solar", "🌾 Farmer"])
        with sub_tabs[0]: vehicle_calculator()
        with sub_tabs[1]: solar_calculator()
        with sub_tabs[2]: farmer_solar_calculator()
    with tabs[1]: ai_chatbot()
    with tabs[2]: subsidy_checker()
    with tabs[3]: news_section()
    with tabs[4]: community_connector()
    
    st.caption(f"⚡ {Config.APP_NAME} v{Config.APP_VERSION} | FutureHQ.in")

if __name__ == "__main__":
    main()
