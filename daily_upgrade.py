#!/usr/bin/env python3
"""
Daily auto-upgrade for Bharat Harit Kranti Portal
Runs at 5 PM every day, generates a small enhancement.
"""

import os
import sys
import subprocess
from datetime import datetime
import google.generativeai as genai

# ---------- CONFIG ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # or st.secrets
APP_FILE = "app.py"
LOG_FILE = "upgrade_log.txt"
# ---------------------------

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)

def get_upgrade_prompt():
    """Return the daily prompt that asks Gemini for a small, safe upgrade."""
    return f"""
You are an expert Python/Streamlit developer. Today is {datetime.now().strftime('%Y-%m-%d')}.

I have a Streamlit app called "Bharat Harit Kranti Portal" (app.py).  
It already works perfectly. Your task: suggest **one small, incremental improvement** that makes the app better without breaking anything.

Rules:
- Only change one function or add one small feature (max 20 lines).
- Do NOT change any existing logic – only add or improve UI/UX.
- Focus on: better mobile responsiveness, new stat card, improved tooltip, cache optimization, or a tiny new filter.
- Output **only valid Python code** inside triple backticks.
- Include a comment at the top of the code block explaining what you improved.
- If you cannot think of anything safe, say "NO_UPDATE_TODAY".

Current app features: solar calculator, EV calculator, farmer pump subsidy, AI chatbot, PM Surya Ghar news.
Example improvements:
- Add a "Last updated" timestamp on the dashboard.
- Cache the news section with @st.cache_data.
- Add a progress bar when loading AI response.
- Show a toast notification on form submit.
- Add an export button for calculator results.
"""

def generate_upgrade():
    """Ask Gemini for a code upgrade."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(get_upgrade_prompt())
    return response.text

def extract_code(gemini_output):
    """Extract Python code from triple backticks."""
    if "NO_UPDATE_TODAY" in gemini_output:
        return None
    import re
    code_blocks = re.findall(r"```python\n(.*?)```", gemini_output, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r"```\n(.*?)```", gemini_output, re.DOTALL)
    return code_blocks[0] if code_blocks else None

def apply_upgrade(new_code_snippet):
    """Append or insert the upgrade safely into app.py."""
    with open(APP_FILE, "r") as f:
        original = f.read()
    
    # Backup
    with open(f"{APP_FILE}.backup", "w") as f:
        f.write(original)
    
    # Look for a marker comment to insert before (you can add "# AUTO-UPGRADE-AREA" in your app.py)
    marker = "# AUTO-UPGRADE-AREA"
    if marker in original:
        # Insert after marker
        parts = original.split(marker)
        new_content = parts[0] + marker + "\n" + new_code_snippet + "\n" + parts[1]
    else:
        # Append near the end, before final "if __name__"
        if "if __name__ == \"__main__\":" in original:
            new_content = original.replace(
                "if __name__ == \"__main__\":",
                new_code_snippet + "\n\nif __name__ == \"__main__\":"
            )
        else:
            new_content = original + "\n\n" + new_code_snippet
    
    with open(APP_FILE, "w") as f:
        f.write(new_content)
    log("Upgrade applied successfully.")

def git_commit_and_push():
    """Commit and push changes to GitHub (so Streamlit Cloud redeploys)."""
    try:
        subprocess.run(["git", "add", APP_FILE], check=True)
        subprocess.run(["git", "commit", "-m", f"Daily auto-upgrade {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        log("Git commit & push successful.")
    except Exception as e:
        log(f"Git error: {e}")

def main():
    log("=== Daily upgrade started ===")
    if not GEMINI_API_KEY:
        log("No Gemini API key – skipping upgrade.")
        return
    
    raw = generate_upgrade()
    code = extract_code(raw)
    if code is None:
        log("Gemini suggested no upgrade today.")
        return
    
    log("Received upgrade code. Applying...")
    apply_upgrade(code)
    git_commit_and_push()
    log("=== Daily upgrade finished ===")

if __name__ == "__main__":
    main()
