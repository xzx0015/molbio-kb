# 🧬 分子生物学知识库

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://xzx0015.github.io/molbio-kb/)

> Molecular Biology Knowledge Base · 从DNA到蛋白质的生命密码

## 🌐 在线访问

**知识库网站**: https://xzx0015.github.io/molbio-kb/

## 📚 项目简介

用AI Agent将分子生物学核心知识转化为结构化知识图谱。目标是用机器的力量辅助教学——从海量文献中自动提取知识单元、识别概念关系、构建学习路径，将传统"死记硬背"的学习过程转化为"探索发现"的认知体验。

分子生物学是第一个试验田。当前阶段聚焦于：
- **实体标注**：基因、蛋白质、酶、技术等18类实体
- **概念关系**：中心法则流程、调控网络、技术原理
- **知识单元**：可复用的知识点（SKU）
- **认知辅助**：语法高亮、交互式学习、知识图谱可视化

## 📁 目录结构

```
molbio-kb/
├── chapters/           # 章节内容（Markdown源文件）
│   ├── 01_绪论.md
│   ├── 02_DNA复制.md
│   ├── 03_RNA转录.md
│   ├── 04_蛋白质翻译.md
│   ├── 05_基因调控.md
│   ├── 06_DNA损伤修复.md
│   └── 07_分子生物学技术.md
├── docs/               # GitHub Pages网站（渲染后的HTML）
│   ├── index.html
│   └── chapters/       # HTML格式章节
├── kg/                 # 知识图谱
│   ├── entities/       # 实体索引（基因、蛋白质、酶等）
│   ├── relations/      # 概念关系
│   └── concepts/       # 核心概念网络
├── entities/           # 实体标注数据
├── scripts/            # 渲染和工具脚本
│   ├── render_html.py  # Markdown→HTML渲染器
│   └── generate_all.py # 批量生成
└── skills/             # 方法论文档
```

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/xzx0015/molbio-kb.git
cd molbio-kb

# 2. 安装依赖
pip install -r requirements.txt

# 3. 生成HTML（单章或全部）
python scripts/render_html.py chapters/01_绪论.md
python scripts/generate_all.py

# 4. 查看结果
# 在线：https://xzx0015.github.io/molbio-kb
# 本地：打开 docs/ 下的HTML文件
```

## 📝 更新日志

- **2025-03-20** - 项目启动，建立知识库框架

---

<p align="center">Built with ❤️ for better education</p>
