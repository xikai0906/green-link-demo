from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- 1. 字体和颜色配置 ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT_REGULAR_NAME = 'AlibabaPuHuiTi-3-55-Regular.ttf'
FONT_BOLD_NAME = 'AlibabaPuHuiTi-3-85-Bold.ttf'

FONT_REGULAR_PATH = os.path.join(BASE_DIR, 'fonts', FONT_REGULAR_NAME)
FONT_BOLD_PATH = os.path.join(BASE_DIR, 'fonts', FONT_BOLD_NAME)

FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_LOADED = False

try:
    if os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH):
        pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Regular', FONT_REGULAR_PATH))
        pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Bold', FONT_BOLD_PATH))
        FONT_REG = "AlibabaPuHuiTi-Regular"
        FONT_BOLD = "AlibabaPuHuiTi-Bold"
        FONT_LOADED = True
        print("✓ 字体加载成功 (Alibaba PuHuiTi fonts loaded successfully)")
    else:
        raise FileNotFoundError("字体文件未在指定路径找到 (Font files not found at path)")
except Exception as e:
    print(f"✗ 字体加载失败 (Font loading failed): {e}")
    print("!!! PDF 将回退到英文字体 (Helvetica), 中文将显示为乱码 '■■■'。")


COLOR_PRIMARY = HexColor("#27ae60")
COLOR_TITLE = HexColor("#2c3e50")
COLOR_TEXT = HexColor("#333333")
COLOR_SUBTLE = HexColor("#7f8c8d")
RISK_LOW = HexColor("#27ae60")
RISK_MEDIUM = HexColor("#f39c12")
RISK_HIGH = HexColor("#e74c3c")

WIDTH, HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = WIDTH - 2 * cm
Y_START = HEIGHT - 2.5 * cm

# --- 2. 核心绘图函数 (已修复) ---

def check_page_break(c, y):
    """检查是否需要分页, 如果需要则返回新的Y坐标"""
    if y < 4 * cm:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        return Y_START
    return y

def draw_wrapped_text(c, x, y, text, font_name, font_size, max_width):
    """
    (新) 在指定坐标(x, y)绘制换行文本
    返回绘制后的新Y坐标
    """
    c.setFont(font_name, font_size)
    
    text = str(text)
    line = ""
    start_y = y
    
    # 逐字符处理以支持中英文混合换行
    for char in text:
        # 检查是否是项目符号
        is_bullet = (char == '•' or char == '✓' or char == '1.' or char == '2.' or char == '3.') and line == ""
        current_x = x
        current_max_width = max_width
        
        if is_bullet:
            c.drawString(current_x, y, char) # 绘制项目符号
            current_x += 0.6*cm
            current_max_width -= 0.6*cm
        else:
            test_line = line + char
            if c.stringWidth(test_line, font_name, font_size) > current_max_width:
                c.drawString(current_x, y, line)
                y -= (font_size * 1.3) / 72 * cm # 1.3倍行距
                line = char
            else:
                line += char
                
    c.drawString(current_x, y, line) # 绘制最后一行
    y -= (font_size * 1.3) / 72 * cm
    
    return y

def draw_section_header(c, y, cn_title, en_title, color):
    """绘制章节标题"""
    y = check_page_break(c, y)
    
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
    """绘制双语字段 (已修复)"""
    y = check_page_break(c, y)
    
    # 1. 绘制标签
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, cn_label)
    
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, en_label)
    
    # 2. 绘制值
    c.setFillColor(value_color)
    
    value_x = MARGIN_LEFT + 5.5*cm
    max_width = MARGIN_RIGHT - value_x
    
    if isinstance(value_text, (list, tuple)):
        # 如果是列表, 逐项换行绘制
        y_after_draw = y
        for item in value_text:
            y_after_draw = draw_wrapped_text(c, value_x, y_after_draw, str(item), FONT_REG, 10, max_width)
        return y_after_draw - 0.3*cm
    else:
        # 如果是单个字符串, 直接绘制
        y_after_draw = draw_wrapped_text(c, value_x, y, str(value_text), FONT_REG, 10, max_width)
        # 返回绘制后的Y坐标
        return y_after_draw - 0.3*cm


def draw_wrapped_block(c, y, text_list, font_name=None, font_size=10, indent=1.0*cm):
    """绘制文本块 (已修复, 增加缩进)"""
    if font_name is None:
        font_name = FONT_REG
    
    c.setFillColor(COLOR_TEXT)
    
    base_x = MARGIN_LEFT + indent # 使用缩进
    max_width = MARGIN_RIGHT - base_x
    
    for text in text_list:
        y = check_page_break(c, y)
        y = draw_wrapped_text(c, base_x, y, str(text), font_name, font_size, max_width)
        y -= 0.3*cm  # 项目间距
    
    return y

