# 🌿 绿链 GreenLink - ESG风险评估平台 Demo

这是一个基于 Streamlit 的 ESG（环境、社会、治理）风险评估演示系统，专注于供应链透明度和可持续性分析。

## 🎯 项目特点

### 三大创新点

1. **另类数据 + AI分析**
   - 🛰️ Sentinel-2卫星遥感数据
   - 📰 公开舆情数据挖掘
   - 🤖 Python自动化分析

2. **E/S分离评分**
   - 环境(E)：基于卫星遥感验证
   - 社会(S)：基于舆情分析
   - 精准定位风险来源

3. **B2B2C价值闭环**
   - B端：风险预警与合规报告
   - C端：消费者信任标签

## 📁 项目结构

```
greenlink-demo/
├── app.py                          # 主应用程序
├── requirements.txt                # Python依赖
├── README.md                       # 项目说明
├── data/                           # 数据文件夹
│   └── FGV.json                    # FGV Holdings 数据
├── assets/                         # 资源文件夹
│   └── satellite_images/           # 卫星图片
│       ├── FGV_2014.png
│       └── FGV_2022.png
├── utils/                          # 工具模块
│   └── pdf_generator.py            # PDF报告生成器
└── b2c_page/                       # B2C页面
    └── index.html                  # 消费者溯源页面
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

## 📊 功能模块

### 1. 风险评估仪表盘 🎯
- 环境风险评估（基于卫星数据）
- 社会风险评估（基于舆情监控）
- 传统评级对比
- 卫星影像对比展示

### 2. 供应链冲击分析 🔗
- 上游供应商风险识别
- 中游加工商影响分析
- 下游市场合规要求
- 风险传导路径可视化
- PDF合规报告生成

### 3. B2C产品溯源 📱
- 二维码生成
- 产品全链路追溯
- 消费者端信任标签展示

## 💻 技术栈

- **前端框架**: Streamlit
- **数据处理**: Pandas
- **图像处理**: Pillow
- **PDF生成**: ReportLab
- **二维码**: qrcode
- **数据来源**: Sentinel-2卫星数据 + 公开舆情

## 📝 数据说明

### FGV Holdings Berhad 案例

- **环境风险**: 低风险（25/100分）
  - 基于 Sentinel-2 卫星影像分析
  - 5年间无大规模毁林证据
  - 符合欧盟EUDR法规

- **社会风险**: 高风险（75/100分）
  - 2020年美国CBP发布进口禁令（强迫劳动指控）
  - 2024年公司提交整改请愿书
  - 持续监控整改进展

## 🎨 演示亮点

### 1. E/S分离的精准度
传统评级（如MSCI）给出模糊的BB级别，无法区分环境和社会风险。绿链通过：
- 环境：卫星数据客观验证（无毁林）
- 社会：舆情追踪精准定位（劳工问题）

### 2. 实时性与成本优势
- 传统评级：年度更新，订阅费高昂
- 绿链：周度更新，基于免费公开数据，成本降低90%

### 3. 供应链透视能力
清晰展示风险如何从上游供应商传导至中游加工商，再影响下游市场合规

## 📦 部署建议

### 本地演示
```bash
streamlit run app.py
```

### 云端部署
1. **Streamlit Cloud** (推荐)
   - 免费托管
   - 自动部署
   - 访问地址：https://your-app.streamlit.app

2. **Heroku**
   - 需要 Procfile
   - 支持自定义域名

3. **Docker**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["streamlit", "run", "app.py"]
   ```

### B2C页面部署
将 `b2c_page/index.html` 部署到 GitHub Pages：
1. 创建 GitHub 仓库
2. 将 `b2c_page/` 内容推送到 `gh-pages` 分支
3. 启用 GitHub Pages
4. 更新 app.py 中的二维码链接

## 🔧 自定义配置

### 添加新公司数据
1. 在 `data/` 目录创建新的 JSON 文件（参考 FGV.json 格式）
2. 在 `app.py` 的 `companies` 字典中添加条目
3. 添加对应的卫星图片到 `assets/satellite_images/`

### 修改样式
在 `app.py` 中的 CSS 部分自定义：
```python
st.markdown("""
<style>
    /* 在这里添加自定义样式 */
</style>
""", unsafe_allow_html=True)
```

## 📊 数据格式说明

JSON 数据结构：
```json
{
  "company": "公司名称",
  "environment": {
    "risk_level": "低风险/高风险",
    "risk_score": 25,
    "analysis": {
      "method": "分析方法",
      "period": "时间周期",
      "evidence": {
        "satellite_image_before": "图片路径",
        "satellite_image_after": "图片路径",
        "conclusion": "分析结论"
      }
    }
  },
  "social": {
    "risk_level": "低风险/高风险",
    "risk_score": 75,
    "key_events": [...]
  },
  "supply_chain": {...}
}
```

## 🎓 适用场景

1. **创新创业大赛展示**
2. **投资者路演**
3. **供应链管理培训**
4. **ESG合规教学**
5. **产品原型演示**

## ⚠️ 注意事项

- 本项目为演示系统，生产环境需要：
  - 数据库集成
  - 用户认证系统
  - API接口开发
  - 实时数据更新机制

- 卫星数据获取：
  - Sentinel-2 数据可从 [Copernicus Open Access Hub](https://scihub.copernicus.eu/) 免费获取
  - 需要注册账号并使用 sentinelsat Python库下载

## 📞 联系方式

- 项目作者:RILEY.SKYE.CHOU
- 邮箱:ysuy5756@gmail.com
- GitHub: [https://github.com/xikai0906]

## 📄 许可证

MIT License

---

© 2024 GreenLink | 创新创业大赛DEMO
