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
        background-color: #000000; /* 纯黑背景 */
        color: #FFFFFF !important; /* 强制纯白字体 */
    }
    
    /* 2. 针对所有文本容器的增强 */
    .stMarkdown, .stText, p, div {
        color: #FFFFFF;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 3. 标题样式 - 清晰锐利 */
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 3.2rem;
        font-weight: 900;
        color: #00FF41; /* 纯霓虹绿 */
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.8); 
        letter-spacing: -2px;
    }
    
    .sub-header {
        font-family: sans-serif;
        font-size: 1.3rem;
        font-weight: bold;
        color: #00F2FF; /* 赛博蓝 */
        text-align: center;
        margin-bottom: 2.5rem;
        letter-spacing: 1px;
    }

    /* 4. 信息卡片 */
    .tech-card {
        background-color: #1A1A1A;
        border: 2px solid #333;
        border-left: 6px solid #00FF41;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8);
    }
    .tech-card h3 { color: #00F2FF !important; margin-top: 0; font-weight: 800; }
    
    /* 5. 对比卡片样式 (新增) */
    .comparison-box {
        background: #111;
        border: 1px solid #444;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* 6. Streamlit 指标组件颜色强制覆盖 */
    div[data-testid="stMetricLabel"] { color: #AAAAAA !important; font-size: 1rem !important; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #00FF41 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    
    /* 7. 侧边栏优化 */
    section[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 { color: #00F2FF !important; }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown('<div class="main-header">GREENLINK_OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">>> 卫星遥感 · 舆情挖掘 · 绿色金融 <<</div>', unsafe_allow_html=True)

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
    "📊 风险监测", 
    "🔗 链式穿透", 
    "💰 绿色金融",
    "📱 消费终端"
])

# ---------- TAB 1: 风险监测 (已恢复原始内容) ----------
with tab1:
    # 1.1 头部信息与评级对比 (恢复了原来的评级对比逻辑)
    col_header, col_chart = st.columns([2, 1])
    
    with col_header:
        st.markdown(f"""
        <div class="tech-card">
            <h3>{data.get('company')}</h3>
            <p><strong>ID:</strong> {company_info['code']}_9928 | <strong>角色:</strong> {company_info['position']}</p>
        </div>
        """, unsafe_allow_html=True)

        # === 恢复：传统评级 vs 绿链评级 ===
        st.markdown("##### ⚔️ 评级体系对比 (VS Traditional)")
        c1, c2 = st.columns(2)
        with c1:
            traditional = data.get('traditional_rating', {}) or data.get('social', {}).get('traditional_rating', {})
            rating_val = traditional.get('rating', traditional.get('msci', 'N/A'))
            st.markdown(f"""
            <div class="comparison-box" style="border-left: 4px solid #555;">
                <div style="color:#888; font-size:0.9rem;">🏢 传统评级 (MSCI)</div>
                <div style="font-size: 2rem; font-weight:bold; color: #FFF;">{rating_val}</div>
                <div style="color:#888; font-size:0.8rem;">❌ 评级模糊，无法区分E/S风险</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="comparison-box" style="border-left: 4px solid #00FF41;">
                <div style="color:#888; font-size:0.9rem;">🌿 绿链 GreenLink</div>
                <div style="font-size: 1.2rem; font-weight:bold; color: #00FF41;">E/S 分离评分</div>
                <div style="color:#EEE; font-size:0.8rem;">✅ 环境: {env_score} | 社会: {soc_score}</div>
                <div style="color:#00FF41; font-size:0.8rem;">精准定位风险源</div>
            </div>
            """, unsafe_allow_html=True)

    with col_chart:
        # 指标与图表
        st.markdown("##### 核心指标")
        st.metric("E-Score (环境)", f"{env_score}", delta="-2.5", delta_color="inverse")
        st.metric("S-Score (社会)", f"{soc_score}", delta="+5.1", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 2) + [env_score/10, soc_score/10], columns=['Env', 'Soc'])
        st.line_chart(chart_data, color=["#00FF41", "#00F2FF"], height=150)

    st.markdown("---")
    
    # 1.2 详细分析 (恢复了卫星图对比)
    col_env, col_soc = st.columns(2)
    
    # === 环境模块 (恢复卫星图对比) ===
    with col_env:
        st.markdown("#### 🌍 SATELLITE_LINK // 环境风险 (E)")
        env_analysis = data.get('environment', {}).get('analysis', {})
        
        st.markdown(f"""
        <div class="tech-card">
            <p><strong>分析方法:</strong> {env_analysis.get('method', 'AI遥感反演')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_cofco:
            # === 核心恢复：卫星影像前后对比 ===
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
                
                # 恢复详细观察
                conclusion = evidence.get('conclusion', env_analysis.get('conclusion', ''))
                st.success(f"✅ **AI分析结论**: {conclusion}")
            else:
                st.info("⚠️ 系统提示: 卫星影像数据流加载中或路径未配置...")
        else:
            # COFCO 的展示逻辑
            st.code(f"# 中粮集团环境合规性\nstatus = 'COMPLIANT'\n# {env_analysis.get('conclusion', 'No Issue')}", language="python")
            
    # === 社会模块 ===
    with col_soc:
        st.markdown("#### 📢 SOCIAL_LISTENING // 社会风险 (S)")
        social = data.get('social', {})
        events = social.get('key_events', [])
        
        if events:
            for event in events[:3]:
                severity = event.get('severity', '中')
                border_color = "#FF3333" if severity in ['高', '严重'] else "#FFCC00"
                
                st.markdown(f"""
                <div style="border-left: 4px solid {border_color}; padding-left: 15px; margin-bottom: 15px; background: #222; padding: 10px; border-radius: 4px;">
                    <div style="color: #888; font-size: 0.8rem; font-weight:bold;">{event.get('date', 'N/A')}</div>
                    <div style="color: #FFF; font-size: 1rem;">{event.get('event', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("暂无重大风险事件")

# ---------- TAB 2: 链式穿透 ----------
with tab2:
    st.header("🔗 供应链风险传导网络")
    
    if is_cofco:
        st.info("💡 提示: 展示风险如何从 FGV (上游) 传导至 中粮 (核心) 再影响 欧美市场 (下游)")
        
        # 流程图可视化
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: center; background: #111; padding: 20px; border-radius: 10px; border: 1px solid #444; margin-bottom: 20px;">
            <div style="text-align: center;">
                <div style="border: 2px solid #FF3333; color: #FF3333; padding: 10px; border-radius: 5px; font-weight: bold;">FGV Holdings<br>(上游/高风险)</div>
            </div>
            <div style="color: #555; font-size: 2rem;">➜</div>
            <div style="text-align: center;">
                <div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px; font-weight: bold;">中粮集团<br>(核心企业)</div>
            </div>
            <div style="color: #555; font-size: 2rem;">➜</div>
            <div style="text-align: center;">
                <div style="border: 2px solid #00F2FF; color: #00F2FF; padding: 10px; border-radius: 5px; font-weight: bold;">欧美市场<br>(合规壁垒)</div>
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
                <div class="tech-card" style="padding: 10px;">
                    <div style="font-size: 1.1rem; font-weight: bold;">{s['name']}</div>
                    <div>状态: {status_html} {risk_status}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🛡️ 阻断策略建议")
            st.markdown("""
            <div class="tech-card">
                <ul style="margin: 0; padding-left: 20px;">
                    <li style="margin-bottom: 10px;"><strong>动态调整:</strong> 立即降低 FGV 采购份额至 10% 以下。</li>
                    <li style="margin-bottom: 10px;"><strong>替代方案:</strong> 激活 IOI Corporation (低风险) 备选通道。</li>
                    <li><strong>物理隔离:</strong> 针对美国 CBP 要求，建立独立仓储。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("当前视图为供应商视角：展示自身风险如何影响下游客户。")
        st.metric("下游客户流失风险", "High", "CBP禁令影响")

# ---------- TAB 3: 绿色金融 (新功能) ----------
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
        
        st.markdown(f'<div style="font-size: 1.2rem; font-weight: bold; color: {rating_color}; margin: 10px 0;">评级结果: {rating_label}</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("基础利率", f"{base_rate}%")
        c2.metric("ESG 优惠", f"-{discount_bp} bp")
        c3.metric("执行利率", f"{final_rate:.2f}%")
        
        st.markdown(f"""
        <div style="background: #222; border: 1px solid #00FF41; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;">
            <span style="color: #888;">预计年利息节省</span><br>
            <span style="font-size: 2rem; color: #00FF41; font-weight: bold; font-family: monospace;">¥ {annual_saving:,.0f}</span>
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

# ---------- TAB 4: 消费终端 ----------
with tab4:
    st.header("📱 B2C 信任溯源")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style="background: white; padding: 10px; display: inline-block; border-radius: 10px;">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=GreenLink_Product_Cert" width="200" />
        </div>
        """, unsafe_allow_html=True)
        st.caption("扫码查看区块链证书")
    with col2:
        st.markdown("""
        <div class="tech-card">
            <h3>消费者视角的信任标签</h3>
            <ul style="font-size: 1.1rem; line-height: 2;">
                <li>👣 <strong>碳足迹:</strong> 1.2kg CO2e / 瓶 (优于行业 20%)</li>
                <li>📍 <strong>产地:</strong> 马来西亚柔佛州 (卫星验证无毁林)</li>
                <li>🤝 <strong>劳工:</strong> 符合 ILO 核心公约</li>
            </ul>
            <div style="margin-top: 20px; color: #00FF41; font-weight: bold; font-size: 1.2rem;">
                ✅ 该产品已通过 GreenLink 绿色认证
            </div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 GreenLink Tech")
