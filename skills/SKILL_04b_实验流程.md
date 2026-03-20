# SKILL_04b: 实验流程 — 分子生物学技术的关系网络

> 定义分子生物学实验技术之间的关系网络，包括步骤序列、技术替代和技术组合，建立实验技能学习的结构化路径。

---

## 一、关系类型定义

### 1.1 步骤序列 (sequence / precedes)

**定义**：表示实验步骤之间的先后顺序关系，前一步骤的输出是后一步骤的输入。

**Schema**：
```
(步骤A, precedes, 步骤B, [dependency, output-input])
```

**方向**：步骤A → 步骤B（单向）

**属性**：
- `dependency`: 依赖类型（强/弱）
  - `strong`: 步骤B必须等待步骤A完成（如：纯化必须在提取之后）
  - `weak`: 步骤B可以在步骤A进行中开始（如：准备试剂与样品处理）
- `output-input`: 前一步的输出作为后一步的输入（true/false）
- `time-gap`: 时间间隔（立即/短时间/长时间）
- `condition`: 转换条件（温度/pH/时间等）

**示例**：DNA提取实验步骤序列

| 步骤 | 关系 | 下一步骤 | 依赖 | 输出-输入 |
|------|------|----------|------|-----------|
| 样品收集 | precedes | 细胞裂解 | 强 | 是 |
| 细胞裂解 | precedes | DNA分离 | 强 | 是 |
| DNA分离 | precedes | DNA纯化 | 强 | 是 |
| DNA纯化 | precedes | DNA定量 | 强 | 是 |
| DNA定量 | precedes | 质量检测 | 弱 | 否 |
| 质量检测 | precedes | 储存/使用 | 强 | 是 |

**完整实验流程示例**：

#### 1. DNA提取流程
```
样品准备
  → 细胞裂解（裂解液 + 蛋白酶K）
    → DNA释放
      → 酚-氯仿抽提 或 柱式纯化
        → DNA沉淀（乙醇/异丙醇）
          → DNA洗涤（70%乙醇）
            → DNA溶解（TE缓冲液/水）
              → 浓度测定（NanoDrop/荧光法）
                → 质量检测（电泳/分光光度计）
                  → [合格] → 储存(-20°C) / 下游实验
                  → [不合格] → 重新提取
```

#### 2. RNA提取流程（TRIzol法）
```
样品收集与液氮速冻
  → 样品研磨/匀浆
    → TRIzol裂解
      → 氯仿相分离
        → 水相回收
          → 异丙醇沉淀RNA
            → 75%乙醇洗涤
              → RNA溶解（DEPC水）
                → DNase I处理（去除DNA污染）
                  → 再次纯化
                    → 浓度与纯度检测
                      → 完整性检测（RIN值）
                        → 逆转录 / 储存(-80°C)
```

#### 3. PCR实验流程
```
模板DNA准备
  → 引物设计（软件设计 + BLAST验证）
    → 反应体系配制
      │   ├── DNA模板
      │   ├── 正向引物
      │   ├── 反向引物
      │   ├── dNTPs
      │   ├── 缓冲液
      │   ├── Mg²⁺
      │   └── Taq酶
      ↓
    热循环仪设置
      │   ├── 预变性（94-95°C, 2-5min）
      │   ├── 循环（30-35次）
      │   │     ├── 变性（94°C, 30s）
      │   │     ├── 退火（50-65°C, 30s）
      │   │     └── 延伸（72°C, 1kb/min）
      │   └── 终延伸（72°C, 5-10min）
      ↓
    产物检测（琼脂糖电泳）
      → 结果分析
        → [阳性] → 产物纯化 / 测序验证
        → [阴性] → 优化条件 / 重新设计
```

#### 4. Western Blot流程
```
蛋白质样品制备
  → 蛋白质定量（BCA/Bradford法）
    → SDS-PAGE电泳
      │   ├── 制胶（分离胶 + 浓缩胶）
      │   ├── 样品变性（95°C, 5min）
      │   ├── 上样
      │   ├── 电泳（80V浓缩 → 120V分离）
      │   └──  marker观察
      ↓
    转膜
      │   ├── 膜平衡（PVDF/NC膜）
      │   ├── 三明治组装
      │   ├── 转印（湿转/半干转/干转）
      │   └── 转印效率检测（丽春红染色）
      ↓
    封闭（5%脱脂奶粉/BSA）
      → 一抗孵育（4°C过夜）
        → 洗涤（TBST × 3）
          → 二抗孵育（室温1-2h）
            → 洗涤（TBST × 3）
              → 显色/发光（ECL/荧光）
                → 成像与分析
```