def set_risk_color(c, level, score):
    """设置风险颜色"""
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
# 主生成函数 (已修复逻辑)
# ============================================================

def generate_pdf_report(data):
    """生成ESG报告PDF"""
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
        ("✓ 实时卫星监控 (E)", "Real-time satellite monitoring (Environment)"),
        ("✓ AI驱动舆情分析 (S)", "AI-powered sentiment analysis (Social)"),
        ("✓ E/S分离评分", "Separated E/S risk scoring for precision"),
        ("✓ 欧盟EUDR合规验证", "EU Deforestation Regulation (EUDR) validation")
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
    
    # ========== 修复逻辑 ==========
    # 使用 draw_wrapped_block 在标签下方绘制缩进的文本
    if is_cofco:
        findings = env_analysis.get('key_findings', ['N/A'])
        y = draw_wrapped_block(c, y, [f"• {f}" for f in findings])
        y -= 0.5*cm
        y = draw_wrapped_block(c, y, [f"结论: {env_analysis.get('conclusion', 'N/A')}"], FONT_BOLD, 10)
    else:
        evidence = env_analysis.get('evidence', {})
        conclusion = evidence.get('conclusion', env_analysis.get('result', 'N/A'))
        # 修复：结论也应该使用 draw_wrapped_block 绘制
        y = draw_wrapped_block(c, y, [conclusion])
    
    # 法规合规性
    y -= 1*cm
    
    # 修复：将合规性项目作为 "值" 传递给 draw_bilingual_field
    compliance = env_data.get('compliance', {})
    if compliance:
        compliance_items = [f"• {v}" for v in compliance.values()]
    else:
        compliance_items = ["• 无数据 (No data)"]
        
    y = draw_bilingual_field(c, y, "法规合规性", "Regulatory Compliance", compliance_items)
    # ============================
    
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
        y = draw_bilingual_field(c, y, "关键问题", "Key Concern", 
                                 social_analysis.get('key_concern', 'N/A')) # 修复：直接作为值传递
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
        y = draw_wrapped_block(c, y, 
                             ["未发现重大负面舆情事件 (No significant negative events found)"])
    
    for event in key_events[:4]:
        y = check_page_break(c, y - 4*cm) # 检查是否有足够空间
        if y == Y_START: # 如果分页了
            y = draw_section_header(c, y, "社会风险分析 (S) - 续", 
                                  "Social Risk Analysis (S) - Cont.", RISK_HIGH)
        
        event_date = event.get('date', event.get('year', 'N/A'))
        event_text = event.get('event', 'N/A')
        event_impact = event.get('impact', 'N/A')
        
        # 修复：使用 draw_bilingual_field 保证对齐
        y = draw_bilingual_field(c, y, "日期 (Date)", "", event_date)
        y = draw_bilingual_field(c, y, "事件 (Event)", "", event_text)
        y = draw_bilingual_field(c, y, "影响 (Impact)", "", event_impact)
        
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
            y = draw_wrapped_block(c, y, 
                                 ["已识别上游高风险供应商 (High-risk upstream suppliers identified):"], 
                                 FONT_BOLD, 10, indent=0.5*cm) # 减小缩进
            
            for supplier in suppliers[:3]:
                name = supplier.get('name', 'N/A')
                status = supplier.get('risk_status', 'N/A')
                color = set_risk_color(c, status, 100 if '高' in status else 30)
                # 修复：使用 bilingual_field
                y = draw_bilingual_field(c, y, f"• {name}", "", status, value_color=color)
        else:
            markets = supply_chain_data.get('downstream', {}).get('markets', [])
            y = draw_wrapped_block(c, y, 
                                 ["下游市场合规风险 (Downstream Market Compliance Risk):"], 
                                 FONT_BOLD, 10, indent=0.5*cm)
            y = draw_wrapped_block(c, y, 
                                 [f"• 主要市场 (Target Markets): {', '.join(markets)}"])
            y = draw_wrapped_block(c, y, 
                                 [f"• 风险点 (Risk): 欧盟EUDR及美国CBP法规"])
        
        y -= 1*cm
    
    y = check_page_break(c, y - 8*cm) # 检查是否有足够空间放“建议”
    
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
    
    y = draw_wrapped_block(c, y, recs) # 使用默认缩进
    
    y = check_page_break(c, y - 4*cm) # 检查放联系方式的空间
    
    # --- 报告结尾 ---
    y -= 2*cm
    c.setFont(FONT_BOLD, 11)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT, y, "联系我们 (Contact Us):")
    y -= 0.6*cm
    
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_TEXT)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "绿链 GreenLink ESG 平台")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "邮箱: support@greenlink.com")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "网站: www.greenlink.com")
    
    draw_footer(c, page_num)
    
    c.save()
    buffer.seek(0)
    
    return buffer
