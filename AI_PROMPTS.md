# 🤖 AI PROMPTS 交互日志

## GitHub Copilot 与 AI 代码生成的交互记录

### 基础关卡 (Green Level) - 2026-05-08

#### Prompt 1: 数据加载
```
"请帮我使用 pandas 读取 data/signal_samples.csv 文件，并用 @st.cache_data 装饰器缓存数据加载函数，确保数据只加载一次。"
```

**AI 生成代码片段：**
```python
@st.cache_data
def load_data():
    df = pd.read_csv('data/signal_samples.csv')
    return df

df = load_data()
st.success(f"✅ 成功加载 {len(df)} 条数据记录")
```

---

#### Prompt 2: 信号强度分级与着色
```
"根据信号强度 RSRP_dBm 的值，定义一个函数将其映射到不同颜色：
- > -90 dBm: 绿色 (优秀)
- -90 ~ -100 dBm: 黄色 (良好)
- -100 ~ -110 dBm: 橙色 (中等)
- < -110 dBm: 红色 (较差)
返回 RGB 颜色值用于 PyDeck 可视化。"
```

**AI 生成代码片段：**
```python
def get_signal_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0, 200]  # 绿色
    elif rsrp > -100:
        return [255, 255, 0, 200]  # 黄色
    elif rsrp > -110:
        return [255, 165, 0, 200]  # 橙色
    else:
        return [255, 0, 0, 200]  # 红色

df['color'] = df['RSRP_dBm'].apply(get_signal_color)
```

---

#### Prompt 3: 交互式地图实现
```
"使用 PyDeck 创建一个交互式地图，显示所有数据点，其中：
1. 点的颜色基于信号强度（使用前面定义的颜色函数）
2. 地图中心应该是所有数据点的平均经纬度
3. 添加 tooltip 显示鼠标悬停时的信号信息（RSRP、SINR、频段、基站ID等）
4. 缩放级别设置为 12，使用 light 地图样式"
```

**AI 生成代码片段：**
```python
midpoint = (
    np.average(df['Latitude']),
    np.average(df['Longitude'])
)

layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position=['Longitude', 'Latitude'],
    get_color='color',
    get_radius=100,
    pickable=True,
    auto_highlight=True,
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
```

---

#### Prompt 4: 数据概览图表
```
"使用 Plotly 创建两个图表：
1. 柱状图：显示各频段���基站数量分布，颜色使用 viridis 渐变
2. 饼图（甜甜圈图）：显示不同终端类型的占比（Smartphone、CPE、IoT）
布局应该是两列，每个图表高度 400px。"
```

**AI 生成代码片段：**
```python
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    band_counts = df['Band'].value_counts().sort_values(ascending=False)
    fig_band = px.bar(
        x=band_counts.index,
        y=band_counts.values,
        title="基站频段统计",
        color=band_counts.values,
        color_continuous_scale='viridis'
    )
    st.plotly_chart(fig_band, use_container_width=True)

with chart_col2:
    terminal_counts = df['TerminalType'].value_counts()
    fig_terminal = px.pie(
        values=terminal_counts.values,
        names=terminal_counts.index,
        title="终端类型占比",
        hole=0.3
    )
    st.plotly_chart(fig_terminal, use_container_width=True)
```

---

#### Prompt 5: 额外增强 - 信号强度分布直方图
```
"再添加一个信号强度 (RSRP_dBm) 的分布直方图，使用 Plotly 的 go.Histogram，
设置 nbinsx=30，颜色为半透明蓝色 rgba(100, 150, 250, 0.7)。"
```

**AI 生成代码片段：**
```python
fig_rsrp = go.Figure()
fig_rsrp.add_trace(go.Histogram(
    x=df['RSRP_dBm'],
    nbinsx=30,
    name='RSRP 分布',
    marker_color='rgba(100, 150, 250, 0.7)',
))
st.plotly_chart(fig_rsrp, use_container_width=True)
```

---

## 总结

✅ **基础关卡完成清单：**
- [x] 数据加载：使用 pandas 读取 CSV
- [x] 信号热力/散点地图：PyDeck 交互式地图，点按 RSRP 变色
- [x] 数据概览图表：频段分布柱图 + 终端类型饼图
- [x] 额外功能：统计指标卡片、数据预览表格、信号分布直方图

**运行方法：**
```bash
pip install -r requirements.txt
streamlit run app.py
```

🚀 **下一步：进阶关卡**
- 侧边栏筛选功能
- 3D 地图可视化
- 单元测试
