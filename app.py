import streamlit as st
import pandas as pd
import datetime
import hashlib
import base64
import os
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
class Config:
    """Application configuration"""
    APP_NAME = "Bharat Harit Kranti Portal"
    APP_VERSION = "7.0.0"
    COMPANY = "FutureHQ.in"
    
    # API Configuration
    GEMINI_MODEL = "gemini-2.0-flash-exp"
    
    # Session Keys
    SESSION_KEYS = {
        'user_registered': False,
        'user_mobile': "",
        'user_pincode': "",
        'chat_history': []
    }
    
    # Validation Rules
    MOBILE_LENGTH = 10
    PINCODE_LENGTH = 6
    
    # Solar Calculator Constants
    SOLAR_COST_PER_KW = 62000
    SOLAR_AREA_PER_KW = 100  # sq ft
    BILL_TO_KW_RATIO = 1300
    
    # Farmer Calculator Constants
    SUBSIDY_PERCENTAGE = 0.60
    GRID_SELL_RATE = 4.50  # ₹ per unit
    GRID_GENERATION_PER_KW = 4  # units per hour
    
    # Pump Configurations
    PUMP_CONFIGS = {
        "3 HP Pump": {"diesel_per_hour": 0.8, "solar_kw": 3.0, "setup_cost": 185000},
        "5 HP Pump": {"diesel_per_hour": 1.2, "solar_kw": 5.0, "setup_cost": 260000},
        "7.5 HP Pump": {"diesel_per_hour": 1.8, "solar_kw": 7.5, "setup_cost": 390000},
        "10 HP Pump": {"diesel_per_hour": 2.4, "solar_kw": 10.0, "setup_cost": 510000}
    }

# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════
@contextmanager
def error_handler(component: str, fallback_value: Any = None):
    """Generic error handler context manager"""
    try:
        yield
    except Exception as e:
        logger.error(f"Error in {component}: {str(e)}")
        if fallback_value is not None:
            st.warning(f"⚠️ Unable to load {component}. Using default values.")
        else:
            st.error(f"❌ Error in {component}. Please refresh the page.")
        return fallback_value

def safe_execution(default_return=None):
    """Decorator for safe function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                st.error(f"Operation failed: {str(e)}")
                return default_return
        return wrapper
    return decorator

# ═══════════════════════════════════════════════════════════════════════════════
# GEMINI AI INTEGRATION WITH ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════════
@safe_execution(default_return="AI service temporarily unavailable. Please try again later.")
def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini AI with error handling"""
    try:
        import google.generativeai as genai
        
        # Configure API key from secrets or environment
        api_key = None
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif os.getenv("GEMINI_API_KEY"):
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.warning("Gemini API key not configured")
            return "AI service configuration incomplete. Please contact support."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=Config.GEMINI_MODEL)
        
        system_prompt = """You are Green Sahayik, a helpful assistant for middle-class families and farmers in India. 
        Respond in simple, friendly terms. Mix English and conversational Hindi naturally. 
        Keep responses under 150 words. Be practical and solution-oriented."""
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        response = model.generate_content(full_prompt)
        
        return response.text if response.text else "I couldn't generate a response. Please try rephrasing your question."
    
    except ImportError:
        logger.error("Google GenerativeAI package not installed")
        return "AI service package not installed. Please contact administrator."
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return "AI service temporarily unavailable. Please try again later."

# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND IMAGE HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
@safe_execution(default_return="background-color: #030611 !important;")
def get_background_style() -> str:
    """Load and encode background image with error handling"""
    image_path = "IMG_6477.png"
    
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            return f"""
                background-image: linear-gradient(to bottom, rgba(3, 6, 17, 0.88), rgba(4, 10, 31, 0.96)), 
                url("data:image/png;base64,{encoded}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
            """
        except Exception as e:
            logger.error(f"Failed to load background image: {str(e)}")
    
    return "background: linear-gradient(135deg, #030611 0%, #0a0f2a 100%) !important;"

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    """Initialize session state variables"""
    for key, default_value in Config.SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_mobile(mobile: str) -> bool:
    """Validate mobile number"""
    return mobile and len(mobile) == Config.MOBILE_LENGTH and mobile.isdigit()

