import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide", initial_sidebar_state="expanded")

st.title("📡 5G 信号可视化看板")
st.markdown("---")
st.markdown("### 实时信号强度监测系统 | Real-time Signal Strength Monitoring")

# ==========================================
# 第一步：数据加载
# ==========================================
@st.cache_data
def load_data():
    """
    从 CSV 文件加载 5G 信号采样数据
    Returns:
        pd.DataFrame: 包含经纬度、小区ID、频段、信号强度等信息的数据框
    """
    df = pd.read_csv('data/signal_samples.csv')
    return df

try:
    df = load_data()
    st.success(f"✅ 成功加载 {len(df)} 条数据记录")
except FileNotFoundError:
    st.error("❌ 未找到 data/signal_samples.csv 文件")
    st.stop()

# ==========================================
# 第二步：信号强度分级与着色逻辑
# ==========================================
def get_signal_color(rsrp):
    """
    根据信号强度 (RSRP_dBm) 返回对应颜色
    信号强度分级标准：
    - > -90 dBm: 绿色 (优秀)
    - -90 ~ -100 dBm: 黄色 (良好)
    - -100 ~ -110 dBm: 橙色 (中等)
    - < -110 dBm: 红色 (较差)
    
    Args:
        rsrp (float): 信号强度值 (dBm)
    Returns:
        list: RGB 颜色值 [R, G, B, A]
    """
    if rsrp > -90:
        return [0, 255, 0, 200]  # 绿色
    elif rsrp > -100:
        return [255, 255, 0, 200]  # 黄色
    elif rsrp > -110:
        return [255, 165, 0, 200]  # 橙色
    else:
        return [255, 0, 0, 200]  # 红色

# 为数据添加颜色列
df['color'] = df['RSRP_dBm'].apply(get_signal_color)

# ==========================================
# 第三步：信息统计
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 总样本数", len(df))
with col2:
    st.metric("📍 基站数量", df['CellID'].nunique())
with col3:
    st.metric("📈 平均信号强度", f"{df['RSRP_dBm'].mean():.2f} dBm")
with col4:
    st.metric("🎯 信噪比均值", f"{df['SINR_dB'].mean():.2f} dB")

st.markdown("---")

# ==========================================
# 第四步：交互式信号热力地图
# ==========================================
st.subheader("🗺️ 信号强度分布地图")

# 定义地图样式和初始视图
midpoint = (
    np.average(df['Latitude']),
    np.average(df['Longitude'])
)

# 使用 PyDeck 创建高级可视化地图
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position=['Longitude', 'Latitude'],
    get_color='color',
    get_radius=100,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=midpoint[0],
    longitude=midpoint[1],
    zoom=12,
    bearing=0,
    pitch=0,
)

tool_tip = {
    'html': '<b>信号信息</b><br/>'
            '信号强度: <b>{RSRP_dBm}</b> dBm<br/>'
            '信噪比: <b>{SINR_dB}</b> dB<br/>'
            '频段: <b>{Band}</b><br/>'
            '基站ID: <b>{CellID}</b><br/>'
            '终端类型: <b>{TerminalType}</b><br/>'
            '下载速率: <b>{Download_Mbps:.2f}</b> Mbps',
    'style': {'backgroundColor': 'steelblue', 'color': 'white'}
}

map_fig = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tool_tip,
    map_style='mapbox://styles/mapbox/light-v11'
)

st.pydeck_chart(map_fig)

st.markdown("---")

# ==========================================
# 第五步：数据概览图表
# ==========================================

# 分为两列布局
chart_col1, chart_col2 = st.columns(2)

# 图表 1: 各频段基站数量
with chart_col1:
    st.subheader("📊 各频段基站分布")
    band_counts = df['Band'].value_counts().sort_values(ascending=False)
    fig_band = px.bar(
        x=band_counts.index,
        y=band_counts.values,
        labels={'x': '频段 (Band)', 'y': '基站数量'},
        title="基站频段统计",
        color=band_counts.values,
        color_continuous_scale='viridis'
    )
    fig_band.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_band, use_container_width=True)

# 图表 2: 终端类型占比
with chart_col2:
    st.subheader("🎯 终端类型分布")
    terminal_counts = df['TerminalType'].value_counts()
    fig_terminal = px.pie(
        values=terminal_counts.values,
        names=terminal_counts.index,
        title="终端类型占比",
        hole=0.3
    )
    fig_terminal.update_layout(height=400)
    st.plotly_chart(fig_terminal, use_container_width=True)

st.markdown("---")

# ==========================================
# 第六步：信号强度分布直方图
# ==========================================
st.subheader("📈 信号强度分布直方图")

fig_rsrp = go.Figure()
fig_rsrp.add_trace(go.Histogram(
    x=df['RSRP_dBm'],
    nbinsx=30,
    name='RSRP 分布',
    marker_color='rgba(100, 150, 250, 0.7)',
    marker_line=dict(color='rgba(100, 150, 250, 1)', width=1)
))

fig_rsrp.update_layout(
    title='信号强度 (RSRP_dBm) 分布分析',
    xaxis_title='信号强度 (dBm)',
    yaxis_title='样本数量',
    hovermode='x unified',
    height=400,
    template='plotly_white'
)

st.plotly_chart(fig_rsrp, use_container_width=True)

st.markdown("---")

# ==========================================
# 第七步：数据预览表格
# ==========================================
st.subheader("📋 数据样本预览 (前 10 条)")
st.dataframe(
    df[['Latitude', 'Longitude', 'CellID', 'Band', 'RSRP_dBm', 'SINR_dB', 'TerminalType', 'Download_Mbps']].head(10),
    use_container_width=True
)

# ==========================================
# 页脚
# ==========================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 12px;'>"
    "🚀 <b>Code with AI</b> 5G Signal Visualization Dashboard | "
    "Built with Streamlit & PyDeck<br/>"
    "Data Source: signal_samples.csv | Last Updated: 2026-05-08"
    "</div>",
    unsafe_allow_html=True
)
