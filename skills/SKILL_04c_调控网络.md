# SKILL_04c: 调控网络 — 分子调控关系的知识图谱

> 定义分子生物学中的转录调控、信号通路和代谢网络关系，构建分子机制的结构化表示。

---

## 一、关系类型定义

### 1.1 转录调控 (transcriptional-regulation)

**定义**：表示转录因子（TF）或其他调控因子对靶基因转录水平的影响。

**Schema**：
```
(调控因子, regulates/activates/inhibits, 靶基因, [mechanism, binding-site, context])
```

**方向**：调控因子 → 靶基因（单向）

**属性**：
- `mechanism`: 调控机制
  - `transcriptional_activation`: 转录激活
  - `transcriptional_repression`: 转录抑制
  - `chromatin_remodeling`: 染色质重塑
  - `enhancer_promoter_looping`: 增强子-启动子环化
- `binding-site`: 结合位点（启动子/增强子/沉默子/绝缘子）
- `context`: 细胞类型/组织/发育阶段/环境刺激
- `evidence`: 实验证据（ChIP-seq/RNA-seq/报告基因/EMSA）
- `confidence`: 置信度

**示例**：

| 调控因子 | 关系 | 靶基因 | 机制 | 结合位点 | 上下文 |
|----------|------|--------|------|----------|--------|
| p53 | activates | p21 | 转录激活 | 启动子p53结合元件 | DNA损伤 |
| p53 | activates | Bax | 转录激活 | 启动子 | 凋亡诱导 |
| p53 | activates | GADD45 | 转录激活 | 启动子 | DNA损伤 |
| p53 | inhibits | MDM2 | 转录抑制 | 启动子 | 负反馈 |
| c-Myc | activates | Cyclin D1 | 转录激活 | E-box元件 | 细胞增殖 |
| NF-κB | activates | IL-6 | 转录激活 | κB位点 | 炎症反应 |
| Oct4 | activates | Nanog | 转录激活 | 启动子 | 干细胞维持 |
| REST | inhibits | 神经元基因 | 转录抑制 | NRSE元件 | 非神经组织 |
| HIF-1α | activates | VEGF | 转录激活 | HRE元件 | 低氧条件 |
| STAT3 | activates | SOCS3 | 转录激活 | GAS元件 | IL-6信号 |

**转录调控层级示例**：

```
DNA损伤信号
  → ATM/ATR激活
    → p53磷酸化稳定
      → p53核定位
        ├── activates → p21
        │   └── 细胞周期阻滞（G1/S检查点）
        ├── activates → GADD45
        │   └── DNA修复
        ├── activates → Bax
        │   └── 线粒体凋亡途径
        ├── activates → PUMA
        │   └── 凋亡
        └── inhibits → MDM2
            └── 负反馈调控p53水平
```

**细胞周期调控网络**：

```
G1期
├── Cyclin D-CDK4/6
│   ├── phosphorylates → Rb
│   │   └── releases → E2F
│   │       ├── activates → Cyclin E
│   │       ├── activates → DNA复制酶基因
│   │       └── 进入S期
│   └── inhibited-by → p16
│
├── p16 (CDK抑制剂)
│   └── inhibits → CDK4/6
│       └── 细胞周期阻滞
│
└── p53-p21通路
    ├── DNA损伤 → activates → p53
    │   └── activates → p21
    │       └── inhibits → CDK2/Cyclin E
    │           └── G1期阻滞
    └── MDM2负反馈
        └── inhibits → p53

S期
├── Cyclin E-CDK2
│   └── 启动DNA复制
│
├── Cyclin A-CDK2
│   └── 推进DNA复制
│
└── 检查点
    ├── ATR-Chk1
    │   └── 复制应激响应
    └── 复制完成 → 进入G2

G2/M转换
├── Cyclin B-CDK1 (MPF)
│   ├── inhibited-by → Wee1/Myt1
│   └── activated-by → Cdc25
│       └── 进入M期
│
└── DNA损伤检查点
    └── ATM-Chk2/p53
        └── G2期阻滞
```

**发现方法**：
1. **数据库导入**：TRANSFAC、JASPAR、ChIP-Atlas、ENCODE
2. **文献挖掘**："X激活Y的转录"、"X抑制Y表达"
3. **实验数据**：ChIP-seq峰、RNA-seq差异表达、报告基因实验
4. **LLM推理**：从调控机制描述中提取关系

