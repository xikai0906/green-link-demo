from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 字体文件名配置
FONT_REGULAR_NAME = 'AlibabaPuHuiTi-3-55-Regular.ttf'
FONT_BOLD_NAME = 'AlibabaPuHuiTi-3-85-Bold.ttf'

# 构建字体文件完整路径
FONT_REGULAR_PATH = os.path.join(BASE_DIR, 'fonts', FONT_REGULAR_NAME)
FONT_BOLD_PATH = os.path.join(BASE_DIR, 'fonts', FONT_BOLD_NAME)

FONT_REG = None
FONT_BOLD = None
FONT_LOADED = False

print("\n" + "="*70)
print("绿链 PDF 生成器 - 字体加载模块")
print("GreenLink PDF Generator - Font Loading Module")
print("="*70)
print(f"字体目录 (Font directory): {os.path.join(BASE_DIR, 'fonts')}")
print(f"常规字体 (Regular font): {FONT_REGULAR_NAME}")
print(f"粗体字体 (Bold font): {FONT_BOLD_NAME}")
print("-"*70)

# 尝试加载阿里巴巴普惠体
try:
    # 检查字体文件是否存在
    if not os.path.exists(FONT_REGULAR_PATH):
        raise FileNotFoundError(f"常规字体文件不存在: {FONT_REGULAR_PATH}")
    
    if not os.path.exists(FONT_BOLD_PATH):
        raise FileNotFoundError(f"粗体字体文件不存在: {FONT_BOLD_PATH}")
    
    # 获取文件大小（用于验证）
    regular_size = os.path.getsize(FONT_REGULAR_PATH) / 1024  # KB
    bold_size = os.path.getsize(FONT_BOLD_PATH) / 1024  # KB
    
    print(f"✓ 找到常规字体: {regular_size:.1f} KB")
    print(f"✓ 找到粗体字体: {bold_size:.1f} KB")
    print("-"*70)
    
    # 注册字体到 ReportLab
    print("正在注册字体到 ReportLab...")
    pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Regular', FONT_REGULAR_PATH))
    pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Bold', FONT_BOLD_PATH))
    
    FONT_REG = "AlibabaPuHuiTi-Regular"
    FONT_BOLD = "AlibabaPuHuiTi-Bold"
    FONT_LOADED = True
    
    print("✓✓✓ 成功：阿里巴巴普惠体加载成功！")
    print("✓✓✓ SUCCESS: Alibaba PuHuiTi fonts loaded successfully!")
    print("="*70 + "\n")
    
except FileNotFoundError as e:
    print(f"✗✗✗ 错误 (ERROR): {e}")
    print("请确保字体文件位于正确的 'fonts' 文件夹中。")
    print("Please ensure font files are in the correct 'fonts' folder.")
    print("="*70 + "\n")
    FONT_REG = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    
except Exception as e:
    print(f"✗✗✗ 字体加载失败 (Font loading FAILED): {e}")
    print("PDF 将使用英文字体，中文可能显示异常。")
    print("PDF will use English fonts, Chinese may display incorrectly.")
    print("="*70 + "\n")
    FONT_REG = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

# ============================================================
# 颜色配置
# ============================================================
COLOR_PRIMARY = HexColor("#27ae60")      # 绿链主色 - 绿色
COLOR_TITLE = HexColor("#2c3e50")        # 标题色 - 深蓝灰
COLOR_TEXT = HexColor("#333333")         # 正文色 - 深灰
COLOR_SUBTLE = HexColor("#7f8c8d")       # 次要文字 - 中灰
RISK_LOW = HexColor("#27ae60")           # 低风险 - 绿色
RISK_MEDIUM = HexColor("#f39c12")        # 中风险 - 橙色
RISK_HIGH = HexColor("#e74c3c")          # 高风险 - 红色

# ============================================================
# 页面布局配置
# ============================================================
WIDTH, HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = WIDTH - 2 * cm
Y_START = HEIGHT - 2.5 * cm

# 图标字符（阿里巴巴普惠体支持常见符号）
ICON_CHECK = "√"   # 勾选标记
ICON_BULLET = "•"  # 项目符号
ICON_ARROW = "→"   # 箭头

# ============================================================
# 辅助绘图函数
# ============================================================

