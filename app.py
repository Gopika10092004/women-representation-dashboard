import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="Women's Representation in Indian Politics",
    page_icon="👩‍💼",
    layout="wide"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
    * { font-family: 'Inter', sans-serif; }
    .flag-strip {
        height: 6px;
        background: linear-gradient(to right, #FF6B00 33.33%, white 33.33%, white 66.66%, #27ae60 66.66%);
        width: 100%; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem; font-weight: 700; color: #1a1a2e;
        text-align: center; margin: 1.5rem 0 0.5rem 0; letter-spacing: -1px;
    }
    .subtitle {
        font-size: 1.1rem; color: #666; text-align: center;
        margin-bottom: 1.5rem; font-weight: 400;
    }
    .live-clock {
        font-size: 1.3rem; font-weight: 600; color: #FF6B00;
        text-align: center; margin-bottom: 1.5rem; font-family: 'Courier New', monospace;
    }
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px; padding: 1.8rem; border: 2px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.3s ease;
        position: relative; overflow: hidden;
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); border-color: #FF6B00; }
    .kpi-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .kpi-label { font-size: 0.9rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
    .kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1a1a2e; font-weight: 700; margin-bottom: 0.3rem; }
    .kpi-change { font-size: 0.85rem; color: #FF6B00; font-weight: 600; }
    .section-divider { display: flex; align-items: center; margin: 2rem 0 1.5rem 0; gap: 1rem; }
    .section-divider-icon { font-size: 1.8rem; }
    .section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #1a1a2e; font-weight: 700; margin: 0; flex-grow: 1; }
    .section-line { height: 3px; background: linear-gradient(to right, #FF6B00, transparent); flex-grow: 1; }
    .chart-container { background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .chart-header {
        background-color: #1a1a2e; color: white; padding: 1rem;
        margin: -1.5rem -1.5rem 1rem -1.5rem; border-radius: 12px 12px 0 0;
        font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700;
    }
    [data-testid="stSidebar"] { background-color: #0f0f1a !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: white !important; }
    .sidebar-section-title {
        color: #FF6B00 !important; font-size: 1.1rem !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 1px !important;
        margin-top: 1.5rem !important; margin-bottom: 0.8rem !important;
    }
    .sidebar-logo { text-align: center; font-size: 3rem; margin-bottom: 1.5rem; margin-top: 1rem; }
    .insights-box {
        background: #ffffff; border-left: 4px solid #FF6B00;
        border-radius: 12px; padding: 1.5rem 2rem; margin: 1.5rem 0;
        font-size: 0.95rem; line-height: 1.8; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .insights-title { color: #FF6B00; font-weight: 700; margin-bottom: 0.8rem; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.06em; }
    .insight-bullet { color: #1a1a2e; margin-bottom: 0.6rem; font-size: 0.97rem; font-weight: 500; }
    .summary-box {
        background: #ffffff; border-radius: 12px; padding: 1.5rem 2rem;
        margin: 1.5rem 0; border: 2px solid #e0e0e0; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .summary-title { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #1a1a2e; font-weight: 700; margin-bottom: 1rem; }
    .summary-box p { color: #1a1a2e; font-size: 0.97rem; font-weight: 400; line-height: 1.7; }
    .countdown-timer {
        background: linear-gradient(135deg, #FF6B00, #FF8C00); color: white;
        border-radius: 8px; padding: 0.8rem; text-align: center;
        font-weight: 700; font-size: 1rem; margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(255,107,0,0.3);
    }
    .footer { text-align: center; color: #999; font-size: 0.9rem; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e0e0e0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="flag-strip"></div>', unsafe_allow_html=True)

PARTY_COLORS = {
    'BJP': '#FF6B00', 'INC': '#00BFFF', 'TMC': '#2ECC71', 'SP': '#E74C3C',
    'BSP': '#9B59B6', 'DMK': '#E67E22', 'AIADMK': '#1ABC9C',
    'AAP': '#F39C12', 'NCP': '#3498DB', 'Others': '#95A5A6'
}

def load_mp_data():
    return {'total_seats': 543, 'women': 74, 'percentage': 13.6}

def load_mla_data():
    data = [
        {'state': 'West Bengal', 'total_seats': 294, 'women': 41, 'percentage': 13.9},
        {'state': 'Rajasthan', 'total_seats': 200, 'women': 27, 'percentage': 13.5},
        {'state': 'Tamil Nadu', 'total_seats': 234, 'women': 29, 'percentage': 12.4},
        {'state': 'Bihar', 'total_seats': 243, 'women': 28, 'percentage': 11.5},
        {'state': 'Uttar Pradesh', 'total_seats': 403, 'women': 44, 'percentage': 10.9},
        {'state': 'Maharashtra', 'total_seats': 288, 'women': 24, 'percentage': 8.3},
        {'state': 'Andhra Pradesh', 'total_seats': 175, 'women': 14, 'percentage': 8.0},
        {'state': 'Karnataka', 'total_seats': 224, 'women': 14, 'percentage': 6.2},
    ]
    return pd.DataFrame(data)

def load_party_data():
    data = [
        {'Party': 'BJP', 'Women_MLAs': 105, 'Women_MPs': 31, 'Total_Women': 136, 'State': 'Multiple'},
        {'Party': 'INC', 'Women_MLAs': 48, 'Women_MPs': 13, 'Total_Women': 61, 'State': 'Multiple'},
        {'Party': 'TMC', 'Women_MLAs': 38, 'Women_MPs': 11, 'Total_Women': 49, 'State': 'West Bengal'},
        {'Party': 'SP', 'Women_MLAs': 20, 'Women_MPs': 5, 'Total_Women': 25, 'State': 'Uttar Pradesh'},
        {'Party': 'DMK', 'Women_MLAs': 15, 'Women_MPs': 5, 'Total_Women': 20, 'State': 'Tamil Nadu'},
        {'Party': 'BSP', 'Women_MLAs': 8, 'Women_MPs': 0, 'Total_Women': 8, 'State': 'Uttar Pradesh'},
        {'Party': 'AIADMK', 'Women_MLAs': 7, 'Women_MPs': 1, 'Total_Women': 8, 'State': 'Tamil Nadu'},
        {'Party': 'AAP', 'Women_MLAs': 12, 'Women_MPs': 0, 'Total_Women': 12, 'State': 'Punjab/Delhi'},
        {'Party': 'NCP', 'Women_MLAs': 5, 'Women_MPs': 1, 'Total_Women': 6, 'State': 'Maharashtra'},
        {'Party': 'Others', 'Women_MLAs': 35, 'Women_MPs': 7, 'Total_Women': 42, 'State': 'Multiple'},
    ]
    return pd.DataFrame(data)

def get_live_time():
    return datetime.now().strftime("%H:%M:%S")

def generate_insights(mp_data, mla_df, party_df):
    insights = []
    insights.append(f"• Women represent {mp_data['percentage']:.1f}% of Lok Sabha members ({mp_data['women']}/{mp_data['total_seats']})")
    best_state = mla_df.loc[mla_df['percentage'].idxmax()]
    insights.append(f"• {best_state['state']} leads with {best_state['percentage']:.1f}% women MLAs ({best_state['women']}/{best_state['total_seats']})")
    top_party = party_df.loc[party_df['Total_Women'].idxmax()]
    insights.append(f"• {top_party['Party']} leads with {int(top_party['Total_Women'])} women representatives across all houses")
    return insights

def create_charts(mp_data, mla_df, selected_state=None):
    if selected_state and selected_state != "All States":
        mla_df = mla_df[mla_df['state'] == selected_state]

    fig_mp = go.Figure(data=[
        go.Bar(name='Men', x=['Lok Sabha'], y=[mp_data['total_seats'] - mp_data['women']], marker_color='#e8e8e8'),
        go.Bar(name='Women', x=['Lok Sabha'], y=[mp_data['women']], marker_color='#FF6B00')
    ])
    fig_mp.update_layout(
        title=dict(text="Women's Representation in Lok Sabha", font=dict(color="#1a1a2e", size=16)),
        barmode='stack', plot_bgcolor='#fafafa', paper_bgcolor='white', height=400,
        font=dict(color="#1a1a2e", family="Inter, sans-serif"),
        legend=dict(font=dict(color="#1a1a2e", size=12)),
        xaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="House", font=dict(color="#1a1a2e", size=13))),
        yaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="Number of MPs", font=dict(color="#1a1a2e", size=13))),
    )

    if selected_state and selected_state != "All States":
        state_data = mla_df.iloc[0] if not mla_df.empty else None
        if state_data is not None:
            fig_mla = go.Figure(data=[
                go.Bar(name='Men', x=[state_data['state']], y=[state_data['total_seats'] - state_data['women']], marker_color='#e8e8e8'),
                go.Bar(name='Women', x=[state_data['state']], y=[state_data['women']], marker_color='#27ae60')
            ])
            fig_mla.update_layout(
                title=dict(text=f"Women's Representation in {state_data['state']} Assembly", font=dict(color="#1a1a2e", size=16)),
                barmode='stack', plot_bgcolor='#fafafa', paper_bgcolor='white', height=400,
                font=dict(color="#1a1a2e", family="Inter, sans-serif"),
                legend=dict(font=dict(color="#1a1a2e", size=12)),
                xaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="State", font=dict(color="#1a1a2e", size=13))),
                yaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="Number of MLAs", font=dict(color="#1a1a2e", size=13))),
            )
        else:
            fig_mla = go.Figure()
            fig_mla.update_layout(title="No data available for selected state")
    else:
        fig_mla = px.bar(mla_df.sort_values('percentage', ascending=False),
                         x='state', y='percentage',
                         title="Women's Representation in State Assemblies (%)",
                         labels={'percentage': 'Women (%)', 'state': 'State'},
                         color='percentage', color_continuous_scale='RdYlBu_r')
        fig_mla.update_layout(
            xaxis_tickangle=-45, plot_bgcolor='#fafafa', paper_bgcolor='white', height=450,
            font=dict(color="#1a1a2e", family="Inter, sans-serif"),
            title=dict(font=dict(color="#1a1a2e", size=16)),
            legend=dict(font=dict(color="#1a1a2e")),
            xaxis=dict(tickfont=dict(color="#1a1a2e", size=11), title=dict(text="State", font=dict(color="#1a1a2e", size=13))),
            yaxis=dict(tickfont=dict(color="#1a1a2e", size=11), title=dict(text="Women (%)", font=dict(color="#1a1a2e", size=13))),
            coloraxis_colorbar=dict(tickfont=dict(color="#1a1a2e"), title=dict(text="Women %", font=dict(color="#1a1a2e")))
        )

    if selected_state and selected_state != "All States":
        state_data = mla_df.iloc[0] if not mla_df.empty else None
        if state_data is not None:
            fig_mla_numbers = go.Figure()
            fig_mla_numbers.add_trace(go.Bar(name='Total Seats', x=[state_data['state']], y=[state_data['total_seats']], marker_color='#e8e8e8'))
            fig_mla_numbers.add_trace(go.Bar(name='Women MLAs', x=[state_data['state']], y=[state_data['women']], marker_color='#27ae60'))
            fig_mla_numbers.update_layout(
                title=dict(text=f"Detailed View: {state_data['state']}", font=dict(color="#1a1a2e", size=16)),
                barmode='group', plot_bgcolor='#fafafa', paper_bgcolor='white', height=400,
                font=dict(color="#1a1a2e", family="Inter, sans-serif"),
                legend=dict(font=dict(color="#1a1a2e", size=12)),
                xaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="State", font=dict(color="#1a1a2e", size=13))),
                yaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="Count", font=dict(color="#1a1a2e", size=13))),
            )
        else:
            fig_mla_numbers = go.Figure()
            fig_mla_numbers.update_layout(title="No data available")
    else:
        fig_mla_numbers = go.Figure()
        fig_mla_numbers.add_trace(go.Bar(name='Total Seats', x=mla_df['state'], y=mla_df['total_seats'], marker_color='#e8e8e8'))
        fig_mla_numbers.add_trace(go.Bar(name='Women MLAs', x=mla_df['state'], y=mla_df['women'], marker_color='#27ae60'))
        fig_mla_numbers.update_layout(
            title=dict(text="Women MLAs by State", font=dict(color="#1a1a2e", size=16)),
            barmode='group', xaxis_tickangle=-45, plot_bgcolor='#fafafa', paper_bgcolor='white', height=450,
            font=dict(color="#1a1a2e", family="Inter, sans-serif"),
            legend=dict(font=dict(color="#1a1a2e", size=12)),
            xaxis=dict(tickfont=dict(color="#1a1a2e", size=11), title=dict(text="State", font=dict(color="#1a1a2e", size=13))),
            yaxis=dict(tickfont=dict(color="#1a1a2e", size=11), title=dict(text="Count", font=dict(color="#1a1a2e", size=13))),
        )

    return fig_mp, fig_mla, fig_mla_numbers

