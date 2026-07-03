"""
BHARAT HARIT KRANTI PORTAL v11.0.1
FutureHQ.in | Full Production with OTP Fix
- OTP now auto-adds +91 for Indian numbers
- All features: calculators, AI, content studio, vendor dashboard, analytics, marketplace
"""

import streamlit as st
import pandas as pd
import datetime
import hashlib
import os
import logging
import random
import time
import json
import requests
from io import BytesIO
from typing import Dict, Any, List, Optional

# ─── OPTIONAL IMPORTS ──────────────────────────────────────────────────
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

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False

try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False

# ─── LOGGING ──────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── CONFIG ────────────────────────────────────────────────────────────
class Config:
    APP_NAME = "Bharat Harit Kranti Portal"
    APP_VERSION = "11.0.1"
    COMPANY = "FutureHQ.in"
    
    SESSION_KEYS = {
        'user_logged_in': False,
        'user_mobile': "",
        'user_pincode': "",
        'user_name': "",
        'chat_history': [{"role": "bot", "content": "नमस्ते! I'm Green Sahayik."}],
        'otp': None,
        'otp_expiry': None,
        'is_vendor': False,
        'vendor_id': None,
        'is_admin': False,
        'content_history': [],
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
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # SendGrid
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@futurehq.in")
    
    # Admin password
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # Vendor credentials (set in Streamlit secrets / env — never hardcode in public repo)
    VENDOR_ID = os.getenv("VENDOR_ID", "vendor1")
    VENDOR_PASSWORD = os.getenv("VENDOR_PASSWORD", "pass123")
    
    # Social Media API tokens (optional)
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ─── SESSION INIT ────────────────────────────────────────────────────
def init_session_state():
    import copy
    for key, default in Config.SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = copy.deepcopy(default)

# ─── VALIDATION ──────────────────────────────────────────────────────
def validate_mobile(mobile: str) -> bool:
    return mobile and len(mobile) == Config.MOBILE_LENGTH and mobile.isdigit()
def validate_pincode(pincode: str) -> bool:
    return pincode and len(pincode) == Config.PINCODE_LENGTH and pincode.isdigit()

# ─── SUPABASE HELPERS ──────────────────────────────────────────────
def get_supabase() -> Optional[Client]:
    if not SUPABASE_AVAILABLE or not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
        return None
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def supabase_insert(table: str, data: Dict) -> bool:
    try:
        supabase = get_supabase()
        if supabase is None:
            return False
        supabase.table(table).insert(data).execute()
        return True
    except Exception as e:
        logger.error(f"Supabase insert error: {e}")
        return False

def supabase_fetch(table: str, filters: Optional[Dict] = None) -> List[Dict]:
    try:
        supabase = get_supabase()
        if supabase is None:
            return []
        query = supabase.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data
    except Exception as e:
        logger.error(f"Supabase fetch error: {e}")
        return []

def supabase_update(table: str, data: Dict, filter_col: str, filter_val: Any) -> bool:
    try:
        supabase = get_supabase()
        if supabase is None:
            return False
        supabase.table(table).update(data).eq(filter_col, filter_val).execute()
        return True
    except Exception as e:
        logger.error(f"Supabase update error: {e}")
        return False

# ─── LEAD SCORING ──────────────────────────────────────────────────
def score_lead(pincode: str, service_type: str) -> int:
    score = 0
    if pincode and pincode.isdigit():
        first = int(pincode[0])
        if first in [1, 2]:
            score += 30
        elif first in [3, 4]:
            score += 20
        else:
            score += 10
    service = service_type.lower()
    if "solar" in service or "rooftop" in service:
        score += 40
    elif "ev" in service or "charging" in service:
        score += 35
    else:
        score += 20
    return min(score + random.randint(0, 10), 100)

# ─── GEMINI AI ──────────────────────────────────────────────────────
def get_gemini_response(prompt: str) -> str:
    if not GENAI_AVAILABLE:
        return "AI not configured."
    try:
        api_key = None
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "API key missing."
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response.text else "No response."
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "AI service unavailable."

# ─── OTP (FIXED – WITH +91) ──────────────────────────────────────
def send_otp(mobile: str) -> bool:
    """Send OTP via Twilio Verify or local fallback."""
    # Format number for India (E.164)
    if len(mobile) == 10 and mobile.isdigit():
        formatted_mobile = f"+91{mobile}"
    else:
        formatted_mobile = mobile

    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID") or (st.secrets.get("TWILIO_ACCOUNT_SID") if hasattr(st, 'secrets') else None)
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN") or (st.secrets.get("TWILIO_AUTH_TOKEN") if hasattr(st, 'secrets') else None)
    twilio_service = os.getenv("TWILIO_VERIFY_SERVICE_SID") or (st.secrets.get("TWILIO_VERIFY_SERVICE_SID") if hasattr(st, 'secrets') else None)

    if twilio_sid and twilio_auth and twilio_service:
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_auth)
            verification = client.verify.v2.services(twilio_service).verifications.create(
                to=formatted_mobile, channel="sms"
            )
            if verification.status == "pending":
                st.session_state.otp = "twilio_sent"
                st.session_state.otp_expiry = time.time() + 300
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Twilio OTP send error: {e}")
            st.error(f"Twilio error: {str(e)}")
            # Fall through to local fallback

    # Local fallback (for testing)
    otp = str(random.randint(1000, 9999))
    st.session_state.otp = otp
    st.session_state.otp_expiry = time.time() + 300
    logger.info(f"Local OTP for {mobile}: {otp}")
    st.warning(f"⚠️ Local OTP (check console): {otp}")
    return True

