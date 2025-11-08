#!/bin/bash

echo "🌿 绿链 GreenLink - ESG风险评估平台"
echo "=================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python 3.7+"
    exit 1
fi

echo "✅ Python 已安装: $(python3 --version)"
echo ""

# 检查是否已安装依赖
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 正在安装依赖包..."
    pip install -r requirements.txt
    echo ""
fi

echo "🚀 启动应用..."
echo ""
echo "应用将在浏览器中自动打开"
echo "默认地址: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止应用"
echo ""

streamlit run app.py
