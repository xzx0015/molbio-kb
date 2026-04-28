# SKILL_04: 关系构建 — 分子生物学知识图谱的关系发现体系

> 设计一套适合分子生物学课程知识库的关系类型体系和发现方法，将孤立的概念、实验流程和调控网络连接成结构化知识图谱。

---

## 一、关系类型体系总览

### 1.1 三大关系类别

分子生物学知识图谱包含三类核心关系：

| 类别 | 文档 | 核心内容 | 适用场景 |
|------|------|----------|----------|
| **概念关系** | SKILL_04a | 概念间的语义关联（上下位、因果、组成、调控） | 理论知识体系构建 |
| **实验流程** | SKILL_04b | 实验技术的关系网络（步骤序列、技术替代、技术组合） | 实验技能学习路径 |
| **调控网络** | SKILL_04c | 分子调控关系（转录调控、信号通路、代谢网络） | 机制理解与应用 |

### 1.2 关系Schema统一格式

所有关系采用统一的三元组格式：

```
(主体: Entity, 关系: RelationType, 客体: Entity, [属性: Properties])
```

**属性字段**（可选）：
- `confidence`: 置信度 (0.0-1.0)
- `evidence`: 证据来源（教材章节/文献/实验数据）
- `context`: 上下文信息（细胞类型/组织/条件）
- `direction`: 方向性（正向/负向/双向）
- `strength`: 强度（强/中/弱）

---

## 二、关系发现方法论

### 2.1 混合发现策略

采用**规则匹配 + LLM推理**的混合方法：

```
┌─────────────────────────────────────────────────────────────┐
│                    关系发现流程                              │
├─────────────────────────────────────────────────────────────┤
│  阶段1: 规则匹配（高置信度、可解释）                          │
│    ├── 模式匹配：正则/句法规则提取显式关系                    │
│    ├── 本体推理：基于上下位关系推导隐含关系                   │
│    └── 数据库映射：利用已知数据库（GO/KEGG/Reactome）         │
│                                                             │
│  阶段2: LLM推理（覆盖复杂语义）                               │
│    ├── 语义理解：从文本描述中推断关系                         │
│    ├── 上下文推理：结合实验条件判断调控方向                   │
│    └── 跨文档关联：连接分散在不同章节的知识                   │
│                                                             │
│  阶段3: 人工校验（质量保证）                                  │
│    ├── 专家审核：生物学专家验证关键关系                       │
│    ├── 一致性检查：检测矛盾关系                               │
│    └── 置信度校准：调整自动发现的置信度                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 规则匹配方法

#### 2.2.1 显式关系模式

从教材文本中直接匹配关键词：

```python
# 上下位关系模式
HYPONYM_PATTERNS = [
    r"({concept})是({concept})的一种",
    r"({concept})属于({concept})",
    r"({concept})包括({concept})",
    r"({concept})可分为({concept})",
]

# 组成关系模式
COMPOSITION_PATTERNS = [
    r"({concept})由({concept})和({concept})组成",
    r"({concept})包含({concept})",
    r"({concept})的组分包括({concept})",
]

# 因果关系模式
CAUSAL_PATTERNS = [
    r"({concept})导致({concept})",
    r"({concept})引起({concept})",
    r"({concept})造成({concept})",
    r"由于({concept})，({concept})",
]

# 调控关系模式
REGULATION_PATTERNS = [
    r"({concept})激活({concept})",
    r"({concept})抑制({concept})",
    r"({concept})促进({concept})",
    r"({concept})下调({concept})",
    r"({concept})上调({concept})",
]
```

#### 2.2.2 本体推理规则

基于已有关系推导新关系：

```
# 传递性推理
IF (A is-a B) AND (B is-a C) THEN (A is-a C)

# 组成推理
IF (X part-of Y) AND (Y part-of Z) THEN (X part-of Z)

# 调控推理
IF (A activates B) AND (B activates C) THEN (A indirectly-activates C)
IF (A inhibits B) AND (B activates C) THEN (A indirectly-inhibits C)
```

### 2.3 LLM推理方法

#### 2.3.1 关系分类提示词

```markdown
分析以下分子生物学概念之间的关系：

概念A: {entity_a}
概念B: {entity_b}
上下文: {context}

请判断它们之间是否存在以下关系类型：
1. is-a (上下位): A是B的一种/类型
2. part-of (组成): A是B的组成部分
3. causes (因果): A导致B发生
4. regulates (调控): A调控B的活性/表达
5. precedes (时序): A在B之前发生
6. associates-with (关联): A与B相关但无明确因果

输出格式：
{
  "relation_type": "关系类型",
  "direction": "正向/负向/双向/无向",
  "confidence": 0.0-1.0,
  "reasoning": "推理理由（50字以内）",
  "evidence": "证据文本片段"
}

如果无明确关系，输出 {"relation_type": "none"}
```

#### 2.3.2 实验流程关系提示词

```markdown
分析以下实验步骤之间的关系：

步骤A: {step_a}
步骤B: {step_b}
所属实验: {experiment}

请判断关系类型：
1. sequence (序列): A是B的前置步骤
2. alternative (替代): A和B是替代方案
3. combination (组合): A和B组合使用
4. prerequisite (前提): A是B的必要条件
5. output-of (产出): A的产物是B的输入