**发现方法**：
1. **模式匹配**："首先...然后..."、"接着..."、"之后..."
2. **动词分析**：提取表示顺序的动词（提取→纯化→检测）
3. **输入输出匹配**：前一步的输出名词与后一步的输入名词匹配
4. **LLM推理**：从实验描述中提取步骤顺序

---

### 1.2 技术替代 (alternative-to)

**定义**：表示两种或多种技术可以互相替代，用于相同或类似的目的。

**Schema**：
```
(技术A, alternative-to, 技术B, [criteria, preference-context])
```

**方向**：双向（无向关系）

**属性**：
- `criteria`: 比较维度（灵敏度/特异性/成本/时间/设备要求）
- `preference-context`: 优先选择的场景
- `equivalence`: 等效程度（完全等效/部分等效/条件等效）
- `trade-offs`: 权衡因素列表

**示例**：

| 技术A | 关系 | 技术B | 比较维度 | 优选场景 |
|-------|------|-------|----------|----------|
| Northern Blot | alternative-to | RT-PCR | 灵敏度/定量性 | Northern用于RNA大小确认，RT-PCR用于定量 |
| RT-PCR | alternative-to | RT-qPCR | 定量精度 | RT-qPCR用于精确定量 |
| Western Blot | alternative-to | ELISA | 通量/特异性 | ELISA用于高通量，Western用于分子量确认 |
| Sanger测序 | alternative-to | NGS | 成本/通量/读长 | Sanger用于验证，NGS用于大规模筛选 |
| 质粒提取（碱裂解法） | alternative-to | 质粒提取（柱式法） | 成本/时间/纯度 | 柱式法快速，碱裂解法经济 |
| 转染（脂质体） | alternative-to | 转染（电穿孔） | 效率/细胞毒性 | 脂质体用于易转染细胞，电穿孔用于难转染细胞 |
| 基因敲除（CRISPR） | alternative-to | 基因敲除（RNAi） | 永久性/效率 | CRISPR永久敲除，RNAi瞬时敲低 |

**详细对比示例**：

#### 1. RNA检测：Northern Blot vs RT-PCR

| 维度 | Northern Blot | RT-PCR |
|------|---------------|--------|
| 原理 | 杂交检测 | 逆转录+扩增 |
| 灵敏度 | 中（ng级） | 高（pg级） |
| 特异性 | 高（大小+序列） | 高（序列特异性） |
| 定量性 | 半定量 | 精确定量（qPCR） |
| 样品量 | 需要较多（10-20μg） | 需要较少（ng级） |
| 时间 | 2-3天 | 半天-1天 |
| 设备 | 电泳+转膜设备 | 热循环仪 |
| 优势 | 可检测RNA大小、可变剪切 | 高灵敏度、精确定量 |
| 劣势 | 灵敏度低、耗时长 | 无法直接看RNA大小 |

#### 2. 蛋白质检测：Western Blot vs ELISA

| 维度 | Western Blot | ELISA |
|------|--------------|-------|
| 原理 | 电泳分离+免疫检测 | 固相免疫检测 |
| 灵敏度 | 中（pg级） | 高（fg级） |
| 特异性 | 高（分子量+抗体） | 中（依赖抗体） |
| 通量 | 低（每次1-10个样品） | 高（96/384孔板） |
| 分子量信息 | 有 | 无 |
| 定量性 | 半定量 | 精确定量 |
| 时间 | 2-3天 | 半天 |
| 优势 | 分子量确认、翻译后修饰检测 | 高通量、精确定量 |
| 劣势 | 通量低、耗时长 | 无分子量信息 |

#### 3. 基因功能研究：CRISPR vs RNAi

| 维度 | CRISPR-Cas9 | RNAi |
|------|-------------|------|
| 机制 | DNA切割、基因敲除 | mRNA降解、基因敲低 |
| 效果 | 永久性、完全敲除 | 瞬时性、部分敲低（70-90%） |
| 脱靶效应 | 低（优化后） | 中 |
| 设计难度 | 需要PAM序列 | 较简单 |
| 成本 | 中 | 低 |
| 时间 | 2-4周建立细胞系 | 几天 |
| 可逆性 | 不可逆 | 可逆 |
| 优势 | 永久、完全敲除、可敲入 | 快速、简单、成本低 |
| 劣势 | 周期长、可能致死 | 不完全敲低、瞬时 |

