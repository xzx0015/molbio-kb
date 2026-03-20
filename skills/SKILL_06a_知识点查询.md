# SKILL 06a: 知识点智能检索系统

> 基于知识图谱的多维度智能检索系统，支持实体检索、关系检索、概念检索及关联推荐。

---

## 一、系统概述

### 1.1 设计目标

- **多维度检索**：支持按实体、关系、概念分类、关键词等多种方式检索
- **语义理解**：理解用户查询意图，支持自然语言查询
- **关联推荐**：基于知识图谱的关联推荐，发现相关知识
- **可视化展示**：知识图谱局部可视化，直观展示知识关系

### 1.2 核心功能

```
┌─────────────────────────────────────────────────────────────────┐
│                     知识点智能检索系统                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │ 实体检索    │  │ 关系检索    │  │ 概念检索    │  │ 语义检索│ │
│  │             │  │             │  │             │  │        │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 关联推荐    │  │ 前置知识    │  │ 可视化展示  │             │
│  │             │  │ 提示        │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、检索维度

### 2.1 实体检索

**定义**：按具体实体（如酶、分子、结构等）进行精确或模糊匹配

**检索类型**：

| 检索方式 | 示例 | 说明 |
|---------|------|------|
| 精确匹配 | "DNA聚合酶III" | 完全匹配实体名称 |
| 前缀匹配 | "DNA聚" | 匹配以关键词开头的实体 |
| 模糊匹配 | "DNA聚合" | 包含关键词的实体 |
| 同义词匹配 | "DNA pol" | 匹配实体的英文/缩写形式 |

**实现示例**：

```python
# Cypher查询 - 实体精确匹配
MATCH (c:Concept)
WHERE c.name = 'DNA聚合酶III' 
   OR c.name_zh = 'DNA聚合酶III'
RETURN c

# Cypher查询 - 实体模糊匹配
MATCH (c:Concept)
WHERE c.name CONTAINS '聚合酶'
   OR c.name_zh CONTAINS '聚合酶'
RETURN c
ORDER BY c.importance DESC

# 同义词扩展
MATCH (c:Concept)-[:HAS_ALIAS]->(a:Alias)
WHERE a.name IN ['DNA pol', 'DNA polymerase']
RETURN c
```

### 2.2 关系检索

**定义**：按知识之间的关系进行检索，发现概念间的联系

**关系类型**：

| 关系类型 | 说明 | 示例 |
|---------|------|------|
| `requires` | 前置依赖 | 学习A需要先学B |
| `isPartOf` | 组成部分 | A是B的一部分 |
| `hasSubConcept` | 包含子概念 | B包含A |
| `relatedTo` | 相关关系 | A与B相关 |
| `leadsTo` | 导致/产生 | A导致B |

**实现示例**：

```python
# 查询某概念的所有前置知识
MATCH (c:Concept {name: 'DNA复制'})-[:requires]->(pre:Concept)
RETURN pre.name, pre.difficulty

# 查询某概念的所有子概念
MATCH (c:Concept {name: 'DNA复制'})-[:hasSubConcept]->(sub:Concept)
RETURN sub.name, sub.importance
ORDER BY sub.importance DESC

# 查询两个概念之间的关系路径
MATCH path = shortestPath(
    (a:Concept {name: 'DNA聚合酶'})-[:requires|isPartOf|relatedTo*]-(b:Concept {name: '冈崎片段'})
)
RETURN path
```

### 2.3 概念分类检索

**定义**：按概念分类树进行层级检索

**分类维度**：

```
中心法则
├── DNA复制
│   ├── 复制机制
│   ├── 复制酶
│   └── 复制调控
├── 转录
│   ├── 转录机制
│   ├── RNA聚合酶
│   └── 转录调控
└── 翻译
    ├── 翻译机制
    ├── 核糖体
    └── 翻译后修饰
