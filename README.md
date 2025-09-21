Global Macro Dashboard (Streamlit) on Render

This repository contains a Streamlit app that embeds TradingView widgets for a macro dashboard.

Local Run

```bash
pip install -r requirements.txt
streamlit run binance_widgets_tradingview.py
```

Optionally set credentials locally:

```bash
export APP_USERNAME="your_user"
export APP_PASSWORD="your_pass"
```

Deploy to Render

1. Push this repo to GitHub.
2. In Render, click "New +" → "Web Service" and select the repo. Render will auto-detect `render.yaml`.
3. In the service, set environment variables:
   - `APP_USERNAME`
   - `APP_PASSWORD`
4. Deploy. Render exposes `$PORT`, and the service will start with:

```bash
streamlit run binance_widgets_tradingview.py --server.port $PORT --server.address 0.0.0.0
```

Notes

- Auth credentials are read from environment variables (and optionally `st.secrets`).
- `.streamlit/config.toml` is set for headless mode and dark theme.

