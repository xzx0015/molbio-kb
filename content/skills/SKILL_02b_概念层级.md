# SKILL 02b: 概念层级 — 核心概念→衍生概念→应用实例

> 构建分子生物学课程的概念层级体系，区分核心概念、衍生概念和应用实例，形成知识金字塔。

---

## 一、核心概念

### 1.1 三层概念模型

分子生物学知识可划分为三个层级：

```
                    ┌─────────────────┐
    应用层          │   应用实例      │  实验技术、案例分析、前沿应用
                    │  (Application)  │  如：PCR实验设计、CRISPR基因编辑
                    ├─────────────────┤
    衍生层          │   衍生概念      │  由核心概念派生，用于描述具体机制
                    │  (Derived)      │  如：前导链、滞后链、冈崎片段
                    ├─────────────────┤
    核心层          │   核心概念      │  课程最基础、最核心的概念
                    │  (Core)         │  如：DNA复制、转录、翻译
                    └─────────────────┘
```

### 1.2 概念层级定义

**核心概念（Core）**：
- 课程最基础、最重要的概念
- 学生必须掌握的核心知识
- 通常是课程大纲的一级主题
- 数量：每章3-5个

**衍生概念（Derived）**：
- 由核心概念派生或细化的概念
- 用于描述具体机制、过程或结构
- 理解核心概念后才能掌握
- 数量：每个核心概念2-4个衍生概念

**应用实例（Application）**：
- 概念在实际中的应用
- 实验技术、案例分析、问题解决
- 体现知识的实用价值
- 数量：灵活，根据教学目标确定

---

## 二、概念分类体系

### 2.1 12类实体类型

分子生物学课程涉及的概念可分为以下12类：

| 类型 | 标记 | 示例 | 层级分布 |
|------|------|------|----------|
| **分子** | `&` | DNA、RNA、蛋白质 | 核心/衍生 |
| **大分子结构** | `=` | 双螺旋、核小体、核糖体 | 核心/衍生 |
| **酶/蛋白质** | `@` | DNA聚合酶、RNA聚合酶 | 核心/衍生 |
| **生物过程** | `~` | 复制、转录、翻译 | 核心 |
| **细胞结构** | `#` | 细胞核、线粒体、内质网 | 核心/衍生 |
| **基因元件** | `^` | 启动子、增强子、内含子 | 衍生 |
| **技术方法** | `$` | PCR、电泳、测序 | 应用 |
| **实验材料** | `*` | 引物、探针、质粒 | 应用 |
| **疾病/表型** | `!` | 癌症、遗传病、突变 | 应用 |
| **理论/模型** | `%` | 中心法则、操纵子模型 | 核心 |
| **人物/发现** | `+` | Watson、Crick、双螺旋发现 | 核心 |
| **定量参数** | `?` | Tm值、酶活、浓度 | 衍生 |

### 2.2 标记符号对照

```markdown
原文：DNA聚合酶在复制叉处催化DNA链的延伸。

标注后：
〖@DNA聚合酶〗在〖=复制叉〗处催化〖&DNA〗链的〖~延伸〗。

标记说明：
- 〖@ 〗 酶/蛋白质
- 〖= 〗 大分子结构
- 〖& 〗 分子
- 〖~ 〗 生物过程
```

---

## 三、核心概念识别

### 3.1 识别标准

一个概念被判定为核心概念需满足以下条件：

| 标准 | 说明 | 检查方法 |
|------|------|----------|
| 大纲地位 | 出现在课程大纲的一级主题中 | 对照教学大纲 |
| 出现频率 | 在全课程中出现>20次 | 全文检索统计 |
| 前置依赖 | 被多个后续概念依赖 | 依赖图分析 |
| 跨章引用 | 被其他章节频繁引用 | 交叉引用统计 |
| 评估权重 | 在考试中占较高分值 | 历年试题分析 |

### 3.2 核心概念示例（DNA复制章节）