```

**实现示例**：

```python
# 查询某分类下的所有概念
MATCH (c:Concept)-[:isPartOf*]->(parent:Concept {name: 'DNA复制'})
RETURN c.name, c.difficulty

# 按分类层级检索
MATCH (c:Concept)
WHERE c.category IN ['复制酶', '复制机制']
RETURN c.name
ORDER BY c.importance DESC

# 查询某概念的所有上级分类
MATCH (c:Concept {name: 'DNA聚合酶III'})-[:isPartOf*]->(parent:Concept)
RETURN parent.name
```

### 2.4 语义检索

**定义**：基于语义理解的智能检索，支持自然语言查询

**语义理解流程**：

```
用户输入: "DNA复制需要什么酶"
   ↓
[意图识别] → 查询意图: 查询某概念的相关实体（酶）
   ↓
[实体识别] → 主体: DNA复制, 目标类型: 酶
   ↓
[查询构建] → 构建图查询
   ↓
[执行检索] → 返回结果
```

**实现示例**：

```python
# 自然语言查询解析
def parse_nl_query(query: str) -> dict:
    """
    解析自然语言查询
    示例: "DNA复制需要什么酶" 
    返回: {
        "intent": "find_related",
        "subject": "DNA复制",
        "relation_type": "involves",
        "target_type": "酶"
    }
    """
    # 使用NLP模型进行意图识别和实体抽取
    pass

# 语义扩展查询
def semantic_search(query: str, expand: bool = True) -> list:
    # 1. 基础关键词匹配
    base_results = keyword_search(query)
    
    # 2. 语义扩展（同义词、上下位词）
    if expand:
        synonyms = get_synonyms(query)
        hypernyms = get_hypernyms(query)
        expanded_query = OR(query, synonyms, hypernyms)
        base_results.extend(keyword_search(expanded_query))
    
    # 3. 去重排序
    return deduplicate_and_rank(base_results)
```

---

## 三、关联推荐

### 3.1 相关知识点推荐

**推荐策略**：

1. **共现推荐**：在同一学习路径中经常一起出现的知识点
2. **依赖推荐**：当前知识点的前置/后续知识
3. **相似推荐**：概念相似度高的知识点
4. **应用推荐**：当前知识点的应用场景

**实现示例**：

```python
# 相关知识点推荐算法
def recommend_related(concept_id: str, limit: int = 5) -> list:
    """
    基于知识图谱的相关知识点推荐
    """
    recommendations = []
    
    # 1. 直接关联（前置/后续知识）
    cypher_direct = """
    MATCH (c:Concept {id: $concept_id})-[:requires|isPrerequisiteFor]->(related:Concept)
    RETURN related, 'dependency' as reason
    LIMIT $limit
    """
    recommendations.extend(run_query(cypher_direct))
    
    # 2. 共同前置知识（相似知识点）
    cypher_similar = """
    MATCH (c:Concept {id: $concept_id})-[:requires]->(common:Concept)<-[:requires]-(similar:Concept)
    WHERE similar <> c
    RETURN similar, 'similar' as reason, count(common) as common_count
    ORDER BY common_count DESC
    LIMIT $limit
    """
    recommendations.extend(run_query(cypher_similar))
    
    # 3. 同分类其他知识点
    cypher_category = """
    MATCH (c:Concept {id: $concept_id})-[:isPartOf]->(parent:Concept)<-[:isPartOf]-(sibling:Concept)
    WHERE sibling <> c
    RETURN sibling, 'sibling' as reason
    LIMIT $limit
    """
    recommendations.extend(run_query(cypher_category))
    
    return deduplicate(recommendations)
