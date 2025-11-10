#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import json
import pandas as pd
from PIL import Image
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 页面配置
# 自定义CSS样式
st.set_page_config(
    page_title="绿链 GreenLink - ESG风险评估平台",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)
# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 155rem;
        font-weight: 700;
        color: 
#2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 122rem;
        font-weight: 400;
        color: 
#7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: 
#f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid 
#27ae60;
    }
    .risk-high {
        color: 
#e74c3c;
        font-weight: bold;
    }
    .risk-low {
        color: 
#27ae60;
        font-weight: bold;
    }
    .supply-chain-box {
        background: linear-gradient(135deg, 
#667eea 0%, 
#764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)
# 标题
st.markdown('<p class="main-header">🌿 绿链 GreenLink</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">基于另类数据的供应链ESG风险评估平台</p>', unsafe_allow_html=True)

# 侧边栏：选择公司
st.sidebar.header("🎯 选择分析对象")
st.sidebar.markdown("---")

# 定义公司列表和供应链关系
companies = {
    "FGV Holdings Berhad": {
        "filename": "FGV.json",
        "type": "上游供应商",
        "position": "种植商"
    },
    "IOI Corporation": {
        "filename": "IOI.json", 
        "type": "上游供应商",
        "position": "种植商"
    },
    "中粮集团 (COFCO)": {
        "filename": "COFCO.json",
        "type": "中游加工商",
        "position": "采购商/加工商"
    }
}

selected_company = st.sidebar.selectbox(
    "选择企业",
    list(companies.keys()),
    help="选择要分析的供应链企业"
)

# 显示当前企业在供应链中的位置
company_info = companies[selected_company]
st.sidebar.info(f"**供应链位置**: {company_info['type']}\n\n**角色**: {company_info['position']}")

# 加载数据
@st.cache_data
def load_data(filename):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    if not os.path.exists(file_path):
        st.warning(f"数据文件 {filename} 未找到，显示示例数据")
        return get_sample_data(), False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 判断数据类型（上游供应商 vs 中游加工商）
        is_cofco = 'COFCO' in filename
        return data, is_cofco

def get_sample_data():
    """返回示例数据结构"""
    return {
        "company": "示例公司",
        "environment": {
            "risk_level": "低风险",
            "risk_score": 25,
            "analysis": {
                "method": "Sentinel-2 卫星影像分析",
                "period": "2014-2022",
                "evidence": {
                    "satellite_image_before": "",
                    "satellite_image_after": "",
                    "conclusion": "种植园边界稳定，无新增毁林证据"
                }
            },
            "compliance": {
                "eudr": "✅ 符合欧盟EUDR法规",
                "rspo": "⚠️ 部分认证暂停"
            }
        },
        "social": {
            "risk_level": "高风险",
            "risk_score": 75,
            "key_events": [],
            "traditional_rating": {
                "msci": "BB",
                "description": "传统评级模糊"
            }
        }
    }

try:
    data, is_cofco = load_data(company_info['filename'])
except Exception as e:
    st.error(f"加载数据时出错: {str(e)}")
    data, is_cofco = get_sample_data(), False

# 创建三个标签页
tab1, tab2, tab3 = st.tabs([
    "🎯 风险评估仪表盘", 
    "🔗 供应链冲击分析", 
    "📱 B2C产品溯源"
])

# ========== 第一幕：风险评估仪表盘 ==========
with tab1:
    st.header(f"📊 {data.get('company', '未知公司')} - ESG风险评估")
    
    # 对比传统评级
    col_compare1, col_compare2 = st.columns(2)
    
    with col_compare1:
        traditional_rating = data.get('traditional_rating', {}) or data.get('social', {}).get('traditional_rating', {})
        rating_value = traditional_rating.get('rating', traditional_rating.get('msci', 'N/A'))
        rating_desc = traditional_rating.get('limitation', traditional_rating.get('description', '传统评级模糊'))
        
        st.info(f"**🏢 传统评级（MSCI）**: {rating_value}\n\n{rating_desc}")
    
    with col_compare2:
        st.success("**🌿 绿链评级**: 采用E/S分离评分\n\n"
                   "✅ 精准定位风险来源\n\n"
                   "✅ 基于客观另类数据")
    
    st.markdown("---")
    
    # 两列布局：环境 vs 社会
    col1, col2 = st.columns(2)
    
    # ===== 环境模块 =====
    with col1:
        st.subheader("🌍 环境风险评估 (E)")
        
        env = data.get('environment', {})
        e_score = env.get('risk_score', 0)
        e_level = env.get('risk_level', '未知')
        
        # 显示大号指标
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                label="风险等级",
                value=e_level,
                delta=f"评分: {e_score}/100",
                delta_color="normal" if e_score < 50 else "inverse"
            )
        with metric_col2:
            analysis_method = env.get('analysis', {}).get('method', '卫星遥感')
            if '卫星' in analysis_method or 'Sentinel' in analysis_method:
                st.metric(label="分析方法", value="卫星遥感", delta="Sentinel-2")
            else:
                st.metric(label="分析方法", value="报告审查", delta="企业披露")
        
        # 分析详情
        st.markdown("**📊 分析详情**")
        analysis = env.get('analysis', {})
        
        if is_cofco:
            # COFCO的数据结构
            st.write(f"- **分析周期**: {analysis.get('period', 'N/A')}")
            st.write(f"- **分析方法**: {analysis.get('method', 'N/A')}")
            key_findings = analysis.get('key_findings', [])
            if key_findings:
                st.write("**关键发现**:")
                for finding in key_findings:
                    st.write(f"  - {finding}")
            st.write(f"- **结论**: {analysis.get('conclusion', 'N/A')}")
        else:
            # FGV/IOI的数据结构
            st.write(f"- **分析周期**: {analysis.get('period', 'N/A')}")
            st.write(f"- **分析方法**: {analysis.get('method', 'N/A')}")
            st.write(f"- **关键指标**: {analysis.get('indicator', 'N/A')}")
            st.write(f"- **分析结果**: {analysis.get('result', 'N/A')}")
        
        
        # 显示卫星图片对比（仅上游供应商）
        if not is_cofco:
            st.markdown("**🛰️ 卫星影像对比**")
            
            evidence = analysis.get('evidence', {})
            img_before = evidence.get('satellite_image_before', '')
            img_after = evidence.get('satellite_image_after', '')
            
            # 从JSON获取相对路径
            img_before_path = os.path.join(BASE_DIR, img_before) if img_before else ''
            img_after_path = os.path.join(BASE_DIR, img_after) if img_after else ''
                
            # 使用绝对路径进行检查和显示
            if img_before_path and img_after_path and os.path.exists(img_before_path):
                col_img1, col_img2 = st.columns(2)
                with col_img1:
                    st.image(img_before_path, caption="基准年", use_column_width=True)
                with col_img2:
                    st.image(img_after_path, caption="最近年", use_column_width=True)
                
                # 显示观察结果（IOI特有）—— 这是一个独立逻辑
                observations = evidence.get('observation', [])
                if observations:
                    with st.expander("📝 详细观察记录"):
                        for obs in observations:
                            st.write(f"- {obs}")
            
            else: 
                # 提示信息可以更具体一点
                st.info(f"💡 卫星图片未找到。请确保JSON中的路径 (如: {img_before}) 正确，且文件已上传。")
            
            # 结论 (仍然在 if not is_cofco 内部)
            conclusion = evidence.get('conclusion', analysis.get('conclusion', ''))
            if conclusion:
                st.success(f"✅ **结论**: {conclusion}")
        
        else:
            # COFCO的环境表现
            positive_actions = env.get('positive_actions', [])
            if positive_actions:
                st.markdown("**✅ 积极行动**")
                for action in positive_actions:
                    st.write(f"- {action}")
        
        

        # 合规状态 (这对所有公司都可见，所以它在 if/else 之外)
        st.markdown("**📋 法规合规性**")
        compliance = env.get('compliance', {})
        if compliance:
            st.write(compliance.get('eudr', ''))
            st.write(compliance.get('rspo', ''))
        
        # 认证信息（IOI特有）
        certifications = env.get('certifications', {})
        if certifications:
            rspo = certifications.get('RSPO', {})
            if rspo:
                with st.expander("🏆 RSPO认证状态"):
                    st.write(f"**状态**: {rspo.get('status', 'N/A')}")
                    st.write(f"**认证面积占比**: {rspo.get('certified_area_percentage', 'N/A')}")
                    if rspo.get('suspension_period'):
                        st.warning(f"⚠️ 曾暂停认证: {rspo.get('suspension_period')}")
    
    # ===== 社会模块 =====
    with col2:
        st.subheader("👥 社会风险评估 (S)")
        
        social = data.get('social', {})
        s_score = social.get('risk_score', 0)
        s_level = social.get('risk_level', '未知')
        
        # 显示大号指标
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                label="风险等级",
                value=s_level,
                delta=f"评分: {s_score}/100",
                delta_color="normal" if s_score < 50 else "inverse"
            )
        with metric_col2:
            st.metric(label="分析方法", value="舆情分析", delta="AI爬虫")
        
        # COFCO特有的风险来源说明
        if is_cofco:
            analysis = social.get('analysis', {})
            if analysis:
                st.warning(f"""
                **⚠️ 风险来源分析**
                
                **方法**: {analysis.get('method', 'N/A')}
                
                **主要风险**: {analysis.get('key_concern', 'N/A')}
                
                **风险类型**: {analysis.get('risk_source', '上游供应商传导')}
                """)
        
        # 关键事件列表
        st.markdown("**📰 关键舆情事件**")
        
        key_events = social.get('key_events', [])
        if not key_events:
            st.info("暂无重大舆情事件记录")
        else:
            for idx, event in enumerate(key_events[:5], 1):  # 只显示前5个
                event_title = event.get('event', '未知事件')
                event_date = event.get('date', event.get('year', 'N/A'))
                
                with st.expander(f"事件 {idx}: {event_title[:50]}...", expanded=(idx == 1)):
                    st.write(f"**日期**: {event_date}")
                    
                    # 处理不同的数据结构
                    if 'source' in event:
                        st.write(f"**来源**: {event['source']}")
                    if 'impact' in event:
                        st.write(f"**影响**: {event['impact']}")
                    if 'severity' in event:
                        severity = event['severity']
                        if severity == '严重' or severity == '高':
                            st.error(f"**严重程度**: {severity}")
                        elif severity == '中' or severity == '中等':
                            st.warning(f"**严重程度**: {severity}")
                        else:
                            st.info(f"**严重程度**: {severity}")
                    
                    # IOI的详细信息
                    if 'details' in event:
                        details = event['details']
                        if isinstance(details, list):
                            st.write("**详细信息**:")
                            for detail in details:
                                st.write(f"- {detail}")
                        else:
                            st.write(f"**详细信息**: {details}")
                    
                    if 'url' in event and event['url'] != "#":
                        st.markdown(f"[📎 查看原文]({event['url']})")
        
        # 风险缓解措施（COFCO/IOI）
        risk_mitigation = social.get('risk_mitigation', [])
        improvement_actions = social.get('improvement_actions', [])
        
        if risk_mitigation:
            with st.expander("✅ 风险缓解措施"):
                for action in risk_mitigation:
                    st.write(f"- {action}")
        
        if improvement_actions:
            with st.expander("📈 改进行动"):
                for action in improvement_actions:
                    if isinstance(action, dict):
                        st.write(f"**{action.get('year', 'N/A')}年**: {action.get('action', 'N/A')}")
                    else:
                        st.write(f"- {action}")
        
        # 传统评级对比
        st.markdown("**🔍 传统评级的局限性**")
        traditional_rating = social.get('traditional_rating', {})
        
        st.warning(f"""
        **MSCI评级**: {traditional_rating.get('msci', traditional_rating.get('rating', 'N/A'))}
        
        {traditional_rating.get('description', '传统评级模糊，无法精准识别具体风险')}
        
        ❌ 评级滞后，无法及时反映新发生的重大事件
        ❌ 评级笼统，无法精准定位风险来源
        """)
        
        st.success("""
        **✅ 绿链的优势**
        
        - 实时监控舆情变化
        - 精准定位社会风险事件
        - 提供详细证据链条
        - 可追溯至原始新闻来源
        """)