---

### 1.2 信号通路 (signaling-pathway)

**定义**：表示信号分子通过级联反应传递信号，最终导致细胞响应的关系网络。

**Schema**：
```
(上游分子, signals-to/activates/inhibits/phosphorylates, 下游分子, [pathway, mechanism, kinetics])
```

**方向**：上游 → 下游（单向，但可能有反馈）

**属性**：
- `pathway`: 所属信号通路名称
- `mechanism`: 信号传递机制（磷酸化/去磷酸化/蛋白切割/第二信使）
- `kinetics`: 动力学特征（快速/慢速/持续/瞬时）
- `amplification`: 信号放大程度
- `crosstalk`: 与其他通路的交互

**示例**：

| 上游分子 | 关系 | 下游分子 | 通路 | 机制 |
|----------|------|----------|------|------|
| 配体 | binds-to | 受体 | 多种 | 配体-受体结合 |
| 受体 | activates | 激酶 | RTK通路 | 自磷酸化 |
| Ras | activates | Raf | MAPK通路 | GTP结合 |
| Raf | phosphorylates | MEK | MAPK通路 | 丝氨酸磷酸化 |
| MEK | phosphorylates | ERK | MAPK通路 | 苏氨酸/酪氨酸磷酸化 |
| ERK | phosphorylates | 转录因子 | MAPK通路 | 核转位 |
| PI3K | produces | PIP3 | PI3K-AKT通路 | 磷酸化 |
| PIP3 | recruits | AKT | PI3K-AKT通路 | 膜定位 |
| PDK1 | phosphorylates | AKT | PI3K-AKT通路 | 激活磷酸化 |
| AKT | phosphorylates | mTOR | PI3K-AKT通路 | 激活 |
| cAMP | activates | PKA | GPCR通路 | 变构激活 |
| IP3 | releases | Ca²⁺ | GPCR通路 | 内质网释放 |
| TGF-β | binds-to | TGF-βR | TGF-β通路 | 受体二聚化 |
| Smad2/3 | phosphorylates | Smad4 | TGF-β通路 | 复合物形成 |
| Wnt | binds-to | Frizzled | Wnt通路 | 受体激活 |
| β-catenin | accumulates | 核内 | Wnt通路 | 降解抑制 |

**MAPK信号通路详解**：

```
生长因子（EGF/PDGF等）
  ↓ binds-to
受体酪氨酸激酶（EGFR/PDGFR）
  ↓ 自磷酸化 + 二聚化
招募适配蛋白（Grb2/SOS）
  ↓
Ras-GDP → Ras-GTP（激活）
  ↓
Raf（MAPKKK）激活
  ↓ 磷酸化
MEK1/2（MAPKK）激活
  ↓ 双磷酸化
ERK1/2（MAPK）激活
  ↓ 核转位
  ├── phosphorylates → Elk-1
  │   └── activates → c-fos
  ├── phosphorylates → c-Myc
  │   └── 细胞周期推进
  ├── phosphorylates → STAT
  │   └── 转录调控
  └── phosphorylates → 其他底物
      └── 细胞增殖/分化/存活

负调控：
- PP2A/PP5: 去磷酸化ERK
- DUSP/MKP: 去磷酸化ERK
- Sprouty: 抑制Raf激活
- RKIP: 抑制Raf-MEK结合
```

**PI3K-AKT信号通路详解**：

```
生长因子/胰岛素
  ↓
受体酪氨酸激酶
  ↓
PI3K激活
  ↓ 催化
PIP2 → PIP3
  ↓ 招募
PDK1 + AKT → 细胞膜
  ↓
PDK1磷酸化AKT-T308
  ↓
mTORC2磷酸化AKT-S473
  ↓
AKT完全激活
  ↓
  ├── inhibits → TSC1/2
  │   └── 释放Rheb
  │       └── activates → mTORC1
  │           ├── phosphorylates → S6K
  │           │   └── 蛋白质合成↑
  │           ├── phosphorylates → 4E-BP1
  │           │   └── 翻译启动↑
  │           └── 细胞生长/增殖
  │
  ├── inhibits → GSK3β
  │   └── 糖原合成↑ / 细胞周期↑
  │
  ├── inhibits → Bad
  │   └── 细胞凋亡↓
  │
  ├── inhibits → Caspase-9
  │   └── 细胞凋亡↓
  │
  ├── activates → NF-κB
  │   └── 细胞存活/炎症
  │
  ├── inhibits → p21/p27
  │   └── 细胞周期推进
  │
  └── 其他底物...

负调控：
- PTEN: 去磷酸化PIP3 → PIP2
- SHIP: 去磷酸化PIP3
- PHLPP: 去磷酸化AKT-S473
- PP2A: 去磷酸化AKT-T308
```