```json
{
  "chapter": "02_DNA复制",
  "core_concepts": [
    {
      "id": "C02.01",
      "name": "DNA复制",
      "name_en": "DNA Replication",
      "definition": "以亲代DNA为模板合成子代DNA的过程",
      "level": "core",
      "type": "process",
      "importance": 5,
      "prerequisites": ["C01.03"]
    },
    {
      "id": "C02.02",
      "name": "半保留复制",
      "name_en": "Semi-conservative Replication",
      "definition": "每个子代DNA分子包含一条亲代链和一条新合成链",
      "level": "core",
      "type": "mechanism",
      "importance": 5,
      "prerequisites": ["C02.01"]
    },
    {
      "id": "C02.03",
      "name": "DNA聚合酶",
      "name_en": "DNA Polymerase",
      "definition": "催化DNA链延伸的酶",
      "level": "core",
      "type": "enzyme",
      "importance": 5,
      "prerequisites": ["C02.01"]
    },
    {
      "id": "C02.04",
      "name": "复制叉",
      "name_en": "Replication Fork",
      "definition": "DNA复制时形成的Y形结构",
      "level": "core",
      "type": "structure",
      "importance": 4,
      "prerequisites": ["C02.01"]
    },
    {
      "id": "C02.05",
      "name": "端粒酶",
      "name_en": "Telomerase",
      "definition": "延长染色体末端端粒的逆转录酶",
      "level": "core",
      "type": "enzyme",
      "importance": 4,
      "prerequisites": ["C02.01", "C02.03"]
    }
  ]
}
```

---

## 四、衍生概念构建

### 4.1 衍生规则

衍生概念从核心概念派生，遵循以下规则：

```
核心概念 + 维度 → 衍生概念

维度包括：
- 结构维度：组成、部位、变体
- 过程维度：阶段、方向、方式
- 功能维度：活性、调控、相互作用
- 分类维度：类型、家族、亚型
```

### 4.2 衍生概念示例

**从"DNA复制"派生**：

| 维度 | 衍生概念 | 定义 | 标记 |
|------|----------|------|------|
| 方向 | 双向复制 | 从起点向两个方向同时进行 | `~双向复制` |
| 连续性 | 半不连续复制 | 前导链连续，滞后链不连续 | `~半不连续复制` |
| 阶段 | 起始阶段 | 复制起点识别和解旋 | `~起始` |
| 阶段 | 延伸阶段 | DNA链的合成延伸 | `~延伸` |
| 阶段 | 终止阶段 | 复制完成和连接 | `~终止` |

**从"DNA聚合酶"派生**：

| 维度 | 衍生概念 | 定义 | 标记 |
|------|----------|------|------|
| 类型 | DNA聚合酶I | 参与修复和引物切除 | `@DNA聚合酶I` |
| 类型 | DNA聚合酶II | 参与DNA修复 | `@DNA聚合酶II` |
| 类型 | DNA聚合酶III | 主要复制酶 | `@DNA聚合酶III` |
| 活性 | 5'→3'聚合活性 | 催化DNA链延伸 | `?5'→3'聚合活性` |
| 活性 | 3'→5'外切活性 | 校对功能 | `?3'→5'外切活性` |

### 4.3 衍生概念数据结构

```json
{
  "chapter": "02_DNA复制",
  "derived_concepts": [
    {
      "id": "D02.01",
      "name": "前导链",
      "name_en": "Leading Strand",
      "definition": "连续合成的DNA链",
      "level": "derived",
      "type": "structure",
      "derived_from": "C02.01",
      "dimension": "连续性",
      "importance": 3
    },
    {
      "id": "D02.02",
      "name": "滞后链",
      "name_en": "Lagging Strand",
      "definition": "不连续合成的DNA链",
      "level": "derived",
      "type": "structure",
      "derived_from": "C02.01",
      "dimension": "连续性",
      "importance": 3
    },
    {
      "id": "D02.03",
      "name": "冈崎片段",
      "name_en": "Okazaki Fragments",
      "definition": "滞后链上合成的不连续短片段",
      "level": "derived",
      "type": "structure",
      "derived_from": "D02.02",
      "dimension": "结构",
      "importance": 3
    }
  ]
}
```

---

## 五、应用实例构建

### 5.1 应用类型

应用实例分为以下类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| **实验技术** | 基于概念开发的实验方法 | PCR、DNA测序、基因克隆 |
| **案例分析** | 概念在真实研究中的应用 | Meselson-Stahl实验 |
| **问题解决** | 利用概念解决生物学问题 | 突变检测、基因诊断 |
| **前沿应用** | 最新技术进展 | CRISPR基因编辑、mRNA疫苗 |
| **临床转化** | 医学应用 | 基因治疗、分子诊断 |

### 5.2 应用实例数据结构

