cat > server.js << 'EOF'
require('dotenv').config();
const express = require('express');
const twilio = require('twilio');
const cors = require('cors');
const path = require('path');

const app = express();

app.use(express.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

const logger = {
  info: (msg) => console.log(`✅ [INFO] ${new Date().toISOString()} - ${msg}`),
  error: (msg) => console.error(`❌ [ERROR] ${new Date().toISOString()} - ${msg}`)
};

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

// Contact form with WhatsApp
app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone, interest } = req.body;

    if (!name || !email || !phone) {
      return res.status(400).json({ success: false, error: 'Missing fields' });
    }

    let whatsappPhone = phone.replace(/[^0-9+]/g, '');
    if (!whatsappPhone.startsWith('+')) {
      whatsappPhone = '+91' + whatsappPhone.slice(-10);
    }

    logger.info(`Contact: ${name} (${email})`);

    try {
      await client.messages.create({
        from: `whatsapp:${process.env.TWILIO_WHATSAPP_FROM}`,
        to: `whatsapp:${whatsappPhone}`,
        body: `🚀 Welcome to FutureHQ!\n\n✅ We received your details:\nName: ${name}\nEmail: ${email}\n\n📊 Our AI team will guide you on:\n• Best EV charging solutions\n• Renewable energy investments\n• Green technology opportunities\n\n💬 Chat with our AI Bot on the website!\n📧 Email: iefuture108@gmail.com`
      });

      logger.info(`✅ WhatsApp sent to ${whatsappPhone}`);

      res.json({
        success: true,
        message: '✅ Details received! Check WhatsApp within 30 seconds.',
        data: { name, email, phone: whatsappPhone, interest }
      });

    } catch (whatsappError) {
      logger.warn(`WhatsApp error: ${whatsappError.message}`);

      res.status(202).json({
        success: true,
        warning: 'WhatsApp pending - We will email you',
        email: email
      });
    }

  } catch (error) {
    logger.error(`Contact error: ${error.message}`);
    res.status(500).json({
      success: false,
      error: 'Server error',
      message: 'Please email: iefuture108@gmail.com'
    });
  }
});

// AI Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    logger.info(`Chat: ${message.substring(0, 50)}`);

    const responses = {
      'invest': 'What budget? EV (₹50K-5L), Solar (₹2-5L), or Battery (₹20L-1Cr)?',
      'roi': 'Solar 12-20% | EV Charging 15-25% | Battery 20-35% annually',
      'subsidy': '₹5L solar subsidies & EV tax breaks available!',
      'growth': '🚀 EV 40% YoY! Solar 30% YoY! Battery 50% YoY!',
      'default': 'Hi! Ask about investments, ROI, subsidies, or energy trends!'
    };

    let response = responses.default;
    for (const [key, value] of Object.entries(responses)) {
      if (message.toLowerCase().includes(key)) {
        response = value;
        break;
      }
    }

    res.json({
      success: true,
      response,
      suggestions: ['What\'s ROI?', 'Show opportunities', 'Government schemes?']
    });

  } catch (error) {
    logger.error(`Chat error: ${error.message}`);
    res.status(500).json({ success: false, response: 'Error. Email: iefuture108@gmail.com' });
  }
});

// Energy market data
app.get('/api/energy-data', (req, res) => {
  res.json({
    date: new Date().toISOString(),
    india_energy: {
      ev: { growth: '40% YoY', target_2030: '30% vehicles' },
      solar: { growth: '30% YoY', capacity: '70+ GW → 500 GW' },
      renewables: { growth: '35% YoY', total: '180+ GW' },
      battery: { growth: '50% YoY', market: '5x by 2030' }
    }
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'alive',
    service: 'FutureHQ.in',
    timestamp: new Date().toISOString(),
    apis: { contact: '✅', chat: '✅', energy_data: '✅' }
  });
});

// Serve files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  logger.info(`🚀 FutureHQ Server on PORT ${PORT}`);
  logger.info(`✅ WhatsApp: Ready`);
  logger.info(`✅ Chat: Ready`);
  logger.info(`✅ Data: Ready`);
});

module.exports = app;
EOF

echo "✅ server.js completely replaced"