def create_party_charts(party_df, selected_parties=None):
    if selected_parties and len(selected_parties) > 0:
        party_df = party_df[party_df['Party'].isin(selected_parties)]

    fig_party_bar = go.Figure()
    fig_party_bar.add_trace(go.Bar(
        y=party_df['Party'], x=party_df['Total_Women'], orientation='h',
        marker_color=[PARTY_COLORS.get(p, '#95A5A6') for p in party_df['Party']],
        text=party_df['Total_Women'], textposition='outside',
        textfont=dict(color="#1a1a2e", size=12)
    ))
    fig_party_bar.update_layout(
        title=dict(text="Women Representatives by Party", font=dict(color="#1a1a2e", size=16)),
        plot_bgcolor='#fafafa', paper_bgcolor='white', height=400, showlegend=False,
        font=dict(color="#1a1a2e", family="Inter, sans-serif"),
        xaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="Total Women (MLAs + MPs)", font=dict(color="#1a1a2e", size=13))),
        yaxis=dict(tickfont=dict(color="#1a1a2e", size=12), title=dict(text="Party", font=dict(color="#1a1a2e", size=13))),
    )

    fig_party_pie = px.pie(party_df, values='Total_Women', names='Party',
                           title="Party-wise Share of Women Representatives",
                           color='Party', color_discrete_map=PARTY_COLORS, height=400)
    fig_party_pie.update_layout(
        paper_bgcolor='white',
        font=dict(color="#1a1a2e", family="Inter, sans-serif"),
        title=dict(font=dict(color="#1a1a2e", size=16)),
        legend=dict(font=dict(color="#1a1a2e", size=12)),
    )
    fig_party_pie.update_traces(
        textfont=dict(color="#1a1a2e", size=13),
        insidetextfont=dict(color="#ffffff", size=12),
    )

    return fig_party_bar, fig_party_pie