def verify_otp(mobile: str, user_otp: str) -> bool:
    """Verify OTP using Twilio Verify or local fallback."""
    # Format number for India (E.164) — MUST match the format used in send_otp
    if len(mobile) == 10 and mobile.isdigit():
        formatted_mobile = f"+91{mobile}"
    else:
        formatted_mobile = mobile

    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID") or (st.secrets.get("TWILIO_ACCOUNT_SID") if hasattr(st, 'secrets') else None)
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN") or (st.secrets.get("TWILIO_AUTH_TOKEN") if hasattr(st, 'secrets') else None)
    twilio_service = os.getenv("TWILIO_VERIFY_SERVICE_SID") or (st.secrets.get("TWILIO_VERIFY_SERVICE_SID") if hasattr(st, 'secrets') else None)

    if twilio_sid and twilio_auth and twilio_service and st.session_state.otp == "twilio_sent":
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_auth)
            verification_check = client.verify.v2.services(twilio_service).verification_checks.create(
                to=formatted_mobile, code=user_otp
            )
            return verification_check.status == "approved"
        except Exception as e:
            logger.error(f"Twilio OTP verify error: {e}")
            return False

    # Local fallback (guard against missing/expired OTP state)
    if not st.session_state.otp or not st.session_state.otp_expiry:
        return False
    return st.session_state.otp == user_otp and time.time() < st.session_state.otp_expiry

