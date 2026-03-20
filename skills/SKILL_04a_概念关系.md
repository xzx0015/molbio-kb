# SKILL_04a: 概念关系 — 分子生物学概念的语义关联

> 定义分子生物学概念间的上下位、因果、组成、调控等关系类型，建立理论知识体系的结构化表示。

---

## 一、关系类型定义

### 1.1 上下位关系 (is-a / hypernym-hyponym)

**定义**：表示概念之间的层级分类关系，子概念继承父概念的所有属性。

**Schema**：
```
(子概念, is-a, 父概念)
```

**方向**：子概念 → 父概念（单向）

**属性**：
- `inheritance`: 继承属性列表
- `differentiation`: 区分特征

**示例**：

| 子概念 | 关系 | 父概念 | 区分特征 |
|--------|------|--------|----------|
| 外显子 | is-a | 基因片段 | 编码蛋白质序列 |
| 内含子 | is-a | 基因片段 | 非编码序列，转录后剪切 |
| mRNA | is-a | RNA | 携带遗传信息，指导蛋白质合成 |
| tRNA | is-a | RNA | 转运氨基酸 |
| rRNA | is-a | RNA | 核糖体组成成分 |
| 点突变 | is-a | 基因突变 | 单个碱基改变 |
| 缺失突变 | is-a | 基因突变 | 碱基序列缺失 |
| 插入突变 | is-a | 基因突变 | 碱基序列插入 |
| 癌基因 | is-a | 基因 | 突变后促进细胞癌变 |
| 抑癌基因 | is-a | 基因 | 抑制细胞异常增殖 |

**层级示例**：
```
生物大分子
├── 核酸
│   ├── DNA
│   │   ├── 基因
│   │   │   ├── 外显子
│   │   │   └── 内含子
│   │   ├── 调控序列
│   │   │   ├── 启动子
│   │   │   ├── 增强子
│   │   │   └── 沉默子
│   │   └── 重复序列
│   └── RNA
│       ├── mRNA
│       ├── tRNA
│       ├── rRNA
│       ├── miRNA
│       └── lncRNA
├── 蛋白质
│   ├── 酶
│   │   ├── 激酶
│   │   ├── 磷酸酶
│   │   └── 蛋白酶
│   ├── 结构蛋白
│   ├── 转运蛋白
│   └── 转录因子
└── 多糖
```

**发现方法**：
1. **模式匹配**："X是Y的一种"、"X属于Y"、"X可分为A、B、C"
2. **本体推理**：基于GO等数据库的层级结构
3. **LLM推理**：从定义文本中推断分类关系

---

### 1.2 因果关系 (causes / leads-to)

**定义**：表示一个概念（原因）导致另一个概念（结果）发生的关系。

**Schema**：
```
(原因, causes, 结果, [mechanism, strength, condition])
```

**方向**：原因 → 结果（单向）

**属性**：
- `mechanism`: 因果机制（分子/细胞/生理层面）
- `strength`: 因果强度（强/中/弱）
- `condition`: 适用条件/上下文
- `evidence`: 证据等级（实验/临床/流行病学）

**示例**：

| 原因 | 关系 | 结果 | 机制 | 强度 |
|------|------|------|------|------|
| DNA突变 | causes | 遗传病 | 蛋白质功能改变 | 强 |
| 碱基替换 | causes | 错义突变 | 密码子改变 | 强 |
| 无义突变 | causes | 蛋白质截短 | 提前出现终止密码子 | 强 |
| BRCA1突变 | causes | 乳腺癌风险增加 | DNA修复功能丧失 | 中 |
| p53突变 | causes | 细胞癌变 | 细胞周期失控 | 强 |
| 病毒感染 | causes | 细胞凋亡 | 免疫应答激活 | 中 |
| 氧化应激 | causes | DNA损伤 | 活性氧攻击碱基 | 中 |
| 表观遗传改变 | causes | 基因表达异常 | 染色质结构改变 | 中 |

**因果链示例**：
```
紫外线照射
  → DNA损伤（嘧啶二聚体形成）
    → p53激活
      → 细胞周期阻滞（G1期停滞）
        → DNA修复启动
          → [修复成功] → 细胞恢复正常
          → [修复失败] → 细胞凋亡
```

