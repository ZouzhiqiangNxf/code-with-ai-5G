# 🚀 5G 信号可视化看板 - Code with AI 挑战赛

## 📋 项目概述

这是一个基于 **Streamlit + PyDeck + Plotly** 构建的交互式 **5G 信号强度实时监测系统**。通过 AI 代码生成工具（GitHub Copilot），将枯燥的 5G 路测数据转化为高大上的交互式 Web 看板。

### 🎯 核心功能（基础关卡 ✅ 已完成）

#### 1️⃣ **数据加载**
- ✅ 使用 `pandas` 读取 `data/signal_samples.csv` CSV 数据
- ✅ 采用 `@st.cache_data` 装饰器优化性能，数据仅加载一次
- ✅ 成功加载 **500+ 条** 5G 信号采样数据

#### 2️⃣ **交互式信号热力地图**
- ✅ 基于 **PyDeck ScatterplotLayer** 的交互式地图
- ✅ **信号强度分色逻辑**：
  ```
  > -90 dBm  → 🟢 绿色 (优秀信号)
  -90~-100   → 🟡 黄色 (良好信号)
  -100~-110  → 🟠 橙色 (中等信号)
  < -110     → 🔴 红色 (较差信号)
  ```
- ✅ **鼠标悬停 Tooltip**：显示完整信号信息（RSRP、SINR、频段、基站ID、终端类型、下载速率）
- ✅ **自动地图中心计算**：地图中心为所有数据点的平均经纬度

#### 3️⃣ **数据概览统计图表**
- ✅ **柱状图**：各频段 (n28, n41, n78) 基站数量分布
- ✅ **甜甜圈图**：不同终端类型占比（Smartphone, CPE, IoT）
- ✅ **统计卡片**：总样本数、基站数、平均信号强度、平均信噪比

#### 4️⃣ **增强信息展示**
- ✅ **直方图**：RSRP 分布分析（30 个分箱）
- ✅ **数据预览表格**：前 10 条记录查看
- ✅ **整体布局**：顶部指标、中部地图、下方图表

---

## 🛠 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| **Streamlit** | ≥1.28.0 | Web 框架 |
| **Pandas** | ≥2.0.0 | 数据处理 |
| **PyDeck** | ≥0.8.0 | 地图可视化 |
| **Plotly** | ≥5.0.0 | 交互式图表 |
| **NumPy** | ≥1.24.0 | 数值计算 |
| **PyArrow** | ≥12.0.0 | 高性能数据处理 |

---

## 📁 项目结构

```
code-with-ai-5G/
├── app.py                          # 主应用程序 (250+ 行)
├── requirements.txt                # 依赖文件
├── data/
│   └── signal_samples.csv          # 500 条 5G 信号采样数据
├── AI_PROMPTS.md                   # AI 交互日志（核心验收项）
└── README.md                       # 项目说明文档（本文件）
```

### 📊 数据文件说明 (`signal_samples.csv`)

```csv
Latitude      - 采样点纬度 (31.18~31.28)
Longitude     - 采样点经度 (121.42~121.52)
CellID        - 基站 ID (1000~2000)
Band          - 频段标识 (n28, n41, n78)
RSRP_dBm      - 信号接收功率 (-119 ~ -70 dBm)
SINR_dB       - 信噪比 (-5 ~ 29.9 dB)
TerminalType  - 终端类型 (Smartphone, CPE, IoT)
Download_Mbps - 下载速率 (13.59 ~ 998.79 Mbps)
```

---

## 🚀 快速开始

### 前置要求
- Python 3.8 或更高版本
- pip 或 conda 包管理工具

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/ZouzhiqiangNxf/code-with-ai-5G.git
cd code-with-ai-5G

# 2. 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
streamlit run app.py
```

### 运行结果

应用启动后，浏览器会自动打开：`http://localhost:8501`

---

## 📖 功能使用指南

### 1. 👁️ 查看地图
- 左键拖拽：移动地图
- 滚轮或 +/- 按钮：缩放地图
- 鼠标悬停：查看具体信号数据

### 2. 📊 查看图表
- **频段分布柱状图**：比较不同频段基站数量
- **终端类型甜甜圈图**：了解用户设备类型分布
- **RSRP 分布直方图**：观察信号强度的分布模式

### 3. 📋 数据预览
- 表格显示前 10 条样本数据
- 支持交互式滚动和列排序

---

## 🤖 AI 代码生成过程

本项目完全通过 **GitHub Copilot** AI 代码生成完成。详见 `AI_PROMPTS.md` 文件，包含 5 个核心 Prompt 和生成的代码片段。

---

## 📈 数据统计概览

```
📊 总数据量：500 条采样记录
🏢 基站覆盖：210+ 个独立基站 ID
📡 频段覆盖：3 种频段 (n28, n41, n78)
📱 终端类型：3 种 (Smartphone, CPE, IoT)

信号强度范围：-119.70 ~ -70.02 dBm
平均信号强度：-93.46 dBm
下载速率范围：13.59 ~ 998.79 Mbps
```

---

## 📝 提交清单

### ✅ 基础关卡提交件 (Green Level)

- [x] **📂 源代码**：`app.py` + `requirements.txt`
- [x] **📄 项目文档**：本 README.md
- [x] **🤖 AI 交互日志**：`AI_PROMPTS.md`
- [ ] **📸 运行截图**：需补充 2-3 张

---

## 🔖 Git 进度打卡

```bash
git tag basic-done
git push origin basic-done
```

---

## 🟡 进阶功能计划

- [ ] 侧边栏联动筛选（Band、RSRP 范围、终端类型）
- [ ] 3D 地图可视化（PyDeck ColumnLayer）
- [ ] 单元测试（pytest）

---

**🚀 Built with ❤️ using Code with AI** | *Last Updated: 2026-05-08*
