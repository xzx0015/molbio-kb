# SKILL 01: 内容采集 — PDF/课件/文献的采集与标准化

> 从多种原始格式（PDF、PPT、Word、网页）采集分子生物学教学资源，统一转换为标准Markdown格式。

---

## 一、核心概念

### 1.1 原始资源类型

分子生物学课程资源通常来自以下渠道：

| 来源类型 | 典型格式 | 内容特征 | 处理优先级 |
|----------|----------|----------|------------|
| 教材扫描 | PDF | 完整章节、权威定义 | ★★★ 最高 |
| 教学课件 | PPT/PPTX | 重点提炼、图示丰富 | ★★★ 最高 |
| 讲义文档 | DOC/DOCX | 补充说明、例题解析 | ★★☆ 中等 |
| 参考文献 | PDF | 前沿进展、实验方法 | ★★☆ 中等 |
| 在线资源 | HTML/Markdown | 互动内容、视频脚本 | ★☆☆ 可选 |

### 1.2 标准化目标格式

所有资源最终统一为 **GitHub Flavored Markdown (GFM)**，原因：
- **纯文本可diff** — 便于版本控制和协作
- **LaTeX公式支持** — `$E=mc^2$` 和 `$$...$$` 块级公式
- **表格友好** — 课程数据常以表格呈现
- **图片嵌入** — `![alt](path)` 语法简洁
- **代码高亮** — 序列数据、脚本示例

---

## 二、阶段1：资源采集

### 2.1 采集目录结构

```
archive/
├── 教材/
│   ├── 分子生物学_第5版_朱玉贤.pdf
│   ├── 分子生物学_第5版_朱玉贤_章节目录.txt
│   └── 封面-版权页-目录.pdf
├── 课件/
│   ├── 第01章_绪论.pptx
│   ├── 第02章_DNA复制.pptx
│   └── ...
├── 文献/
│   ├── 2023_Crispr_Review.pdf
│   └── ...
└── 补充/
    └── 实验指导.docx
```

### 2.2 命名规范

**文件命名**：`{序号}_{主题}.{扩展名}`

```
✓ 第01章_绪论与历史.pptx
✓ 第02章_DNA复制机制.pdf
✓ 第03章_转录与RNA加工.pptx
✗ 分子生物学第一章.pptx      ← 缺少序号
✗ 第1章.pptx                 ← 序号未补零
✗ DNA复制(2).pptx            ← 无序号，有重复标记
```

**章节编号规则**：
- 两位数编号（01-99），确保文件排序正确
- 使用阿拉伯数字，避免"第一章"等中文数字
- 主题使用简洁英文或中文，无空格用下划线替代

---

## 三、阶段2：格式转换

### 3.1 PDF转Markdown

**工具链**：`pdfplumber`（保留布局）+ `pandoc`（精修格式）

```python
import pdfplumber

def pdf_to_markdown(pdf_path, output_path):
    """PDF转Markdown，保留章节结构和公式"""
    with pdfplumber.open(pdf_path) as pdf:
        md_content = []
        for page in pdf.pages:
            text = page.extract_text()
            # 识别标题层级（字体大小/粗体）
            # 识别公式块（居中、特殊字符）
            # 识别表格（线条对齐）
            md_content.append(process_page(text))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(md_content))
```

**PDF特殊元素处理**：

| 元素 | 识别特征 | Markdown转换 |
|------|----------|--------------|
| 章节标题 | 大字号、粗体、数字编号 | `# 第N章 标题` |
| 小节标题 | 中等字号、粗体 | `## N.M 标题` |
| 正文段落 | 常规字号 | 普通段落 |
| 公式块 | 居中、希腊字母/上下标 | `$$...$$` |
| 行内公式 | 特殊符号夹杂 | `$...$` |
| 表格 | 线条对齐 | GFM表格语法 |
| 图片 | 图注"图N-X" | `![图注](images/...)` |
| 页眉页脚 | 每页重复 | 删除 |

### 3.2 PPT转Markdown

**工具链**：`python-pptx` 提取文本 + 手动整理结构

```python
from pptx import Presentation

def pptx_to_markdown(pptx_path, output_path):
    """PPT转Markdown，每页转为一个小节"""
    prs = Presentation(pptx_path)
    md_content = []
    
    for i, slide in enumerate(prs.slides, 1):
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text.append(shape.text.strip())
        
        if slide_text:
            md_content.append(f"## 幻灯片 {i}\n\n")
            md_content.append('\n\n'.join(slide_text))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(md_content))
```

**PPT特殊处理**：
- 提取备注栏内容作为补充说明
- 识别SmartArt图形转为列表或表格
- 图片另存到 `images/` 目录，Markdown引用相对路径

### 3.3 Word转Markdown

**推荐工具**：`pandoc`（最可靠）

```bash
# 基础转换
pandoc -s input.docx -t markdown -o output.md

# 保留图片（提取到指定目录）
pandoc -s input.docx -t markdown --extract-media=./images -o output.md

# 保留表格宽度信息
pandoc -s input.docx -t markdown --wrap=none -o output.md
```

---

## 四、阶段3：内容清洗

### 4.1 清洗规则

**删除内容**：
- 页眉页脚（页码、章节名重复）
- 版权声明页
- 空白页/分隔页
- "本章小结"等模板化内容（保留核心要点）

**规范化内容**：
- 统一术语拼写（如"DNA"不写作"Dna"或"dna"）
- 统一标点符号（中文内容用中文标点，英文用英文标点）
- 统一单位格式（"kb"→"kb"，"°C"→"°C"）