```json
{
  "chapter": "02_DNA复制",
  "applications": [
    {
      "id": "A02.01",
      "name": "PCR技术",
      "name_en": "Polymerase Chain Reaction",
      "level": "application",
      "type": "technique",
      "based_on": ["C02.03", "C02.01"],
      "description": "基于DNA复制的体外扩增技术",
      "components": ["DNA模板", "引物", "dNTPs", "DNA聚合酶"],
      "steps": ["变性", "退火", "延伸"],
      "importance": 5
    },
    {
      "id": "A02.02",
      "name": "Meselson-Stahl实验",
      "name_en": "Meselson-Stahl Experiment",
      "level": "application",
      "type": "case_study",
      "based_on": ["C02.02"],
      "description": "证明DNA半保留复制的经典实验",
      "year": 1958,
      "method": "密度梯度离心",
      "conclusion": "DNA复制是半保留的",
      "importance": 4
    }
  ]
}
```

---

## 六、概念层级树

### 6.1 树形结构表示

```
DNA复制（核心）
├── 半保留复制（核心）
│   └── Meselson-Stahl实验（应用）
├── DNA聚合酶（核心）
│   ├── DNA聚合酶I（衍生）
│   ├── DNA聚合酶II（衍生）
│   ├── DNA聚合酶III（衍生）
│   └── PCR技术（应用）
├── 复制叉（核心）
│   ├── 前导链（衍生）
│   ├── 滞后链（衍生）
│   │   └── 冈崎片段（衍生）
│   └── DNA连接酶（衍生）
└── 端粒酶（核心）
    └── 端粒延长机制（衍生）
```

### 6.2 数据结构

```json
{
  "concept_tree": {
    "id": "C02.01",
    "name": "DNA复制",
    "level": "core",
    "children": [
      {
        "id": "C02.02",
        "name": "半保留复制",
        "level": "core",
        "children": [
          {
            "id": "A02.02",
            "name": "Meselson-Stahl实验",
            "level": "application"
          }
        ]
      },
      {
        "id": "C02.03",
        "name": "DNA聚合酶",
        "level": "core",
        "children": [
          {
            "id": "D02.04",
            "name": "DNA聚合酶I",
            "level": "derived"
          },
          {
            "id": "D02.05",
            "name": "DNA聚合酶II",
            "level": "derived"
          },
          {
            "id": "D02.06",
            "name": "DNA聚合酶III",
            "level": "derived"
          },
          {
            "id": "A02.01",
            "name": "PCR技术",
            "level": "application"
          }
        ]
      }
    ]
  }
}
```

---

## 七、工具链

### 7.1 脚本一览

| 脚本 | 位置 | 功能 |
|------|------|------|
| `concept_extract.py` | scripts/ | 从标注文本提取概念 |
| `concept_classify.py` | scripts/ | 对概念进行层级分类 |
| `concept_hierarchy.py` | scripts/ | 构建概念层级树 |
| `concept_tree_build.py` | scripts/ | 生成概念树可视化 |
| `lint_concepts.py` | scripts/ | 概念层级验证 |

### 7.2 处理流程

```bash
# 1. 提取所有概念
python scripts/concept_extract.py

# 2. 对概念进行层级分类
python scripts/concept_classify.py

# 3. 构建概念层级树
python scripts/concept_hierarchy.py

# 4. 生成可视化
python scripts/concept_tree_build.py

# 5. 验证
python scripts/lint_concepts.py
```

---

## 八、质量检查

### 8.1 lint_concepts.py 检查项

**概念层级检查**：
- 每个概念有明确的level标记（core/derived/application）
- 核心概念数量适中（每章3-5个）
- 衍生概念有明确的derived_from指向
- 应用实例有明确的based_on指向

**概念完整性检查**：
- 概念有定义
- 概念有英文名称
- 概念有类型标记

**常见问题及修复**：

| 问题 | 表现 | 修复方式 |
|------|------|---------|
| 核心概念过多 | 每章>10个核心概念 | 合并相关概念，或降级为衍生概念 |
| 悬空衍生概念 | derived_from指向不存在的概念 | 修正指向或补充缺失概念 |
| 循环派生 | A派生B，B又派生A | 检查并打破循环 |
| 概念缺失定义 | 只有名称没有定义 | 补充概念定义 |

---

## 九、扩展到其他课程

| 课程类型 | 核心概念示例 | 衍生维度 |
|----------|--------------|----------|
| 细胞生物学 | 细胞膜、细胞器 | 结构、功能、类型 |
| 生物化学 | 代谢途径、酶动力学 | 底物、产物、调控 |
| 遗传学 | 孟德尔定律、连锁互换 | 基因型、表现型、概率 |
| 微生物学 | 细菌结构、病毒复制 | 形态、生理、分类 |

---

*本SKILL文档基于分子生物学课程的概念层级构建经验提炼。*
*核心产出：15章×平均4核心概念 ≈ 60核心概念，~180衍生概念，~90应用实例。*
