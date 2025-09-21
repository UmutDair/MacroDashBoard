import streamlit as st
import streamlit.components.v1 as components
import os

# Authentication function
def check_password():
    """Returns `True` if the user had the correct password."""

    # Read expected credentials from environment (Render) or Streamlit secrets
    expected_username = os.getenv("APP_USERNAME") or st.secrets.get("APP_USERNAME", "")
    expected_password = os.getenv("APP_PASSWORD") or st.secrets.get("APP_PASSWORD", "")

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"].strip() == expected_username and st.session_state["password"] == expected_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
            del st.session_state["username"]  # Don't store the username.
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for username and password.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

# Page configuration
st.set_page_config(
    page_title="Global Macro Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .tradingview-widget-container {
        background-color: #131722;
        border-radius: 4px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .tradingview-widget-copyright {
        display: none;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

def create_tradingview_chart(symbol, height=610):
    """Helper function to create TradingView advanced charts"""
    components.html(
    f"""
    <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {{
            "width": "100%",
            "height": {height},
            "symbol": "{symbol}",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "calendar": false,
            "hide_side_toolbar": false,
            "details": true,
            "studies": [],
            "backgroundColor": "#0F0F0F",
            "gridColor": "rgba(242, 242, 242, 0.06)"
        }}
        </script>
    </div>
    """,
    height=height + 40
    )

def main():
    if not check_password():
        st.stop()
    
    with st.spinner("Loading dashboard data..."):
        st.title("Global Macro Dashboard")

    # Create tabs
    market_tab, currency_tab, economy_tab, rates_tab, commodities_tab = st.tabs([
        "🎯 Market Overview", 
        "💱 Currency Markets", 
        "📈 Economic Indicators",
        "🏦 Rates & Policy",
        "🪙 Commodities"
    ])

    # Market Overview Tab
    with market_tab:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("VIX - Advanced Chart")
            create_tradingview_chart("CAPITALCOM:VIX")
        with col2:
            st.subheader("S&P 500 Index")
            create_tradingview_chart("VANTAGE:SP500")
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("DXY - US Dollar Index")
            create_tradingview_chart("CAPITALCOM:DXY")
        with col2:
            st.subheader("Economic Calendar")
            components.html(
            """
            <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
                {
                    "width": "100%",
                    "height": 600,
                    "colorTheme": "dark",
                    "isTransparent": false,
                    "locale": "en",
                    "importanceFilter": "-1,0,1"
                }
                </script>
            </div>
            """,
            height=650
            )

    # Currency Markets Tab
    with currency_tab:
        # Forex Heatmap
        st.subheader("Forex Market Heatmap")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
            {
                "width": "100%",
                "height": 400,
                "currencies": [
                    "EUR",
                    "USD",
                    "JPY",
                    "GBP",
                    "CHF",
                    "AUD",
                    "CAD",
                    "NZD",
                    "CNY"
                ],
                "isTransparent": false,
                "colorTheme": "dark",
                "locale": "en"
            }
            </script>
        </div>
        """,
        height=450
        )

        # First row of currency pairs
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("EUR/USD")
            create_tradingview_chart("EURUSD")
        with col2:
            st.subheader("USD/CNY")
            create_tradingview_chart("USDCNY")

        # Second row of currency pairs
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("GBP/USD")
            create_tradingview_chart("GBPUSD")

    # Economic Indicators Tab
    with economy_tab:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("US GDP Growth Rate")
            create_tradingview_chart("FRED:GDP")
        with col2:
            st.subheader("US Unemployment Rate")
            create_tradingview_chart("FRED:UNRATE")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("US Industrial Production")
            create_tradingview_chart("FRED:INDPRO")
        with col2:
            st.subheader("US Core CPI")
            create_tradingview_chart("FRED:CPILFESL")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("US Retail Sales")
            create_tradingview_chart("FRED:RSXFS")
        with col2:
            st.subheader("US Non-Farm Payrolls")
            create_tradingview_chart("FRED:PAYEMS")

    # Rates & Policy Tab
    with rates_tab:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Federal Funds Rate")
            create_tradingview_chart("FRED:FEDFUNDS")
        with col2:
            st.subheader("10-Year Treasury Rate")
            create_tradingview_chart("US10Y")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("2-Year Treasury Rate")
            create_tradingview_chart("US02Y")
        with col2:
            st.subheader("30-Year Treasury Rate")
            create_tradingview_chart("US30Y")

    # Commodities Tab
    with commodities_tab:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gold Price")
            create_tradingview_chart("GOLD")
        with col2:
            st.subheader("Crude Oil Price")
            create_tradingview_chart("USOIL")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Natural Gas")
            create_tradingview_chart("NATURALGAS")
        with col2:
            st.subheader("Copper Price")
            create_tradingview_chart("COPPER")

if __name__ == "__main__":
    main()
