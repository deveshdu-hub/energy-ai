<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Future HQ India | AI Energy Future Platform</title>

  <meta name="description" content="India's futuristic AI-powered EV, Solar & Clean Energy PWA platform." />

  <meta property="og:title" content="Future HQ India" />
  <meta property="og:description" content="AI-powered India Energy Future Platform" />
  <meta property="og:type" content="website" />

  <meta name="theme-color" content="#00d9ff" />

  <link rel="manifest" href="manifest.json" />
  <link rel="stylesheet" href="style.css" />

  <link rel="icon" href="icon-192.png" />

  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>

<body>

  <!-- Animated Background -->
  <div class="bg-animation"></div>

  <!-- Header -->
  <header class="header">
    <div class="logo">
      ⚡ FUTURE HQ INDIA
    </div>

    <nav class="nav">
      <a href="#ev">EV</a>
      <a href="#solar">Solar</a>
      <a href="#ai">AI</a>
      <a href="#schemes">Schemes</a>
    </nav>
  </header>

  <!-- Hero Section -->
  <section class="hero">

    <div class="hero-content">

      <p class="tag">
        INDIA'S AI ENERGY FUTURE
      </p>

      <h1>
        Smart EV & Solar Intelligence Platform
      </h1>

      <p class="hero-text">
        Explore AI-powered energy insights, EV savings,
        solar ROI calculators, charging intelligence,
        and India's clean energy future.
      </p>

      <div class="hero-buttons">
        <button class="primary-btn">
          Launch AI Assistant
        </button>

        <button class="secondary-btn">
          Explore Calculators
        </button>
      </div>

    </div>

  </section>

  <!-- AI Assistant -->
  <section id="ai" class="glass-card">

    <h2>🤖 AI Energy Assistant</h2>

    <div class="ai-box">

      <div class="ai-message">
        Hello 👋 <br>
        Ask anything about EVs, Solar, Batteries,
        or India Energy Future.
      </div>

      <input type="text"
        placeholder="Ask AI something..."
        class="ai-input">

      <button class="primary-btn">
        Ask AI
      </button>

    </div>

  </section>

  <!-- EV Calculator -->
  <section id="ev" class="glass-card">

    <h2>⚡ EV Savings Calculator</h2>

    <div class="calculator">

      <input type="number"
        id="petrolCost"
        placeholder="Monthly Petrol Expense ₹">

      <button onclick="calculateSavings()"
        class="primary-btn">
        Calculate Savings
      </button>

      <h3 id="result"></h3>

    </div>

  </section>

  <!-- Solar Calculator -->
  <section id="solar" class="glass-card">

    <h2>☀️ Solar ROI Calculator</h2>

    <div class="calculator">

      <input type="number"
        id="solarBill"
        placeholder="Monthly Electricity Bill ₹">

      <button onclick="calculateSolar()"
        class="primary-btn">
        Calculate ROI
      </button>

      <h3 id="solarResult"></h3>

    </div>

  </section>

  <!-- Energy News -->
  <section class="glass-card">

    <h2>📰 India Energy Insights</h2>

    <div class="news-grid">

      <div class="news-card">
        <h3>EV Growth</h3>
        <p>India EV adoption expected to grow rapidly by 2030.</p>
      </div>

      <div class="news-card">
        <h3>Solar Revolution</h3>
        <p>Rooftop solar installations accelerating nationwide.</p>
      </div>

      <div class="news-card">
        <h3>Battery Future</h3>
        <p>Next-gen battery tech transforming clean mobility.</p>
      </div>

    </div>

  </section>

  <!-- Charging Map -->
  <section class="glass-card">

    <h2>📍 Future Charging Map</h2>

    <div class="map-placeholder">
      Smart Charging Infrastructure Map Coming Soon...
    </div>

  </section>

  <!-- Government Schemes -->
  <section id="schemes" class="glass-card">

    <h2>🏛 Government Energy Schemes</h2>

    <div class="scheme-list">

      <div class="scheme-card">
        FAME India EV Subsidy
      </div>

      <div class="scheme-card">
        PM Solar Rooftop Yojana
      </div>

      <div class="scheme-card">
        State EV Incentives
      </div>

    </div>

  </section>

  <!-- Footer -->
  <footer class="footer">

    <h2>⚡ FUTURE HQ INDIA</h2>

    <p>
      AI Powered India Energy Ecosystem
    </p>

    <p class="footer-small">
      Built for India's Sustainable Future
    </p>

  </footer>

  <!-- Bottom Navigation -->
  <div class="bottom-nav">

    <a href="#">🏠</a>
    <a href="#ev">⚡</a>
    <a href="#solar">☀️</a>
    <a href="#ai">🤖</a>

  </div>

  <!-- JS -->
  <script src="app.js"></script>

  <!-- Service Worker -->
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('service-worker.js');
    }
  </script>

</body>
</html>
