#!/bin/bash
# 修复所有章节导航栏

CHAPTERS_DIR="/Users/xubot/.openclaw/workspace/skills/molbio-kb/docs/chapters"

for i in 1 2 3 4 5 6 7 8; do
    FILE="$CHAPTERS_DIR/chapter${i}.html"
    
    # 检查文件是否存在
    if [ ! -f "$FILE" ]; then
        echo "❌ chapter${i}.html 不存在"
        continue
    fi
    
    # 创建新的导航栏（当前章节高亮）
    NAV="    <nav class=\"chapter-nav\">\n"
    NAV+="        <a href=\"../index.html\">🏠 首页</a>\n"
    
    for j in 1 2 3 4 5 6 7 8; do
        if [ $j -eq $i ]; then
            NAV+="        <a href=\"chapter${j}.html\" class=\"active\">第${j}章</a>\n"
        else
            NAV+="        <a href=\"chapter${j}.html\">第${j}章</a>\n"
        fi
    done
    
    NAV+="        <a href=\"../kg/entities/network.html\">🕸️ 关联图谱</a>\n"
    NAV+="    </nav>"
    
    # 使用 sed 替换导航栏（简化版，先输出检查）
    echo "=== Chapter $i ==="
    echo "$NAV"
    echo ""
done