**发现方法**：
1. **模式匹配**："X导致Y"、"X引起Y"、"由于X，Y发生"
2. **数据库导入**：从疾病数据库（OMIM/ClinVar）导入基因-疾病关系
3. **LLM推理**：从机制描述中提取因果关系

---

### 1.3 组成关系 (part-of / has-part)

**定义**：表示整体与部分之间的构成关系。

**Schema**：
```
(部分, part-of, 整体)
(整体, has-part, 部分)
```

**方向**：双向（互逆关系）

**属性**：
- `cardinality`: 数量关系（1:1, 1:n, n:m）
- `essential`: 是否必需（true/false）
- `location`: 空间位置关系

**示例**：

| 部分 | 关系 | 整体 | 数量 | 必需 |
|------|------|------|------|------|
| 大亚基 | part-of | 核糖体 | 1 | 是 |
| 小亚基 | part-of | 核糖体 | 1 | 是 |
| rRNA | part-of | 核糖体亚基 | 多 | 是 |
| 核糖体蛋白 | part-of | 核糖体亚基 | 多 | 是 |
| 外显子 | part-of | 基因 | 多 | 是 |
| 内含子 | part-of | 基因 | 多 | 否（可变剪切） |
| 启动子 | part-of | 基因 | 1 | 是 |
| 增强子 | part-of | 基因调控区 | 多 | 否 |
| 组蛋白 | part-of | 核小体 | 8 | 是 |
| DNA | part-of | 核小体 | 147bp | 是 |
| 核小体 | part-of | 染色质 | 多 | 是 |

**组成层级示例**：
```
细胞
├── 细胞核
│   ├── 核膜
│   ├── 核仁
│   └── 染色质
│       ├── 核小体
│       │   ├── 组蛋白八聚体
│       │   │   ├── H2A (×2)
│       │   │   ├── H2B (×2)
│       │   │   ├── H3 (×2)
│       │   │   └── H4 (×2)
│       │   └── DNA (147bp)
│       └── 连接DNA
├── 细胞质
│   ├── 核糖体
│   │   ├── 大亚基（60S/50S）
│   │   │   ├── rRNA（28S, 5.8S, 5S / 23S, 5S）
│   │   │   └── 核糖体蛋白（~46种）
│   │   └── 小亚基（40S/30S）
│   │       ├── rRNA（18S / 16S）
│   │       └── 核糖体蛋白（~33种）
│   └── ...
└── ...
```

**发现方法**：
1. **模式匹配**："X由Y和Z组成"、"X包含Y"、"Y是X的组分"
2. **结构数据库**：从PDB等结构数据库导入组成关系
3. **LLM推理**：从描述文本中提取组成信息

---

### 1.4 调控关系 (regulates / activates / inhibits)

**定义**：表示一个分子对另一个分子的活性、表达或功能进行调控的关系。

**Schema**：
```
(调控因子, regulates/activates/inhibits, 被调控对象, [mechanism, direction, context])
```

**方向**：调控因子 → 被调控对象（单向）

**属性**：
- `mechanism`: 调控机制（转录/翻译/修饰/定位/降解）
- `direction`: 方向（positive/negative）
- `context`: 细胞类型/组织/发育阶段/环境条件
- `strength`: 调控强度（强/中/弱）
- `evidence`: 实验证据类型

**示例**：

| 调控因子 | 关系 | 被调控对象 | 机制 | 方向 |
|----------|------|------------|------|------|
| 转录因子 | activates | 靶基因 | 转录激活 | 正向 |
| 阻遏蛋白 | inhibits | 靶基因 | 转录抑制 | 负向 |
| 激酶 | activates | 靶蛋白 | 磷酸化 | 正向 |
| 磷酸酶 | inhibits | 靶蛋白 | 去磷酸化 | 负向 |
| miRNA | inhibits | 靶mRNA | 翻译抑制/降解 | 负向 |
| 激素 | activates | 受体 | 信号转导 | 正向 |
| 变构效应物 | regulates | 酶活性 | 构象改变 | 双向 |

**具体调控示例**：