输出格式同上。
```

#### 2.3.3 调控网络关系提示词

```markdown
分析以下分子间的调控关系：

分子A: {molecule_a} (类型: {type_a})
分子B: {molecule_b} (类型: {type_b})
生物过程: {process}

请判断：
1. A是否调控B的表达/活性？
2. 调控方向是激活还是抑制？
3. 是直接调控还是间接调控？
4. 调控机制是什么（转录/翻译/修饰/降解）？

输出格式：
{
  "relation_type": "activates/inhibits/regulates/none",
  "mechanism": "mechanism_type",
  "direct": true/false,
  "confidence": 0.0-1.0,
  "evidence": "支持证据"
}
```

---

## 三、数据来源与整合

### 3.1 内部数据来源

| 来源 | 内容 | 关系类型 |
|------|------|----------|
| 教材文本 | 概念定义、实验步骤、机制描述 | 全部类型 |
| 课程讲义 | 教学重点、知识脉络 | 概念关系 |
| 实验手册 | 操作流程、注意事项 | 实验流程 |
| 习题库 | 知识点关联 | 概念关系 |

### 3.2 外部数据库

| 数据库 | 用途 | 关系类型 |
|--------|------|----------|
| **Gene Ontology (GO)** | 功能注释、层级关系 | is-a, part-of |
| **KEGG** | 通路关系、代谢网络 | pathway, reaction |
| **Reactome** | 信号通路、分子互作 | regulates, binds-to |
| **BioGRID** | 蛋白-蛋白相互作用 | interacts-with |
| **ChEMBL** | 化合物-靶点关系 | inhibits, activates |
| **TRANSFAC/JASPAR** | 转录因子-靶基因 | regulates |
| **UniProt** | 蛋白功能、修饰 | has-function, modified-by |

### 3.3 数据整合策略

```python
def integrate_external_databases():
    """整合外部数据库关系"""
    
    # 1. 导入GO术语层级
    go_is_a = load_go_ontology()  # is-a关系
    go_part_of = load_go_relationships()  # part-of关系
    
    # 2. 导入KEGG通路
    kegg_pathways = load_kegg_pathways()  # pathway关系
    kegg_reactions = load_kegg_reactions()  # substrate-product关系
    
    # 3. 导入PPI网络
    ppi_network = load_biogrid_data()  # interacts-with关系
    
    # 4. 导入调控网络
    tf_targets = load_jaspar_data()  # TF-target关系
    
    # 5. 映射到本地实体
    mapped_relations = map_to_local_entities(
        go_is_a, go_part_of, kegg_pathways, 
        kegg_reactions, ppi_network, tf_targets
    )
    
    # 6. 冲突检测与解决
    resolved_relations = resolve_conflicts(mapped_relations)
    
    return resolved_relations
```

---

## 四、关系数据格式

### 4.1 JSON Schema

```json
{
  "relation_id": "rel_001",
  "relation_type": "activates",
  "subject": {
    "id": "ent_001",
    "name": "p53",
    "type": "protein",
    "category": "transcription_factor"
  },
  "object": {
    "id": "ent_002", 
    "name": "p21",
    "type": "gene",
    "category": "cell_cycle_regulator"
  },
  "properties": {
    "confidence": 0.95,
    "direction": "positive",
    "mechanism": "transcriptional_activation",
    "evidence": ["文献PMID:12345678", "教材第5章"],
    "context": {
      "cell_type": "fibroblast",
      "condition": "DNA_damage"
    }
  },
  "source": {
    "method": "llm_inference",
    "text": "p53蛋白激活p21基因的转录",
    "chapter": "ch05_cell_cycle"
  },
  "verified": true,
  "created_at": "2026-03-17",
  "updated_at": "2026-03-17"
}
```

### 4.2 CSV导出格式

```csv
relation_id,subject_id,subject_name,subject_type,relation_type,object_id,object_name,object_type,confidence,evidence
rel_001,ent_001,p53,protein,activates,ent_002,p21,gene,0.95,教材第5章
rel_002,ent_003,DNA,concept,has-part,ent_004,gene,concept,1.0,教材第2章
rel_003,ent_005,RT-PCR,technique,alternative-to,ent_006,Northern_Blot,technique,0.85,教材第8章
```

---

## 五、质量控制

### 5.1 一致性检查

```python
def validate_relation_consistency(relations):
    """检查关系一致性"""
    issues = []
    
    # 检查1: 反对称关系
    for rel in relations:
        if rel['relation_type'] == 'is-a':
            # 检查是否存在反向关系
            reverse = find_reverse_relation(relations, rel)
            if reverse and reverse['relation_type'] == 'is-a':
                issues.append(f"循环is-a: {rel['subject']} ↔ {rel['object']}")
    
    # 检查2: 矛盾调控
    for entity in get_all_entities():
        activators = get_activators(entity, relations)
        inhibitors = get_inhibitors(entity, relations)
        common = set(activators) & set(inhibitors)
        if common:
            issues.append(f"矛盾调控: {entity} 被 {common} 同时激活和抑制")
    
    # 检查3: 传递闭包
    for rel in relations:
        if rel['relation_type'] in ['is-a', 'part-of']:
            # 检查传递性是否一致
            transitive_issues = check_transitivity(rel, relations)
            issues.extend(transitive_issues)
    
    return issues
```