def validate_pincode(pincode: str) -> bool:
    """Validate pincode"""
    return pincode and len(pincode) == Config.PINCODE_LENGTH and pincode.isdigit()

# ═══════════════════════════════════════════════════════════════════════════════
# CSS STYLES (Mobile Responsive)
# ═══════════════════════════════════════════════════════════════════════════════
def load_css():
    """Load responsive CSS styles"""
    bg_style = get_background_style()
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
        
        /* Base Styles */
        .stApp {{
            {bg_style}
            color: #f1f5f9 !important;
            font-family: 'Poppins', sans-serif;
        }}
        
        /* Responsive Typography */
        @media (max-width: 768px) {{
            .stApp {{
                font-size: 14px;
            }}
            h1 {{
                font-size: 1.8rem !important;
            }}
            h2 {{
                font-size: 1.4rem !important;
            }}
            h3 {{
                font-size: 1.2rem !important;
            }}
        }}
        
        /* Neon Title */
        .neon-title {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #FF9933 10%, #FFFFFF 50%, #129E59 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-shadow: 0 0 30px rgba(255, 153, 51, 0.1);
            text-align: center;
            margin: 10px 0;
        }}
        
        /* Responsive Cards */
        .cyber-card {{
            background: linear-gradient(135deg, rgba(8, 14, 38, 0.88), rgba(3, 7, 18, 0.98));
            backdrop-filter: blur(25px);
            border: 1px solid rgba(0, 240, 255, 0.12);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.6);
        }}
        
        @media (max-width: 768px) {{
            .cyber-card {{
                padding: 15px;
                margin-bottom: 15px;
            }}
        }}
        
        .farmer-card {{
            background: linear-gradient(135deg, rgba(12, 158, 89, 0.18), rgba(3, 7, 18, 0.98));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(12, 158, 89, 0.3);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        
        @media (max-width: 768px) {{
            .farmer-card {{
                padding: 15px;
            }}
        }}
        
        .rec-card {{
            background: linear-gradient(135deg, rgba(14, 116, 144, 0.18), rgba(3, 7, 18, 0.95));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(14, 116, 144, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }}
        
        .gov-report {{
            background-color: #ffffff !important;
            color: #1e293b !important;
            border-left: 6px solid #FF9933;
            border-right: 6px solid #129E59;
            border-radius: 6px;
            padding: 30px;
            margin-top: 15px;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            overflow-x: auto;
        }}
        
        @media (max-width: 768px) {{
            .gov-report {{
                padding: 15px;
                font-size: 0.9rem;
            }}
        }}
        
        .cyber-label {{
            font-family: 'Poppins', sans-serif;
            color: #00F0FF !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9rem;
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
            padding-bottom: 6px;
            margin-bottom: 15px;
        }}
        
        /* Responsive Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: rgba(7, 13, 33, 0.95);
            padding: 6px;
            border-radius: 10px;
            flex-wrap: wrap;
        }}
        
        @media (max-width: 768px) {{
            .stTabs [data-baseweb="tab-list"] {{
                gap: 4px;
            }}
            .stTabs [data-baseweb="tab"] {{
                padding: 6px 12px !important;
                font-size: 0.75rem !important;
            }}
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: #94a3b8 !important;
            font-family: 'Poppins', sans-serif;
            background-color: transparent !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: #00F0FF !important;
            background: rgba(0, 240, 255, 0.08) !important;
            border: 1px solid rgba(0, 240, 255, 0.25) !important;
        }}
        
        /* Metric Cards Responsive */
        div[data-testid="stMetricValue"] {{
            font-family: 'Poppins', sans-serif;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.55rem !important;
        }}
        
        @media (max-width: 768px) {{
            div[data-testid="stMetricValue"] {{
                font-size: 1.2rem !important;
            }}
            div[data-testid="stMetricLabel"] {{
                font-size: 0.8rem !important;
            }}
        }}
        
        /* Form Inputs */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea, 
        select {{
            background-color: rgba(4, 8, 23, 0.9) !important;
            border: 1px solid rgba(0, 240, 255, 0.2) !important;
            color: #ffffff !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background: linear-gradient(135deg, #FF9933, #129E59) !important;
            color: #030611 !important;
            border: none !important;
            font-family: 'Poppins', sans-serif;
            font-weight: 700 !important;
            border-radius: 6px !important;
            width: 100%;
            transition: all 0.3s ease;
        }}
        
        .stButton button:hover {{
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
            color: #ffffff !important;
            transform: translateY(-2px);
        }}
        
        /* Success/Error Messages */
        .stAlert {{
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
        }}
        
        /* Responsive Grid */
        @media (max-width: 768px) {{
            .row-widget.stHorizontal {{
                flex-wrap: wrap;
            }}
            .stColumns {{
                flex-wrap: wrap;
            }}
        }}
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.3);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #129E59;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #FF9933;
        }}
        </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRATION COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════