**发现方法**：
1. **关键词匹配**："也可以用..."、"替代方法..."、"另一种选择是..."
2. **目的匹配**：相同实验目的的不同技术路径
3. **教材对比**：教材中并列介绍的技术
4. **LLM推理**：从技术描述中推断可替代性

---

### 1.3 技术组合 (combination-of / uses)

**定义**：表示复杂技术由多个基础技术组合而成，或某技术使用/依赖其他技术。

**Schema**：
```
(复合技术, combination-of, 基础技术, [role, necessity])
```

**方向**：复合技术 → 基础技术（单向）

**属性**：
- `role`: 在组合中的作用（核心/辅助/前置/验证）
- `necessity`: 必要性（必需/可选/增强）
- `order`: 执行顺序（并行/串行）

**示例**：

| 复合技术 | 关系 | 基础技术 | 作用 | 必要性 |
|----------|------|----------|------|--------|
| ChIP-seq | combination-of | ChIP | 核心 | 必需 |
| ChIP-seq | combination-of | 高通量测序 | 核心 | 必需 |
| ChIP-seq | combination-of | 生物信息学分析 | 核心 | 必需 |
| RNA-seq | combination-of | RNA提取 | 前置 | 必需 |
| RNA-seq | combination-of | 文库制备 | 核心 | 必需 |
| RNA-seq | combination-of | 高通量测序 | 核心 | 必需 |
| RNA-seq | combination-of | 差异表达分析 | 核心 | 必需 |
| CRISPR-Cas9 | combination-of | sgRNA设计 | 核心 | 必需 |
| CRISPR-Cas9 | combination-of | Cas9表达 | 核心 | 必需 |
| CRISPR-Cas9 | combination-of | 转染 | 核心 | 必需 |
| CRISPR-Cas9 | combination-of | 单克隆筛选 | 辅助 | 可选 |
| RT-qPCR | combination-of | 逆转录（RT） | 核心 | 必需 |
| RT-qPCR | combination-of | 实时定量PCR（qPCR） | 核心 | 必需 |
| 质谱蛋白质组学 | combination-of | 蛋白质提取 | 前置 | 必需 |
| 质谱蛋白质组学 | combination-of | 蛋白质酶切 | 核心 | 必需 |
| 质谱蛋白质组学 | combination-of | LC-MS/MS | 核心 | 必需 |
| 质谱蛋白质组学 | combination-of | 蛋白质鉴定 | 核心 | 必需 |

**技术组合层级示例**：

```
ChIP-seq
├── 湿实验部分
│   ├── 交联（Crosslinking）
│   ├── 染色质断裂（Sonication/Enzyme）
│   ├── 免疫沉淀（IP）
│   ├── 解交联（Reverse crosslinking）
│   ├── DNA纯化
│   └── 文库制备
│       ├── 末端修复
│       ├── 加A尾
│       ├── 接头连接
│       └── PCR扩增
├── 测序部分
│   └── 高通量测序（Illumina）
└── 干实验部分
    ├── 质量控制（FastQC）
    ├── 比对（Bowtie2/BWA）
    ├── 峰 calling（MACS2）
    ├── 注释（ChIPseeker）
    └──  motif分析（HOMER/MEME）
```

```
CRISPR-Cas9基因编辑
├── 设计阶段
│   ├── 靶点选择（sgRNA设计）
│   ├── 脱靶预测（Cas-OFFinder）
│   └── 载体构建
│       ├── sgRNA克隆
│       └── Cas9表达载体
├── 实验阶段
│   ├── 细胞培养
│   ├── 转染/电穿孔
│   │   ├── 质粒转染
│   │   ├── RNP复合物递送
│   │   └── 病毒转导
│   └── 筛选
│       ├── 抗生素筛选
│       └── 单克隆分离
└── 验证阶段
    ├── 基因组DNA提取
    ├── 编辑效率检测（T7E1）
    ├── 测序验证（Sanger/NGS）
    └── 功能验证
```

**发现方法**：
1. **名称分析**："X-seq"、"X-PCR"等复合技术命名
2. **流程分解**：从完整流程中提取子技术
3. **依赖分析**：某技术需要其他技术作为前置
4. **LLM推理**：从技术描述中提取组成关系

---

## 二、实验技术知识图谱

### 2.1 技术分类体系

