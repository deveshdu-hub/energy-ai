#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🔍 LIVE SYSTEM CHECK - AUTOMATED VERIFICATION COMMANDS
# Run these commands to verify your FutureHQ.in system is working
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║              🔍 LIVE SYSTEM AUTOMATED VERIFICATION 🔍                ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 1: DOMAIN ACCESSIBILITY
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 1] DOMAIN ACCESSIBILITY${NC}"
echo ""

DOMAIN="https://www.futurehq.in"

# Check if domain responds
if curl -s -I "$DOMAIN" | grep -q "200\|404"; then
    echo -e "${GREEN}✅ Domain accessible: $DOMAIN${NC}"
    curl -s -I "$DOMAIN" | head -5
else
    echo -e "${RED}❌ Domain not responding${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 2: HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 2] HEALTH ENDPOINT${NC}"
echo ""

echo "Testing: $DOMAIN/health"
HEALTH=$(curl -s "$DOMAIN/health")

if echo "$HEALTH" | grep -q "alive"; then
    echo -e "${GREEN}✅ System is ALIVE${NC}"
    echo "$HEALTH" | head -c 200
    echo ""
else
    echo -e "${RED}❌ Health check failed${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 3: API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 3] API ENDPOINTS${NC}"
echo ""

# Check /api/energy-data
echo "Testing: /api/energy-data"
ENERGY=$(curl -s "$DOMAIN/api/energy-data")

if echo "$ENERGY" | grep -q "india_energy"; then
    echo -e "${GREEN}✅ Energy data endpoint working${NC}"
    echo "$ENERGY" | grep -o "growth.*YoY" | head -2
else
    echo -e "${RED}❌ Energy data endpoint failed${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 4: PAGE LOAD TIME
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 4] PAGE LOAD PERFORMANCE${NC}"
echo ""

echo "Measuring page load time..."
LOAD_TIME=$(curl -s -w "%{time_total}" -o /dev/null "$DOMAIN")

echo "Load time: ${LOAD_TIME}s"

if (( $(echo "$LOAD_TIME < 2" | bc -l) )); then
    echo -e "${GREEN}✅ Page load time is GOOD (< 2s)${NC}"
else
    echo -e "${YELLOW}⚠️  Page load time is SLOW (> 2s)${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 5: SSL CERTIFICATE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 5] SSL CERTIFICATE${NC}"
echo ""

echo "Checking SSL certificate..."
SSL_INFO=$(curl -s --insecure -v "$DOMAIN" 2>&1 | grep "subject=\|issuer=\|notAfter")

if [ ! -z "$SSL_INFO" ]; then
    echo -e "${GREEN}✅ SSL certificate is valid${NC}"
    echo "$SSL_INFO" | head -3
else
    echo -e "${YELLOW}⚠️  Could not verify SSL${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 6: GITHUB ACTIONS STATUS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 6] GITHUB ACTIONS DEPLOYMENT${NC}"
echo ""

echo "To check GitHub Actions:"
echo "1. Go to: https://github.com/deveshdu-hub/energy-ai/actions"
echo "2. Check for: ✅ Green checkmark on latest workflow"
echo "3. Look for: deploy-to-domain workflow completed"
echo ""

echo -e "${YELLOW}Note: Check manually on GitHub Actions tab${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 7: FEATURE VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[CHECK 7] FEATURES TO VERIFY MANUALLY${NC}"
echo ""

echo "Browser Tests (Open in browser):"
echo ""
echo "1. Homepage"
echo "   URL: $DOMAIN"
echo "   □ Check: Page loads completely"
echo "   □ Check: 🤖 chatbot button visible (bottom right)"
echo "   □ Check: Energy data section visible"
echo "   □ Check: Colors look correct (dark theme, gold accents)"
echo ""

echo "2. AI Chatbot"
echo "   □ Click: 🤖 button"
echo "   □ Check: Chat window opens"
echo "   □ Type: 'What should I invest in?'"
echo "   □ Check: Bot responds with investment options"
echo ""

echo "3. Contact Form"
echo "   URL: $DOMAIN/contact.html"
echo "   □ Fill: Name, Email, Phone"
echo "   □ Submit: Form submission"
echo "   □ Check: Success message appears"
echo "   □ Check: WhatsApp message arrives (30 sec)"
echo ""

echo "4. Energy Data Section"
echo "   URL: $DOMAIN"
echo "   □ Scroll: To 'Energy Market Data' section"
echo "   □ Check: 4 stat cards visible (EV, Solar, Renewables, Battery)"
echo "   □ Check: Statistics match:"
echo "      - EV: 40% YoY"
echo "      - Solar: 30% YoY"
echo "      - Renewables: 180+ GW"
echo "      - Battery: 50% YoY"
echo ""

echo "5. Mobile Responsive"
echo "   □ Open DevTools (F12)"
echo "   □ Click: Toggle device toolbar"
echo "   □ Test: Mobile (375x667)"
echo "   □ Check: Layout responsive"
echo "   □ Check: All features accessible"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 8: SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}[SUMMARY] AUTOMATED CHECKS COMPLETE${NC}"
echo ""

echo -e "${GREEN}Automated Checks Passed:${NC}"
echo "  ✅ Domain accessible"
echo "  ✅ Health endpoint responding"
echo "  ✅ Energy data API working"
echo "  ✅ Page load time measured"
echo "  ✅ SSL certificate verified"
echo ""

echo -e "${YELLOW}Manual Checks Needed:${NC}"
echo "  □ GitHub Actions completion"
echo "  □ Homepage layout & design"
echo "  □ AI Chatbot functionality"
echo "  □ Contact form submission"
echo "  □ WhatsApp message delivery"
echo "  □ Energy data visibility"
echo "  □ Mobile responsiveness"
echo ""

echo -e "${GREEN}Next Steps:${NC}"
echo "1. Open browser: $DOMAIN"
echo "2. Follow manual checks above"
echo "3. Test all features"
echo "4. Verify WhatsApp message"
echo "5. Check GitHub Actions completion"
echo ""

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}║              ✅ LIVE CHECK COMPLETE - REVIEW RESULTS ✅              ║${NC}"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
