#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import json
import pandas as pd
import numpy as np
import os
from PIL import Image

# 基础路径设置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 1. 页面配置与科技风 CSS
# ==========================================
st.set_page_config(
    page_title="GreenLink 绿链 | 智能ESG风险与金融平台",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 科技风 CSS 样式
st.markdown("""
<style>
    /* 全局深色背景适配 */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* 标题样式 - 赛博风格 */
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00ff41, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }
    
    .sub-header {
        font-family: 'Roboto', sans-serif;
        font-size: 1.2rem;
        color: #00f2ff;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }

    /* 科技感卡片 */
    .tech-card {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-left: 4px solid #00ff41;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .tech-card:hover {
        border-color: #00f2ff;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }

    /* 风险标签 */
    .risk-tag {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-family: monospace;
    }
    .tag-high { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
    .tag-low { background-color: rgba(0, 255, 65, 0.1); color: #00ff41; border: 1px solid #00ff41; }
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #374151;
    }
    
    /* 指标样式 */
    div[data-testid="stMetricValue"] {
        font-family: 'Courier New', monospace;
        color: #00f2ff !important;
    }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown('<p class="main-header">🌿 GREENLINK_OS v2.0</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">>> 卫星遥感 · 舆情挖掘 · 绿色金融 <<</p>', unsafe_allow_html=True)

# ==========================================
# 2. 数据加载与处理
# ==========================================
companies = {
    "FGV Holdings Berhad": {"filename": "FGV.json", "type": "上游供应商", "position": "种植商", "code": "FGV"},
    "IOI Corporation": {"filename": "IOI.json", "type": "上游供应商", "position": "种植商", "code": "IOI"},
    "中粮集团 (COFCO)": {"filename": "COFCO.json", "type": "中游加工商", "position": "核心企业", "code": "COFCO"}
}

st.sidebar.markdown("### 📡 目标锁定")
selected_company = st.sidebar.selectbox("Select Target", list(companies.keys()))
company_info = companies[selected_company]

# 模拟加载数据
@st.cache_data
def load_data(filename):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    if not os.path.exists(file_path):
        return get_sample_data(), False
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        is_cofco = 'COFCO' in filename
        return data, is_cofco

def get_sample_data():
    return {
        "company": "示例公司",
        "environment": {"risk_level": "低风险", "risk_score": 25},
        "social": {"risk_level": "高风险", "risk_score": 75},
        "supply_chain": {}
    }

try:
    data, is_cofco = load_data(company_info['filename'])
except:
    data, is_cofco = get_sample_data(), False

# 动态计算综合评分 (用于金融模块)
env_score = data.get('environment', {}).get('risk_score', 50)
soc_score = data.get('social', {}).get('risk_score', 50)
total_score = (env_score + soc_score) / 2
credit_rating = "AAA" if total_score < 30 else ("AA" if total_score < 50 else "B")

# ==========================================
# 3. 主界面 Tabs
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 风险监测", 
    "🔗 链式穿透", 
    "💰 绿色金融",
    "📱 消费终端"
])

# ---------- TAB 1: 风险监测 (Tech Style) ----------
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="tech-card">
            <h3>{data.get('company')}</h3>
            <p>ID: {company_info['code']}_9928</p>
            <p>Role: {company_info['position']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 仪表盘风格指标
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("E-Score (环境)", f"{env_score}", delta="-2.5 (WoW)", delta_color="inverse")
        with col_m2:
            st.metric("S-Score (社会)", f"{soc_score}", delta="+5.1 (WoW)", delta_color="inverse")
            
    with col2:
        # 使用 Streamlit 图表代替纯文本
        st.markdown("##### 🛰️ 实时监控数据流")
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) + [env_score/10, soc_score/10],
            columns=['环境波动', '舆情波动']
        )
        st.line_chart(chart_data, color=["#00ff41", "#00f2ff"], height=200)

    st.markdown("---")
    
    # 卫星与舆情详情
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌍 SATELLITE_LINK // Sentinel-2")
        env_analysis = data.get('environment', {}).get('analysis', {})
        st.info(f"📡 分析方法: {env_analysis.get('method', 'AI遥感反演')}")
        
        # 图片展示逻辑 (保持原逻辑，换样式)
        if not is_cofco:
            evidence = env_analysis.get('evidence', {})
            img_path = os.path.join(BASE_DIR, evidence.get('satellite_image_after', ''))
            if os.path.exists(img_path):
                st.image(img_path, caption="最新遥感影像", use_column_width=True)
            else:
                st.markdown("```\n[SYSTEM] 正在请求卫星影像数据...\n[ERROR] 影像未缓存\n```")
        else:
            st.markdown("```python\n# 中粮集团环境数据\nstatus = 'COMPLIANT'\ncarbon_target = '2030 Peak'\n```")
            
    with c2:
        st.markdown("#### 📢 SOCIAL_LISTENING // Global Web")
        social = data.get('social', {})
        events = social.get('key_events', [])
        
        if events:
            for event in events[:3]:
                severity = event.get('severity', '中')
                color = "#ef4444" if severity in ['高', '严重'] else "#f59e0b"
                st.markdown(f"""
                <div style="border-left: 3px solid {color}; padding-left: 10px; margin-bottom: 10px; background: rgba(255,255,255,0.05);">
                    <small style="color: #9ca3af">{event.get('date', 'N/A')}</small><br>
                    <span style="color: #e0e0e0">{event.get('event', '')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("暂无重大风险事件")

# ---------- TAB 2: 链式穿透 ----------
with tab2:
    st.header("🔗 供应链风险传导网络")
    
    if is_cofco:
        # Mermaid 流程图 (需要安装 streamlit-mermaid 或直接用 markdown 模拟)
        st.markdown("""
        ```mermaid
        graph LR
            A[FGV Holdings] -- 高风险(劳工) --> B(中粮集团)
            B -- 潜在合规风险 --> C{欧美市场}
            C -- 禁止准入 --> D[损失预估]
            
            style A fill:#300,stroke:#f00,stroke-width:2px
            style B fill:#330,stroke:#ff0,stroke-width:2px
            style C fill:#003,stroke:#0ff,stroke-width:2px
        ```
        *注：风险传导路径可视化*
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🚨 上游风险源")
            suppliers = data.get('supply_chain', {}).get('upstream', {}).get('suppliers', [])
            for s in suppliers:
                risk_color = "red" if "高" in s.get('risk_status', '') else "green"
                st.markdown(f"**{s['name']}**: :{risk_color}[{s['risk_status']}]")
        
        with col2:
            st.markdown("### 🛡️ 阻断策略")
            st.markdown("""
            1. **动态调整采购比例**：立即降低 FGV 采购份额至 10% 以下。
            2. **替代供应商激活**：启动 IOI Corporation (低风险) 备选方案。
            3. **合规防火墙**：针对美国 CBP 要求，建立独立仓储，物理隔离风险原料。
            """)
            
    else:
        st.info("当前视图为供应商视角：展示自身风险如何影响下游客户。")
        st.metric("下游客户流失风险", "High", "CBP禁令影响")

# ---------- TAB 3: 绿色金融 (新增核心模块) ----------
with tab3:
    st.markdown("## 💰 绿色金融与风险定价")
    st.caption("基于 ESG 另类数据的金融价值转化")
    
    # 分两列：左侧计算器，右侧授信分析
    fin_col1, fin_col2 = st.columns([1, 1])
    
    with fin_col1:
        st.markdown("### 🏦 ESG 挂钩贷款模拟器")
        st.markdown("""
        <div class="tech-card">
            基于企业的实时 ESG 评分，计算可获得的绿色贷款利率优惠。
        </div>
        """, unsafe_allow_html=True)
        
        loan_amount = st.number_input("贷款金额 (万元)", min_value=100, value=5000, step=100)
        base_rate = 4.35  # 基础LPR
        
        # 逻辑：分数越低(风险越低)，优惠越大。注意：原数据中分数是风险分，低分=好
        # 假设：0-30分(优)优惠 50bp, 30-50分(良)优惠 20bp
        discount_bp = 0
        if total_score <= 30:
            discount_bp = 50
            rating_label = "🌿 深绿企业 (Deep Green)"
        elif total_score <= 50:
            discount_bp = 20
            rating_label = "🍃 浅绿企业 (Light Green)"
        else:
            discount_bp = 0
            rating_label = "🍂 棕色企业 (Transition)"
            
        final_rate = base_rate - (discount_bp / 100)
        annual_saving = loan_amount * (discount_bp / 10000)
        
        st.success(f"当前评级: **{rating_label}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("基础利率", f"{base_rate}%")
        c2.metric("ESG 优惠", f"-{discount_bp} bp", delta_color="normal")
        c3.metric("执行利率", f"{final_rate:.2f}%", delta_color="inverse")
        
        st.markdown(f"### 💸 预计年利息节省: **{annual_saving:,.0f} 万元**")
        
    with fin_col2:
        st.markdown("### 📉 财务风险量化")
        st.markdown("""
        <div class="tech-card">
            预估因 ESG 合规问题可能导致的潜在财务损失。
        </div>
        """, unsafe_allow_html=True)
        
        if total_score > 60:
            potential_loss = loan_amount * 0.15 # 假设高风险导致15%营收受损
            st.error(f"⚠️ 风险敞口极高")
            st.progress(85)
            st.write("主要风险源：")
            st.markdown("- 🇪🇺 **欧盟 EUDR 违规罚款**: 营收的 4%")
            st.markdown("- 🇺🇸 **货物滞留/退运成本**: 约 200 万 USD")
            st.markdown("- 📉 **品牌声誉受损**: 估值下调 5-10%")
            
            st.metric("潜在财务损失预估", f"¥ {potential_loss/10000:,.1f} 亿", delta="-15% 营收", delta_color="inverse")
        else:
            st.success("✅ 财务风险可控")
            st.progress(15)
            st.write("当前 ESG 表现有助于提升估值溢价。")
            st.metric("绿色溢价 (Greenium)", "+ 2.5%", "融资成本优势")

    st.markdown("---")
    
    # 供应链金融部分
    st.subheader("⛓️ 供应链金融 (Supply Chain Finance)")
    st.markdown("基于绿链数据的**动态授信额度**调整模型")
    
    scf_df = pd.DataFrame({
        "供应商": ["FGV Holdings", "IOI Corp", "Sime Darby", "Wilmar"],
        "ESG 风险分": [75, 25, 30, 40],
        "基础授信 (万)": [1000, 1000, 1000, 1000]
    })
    
    # 动态计算
    scf_df["调整系数"] = scf_df["ESG 风险分"].apply(lambda x: 0.5 if x > 60 else (1.2 if x < 30 else 1.0))
    scf_df["动态授信 (万)"] = scf_df["基础授信 (万)"] * scf_df["调整系数"]
    
    st.dataframe(
        scf_df.style.highlight_max(axis=0, color='#1f2937', subset=['动态授信 (万)'])
              .format({"动态授信 (万)": "{:.0f}"}),
        use_container_width=True
    )

# ---------- TAB 4: 消费终端 (原 B2C) ----------
with tab3: # 这里有个小bug, tab4其实是变量名, 之前定义了tab1-4
    pass # 之前tab3里的内容移到这里，但因为tab变量作用域问题，直接用下面代码

with tab4:
    st.header("📱 B2C 信任溯源")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=GreenLink_Demo", caption="扫码查看区块链证书")
    with col2:
        st.markdown("""
        ### 消费者视角的信任标签
        
        - **碳足迹**: 1.2kg CO2e / 瓶 (低于行业平均 20%)
        - **产地**: 马来西亚柔佛州 (卫星验证无毁林)
        - **劳工**: 符合 ILO 核心公约
        """)
        st.success("✅ 该产品已通过 GreenLink 绿色认证")

# 侧边栏底部
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 GreenLink Tech | Powered by Sentinel-2 & AI")