```
分子生物学实验技术
├── 核酸操作技术
│   ├── 核酸提取
│   │   ├── DNA提取
│   │   │   ├── 基因组DNA提取
│   │   │   ├── 质粒DNA提取
│   │   │   └── 线粒体DNA提取
│   │   └── RNA提取
│   │       ├── 总RNA提取
│   │       ├── mRNA纯化
│   │       └── miRNA提取
│   ├── 核酸扩增
│   │   ├── PCR
│   │   │   ├── 常规PCR
│   │   │   ├── 热启动PCR
│   │   │   ├──  touchdown PCR
│   │   │   └── 巢式PCR
│   │   ├── 定量PCR
│   │   │   ├── RT-qPCR
│   │   │   └── 数字PCR
│   │   └── 等温扩增
│   │       ├── LAMP
│   │       └── RPA
│   ├── 核酸电泳
│   │   ├── 琼脂糖凝胶电泳
│   │   ├── PAGE
│   │   └── 脉冲场凝胶电泳
│   ├── 核酸杂交
│   │   ├── Southern Blot
│   │   ├── Northern Blot
│   │   └── 原位杂交
│   └── 核酸测序
│       ├── Sanger测序
│       └── 高通量测序
│           ├── DNA-seq
│           ├── RNA-seq
│           ├── ChIP-seq
│           ├── ATAC-seq
│           └── 单细胞测序
├── 蛋白质操作技术
│   ├── 蛋白质提取与分离
│   │   ├── 蛋白质提取
│   │   ├── SDS-PAGE
│   │   ├── 双向电泳
│   │   └── 层析
│   │       ├── 离子交换层析
│   │       ├── 凝胶过滤层析
│   │       └── 亲和层析
│   ├── 蛋白质检测
│   │   ├── Western Blot
│   │   ├── ELISA
│   │   ├── 免疫组化
│   │   └── 免疫荧光
│   ├── 蛋白质相互作用
│   │   ├── Co-IP
│   │   ├── Yeast Two-Hybrid
│   │   ├── FRET
│   │   └── 质谱蛋白质组学
│   └── 蛋白质修饰分析
│       ├── 磷酸化检测
│       ├── 泛素化检测
│       └── 质谱修饰分析
├── 细胞操作技术
│   ├── 细胞培养
│   ├── 细胞转染
│   │   ├── 脂质体转染
│   │   ├── 电穿孔
│   │   └── 病毒转导
│   ├── 基因编辑
│   │   ├── CRISPR-Cas9
│   │   ├── TALEN
│   │   └── ZFN
│   ├── 流式细胞术
│   └── 显微操作
└── 生物信息学分析
    ├── 序列分析
    ├── 基因组分析
    ├── 转录组分析
    ├── 蛋白质组分析
    └── 系统生物学
```

### 2.2 技术关系网络示例

#### PCR技术家族关系

```
PCR
├── precedes → 产物纯化
├── precedes → 克隆
├── precedes → 测序
├── alternative-to → 等温扩增
├── combination-of → 逆转录 = RT-PCR
├── combination-of → 实时荧光 = qPCR
├── combination-of → 逆转录 + 实时荧光 = RT-qPCR
└── combination-of → 数字PCR

RT-PCR
├── precedes → 电泳检测
├── alternative-to → Northern Blot
└── combination-of → qPCR = RT-qPCR

qPCR
├── alternative-to → 常规PCR（定量能力）
├── alternative-to → 数字PCR
└── combination-of → RT = RT-qPCR
```

#### 测序技术演进关系

```
Sanger测序
├── precedes → NGS（历史发展）
├── alternative-to → NGS（小规模验证）
├── combination-of → 克隆 = 克隆测序
└── used-by → 片段验证

NGS（二代测序）
├── precedes → 生物信息学分析
├── alternative-to → Sanger（大规模应用）
├── combination-of → ChIP = ChIP-seq
├── combination-of → RNA提取 + 文库制备 = RNA-seq
├── combination-of → DNA-seq
├── combination-of → ATAC = ATAC-seq
└── precedes → 三代测序（技术演进）

三代测序
├── alternative-to → NGS（读长优势）
└── combination-of → 各种应用
```

---

## 三、关系发现方法

### 3.1 规则匹配模式