| 调控因子 | 关系 | 被调控对象 | 机制 | 生物学意义 |
|----------|------|------------|------|------------|
| p53 | activates | p21 | 转录激活 | 细胞周期阻滞 |
| p53 | activates | Bax | 转录激活 | 诱导凋亡 |
| MDM2 | inhibits | p53 | 泛素化降解 | p53负反馈调控 |
| Cyclin D | activates | CDK4/6 | 结合激活 | G1期推进 |
| p16 | inhibits | CDK4/6 | 竞争性抑制 | 细胞周期阻滞 |
| E2F | activates | S期基因 | 转录激活 | DNA复制启动 |
| Rb | inhibits | E2F | 结合抑制 | G1期阻滞 |
| AKT | activates | mTOR | 磷酸化激活 | 细胞生长 |
| PTEN | inhibits | AKT | 去磷酸化 | 抑制生长信号 |

**发现方法**：
1. **模式匹配**："X激活Y"、"X抑制Y"、"X促进Y"、"X下调Y"
2. **数据库导入**：从TRANSFAC/JASPAR导入TF-靶基因关系
3. **通路数据库**：从KEGG/Reactome导入调控关系
4. **LLM推理**：从机制描述中提取调控关系

---

## 二、关系发现规则

### 2.1 显式关系模式库

```python
CONCEPT_RELATION_PATTERNS = {
    # 上下位关系
    "is-a": [
        r"({concept})是({concept})的一种",
        r"({concept})属于({concept})",
        r"({concept})是({concept})的类型",
        r"({concept})可分为({concept})",
        r"({concept})包括({concept})",
    ],
    
    # 因果关系
    "causes": [
        r"({concept})导致({concept})",
        r"({concept})引起({concept})",
        r"({concept})造成({concept})",
        r"({concept})引发({concept})",
        r"由于({concept})，({concept})",
        r"({concept})是({concept})的原因",
    ],
    
    # 组成关系
    "part-of": [
        r"({concept})由({concept})组成",
        r"({concept})包含({concept})",
        r"({concept})的组分包括({concept})",
        r"({concept})是({concept})的组成部分",
        r"({concept})由({concept})和({concept})构成",
    ],
    
    # 调控关系
    "activates": [
        r"({concept})激活({concept})",
        r"({concept})促进({concept})",
        r"({concept})上调({concept})",
        r"({concept})增强({concept})",
    ],
    "inhibits": [
        r"({concept})抑制({concept})",
        r"({concept})下调({concept})",
        r"({concept})阻断({concept})",
        r"({concept})减弱({concept})",
    ],
}
```

### 2.2 本体推理规则

```python
ONTOLOGY_INFERENCE_RULES = {
    # 传递性
    "is-a-transitive": {
        "if": [("A", "is-a", "B"), ("B", "is-a", "C")],
        "then": ("A", "is-a", "C"),
        "confidence": 0.95
    },
    
    "part-of-transitive": {
        "if": [("A", "part-of", "B"), ("B", "part-of", "C")],
        "then": ("A", "part-of", "C"),
        "confidence": 0.90
    },
    
    # 继承性
    "property-inheritance": {
        "if": [("A", "is-a", "B"), ("B", "has-property", "P")],
        "then": ("A", "has-property", "P"),
        "confidence": 0.85
    },
    
    # 调控传递
    "activation-chain": {
        "if": [("A", "activates", "B"), ("B", "activates", "C")],
        "then": ("A", "indirectly-activates", "C"),
        "confidence": 0.70
    },
    
    "inhibition-chain": {
        "if": [("A", "inhibits", "B"), ("B", "activates", "C")],
        "then": ("A", "indirectly-inhibits", "C"),
        "confidence": 0.70
    },
}
```

### 2.3 LLM推理提示词

