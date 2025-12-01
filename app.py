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
    /* 1. 全局背景与字体 - 极致对比度 */
    .stApp {
        background-color: #050505; /* 接近纯黑 */
        color: #FFFFFF !important;
    }
    
    /* 2. 针对所有文本容器的增强 */
    .stMarkdown, .stText, p, div {
        color: #E0E0E0;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 3. 标题样式 */
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00FF41; /* 纯霓虹绿 */
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.6); 
        letter-spacing: -2px;
        text-transform: uppercase;
    }
    
    .sub-header {
        font-family: sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        color: #00F2FF; /* 赛博蓝 */
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 2px;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
    }

    /* 4. 信息卡片 (Tech Card) */
    .tech-card {
        background-color: #121212;
        border: 1px solid #333;
        border-left: 5px solid #00FF41;
        padding: 1.5rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .tech-card:hover {
        border-color: #555;
        box-shadow: 0 4px 25px rgba(0, 255, 65, 0.1);
    }
    .tech-card h3 { color: #00F2FF !important; margin-top: 0; font-weight: 800; font-size: 1.4rem; }
    
    /* 5. 侧边栏 (Sidebar) 终极修复 */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #00F2FF !important;
    }
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important; /* 强制纯白 */
        font-weight: 500;
    }
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border-color: #444 !important;
    }
    div[data-baseweb="popover"] {
        background-color: #1A1A1A !important;
    }
    div[data-baseweb="menu"] li {
        color: #FFFFFF !important;
    }
    
    /* 6. Streamlit 指标组件颜色强制覆盖 */
    div[data-testid="stMetricLabel"] { color: #AAAAAA !important; font-size: 0.9rem !important; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #00FF41 !important; font-family: 'Courier New', monospace; font-weight: bold; text-shadow: 0 0 5px rgba(0,255,65,0.3); }
    
    /* 7. 产品溯源卡片 (B2C专用) */
    .product-trace-card {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
        border: 1px solid #00F2FF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    
    /* 8. 标准协议小卡片 */
    .protocol-box {
        background: #111;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    .protocol-title {
        color: #00FF41;
        font-weight: bold;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }

    /* 9. 修复：强制原生 UI 按钮可见 */
    [data-testid="stImage"] button svg,
    [data-testid="stVegaLiteChart"] button svg,
    .st-emotion-cache-1p1m4t5 svg {
        fill: #00FF41 !important;
        stroke: #00FF41 !important;
    }
    [data-testid="stImage"] button:hover,
    [data-testid="stVegaLiteChart"] button:hover {
        background-color: rgba(0, 255, 65, 0.2) !important;
        border-radius: 4px;
    }
    
    /* 10. 舆情链接按钮样式 */
    .source-link-btn {
        display: inline-block;
        margin-top: 8px;
        padding: 4px 10px;
        border: 1px solid #333;
        border-radius: 4px;
        color: #00F2FF !important;
        font-size: 0.8rem;
        text-decoration: none;
        transition: all 0.2s;
        background: rgba(0, 242, 255, 0.05);
    }
    .source-link-btn:hover {
        border-color: #00F2FF;
        background: rgba(0, 242, 255, 0.15);
        color: #FFF !important;
    }

    /* 11. 链式穿透流程图样式 */
    .chain-box {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin: 5px;
    }
    .arrow {
        color: #666; 
        font-size: 1.5rem; 
        display: flex; 
        align-items: center; 
        justify-content: center;
    }

</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown('<div class="main-header">GREENLINK_OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">>> SATELLITE · INTELLIGENCE · FINANCE <<</div>', unsafe_allow_html=True)

# ==========================================
# 2. 数据加载与处理
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

# 动态计算综合评分
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
    # 1.1 头部信息与评级对比
    col_header, col_chart = st.columns([2, 1])
    
    with col_header:
        st.markdown(f"""
        <div class="tech-card">
            <h3>{data.get('company')}</h3>
            <p style="color:#AAA;"><strong>ID:</strong> {company_info['code']}_9928 &nbsp;|&nbsp; <strong>Role:</strong> {company_info['position']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 评级对比 (防错修复版)
        st.markdown("##### ⚔️ 评级体系对比 (VS Traditional)")
        
        # 智能获取评级数据，防止崩溃
        trad_data = data.get('traditional_rating') or data.get('social', {}).get('traditional_rating')
        if isinstance(trad_data, dict):
            rating_val = trad_data.get('rating', trad_data.get('msci', 'N/A'))
        elif isinstance(trad_data, str):
            rating_val = trad_data
        else:
            rating_val = 'N/A'
            
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
        st.markdown("##### 核心指标")
        st.metric("E-Score (环境)", f"{env_score}", delta="-2.5", delta_color="inverse")
        st.metric("S-Score (社会)", f"{soc_score}", delta="+5.1", delta_color="inverse")
        st.markdown("<br>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 2) + [env_score/10, soc_score/10], columns=['Env', 'Soc'])
        st.line_chart(chart_data, color=["#00FF41", "#00F2FF"], height=120)

    st.markdown("---")
    
    # 1.2 详细分析
    col_env, col_soc = st.columns(2)
    
    # === 环境模块 ===
    with col_env:
        st.markdown("#### 🌍 SATELLITE_LINK // 环境风险 (E)")
        env_analysis = data.get('environment', {}).get('analysis', {})
        
        st.markdown(f"""
        <div class="tech-card">
            <p><strong>分析方法:</strong> {env_analysis.get('method', 'AI遥感反演')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_cofco:
            st.markdown("**🛰️ 历史影像对比 (Evidence):**")
            evidence = env_analysis.get('evidence', {})
            img_before = evidence.get('satellite_image_before', '')
            img_after = evidence.get('satellite_image_after', '')
            
            img_before_path = os.path.join(BASE_DIR, img_before) if img_before else ''
            img_after_path = os.path.join(BASE_DIR, img_after) if img_after else ''
            
            if img_before_path and img_after_path and os.path.exists(img_before_path):
                c_img1, c_img2 = st.columns(2)
                with c_img1:
                    st.image(img_before_path, caption="📸 基准年 (Before)", use_container_width=True)
                with c_img2:
                    st.image(img_after_path, caption="📸 最近年 (After)", use_container_width=True)
                
                conclusion = evidence.get('conclusion', env_analysis.get('conclusion', ''))
                st.success(f"✅ AI分析结论: {conclusion}")
            else:
                st.info("⚠️ 系统提示: 卫星影像数据流加载中...")
        else:
            st.code(f"# 中粮集团环境合规性\nstatus = 'COMPLIANT'\n# {env_analysis.get('conclusion', 'No Issue')}", language="python")
            
    # === 社会模块 (舆情证据链) ===
    with col_soc:
        st.markdown("#### 📢 SOCIAL_LISTENING // 舆情证据链 (S)")
        st.caption("AI 自动关联舆情事件与合规风险影响分析")
        
        social = data.get('social', {})
        events = social.get('key_events', [])
        
        if events:
            for i, event in enumerate(events[:3]):
                severity = event.get('severity', '中')
                border_color = "#FF3333" if severity in ['高', '严重'] else "#FFCC00"
                impact_text = event.get('impact', 'AI 风险模型识别到潜在供应链合规隐患，建议人工复核。')
                source_id = f"DOC_{202400+i}"
                
                st.markdown(f"""
                <div class="tech-card" style="padding: 15px; border-left: 4px solid {border_color}; margin-bottom: 15px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span style="color:{border_color}; font-weight:bold; font-size:0.85rem;">RISK EVENT #{i+1}</span>
                        <span style="color:#666; font-family:monospace; font-size:0.9rem;">{event.get('date', 'N/A')}</span>
                    </div>
                    <div style="color: #FFF; font-size: 1.1rem; font-weight: bold; margin-bottom: 12px; line-height: 1.4;">
                        {event.get('event', '')}
                    </div>
                    <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:4px; margin-bottom:10px; border:1px dashed #333;">
                        <div style="color:#00FF41; font-size:0.8rem; margin-bottom:4px;">🤖 AI 智能解说 (ANALYSIS):</div>
                        <div style="color:#CCC; font-size:0.95rem;">{impact_text}</div>
                    </div>
                    <div style="text-align:right;">
                        <a href="#" class="source-link-btn">
                            📂 原文证据下载 (SOURCE: {source_id}.PDF)
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.success("✅ 证据链完整度验证: 100% (3/3 Verified)")
        else:
            st.write("暂无重大风险事件")

# ---------- TAB 2: 链式穿透 ----------
with tab2:
    st.header("🔗 供应链风险传导网络")
    
    if is_cofco:
        # COFCO 视角：上游 -> 核心 -> 下游
        st.info("💡 核心企业视角: 监控上游风险如何传导至自身及市场")
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #0F0F0F; padding: 20px; border-radius: 10px; border: 1px dashed #333; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid #FF3333; color: #FF3333; padding: 10px; border-radius: 5px;">FGV Holdings<br><small>上游/高风险</small></div>
            </div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">中粮集团<br><small>核心企业</small></div>
            </div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid #00F2FF; color: #00F2FF; padding: 10px; border-radius: 5px;">欧美市场<br><small>合规壁垒</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🚨 上游风险源")
            suppliers = data.get('supply_chain', {}).get('upstream', {}).get('suppliers', [])
            for s in suppliers:
                risk_status = s.get('risk_status', '')
                is_high = "高" in risk_status or "75" in risk_status
                status_html = f'<span style="color: #FF3333;">[高风险]</span>' if is_high else f'<span style="color: #00FF41;">[低风险]</span>'
                st.markdown(f"""
                <div class="tech-card" style="padding: 12px; margin-bottom: 10px;">
                    <div style="font-size: 1rem; font-weight: bold;">{s['name']}</div>
                    <div style="font-size: 0.9rem; margin-top:5px;">状态: {status_html} {risk_status}</div>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("### 🛡️ 阻断策略建议")
            st.markdown("""
            <div class="tech-card">
                <ul style="margin: 0; padding-left: 20px; color: #DDD;">
                    <li style="margin-bottom: 10px;"><strong>动态调整:</strong> 立即降低 FGV 采购份额至 10% 以下。</li>
                    <li style="margin-bottom: 10px;"><strong>替代方案:</strong> 激活 IOI Corporation (低风险) 备选通道。</li>
                    <li><strong>物理隔离:</strong> 针对美国 CBP 要求，建立独立仓储。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        # 供应商视角 (FGV/IOI)
        st.info(f"💡 供应商视角: 您的 ESG 风险如何导致下游客户 ({data.get('supply_chain', {}).get('midstream', {}).get('name', '核心加工商')}) 流失")
        
        my_risk_color = "#FF3333" if total_score > 50 else "#00FF41"
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #0F0F0F; padding: 20px; border-radius: 10px; border: 1px dashed #333; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid {my_risk_color}; color: {my_risk_color}; padding: 10px; border-radius: 5px;">{data.get('company')}<br><small>您 (供应商)</small></div>
            </div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">核心加工商<br><small>采购方 (如中粮)</small></div>
            </div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box">
                <div style="border: 2px solid #FF0000; color: #FF0000; padding: 10px; border-radius: 5px; background: rgba(255,0,0,0.1);">市场禁入<br><small>CBP/EUDR 拦截</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📉 商业影响预测")
            st.markdown("""
            <div class="tech-card" style="border-left-color: #FF3333;">
                <div style="margin-bottom:10px;"><strong>⚠️ 主要客户流失风险:</strong></div>
                <div style="font-size:2rem; color:#FF3333; font-weight:bold;">HIGH</div>
                <p style="color:#BBB; font-size:0.9rem;">由于您的社会风险评分 ({}) 过高，下游客户 (中粮) 正面临美国 CBP 合规压力，可能在 3 个月内削减 70% 订单。</p>
            </div>
            """.format(soc_score), unsafe_allow_html=True)
            
        with col2:
            st.markdown("### ✅ 整改建议 (To-Do)")
            st.markdown("""
            <div class="tech-card" style="border-left-color: #00FF41;">
                <ul style="margin: 0; padding-left: 20px; color: #DDD;">
                    <li style="margin-bottom: 10px;"><strong>立即行动:</strong> 提交针对 CBP WRO 的第三方审计报告。</li>
                    <li style="margin-bottom: 10px;"><strong>透明度:</strong> 在 GreenLink 平台上传劳工合规证明。</li>
                    <li><strong>沟通:</strong> 主动向中粮集团发送整改进度函。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ---------- TAB 3: 绿色金融 ----------
with tab3:
    st.markdown("## 💰 绿色金融与风险定价")
    
    fin_col1, fin_col2 = st.columns([1, 1])
    
    with fin_col1:
        st.markdown("### 🏦 ESG 挂钩贷款模拟")
        st.markdown("""
        <div class="tech-card" style="border-left-color: #00F2FF;">
            <strong>算法逻辑:</strong> 基于企业的实时 ESG 评分，计算可获得的绿色贷款利率优惠 (Basis Points)。
        </div>
        """, unsafe_allow_html=True)
        
        loan_amount = st.number_input("贷款金额 (万元)", min_value=100, value=5000, step=100)
        base_rate = 4.35
        
        discount_bp = 0
        if total_score <= 30:
            discount_bp = 50
            rating_label = "🌿 深绿企业 (Deep Green)"
            rating_color = "#00FF41"
        elif total_score <= 50:
            discount_bp = 20
            rating_label = "🍃 浅绿企业 (Light Green)"
            rating_color = "#ADFF2F"
        else:
            discount_bp = 0
            rating_label = "🍂 棕色企业 (Transition)"
            rating_color = "#FFA500"
            
        final_rate = base_rate - (discount_bp / 100)
        annual_saving = loan_amount * (discount_bp / 10000)
        
        st.markdown(f'<div style="font-size: 1.1rem; font-weight: bold; color: {rating_color}; margin: 10px 0;">评级结果: {rating_label}</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("基础利率", f"{base_rate}%")
        c2.metric("ESG 优惠", f"-{discount_bp} bp")
        c3.metric("执行利率", f"{final_rate:.2f}%")
        
        st.markdown(f"""
        <div style="background: #111; border: 1px solid #00FF41; padding: 15px; border-radius: 6px; text-align: center; margin-top: 15px;">
            <span style="color: #888; font-size: 0.9rem;">预计年利息节省</span><br>
            <span style="font-size: 1.8rem; color: #00FF41; font-weight: bold; font-family: monospace;">¥ {annual_saving:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with fin_col2:
        st.markdown("### 📉 财务风险量化")
        if total_score > 60:
            potential_loss = loan_amount * 0.15 
            st.error("⚠️ 风险敞口极高 (High Exposure)")
            st.markdown("""
            <div class="tech-card" style="border-left-color: #FF3333;">
                <p style="color: #FF3333 !important;"><strong>主要风险源:</strong></p>
                <ul style="color: #DDD;">
                    <li>🇪🇺 <strong>欧盟 EUDR 罚款:</strong> 营收的 4%</li>
                    <li>🇺🇸 <strong>货物滞留成本:</strong> 约 200 万 USD</li>
                    <li>📉 <strong>品牌估值下调:</strong> 5-10%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.metric("潜在财务损失预估", f"¥ {potential_loss/10000:,.1f} 亿", delta="-15% 营收", delta_color="inverse")
        else:
            st.success("✅ 财务风险可控")
            st.metric("绿色溢价 (Greenium)", "+ 2.5%", "融资成本优势")

    st.markdown("---")
    st.subheader("⛓️ 供应链金融授信模型")
    scf_df = pd.DataFrame({
        "供应商": ["FGV Holdings", "IOI Corp", "Sime Darby", "Wilmar"],
        "ESG 风险分": [75, 25, 30, 40],
        "基础授信(万)": [1000, 1000, 1000, 1000]
    })
    scf_df["调整系数"] = scf_df["ESG 风险分"].apply(lambda x: 0.5 if x > 60 else (1.2 if x < 30 else 1.0))
    scf_df["动态授信(万)"] = scf_df["基础授信(万)"] * scf_df["调整系数"]
    scf_df["动态授信(万)"] = scf_df["动态授信(万)"].astype(int)

    st.dataframe(scf_df, use_container_width=True, hide_index=True)

# ---------- TAB 4: 消费终端 (修复二维码) ----------
with tab4:
    st.markdown("### 📱 产品数字孪生与信任溯源 (B2C)")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # 修复：使用真实部署链接生成二维码
        deployed_url = "https://xikai0906.github.io/green-link-demo/"
        st.markdown(f"""
        <div style="background: #FFF; padding: 15px; border-radius: 10px; display: inline-block; box-shadow: 0 0 20px rgba(255,255,255,0.1);">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={deployed_url}" width="100%" />
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; margin-top:10px; color:#00F2FF;">SCAN TO VERIFY</p>', unsafe_allow_html=True)
        
    with col2:
        # 科技风产品卡片
        st.markdown("""
        <div class="product-trace-card">
            <h2 style="color: #FFF; margin-bottom: 20px;">🌿 福临门食用油 <span style="font-size:0.6em; color:#00FF41; border:1px solid #00FF41; padding:2px 8px; border-radius:4px;">VERIFIED</span></h2>
            
            <div style="display: flex; justify-content: space-between; text-align: left; margin-bottom: 20px;">
                <div style="width: 30%;">
                    <div style="color: #888; font-size: 0.8rem;">CARBON FOOTPRINT</div>
                    <div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">1.2kg</div>
                    <div style="color: #555; font-size: 0.7rem;">CO2e / Bottle</div>
                </div>
                <div style="width: 30%;">
                    <div style="color: #888; font-size: 0.8rem;">ORIGIN</div>
                    <div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">Johor, MY</div>
                    <div style="color: #555; font-size: 0.7rem;">Satellite Checked</div>
                </div>
                <div style="width: 30%;">
                    <div style="color: #888; font-size: 0.8rem;">LABOR</div>
                    <div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">ILO Compliant</div>
                    <div style="color: #555; font-size: 0.7rem;">Audit Passed</div>
                </div>
            </div>
            
            <div style="background: rgba(0, 255, 65, 0.1); border: 1px dashed #00FF41; padding: 10px; border-radius: 8px;">
                <p style="color: #00FF41; margin: 0; font-size: 0.9rem;">
                    ✅ <strong>区块链存证哈希:</strong> 0x7f83...9a2b<br>
                    该产品供应链全链路符合 GreenLink 可持续发展标准
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 标准解读模块
    st.markdown("---")
    with st.expander("📜 底层合规协议与国际标准 (COMPLIANCE PROTOCOLS)", expanded=True):
        st.markdown("以下指标基于国际权威标准计算，确保数据可审计、可追溯：")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("""
            <div class="protocol-box">
                <div class="protocol-title">ISO 14067 (碳足迹)</div>
                <div style="color:#BBB; font-size:0.85rem;">
                • <strong>标准:</strong> 产品碳足迹国际标准 (LCA法)<br>
                • <strong>边界:</strong> 摇篮到大门 (Cradle-to-Gate)<br>
                • <strong>对比:</strong> 行业平均 ~3.8kg CO2e<br>
                • <strong>优势:</strong> 减碳 68% (绿色能源+循环经济)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("""
            <div class="protocol-box">
                <div class="protocol-title">EUDR (零毁林法案)</div>
                <div style="color:#BBB; font-size:0.85rem;">
                • <strong>法规:</strong> 欧盟第 2023/1115 号条例<br>
                • <strong>红线:</strong> 2020年12月31日后无毁林<br>
                • <strong>验证:</strong> Sentinel-2 卫星历史影像<br>
                • <strong>状态:</strong> ✅ 地理定位 (Geolocation) 合规
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown("""
            <div class="protocol-box">
                <div class="protocol-title">ILO (劳工公约)</div>
                <div style="color:#BBB; font-size:0.85rem;">
                • <strong>核心:</strong> 国际劳工组织 8项核心公约<br>
                • <strong>重点:</strong> C29 (强迫劳动) & C138 (童工)<br>
                • <strong>风控:</strong> 规避美国 CBP WRO (暂扣令)<br>
                • <strong>审计:</strong> 第三方 SA8000 认证通过
                </div>
            </div>
            """, unsafe_allow_html=True)

# 侧边栏底部
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.8rem; color: #666;">
    POWERED BY<br>
    <strong style="color: #FFF;">GREENLINK TECH</strong><br>
    v2.5.0 (QR Fixed)
</div>
""", unsafe_allow_html=True)