```

### 3.2 前置知识提示

**功能说明**：在学习某知识点前，提示需要掌握的前置知识

**交互设计**：

```
┌─────────────────────────────────────────────────────────────┐
│  正在学习: DNA复制                                          │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ 前置知识检查                                            │
│  学习此知识点前，建议先掌握以下内容：                        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ DNA结构     │  │ 碱基配对    │  │ 酶的基本概念│         │
│  │ [已掌握 ✓]  │  │ [未掌握 ⚠]  │  │ [已掌握 ✓]  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  [跳过并继续]  [先学习前置知识]                             │
└─────────────────────────────────────────────────────────────┘
```

**实现示例**：

```python
def check_prerequisites(concept_id: str, user_id: str) -> dict:
    """
    检查用户是否已掌握某知识点的前置知识
    """
    # 1. 查询所有前置知识
    cypher = """
    MATCH (c:Concept {id: $concept_id})-[:requires]->(prereq:Concept)
    RETURN prereq.id as prereq_id, prereq.name as prereq_name
    """
    prerequisites = run_query(cypher, concept_id=concept_id)
    
    # 2. 查询用户掌握度
    result = {"missing": [], "mastered": []}
    for prereq in prerequisites:
        mastery = get_user_mastery(user_id, prereq["prereq_id"])
        if mastery >= 0.7:
            result["mastered"].append(prereq)
        else:
            result["missing"].append(prereq)
    
    return result
```

---

## 四、可视化展示

### 4.1 知识图谱局部可视化

**展示内容**：

1. **中心节点**：当前查询的知识点
2. **直接关联**：前置知识、后续知识、子概念、父概念
3. **间接关联**：二级关联的知识点（可选）

**可视化设计**：

```
                    ┌─────────────┐
                    │   中心法则   │
                    │   (父概念)   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
         │ DNA结构 │  │ DNA复制 │  │ 复制起点│
         │(前置知识)│  │【当前】 │  │(子概念) │
         └─────────┘  └────┬────┘  └─────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
         │DNA聚合酶│  │冈崎片段 │  │ 引物酶  │
         │(相关酶) │  │(相关机制)│  │(相关酶) │
         └─────────┘  └─────────┘  └─────────┘
```

**颜色与样式规范**：

| 节点类型 | 颜色 | 形状 | 说明 |
|---------|------|------|------|
| 当前节点 | #FF6B6B | 圆形 | 红色高亮 |
| 前置知识 | #4ECDC4 | 圆形 | 青色，虚线边 |
| 后续知识 | #95E1D3 | 圆形 | 浅绿，虚线边 |
| 父概念 | #F7DC6F | 方形 | 黄色 |
| 子概念 | #BB8FCE | 方形 | 紫色 |
| 相关概念 | #85C1E2 | 圆形 | 蓝色 |

**实现技术**：

```javascript
// D3.js 知识图谱可视化
function renderKnowledgeGraph(container, data) {
    const width = 800;
    const height = 600;
    
    const svg = d3.select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height);
    
    // 定义力导向模拟
    const simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));
    
    // 绘制连线
    const link = svg.append("g")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("stroke", d => getLinkColor(d.type))
        .attr("stroke-width", 2)
        .attr("stroke-dasharray", d => d.type === 'requires' ? "5,5" : null);
    
    // 绘制节点
    const node = svg.append("g")
        .selectAll("g")
        .data(data.nodes)
        .enter().append("g")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    
    // 节点形状和颜色
    node.append(d => d.type === 'current' ? 'circle' : 
                 d.category === 'parent' ? 'rect' : 'circle')
        .attr("r", d => d.type === 'current' ? 30 : 20)
        .attr("fill", d => getNodeColor(d.type, d.category))
        .attr("stroke", "#fff")
        .attr("stroke-width", 2);
    
    // 节点标签
    node.append("text")
        .text(d => d.name)
        .attr("text-anchor", "middle")
        .attr("dy", 5)
        .attr("font-size", "12px")
        .attr("fill", "#333");
    
    // 更新位置
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);
        
        node.attr("transform", d => `translate(${d.x},${d.y})`);
    });
}
```

### 4.2 知识卡片设计

**卡片内容**：

```
┌─────────────────────────────────────────────────────────────┐
│  DNA复制                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  📚 分类: 中心法则 > DNA复制                                 │
│  📊 难度: ⭐⭐⭐ (进阶)                                       │
│  ⏱️ 建议时长: 45分钟                                         │
│  🔥 重要程度: 核心知识点                                     │
├─────────────────────────────────────────────────────────────┤
│  📖 定义                                                    │
│  DNA复制是指DNA双链在细胞分裂前进行精确拷贝的过程，         │
│  确保遗传信息准确传递给子代细胞。                           │
├─────────────────────────────────────────────────────────────┤
│  🔑 关键概念                                                │
│  • 半保留复制机制                                          │
│  • 复制叉与前导链/后随链                                    │
│  • DNA聚合酶的作用                                         │
│  • 冈崎片段与DNA连接酶                                      │
├─────────────────────────────────────────────────────────────┤
│  📎 相关知识点                                              │
│  [DNA聚合酶] [冈崎片段] [复制起点] [细胞周期]               │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ 前置知识                                                │
│  ✓ DNA结构  ✓ 碱基配对  ⚠ 酶的基本概念                     │
├─────────────────────────────────────────────────────────────┤
│  [开始学习]  [查看图谱]  [练习题目]                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、用户交互流程