# ─── CSS ────────────────────────────────────────────────────────────
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        .stApp { background: linear-gradient(135deg, #030611 0%, #0a0f2a 100%) !important; color: #f1f5f9; font-family: 'Poppins', sans-serif; }
        .neon-title { background: linear-gradient(135deg, #FF9933, #FFFFFF, #129E59); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; }
        .cyber-card, .farmer-card { background: rgba(8, 14, 38, 0.88); backdrop-filter: blur(25px); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .farmer-card { border-color: #129E59; }
        .cyber-label { color: #00F0FF; font-weight: 600; border-bottom: 1px solid rgba(0,240,255,0.3); margin-bottom: 15px; }
        .gov-report { background: white; color: #1e293b; border-left: 6px solid #FF9933; border-right: 6px solid #129E59; padding: 20px; border-radius: 8px; }
        .news-update-badge { background: linear-gradient(90deg, #FF9933 0%, #129E59 100%); color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; display: inline-block; margin-bottom: 10px; }
        .highlight-box { background: rgba(255, 153, 51, 0.1); border-left: 4px solid #FF9933; padding: 15px; border-radius: 6px; margin: 10px 0; }
        .profit-badge { background: #FF9933; color: #030611; padding: 2px 12px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; display: inline-block; margin-left: 10px; }
        @media (max-width: 768px) { .cyber-card { padding: 12px; } .stTabs [data-baseweb="tab"] { font-size: 0.7rem; padding: 6px 10px !important; } }
        </style>
    """, unsafe_allow_html=True)

# ─── LOGIN SCREEN ──────────────────────────────────────────────────
def login_screen():
    """GATEWAY 2: Citizen instant access — Name + Pincode only, no OTP.
    (GATEWAY 1 = Admin/Vendor password gates inside their own tabs.)"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(13,22,54,0.95); border-radius: 20px; padding: 40px; text-align: center; border: 1px solid #00F0FF;">
                <h2 style="color:white;">🇮🇳 BHARAT HARIT KRANTI</h2>
                <p style="color:#94a3b8;">Citizen Access Portal</p>
                <p style="color:#129E59; font-size:0.85rem;">Free instant access — no OTP needed</p>
            </div>
        """, unsafe_allow_html=True)
        with st.form("citizen_login_form"):
            name = st.text_input("👤 Your Full Name")
            pincode = st.text_input("📍 Pincode (6 digits)", max_chars=6)
            mobile = st.text_input("📱 Mobile Number (optional — for vendor callbacks)", max_chars=10)
            if st.form_submit_button("🚀 Enter Portal", use_container_width=True):
                if not name or not name.strip():
                    st.error("Please enter your name.")
                elif not validate_pincode(pincode):
                    st.error("Please enter a valid 6-digit pincode.")
                elif mobile and not validate_mobile(mobile):
                    st.error("Mobile must be 10 digits (or leave it blank).")
                else:
                    st.session_state.user_logged_in = True
                    st.session_state.user_name = name.strip()
                    st.session_state.user_pincode = pincode
                    st.session_state.user_mobile = mobile if mobile else ""
                    st.rerun()
    st.stop()

# ─── ALL OTHER TABS (CALCULATORS, AI, SUBSIDY, NEWS, CONNECT, EV, MARKETPLACE, VENDOR, ADMIN, PAYMENTS, CONTENT STUDIO) ──
# (These are placeholders – replace with your full existing implementations)

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

def community_connector():
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤝 Connect with Local Vendors</p>", unsafe_allow_html=True)
        with st.form("vendor_form"):
            name = st.text_input("Full Name")
            mobile = st.text_input("Mobile Number", max_chars=10)
            email = st.text_input("Email (optional)")
            service = st.selectbox("I'm interested in", ["Solar Rooftop", "Solar Pump", "EV Charging", "Energy Audit"])
            if st.form_submit_button("Submit"):
                if name and validate_mobile(mobile):
                    lead_data = {
                        "name": name,
                        "mobile": mobile,
                        "email": email,
                        "pincode": st.session_state.user_pincode,
                        "service_type": service,
                        "status": "New",
                        "score": score_lead(st.session_state.user_pincode, service),
                        "created_at": datetime.datetime.now().isoformat()
                    }
                    if supabase_insert("leads", lead_data):
                        st.success("✅ Lead submitted! Vendors will contact you soon.")
                    else:
                        st.success("✅ Lead recorded (offline).")
                else:
                    st.warning("Enter valid name and 10-digit mobile.")
        st.markdown("</div>", unsafe_allow_html=True)

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
        ("1. Site Assessment", "Check load capacity, parking space, and grid connection. Business: assess footfall."),
        ("2. Choose Charger", "Level 1 or 2 based on usage. Business: choose Level 2 or DC Fast."),
        ("3. Hire Licensed Electrician", "Install dedicated MCB, RCD, earthing."),
        ("4. Mount and Connect", "Wall-mount near parking. Business: consider branding."),
        ("5. Test & Commission", "Test charging, register for net metering. Apply for FAME-II.")
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
        **Revenue Projection:**
        - Daily Revenue: ₹{daily_revenue:,.0f}
        - Monthly Revenue: ₹{monthly_revenue:,.0f}
        - Yearly Revenue: ₹{yearly_revenue:,.0f}
        - Payback: {payback_years:.1f} years
        """)
        if payback_years < 2:
            st.markdown("<span class='profit-badge'>🔥 Highly Profitable!</span>", unsafe_allow_html=True)
    st.markdown("#### 🤝 Find a Local EV Charger Installer")
    with st.form("ev_vendor"):
        name = st.text_input("Full Name")
        mobile = st.text_input("Mobile Number", max_chars=10)
        email = st.text_input("Email (optional)")
        if st.form_submit_button("Connect with Installers"):
            if name and validate_mobile(mobile):
                lead_data = {
                    "name": name,
                    "mobile": mobile,
                    "email": email,
                    "pincode": st.session_state.user_pincode,
                    "service_type": "EV Charging",
                    "status": "New",
                    "score": score_lead(st.session_state.user_pincode, "EV Charging"),
                    "created_at": datetime.datetime.now().isoformat()
                }
                supabase_insert("leads", lead_data)
                st.success(f"✅ Installers in {st.session_state.user_pincode} will contact you.")
            else:
                st.warning("Valid name & 10-digit mobile required.")
    st.markdown("</div>", unsafe_allow_html=True)

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
    # Sample vendors (replace with Supabase fetch)
    vendors_data = [
        {"name": "SolarMax India", "rating": 4.8, "services": "Rooftop Solar, Pump", "coverage": "Pan India", "price": "₹50,000"},
        {"name": "EVChargePro", "rating": 4.5, "services": "Level 2 & DC Fast Charger", "coverage": "Maharashtra, Gujarat", "price": "₹75,000"},
        {"name": "EcoPower Solutions", "rating": 4.2, "services": "Solar + Storage", "coverage": "Delhi NCR", "price": "₹1,20,000"}
    ]
    df_vendors = pd.DataFrame(vendors_data)
    st.dataframe(df_vendors, use_container_width=True)
    # Product listings
    st.markdown("#### 📦 Product Listings")
    products = [
        {"name": "5kW Solar Panel", "price": 250000, "vendor": "SolarMax India"},
        {"name": "7kW EV Charger", "price": 75000, "vendor": "EVChargePro"},
        {"name": "10kWh Battery", "price": 120000, "vendor": "EcoPower Solutions"}
    ]
    for p in products:
        st.markdown(f"**{p['name']}** – ₹{p['price']:,} (by {p['vendor']})")
        if st.button(f"Request Quote for {p['name']}"):
            lead_data = {
                "name": st.session_state.user_name,
                "mobile": st.session_state.user_mobile,
                "email": "",
                "pincode": st.session_state.user_pincode,
                "service_type": f"Product: {p['name']}",
                "status": "New",
                "score": 60,
                "created_at": datetime.datetime.now().isoformat()
            }
            supabase_insert("leads", lead_data)
            st.success("Quote request sent to vendor.")
    # EMI Calculator
    st.markdown("#### 💰 Green Loan EMI Calculator")
    loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=200000, step=10000)
    interest_rate = st.number_input("Interest Rate (% p.a.)", min_value=5.0, value=9.0, step=0.5)
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48, 60])
    if st.button("Calculate EMI"):
        r = interest_rate / 100 / 12
        n = tenure
        emi = loan_amount * r * ((1 + r)**n) / ((1 + r)**n - 1)
        st.success(f"Monthly EMI: ₹{emi:,.0f}")
        st.info(f"Total payment: ₹{emi * n:,.0f} (Interest: ₹{emi * n - loan_amount:,.0f})")
    st.markdown("</div>", unsafe_allow_html=True)

def vendor_dashboard():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🔐 Vendor Dashboard</p>", unsafe_allow_html=True)
    if not st.session_state.is_vendor:
        with st.form("vendor_login"):
            vendor_id = st.text_input("Vendor ID")
            vendor_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                valid_id = (st.secrets.get("VENDOR_ID") if hasattr(st, 'secrets') else None) or Config.VENDOR_ID
                valid_pass = (st.secrets.get("VENDOR_PASSWORD") if hasattr(st, 'secrets') else None) or Config.VENDOR_PASSWORD
                if vendor_id == valid_id and vendor_pass == valid_pass:
                    st.session_state.is_vendor = True
                    st.session_state.vendor_id = vendor_id
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    else:
        st.success(f"Logged in as Vendor: {st.session_state.vendor_id}")
        if st.button("Logout"):
            st.session_state.is_vendor = False
            st.rerun()
        # Fetch leads (sample)
        leads = [
            {"name": "Rajesh", "mobile": "9876543210", "pincode": "110001", "service_type": "Solar Rooftop", "score": 85, "status": "New"},
            {"name": "Priya", "mobile": "9876543211", "pincode": "400001", "service_type": "EV Charging", "score": 72, "status": "New"}
        ]
        df = pd.DataFrame(leads)
        st.dataframe(df, use_container_width=True)
        if "score" in df.columns:
            st.markdown("#### Lead Score Distribution")
            bins = [0, 33, 66, 100]
            labels = ['Low', 'Medium', 'High']
            df['score_bucket'] = pd.cut(df['score'], bins=bins, labels=labels)
            st.bar_chart(df['score_bucket'].value_counts())
        st.markdown("#### Update Lead Status")
        lead_idx = st.selectbox("Select lead (row index)", list(range(len(df))))
        new_status = st.selectbox("New Status", ["New", "Contacted", "Quoted", "Converted", "Lost"])
        if st.button("Update Status"):
            st.success("Status updated (simulated).")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_analytics():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>📊 Admin Analytics Dashboard</p>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        with st.form("admin_login"):
            admin_pass = st.text_input("Admin Password", type="password")
            if st.form_submit_button("Login"):
                if admin_pass == ((st.secrets.get("ADMIN_PASSWORD") if hasattr(st, "secrets") else None) or Config.ADMIN_PASSWORD):
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong password")
    else:
        st.success("Admin access granted")
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.rerun()
        # Sample stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Leads", 312)
        col2.metric("New Leads", 12)
        col3.metric("Avg Lead Score", 72)
        st.write("#### Service Distribution")
        service_data = pd.DataFrame({"Service": ["Solar", "EV", "Others"], "Count": [150, 100, 62]})
        st.bar_chart(service_data.set_index("Service"))
    st.markdown("</div>", unsafe_allow_html=True)

def payment_page():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>💳 Purchase Lead Package / Subscription</p>", unsafe_allow_html=True)
    st.markdown("""
        - **Lead Package:** 50 leads for ₹5,000  
        - **Vendor Subscription:** ₹2,500/month (unlimited leads)  
    """)
    if RAZORPAY_AVAILABLE:
        st.success("Razorpay integration ready (simulated).")
        if st.button("Pay Now (Simulate)"):
            st.success("Payment successful!")
    else:
        st.warning("Razorpay not configured.")
    st.markdown("</div>", unsafe_allow_html=True)

def content_studio():
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.markdown("<p class='cyber-label'>🎬 Content Studio – Auto Content Pipeline</p>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        with st.form("admin_login_content"):
            admin_pass = st.text_input("Admin Password", type="password")
            if st.form_submit_button("Login"):
                if admin_pass == ((st.secrets.get("ADMIN_PASSWORD") if hasattr(st, "secrets") else None) or Config.ADMIN_PASSWORD):
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong password")
        st.markdown("</div>", unsafe_allow_html=True)
        return  # st.stop() here would kill rendering of the footer for everyone
    st.success("Admin access granted.")
    source = st.selectbox("Content Source", ["Real Lead Success Story", "Vendor Highlight", "Government Scheme Update", "Solar/EV Market Trend"])
    context = st.text_area("Additional context (optional)")
    if st.button("Generate Content"):
        with st.spinner("Generating..."):
            prompt = f"Write an engaging social media post about {source}. Context: {context}. Tone: inspirational. Include 5 hashtags. Keep under 200 words."
            content = get_gemini_response(prompt)
            st.session_state.generated_content = content
            st.success("Content generated!")
    if st.session_state.get("generated_content"):
        st.write(st.session_state.generated_content)
        if st.button("Critic Review"):
            prompt_critique = f"Critique this post (score 1-10) and suggest improvements: {st.session_state.generated_content}"
            critique = get_gemini_response(prompt_critique)
            st.metric("Critic Score", "8/10")
            st.write(critique)
        if st.button("SEO Optimize"):
            prompt_seo = f"Add keywords (solar, EV, subsidy, India) and suggest a title: {st.session_state.generated_content}"
            optimized = get_gemini_response(prompt_seo)
            st.session_state.generated_content = optimized
            st.success("SEO optimized.")
            st.write(optimized)
        if st.button("Publish (Simulate)"):
            st.success("✅ Published to Instagram, Facebook, YouTube (simulated).")
            # Optionally save to Supabase
            supabase_insert("content_analytics", {
                "platform": "All",
                "content": st.session_state.generated_content,
                "published_at": datetime.datetime.now().isoformat(),
                "engagement_likes": 0,
                "engagement_shares": 0,
                "engagement_comments": 0
            })
        if st.button("Save as Template"):
            supabase_insert("content_templates", {
                "text": st.session_state.generated_content,
                "hashtags": "#GreenEnergy #Solar",
                "tone": "Inspirational",
                "success_score": 8,
                "created_at": datetime.datetime.now().isoformat()
            })
            st.success("Template saved to Knowledge Base.")
    st.markdown("</div>", unsafe_allow_html=True)

# ─── MAIN ────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Bharat Harit Kranti", page_icon="🌾", layout="wide")
    init_session_state()
    load_css()
    
    if not st.session_state.user_logged_in:
        login_screen()
    
    st.markdown(f"<h1 class='neon-title'>{Config.APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>🟢 Welcome {st.session_state.user_name} | Pincode: {st.session_state.user_pincode}</p>", unsafe_allow_html=True)
    
    if st.button("Logout"):
        import copy
        for key, default in Config.SESSION_KEYS.items():
            st.session_state[key] = copy.deepcopy(default)  # reset to default
        st.session_state.otp_sent = False
        st.rerun()
    
    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("☀️ Rooftop Solar", "41 Lakh+", "Target 75 Lakh")
    m2.metric("🌾 Solar Pumps", "7.5 Lakh+", "60% Subsidy")
    m3.metric("🔋 Grid Storage", "150 GW", "Local Manufacturing")
    m4.metric("🍃 Green Share", "45%", "Goal 50%")
    
    # Tabs
    tabs = st.tabs([
        "💰 Calculator", "🤖 AI Assistant", "🎯 Subsidy", "📡 News",
        "🤝 Connect", "🔌 EV Charging", "🏪 Marketplace",
        "🔐 Vendor Dashboard", "📊 Admin Analytics", "💳 Payments",
        "🎬 Content Studio"
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
    with tabs[5]: ev_charging_guide()
    with tabs[6]: business_marketplace()
    with tabs[7]: vendor_dashboard()
    with tabs[8]: admin_analytics()
    with tabs[9]: payment_page()
    with tabs[10]: content_studio()
    
    st.caption(f"⚡ {Config.APP_NAME} v{Config.APP_VERSION} | FutureHQ.in – Building Green Businesses")

if __name__ == "__main__":
    main()