**信号通路交叉对话（Crosstalk）**：

```
MAPK通路 ←───交互───→ PI3K-AKT通路
    │                    │
    ├── ERK磷酸化TSC1/2 ──┤
    │   （抑制mTORC1）    │
    │                    │
    ├── AKT磷酸化Raf ─────┤
    │   （抑制MAPK）      │
    │                    │
    └── 共同靶点：        │
        ├── p90RSK       │
        ├── GSK3β        │
        └── mTOR         │

Wnt通路 ←───交互───→ TGF-β通路
    │                    │
    ├── Smad与β-catenin复合物形成
    │                    │
    └── 共同调控细胞分化

炎症信号（NF-κB）←───交互───→ 凋亡信号
    │                    │
    ├── NF-κB激活抗凋亡基因
    │   （Bcl-2, c-IAP等）
    │                    │
    └── TNF-α同时激活两者
```

**发现方法**：
1. **数据库导入**：KEGG、Reactome、PhosphoSitePlus、Signor
2. **文献挖掘**："X磷酸化Y"、"X激活Y"、"X通路调控Y"
3. **磷酸化蛋白质组学**：质谱鉴定磷酸化位点和激酶-底物关系
4. **LLM推理**：从信号转导描述中提取级联关系

---

### 1.3 代谢网络 (metabolic-network)

**定义**：表示代谢物之间的转化关系，包括底物-产物关系、酶催化关系等。

**Schema**：
```
(底物, converted-to, 产物, [enzyme, reaction-type, compartment])
(酶, catalyzes, 反应, [substrates, products, kinetics])
```

**方向**：底物 → 产物（单向或双向）

**属性**：
- `enzyme`: 催化酶
- `reaction-type`: 反应类型（氧化/还原/水解/磷酸化/脱羧等）
- `compartment`: 亚细胞定位（胞质/线粒体/内质网等）
- `reversibility`: 可逆性（可逆/不可逆）
- `energy-change`: 能量变化（ATP/GTP/NADH等）
- `regulation`: 调控信息（激活/抑制）

**示例**：

| 底物 | 关系 | 产物 | 酶 | 反应类型 | 能量变化 |
|------|------|------|-----|----------|----------|
| 葡萄糖 | converted-to | 葡萄糖-6-磷酸 | 己糖激酶 | 磷酸化 | -1 ATP |
| 葡萄糖-6-磷酸 | converted-to | 果糖-6-磷酸 | 磷酸葡萄糖异构酶 | 异构化 | 0 |
| 果糖-6-磷酸 | converted-to | 果糖-1,6-二磷酸 | 磷酸果糖激酶-1 | 磷酸化 | -1 ATP |
| 丙酮酸 | converted-to | 乙酰CoA | 丙酮酸脱氢酶 | 氧化脱羧 | +1 NADH |
| 乙酰CoA | converted-to | 柠檬酸 | 柠檬酸合酶 | 缩合 | 0 |
| 异柠檬酸 | converted-to | α-酮戊二酸 | 异柠檬酸脱氢酶 | 氧化脱羧 | +1 NADH |
| α-酮戊二酸 | converted-to | 琥珀酰CoA | α-酮戊二酸脱氢酶 | 氧化脱羧 | +1 NADH |
| 琥珀酰CoA | converted-to | 琥珀酸 | 琥珀酰CoA合成酶 | 底物水平磷酸化 | +1 GTP |

**糖酵解通路详解**：

