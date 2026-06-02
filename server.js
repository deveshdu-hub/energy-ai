const express = require('express');
const dotenv = require('dotenv');
const twilio = require('twilio');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

const twilioClient = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

// Contact Form Handler
app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone, interest, message } = req.body;

    if (!name || !phone || !interest) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    console.log(`📝 New inquiry from ${name} about ${interest}`);

    // Customer message
    const customerMessage = await twilioClient.messages.create({
      body: `🚀 Hi ${name}!\n\nThanks for your interest in ${interest}.\n\nWe specialize in India's energy future:\n✅ EV Infrastructure\n✅ Renewable Energy\n✅ Clean Technology\n\nOur team will contact you within 24 hours.\n\n📱 Follow @indiaenergyfuture_hq for daily insights!\n\n- FutureHQ Team`,
      from: process.env.TWILIO_WHATSAPP_FROM,
      to: `whatsapp:${phone}`
    });

    // Internal notification
    const internalNotification = await twilioClient.messages.create({
      body: `🔔 NEW INQUIRY - FutureHQ.in\n\nName: ${name}\nPhone: ${phone}\nEmail: ${email}\nInterest: ${interest}\nMessage: ${message}\n\nReply ASAP!`,
      from: process.env.TWILIO_WHATSAPP_FROM,
      to: process.env.TWILIO_WHATSAPP_TO
    });

    const leadData = {
      name, email, phone, interest, message,
      source: 'futurehq_website_form',
      timestamp: new Date(),
      status: 'new'
    };

    console.log('✅ FutureHQ Lead captured:', leadData);

    res.json({
      success: true,
      message: 'Thanks for reaching out! Check your WhatsApp for our response.',
      leadId: leadData.timestamp
    });

  } catch (error) {
    console.error('❌ Error in contact form:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Instagram Metrics
app.get('/api/instagram/metrics', async (req, res) => {
  try {
    const response = await axios.get('https://graph.instagram.com/me', {
      params: {
        fields: 'ig_username,followers_count,biography,website',
        access_token: process.env.INSTAGRAM_TOKEN
      }
    });

    res.json({
      profile: '@indiaenergyfuture_hq',
      username: response.data.ig_username,
      followers: response.data.followers_count,
      bio: response.data.biography,
      website: response.data.website,
      timestamp: new Date()
    });
  } catch (error) {
    console.error('Instagram API error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Daily Report
app.get('/api/daily-report', async (req, res) => {
  try {
    const report = {
      date: new Date().toISOString().split('T')[0],
      domain: 'futurehq.in',
      instagram: { profile: '@indiaenergyfuture_hq', status: 'active' },
      whatsapp: { integration: 'active', status: 'ready' },
      website: { domain: 'https://www.futurehq.in', status: 'live' },
      automation: {
        content_generation: 'scheduled_6am',
        metrics_collection: 'scheduled_8am',
        status: 'active'
      }
    };
    res.json(report);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Health Check
app.get('/health', (req, res) => {
  res.json({
    status: 'alive',
    service: 'FutureHQ.in Automation',
    timestamp: new Date(),
    uptime: process.uptime()
  });
});

// Homepage
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`
  🚀 FutureHQ.in Automation Server Running
  📍 Domain: https://www.futurehq.in
  🌐 Backend: Energy-Nexus-Insight
  📱 Instagram: @indiaenergyfuture_hq
  ✅ Status: LIVE & READY
  `);
});

module.exports = app;
