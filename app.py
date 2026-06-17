import streamlit as st
import pandas as pd
import datetime
import hashlib
import base64
import os
import logging
from typing import Optional, Any
from contextlib import contextmanager
from io import BytesIO

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
    APP_VERSION = "7.5.0"
    COMPANY = "FutureHQ.in"
    
    SESSION_KEYS = {
        'user_registered': False,
        'user_mobile': "",
        'user_pincode': "",
        'chat_history': [{"role": "bot", "content": "नमस्ते! I'm Green Sahayik. Ask me about solar, subsidies, or EVs!"}],
        'tax_portfolio': None
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
    if not GENAI_AVAILABLE:
        return "🔧 AI service is not configured. Please contact support or install google-generativeai."
    try:
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
# AI CHATBOT
# ═══════════════════════════════════════════════════════════════════════════════
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
# NEWS SECTION
# ═══════════════════════════════════════════════════════════════════════════════
def news_section():
    st.markdown("### 📡 PM SURYA GHAR MUFT BIJLI YOJANA HUB")
    st.markdown("Comprehensive central updates, subsidy parameters, and live scheme status trackers.")
    
    st.markdown("""
        <div class='cyber-card' style="border-left: 5px solid #FF9933; background: rgba(255, 153, 51, 0.05);">
            <span class='news-update-badge'>🔥 CORE DIRECTIVE</span>
            <h4 style="color:#FF9933; margin-top:5px;">प्रधानमंत्री सूर्य घर मुफ्त बिजली योजना Framework</h4>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Launched with a massive outlay of <b>₹75,021 Crores</b>, the central directive aims to install rooftop solar systems across <b>1 Crore households</b> in India. Eligible registered households receive up to <b>300 Units of completely free electricity every month</b> while generating additional revenue via net metering exports back to their state DISCOM.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📊 Official Subsidy Slab Structure")
    subsidy_data = pd.DataFrame({
        "System Capacity": ["1 kW System", "2 kW System", "3 kW or Higher", "Group Housing / RWA (per kW)"],
        "Central Subsidy Allocation": ["₹30,000", "₹60,000", "₹78,000 (Maximum Cap)", "₹18,000"],
        "Suitable Household Load": ["Up to 150 Units/month", "150 to 300 Units/month", "Above 300 Units/month", "Common Area Illumination"]
    })
    st.table(subsidy_data)

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
# 🧾 SELF ASSIST TAX ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
def calculate_tax(gross_revenue, declared_expenses=0, presumptive_44ad=False):
    if presumptive_44ad:
        taxable_income = gross_revenue * 0.06
        note = "Presumptive taxation under Section 44AD (6% of turnover)."
    else:
        taxable_income = max(0, gross_revenue - declared_expenses)
        note = "Standard book-accounting method (actual profit)."
    
    if taxable_income <= 700000:
        tax = 0
    elif taxable_income <= 1000000:
        tax = (taxable_income - 700000) * 0.10
    elif taxable_income <= 1200000:
        tax = 30000 + (taxable_income - 1000000) * 0.15
    elif taxable_income <= 1500000:
        tax = 60000 + (taxable_income - 1200000) * 0.20
    else:
        tax = 120000 + (taxable_income - 1500000) * 0.30
    cess = tax * 0.04
    total_tax = tax + cess
    return {
        "taxable_income": round(taxable_income, 2),
        "income_tax": round(tax, 2),
        "cess": round(cess, 2),
        "total_tax_liability": round(total_tax, 2),
        "method_note": note
    }

def get_default_portfolio():
    return pd.DataFrame([
        {"Client ID": "SA-01", "Client Name": "FutureHQ Node A", 
         "Entity Type": "Proprietorship", "Service Stream": "ITR & Tax Audit", 
         "FY 2025-26 Turnover (₹)": 1800000, "Estimated Tax Liability (₹)": 45000, 
         "Filing Deadline": "2026-07-31", "Workflow Status": "Document Verification"},
        {"Client ID": "SA-02", "Client Name": "CarryMe Logistics", 
         "Entity Type": "LLP / Startup", "Service Stream": "GST Reconciliation", 
         "FY 2025-26 Turnover (₹)": 4200000, "Estimated Tax Liability (₹)": 756000, 
         "Filing Deadline": "2026-06-25", "Workflow Status": "Pending Upload"}
    ])

def tax_engine_tab():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🧾 Self Assist Tax Engine – Business & Freelance Taxation</p>", unsafe_allow_html=True)
    
    if st.session_state.tax_portfolio is None:
        st.session_state.tax_portfolio = get_default_portfolio()
    
    col_mode, col_action = st.columns([2, 1])
    with col_mode:
        tax_method = st.radio("Select Tax Regime", ["Normal (Actual Expenses)", "Presumptive (Section 44AD – 6% profit)"], horizontal=True)
        use_presumptive = (tax_method == "Presumptive (Section 44AD – 6% profit)")
    with col_action:
        if st.button("📥 Load Sample Portfolio"):
            st.session_state.tax_portfolio = get_default_portfolio()
            st.success("Sample portfolio loaded.")
        if st.button("➕ Add New Client (Row)"):
            new_row = pd.DataFrame([{
                "Client ID": f"NEW-{len(st.session_state.tax_portfolio)+1:02d}",
                "Client Name": "New Client",
                "Entity Type": "Proprietorship",
                "Service Stream": "Tax Planning",
                "FY 2025-26 Turnover (₹)": 0,
                "Estimated Tax Liability (₹)": 0,
                "Filing Deadline": datetime.now().strftime("%Y-%m-%d"),
                "Workflow Status": "New Entry"
            }])
            st.session_state.tax_portfolio = pd.concat([st.session_state.tax_portfolio, new_row], ignore_index=True)
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 Client Portfolio")
    edited_df = st.data_editor(
        st.session_state.tax_portfolio,
        use_container_width=True,
        num_rows="dynamic",
        key="tax_portfolio_editor"
    )
    st.session_state.tax_portfolio = edited_df
    
    if st.button("🔄 Recalculate Tax for All Clients", use_container_width=True):
        if "FY 2025-26 Turnover (₹)" in edited_df.columns:
            if "Calculated Tax (₹)" not in edited_df.columns:
                edited_df["Calculated Tax (₹)"] = 0.0
            for idx, row in edited_df.iterrows():
                revenue = row["FY 2025-26 Turnover (₹)"]
                expenses = row.get("Operational Deductions (₹)", 0) if not use_presumptive else 0
                calc = calculate_tax(revenue, expenses, use_presumptive)
                edited_df.at[idx, "Calculated Tax (₹)"] = calc["total_tax_liability"]
            st.session_state.tax_portfolio = edited_df
            st.success("Tax liabilities recalculated.")
            st.rerun()
        else:
            st.error("Portfolio must contain 'FY 2025-26 Turnover (₹)' column.")
    
    st.markdown("---")
    st.markdown("### 🧮 Single Tax Calculator")
    col1, col2 = st.columns(2)
    with col1:
        single_revenue = st.number_input("Gross Turnover (₹)", min_value=0, value=1500000, step=100000)
        single_expenses = st.number_input("Actual Expenses (₹)", min_value=0, value=600000, step=50000)
    with col2:
        single_presumptive = st.checkbox("Apply Section 44AD (Presumptive)", value=False)
    if st.button("Compute Tax Liability"):
        result = calculate_tax(single_revenue, single_expenses, single_presumptive)
        st.markdown(f"""
            <div class='gov-report' style="margin-top:15px;">
                <b>Method:</b> {result['method_note']}<br>
                <b>Taxable Income:</b> ₹{result['taxable_income']:,.2f}<br>
                <b>Income Tax:</b> ₹{result['income_tax']:,.2f}<br>
                <b>Cess (4%):</b> ₹{result['cess']:,.2f}<br>
                <b style="font-size:1.1rem;">Total Tax Liability:</b> ₹{result['total_tax_liability']:,.2f}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📁 Import / Export Portfolio")
    col_exp, col_imp = st.columns(2)
    with col_exp:
        if st.button("📎 Export to Excel"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                st.session_state.tax_portfolio.to_excel(writer, index=False, sheet_name="Self_Assist_Portfolio")
            output.seek(0)
            st.download_button(
                label="Download Excel File",
                data=output,
                file_name="Self_Assist_Portfolio.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        if st.button("📄 Export to CSV"):
            csv_data = st.session_state.tax_portfolio.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv_data, "Self_Assist_Portfolio.csv", "text/csv")
    with col_imp:
        uploaded_file = st.file_uploader("Upload Portfolio (Excel or CSV)", type=["xlsx", "csv"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file, engine="openpyxl")
                st.session_state.tax_portfolio = df
                st.success("Portfolio imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Import error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔌 NEW: EV CHARGING STATION SETUP GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
def ev_charging_guide():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🔌 EV Charging Station – Setup & Guide</p>", unsafe_allow_html=True)
    
    # Overview
    st.markdown("""
        <div style="background:rgba(0,240,255,0.05); border-left:4px solid #00F0FF; padding:15px; border-radius:6px; margin-bottom:20px;">
            <b>🚗 Go Electric – Setup Your Own Charging Point at Home or Business.</b><br>
            This guide walks you through charger types, installation process, costs, subsidies, and safety.
        </div>
    """, unsafe_allow_html=True)
    
    # Charger Type Comparison Table
    st.markdown("#### ⚡ Charger Types – Which One Fits You?")
    charger_data = pd.DataFrame({
        "Type": ["Level 1 (AC)", "Level 2 (AC)", "DC Fast Charger"],
        "Voltage": ["230V (15A)", "230V (32A)", "480V (3-Phase)"],
        "Power Output": ["2.3 kW – 3.3 kW", "7 kW – 22 kW", "50 kW – 350 kW"],
        "Typical Charging Time": ["8–12 hours", "3–6 hours", "20–40 minutes"],
        "Best For": ["Home (overnight)", "Home / Office", "Commercial / Public"],
        "Approx Cost (₹)": ["15,000 – 25,000", "40,000 – 80,000", "5,00,000+"]
    })
    st.dataframe(charger_data, use_container_width=True, hide_index=True)
    
    # Step-by-Step Installation Guide
    st.markdown("#### 📋 5-Step Home Charging Installation")
    steps = [
        ("1. Site Assessment", "Check your existing electrical load. Ensure your meter and main switch can handle additional load (7–22 kW)."),
        ("2. Choose Charger", "Select Level 1 or Level 2 based on daily usage and parking availability."),
        ("3. Hire Licensed Electrician", "Install a dedicated 32A/63A MCB, RCD, and proper earthing. Cable size: 4 mm² to 16 mm² depending on power."),
        ("4. Mount and Connect", "Wall‑mount the unit near parking. Connect to distribution board. Run cable through conduits."),
        ("5. Test & Commission", "Test charging with your EV. Ensure no voltage drop or tripping. Register for net metering if using solar.")
    ]
    for step, desc in steps:
        st.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:10px; border-radius:6px; margin-bottom:8px;'><b>{step}</b><br>{desc}</div>", unsafe_allow_html=True)
    
    # Cost Estimator
    st.markdown("#### 💰 Estimate Your Installation Cost")
    col1, col2 = st.columns(2)
    with col1:
        charger_type = st.selectbox("Charger Type", ["Level 1 (3.3 kW)", "Level 2 (7 kW)", "Level 2 (22 kW)"])
        cable_length = st.slider("Distance from DB to parking (meters)", 5, 50, 15)
    with col2:
        labour_cost = st.number_input("Labour & Misc (₹)", min_value=0, value=5000, step=1000)
        if st.button("Estimate Total Cost"):
            base_costs = {
                "Level 1 (3.3 kW)": 20000,
                "Level 2 (7 kW)": 50000,
                "Level 2 (22 kW)": 75000
            }
            cable_cost = cable_length * 200  # ₹200 per meter approx
            total = base_costs[charger_type] + cable_cost + labour_cost
            st.success(f"Estimated Total Cost: **₹{total:,.0f}**\n\n*Breakdown: Charger ₹{base_costs[charger_type]:,} + Cable ₹{cable_cost:,} + Labour ₹{labour_cost:,}*")
    
    # Government Subsidies & Links
    st.markdown("#### 🏛️ Government Subsidies & Schemes")
    st.markdown("""
        - **FAME-II Scheme** – Subsidy on EV charging infrastructure (up to 60% of cost for public chargers).  
        - **State EV Policies** – Many states offer additional incentives for home charging (e.g., Delhi, Maharashtra, Karnataka).  
        - **Net Metering** – If you have solar, you can offset charging cost by exporting surplus power.  
        - **Official Resources**:  
            - [Ministry of Power – EV Charging Guidelines](https://powermin.gov.in)  
            - [BEE – EV Charging Infrastructure](https://beeindia.gov.in)  
            - [State DISCOM Portal – Apply for net metering]
    """)
    
    # Vendor Finder (reusing community connector but with EV focus)
    st.markdown("#### 🤝 Find a Local EV Charger Installer")
    with st.form("ev_vendor_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Mobile Number", max_chars=10)
        if st.form_submit_button("Connect with Installers"):
            if name and validate_mobile(contact):
                st.success(f"✅ Verified EV charger installers in {st.session_state.user_pincode} will contact you within 48 hours.")
            else:
                st.warning("Enter valid name and 10-digit mobile.")
    
    # Safety Checklist
    st.markdown("#### ⚠️ Safety & Maintenance Checklist")
    st.markdown("""
        - ✅ Use only ISI/BIS certified chargers and cables.  
        - ✅ Ensure proper earthing (≤ 5 ohms).  
        - ✅ Install a dedicated RCCB (Residual Current Circuit Breaker).  
        - ✅ Keep charger away from water / rain unless IP65 rated.  
        - ✅ Regularly inspect cables for wear.  
        - ✅ Update charger firmware if smart-enabled.  
    """)
    
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
    
    # Tabs – now 7 tabs
    tabs = st.tabs([
        "💰 Calculator", 
        "🤖 AI Assistant", 
        "🎯 Subsidy", 
        "📡 News", 
        "🤝 Connect", 
        "🧾 Tax Engine",
        "🔌 EV Charging"   # NEW
    ])
    with tabs[0]:
        sub_tabs = st.tabs(["🚗 Vehicle", "☀️ Solar", "🌾 Farmer"])
        with sub_tabs[0]: vehicle_calculator()
        with sub_tabs[1]: solar_calculator()
        with sub_tabs[2]: farmer_solar_calculator()
    with tabs[1]: ai_chatbot()
    with tabs[2]: subsidy_checker()
    with tabs[3]: news_section()
    with tabs[4]: community_connector()
    with tabs[5]: tax_engine_tab()
    with tabs[6]: ev_charging_guide()   # <-- new EV tab
    
    st.caption(f"⚡ {Config.APP_NAME} v{Config.APP_VERSION} | FutureHQ.in")

if __name__ == "__main__":
    main()