```
葡萄糖
  ↓ 己糖激酶（HK）
葡萄糖-6-磷酸（G6P）
  │   ← 被己糖磷酸异构酶催化 ← 果糖-6-磷酸（F6P）
  │     （糖异生方向）
  ↓ 磷酸葡萄糖异构酶（PGI）
果糖-6-磷酸（F6P）
  ↓ 磷酸果糖激酶-1（PFK-1）
  │   【关键限速酶，被ATP/柠檬酸抑制，被AMP/F-2,6-BP激活】
果糖-1,6-二磷酸（F1,6BP）
  ↓ 醛缩酶（ALD）
甘油醛-3-磷酸（G3P） + 二羟丙酮磷酸（DHAP）
  │   ← DHAP被丙糖磷酸异构酶（TPI）转化为G3P
  ↓
2 × 甘油醛-3-磷酸（G3P）
  ↓ 甘油醛-3-磷酸脱氢酶（GAPDH）
  │   【+ NAD⁺ + Pi → + NADH】
1,3-二磷酸甘油酸（1,3-BPG）
  ↓ 磷酸甘油酸激酶（PGK）
  │   【ADP → ATP（底物水平磷酸化）】
3-磷酸甘油酸（3-PG）
  ↓ 磷酸甘油酸变位酶（PGAM）
2-磷酸甘油酸（2-PG）
  ↓ 烯醇化酶（ENO）
磷酸烯醇式丙酮酸（PEP）
  ↓ 丙酮酸激酶（PK）
  │   【关键限速酶，ADP → ATP】
丙酮酸
  │
  ├── [有氧] → 进入线粒体 → 丙酮酸脱氢酶 → 乙酰CoA → TCA循环
  │
  └── [无氧] → 乳酸脱氢酶（LDH）
        【+ NADH → NAD⁺，再生NAD⁺维持糖酵解】
        乳酸

总反应：
葡萄糖 + 2 NAD⁺ + 2 ADP + 2 Pi → 2 丙酮酸 + 2 NADH + 2 ATP + 2 H⁺
```

**TCA循环（三羧酸循环）详解**：

```
乙酰CoA（2C） + 草酰乙酸（4C）
  ↓ 柠檬酸合酶（CS）
柠檬酸（6C）
  ↓ 顺乌头酸酶（ACO）
异柠檬酸（6C）
  ↓ 异柠檬酸脱氢酶（IDH）
  │   【+ NAD⁺ → NADH + CO₂】
α-酮戊二酸（5C）
  ↓ α-酮戊二酸脱氢酶复合体（α-KGDH）
  │   【+ NAD⁺ → NADH + CO₂】
  │   【类似丙酮酸脱氢酶复合体】
琥珀酰CoA（4C）
  ↓ 琥珀酰CoA合成酶（SCS）
  │   【GDP + Pi → GTP（底物水平磷酸化）】
琥珀酸（4C）
  ↓ 琥珀酸脱氢酶（SDH）
  │   【+ FAD → FADH₂】
  │   【位于线粒体内膜，电子传递链复合体II】
延胡索酸（4C）
  ↓ 延胡索酸酶（FH）
苹果酸（4C）
  ↓ 苹果酸脱氢酶（MDH）
  │   【+ NAD⁺ → NADH】
草酰乙酸（4C）
  ↓ 与下一个乙酰CoA结合，循环继续

每轮TCA循环产物（1乙酰CoA）：
- 3 NADH
- 1 FADH₂
- 1 GTP（相当于ATP）
- 2 CO₂

总能量产出（1葡萄糖 → 2乙酰CoA → 2轮TCA）：
- 6 NADH
- 2 FADH₂
- 2 GTP
```

**氧化磷酸化与电子传递链**：

```
NADH（来自糖酵解/TCA/脂肪酸氧化）
  ↓ 复合体I（NADH脱氢酶）
  │   【4H⁺泵出线粒体基质】
泛醌（CoQ）
  ← 复合体II（琥珀酸脱氢酶，来自FADH₂）
  ↓
复合体III（细胞色素bc1复合体）
  │   【4H⁺泵出】
细胞色素c（Cyt c）
  ↓
复合体IV（细胞色素c氧化酶）
  │   【2H⁺泵出】
  │   【½ O₂ + 2H⁺ → H₂O】
O₂

质子梯度（线粒体内膜间隙 → 基质）
  ↓
ATP合酶（复合体V）
  │   【质子回流驱动旋转】
  │   【ADP + Pi → ATP】
ATP

化学计量：
- 1 NADH → ~2.5 ATP
- 1 FADH₂ → ~1.5 ATP
```