```python
EXPERIMENT_RELATION_PATTERNS = {
    # 步骤序列
    "precedes": [
        r"首先({step})，然后({step})",
        r"({step})后，进行({step})",
        r"({step})完成后，({step})",
        r"({step})是({step})的前置步骤",
        r"({step})的产物用于({step})",
    ],
    
    # 技术替代
    "alternative-to": [
        r"({tech})也可以用({tech})替代",
        r"({tech})和({tech})都可以用于",
        r"({tech})的替代方法是({tech})",
        r"除了({tech})，还可以使用({tech})",
    ],
    
    # 技术组合
    "combination-of": [
        r"({tech})是({tech})和({tech})的组合",
        r"({tech})结合了({tech})和({tech})",
        r"({tech})包括({tech})",
        r"({tech})使用({tech})",
        r"({tech})依赖({tech})",
    ],
}
```

### 3.2 LLM推理提示词

```markdown
## 任务
分析以下分子生物学实验技术之间的关系。

## 技术信息
技术A: {tech_a}
技术B: {tech_b}

## 上下文描述
{context}

## 关系类型选项
1. **precedes**: A是B的前置步骤（A完成后才能进行B）
2. **alternative-to**: A和B是替代关系（可用于相同目的）
3. **combination-of**: A是B的组合/包含B（A使用或依赖B）
4. **output-of**: A的产物是B的输入
5. **prerequisite**: A是B的必要前提
6. **none**: 无明确关系

## 输出格式
```json
{
  "relation_type": "关系类型",
  "direction": "A→B / B→A / 双向",
  "confidence": 0.0-1.0,
  "reasoning": "推理理由",
  "attributes": {
    "dependency": "强/弱",
    "output_input": true/false,
    "trade_offs": ["权衡因素"]
  }
}
```

## 示例
- precedes: "细胞裂解 precedes DNA纯化"
- alternative-to: "Northern Blot alternative-to RT-PCR"
- combination-of: "ChIP-seq combination-of ChIP"
```

---

## 四、学习路径生成

基于实验流程关系网络，可以自动生成学习路径：

```python
def generate_learning_path(target_technique, student_level):
    """生成学习路径"""
    
    # 1. 获取前置技术（prerequisite/precedes）
    prerequisites = get_prerequisites(target_technique)
    
    # 2. 获取基础技术（combination-of）
    basic_techs = get_basic_techniques(target_technique)
    
    # 3. 获取替代技术（alternative-to，用于对比学习）
    alternatives = get_alternatives(target_technique)
    
    # 4. 根据学生水平排序
    if student_level == "beginner":
        path = prerequisites + basic_techs
    elif student_level == "intermediate":
        path = prerequisites + basic_techs + [target_technique]
    else:
        path = prerequisites + basic_techs + [target_technique] + alternatives
    
    return path

# 示例：ChIP-seq学习路径
learning_path = generate_learning_path("ChIP-seq", "intermediate")
# 输出: ["DNA提取", "PCR", "ChIP", "高通量测序", "生物信息学基础", "ChIP-seq"]
```

---

## 五、数据格式

### 5.1 实验技术关系JSON

```json
{
  "relation_id": "exp_rel_001",
  "relation_type": "precedes",
  "subject": {
    "id": "tech_001",
    "name": "细胞裂解",
    "type": "experimental_step",
    "category": "DNA提取"
  },
  "object": {
    "id": "tech_002",
    "name": "DNA纯化",
    "type": "experimental_step",
    "category": "DNA提取"
  },
  "properties": {
    "confidence": 1.0,
    "dependency": "strong",
    "output_input": true,
    "evidence": ["教材第3章"]
  },
  "source": {
    "method": "rule_matching",
    "text": "细胞裂解后，进行DNA纯化"
  }
}
```

### 5.2 实验流程模板

```json
{
  "experiment_id": "exp_001",
  "name": "DNA提取",
  "category": "核酸操作",
  "steps": [
    {
      "step_id": "step_001",
      "name": "样品收集",
      "order": 1,
      "prerequisites": [],
      "outputs": ["样品"],
      "duration": "10min"
    },
    {
      "step_id": "step_002",
      "name": "细胞裂解",
      "order": 2,
      "prerequisites": ["step_001"],
      "inputs": ["样品"],
      "outputs": ["裂解液"],
      "duration": "30min"
    },
    {
      "step_id": "step_003",
      "name": "DNA纯化",
      "order": 3,
      "prerequisites": ["step_002"],
      "inputs": ["裂解液"],
      "outputs": ["纯化DNA"],
      "duration": "1h"
    }
  ]
}
```