```markdown
## 任务
分析以下分子生物学概念之间的关系，判断它们属于哪种关系类型。

## 概念对
概念A: {entity_a}
概念B: {entity_b}

## 上下文文本
{text_context}

## 关系类型选项
1. **is-a**: A是B的一种/类型/子类（如：tRNA是RNA的一种）
2. **part-of**: A是B的组成部分（如：外显子是基因的组成部分）
3. **causes**: A导致/引起B（如：基因突变导致遗传病）
4. **activates**: A激活/促进B（如：转录因子激活基因表达）
5. **inhibits**: A抑制/下调B（如：阻遏蛋白抑制基因表达）
6. **associates-with**: A与B相关联但无明确因果（如：蛋白质复合物成员）
7. **none**: 无明确关系

## 输出格式
```json
{
  "relation_type": "关系类型",
  "direction": "A→B / B→A / 无向",
  "confidence": 0.0-1.0,
  "reasoning": "推理理由",
  "evidence": "证据文本片段"
}
```

---

## 三、分子生物学概念关系示例

### 3.1 核酸相关概念关系

```
DNA
├── is-a → 核酸
├── has-part → 碱基（A/T/G/C）
├── has-part → 脱氧核糖
├── has-part → 磷酸基团
├── has-part → 基因
│   ├── has-part → 外显子
│   ├── has-part → 内含子
│   └── has-part → 启动子
├── has-part → 调控序列
│   ├── has-part → 增强子
│   ├── has-part → 沉默子
│   └── has-part → 绝缘子
└── has-part → 端粒

RNA
├── is-a → 核酸
├── has-part → 碱基（A/U/G/C）
├── has-part → 核糖
├── has-part → 磷酸基团
├── has-subtype → mRNA
├── has-subtype → tRNA
├── has-subtype → rRNA
├── has-subtype → miRNA
└── has-subtype → lncRNA
```

### 3.2 蛋白质相关概念关系

```
蛋白质
├── is-a → 生物大分子
├── has-part → 氨基酸
├── has-part → 一级结构（氨基酸序列）
├── has-part → 二级结构（α螺旋/β折叠）
├── has-part → 三级结构
├── has-part → 四级结构（多亚基）
├── has-subtype → 酶
│   ├── has-subtype → 激酶
│   ├── has-subtype → 磷酸酶
│   ├── has-subtype → 蛋白酶
│   └── has-subtype → 聚合酶
├── has-subtype → 结构蛋白
├── has-subtype → 转运蛋白
├── has-subtype → 转录因子
└── has-subtype → 受体蛋白
```

### 3.3 基因突变与疾病关系

```
基因突变
├── causes → 遗传病
│   ├── 镰刀型细胞贫血：HbS突变
│   ├── 囊性纤维化：CFTR突变
│   └── 亨廷顿病：CAG重复扩增
├── causes → 癌症（累积突变）
│   ├── 原癌基因激活（Ras, Myc）
│   └── 抑癌基因失活（p53, Rb）
└── part-of → 进化过程

突变类型
├── is-a → 点突变
│   ├── causes → 错义突变（氨基酸改变）
│   ├── causes → 无义突变（提前终止）
│   └── causes → 同义突变（ silent）
├── is-a → 插入突变
├── is-a → 缺失突变
├── is-a → 重复突变
├── is-a → 倒位突变
└── is-a → 易位突变
```

---

## 四、数据格式

### 4.1 概念关系JSON Schema

```json
{
  "relation_id": "concept_rel_001",
  "relation_type": "is-a",
  "subject": {
    "id": "ent_exon",
    "name": "外显子",
    "type": "concept",
    "category": "gene_structure"
  },
  "object": {
    "id": "ent_gene_segment",
    "name": "基因片段",
    "type": "concept",
    "category": "gene_structure"
  },
  "properties": {
    "confidence": 1.0,
    "differentiation": "编码蛋白质序列",
    "inheritance": ["DNA序列", "遗传信息"]
  },
  "source": {
    "method": "rule_matching",
    "text": "外显子是基因中编码蛋白质的部分",
    "chapter": "ch02_gene_structure"
  }
}
```

### 4.2 关系统计输出

```markdown
| 关系类型 | 数量 | 占比 | 主要来源 |
|----------|------|------|----------|
| is-a | 450 | 35% | 教材定义 + GO |
| part-of | 320 | 25% | 教材描述 + 结构数据 |
| causes | 180 | 14% | 疾病数据库 + 文献 |
| activates | 200 | 16% | 通路数据库 + 文献 |
| inhibits | 130 | 10% | 通路数据库 + 文献 |
| total | 1,280 | 100% | - |
```