def main():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🏛️</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">📊 Filters</div>', unsafe_allow_html=True)

        mla_df = load_mla_data()
        party_df = load_party_data()

        state_options = ["All States"] + sorted(mla_df['state'].tolist())
        selected_state = st.selectbox("Select State:", options=state_options, key="state_filter")

        party_options = sorted(party_df['Party'].tolist())
        selected_parties = st.multiselect("Select Parties:", options=party_options, default=party_options, key="party_filter")

        st.markdown('<div class="sidebar-section-title">⏱️ Status</div>', unsafe_allow_html=True)
        if "countdown" not in st.session_state:
            st.session_state.countdown = 10
        st.markdown(f'<div class="countdown-timer">Next refresh in {st.session_state.countdown}s</div>', unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">👩‍💼 Women\'s Representation in Indian Politics</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Real-time Analysis of Women in Lok Sabha & State Assemblies</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="live-clock">🕐 Last Updated: {get_live_time()}</div>', unsafe_allow_html=True)

    mp_data = load_mp_data()
    mla_df = load_mla_data()
    party_df = load_party_data()

    filtered_mla_df = mla_df if selected_state == "All States" else mla_df[mla_df['state'] == selected_state]
    filtered_party_df = party_df[party_df['Party'].isin(selected_parties)] if selected_parties else party_df

    # KPI Cards
    st.markdown('<div class="section-divider"><span class="section-divider-icon">📊</span><h2 class="section-title">Key Metrics</h2><div class="section-line"></div></div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">👥</div><div class="kpi-label">Lok Sabha</div><div class="kpi-value">{mp_data["women"]}</div><div class="kpi-change">{mp_data["percentage"]:.1f}% of {mp_data["total_seats"]}</div></div>', unsafe_allow_html=True)
    with col2:
        avg_pct = filtered_mla_df['percentage'].mean() if not filtered_mla_df.empty else 0
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🙋‍♀️</div><div class="kpi-label">State Average</div><div class="kpi-value">{avg_pct:.1f}%</div><div class="kpi-change">Across {len(filtered_mla_df)} states</div></div>', unsafe_allow_html=True)
    with col3:
        total_party_women = filtered_party_df['Total_Women'].sum()
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">👨</div><div class="kpi-label">Party Women Reps</div><div class="kpi-value">{int(total_party_women)}</div><div class="kpi-change">{len(filtered_party_df)} parties selected</div></div>', unsafe_allow_html=True)
    with col4:
        if not filtered_mla_df.empty:
            best_state = filtered_mla_df.loc[filtered_mla_df['percentage'].idxmax()]
            st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📈</div><div class="kpi-label">Top State</div><div class="kpi-value">{best_state["state"]}</div><div class="kpi-change">{best_state["percentage"]:.1f}% women</div></div>', unsafe_allow_html=True)

    # Parliamentary Analysis
    st.markdown('<div class="section-divider"><span class="section-divider-icon">🏛️</span><h2 class="section-title">Parliamentary Analysis</h2><div class="section-line"></div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    fig_mp, fig_mla, fig_mla_numbers = create_charts(mp_data, mla_df, selected_state)
    with col1:
        st.plotly_chart(fig_mp, use_container_width=True)
    with col2:
        st.plotly_chart(fig_mla, use_container_width=True)
    st.plotly_chart(fig_mla_numbers, use_container_width=True)

    # Party Analysis
    st.markdown('<div class="section-divider"><span class="section-divider-icon">🎯</span><h2 class="section-title">Party-wise Analysis</h2><div class="section-line"></div></div>', unsafe_allow_html=True)
    fig_party_bar, fig_party_pie = create_party_charts(party_df, selected_parties)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_party_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_party_pie, use_container_width=True)

    if not filtered_party_df.empty:
        top_party = filtered_party_df.loc[filtered_party_df['Total_Women'].idxmax()]
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🏆</div><div class="kpi-label">Top Party by Women Representatives</div><div class="kpi-value">{top_party["Party"]}</div><div class="kpi-change">{int(top_party["Total_Women"])} women representatives</div></div>', unsafe_allow_html=True)

    # Data Tables
    st.markdown('<div class="section-divider"><span class="section-divider-icon">📋</span><h2 class="section-title">Detailed Data</h2><div class="section-line"></div></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Parliamentary", "State Assemblies", "By Party"])
    with tab1:
        mp_df = pd.DataFrame([mp_data])
        mp_df.index = ['Lok Sabha']
        st.dataframe(mp_df, use_container_width=True)
    with tab2:
        st.dataframe(filtered_mla_df.sort_values('percentage', ascending=False), use_container_width=True)
    with tab3:
        st.dataframe(filtered_party_df.sort_values('Total_Women', ascending=False), use_container_width=True)

    # Insights
    st.markdown('<div class="section-divider"><span class="section-divider-icon">💡</span><h2 class="section-title">Key Insights</h2><div class="section-line"></div></div>', unsafe_allow_html=True)
    insights = generate_insights(mp_data, mla_df, party_df)
    insights_html = '<div class="insights-box"><div class="insights-title">📌 Highlights</div>'
    for insight in insights:
        insights_html += f'<div class="insight-bullet">{insight}</div>'
    insights_html += '</div>'
    st.markdown(insights_html, unsafe_allow_html=True)

    st.markdown('<div class="summary-box"><div class="summary-title">Summary</div><p>This dashboard provides a comprehensive analysis of women\'s political representation in India. It tracks real-time data on women MLAs (State Assembly Members) and MPs (Parliament Members), organized by state and political party. The data updates automatically every 10 seconds to reflect any changes.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">📊 Data Sources: mla_data.csv • mp_data.csv • party_data.csv | 🔄 Auto-refresh: Every 10 seconds</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()

    elapsed = time.time() - st.session_state.last_refresh
    if elapsed >= 10:
        st.session_state.last_refresh = time.time()
        st.cache_data.clear()
        st.session_state.countdown = 10
        time.sleep(0.1)
        st.rerun()
    else:
        st.session_state.countdown = max(0, int(10 - elapsed))
        time.sleep(0.5)
        st.rerun()
