# VOLT / Energy AI — "Bharat Harit Kranti Portal" (repo `deveshdu-hub/energy-ai`) — Review

Reviewed 2026-07-06. **Verdict: mature, well-built. No code fix needed; one small cleanup.**

## Why it's good
- Config correct (`.streamlit/config.toml`, dark theme, XSRF on).
- AI uses **Gemini `gemini-2.0-flash`** (free tier) — zero-cost core.
- Uses **Supabase** for data (free tier) — proper persistent database, not local files.
- Ships an **MCP server** (`mcp.py`) that connects Claude to the Supabase leads/stats.
- Paid services (**Twilio** OTP, **Razorpay** payments, **SendGrid** email) are all
  **optional and feature-gated** — they only activate if you add those secrets, so the
  app runs **zero-cost by default**. Add those keys only when you want SMS/payments/email.

## One cleanup (low severity — no leak)
`.streamlit/secrets.toml` is committed to the repo but is **empty** (no keys leaked), and
`.gitignore` already lists it. Still, untrack it so a real key can never get committed later:
```bash
git rm --cached .streamlit/secrets.toml
git commit -m "stop tracking secrets.toml (keep it local only)"
git push
```

## Note
This is a big production app (OTP, calculators, content studio, vendor dashboard,
marketplace). It's in good shape — I did not rewrite it. If you want, later I can do a
focused pass on any one feature you name.