**代谢通路交叉与调控**：

```
                    葡萄糖
                      │
                      ↓ 糖酵解
                    丙酮酸
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    乳酸（无氧）  乙酰CoA    丙氨酸（转氨）
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    TCA循环      脂肪酸合成    胆固醇合成
        │             │             │
        ↓             ↓             ↓
    能量（ATP）   脂肪储存     膜合成/激素
        │
        ↓
    氨基酸合成（α-酮戊二酸、草酰乙酸等）

关键调控点：
1. 己糖激酶（被G6P反馈抑制）
2. 磷酸果糖激酶-1（限速酶）
   - 抑制：ATP、柠檬酸
   - 激活：AMP、F-2,6-BP
3. 丙酮酸激酶
   - 抑制：ATP、丙氨酸
   - 激活：F-1,6-BP
4. 丙酮酸脱氢酶复合体
   - 抑制：乙酰CoA、NADH、ATP
5. 柠檬酸合酶
   - 抑制：ATP、琥珀酰CoA、NADH
6. 异柠檬酸脱氢酶
   - 抑制：ATP、NADH
   - 激活：ADP、Ca²⁺
7. α-酮戊二酸脱氢酶
   - 抑制：琥珀酰CoA、NADH
```

**发现方法**：
1. **数据库导入**：KEGG、MetaCyc、Reactome、HMDB
2. **文献挖掘**："X转化为Y"、"X酶催化Y反应"
3. **代谢组学**：质谱检测代谢物水平变化
4. **LLM推理**：从代谢通路描述中提取转化关系

---

## 二、调控网络整合

### 2.1 多层次调控整合

```
表观遗传调控
    ↓
染色质重塑 → DNA可及性改变
    ↓
转录调控（TF → 靶基因）
    ↓
RNA加工（剪切/编辑/转运）
    ↓
转录后调控（miRNA/lncRNA）
    ↓
翻译调控
    ↓
翻译后修饰（磷酸化/泛素化/乙酰化等）
    ↓
蛋白质活性/定位/稳定性
    ↓
代谢酶活性
    ↓
代谢流/能量产生
    ↓
细胞表型/功能

示例：胰岛素信号整合
胰岛素
  ↓
受体酪氨酸激酶激活
  ↓
  ├── PI3K-AKT通路
  │   ├── 葡萄糖转运（GLUT4转位）
  │   ├── 糖原合成（GSK3β抑制）
  │   ├── 蛋白质合成（mTOR激活）
  │   └── 基因表达（FOXO磷酸化）
  │
  └── MAPK通路
      ├── 细胞增殖
      └── 基因表达
```

### 2.2 网络拓扑分析

```python
def analyze_regulatory_network(relations):
    """分析调控网络拓扑特征"""
    
    # 1. 构建网络图
    G = build_network_graph(relations)
    
    # 2. 计算中心性指标
    centrality = {
        "degree": nx.degree_centrality(G),
        "betweenness": nx.betweenness_centrality(G),
        "pagerank": nx.pagerank(G)
    }
    
    # 3. 识别关键节点（枢纽基因/蛋白）
    hub_nodes = identify_hubs(G, threshold=0.9)
    
    # 4. 发现调控模块
    modules = community_detection(G)
    
    # 5. 识别反馈回路
    feedback_loops = find_cycles(G)
    
    # 6. 通路富集分析
    pathway_enrichment = enrich_pathways(modules)
    
    return {
        "centrality": centrality,
        "hubs": hub_nodes,
        "modules": modules,
        "feedback_loops": feedback_loops,
        "pathway_enrichment": pathway_enrichment
    }
```

---

## 三、关系发现方法

### 3.1 规则匹配模式

```python
REGULATION_RELATION_PATTERNS = {
    # 转录调控
    "transcriptional_regulation": [
        r"({tf})激活({gene})的转录",
        r"({tf})抑制({gene})的表达",
        r"({tf})调控({gene})",
        r"({tf})结合到({gene})的启动子",
    ],
    
    # 信号传递
    "signal_transduction": [
        r"({protein})磷酸化({protein})",
        r"({protein})激活({protein})",
        r"({protein})抑制({protein})",
        r"({protein})通过({pathway})信号通路",
    ],
    
    # 代谢转化
    "metabolic_conversion": [
        r"({substrate})转化为({product})",
        r"({enzyme})催化({substrate})生成({product})",
        r"({substrate})在({enzyme})作用下生成({product})",
    ],
}
```

