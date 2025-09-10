import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
from datetime import datetime, timedelta
import hmac
import hashlib

# Authentication function
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"].strip() == "DairCapital" and st.session_state["password"] == "DairResearch123!":
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

def main():
    if not check_password():
        st.stop()  # Do not continue if check_password is not True
    
    st.title("Global Macro Dashboard")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    # VIX Advanced Chart Widget
    with col1:
        st.subheader("VIX - Advanced Chart")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "CAPITALCOM:VIX",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )    # DXY Advanced Chart Widget
    with col2:
        st.subheader("DXY - US Dollar Index")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "CAPITALCOM:DXY",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # CFNAI Advanced Chart Widget
    with col1:
        st.subheader("CFNAI - Chicago Fed National Activity Index")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FRED:CFNAI",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # UNRATE Advanced Chart Widget
    with col2:
        st.subheader("UNRATE - US Unemployment Rate")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FRED:UNRATE",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # Federal Funds Rate Chart Widget
    with col1:
        st.subheader("Federal Funds Rate (FEDFUNDS)")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FRED:FEDFUNDS",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Oil Price Chart Widget
    with col2:
        st.subheader("Crude Oil Price")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "MARKETSCOM:OIL",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # Gold Price Chart Widget
    with col1:
        st.subheader("Gold Price")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "CAPITALCOM:GOLD",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # S&P 500 Chart Widget
    with col2:
        st.subheader("S&P 500 Index")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "VANTAGE:SP500",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # Industrial Production Index Chart Widget
    with col1:
        st.subheader("Industrial Production Index (INDPRO)")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FRED:INDPRO",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Initialize FRED API
    fred = Fred(api_key=st.secrets["FRED_API_KEY"])
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*20)  # 20 years of data

    def create_fred_chart(series_id, title, units="", calculate_pct_change=False):
        data = fred.get_series(series_id, start_date, end_date)
        df = pd.DataFrame(data).reset_index()
        df.columns = ['Date', 'Value']
        
        if calculate_pct_change:
            # Calculate month-over-month percentage change
            df['Value'] = df['Value'].pct_change() * 100
            # Drop the first row as it will be NaN
            df = df.dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], mode='lines', name=title))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=units,
            template="plotly_dark",
            height=500,
            showlegend=False,
            paper_bgcolor="#131722",
            plot_bgcolor="#131722",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        return fig

    # Create new columns for FRED charts
    col1, col2 = st.columns(2)

    # Real GDP (Quarterly, Billions of Dollars)
    with col1:
        st.subheader("Real GDP")
        gdp_fig = create_fred_chart('GDPC1', 'Real Gross Domestic Product', 'Billions of Chained 2012 Dollars')
        st.plotly_chart(gdp_fig, use_container_width=True)

    # Consumer Price Index (Monthly % Change)
    with col2:
        st.subheader("CPI Monthly Percentage Change")
        cpi_fig = create_fred_chart('CPIAUCSL', 'Consumer Price Index (1-Month % Change)', 'Percent Change', calculate_pct_change=True)
        st.plotly_chart(cpi_fig, use_container_width=True)

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # Nonfarm Payroll (Monthly, Thousands of Persons)
    with col1:
        st.subheader("Total Nonfarm Payroll")
        nfp_fig = create_fred_chart('PAYEMS', 'All Employees: Total Nonfarm', 'Thousands of Persons')
        st.plotly_chart(nfp_fig, use_container_width=True)

    # Retail Sales (Monthly, Millions of Dollars)
    with col2:
        st.subheader("Retail Sales")
        retail_fig = create_fred_chart('RSXFS', 'Advance Retail Sales: Retail Trade', 'Millions of Dollars')
        st.plotly_chart(retail_fig, use_container_width=True)

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # 10-Year Treasury Rate (Daily, Percent)
    with col1:
        st.subheader("10-Year Treasury Rate")
        treasury_fig = create_fred_chart('DGS10', '10-Year Treasury Constant Maturity Rate', 'Percent')
        st.plotly_chart(treasury_fig, use_container_width=True)

    # Economic Calendar Widget
    with col2:
        st.subheader("Economic Calendar")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
            {
                "colorTheme": "dark",
                "isTransparent": false,
                "locale": "en",
                "countryFilter": "ar,au,br,ca,cn,fr,de,in,id,it,jp,kr,mx,ru,sa,za,tr,gb,us,eu",
                "importanceFilter": "-1,0,1",
                "width": "100%",
                "height": 500
            }
            </script>
        </div>
        """,
        height=550
    )

    # Create new columns for next row
    col1, col2 = st.columns(2)

    # Forex Heatmap Widget
    with col1:
        st.subheader("Forex Market Heatmap")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
            {
                "colorTheme": "dark",
                "isTransparent": false,
                "locale": "en",
                "currencies": [
                    "EUR",
                    "USD",
                    "JPY",
                    "GBP",
                    "CNY"
                ],
                "backgroundColor": "#0F0F0F",
                "width": "100%",
                "height": 500
            }
            </script>
        </div>
        """,
        height=550
    )

    # Create new columns for forex pairs
    col1, col2 = st.columns(2)

    # EUR/USD Chart Widget
    with col1:
        st.subheader("EUR/USD")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "CMCMARKETS:EURUSD",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # USD/CNY Chart Widget
    with col2:
        st.subheader("USD/CNY")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FX_IDC:USDCNY",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

    # Create new columns for the last forex pair
    col1, col2 = st.columns(2)

    # USD/GBP Chart Widget
    with col1:
        st.subheader("USD/GBP")
        components.html(
        """
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {
                "allow_symbol_change": true,
                "calendar": false,
                "details": false,
                "hide_side_toolbar": true,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "hide_volume": false,
                "hotlist": false,
                "interval": "D",
                "locale": "en",
                "save_image": true,
                "style": "1",
                "symbol": "FX_IDC:USDGBP",
                "theme": "dark",
                "timezone": "Etc/UTC",
                "backgroundColor": "#0F0F0F",
                "gridColor": "rgba(242, 242, 242, 0.06)",
                "watchlist": [],
                "withdateranges": false,
                "compareSymbols": [],
                "studies": [],
                "width": "100%",
                "height": 610
            }
            </script>
        </div>
        """,
        height=650
    )

if __name__ == "__main__":
    main()