# ========== 第二幕：供应链冲击分析 ==========
with tab2:
    st.header("🔗 供应链风险冲击分析")
    
    st.markdown("""
    本模块展示绿链的**创新点2**：供应链透视。
    当上游供应商出现ESG风险时，如何影响中游加工商和下游市场。
    """)
    
    st.markdown("---")
    
    # 根据选择的公司展示不同的供应链视图
    if is_cofco:
        # ========== COFCO视角：展示完整的上中下游 ==========
        st.subheader("🏭 中粮集团的供应链风险全景")
        
        supply_chain = data.get('supply_chain', {})
        
        # 三列布局
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🌱 上游供应商")
            
            upstream = supply_chain.get('upstream', {})
            suppliers = upstream.get('suppliers', [])
            
            for supplier in suppliers:
                risk_status = supplier.get('risk_status', '未知')
                
                # 根据风险状态选择颜色
                if '高' in risk_status or '75' in risk_status:
                    st.error(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"⚠️ {risk_status}")
                elif '低' in risk_status:
                    st.success(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"✅ {risk_status}")
                else:
                    st.info(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"ℹ️ {risk_status}")
                
                if supplier.get('note'):
                    st.caption(supplier['note'])
                
                st.markdown("---")
        
        with col2:
            st.markdown("### 🏭 中游加工商（当前）")
            
            st.markdown('<div class="supply-chain-box"><h3>中粮集团</h3><p>中国最大农产品加工企业</p></div>', 
                       unsafe_allow_html=True)
            
            st.write(f"**环境风险**: {data['environment']['risk_score']}分 ({data['environment']['risk_level']})")
            st.write(f"**社会风险**: {data['social']['risk_score']}分 ({data['social']['risk_level']})")
            
            st.info("""
            **供应链曝露**
            
            对FGV等高风险供应商依赖度较高
            
            ⚠️ 需要多元化采购策略
            """)
        
        with col3:
            st.markdown("### 🌍 下游市场")
            
            downstream = supply_chain.get('downstream', {})
            markets = downstream.get('markets', [])
            
            for market in markets:
                if isinstance(market, dict):
                    region = market.get('region', 'N/A')
                    regulation = market.get('regulation', 'N/A')
                    risk = market.get('risk', 'N/A')
                    
                    with st.expander(f"🌐 {region}"):
                        st.write(f"**产品**: {', '.join(market.get('products', []))}")
                        st.write(f"**法规**: {regulation}")
                        if market.get('compliance_deadline'):
                            st.warning(f"⏰ 截止日期: {market['compliance_deadline']}")
                        st.write(f"**风险**: {risk}")
                else:
                    st.write(f"- 🌐 {market}")
        
        # 风险传导路径
        st.markdown("---")
        st.markdown("#### 🔴 风险传导路径")
        
        risk_paths = upstream.get('risk_transmission_path', [])
        if risk_paths:
            for path in risk_paths:
                st.error(f"⚠️ {path}")
        
        # 缓解策略
        st.markdown("---")
        st.subheader("💡 供应链风险缓解策略")
        
        mitigation = supply_chain.get('mitigation_strategy', {})
        
        col_strat1, col_strat2 = st.columns(2)
        
        with col_strat1:
            st.markdown("**⚡ 短期措施**")
            short_term = mitigation.get('short_term', [])
            for action in short_term:
                st.write(f"- {action}")
        
        with col_strat2:
            st.markdown("**🎯 长期策略**")
            long_term = mitigation.get('long_term', [])
            for action in long_term:
                st.write(f"- {action}")
        
        # 合规状态
        st.markdown("---")
        st.subheader("📋 法规合规状态")
        
        regulatory = data.get('regulatory_compliance', {})
        
        if regulatory:
            col_reg1, col_reg2 = st.columns(2)
            
            with col_reg1:
                eudr = regulatory.get('EUDR', {})
                if eudr:
                    st.markdown("**🇪🇺 欧盟EUDR**")
                    st.write(f"**状态**: {eudr.get('status', 'N/A')}")
                    st.write(f"**截止日期**: {eudr.get('deadline', 'N/A')}")
                    st.write(f"**进展**: {eudr.get('progress', 'N/A')}")
            
            with col_reg2:
                cbp = regulatory.get('US_CBP', {})
                if cbp:
                    st.markdown("**🇺🇸 美国CBP**")
                    st.write(f"**状态**: {cbp.get('status', 'N/A')}")
                    st.write(f"**风险**: {cbp.get('risk', 'N/A')}")
                    st.write(f"**行动**: {cbp.get('action', 'N/A')}")
    
    else:
        # ========== 上游供应商视角（FGV/IOI）==========
        st.subheader(f"🌱 {data.get('company', '供应商')}的供应链影响")
        
        supply_chain_data = data.get('supply_chain', {})
        
        # 如果数据中有完整的供应链结构
        if 'upstream' in supply_chain_data or 'midstream' in supply_chain_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🌱 上游（当前）")
                
                st.markdown(f'<div class="supply-chain-box"><h3>{data.get("company", "供应商")}</h3><p>{data.get("industry", "棕榈油生产")}</p></div>', 
                           unsafe_allow_html=True)
                
                st.write(f"**环境风险**: {data['environment']['risk_score']}分")
                st.write(f"**社会风险**: {data['social']['risk_score']}分")
                
                if data['environment']['risk_score'] > 60 or data['social']['risk_score'] > 60:
                    st.error("⚠️ 高风险警报")
            
            with col2:
                st.markdown("### 🏭 中游加工商")
                
                midstream = supply_chain_data.get('midstream', {})
                
                if midstream:
                    if isinstance(midstream, dict):
                        st.write(f"**公司**: {midstream.get('name', 'N/A')}")
                        st.write(f"**位置**: 📍 {midstream.get('location', 'N/A')}")
                        products = midstream.get('products', [])
                        if products:
                            st.write(f"**产品**: {', '.join(products)}")
                        
                        exposure = midstream.get('exposure', '')
                        if exposure:
                            st.info(f"**供应链曝露**: {exposure}")
                    else:
                        st.write(midstream)
                else:
                    st.info("**主要客户**: 中粮集团等国际加工商")
            
            with col3:
                st.markdown("### 🌍 下游市场")
                
                downstream = supply_chain_data.get('downstream', {})
                
                if downstream:
                    if isinstance(downstream, dict):
                        markets = downstream.get('markets', [])
                        for market in markets:
                            st.write(f"- 🌐 {market}")
                        
                        # 显示主要客户（IOI特有）
                        major_customers = downstream.get('major_customers', [])
                        if major_customers:
                            with st.expander("🏢 主要客户"):
                                for customer in major_customers:
                                    st.write(f"- {customer}")
                    else:
                        for market in downstream:
                            st.write(f"- 🌐 {market}")
        
        # 风险传导分析
        st.markdown("---")
        st.markdown("#### 🔴 风险传导影响")
        
        # IOI/FGV的风险传导
        if 'risk_transmission' in supply_chain_data:
            transmission = supply_chain_data['risk_transmission']
            st.write(transmission.get('description', ''))
            
            pathways = transmission.get('pathway', [])
            for pathway in pathways:
                st.error(f"⚠️ {pathway}")
        else:
            # 默认展示
            st.warning(f"""
            **风险传导路径**:
            
            {data.get('company', '供应商')} ({data['social']['risk_level']})
            ⬇️
            中游加工商（受影响）
            ⬇️
            欧盟/美国/中国市场（合规压力）
            """)
        
        # 对下游的建议
        st.markdown("---")
        st.subheader("💼 对下游客户的建议")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("**🔍 立即行动**")
            st.markdown("""
            1. ✅ 评估供应链曝露度
            2. ✅ 寻找替代供应商
            3. ✅ 监督供应商整改进度
            4. ✅ 准备合规文件
            """)
        
        with col_rec2:
            st.markdown("**📊 长期策略**")
            st.markdown("""
            1. 🌿 建立供应商分级体系
            2. 🌿 多元化供应链布局
            3. 🌿 定期ESG审计
            4. 🌿 透明度承诺
            """)
    
    # PDF报告下载（所有公司通用）
    st.markdown("---")
    st.subheader("📥 生成并下载合规报告")
    
    st.info("💡 点击下方按钮生成PDF格式的详细ESG合规报告，可用于内部风控或向客户展示。")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button("📄 生成PDF合规报告", type="primary", use_container_width=True):
            try:
                from utils.pdf_generator import generate_pdf_report
                
                with st.spinner('正在生成PDF报告...'):
                    pdf_buffer = generate_pdf_report(data)
                
                st.download_button(
                    label="⬇️ 下载PDF报告",
                    data=pdf_buffer,
                    file_name=f"{selected_company.replace(' ', '_')}_ESG_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ 报告生成成功！点击上方按钮下载")
                
            except ImportError:
                st.warning("PDF生成模块未找到，请确保 `utils/pdf_generator.py` 存在")
            except Exception as e:
                st.error(f"生成PDF时出错: {str(e)}")