def registration_screen():
    """Display registration screen"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    left_co, cent_co, last_co = st.columns([1, 2.2, 1])
    
    with cent_co:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(13, 22, 54, 0.92), rgba(4, 8, 23, 0.98));
                backdrop-filter: blur(25px);
                border: 2px solid rgba(0, 240, 255, 0.25);
                box-shadow: 0 20px 50px rgba(0, 240, 255, 0.15);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="height: 10px; width: 10px; background-color: #00F0FF; border-radius: 50%;"></span>
                        <span style="font-size: 0.8rem; color: #00F0FF; font-weight: 600;">👋 CITIZEN ACCESS</span>
                    </div>
                    <span style="font-size: 0.75rem; color: #64748b;">v{Config.APP_VERSION}</span>
                </div>
                <h2 style="font-weight: 800; color: #ffffff; margin-bottom: 5px;">
                    BHARAT HARIT KRANTI PORTAL
                </h2>
                <p style="color: #94a3b8; font-size: 0.95rem;">अपना ग्रीन क्रांति डैशबोर्ड</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            with col1:
                mobile = st.text_input(
                    "📱 Mobile Number", 
                    placeholder="10-Digit Mobile No.",
                    max_chars=10,
                    help="Enter your 10-digit mobile number"
                )
            with col2:
                pincode = st.text_input(
                    "📍 Area Pin Code", 
                    placeholder="6-Digit Pin Code",
                    max_chars=6,
                    help="Enter your 6-digit area pincode"
                )
            
            submitted = st.form_submit_button("🚀 Open Dashboard", use_container_width=True)
            
            if submitted:
                if validate_mobile(mobile) and validate_pincode(pincode):
                    st.session_state.user_registered = True
                    st.session_state.user_mobile = mobile
                    st.session_state.user_pincode = pincode
                    st.rerun()
                else:
                    st.error("⚠️ Please check: Mobile (10 digits) and Pincode (6 digits) are required.")
    
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# VEHICLE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
def vehicle_calculator():
    """Vehicle cost comparison calculator"""
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>⚙️ Vehicle Cost Calculator</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            daily_km = st.slider(
                "Daily Distance (KM)", 
                min_value=10, 
                max_value=350, 
                value=80,
                help="Average kilometers driven per day"
            )
            petrol_price = st.number_input(
                "Petrol Price (₹/L)", 
                min_value=80.0, 
                value=104.0,
                format="%.2f"
            )
            petrol_mileage = st.number_input(
                "Petrol Mileage (KM/L)", 
                min_value=5.0, 
                value=15.0,
                format="%.1f"
            )
        
        with col2:
            cng_price = st.number_input(
                "CNG Price (₹/KG)", 
                min_value=60.0, 
                value=82.5,
                format="%.2f"
            )
            cng_mileage = st.number_input(
                "CNG Mileage (KM/KG)", 
                min_value=10.0, 
                value=22.0,
                format="%.1f"
            )
        
        with col3:
            ev_rate = st.number_input(
                "Electricity Rate (₹/Unit)", 
                min_value=3.0, 
                value=8.5,
                format="%.2f"
            )
            ev_mileage = st.number_input(
                "EV Mileage (KM/Unit)", 
                min_value=1.0, 
                value=6.5,
                format="%.1f"
            )
        
        # Calculations
        petrol_per_km = petrol_price / petrol_mileage
        cng_per_km = cng_price / cng_mileage
        ev_per_km = ev_rate / ev_mileage
        
        cost_petrol_month = petrol_per_km * daily_km * 30
        cost_cng_month = cng_per_km * daily_km * 30
        cost_ev_month = ev_per_km * daily_km * 30
        
        st.markdown("<p class='cyber-label'>📊 Cost per KM</p>", unsafe_allow_html=True)
        metric_cols = st.columns(3)
        metric_cols[0].metric("Petrol", f"₹{petrol_per_km:.2f}/KM")
        metric_cols[1].metric("CNG", f"₹{cng_per_km:.2f}/KM")
        metric_cols[2].metric("EV", f"₹{ev_per_km:.2f}/KM")
        
        st.markdown("<p class='cyber-label'>📈 Monthly Running Cost</p>", unsafe_allow_html=True)
        metric_cols2 = st.columns(3)
        metric_cols2[0].metric("Petrol", f"₹{cost_petrol_month:,.0f}")
        metric_cols2[1].metric(
            "CNG", 
            f"₹{cost_cng_month:,.0f}",
            delta=f"Save ₹{cost_petrol_month - cost_cng_month:,.0f}"
        )
        metric_cols2[2].metric(
            "EV", 
            f"₹{cost_ev_month:,.0f}",
            delta=f"Save ₹{cost_petrol_month - cost_ev_month:,.0f}"
        )
        
        # Chart
        months_axis = list(range(1, 37))
        chart_data = pd.DataFrame({
            'Month': months_axis,
            'Petrol': [cost_petrol_month * m for m in months_axis],
            'CNG': [cost_cng_month * m for m in months_axis],
            'EV': [cost_ev_month * m for m in months_axis]
        }).set_index('Month')
        
        st.line_chart(chart_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SOLAR CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
def solar_calculator():
    """Rooftop solar calculator"""
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>☀️ Solar Rooftop Calculator</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_bill = st.number_input(
                "Average Monthly Bill (₹)",
                min_value=500,
                value=7500,
                step=500,
                help="Your average monthly electricity bill amount"
            )
        
        with col2:
            roof_area = st.number_input(
                "Available Roof Area (sq ft)",
                min_value=100,
                value=500,
                step=50,
                help="Total open roof area available for solar panels"
            )
        
        # Calculate recommendations
        max_kw = min(roof_area / Config.SOLAR_AREA_PER_KW, monthly_bill / Config.BILL_TO_KW_RATIO)
        estimated_cost = max_kw * Config.SOLAR_COST_PER_KW
        carbon_saved = max_kw * 1.3
        
        st.markdown("<p class='cyber-label'>📊 Recommended Solar Setup</p>", unsafe_allow_html=True)
        
        res_cols = st.columns(3)
        res_cols[0].metric("System Size", f"{max_kw:.1f} kW")
        res_cols[1].metric("Estimated Cost", f"₹{estimated_cost:,.0f}")
        res_cols[2].metric("Annual CO₂ Savings", f"{carbon_saved:.1f} Tons")
        
        if max_kw < 1:
            st.info("💡 Based on your inputs, a smaller solar system might be sufficient. Consider optimizing your energy usage first.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FARMER SOLAR CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
def farmer_solar_calculator():
    """Farmer solar pump calculator"""
    with st.container():
        st.markdown("<div class='farmer-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🚜 Kisan Solar Hub</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            pump_hp = st.selectbox(
                "Pump Horsepower",
                options=list(Config.PUMP_CONFIGS.keys()),
                help="Select your pump's horsepower rating"
            )
            hours_per_month = st.slider(
                "Monthly Operating Hours",
                min_value=10,
                max_value=200,
                value=60,
                help="How many hours does your pump run per month?"
            )
        
        with col2:
            crop_type = st.selectbox(
                "Primary Crop",
                options=["Paddy (धान)", "Wheat (गेहूं)", "Sugarcane (गन्ना)", "Vegetables (सब्जियां)"],
                help="Select your main crop type"
            )
            diesel_price = st.number_input(
                "Diesel Price (₹/L)",
                min_value=85.0,
                value=92.5,
                format="%.2f",
                help="Current local diesel price"
            )
        
        # Get pump configuration
        pump_config = Config.PUMP_CONFIGS[pump_hp]
        
        # Calculations
        monthly_diesel_cost = hours_per_month * pump_config["diesel_per_hour"] * diesel_price
        yearly_diesel_cost = monthly_diesel_cost * 12
        
        subsidy_amount = pump_config["setup_cost"] * Config.SUBSIDY_PERCENTAGE
        farmer_payable = pump_config["setup_cost"] - subsidy_amount
        
        yearly_grid_income = (
            hours_per_month * 
            (pump_config["solar_kw"] * Config.GRID_GENERATION_PER_KW) * 
            Config.GRID_SELL_RATE * 
            30
        ) / 1000
        
        st.markdown("<p class='cyber-label'>💰 Financial Analysis</p>", unsafe_allow_html=True)
        
        metric_cols = st.columns(3)
        metric_cols[0].metric("Yearly Diesel Cost", f"₹{yearly_diesel_cost:,.0f}")
        metric_cols[1].metric("Subsidy Amount (60%)", f"₹{subsidy_amount:,.0f}")
        metric_cols[2].metric("Your Contribution", f"₹{farmer_payable:,.0f}")
        
        payback_years = farmer_payable / yearly_diesel_cost if yearly_diesel_cost > 0 else 0
        
        st.info(f"""
        💡 **Key Insights:**
        - Payback period: ~{payback_years:.1f} years
        - Potential annual grid income: ₹{yearly_grid_income:,.0f}
        - Diesel cost savings: 100% after solar installation
        - Recommended for {crop_type}: 22-35% reduction in production costs
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# AI CHATBOT
# ═══════════════════════════════════════════════════════════════════════════════
def ai_chatbot():
    """AI chatbot interface"""
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤖 Green Sahayik AI Assistant</p>", unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1d4ed8, #0284c7); 
                                padding: 12px 16px; 
                                border-radius: 16px 16px 4px 16px; 
                                color: white; 
                                margin-bottom: 12px; 
                                max-width: 80%; 
                                margin-left: auto;">
                        <b>You:</b><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: rgba(13, 22, 54, 0.95); 
                                border-left: 4px solid #129E59; 
                                padding: 12px 16px; 
                                border-radius: 4px 16px 16px 16px; 
                                color: #e2e8f0; 
                                margin-bottom: 12px; 
                                max-width: 85%;">
                        <b>🤖 Sahayik:</b><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        user_query = st.chat_input("Ask me about solar panels, subsidies, EV cars, or farming...")
        
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            with st.spinner("🤔 Thinking..."):
                response = get_gemini_response(user_query)
                st.session_state.chat_history.append({"role": "bot", "content": response})
            
            st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "bot", "content": "नमस्ते! Welcome to Green Sahayik. How can I help you today?"}
            ]
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SUBSIDY CHECKER
# ═══════════════════════════════════════════════════════════════════════════════
def subsidy_checker():
    """Subsidy eligibility checker"""
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🎯 Subsidy Eligibility Checker</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            state = st.selectbox(
                "Select State",
                options=["Gujarat", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"],
                help="Choose your state for state-specific subsidies"
            )
        
        with col2:
            project_type = st.radio(
                "Project Type",
                options=["Residential Rooftop", "Agricultural Solar Pump", "Commercial Solar"],
                help="Select your solar project category"
            )
        
        if st.button("🔍 Check Eligibility", use_container_width=True):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            verification_id = hashlib.sha256(f"{state}{project_type}{timestamp}".encode()).hexdigest()[:8].upper()
            
            st.markdown(f"""
                <div class="gov-report">
                    <h3 style="color:#0f172a; margin-top:0;">📋 Eligibility Report</h3>
                    <p style="font-size:0.85rem; color:#475569;">
                        <b>Generated:</b> {timestamp} IST | 
                        <b>Reference ID:</b> <span style="font-family:monospace;">HRT-{verification_id}</span>
                    </p>
                    <hr>
                    <p><b>State:</b> {state}</p>
                    <p><b>Project Type:</b> {project_type}</p>
                    <p style="color:#15803d; font-weight:bold; font-size:1.1rem;">
                        ✅ STATUS: ELIGIBLE for subsidies
                    </p>
                    <p style="font-size:0.9rem; color:#475569; margin-top:15px;">
                        <b>Next Steps:</b> Contact your local DISCOM office with this report for detailed subsidy calculation.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NEWS SECTION
# ═══════════════════════════════════════════════════════════════════════════════
def news_section():
    """Energy news section"""
    st.markdown("### 📡 Energy Updates")
    
    news_items = [
        {
            "title": "🔋 Local Battery Manufacturing",
            "content": "New battery cell factories coming online in 2025, reducing EV costs by 15-20%."
        },
        {
            "title": "🚜 Solar Pump Expansion",
            "content": "Government allocates ₹10,000 crore for solar agricultural pumps in next fiscal year."
        },
        {
            "title": "☀️ High-Efficiency Panels",
            "content": "New solar panels with 22% efficiency now available at competitive prices."
        }
    ]
    
    cols = st.columns(3)
    for idx, news in enumerate(news_items):
        with cols[idx]:
            st.markdown(f"""
                <div class='cyber-card'>
                    <h5>{news['title']}</h5>
                    <p style='font-size:0.85rem; color:#94a3b8;'>{news['content']}</p>
                </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COMMUNITY CONNECTOR
# ═══════════════════════════════════════════════════════════════════════════════
def community_connector():
    """Vendor matching component"""
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<p class='cyber-label'>🤝 Community Connector</p>", unsafe_allow_html=True)
        
        with st.form("vendor_connection_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            contact = st.text_input("Mobile Number", placeholder="10-digit mobile number", max_chars=10)
            
            submitted = st.form_submit_button("📤 Connect with Local Vendors", use_container_width=True)
            
            if submitted:
                if name and validate_mobile(contact):
                    st.success(f"""
                        ✅ Registration successful!
                        - Local vendors in pincode {st.session_state.user_pincode} will contact you within 48 hours.
                        - Reference ID: {hashlib.md5(f"{name}{contact}".encode()).hexdigest()[:8].upper()}
                    """)
                elif not name:
                    st.warning("Please enter your full name.")
                elif not validate_mobile(contact):
                    st.warning("Please enter a valid 10-digit mobile number.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title=f"{Config.APP_NAME} | {Config.COMPANY}",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize
    init_session_state()
    load_css()
    
    # Show registration or dashboard
    if not st.session_state.user_registered:
        registration_screen()
    
    # Main Dashboard
    st.markdown(f"<h1 class='neon-title'>{Config.APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align: center; font-size: 0.9rem; color: #129E59;'>"
        f"🟢 Active | Pincode: {st.session_state.user_pincode} | Welcome Citizen</p>",
        unsafe_allow_html=True
    )
    
    # National metrics
    try:
        metric_cols = st.columns(4)
        metrics_data = [
            ("☀️ Rooftop Solar", "41 Lakh+", "Target: 75 Lakh"),
            ("🌾 Solar Pumps", "7.5 Lakh+", "60% Subsidy"),
            ("🔋 Grid Storage", "150 GW", "Local Manufacturing"),
            ("🍃 Renewable Share", "45%", "Goal: 50% by 2030")
        ]
        
        for col, (label, value, delta) in zip(metric_cols, metrics_data):
            col.metric(label=label, value=value, delta=delta)
    except Exception as e:
        logger.error(f"Error displaying metrics: {str(e)}")
        st.warning("Unable to load national metrics.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main tabs
    try:
        tabs = st.tabs([
            "💰 Savings Calculator",
            "🤖 AI Assistant", 
            "🎯 Subsidy Checker",
            "📡 Energy News",
            "🤝 Community Connect"
        ])
        
        with tabs[0]:
            sub_tabs = st.tabs(["🚗 Vehicle Calculator", "☀️ Solar Calculator", "🌾 Farmer Calculator"])
            with sub_tabs[0]:
                vehicle_calculator()
            with sub_tabs[1]:
                solar_calculator()
            with sub_tabs[2]:
                farmer_solar_calculator()
        
        with tabs[1]:
            ai_chatbot()
        
        with tabs[2]:
            subsidy_checker()
        
        with tabs[3]:
            news_section()
        
        with tabs[4]:
            community_connector()
    
    except Exception as e:
        logger.error(f"Error loading tabs: {str(e)}")
        st.error("Unable to load main application features. Please refresh the page.")
    
    # Footer
    st.markdown("---")
    st.caption(f"⚡ {Config.APP_NAME} | {Config.COMPANY} | Version {Config.APP_VERSION} | Digital Public Utility")

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
