from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ============================================================
# 字体配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(BASE_DIR, 'fonts')

FONT_REG = None
FONT_BOLD = None

try:
    regular_path = os.path.join(FONT_DIR, 'AlibabaPuHuiTi-3-55-Regular.ttf')
    bold_path = os.path.join(FONT_DIR, 'AlibabaPuHuiTi-3-85-Bold.ttf')
    
    if os.path.exists(regular_path) and os.path.exists(bold_path):
        pdfmetrics.registerFont(TTFont('PuHuiTi-Regular', regular_path))
        pdfmetrics.registerFont(TTFont('PuHuiTi-Bold', bold_path))
        FONT_REG = "PuHuiTi-Regular"
        FONT_BOLD = "PuHuiTi-Bold"
        print("✓ 阿里巴巴普惠体加载成功")
    else:
        raise FileNotFoundError("字体文件不存在")
except Exception as e:
    print(f"⚠ 使用英文字体: {e}")
    FONT_REG = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

# ============================================================
# 配色方案
# ============================================================
COLOR_PRIMARY = HexColor("#27ae60")      # 主色
COLOR_TITLE = HexColor("#2c3e50")        # 标题
COLOR_TEXT = HexColor("#333333")         # 正文
COLOR_SUBTLE = HexColor("#7f8c8d")       # 次要
RISK_LOW = HexColor("#27ae60")           # 低风险
RISK_MEDIUM = HexColor("#f39c12")        # 中风险
RISK_HIGH = HexColor("#e74c3c")          # 高风险

# ============================================================
# 页面布局
# ============================================================
WIDTH, HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = WIDTH - 2 * cm
Y_START = HEIGHT - 2.5 * cm

# ============================================================
# 【核心函数】正确处理项目符号的文本绘制
# ============================================================

def draw_text_line(c, x, y, text, font_name, font_size, max_width):
    """
    绘制单行或多行文本，正确处理项目符号
    
    关键修复:
    1. 检测项目符号 (•, 1., 2., etc.)
    2. 分离符号和内容
    3. 符号画在 x 位置
    4. 内容画在 x + offset 位置
    5. 换行保持相同缩进
    
    Args:
        c: Canvas对象
        x: X坐标
        y: Y坐标
        text: 文本内容
        font_name: 字体名称
        font_size: 字体大小
        max_width: 最大宽度
        
    Returns:
        新的Y坐标
    """
    c.setFont(font_name, font_size)
    
    # 1. 识别项目符号类型
    bullet = None
    content = text
    bullet_offset = 0.7 * cm  # 符号与文本的间距
    
    # 检测 "• " 或 "•"
    if text.startswith("• "):
        bullet = "•"
        content = text[2:]  # 去掉 "• "
    elif text.startswith("•"):
        bullet = "•"
        # 去掉所有前导的 "•" 和空格
        content = text.lstrip("•").lstrip()
    
    # 检测数字列表 "1. ", "2. "
    elif text and len(text) > 2 and text[0].isdigit():
        for i in range(min(3, len(text))):
            if text[i] == '.':
                bullet = text[:i+1]  # "1.", "2.", etc.
                content = text[i+1:].lstrip()
                bullet_offset = c.stringWidth(bullet + " ", font_name, font_size)
                break
    
    # 2. 绘制项目符号（如果有）
    if bullet:
        # 画符号
        c.drawString(x, y, bullet)
        
        # 计算文本起始位置
        text_x = x + bullet_offset
        text_max_width = max_width - bullet_offset
        
        # 3. 处理文本换行
        lines = []
        current_line = ""
        
        for char in content:
            test_line = current_line + char
            char_width = c.stringWidth(test_line, font_name, font_size)
            
            if char_width > text_max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        
        # 添加最后一行
        if current_line:
            lines.append(current_line)
        
        # 4. 绘制所有行（保持相同缩进）
        for line in lines:
            c.drawString(text_x, y, line)
            y -= (font_size * 1.4) / 72 * cm  # 行距
        
        return y - 0.2*cm  # 项目间距
    
    else:
        # 无项目符号的普通文本
        lines = []
        current_line = ""
        
        for char in content:
            test_line = current_line + char
            
            if c.stringWidth(test_line, font_name, font_size) > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            c.drawString(x, y, line)
            y -= (font_size * 1.4) / 72 * cm
        
        return y - 0.2*cm


# ============================================================
# 其他辅助函数
# ============================================================

def draw_section_header(c, y, cn_title, en_title, color):
    """绘制章节标题"""
    if y < 6 * cm:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        y = Y_START
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(color)
    c.drawString(MARGIN_LEFT, y, cn_title)
    
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT, y - 0.5*cm, en_title)
    
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(MARGIN_LEFT, y - 0.8*cm, MARGIN_RIGHT, y - 0.8*cm)
    
    return y - 1.8*cm


