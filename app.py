import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Maruti Suzuki | Financial Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

COMPANY_NAME = "Maruti Suzuki India Ltd"
ACCENT = "#00C2A8"
ACCENT_2 = "#4C8BF5"
PURPLE = "#B18CFF"
RED = "#FF5C5C"
GREEN = "#3DDC84"
AMBER = "#FFC24B"

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* Animated gradient backdrop */
.stApp {{
    background: linear-gradient(120deg, #05070a, #0a0f14, #070c12, #05070a);
    background-size: 300% 300%;
    animation: bgFlow 22s ease infinite;
}}
@keyframes bgFlow {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Custom scrollbar */
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-thumb {{ background: rgba(0,194,168,0.45); border-radius: 10px; }}
::-webkit-scrollbar-track {{ background: transparent; }}

/* ---------- HERO ---------- */
.hero {{
    position: relative;
    padding: 30px 32px;
    border-radius: 20px;
    background: linear-gradient(120deg, rgba(0,194,168,0.20), rgba(76,139,245,0.12) 50%, rgba(177,140,255,0.10));
    background-size: 200% 200%;
    animation: heroShift 12s ease infinite;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
    overflow: hidden;
}}
@keyframes heroShift {{
    0% {{ background-position: 0% 0%; }}
    50% {{ background-position: 100% 100%; }}
    100% {{ background-position: 0% 0%; }}
}}
.hero::after {{
    content: "🚗";
    position: absolute;
    font-size: 7rem;
    opacity: 0.06;
    right: 10px;
    top: -10px;
    transform: rotate(-8deg);
}}
.hero h1 {{
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 4px;
    color: #F5F7FA;
    letter-spacing: -0.01em;
}}
.hero p {{
    color: #9BA5B4;
    font-size: 0.97rem;
    margin: 0;
}}

/* ---------- CHIPS ---------- */
.chip-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; }}
.chip {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: #D5DAE1;
    transition: all 0.2s ease;
}}
.chip:hover {{
    border-color: {ACCENT};
    background: rgba(0,194,168,0.10);
    transform: translateY(-1px);
}}

/* ---------- TICKER ---------- */
.ticker-wrap {{
    overflow: hidden;
    white-space: nowrap;
    border-radius: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 9px 0;
    margin-bottom: 20px;
}}
.ticker-track {{
    display: flex;
    width: max-content;
    animation: tickerScroll 32s linear infinite;
    gap: 60px;
}}
.ticker-track span {{
    white-space: nowrap;
    padding-right: 60px;
    color: #A7B0BC;
    font-size: 0.85rem;
}}
@keyframes tickerScroll {{
    from {{ transform: translateX(0); }}
    to {{ transform: translateX(-50%); }}
}}

/* ---------- KPI CARDS ---------- */
.kpi-card {{
    background: rgba(255,255,255,0.045);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px 16px 4px 4px;
    padding: 18px 20px 6px 20px;
    opacity: 0;
    animation: fadeInUp 0.55s ease forwards;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}}
.kpi-card:hover {{
    transform: translateY(-4px);
    border-color: rgba(0,194,168,0.55);
    box-shadow: 0 10px 26px rgba(0,194,168,0.12);
}}
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.kpi-label {{
    color: #9BA5B4;
    font-size: 0.80rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}}
.kpi-value {{
    font-size: 1.85rem;
    font-weight: 800;
    color: #F5F7FA;
    margin-top: 3px;
    line-height: 1.1;
}}
.kpi-delta-pos {{ color: {GREEN}; font-weight: 600; font-size: 0.85rem; }}
.kpi-delta-neg {{ color: {RED}; font-weight: 600; font-size: 0.85rem; }}
.kpi-spark {{ margin-top: 6px; }}

/* ---------- BADGES ---------- */
.badge-grew {{
    background: rgba(61,220,132,0.15); color: {GREEN};
    padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
}}
.badge-declined {{
    background: rgba(255,92,92,0.15); color: {RED};
    padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
}}

/* ---------- SECTION CARD WRAPPER ---------- */
.section-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px 18px 4px 18px;
    margin-bottom: 18px;
    animation: fadeInUp 0.6s ease forwards;
}}
.section-title {{
    font-size: 1.02rem;
    font-weight: 700;
    color: #F0F2F5;
    margin-bottom: 8px;
}}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {{
    background: #0A0D12;
    border-right: 1px solid rgba(255,255,255,0.06);
}}