def draw_section_header(c, y, cn_title, en_title, color):
    """
    绘制双语章节标题
    Draw bilingual section header
    """
    if y < 6 * cm:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        y = Y_START
    
    # 中文标题
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(color)
    c.drawString(MARGIN_LEFT, y, cn_title)
    
    # 英文副标题
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT, y - 0.5*cm, en_title)
    
    # 分隔线
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(MARGIN_LEFT, y - 0.8*cm, MARGIN_RIGHT, y - 0.8*cm)
    
    return y - 1.8*cm


def draw_bilingual_field(c, y, cn_label, en_label, value_text, value_color=COLOR_TEXT):
    """
    绘制双语字段（标签 + 值）
    Draw bilingual field (label + value)
    """
    if y < 4 * cm:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        y = Y_START
    
    # 中文标签
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, cn_label)
    
    # 英文标签
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, en_label)
    
    # 字段值（支持自动换行）
    c.setFont(FONT_REG, 10)
    c.setFillColor(value_color)
    
    max_width = 12 * cm
    line = ""
    start_y = y
    
    # 处理列表或字符串值
    if isinstance(value_text, (list, tuple)):
        value_str = ", ".join(str(v) for v in value_text)
    else:
        value_str = str(value_text)
    
    # 自动换行逻辑
    for char in value_str:
        test_line = line + char
        if c.stringWidth(test_line, FONT_REG, 10) > max_width:
            c.drawString(MARGIN_LEFT + 5.5*cm, y, line)
            y -= 0.5*cm
            line = char
        else:
            line = test_line
    
    # 绘制最后一行
    if line:
        c.drawString(MARGIN_LEFT + 5.5*cm, y, line)
    
    return min(y - 0.8*cm, start_y - 0.8*cm)


def draw_wrapped_block(c, y, text_list, font_name=None, font_size=10):
    """
    绘制自动换行的文本块
    Draw text block with automatic line wrapping
    """
    if font_name is None:
        font_name = FONT_REG
    
    c.setFont(font_name, font_size)
    c.setFillColor(COLOR_TEXT)
    max_width = MARGIN_RIGHT - MARGIN_LEFT - 1*cm
    
    for item in text_list:
        if y < 4 * cm:
            c.showPage()
            draw_footer(c, c.getPageNumber())
            y = Y_START
        
        item_str = str(item)
        line = ""
        
        # 逐字符处理换行
        for char in item_str:
            test_line = line + char
            if c.stringWidth(test_line, font_name, font_size) > max_width:
                c.drawString(MARGIN_LEFT + 1*cm, y, line)
                y -= (font_size * 1.2) / 72 * cm
                line = char
            else:
                line = test_line
        
        # 绘制最后一行
        if line:
            c.drawString(MARGIN_LEFT + 1*cm, y, line)
        
        y -= (font_size * 1.4) / 72 * cm
    
    return y


def set_risk_color(c, level, score):
    """
    根据风险级别设置颜色
    Set color based on risk level
    """
    level_str = str(level).lower()
    
    if "低" in level_str or "low" in level_str or score < 40:
        c.setFillColor(RISK_LOW)
        return RISK_LOW
    elif "中" in level_str or "medium" in level_str or score < 70:
        c.setFillColor(RISK_MEDIUM)
        return RISK_MEDIUM
    else:
        c.setFillColor(RISK_HIGH)
        return RISK_HIGH


def draw_footer(c, page_num):
    """
    绘制页脚
    Draw page footer
    """
    c.setFont(FONT_REG, 8)
    c.setFillColor(COLOR_SUBTLE)
    c.drawCentredString(WIDTH/2, 1.5*cm, 
                       f"第 {page_num} 页 (Page {page_num}) | 秘密文件 (Confidential)")
    c.drawCentredString(WIDTH/2, 1*cm, 
                       "由绿链 (GreenLink) 平台生成 | Based on Satellite & AI Analysis")


# ============================================================
# 主生成函数
# ============================================================