### 5.1 检索流程

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ 用户输入 │ ──→ │ 查询解析 │ ──→ │ 执行检索 │ ──→ │ 结果展示 │
│ 查询词   │     │         │     │         │     │         │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                      │               │
                      ↓               ↓
                ┌─────────┐     ┌─────────┐
                │意图识别 │     │多源检索 │
                │实体抽取 │     │结果融合 │
                └─────────┘     └─────────┘
```

### 5.2 交互界面设计

**搜索页面**：

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 分子生物学知识检索                        [用户头像]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌─────────────────────────────────────────────────┐    │
│     │ 搜索知识点、概念、酶、分子...                    │ 🔍 │
│     └─────────────────────────────────────────────────┘    │
│                                                             │
│     热门搜索: [DNA复制] [转录] [翻译] [PCR] [CRISPR]       │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 筛选条件:                                              ││
│  │ [全部 ▼] [难度: 全部 ▼] [分类: 全部 ▼] [重要程度 ▼]    ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  搜索结果 (共 12 条):                                       │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 1. DNA复制                                             ││
│  │    分类: 中心法则 > DNA复制  |  难度: ⭐⭐⭐           ││
│  │    DNA分子自我复制的过程，包括半保留复制机制...        ││
│  │    [查看详情] [加入学习路径]                           ││
│  └────────────────────────────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────┐│
│  │ 2. DNA聚合酶                                           ││
│  │    ...                                                 ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 六、API接口设计

### 6.1 检索接口

```yaml
# 全文检索
GET /api/search
参数:
  q: 查询词 (必填)
  type: 检索类型 (entity|concept|relation|all, 默认all)
  difficulty: 难度过滤 (basic|intermediate|advanced)
  category: 分类过滤
  importance: 重要程度过滤 (core|important|supplementary)
  limit: 返回数量 (默认10)
  offset: 偏移量 (默认0)
返回:
  total: 总结果数
  results: 结果列表
    - id: 知识点ID
      name: 名称
      category: 分类
      difficulty: 难度
      importance: 重要程度
      snippet: 内容摘要
      match_score: 匹配分数

# 实体详情
GET /api/concepts/{id}
返回:
  id: 知识点ID
  name: 名称
  name_en: 英文名称
  category: 分类路径
  definition: 定义
  difficulty: 难度
  importance: 重要程度
  study_time: 建议学习时长
  prerequisites: 前置知识列表
  sub_concepts: 子概念列表
  related_concepts: 相关概念列表
  questions: 关联题目数量

# 关系查询
GET /api/concepts/{id}/relations
参数:
  relation_type: 关系类型 (requires|isPartOf|relatedTo|all)
  depth: 查询深度 (1-3, 默认1)