### 3.2 LLM推理提示词

```markdown
## 任务
分析以下分子间的调控关系。

## 分子信息
分子A: {molecule_a} (类型: {type_a})
分子B: {molecule_b} (类型: {type_b})

## 上下文描述
{context}

## 关系类型选项
1. **transcriptional_activation**: A转录激活B（A是TF，B是靶基因）
2. **transcriptional_repression**: A转录抑制B
3. **phosphorylates**: A磷酸化B（激酶-底物）
4. **dephosphorylates**: A去磷酸化B（磷酸酶-底物）
5. **activates**: A激活B的活性
6. **inhibits**: A抑制B的活性
7. **binds-to**: A与B结合
8. **converts-to**: A转化为B（代谢反应）
9. **catalyzes**: A催化B的转化（A是酶）
10. **none**: 无明确关系

## 输出格式
```json
{
  "relation_type": "关系类型",
  "direction": "A→B / B→A / 无向",
  "mechanism": "具体机制",
  "pathway": "所属通路（如有）",
  "confidence": 0.0-1.0,
  "evidence": "证据来源",
  "context": "适用条件"
}
```
```

---

## 四、数据格式

### 4.1 调控关系JSON

```json
{
  "relation_id": "reg_001",
  "relation_type": "transcriptional_activation",
  "subject": {
    "id": "ent_p53",
    "name": "p53",
    "type": "protein",
    "category": "transcription_factor",
    "function": "tumor_suppressor"
  },
  "object": {
    "id": "ent_p21",
    "name": "p21",
    "type": "gene",
    "category": "CDK_inhibitor"
  },
  "properties": {
    "confidence": 0.98,
    "mechanism": "direct_binding",
    "binding_site": "p53_response_element",
    "context": {
      "cell_type": "fibroblast",
      "condition": "DNA_damage",
      "stimulus": "UV_irradiation"
    },
    "evidence": [
      "ChIP-seq",
      "luciferase_reporter",
      "RNA-seq"
    ],
    "references": ["PMID:12345678"]
  },
  "source": {
    "method": "database_import",
    "database": "TRRUST",
    "version": "v2"
  }
}
```

### 4.2 信号通路JSON

```json
{
  "pathway_id": "path_001",
  "name": "MAPK_signaling",
  "category": "signal_transduction",
  "description": "丝裂原活化蛋白激酶信号通路",
  "nodes": [
    {"id": "Ras", "type": "small_GTPase"},
    {"id": "Raf", "type": "kinase"},
    {"id": "MEK", "type": "kinase"},
    {"id": "ERK", "type": "kinase"}
  ],
  "edges": [
    {"source": "Ras", "target": "Raf", "type": "activates"},
    {"source": "Raf", "target": "MEK", "type": "phosphorylates"},
    {"source": "MEK", "target": "ERK", "type": "phosphorylates"}
  ],
  "crosstalk": [
    {"pathway": "PI3K-AKT", "interaction": "inhibition", "node": "Raf"}
  ]
}
```

### 4.3 代谢反应JSON

```json
{
  "reaction_id": "rxn_001",
  "name": "hexokinase_reaction",
  "enzyme": {
    "id": "ent_HK",
    "name": "hexokinase",
    "ec_number": "2.7.1.1"
  },
  "substrates": [
    {"id": "ent_glucose", "name": "glucose", "stoichiometry": 1},
    {"id": "ent_ATP", "name": "ATP", "stoichiometry": 1}
  ],
  "products": [
    {"id": "ent_G6P", "name": "glucose-6-phosphate", "stoichiometry": 1},
    {"id": "ent_ADP", "name": "ADP", "stoichiometry": 1}
  ],
  "properties": {
    "reversibility": false,
    "compartment": "cytoplasm",
    "regulation": {
      "inhibitors": ["glucose-6-phosphate"],
      "activators": ["insulin"]
    }
  }
}
```