/* ---------- TABS ---------- */
div[data-baseweb="tab-list"] {{
    gap: 4px;
    background: rgba(255,255,255,0.03);
    padding: 6px;
    border-radius: 14px;
}}
button[data-baseweb="tab"] {{
    border-radius: 10px !important;
    transition: all 0.2s ease;
    color: #9BA5B4 !important;
}}
button[data-baseweb="tab"]:hover {{
    background: rgba(0,194,168,0.10);
    color: #F5F7FA !important;
}}
button[aria-selected="true"] {{
    background: linear-gradient(120deg, rgba(0,194,168,0.25), rgba(76,139,245,0.18)) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

div[data-testid="stMetricValue"] {{ font-size: 1.6rem; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SPARKLINE HELPER (pure SVG, no JS)
# ============================================================
def sparkline_svg(values, color, width=140, height=34):
    values = [v for v in values if pd.notna(v)]
    if len(values) < 2:
        return ""
    vmin, vmax = min(values), max(values)
    rng = (vmax - vmin) or 1
    n = len(values)
    step = width / (n - 1)
    pts = [(i * step, height - ((v - vmin) / rng) * (height - 6) - 3) for i, v in enumerate(values)]
    line_path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area_path = f"M {pts[0][0]:.1f},{height} L " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L {pts[-1][0]:.1f},{height} Z"
    lx, ly = pts[-1]
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="display:block;">
        <path d="{area_path}" fill="{color}" opacity="0.16"/>
        <path d="{line_path}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.4" fill="{color}">
            <animate attributeName="r" values="3;4.5;3" dur="1.8s" repeatCount="indefinite"/>
        </circle>
    </svg>
    """


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("company_financials_clean.csv")
    try:
        model_results = pd.read_csv("model_comparison.csv")
    except FileNotFoundError:
        model_results = None
    return df, model_results

df, model_results = load_data()
df["Period_dt"] = pd.to_datetime(df["Period"], format="%b-%Y")
df = df.sort_values("Period_dt").reset_index(drop=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🚗 " + COMPANY_NAME)
    st.caption("CA2 Project — MCA Data Science, LPU")
    st.markdown("---")

    periods = df["Period"].tolist()
    p_range = st.select_slider(
        "📅 Filter by period range",
        options=periods,
        value=(periods[0], periods[-1]),
    )
    start_idx, end_idx = periods.index(p_range[0]), periods.index(p_range[1])
    n_shown = end_idx - start_idx + 1
    st.progress(n_shown / len(periods))
    st.caption(f"Showing {n_shown} of {len(periods)} quarters")

    st.markdown("---")
    st.markdown("**Data source:** [Screener.in](https://www.screener.in)")
    st.markdown("**Sector:** Automobile — Passenger Vehicles")
    st.markdown("**Frequency:** Quarterly")
    st.markdown("---")
    st.caption("Built with Streamlit + Plotly")

fdf = df.iloc[start_idx:end_idx + 1].reset_index(drop=True)

# ============================================================
# HERO HEADER
# ============================================================
st.markdown(f"""
<div class="hero">
    <h1>📊 Financial Performance Dashboard</h1>
    <p>{COMPANY_NAME} &nbsp;•&nbsp; Quarterly Results &nbsp;•&nbsp; {fdf['Period'].iloc[0]} to {fdf['Period'].iloc[-1]}</p>
    <div class="chip-row">
        <span class="chip">🏭 Sector: Automobile</span>
        <span class="chip">📈 Exchange: NSE / BSE</span>
        <span class="chip">💱 Currency: INR (₹ Crore)</span>
        <span class="chip">🗂 Frequency: Quarterly</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TICKER
# ============================================================
sales_growth_total = (fdf["Sales"].iloc[-1] / fdf["Sales"].iloc[0] - 1) * 100 if len(fdf) > 1 else 0
best_q = fdf.loc[fdf["Net_Profit"].idxmax(), "Period"]
worst_opm_q = fdf.loc[fdf["OPM_Percent"].idxmin(), "Period"]
ticker_items = [
    f"📈 Sales grew {sales_growth_total:.1f}% from {fdf['Period'].iloc[0]} to {fdf['Period'].iloc[-1]}",
    f"💰 Latest Net Profit: ₹{fdf['Net_Profit'].iloc[-1]:,.0f} Cr",
    f"⚙️ Average OPM: {fdf['OPM_Percent'].mean():.2f}%",
    f"🏆 Strongest Net Profit quarter: {best_q}",
    f"📉 Softest OPM quarter: {worst_opm_q}",
    f"💵 Latest EPS: ₹{fdf['EPS'].iloc[-1]:.2f}",
]
ticker_html = "".join(f"<span>{t}</span>" for t in ticker_items) * 2
st.markdown(f"""
<div class="ticker-wrap"><div class="ticker-track">{ticker_html}</div></div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS (with sparklines + QoQ delta)
# ============================================================
latest = fdf.iloc[-1]
prev = fdf.iloc[-2] if len(fdf) > 1 else latest

def delta_pct(cur, prv):
    if prv == 0 or pd.isna(prv):
        return None
    return (cur - prv) / abs(prv) * 100

spark_window = fdf.tail(8)
kpis = [
    ("💰 Latest Sales", f"₹{latest['Sales']:,.0f} Cr", delta_pct(latest["Sales"], prev["Sales"]), spark_window["Sales"].tolist(), ACCENT_2),
    ("📈 Net Profit", f"₹{latest['Net_Profit']:,.0f} Cr", delta_pct(latest["Net_Profit"], prev["Net_Profit"]), spark_window["Net_Profit"].tolist(), ACCENT),
    ("⚙️ OPM Margin", f"{latest['OPM_Percent']:.2f}%", delta_pct(latest["OPM_Percent"], prev["OPM_Percent"]), spark_window["OPM_Percent"].tolist(), AMBER),
    ("💵 EPS", f"₹{latest['EPS']:.2f}", delta_pct(latest["EPS"], prev["EPS"]), spark_window["EPS"].tolist(), PURPLE),
]

cols = st.columns(4)
for i, (col, (label, value, delta, spark_vals, spark_color)) in enumerate(zip(cols, kpis)):
    if delta is None:
        delta_html = "&nbsp;"
    elif delta >= 0:
        delta_html = f'<span class="kpi-delta-pos">▲ {delta:.1f}% QoQ</span>'
    else:
        delta_html = f'<span class="kpi-delta-neg">▼ {abs(delta):.1f}% QoQ</span>'
    spark = sparkline_svg(spark_vals, spark_color)
    col.markdown(f"""
    <div class="kpi-card" style="animation-delay:{i*0.08:.2f}s">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
        <div class="kpi-spark">{spark}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Trends & Charts", "🧮 Statistics", "🤖 Model Comparison", "📋 Raw Data"]
)

PLOTLY_TEMPLATE = "plotly_dark"
COMMON_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#D5DAE1"),
    transition=dict(duration=400, easing="cubic-in-out"),
)

# ---------- TAB 1: TRENDS ----------
with tab1:
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown('<div class="section-card"><div class="section-title">Sales & Net Profit Trend</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fdf["Period"], y=fdf["Sales"], mode="lines+markers", name="Sales",
            line=dict(color=ACCENT_2, width=3, shape="spline"), marker=dict(size=8),
            fill="tozeroy", fillcolor="rgba(76,139,245,0.08)",
            hovertemplate="%{x}<br>Sales: ₹%{y:,.0f} Cr<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=fdf["Period"], y=fdf["Net_Profit"], mode="lines+markers", name="Net Profit",
            line=dict(color=ACCENT, width=3, shape="spline"), marker=dict(size=8),
            fill="tozeroy", fillcolor="rgba(0,194,168,0.10)",
            hovertemplate="%{x}<br>Net Profit: ₹%{y:,.0f} Cr<extra></extra>"
        ))
        fig.update_layout(template=PLOTLY_TEMPLATE, height=380, margin=dict(t=10, b=10, l=10, r=10),
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                           yaxis_title="₹ Crore", hovermode="x unified", **COMMON_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-card"><div class="section-title">OPM Gauge (Latest Q)</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest["OPM_Percent"],
            number={"suffix": "%", "font": {"size": 34, "color": "#F5F7FA"}},
            gauge={
                "axis": {"range": [0, 20], "tickcolor": "#9BA5B4"},
                "bar": {"color": ACCENT},
                "bgcolor": "rgba(255,255,255,0.02)",
                "steps": [
                    {"range": [0, 8], "color": "rgba(255,92,92,0.25)"},
                    {"range": [8, 14], "color": "rgba(255,196,0,0.20)"},
                    {"range": [14, 20], "color": "rgba(61,220,132,0.25)"},
                ],
            },
        ))
        fig_gauge.update_layout(template=PLOTLY_TEMPLATE, height=280, margin=dict(t=30, b=10, l=20, r=20), **COMMON_LAYOUT)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-card"><div class="section-title">Operating Profit Margin (OPM %)</div>', unsafe_allow_html=True)
        colors = [GREEN if v >= fdf["OPM_Percent"].mean() else RED for v in fdf["OPM_Percent"]]
        fig_bar = go.Figure(go.Bar(
            x=fdf["Period"], y=fdf["OPM_Percent"], marker_color=colors, marker_line_width=0,
            hovertemplate="%{x}<br>OPM: %{y:.2f}%<extra></extra>"
        ))
        fig_bar.add_hline(y=fdf["OPM_Percent"].mean(), line_dash="dot", line_color="#9BA5B4",
                           annotation_text="Average", annotation_font_color="#9BA5B4")
        fig_bar.update_layout(template=PLOTLY_TEMPLATE, height=340, margin=dict(t=10, b=10, l=10, r=10),
                               yaxis_title="OPM %", **COMMON_LAYOUT)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="section-card"><div class="section-title">Net Profit Distribution by Profit Trend</div>', unsafe_allow_html=True)
        fig_box = px.box(fdf, x="Profit_Trend", y="Net_Profit", color="Profit_Trend",
                          color_discrete_map={"Profit Grew": GREEN, "Profit Declined": RED},
                          points="all")
        fig_box.update_layout(template=PLOTLY_TEMPLATE, height=340, margin=dict(t=10, b=10, l=10, r=10),
                               showlegend=False, yaxis_title="Net Profit (₹ Crore)", **COMMON_LAYOUT)
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Sales vs Net Profit vs Other Income — Composition</div>', unsafe_allow_html=True)
    fig_area = go.Figure()
    for col_name, color in [("Sales", ACCENT_2), ("Other_Income", PURPLE), ("Net_Profit", ACCENT)]:
        fig_area.add_trace(go.Scatter(
            x=fdf["Period"], y=fdf[col_name], name=col_name.replace("_", " "),
            mode="lines", line=dict(width=2.4, color=color, shape="spline")
        ))
    fig_area.update_layout(template=PLOTLY_TEMPLATE, height=320, margin=dict(t=10, b=10, l=10, r=10),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                            yaxis_title="₹ Crore", hovermode="x unified", **COMMON_LAYOUT)
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- TAB 2: STATISTICS ----------
with tab2:
    st.markdown('<div class="section-card"><div class="section-title">Descriptive Statistics</div>', unsafe_allow_html=True)
    stats = fdf[["Sales", "Net_Profit", "OPM_Percent", "EPS"]].agg(["mean", "median", "std"]).T
    stats.columns = ["Mean", "Median", "Std Dev"]
    st.dataframe(stats.style.format("{:.2f}").background_gradient(cmap="GnBu", axis=0), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Quarter-over-Quarter Growth Rates</div>', unsafe_allow_html=True)
    growth_cols = ["Period", "Sales_Growth", "Net_Profit_Growth"]
    gdf = fdf[growth_cols].dropna()
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(x=gdf["Period"], y=gdf["Sales_Growth"], name="Sales Growth %", marker_color=ACCENT_2))
    fig_growth.add_trace(go.Bar(x=gdf["Period"], y=gdf["Net_Profit_Growth"], name="Net Profit Growth %", marker_color=ACCENT))
    fig_growth.update_layout(barmode="group", template=PLOTLY_TEMPLATE, height=360,
                              margin=dict(t=10, b=10, l=10, r=10),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                              yaxis_title="Growth %", **COMMON_LAYOUT)
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    grew = (fdf["Profit_Trend"] == "Profit Grew").sum()
    declined = (fdf["Profit_Trend"] == "Profit Declined").sum()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><div class="section-title">Profit Trend Split</div>', unsafe_allow_html=True)
        fig_pie = px.pie(names=["Profit Grew", "Profit Declined"], values=[grew, declined],
                          color=["Profit Grew", "Profit Declined"],
                          color_discrete_map={"Profit Grew": GREEN, "Profit Declined": RED},
                          hole=0.58)
        fig_pie.update_traces(textfont_size=13, marker=dict(line=dict(color="#05070a", width=2)))
        fig_pie.update_layout(template=PLOTLY_TEMPLATE, height=300, margin=dict(t=10, b=10, l=10, r=10),
                               showlegend=True, **COMMON_LAYOUT)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="section-card" style="padding-top:18px;">
            <div class="section-title">✨ Quick Read</div>
            <p style="color:#D5DAE1; font-size:0.92rem; line-height:1.7;">
            Out of <b>{len(fdf)}</b> quarters shown, profit <b style="color:{GREEN}">grew in {grew}</b>
            and <b style="color:{RED}">declined in {declined}</b>.<br><br>
            Average OPM: <b>{fdf['OPM_Percent'].mean():.2f}%</b><br>
            Average Sales growth (QoQ): <b>{fdf['Sales_Growth'].mean():.2f}%</b><br>
            Average Net Profit growth (QoQ): <b>{fdf['Net_Profit_Growth'].mean():.2f}%</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

# ---------- TAB 3: MODEL COMPARISON ----------
with tab3:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Logistic Regression vs Decision Tree</div>
        <p style="color:#9BA5B4; font-size:0.88rem;">Predicting <code>Profit_Trend</code> from Sales_Growth, OPM_Percent, Interest, and Other_Income.</p>
    </div>
    """, unsafe_allow_html=True)

    if model_results is not None:
        mcols = st.columns(len(model_results))
        for i, (col, (_, row)) in enumerate(zip(mcols, model_results.iterrows())):
            color = ACCENT_2 if i == 0 else ACCENT
            col.markdown(f"""
            <div class="kpi-card" style="animation-delay:{i*0.1:.2f}s">
                <div class="kpi-label">{row['Model']}</div>
                <div class="kpi-value" style="color:{color}">{row['Accuracy']*100:.1f}%</div>
                <span style="color:#9BA5B4; font-size:0.82rem;">on {int(row['Test_Samples'])} test samples</span>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig_model = go.Figure(go.Bar(
            x=model_results["Model"], y=model_results["Accuracy"] * 100,
            marker_color=[ACCENT_2, ACCENT], text=[f"{a*100:.1f}%" for a in model_results["Accuracy"]],
            textposition="outside", marker_line_width=0
        ))
        fig_model.update_layout(template=PLOTLY_TEMPLATE, height=340, margin=dict(t=20, b=10, l=10, r=10),
                                 yaxis_title="Accuracy %", yaxis_range=[0, 100], **COMMON_LAYOUT)
        st.plotly_chart(fig_model, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.warning(
            "⚠️ **Small-sample limitation:** with only ~10 quarterly rows, these accuracy figures "
            "are illustrative only and should not be read as a robust estimate of real predictive power."
        )
    else:
        st.info("Run the Colab notebook first to generate `model_comparison.csv`.")

# ---------- TAB 4: RAW DATA ----------
with tab4:
    st.markdown('<div class="section-card"><div class="section-title">Underlying Quarterly Data</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Filter by period (e.g. 2025)", "")
    display_df = fdf.drop(columns=["Period_dt"]).copy()
    if search:
        display_df = display_df[display_df["Period"].str.contains(search, case=False)]

    st.dataframe(
        display_df.style.format({
            "Sales": "{:,.1f}", "Operating_Profit": "{:,.1f}", "OPM_Percent": "{:.2f}",
            "Other_Income": "{:,.1f}", "Interest": "{:,.1f}", "Depreciation": "{:,.1f}",
            "Profit_Before_Tax": "{:,.1f}", "Net_Profit": "{:,.1f}", "EPS": "{:.2f}",
            "Sales_Growth": "{:.2f}", "Net_Profit_Growth": "{:.2f}",
        }, na_rep="—").background_gradient(subset=["Net_Profit"], cmap="Greens"),
        use_container_width=True, height=380
    )

    csv_download = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered data as CSV", csv_download,
                        file_name="maruti_suzuki_filtered_data.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; padding: 18px 0; color:#6B7480; font-size:0.82rem; border-top:1px solid rgba(255,255,255,0.06); margin-top:10px;">
    📊 {COMPANY_NAME} Financial Dashboard &nbsp;·&nbsp; Data: Screener.in &nbsp;·&nbsp; CA2 Project, MCA Data Science, LPU
</div>
""", unsafe_allow_html=True)