def generate_pdf_report(data):
    """
    生成 ESG 合规报告 PDF
    Generate ESG Compliance Report PDF
    
    Args:
        data (dict): 包含公司ESG数据的字典
        
    Returns:
        BytesIO: PDF文件的字节流
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f"{data.get('company', 'Report')} - ESG Report")
    
    # 验证字体加载状态
    if not FONT_LOADED:
        print("\n⚠️  警告：字体未正确加载，PDF中的中文可能显示异常！")
        print("⚠️  WARNING: Fonts not loaded properly, Chinese may not display correctly!\n")
    
    # 提取数据
    company_name = data.get('company', '未知公司')
    is_cofco = 'COFCO' in company_name or '中粮' in company_name
    env_data = data.get('environment', {})
    social_data = data.get('social', {})
    supply_chain_data = data.get('supply_chain', {})
    page_num = 1
    
    # ==================================================
    # 第一页：封面
    # Cover Page
    # ==================================================
    
    # 顶部绿色背景条
    c.setFillColor(COLOR_PRIMARY)
    c.rect(0, HEIGHT - 5*cm, WIDTH, 5*cm, fill=True, stroke=False)
    
    # 主标题 - 绿链
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(FONT_BOLD, 32)
    c.drawCentredString(WIDTH/2, HEIGHT - 2.8*cm, "绿链 (GreenLink)")
    
    # 副标题
    c.setFont(FONT_REG, 16)
    c.drawCentredString(WIDTH/2, HEIGHT - 3.8*cm, 
                       "ESG 风险评估报告 (ESG Risk Assessment Report)")
    
    # 公司名称
    c.setFillColor(COLOR_TITLE)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(WIDTH/2, HEIGHT - 7.5*cm, company_name)
    
    # 报告基本信息
    y = HEIGHT - 10*cm
    c.setFont(FONT_REG, 11)
    c.drawCentredString(WIDTH/2, y, 
                       f"报告日期 (Report Date): {datetime.now().strftime('%Y-%m-%d')}")
    y -= 0.6*cm
    
    # 公司类型判断
    if is_cofco:
        company_type_cn = "中游加工商 / 采购商"
        company_type_en = "Midstream Processor / Buyer"
    else:
        company_type_cn = "上游供应商 / 种植商"
        company_type_en = "Upstream Supplier / Plantation"
    
    c.drawCentredString(WIDTH/2, y, 
                       f"公司类型 (Company Type): {company_type_cn} ({company_type_en})")
    y -= 0.6*cm
    
    period = env_data.get('analysis', {}).get('period', 'N/A')
    c.drawCentredString(WIDTH/2, y, 
                       f"评估周期 (Assessment Period): {period}")
    
    # --- 风险等级概览 ---
    y = HEIGHT - 15*cm
    y = draw_section_header(c, y, "风险等级概览", "Risk Level Overview", COLOR_PRIMARY)
    
    # 环境风险 (E)
    e_level = env_data.get('risk_level', '未知')
    e_score = env_data.get('risk_score', 0)
    e_color = set_risk_color(c, e_level, e_score)
    y = draw_bilingual_field(c, y, "环境风险 (E)", "Environmental Risk (E)", 
                             f"{e_level} ({e_score}/100)", value_color=e_color)
    
    # 社会风险 (S)
    s_level = social_data.get('risk_level', '未知')
    s_score = social_data.get('risk_score', 0)
    s_color = set_risk_color(c, s_level, s_score)
    y = draw_bilingual_field(c, y, "社会风险 (S)", "Social Risk (S)", 
                             f"{s_level} ({s_score}/100)", value_color=s_color)
    
    # --- 平台优势 ---
    y -= 1*cm
    y = draw_section_header(c, y, "绿链评估优势", "GreenLink Advantage", COLOR_TITLE)
    
    advantages = [
        (f"{ICON_CHECK} 实时卫星监控 (E)", "Real-time satellite monitoring (Environment)"),
        (f"{ICON_CHECK} AI驱动舆情分析 (S)", "AI-powered sentiment analysis (Social)"),
        (f"{ICON_CHECK} E/S分离评分", "Separated E/S risk scoring for precision"),
        (f"{ICON_CHECK} 欧盟EUDR合规验证", "EU Deforestation Regulation (EUDR) validation")
    ]
    
    c.setFont(FONT_REG, 10)
    for cn_adv, en_adv in advantages:
        c.setFillColor(COLOR_TEXT)
        c.drawString(MARGIN_LEFT + 0.5*cm, y, cn_adv)
        c.setFillColor(COLOR_SUBTLE)
        c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, en_adv)
        y -= 0.8*cm
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # 第二页：环境风险分析 (E)
    # Environmental Risk Analysis
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "环境风险分析 (E)", 
                           "Environmental Risk Analysis (E)", COLOR_PRIMARY)
    
    env_analysis = env_data.get('analysis', {})
    
    y = draw_bilingual_field(c, y, "分析方法", "Analysis Method", 
                            env_analysis.get('method', 'N/A'))
    y = draw_bilingual_field(c, y, "分析周期", "Analysis Period", 
                            env_analysis.get('period', 'N/A'))
    
    # 关键发现
    y -= 0.5*cm
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "关键发现 / 结论")
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Findings / Conclusion")
    y -= 1*cm
    
    if is_cofco:
        findings = env_analysis.get('key_findings', ['N/A'])
        y = draw_wrapped_block(c, y, [f"{ICON_BULLET} {f}" for f in findings])
        y -= 0.5*cm
        conclusion_text = f"结论: {env_analysis.get('conclusion', 'N/A')}"
        y = draw_wrapped_block(c, y, [conclusion_text], FONT_BOLD, 10)
    else:
        evidence = env_analysis.get('evidence', {})
        conclusion = evidence.get('conclusion', env_analysis.get('result', 'N/A'))
        y = draw_wrapped_block(c, y, [conclusion])
    
    # 法规合规性
    y -= 1*cm
    y = draw_bilingual_field(c, y, "法规合规性", "Regulatory Compliance", "")
    
    compliance = env_data.get('compliance', {})
    if compliance:
        y = draw_wrapped_block(c, y, [f"{ICON_BULLET} {v}" for v in compliance.values()])
    else:
        y = draw_wrapped_block(c, y, [f"{ICON_BULLET} 无数据 (No data)"])
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # 第三页：社会风险分析 (S)
    # Social Risk Analysis
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "社会风险分析 (S)", 
                           "Social Risk Analysis (S)", RISK_HIGH)
    
    if is_cofco:
        social_analysis = social_data.get('analysis', {})
        y = draw_bilingual_field(c, y, "风险来源", "Risk Source", 
                                social_analysis.get('risk_source', 'N/A'))
        y = draw_bilingual_field(c, y, "关键问题", "Key Concern", "")
        y = draw_wrapped_block(c, y, [social_analysis.get('key_concern', 'N/A')])
        y -= 1*cm
    
    # 关键风险事件
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "关键风险事件")
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Risk Events")
    y -= 1*cm
    
    key_events = social_data.get('key_events', [])
    if not key_events:
        y = draw_wrapped_block(c, y, 
                              ["未发现重大负面舆情事件 (No significant negative events found)"])
    
    for event in key_events[:4]:  # 最多显示4个事件
        if y < 8 * cm:
            c.showPage()
            draw_footer(c, page_num)
            page_num += 1
            y = Y_START
            y = draw_section_header(c, y, "社会风险分析 (S) - 续", 
                                  "Social Risk Analysis (S) - Cont.", RISK_HIGH)
            c.setFont(FONT_BOLD, 10)
            c.setFillColor(COLOR_TITLE)
            c.drawString(MARGIN_LEFT + 0.5*cm, y, "关键风险事件 (续)")
            c.setFont(FONT_REG, 9)
            c.setFillColor(COLOR_SUBTLE)
            c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Risk Events (Cont.)")
            y -= 1*cm
        
        event_date = event.get('date', event.get('year', 'N/A'))
        event_text = event.get('event', 'N/A')
        event_impact = event.get('impact', 'N/A')
        
        y = draw_bilingual_field(c, y, "日期 (Date)", "", event_date)
        y = draw_bilingual_field(c, y, "事件 (Event)", "", "")
        y = draw_wrapped_block(c, y, [event_text], font_size=9)
        y = draw_bilingual_field(c, y, "影响 (Impact)", "", "")
        y = draw_wrapped_block(c, y, [event_impact], font_size=9)
        
        c.line(MARGIN_LEFT, y, MARGIN_RIGHT, y)
        y -= 0.5*cm
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # 第四页：供应链分析与建议措施
    # Supply Chain Analysis & Recommendations
    # ==================================================
    
    y = Y_START
    
    # 供应链分析
    if supply_chain_data:
        y = draw_section_header(c, y, "供应链分析", "Supply Chain Analysis", COLOR_TITLE)
        
        if is_cofco:
            suppliers = supply_chain_data.get('upstream', {}).get('suppliers', [])
            y = draw_wrapped_block(c, y, 
                                 ["已识别上游高风险供应商 (High-risk upstream suppliers identified):"], 
                                 FONT_BOLD, 10)
            
            for supplier in suppliers[:3]:
                name = supplier.get('name', 'N/A')
                status = supplier.get('risk_status', 'N/A')
                color = set_risk_color(c, status, 100 if '高' in status else 30)
                y = draw_bilingual_field(c, y, f"{ICON_BULLET} {name}", "", 
                                       status, value_color=color)
        else:
            markets = supply_chain_data.get('downstream', {}).get('markets', [])
            y = draw_wrapped_block(c, y, 
                                 ["下游市场合规风险 (Downstream Market Compliance Risk):"], 
                                 FONT_BOLD, 10)
            y = draw_wrapped_block(c, y, 
                                 [f"{ICON_BULLET} 主要市场 (Target Markets): {', '.join(markets)}"])
            y = draw_wrapped_block(c, y, 
                                 [f"{ICON_BULLET} 风险点 (Risk): 欧盟EUDR及美国CBP法规 (EUDR & US CBP Regulations)"])
        
        y -= 1*cm
    
    # 建议措施
    y = draw_section_header(c, y, "建议措施", "Recommended Actions", COLOR_PRIMARY)
    
    if is_cofco:
        recs = [
            "1. 启动对高风险供应商的详细尽职调查。(Conduct due diligence on high-risk suppliers.)",
            "2. 准备EUDR合规文件，确保上游数据可追溯。(Prepare EUDR documentation, ensure traceability.)",
            "3. 增加对低风险供应商的采购比例。(Increase procurement from low-risk suppliers.)"
        ]
    else:
        recs = [
            "1. 立即提交CBP（劳工问题）或EUDR（毁林问题）整改报告。(Submit CBP/EUDR remediation report.)",
            "2. 实施并披露劳工/环境整改措施。(Implement and disclose remediation actions.)",
            "3. 建立透明的申诉机制。(Establish a transparent grievance mechanism.)"
        ]
    
    y = draw_wrapped_block(c, y, recs)
    
    # 联系信息
    y -= 2*cm
    c.setFont(FONT_BOLD, 11)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT, y, "联系我们 (Contact Us):")
    y -= 0.6*cm
    
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_TEXT)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "绿链 GreenLink ESG 平台")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "邮箱 (Email): support@greenlink.com")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "网站 (Website): www.greenlink.com (Demo)")
    
    draw_footer(c, page_num)
    
    # 保存 PDF
    c.save()
    buffer.seek(0)
    
    print(f"\n✓ PDF 生成成功！共 {page_num} 页")
    print(f"✓ PDF generated successfully! Total {page_num} pages\n")
    
    return buffer


# ============================================================
# 测试函数
# ============================================================

def test_generate_sample_pdf():
    """
    生成测试 PDF
    Generate test PDF
    """
    sample_data = {
        'company': '测试公司 Test Company',
        'environment': {
            'risk_level': '低风险',
            'risk_score': 25,
            'analysis': {
                'method': '卫星影像分析',
                'period': '2023-2024',
                'conclusion': '未发现森林砍伐迹象'
            },
            'compliance': {
                'eudr': '符合欧盟EUDR法规'
            }
        },
        'social': {
            'risk_level': '中风险',
            'risk_score': 55,
            'key_events': [
                {
                    'date': '2024-01',
                    'event': '测试事件',
                    'impact': '中等影响'
                }
            ]
        },
        'supply_chain': {}
    }
    
    pdf_buffer = generate_pdf_report(sample_data)
    
    # 保存测试文件
    with open('/tmp/test_report.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print("测试 PDF 已保存到: /tmp/test_report.pdf")
    print("Test PDF saved to: /tmp/test_report.pdf")


if __name__ == "__main__":
    test_generate_sample_pdf()