### 4.2 公式标准化

**LaTeX公式规范**：

```markdown
# 行内公式
DNA双螺旋直径约为 $2\,\text{nm}$，螺距约为 $3.4\,\text{nm}$。

# 块级公式（独立成行）
$$
DNA_{浓度}(\mu g/mL) = \frac{OD_{260} \times 稀释倍数 \times 50}{1000}
$$

# 化学方程式
$$
\text{dNTP} + \text{DNA}_{n} \xrightarrow{\text{DNA聚合酶}} \text{DNA}_{n+1} + \text{PPi}
$$
```

**常见公式替换**：

| 原文 | 替换为 | 说明 |
|------|--------|------|
| α | `\alpha` | 希腊字母 |
| β | `\beta` | 希腊字母 |
| °C | `^\circ\text{C}` | 摄氏度 |
| 下标n | `_n` | 下标 |
| 上标2 | `^2` | 上标 |

### 4.3 图片处理

**图片命名**：`{章节号}_{序号}_{描述}.png`

```
images/
├── 02_01_dna_double_helix.png
├── 02_02_replication_fork.png
├── 02_03_okazaki_fragments.png
└── ...
```

**Markdown引用**：
```markdown
![DNA双螺旋结构示意图](images/02_01_dna_double_helix.png)
*图2-1 DNA双螺旋结构示意图。显示两条反向平行的多核苷酸链，碱基对位于内侧，通过氢键连接。*
```

---

## 五、阶段4：质量验证

### 5.1 自动化检查

```python
# lint_raw_md.py — 原始Markdown质量检查

def check_markdown_quality(md_path):
    """检查转换后的Markdown质量"""
    issues = []
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查1：标题层级是否连续
    headers = re.findall(r'^(#{1,6})\s', content, re.MULTILINE)
    # 不允许从#直接跳到###
    
    # 检查2：公式语法是否正确
    # 行内公式 $...$ 必须成对
    # 块级公式 $$...$$ 必须成对
    
    # 检查3：图片引用是否存在
    images = re.findall(r'!\[.*?\]\((.*?)\)', content)
    for img in images:
        if not os.path.exists(os.path.join(os.path.dirname(md_path), img)):
            issues.append(f"图片缺失: {img}")
    
    # 检查4：表格格式是否正确
    # GFM表格必须有表头分隔行 |---|---|
    
    # 检查5：编码问题
    # 不应有乱码字符 
    
    return issues
```

### 5.2 人工审核清单

| 检查项 | 合格标准 |
|--------|----------|
| 章节完整性 | 无遗漏小节，顺序正确 |
| 公式准确性 | 与原文一致，渲染正确 |
| 图片清晰度 | 分辨率足够，标注清晰 |
| 术语一致性 | 全文术语统一 |
| 引用完整性 | 图表引用编号连续 |

---

## 六、输出规范

### 6.1 标准化后目录结构

```
docs/raw/
├── 01_绪论与历史.md
├── 02_DNA复制.md
├── 03_转录与RNA加工.md
├── 04_翻译与蛋白质合成.md
├── 05_基因表达调控.md
├── 06_分子生物学技术.md
├── 07_基因组学与蛋白质组学.md
└── images/
    ├── 01_01_central_dogma.png
    ├── 02_01_dna_structure.png
    └── ...
```

### 6.2 文件头元数据

每个标准化Markdown文件应包含YAML frontmatter：

```markdown
---
chapter: 02
title: DNA复制
source: 分子生物学_第5版_朱玉贤.pdf
pages: 45-89
topics:
  - DNA半保留复制
  - 复制起点与方向
  - DNA聚合酶
  - 复制叉与冈崎片段
  - 端粒与端粒酶
keywords:
  - DNA replication
  - DNA polymerase
  - replication fork
  - Okazaki fragments
  - telomerase
difficulty: intermediate
prerequisites:
  - 01_绪论与历史
---

# 第2章 DNA复制

## 2.1 DNA复制的基本特征

...
```

---

## 七、工具链

| 脚本 | 位置 | 功能 |
|------|------|------|
| `pdf_to_md.py` | scripts/ | PDF转Markdown，保留结构 |
| `pptx_to_md.py` | scripts/ | PPT转Markdown |
| `docx_to_md.py` | scripts/ | Word转Markdown（pandoc包装） |
| `clean_md.py` | scripts/ | 内容清洗（去页眉页脚等） |
| `lint_raw_md.py` | scripts/ | Markdown质量检查 |
| `extract_images.py` | scripts/ | 批量提取和重命名图片 |

---

## 八、经验教训

1. **PDF扫描件需OCR** — 扫描版PDF需先进行OCR识别，推荐`Tesseract`+`pdf2image`
2. **公式优先保留LaTeX** — 图片公式难以编辑，尽量转换为LaTeX源码
3. **表格手动校对** — 自动转换的表格常有对齐问题，需人工检查
4. **图片单独管理** — 图片与Markdown分离，便于后续替换和优化
5. **版本控制原始文件** — `archive/`目录纳入git，保留原始资源可追溯
6. **批注转为引用块** — 教材边栏批注用 `> ...` 引用块格式保留

---

## 九、扩展到其他课程

| 课程类型 | 特殊处理 |
|----------|----------|
| 实验课 | 保留实验步骤编号，安全注意事项高亮 |
| 习题课 | 题目与答案分离存储，便于生成练习 |
| 双语课程 | 标注原文术语，建立术语对照表 |
| 前沿讲座 | 标注演讲日期，区分经典与前沿内容 |
