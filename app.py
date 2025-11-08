#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import json
import pandas as pd
from PIL import Image
import os

# 页面配置
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
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #27ae60;
    }
    .risk-high {
        color: #e74c3c;
        font-weight: bold;
    }
    .risk-low {
        color: #27ae60;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<p class="main-header">🌿 绿链 GreenLink</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">基于另类数据的供应链ESG风险评估平台</p>', unsafe_allow_html=True)

# 侧边栏：选择公司
st.sidebar.header("🎯 选择分析对象")
st.sidebar.markdown("---")

companies = {
    "FGV Holdings Berhad": "FGV.json",
    "IOI Corporation": "IOI.json",
    "中粮集团": "COFCO.json"
}

selected_company = st.sidebar.selectbox(
    "供应商",
    list(companies.keys()),
    help="选择要分析的供应链企业"
)

# 加载数据
@st.cache_data
def load_data(filename):
    file_path = f'data/{filename}'
    if not os.path.exists(file_path):
        st.warning(f"数据文件 {filename} 未找到，显示示例数据")
        return get_sample_data()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_sample_data():
    """返回示例数据结构"""
    return {
        "company": "示例公司",
        "environment": {
            "risk_level": "低风险",
            "risk_score": 25,
            "status": "✅",
            "analysis": {
                "method": "Sentinel-2 卫星影像分析",
                "period": "2014-2022",
                "indicator": "森林覆盖变化率",
                "result": "未检测到大规模毁林活动",
                "evidence": {
                    "satellite_image_before": "",
                    "satellite_image_after": "",
                    "ndvi_change": -2.3,
                    "conclusion": "种植园边界稳定，无新增毁林证据"
                }
            },
            "compliance": {
                "eudr": "✅ 符合欧盟EUDR法规（无毁林）",
                "rspo": "⚠️ 部分认证暂停"
            }
        },
        "social": {
            "risk_level": "高风险",
            "risk_score": 75,
            "status": "⚠️",
            "key_events": [
                {
                    "date": "2020-09-30",
                    "event": "示例风险事件",
                    "source": "示例来源",
                    "impact": "示例影响",
                    "url": "#"
                }
            ],
            "traditional_rating": {
                "msci": "BB",
                "description": "传统评级模糊，无法精准识别具体风险"
            }
        },
        "supply_chain": {
            "upstream": {
                "name": "示例供应商",
                "role": "原料供应商",
                "location": "示例地区",
                "risk_alert": True
            },
            "midstream": {
                "name": "示例加工商",
                "role": "加工商",
                "location": "中国",
                "products": ["示例产品"],
                "exposure": "示例占比"
            },
            "downstream": {
                "markets": ["欧盟", "美国", "中国"],
                "regulations": {
                    "eu": "EUDR法规要求零毁林证明",
                    "us": "示例监管要求",
                    "china": "消费者关注可持续性"
                }
            },
            "impact_alert": {
                "severity": "高",
                "message": "示例风险警报信息"
            }
        }
    }

try:
    data = load_data(companies[selected_company])
except Exception as e:
    st.error(f"加载数据时出错: {str(e)}")
    data = get_sample_data()

# 创建三个标签页
tab1, tab2, tab3 = st.tabs([
    "🎯 风险评估仪表盘", 
    "🔗 供应链冲击分析", 
    "📱 B2C产品溯源"
])

# ========== 第一幕：风险评估仪表盘 ==========
with tab1:
    st.header(f"📊 {data['company']} - ESG风险评估")
    
    # 对比传统评级
    col_compare1, col_compare2 = st.columns(2)
    
    with col_compare1:
        st.info(f"**🏢 传统评级（MSCI）**: {data['social']['traditional_rating']['msci']}\n\n"
                f"{data['social']['traditional_rating']['description']}")
    
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
        
        # 风险评分卡片
        e_score = data['environment']['risk_score']
        e_level = data['environment']['risk_level']
        
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
            st.metric(
                label="分析方法",
                value="卫星遥感",
                delta="Sentinel-2"
            )
        
        # 分析详情
        st.markdown("**📊 分析详情**")
        st.write(f"- **分析周期**: {data['environment']['analysis']['period']}")
        st.write(f"- **分析方法**: {data['environment']['analysis']['method']}")
        st.write(f"- **关键指标**: {data['environment']['analysis']['indicator']}")
        st.write(f"- **分析结果**: {data['environment']['analysis']['result']}")
        
        # 显示卫星图片对比
        st.markdown("**🛰️ 卫星影像对比**")
        
        img_before = data['environment']['analysis']['evidence']['satellite_image_before']
        img_after = data['environment']['analysis']['evidence']['satellite_image_after']
        
        if img_before and img_after and os.path.exists(img_before):
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(img_before, caption="2014年", use_column_width=True)
            with col_img2:
                st.image(img_after, caption="2022年", use_column_width=True)
        else:
            st.info("💡 卫星图片文件未上传。请将图片放置在 `assets/satellite_images/` 目录下")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.markdown("```\n📷 2014年卫星图\n（待上传）\n```")
            with col_img2:
                st.markdown("```\n📷 2022年卫星图\n（待上传）\n```")
        
        # 结论
        st.success(f"✅ **结论**: {data['environment']['analysis']['evidence']['conclusion']}")
        
        # 合规状态
        st.markdown("**📋 法规合规性**")
        st.write(data['environment']['compliance']['eudr'])
        st.write(data['environment']['compliance']['rspo'])
    
    # ===== 社会模块 =====
    with col2:
        st.subheader("👥 社会风险评估 (S)")
        
        s_score = data['social']['risk_score']
        s_level = data['social']['risk_level']
        
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
            st.metric(
                label="分析方法",
                value="舆情分析",
                delta="AI爬虫"
            )
        
        # 关键事件列表
        st.markdown("**📰 关键舆情事件**")
        
        for idx, event in enumerate(data['social']['key_events'], 1):
            with st.expander(f"事件 {idx}: {event['event'][:50]}...", expanded=(idx == 1)):
                st.write(f"**日期**: {event['date']}")
                st.write(f"**来源**: {event['source']}")
                st.write(f"**影响**: {event['impact']}")
                
                if event['url'] != "#":
                    st.markdown(f"[📎 查看原文]({event['url']})")
        
        # 传统评级对比
        st.markdown("**🔍 传统评级的局限性**")
        st.warning(f"""
        **MSCI评级**: {data['social']['traditional_rating']['msci']}
        
        {data['social']['traditional_rating']['description']}
        
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
    
    # 三列布局：上游 -> 中游 -> 下游
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌱 上游供应商")
        
        upstream = data['supply_chain']['upstream']
        
        if upstream['risk_alert']:
            st.error(f"**⚠️ 风险警报**")
        
        st.write(f"**公司名称**: {upstream['name']}")
        st.write(f"**角色**: {upstream['role']}")
        st.write(f"**位置**: 📍 {upstream['location']}")
        
        st.warning(f"""
        **发现问题**:
        - 环境: {data['environment']['risk_level']} ({data['environment']['risk_score']}分)
        - 社会: {data['social']['risk_level']} ({data['social']['risk_score']}分)
        """)
    
    with col2:
        st.markdown("### 🏭 中游加工商")
        
        midstream = data['supply_chain']['midstream']
        
        st.write(f"**公司名称**: {midstream['name']}")
        st.write(f"**角色**: {midstream['role']}")
        st.write(f"**位置**: 📍 {midstream['location']}")
        st.write(f"**主要产品**: {', '.join(midstream['products'])}")
        
        st.info(f"""
        **供应链曝露度**
        
        上游供应商占比: {midstream['exposure']}
        
        ⚠️ 高度依赖该供应商
        """)
    
    with col3:
        st.markdown("### 🌍 下游市场")
        st.success("**目标市场**")
        for market in data['supply_chain']['downstream']['markets']:
            st.write(f"- 🌐 {market}")
    
    # 风险传导流程图
    st.markdown("---")
    st.markdown("#### 🔴 风险传导路径")
    
    st.markdown(f"""
```
    {data['supply_chain']['upstream']['name']} (高风险)
            ⬇️  原料供应
    {data['supply_chain']['midstream']['name']} (受影响)
            ⬇️  产品出口
    {'  ⬇️  '.join(data['supply_chain']['downstream']['markets'])} (市场风险)
```
    """)
    
    # 风险警报
    st.markdown("---")
    st.subheader("⚠️ 风险冲击警报")
    
    alert_severity = data['supply_chain']['impact_alert']['severity']
    alert_message = data['supply_chain']['impact_alert']['message']
    
    if alert_severity == "高":
        st.error(f"**🚨 高风险警报**\n\n{alert_message}")
    elif alert_severity == "中":
        st.warning(f"**⚠️ 中风险警报**\n\n{alert_message}")
    else:
        st.info(f"**ℹ️ 低风险提示**\n\n{alert_message}")
    
    # 法规影响分析
    st.markdown("---")
    st.subheader("📋 目标市场法规影响分析")
    
    regs = data['supply_chain']['downstream']['regulations']
    
    reg_cols = st.columns(len(regs))
    
    for idx, (region, desc) in enumerate(regs.items()):
        with reg_cols[idx]:
            region_name = {
                'eu': '🇪🇺 欧盟',
                'us': '🇺🇸 美国',
                'china': '🇨🇳 中国'
            }.get(region, region)
            
            with st.expander(region_name, expanded=True):
                st.write(desc)
    
    # 推荐措施
    st.markdown("---")
    st.subheader("💼 推荐应对措施")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("**🔍 立即行动**")
        st.markdown("""
        1. ✅ 启动供应商ESG审计
        2. ✅ 评估替代供应商
        3. ✅ 与现有供应商沟通整改
        4. ✅ 准备应急采购方案
        """)
    
    with col_rec2:
        st.markdown("**📊 长期策略**")
        st.markdown("""
        1. 🌿 建立供应商ESG监控体系
        2. 🌿 多元化供应链布局
        3. 🌿 提升供应链透明度
        4. 🌿 获取绿链认证增强竞争力
        """)
    
    # PDF报告下载
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
                    file_name=f"{selected_company}_ESG_Report.pdf",
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
            
            qr_url = "https://github.com/xikai0906/green-link-demo/"
            
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
        
        # 原料产地
        with st.container():
            st.markdown("### 🌍 原料产地")
            
            col_info1, col_info2 = st.columns([1, 1])
            
            with col_info1:
                st.write("**种植园位置**")
                st.write(f"📍 {data['supply_chain']['upstream']['location']}")
                st.write(f"🏭 {data['supply_chain']['upstream']['name']}")
            
            with col_info2:
                st.write("**卫星验证结果**")
                st.success(f"✅ {data['environment']['risk_level']}")
                st.write(f"✅ {data['environment']['analysis']['evidence']['conclusion'][:50]}...")
            
            img_after = data['environment']['analysis']['evidence']['satellite_image_after']
            if img_after and os.path.exists(img_after):
                st.image(img_after, caption="卫星验证图", use_column_width=True)
        
        st.markdown("---")
        
        # 加工工厂
        with st.container():
            st.markdown("### 🏭 加工工厂")
            
            st.write(f"**生产商**: {data['supply_chain']['midstream']['name']}")
            st.write(f"**工厂位置**: 📍 {data['supply_chain']['midstream']['location']}")
            st.write(f"**产品**: {', '.join(data['supply_chain']['midstream']['products'])}")
            
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
            
            st.write(f"✅ 绿链ESG风险评估：{data['environment']['risk_level']}")
            st.write("✅ 供应链透明度认证")
            st.write(data['environment']['compliance']['eudr'])
        
        st.markdown("---")
        
        # 感谢信息
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;">
            <h3>❤️ 感谢您的选择</h3>
            <p>每一次购买绿链认证产品，都是对可持续发展的支持！</p>
            <p><small>由 GreenLink 技术驱动 | 基于卫星遥感和AI分析</small></p>
        </div>
        """, unsafe_allow_html=True)

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
st.sidebar.caption("© 2024 GreenLink | 创新创业大赛DEMO")