def draw_bilingual_field(c, y, cn_label, en_label, value_text, value_color=COLOR_TEXT):
    """绘制双语字段"""
    if y < 4 * cm:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        y = Y_START
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, cn_label)
    
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, en_label)
    
    c.setFillColor(value_color)
    
    if isinstance(value_text, (list, tuple)):
        value_str = ", ".join(str(v) for v in value_text)
    else:
        value_str = str(value_text)
    
    max_width = 12 * cm
    y = draw_text_line(c, MARGIN_LEFT + 5.5*cm, y, value_str, FONT_REG, 10, max_width)
    
    return y - 0.3*cm


def draw_text_block(c, y, text_list, font_name=None, font_size=10):
    """绘制文本块"""
    if font_name is None:
        font_name = FONT_REG
    
    c.setFillColor(COLOR_TEXT)
    
    base_x = MARGIN_LEFT + 1*cm
    max_width = MARGIN_RIGHT - base_x - 0.5*cm
    
    for text in text_list:
        if y < 4 * cm:
            c.showPage()
            draw_footer(c, c.getPageNumber())
            y = Y_START
        
        y = draw_text_line(c, base_x, y, str(text), font_name, font_size, max_width)
    
    return y


def set_risk_color(c, level, score):
    """根据风险等级设置颜色"""
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
    """绘制页脚"""
    c.setFont(FONT_REG, 8)
    c.setFillColor(COLOR_SUBTLE)
    c.drawCentredString(WIDTH/2, 1.5*cm, 
                       f"第 {page_num} 页 (Page {page_num}) | 秘密文件 (Confidential)")
    c.drawCentredString(WIDTH/2, 1*cm, 
                       "由绿链 (GreenLink) 平台生成 | Based on Satellite & AI Analysis")


# ============================================================
# 主函数
# ============================================================

