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
# 1. 页面配置与高对比度 CSS
# ==========================================
st.set_page_config(
    page_title="GreenLink 绿链 | 智能ESG风险与金融平台",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 高清晰度科技风 CSS
st.markdown("""
<style>
    /* 1. 全局背景与字体 - 白色主调 + 绿色点缀 */
    .stApp {
        background-color: #f8fff8 !important;   /* 浅绿色调白底 */
        color: #1a3c1a !important;              /* 深绿色文字 */
    }
    .stMarkdown, .stText, p, div, label {
        color: #1a3c1a !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 2. 标题 - 更醒目的绿色科技风 */
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00b140 !important;              /* 更鲜艳的绿色 */
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 177, 64, 0.4);
        letter-spacing: -2px;
        text-transform: uppercase;
    }
    .sub-header {
        font-family: sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        color: #00c8a0 !important;              /* 青绿色 */
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 2px;
        border-bottom: 2px solid #e0f0e0;
        padding-bottom: 20px;
    }

    /* 3. 卡片样式 - 白色卡片 + 绿色左边框 */
    .tech-card {
        background-color: #ffffff !important;
        border: 1px solid #d0e8d0 !important;
        border-left: 6px solid #00b140 !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0, 177, 64, 0.12);
    }
    .tech-card h3 { 
        color: #00b140 !important; 
        margin-top: 0; 
        font-weight: 800; 
    }

    /* 4. 侧边栏 - 浅绿色 */
    section[data-testid="stSidebar"] {
        background-color: #f0f9f0 !important;
        border-right: 1px solid #c0e0c0;
    }
    section[data-testid="stSidebar"] * {
        color: #1a3c1a !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a3c1a !important;
        border: 1px solid #a0d0a0 !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #ffffff !important;
        border-color: #c0e0c0 !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #00b140 !important;
        color: #ffffff !important;
    }

    /* 5. 评分图例 - 适配浅色 */
    .score-legend-compact {
        background: #f8fff8;
        border: 1px solid #c0e0c0;
        padding: 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        height: 100%;
    }
    .legend-row {
        display: flex;
        align-items: center;
        margin-bottom: 3px;
        color: #1a3c1a;
    }

    /* 6. Metric 指标 */
    div[data-testid="stMetricLabel"] { 
        color: #006633 !important; 
        font-size: 0.85rem !important; 
    }
    div[data-testid="stMetricValue"] { 
        color: #00b140 !important; 
        font-family: 'Courier New', monospace; 
        font-size: 1.8rem !important; 
    }

    /* 7. 产品溯源卡片 & 协议框 - 适配浅色 */
    .product-trace-card {
        background: linear-gradient(145deg, #ffffff, #f0fff0);
        border: 2px solid #00b140;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 177, 64, 0.15);
    }
    .protocol-box {
        background: #f8fff8;
        border: 1px solid #a0d0a0;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .protocol-title { 
        color: #00b140; 
        font-weight: bold; 
        border-bottom: 1px solid #c0e0c0; 
        padding-bottom: 5px; 
        margin-bottom: 5px; 
    }

    /* 8. 供应链箭头框 */
    .chain-box {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin: 5px;
        background: #ffffff;
        border: 2px solid #00b140;
    }

    /* 9. Expander 折叠面板 */
    details[data-testid="stExpander"], div[data-testid="stExpander"] {
        background-color: #f8fff8 !important;
        border: 1px solid #c0e0c0 !important;
        border-radius: 8px !important;
    }
    details[data-testid="stExpander"] summary {
        color: #00b140 !important;
        background-color: #f0f9f0 !important;
    }

    /* 10. 按钮 - 绿色科技风 */
    button[kind="primary"] {
        background-color: #00b140 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
    }
    button[kind="primary"]:hover {
        background-color: #00c8a0 !important;
        box-shadow: 0 0 15px rgba(0, 200, 160, 0.5) !important;
    }

    /* 额外小优化：让所有链接和危险提示也更协调 */
    .source-link-btn {
        color: #00b140 !important;
        border: 1px solid #00b140;
    }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown('<div class="main-header">GREENLINK_OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">>> SATELLITE · INTELLIGENCE · FINANCE <<</div>', unsafe_allow_html=True)

# ==========================================
# 2. 数据加载
# ==========================================
companies = {
    "FGV Holdings Berhad": {"filename": "FGV.json", "type": "上游供应商", "position": "种植商", "code": "FGV"},
    "IOI Corporation": {"filename": "IOI.json", "type": "上游供应商", "position": "种植商", "code": "IOI"},
    "中粮集团 (COFCO)": {"filename": "COFCO.json", "type": "中游加工商", "position": "核心企业", "code": "COFCO"}
}

st.sidebar.markdown("### 📡 目标锁定 (TARGET)")
selected_company = st.sidebar.selectbox("选择企业对象", list(companies.keys()))
company_info = companies[selected_company]

@st.cache_data
def load_data(filename):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    if not os.path.exists(file_path): return get_sample_data(), False
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data, 'COFCO' in filename

def get_sample_data():
    return {"company": "Demo", "environment": {"risk_score": 25}, "social": {"risk_score": 75}, "supply_chain": {}}

try:
    data, is_cofco = load_data(company_info['filename'])
except:
    data, is_cofco = get_sample_data(), False

env_score = data.get('environment', {}).get('risk_score', 50)
soc_score = data.get('social', {}).get('risk_score', 50)
total_score = (env_score + soc_score) / 2

# ==========================================
# 3. 主界面 Tabs
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 风险监测 (MONITOR)", 
    "🔗 链式穿透 (CHAIN)", 
    "💰 绿色金融 (FINANCE)",
    "📱 消费终端 (CONSUMER)"
])

# ---------- TAB 1: 风险监测 ----------
with tab1:
    col_header, col_chart = st.columns([2, 1])
    
    with col_header:
        st.markdown(f"""
        <div class="tech-card">
            <h3>{data.get('company')}</h3>
            <p style="color:#AAA;"><strong>ID:</strong> {company_info['code']}_9928 &nbsp;|&nbsp; <strong>Role:</strong> {company_info['position']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### ⚔️ 评级体系对比 (VS Traditional)")
        trad_data = data.get('traditional_rating') or data.get('social', {}).get('traditional_rating')
        rating_val = trad_data.get('rating', trad_data.get('msci', 'N/A')) if isinstance(trad_data, dict) else (trad_data if isinstance(trad_data, str) else 'N/A')
            
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#1a1a1a; padding:15px; border-left:4px solid #666; border-radius:4px;">
                <div style="color:#888; font-size:0.8rem;">🏢 传统评级 (MSCI)</div>
                <div style="font-size: 2rem; font-weight:bold; color: #BBB;">{rating_val}</div>
                <div style="color:#666; font-size:0.8rem;">❌ 评级模糊</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div style="background:#1a1a1a; padding:15px; border-left:4px solid #00FF41; border-radius:4px;">
                <div style="color:#888; font-size:0.8rem;">🌿 绿链 GreenLink</div>
                <div style="font-size: 1.1rem; font-weight:bold; color: #00FF41;">E/S 分离评分</div>
                <div style="color:#EEE; font-size:0.8rem;">Env: {env_score} | Soc: {soc_score}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("##### 核心指标 (Core Metrics)")
        
        c_metrics, c_legend = st.columns([1.2, 1])
        with c_metrics:
            st.metric("E-Score", f"{env_score}", delta="-2.5", delta_color="inverse")
            st.metric("S-Score", f"{soc_score}", delta="+5.1", delta_color="inverse")
        with c_legend:
            st.markdown("""
            <div class="score-legend-compact">
                <div style="color: #FFF; margin-bottom: 5px; border-bottom:1px solid #333;"><strong>📏 评分标准</strong></div>
                <div class="legend-row"><span class="color-dot" style="background:#00FF41;"></span>0-25: 优</div>
                <div class="legend-row"><span class="color-dot" style="background:#ADFF2F;"></span>25-50: 良</div>
                <div class="legend-row"><span class="color-dot" style="background:#FFFF00;"></span>50-75: 中</div>
                <div class="legend-row"><span class="color-dot" style="background:#FF3333;"></span>75+: 差</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 2) + [env_score/10, soc_score/10], columns=['Env', 'Soc'])
        st.line_chart(chart_data, color=["#00FF41", "#00F2FF"], height=100)

    st.markdown("---")
    
    col_env, col_soc = st.columns(2)
    
    with col_env:
        st.markdown("#### 🌍 SATELLITE_LINK // 环境风险 (E)")
        env_analysis = data.get('environment', {}).get('analysis', {})
        st.markdown(f"""<div class="tech-card"><p><strong>分析方法:</strong> {env_analysis.get('method', 'AI遥感反演')}</p></div>""", unsafe_allow_html=True)
        
        if not is_cofco:
            st.markdown("**🛰️ 历史影像对比 (Evidence):**")
            evidence = env_analysis.get('evidence', {})
            img_before = os.path.join(BASE_DIR, evidence.get('satellite_image_before', ''))
            img_after = os.path.join(BASE_DIR, evidence.get('satellite_image_after', ''))
            
            if os.path.exists(img_before) and os.path.exists(img_after):
                c_img1, c_img2 = st.columns(2)
                with c_img1: st.image(img_before, caption="📸 基准年 (Before)", use_container_width=True)
                with c_img2: st.image(img_after, caption="📸 最近年 (After)", use_container_width=True)
                st.success(f"✅ AI分析结论: {evidence.get('conclusion', '')}")
            else:
                st.info("⚠️ 卫星数据加载中...")
        else:
            st.code("# COFCO Environmental Status: COMPLIANT", language="python")
            
    with col_soc:
        st.markdown("#### 📢 SOCIAL_LISTENING // 舆情证据链 (S)")
        social = data.get('social', {})
        events = social.get('key_events', [])
        
        if events:
            for i, event in enumerate(events[:3]):
                border_color = "#FF3333" if event.get('severity', '中') in ['高', '严重'] else "#FFCC00"
                st.markdown(f"""
                <div class="tech-card" style="padding: 15px; border-left: 4px solid {border_color}; margin-bottom: 15px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span style="color:{border_color}; font-weight:bold; font-size:0.85rem;">RISK EVENT #{i+1}</span>
                        <span style="color:#666; font-family:monospace; font-size:0.9rem;">{event.get('date', 'N/A')}</span>
                    </div>
                    <div style="color: #FFF; font-size: 1.1rem; font-weight: bold; margin-bottom: 12px; line-height: 1.4;">{event.get('event', '')}</div>
                    <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:4px; margin-bottom:10px; border:1px dashed #333;">
                        <div style="color:#00FF41; font-size:0.8rem; margin-bottom:4px;">🤖 AI 智能解说 (ANALYSIS):</div>
                        <div style="color:#CCC; font-size:0.95rem;">{event.get('impact', 'AI识别到潜在风险，建议复核。')}</div>
                    </div>
                    <div style="text-align:right;"><a href="#" class="source-link-btn">📂 原文下载 (DOC_{202400+i}.PDF)</a></div>
                </div>
                """, unsafe_allow_html=True)
            st.success("✅ 证据链完整度: 100% (3/3 Verified)")

            st.markdown("---")
            with st.expander("💡 为什么只显示这 3 个事件？(AI Scoring Logic)", expanded=False):
                st.markdown("""
                <div style="font-size: 0.95rem;">
                    <p><strong>1. 关键风险归因 (Pareto Principle):</strong><br>
                    在 ESG 风险评估中，少数<strong>重大合规事件</strong>（如美国 CBP 暂扣令、欧盟反毁林调查）往往对企业信用具有<strong>"一票否决权"</strong>。系统筛选出这 Top 3 关键事件，解释了当前高风险评分 80% 的来源。</p>
                    <p><strong>2. 时间窗口与活跃度 (Time Window):</strong><br>
                    AI 模型优先展示<strong>"当前活跃 (Active)"</strong>或<strong>"未决 (Pending)"</strong>的风险事件。已解决的历史旧闻权重会随时间衰减。</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("暂无重大风险事件")

# ---------- TAB 2: 链式穿透 ----------
with tab2:
    st.header("🔗 供应链风险传导网络")
    
    if is_cofco:
        st.info("💡 核心企业视角: 监控上游风险如何传导至自身及市场")
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #0F0F0F; padding: 20px; border-radius: 10px; border: 1px dashed #333; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FF3333; color: #FF3333; padding: 10px; border-radius: 5px;">FGV Holdings<br><small>上游/高风险</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">中粮集团<br><small>核心企业</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #00F2FF; color: #00F2FF; padding: 10px; border-radius: 5px;">欧美市场<br><small>合规壁垒</small></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🚨 上游风险源")
            suppliers = data.get('supply_chain', {}).get('upstream', {}).get('suppliers', [])
            for s in suppliers:
                is_high = "高" in s.get('risk_status', '') or "75" in s.get('risk_status', '')
                status_html = f'<span style="color: #FF3333;">[高风险]</span>' if is_high else f'<span style="color: #00FF41;">[低风险]</span>'
                st.markdown(f"""<div class="tech-card" style="padding: 12px; margin-bottom: 10px;"><div style="font-size: 1rem; font-weight: bold;">{s['name']}</div><div style="font-size: 0.9rem; margin-top:5px;">状态: {status_html} {s.get('risk_status','')}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("### 🛡️ 阻断策略建议")
            st.markdown("""<div class="tech-card"><ul style="margin: 0; padding-left: 20px; color: #DDD;"><li style="margin-bottom: 10px;"><strong>动态调整:</strong> 立即降低 FGV 采购份额至 10% 以下。</li><li style="margin-bottom: 10px;"><strong>替代方案:</strong> 激活 IOI Corporation (低风险) 备选通道。</li><li><strong>物理隔离:</strong> 针对美国 CBP 要求，建立独立仓储。</li></ul></div>""", unsafe_allow_html=True)
            
    else:
        st.info(f"💡 供应商视角: 您的 ESG 风险如何导致下游客户流失")
        my_risk_color = "#FF3333" if total_score > 50 else "#00FF41"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #0F0F0F; padding: 20px; border-radius: 10px; border: 1px dashed #333; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid {my_risk_color}; color: {my_risk_color}; padding: 10px; border-radius: 5px;">{data.get('company')}<br><small>您 (供应商)</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">核心加工商<br><small>采购方</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FF0000; color: #FF0000; padding: 10px; border-radius: 5px; background: rgba(255,0,0,0.1);">市场禁入<br><small>CBP/EUDR 拦截</small></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📉 商业影响预测")
            st.markdown(f"""<div class="tech-card" style="border-left-color: #FF3333;"><div style="margin-bottom:10px;"><strong>⚠️ 主要客户流失风险:</strong></div><div style="font-size:2rem; color:#FF3333; font-weight:bold;">HIGH</div><p style="color:#BBB; font-size:0.9rem;">由于您的社会风险评分 ({soc_score}) 过高，下游客户面临合规压力，预计削减 70% 订单。</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("### ✅ 整改建议 (To-Do)")
            st.markdown("""<div class="tech-card" style="border-left-color: #00FF41;"><ul style="margin: 0; padding-left: 20px; color: #DDD;"><li style="margin-bottom: 10px;"><strong>立即行动:</strong> 提交针对 CBP WRO 的第三方审计报告。</li><li><strong>透明度:</strong> 上传劳工合规证明。</li></ul></div>""", unsafe_allow_html=True)

# ---------- TAB 3: 绿色金融 ----------
with tab3:
    st.markdown("## 💰 绿色金融与风险定价")
    fin_col1, fin_col2 = st.columns([1, 1])
    
    with fin_col1:
        st.markdown("### 🏦 ESG 挂钩贷款模拟")
        st.markdown("""<div class="tech-card" style="border-left-color: #00F2FF;"><strong>算法逻辑:</strong> 基于企业的实时 ESG 评分，计算可获得的绿色贷款利率优惠 (Basis Points)。</div>""", unsafe_allow_html=True)
        
        loan_amount = st.number_input("贷款金额 (万元)", min_value=100, value=5000, step=100)
        
        # 按钮 (Session State 状态保持)
        if 'show_loan_result' not in st.session_state:
            st.session_state.show_loan_result = False
        
        if st.button("🚀 开始 AI 评级测算 (START RATING)", type="primary", use_container_width=True):
            st.session_state.show_loan_result = True
            
        if st.session_state.show_loan_result:
            base_rate = 4.35
            discount_bp = 50 if total_score <= 30 else (20 if total_score <= 50 else 0)
            rating_color = "#00FF41" if total_score <= 30 else ("#ADFF2F" if total_score <= 50 else "#FFA500")
            rating_label = "🌿 深绿企业" if total_score <= 30 else ("🍃 浅绿企业" if total_score <= 50 else "🍂 棕色企业")
            final_rate = base_rate - (discount_bp / 100)
            annual_saving = loan_amount * (discount_bp / 10000)
            
            st.markdown("---")
            st.markdown(f'<div style="font-size: 1.1rem; font-weight: bold; color: {rating_color}; margin: 10px 0;">评级结果: {rating_label}</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("基础利率", f"{base_rate}%")
            c2.metric("ESG 优惠", f"-{discount_bp} bp")
            c3.metric("执行利率", f"{final_rate:.2f}%")
            st.markdown(f"""<div style="background: #111; border: 1px solid #00FF41; padding: 15px; border-radius: 6px; text-align: center; margin-top: 15px;"><span style="color: #888; font-size: 0.9rem;">预计年利息节省</span><br><span style="font-size: 1.8rem; color: #00FF41; font-weight: bold; font-family: monospace;">¥ {annual_saving:,.0f}</span></div>""", unsafe_allow_html=True)
        else:
            st.info("💡 请输入贷款金额，点击上方按钮开始测算")
        
    with fin_col2:
        st.markdown("### 📉 财务风险量化")
        if total_score > 60:
            potential_loss = loan_amount * 0.15 
            st.error("⚠️ 风险敞口极高 (High Exposure)")
            st.markdown("""<div class="tech-card" style="border-left-color: #FF3333;"><p style="color: #FF3333 !important;"><strong>主要风险源:</strong></p><ul style="color: #DDD;"><li>🇪🇺 <strong>欧盟 EUDR 罚款:</strong> 营收的 4%</li><li>🇺🇸 <strong>货物滞留成本:</strong> 约 200 万 USD</li></ul></div>""", unsafe_allow_html=True)
            st.metric("潜在财务损失预估", f"¥ {potential_loss/10000:,.1f} 亿", delta="-15% 营收", delta_color="inverse")
        else:
            st.success("✅ 财务风险可控")
            st.metric("绿色溢价 (Greenium)", "+ 2.5%", "融资成本优势")

    st.markdown("---")
    st.subheader("⛓️ 供应链金融授信模型")
    scf_df = pd.DataFrame({"供应商": ["FGV", "IOI", "Sime Darby", "Wilmar"], "ESG 风险分": [75, 25, 30, 40], "基础授信(万)": [1000, 1000, 1000, 1000]})
    scf_df["调整系数"] = scf_df["ESG 风险分"].apply(lambda x: 0.5 if x > 60 else (1.2 if x < 30 else 1.0))
    scf_df["动态授信(万)"] = (scf_df["基础授信(万)"] * scf_df["调整系数"]).astype(int)
    st.dataframe(scf_df, use_container_width=True, hide_index=True)

# ---------- TAB 4: 消费终端 ----------
with tab4:
    st.markdown("### 📱 产品数字孪生与信任溯源 (B2C)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""<div style="background: #FFF; padding: 15px; border-radius: 10px; display: inline-block;"><img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://xikai0906.github.io/green-link-demo/" width="100%" /></div>""", unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; margin-top:10px; color:#00F2FF;">SCAN TO VERIFY</p>', unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="product-trace-card">
            <h2 style="color: #FFF; margin-bottom: 20px;">🌿 福临门食用油 <span style="font-size:0.6em; color:#00FF41; border:1px solid #00FF41; padding:2px 8px; border-radius:4px;">VERIFIED</span></h2>
            <div style="display: flex; justify-content: space-between; text-align: left; margin-bottom: 20px;">
                <div style="width: 30%;"><div style="color: #888; font-size: 0.8rem;">CARBON FOOTPRINT</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">1.2kg</div><div style="color: #555; font-size: 0.7rem;">CO2e / Bottle</div></div>
                <div style="width: 30%;"><div style="color: #888; font-size: 0.8rem;">ORIGIN</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">Johor, MY</div><div style="color: #555; font-size: 0.7rem;">Satellite Checked</div></div>
                <div style="width: 30%;"><div style="color: #888; font-size: 0.8rem;">LABOR</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">ILO Compliant</div><div style="color: #555; font-size: 0.7rem;">Audit Passed</div></div>
            </div>
            <div style="background: rgba(0, 255, 65, 0.1); border: 1px dashed #00FF41; padding: 10px; border-radius: 8px;"><p style="color: #00FF41; margin: 0; font-size: 0.9rem;">✅ <strong>区块链存证哈希:</strong> 0x7f83...9a2b<br>该产品供应链全链路符合 GreenLink 可持续发展标准</p></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📜 底层合规协议与国际标准 (COMPLIANCE PROTOCOLS)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("""<div class="protocol-box"><div class="protocol-title">ISO 14067 (碳足迹)</div><div style="color:#BBB; font-size:0.85rem;">• <strong>标准:</strong> LCA法<br>• <strong>优势:</strong> 减碳 68%</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="protocol-box"><div class="protocol-title">EUDR (零毁林)</div><div style="color:#BBB; font-size:0.85rem;">• <strong>红线:</strong> 2020年后无毁林<br>• <strong>验证:</strong> Sentinel-2 卫星</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="protocol-box"><div class="protocol-title">ILO (劳工公约)</div><div style="color:#BBB; font-size:0.85rem;">• <strong>重点:</strong> 规避美国 CBP 禁令<br>• <strong>审计:</strong> SA8000 认证</div></div>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""<div style="font-size: 0.8rem; color: #666;">POWERED BY <strong style="color: #FFF;">GREENLINK TECH</strong><br>v3.6.0 (Dual-Lock Fix)</div>""", unsafe_allow_html=True)
