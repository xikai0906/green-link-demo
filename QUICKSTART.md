# 🚀 快速开始指南

## 步骤1：确保环境准备就绪

### 检查 Python 版本
```bash
python3 --version
# 需要 Python 3.7 或更高版本
```

### 如果没有 Python，请先安装：
- Windows: 从 [python.org](https://www.python.org/downloads/) 下载安装
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3`

## 步骤2：安装依赖

在项目目录下运行：
```bash
pip install -r requirements.txt
```

或者使用国内镜像加速：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 步骤3：启动应用

### 方法1：使用启动脚本（推荐）
```bash
./run.sh
```

### 方法2：直接运行
```bash
streamlit run app.py
```

### 方法3：指定端口
```bash
streamlit run app.py --server.port 8080
```

## 步骤4：访问应用

浏览器会自动打开，如果没有，手动访问：
```
http://localhost:8501
```

## 🎯 演示流程建议

### 第一幕：风险评估仪表盘（5分钟）
1. 展示传统评级（MSCI BB级）的模糊性
2. 对比绿链的E/S分离评分：
   - 环境：低风险（25分）- 基于卫星验证
   - 社会：高风险（75分）- 基于舆情分析
3. 展示卫星图片对比（2014 vs 2022）
4. 解释关键舆情事件（美国CBP禁令）

### 第二幕：供应链冲击分析（5分钟）
1. 展示三层供应链结构：
   - 上游：FGV（马来西亚种植商）
   - 中游：中粮集团（加工商）
   - 下游：欧盟/美国/中国市场
2. 解释风险传导路径
3. 展示法规影响（EUDR、CBP禁令）
4. 生成并下载PDF合规报告

### 第三幕：B2C产品溯源（3分钟）
1. 展示产品实物道具（福临门食用油）
2. 扫描二维码演示
3. 展示消费者端溯源信息
4. 强调B2B2C价值闭环

## 🎨 演示技巧

### 1. 数据对比突出
强调传统评级的问题：
- "MSCI给FGV评级BB，但无法告诉你问题在哪"
- "绿链精准定位：环境好，社会差"

### 2. 成本优势
- 传统评级：年费数万美元，年度更新
- 绿链：基于免费数据，周度更新，成本降低90%

### 3. 实时性优势
- 2024年7月 FGV提交整改请愿书
- 传统评级尚未更新
- 绿链已同步更新

## 🐛 常见问题

### Q1: 图片不显示？
检查文件路径是否正确：
```
assets/satellite_images/FGV_2014.png
assets/satellite_images/FGV_2022.png
```

### Q2: PDF生成失败？
确保安装了 reportlab：
```bash
pip install reportlab
```

### Q3: 端口被占用？
更换端口：
```bash
streamlit run app.py --server.port 8080
```

### Q4: 中文显示乱码？
确保文件编码为 UTF-8

## 📝 自定义数据

### 添加新公司案例
1. 复制 `data/FGV.json` 为模板
2. 修改公司信息和数据
3. 添加卫星图片到 `assets/satellite_images/`
4. 在 `app.py` 中更新公司列表

### 修改配色方案
在 `app.py` 中修改 CSS：
```python
st.markdown("""
<style>
    .main-header {
        color: #your-color;  /* 修改标题颜色 */
    }
</style>
""")
```

## 🎓 推荐学习资源

- Streamlit 官方文档: https://docs.streamlit.io
- Sentinel-2 数据: https://scihub.copernicus.eu
- ESG评级方法: MSCI, Sustainalytics 官网

## 💡 进阶功能建议

1. **实时数据更新**
   - 接入新闻API自动抓取舆情
   - 定期从Sentinel Hub更新卫星数据

2. **用户管理**
   - 添加登录系统
   - 保存用户的查询历史

3. **API开发**
   - 提供REST API接口
   - 支持批量查询

4. **数据库集成**
   - 使用PostgreSQL存储历史数据
   - 支持数据分析和趋势追踪

---

祝演示成功！🎉