返回:
  nodes: 节点列表
  edges: 关系列表
```

### 6.2 推荐接口

```yaml
# 相关推荐
GET /api/concepts/{id}/recommendations
参数:
  type: 推荐类型 (related|prerequisite|similar|all)
  limit: 数量 (默认5)
返回:
  recommendations:
    - concept: 推荐知识点
      reason: 推荐理由
      score: 推荐分数

# 前置知识检查
GET /api/concepts/{id}/prerequisites/check
参数:
  user_id: 用户ID
返回:
  prerequisites:
    - concept: 前置知识点
      required_level: 要求掌握度
      user_level: 用户当前掌握度
      status: 状态 (mastered|partial|missing)
```

### 6.3 可视化接口

```yaml
# 知识图谱数据
GET /api/concepts/{id}/graph
参数:
  depth: 深度 (1-3, 默认2)
  include_indirect: 是否包含间接关联 (默认false)
返回:
  nodes:
    - id: 节点ID
      name: 名称
      type: 节点类型 (current|prerequisite|sub_concept|parent|related)
      category: 分类
      x: x坐标
      y: y坐标
  edges:
    - source: 源节点ID
      target: 目标节点ID
      type: 关系类型
      label: 关系标签
```

---

## 七、性能优化

### 7.1 索引策略

```python
# Neo4j 索引创建
CREATE INDEX concept_name_index FOR (c:Concept) ON (c.name);
CREATE INDEX concept_category_index FOR (c:Concept) ON (c.category);
CREATE INDEX concept_difficulty_index FOR (c:Concept) ON (c.difficulty);

# Elasticsearch 索引配置
PUT /molbio_concepts
{
  "mappings": {
    "properties": {
      "name": {"type": "text", "analyzer": "ik_max_word"},
      "name_en": {"type": "text"},
      "definition": {"type": "text", "analyzer": "ik_max_word"},
      "category": {"type": "keyword"},
      "difficulty": {"type": "keyword"},
      "importance": {"type": "keyword"}
    }
  }
}
```

### 7.2 缓存策略

```python
# Redis缓存配置
CACHE_CONFIG = {
    "concept_detail": {"ttl": 3600},      # 知识点详情缓存1小时
    "search_results": {"ttl": 300},       # 搜索结果缓存5分钟
    "graph_data": {"ttl": 1800},          # 图谱数据缓存30分钟
    "recommendations": {"ttl": 600},      # 推荐结果缓存10分钟
    "hot_concepts": {"ttl": 3600}         # 热门知识点缓存1小时
}

# 缓存键设计
def get_cache_key(prefix, *args):
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"

# 示例
cache_key = get_cache_key("concept", "detail", concept_id)
# 结果: "concept:detail:dna_replication"
```

### 7.3 查询优化

```python
# 分页查询优化
def paginated_search(query, page=1, per_page=10):
    # 使用SKIP和LIMIT进行分页
    cypher = """
    MATCH (c:Concept)
    WHERE c.name CONTAINS $query
    RETURN c
    ORDER BY c.importance DESC, c.name
    SKIP $skip
    LIMIT $limit
    """
    skip = (page - 1) * per_page
    return run_query(cypher, query=query, skip=skip, limit=per_page)

# 异步并行查询
async def parallel_search(query):
    # 同时执行多个查询
    tasks = [
        search_neo4j(query),
        search_elasticsearch(query),
        search_cache(query)
    ]
    results = await asyncio.gather(*tasks)
    return merge_results(results)
```

---

## 八、总结

知识点智能检索系统的核心特性：

1. **多维度检索**：支持实体、关系、概念、语义四种检索方式
2. **智能推荐**：基于知识图谱的关联推荐和前置知识提示
3. **可视化展示**：D3.js驱动的知识图谱可视化，直观展示知识关系
4. **高性能**：多级缓存、索引优化、异步查询确保响应速度
5. **用户友好**：清晰的交互流程和丰富的知识卡片展示