def generate_pdf_report(data):
    """
    生成ESG合规报告PDF
    
    Args:
        data: ESG数据字典，包含:
            - company: 公司名称
            - environment: 环境数据
            - social: 社会数据
            - supply_chain: 供应链数据
    
    Returns:
        BytesIO: PDF文件流
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f"{data.get('company', 'Report')} - ESG Report")
    
    company_name = data.get('company', '未知公司')
    is_cofco = 'COFCO' in company_name or '中粮' in company_name
    env_data = data.get('environment', {})
    social_data = data.get('social', {})
    supply_chain_data = data.get('supply_chain', {})
    page_num = 1
    
    # ==================================================
    # 第一页：封面
    # ==================================================
    
    c.setFillColor(COLOR_PRIMARY)
    c.rect(0, HEIGHT - 5*cm, WIDTH, 5*cm, fill=True, stroke=False)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(FONT_BOLD, 32)
    c.drawCentredString(WIDTH/2, HEIGHT - 2.8*cm, "绿链 (GreenLink)")
    
    c.setFont(FONT_REG, 16)
    c.drawCentredString(WIDTH/2, HEIGHT - 3.8*cm, 
                       "ESG 风险评估报告 (ESG Risk Assessment Report)")
    
    c.setFillColor(COLOR_TITLE)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(WIDTH/2, HEIGHT - 7.5*cm, company_name)
    
    y = HEIGHT - 10*cm
    c.setFont(FONT_REG, 11)
    c.drawCentredString(WIDTH/2, y, 
                       f"报告日期 (Report Date): {datetime.now().strftime('%Y-%m-%d')}")
    y -= 0.6*cm
    
    if is_cofco:
        company_type = "中游加工商 / 采购商 (Midstream Processor / Buyer)"
    else:
        company_type = "上游供应商 / 种植商 (Upstream Supplier / Plantation)"
    
    c.drawCentredString(WIDTH/2, y, f"公司类型 (Company Type): {company_type}")
    y -= 0.6*cm
    
    period = env_data.get('analysis', {}).get('period', 'N/A')
    c.drawCentredString(WIDTH/2, y, f"评估周期 (Assessment Period): {period}")
    
    # 风险概览
    y = HEIGHT - 15*cm
    y = draw_section_header(c, y, "风险等级概览", "Risk Level Overview", COLOR_PRIMARY)
    
    e_level = env_data.get('risk_level', '未知')
    e_score = env_data.get('risk_score', 0)
    e_color = set_risk_color(c, e_level, e_score)
    y = draw_bilingual_field(c, y, "环境风险 (E)", "Environmental Risk (E)", 
                             f"{e_level} ({e_score}/100)", value_color=e_color)
    
    s_level = social_data.get('risk_level', '未知')
    s_score = social_data.get('risk_score', 0)
    s_color = set_risk_color(c, s_level, s_score)
    y = draw_bilingual_field(c, y, "社会风险 (S)", "Social Risk (S)", 
                             f"{s_level} ({s_score}/100)", value_color=s_color)
    
    # 平台优势
    y -= 1*cm
    y = draw_section_header(c, y, "绿链评估优势", "GreenLink Advantage", COLOR_TITLE)
    
    advantages = [
        ("√ 实时卫星监控 (E)", "Real-time satellite monitoring (Environment)"),
        ("√ AI驱动舆情分析 (S)", "AI-powered sentiment analysis (Social)"),
        ("√ E/S分离评分", "Separated E/S risk scoring for precision"),
        ("√ 欧盟EUDR合规验证", "EU Deforestation Regulation (EUDR) validation")
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
    # 第二页：环境风险
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "环境风险分析 (E)", 
                           "Environmental Risk Analysis (E)", COLOR_PRIMARY)
    
    env_analysis = env_data.get('analysis', {})
    
    y = draw_bilingual_field(c, y, "分析方法", "Analysis Method", 
                            env_analysis.get('method', 'N/A'))
    y = draw_bilingual_field(c, y, "分析周期", "Analysis Period", 
                            env_analysis.get('period', 'N/A'))
    
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
        y = draw_text_block(c, y, [f"• {f}" for f in findings])
        y -= 0.5*cm
        y = draw_text_block(c, y, [f"结论: {env_analysis.get('conclusion', 'N/A')}"], 
                           FONT_BOLD, 10)
    else:
        evidence = env_analysis.get('evidence', {})
        conclusion = evidence.get('conclusion', env_analysis.get('result', 'N/A'))
        y = draw_text_block(c, y, [conclusion])
    
    # 【关键位置】法规合规性 - 这里会正确处理项目符号
    y -= 1*cm
    y = draw_bilingual_field(c, y, "法规合规性", "Regulatory Compliance", "")
    
    compliance = env_data.get('compliance', {})
    if compliance:
        # 生成带项目符号的列表
        compliance_items = [f"• {v}" for v in compliance.values()]
        # 使用修复后的函数绘制
        y = draw_text_block(c, y, compliance_items)
    else:
        y = draw_text_block(c, y, ["• 无数据 (No data)"])
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # 第三页：社会风险
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "社会风险分析 (S)", 
                           "Social Risk Analysis (S)", RISK_HIGH)
    
    if is_cofco:
        social_analysis = social_data.get('analysis', {})
        y = draw_bilingual_field(c, y, "风险来源", "Risk Source", 
                                social_analysis.get('risk_source', 'N/A'))
        y = draw_bilingual_field(c, y, "关键问题", "Key Concern", "")
        y = draw_text_block(c, y, [social_analysis.get('key_concern', 'N/A')])
        y -= 1*cm
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "关键风险事件")
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Risk Events")
    y -= 1*cm
    
    key_events = social_data.get('key_events', [])
    if not key_events:
        y = draw_text_block(c, y, 
                           ["未发现重大负面舆情事件 (No significant negative events found)"])
    
    for event in key_events[:4]:
        if y < 8 * cm:
            c.showPage()
            draw_footer(c, page_num)
            page_num += 1
            y = Y_START
            y = draw_section_header(c, y, "社会风险分析 (S) - 续", 
                                  "Social Risk Analysis (S) - Cont.", RISK_HIGH)
        
        event_date = event.get('date', event.get('year', 'N/A'))
        event_text = event.get('event', 'N/A')
        event_impact = event.get('impact', 'N/A')
        
        y = draw_bilingual_field(c, y, "日期 (Date)", "", event_date)
        y = draw_bilingual_field(c, y, "事件 (Event)", "", "")
        y = draw_text_block(c, y, [event_text], font_size=9)
        y = draw_bilingual_field(c, y, "影响 (Impact)", "", "")
        y = draw_text_block(c, y, [event_impact], font_size=9)
        
        c.line(MARGIN_LEFT, y, MARGIN_RIGHT, y)
        y -= 0.5*cm
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # 第四页：供应链与建议
    # ==================================================
    
    y = Y_START
    
    if supply_chain_data:
        y = draw_section_header(c, y, "供应链分析", "Supply Chain Analysis", COLOR_TITLE)
        
        if is_cofco:
            suppliers = supply_chain_data.get('upstream', {}).get('suppliers', [])
            y = draw_text_block(c, y, 
                              ["已识别上游高风险供应商 (High-risk upstream suppliers identified):"], 
                              FONT_BOLD, 10)
            
            for supplier in suppliers[:3]:
                name = supplier.get('name', 'N/A')
                status = supplier.get('risk_status', 'N/A')
                color = set_risk_color(c, status, 100 if '高' in status else 30)
                y = draw_bilingual_field(c, y, f"• {name}", "", status, value_color=color)
        else:
            markets = supply_chain_data.get('downstream', {}).get('markets', [])
            y = draw_text_block(c, y, 
                              ["下游市场合规风险 (Downstream Market Compliance Risk):"], 
                              FONT_BOLD, 10)
            y = draw_text_block(c, y, 
                              [f"• 主要市场 (Target Markets): {', '.join(markets)}"])
            y = draw_text_block(c, y, 
                              [f"• 风险点 (Risk): 欧盟EUDR及美国CBP法规 (EUDR & US CBP Regulations)"])
        
        y -= 1*cm
    
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
    
    y = draw_text_block(c, y, recs)
    
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
    
    c.save()
    buffer.seek(0)
    
    return buffer
