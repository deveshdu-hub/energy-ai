import google.generativeai as genai

# Securely configure the free Gemini API using Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")

def get_ai_response(user_input, system_prompt):
    try:
        # Utilizing gemini-1.5-flash for lightning-fast, free execution
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error connecting to AI backend: {str(e)}"