# ========== 第三幕：B2C产品溯源 ==========
with tab3:
    st.header("📱 B2C 可追溯的信任标签")
    
    st.markdown("""
    本模块展示绿链的**创新点3**：B2B2C价值闭环。
    将B端的供应链合规转化为C端消费者可感知的"信任标签"。
    """)
    
    st.markdown("---")
    
    if is_cofco:
        # COFCO视角：展示终端产品
        st.info("💡 **演示场景**: 消费者在超市购买福临门食用油，扫描瓶身上的'绿链认证'二维码，即可查看完整的产品溯源信息。")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🏺 实物演示道具")
            
            st.markdown("""
            **产品**: 福临门食用油（5L装）
            
            **特点**:
            - ✅ 贴有"绿链认证"标签
            - ✅ 印有二维码
            - ✅ 标注"可持续来源"
            """)
            
            # 生成二维码
            try:
                import qrcode
                from io import BytesIO
                
                qr_url = "https://xikai0906.github.io/green-link-demo/"
                
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="green", back_color="white")
                
                buf = BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                
                st.image(buf, caption="扫描查看产品溯源", width=250)
                
                st.caption(f"🔗 链接: {qr_url}")
                
            except ImportError:
                st.warning("需要安装 qrcode 库: `pip install qrcode`")
                st.markdown("```\n[二维码占位符]\n扫描查看溯源信息\n```")
        
        with col2:
            st.subheader("📲 消费者手机端预览")
            
            st.markdown("""
            <div style="border: 3px solid #333; border-radius: 20px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h2 style="text-align: center; margin-bottom: 20px;">🌿 一瓶油的绿色旅程</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 显示供应链溯源
            supply_chain = data.get('supply_chain', {})
            upstream = supply_chain.get('upstream', {})
            suppliers = upstream.get('suppliers', [])
            
            # 原料产地
            with st.container():
                st.markdown("### 🌍 原料产地")
                
                if suppliers:
                    for idx, supplier in enumerate(suppliers[:2], 1):  # 显示前2个供应商
                        col_info1, col_info2 = st.columns([1, 1])
                        
                        with col_info1:
                            st.write(f"**供应商 {idx}**")
                            st.write(f"📍 {supplier.get('country', 'N/A')}")
                            st.write(f"🏭 {supplier.get('name', 'N/A')}")
                        
                        with col_info2:
                            st.write("**风险评估**")
                            risk_status = supplier.get('risk_status', '')
                            if '低' in risk_status:
                                st.success(f"✅ {risk_status}")
                            elif '高' in risk_status:
                                st.warning(f"⚠️ {risk_status}")
                            else:
                                st.info(risk_status)
                        
                        st.markdown("---")
            
            # 加工工厂
            with st.container():
                st.markdown("### 🏭 加工工厂")
                
                st.write(f"**生产商**: {data.get('company', 'N/A')}")
                st.write(f"**工厂位置**: 📍 {data.get('headquarters', 'N/A')}")
                
                st.success("""
                **质量认证**:
                - ✅ ISO 22000 食品安全管理
                - ✅ HACCP 危害分析
                - ✅ 绿链ESG认证
                """)
            
            st.markdown("---")
            
            # 可持续认证
            with st.container():
                st.markdown("### 📋 可持续认证")
                
                st.write(f"✅ 绿链ESG环境风险评估：{data['environment']['risk_level']} ({data['environment']['risk_score']}分)")
                st.write(f"✅ 绿链ESG社会风险评估：{data['social']['risk_level']} ({data['social']['risk_score']}分)")
                st.write("✅ 供应链透明度认证")
            
            st.markdown("---")
            
            # 感谢信息
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;">
                <h3>❤️ 感谢您的选择</h3>
                <p>每一次购买绿链认证产品，都是对可持续发展的支持！</p>
                <p><small>由 GreenLink 技术驱动 | 基于卫星遥感和AI分析</small></p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # 上游供应商视角：展示B2B价值
        st.info(f"💡 {data.get('company', '供应商')}作为上游供应商，可以通过绿链认证提升品牌价值，获得下游客户信任。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 B2B价值")
            
            b2b_value = data.get('b2b_value', {})
            
            for_buyers = b2b_value.get('for_buyers', [])
            if for_buyers:
                st.markdown("**对采购商的价值**")
                for value in for_buyers:
                    st.write(f"✅ {value}")
            
            for_investors = b2b_value.get('for_investors', [])
            if for_investors:
                st.markdown("**对投资者的价值**")
                for value in for_investors:
                    st.write(f"📊 {value}")
        
        with col2:
            st.markdown("### 👥 B2C价值")
            
            b2c_value = data.get('b2c_value', {})
            
            st.write(f"**信任标签**: {b2c_value.get('consumer_trust_label', '绿链ESG认证')}")
            st.write(f"**溯源方式**: {b2c_value.get('qr_code_traceability', '二维码扫描')}")
            
            messaging = b2c_value.get('messaging', '')
            if messaging:
                st.info(messaging)

# 侧边栏底部信息
st.sidebar.markdown("---")
st.sidebar.subheader("📚 关于绿链 GreenLink")

st.sidebar.markdown("""
**🎯 三大创新点**

1️⃣ **另类数据 + AI分析**
- 🛰️ Sentinel-2卫星遥感
- 📰 公开舆情数据挖掘
- 🤖 Python自动化分析

2️⃣ **E/S分离评分**
- 环境(E)：卫星验证
- 社会(S)：舆情分析
- 精准定位风险来源

3️⃣ **B2B2C价值闭环**
- B端：风险预警
- B端：合规报告
- C端：信任标签
""")

st.sidebar.markdown("---")

# 绿链优势展示
if 'greenlink_advantage' in data:
    advantage = data['greenlink_advantage']
    
    with st.sidebar.expander("🌟 绿链优势"):
        vs_traditional = advantage.get('vs_traditional_rating', [])
        for item in vs_traditional:
            st.write(f"- {item}")
        
        real_time = advantage.get('real_time_monitoring', [])
        if real_time:
            st.markdown("**实时监控**:")
            for item in real_time:
                st.write(f"- {item}")

st.sidebar.info("""
**💻 技术栈**
- Streamlit: Web应用框架
- Python: 数据分析
- Sentinel-2: 卫星数据
- ReportLab: PDF生成
- GitHub Pages: B2C部署

**📊 数据更新**
每周自动更新
""")

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 GreenLink | 创新创业大赛DEMO")
st.sidebar.caption("ysuy5756@gmail.com | RIELY | GXUFE")
