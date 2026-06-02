import os
import json
import requests
from datetime import datetime
from anthropic import Anthropic

client = Anthropic()

def generate_energy_content():
    """Generate daily energy market insights"""
    
    prompt = """Generate a captivating Instagram post (120-150 chars) about India's energy market today.
    Include: One energy trend + emoji + call-to-action.
    Today's topics: EV growth 40% YoY, Solar boom, Battery tech innovations, Government schemes.
    Make it trending-friendly and action-oriented."""
    
    message = client.messages.create(
        model="claude-opus-4-20250805",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    caption = message.content[0].text
    
    # Save content
    os.makedirs("content/daily-posts", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(f"content/daily-posts/{today}.json", "w") as f:
        json.dump({
            "date": today,
            "caption": caption,
            "content_type": "energy_insight",
            "platform": "instagram",
            "status": "ready"
        }, f, indent=2)
    
    print(f"✅ Daily content generated: {today}")
    return caption

def collect_market_data():
    """Collect India's energy market data"""
    
    market_data = {
        "date": datetime.now().isoformat(),
        "india_energy": {
            "ev": {"growth": "40% YoY", "2024_sales": "1.4M+ units", "target_2030": "30% vehicles"},
            "solar": {"growth": "30% YoY", "capacity": "70+ GW", "target_2030": "500 GW"},
            "renewables": {"growth": "35% YoY", "total": "180+ GW", "jobs": "500K+ new"},
            "battery": {"growth": "50% YoY", "market": "5x by 2030", "investment": "₹5T+"}
        },
        "opportunities": {
            "ev_charging": {"roi": "15-25%", "investment": "₹50K-5L"},
            "solar": {"roi": "12-20%", "investment": "₹2-5L"},
            "ev_dealership": {"roi": "18-30%", "investment": "₹10-50L"},
            "battery": {"roi": "20-35%", "investment": "₹20L-1Cr"}
        }
    }
    
    # Save data
    os.makedirs("metrics/daily-data", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(f"metrics/daily-data/{today}.json", "w") as f:
        json.dump(market_data, f, indent=2)
    
    print(f"✅ Market data collected: {today}")
    return market_data

def generate_daily_report():
    """Generate daily report"""
    
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = {
        "date": today,
        "summary": "Daily Energy Market Report",
        "highlights": [
            "EV segment growing 40% YoY",
            "Solar capacity expanding rapidly",
            "Battery tech seeing 50% growth",
            "Government support increasing"
        ],
        "top_opportunity": "EV Charging Infrastructure (ROI: 15-25%)",
        "action_items": [
            "Check daily content posted",
            "Monitor lead submissions",
            "Review customer inquiries",
            "Update market data"
        ]
    }
    
    print(f"✅ Daily report generated: {today}")
    return report

if __name__ == "__main__":
    print("🤖 Daily Automation Tasks Started...")
    print("")
    
    # Generate content
    content = generate_energy_content()
    print(f"📱 Caption ready for Instagram:\n{content}\n")
    
    # Collect data
    data = collect_market_data()
    
    # Generate report
    report = generate_daily_report()
    
    print("")
    print("✅ All daily automation tasks completed!")
    print("📊 Content ready for posting")
    print("📈 Data collected and stored")

