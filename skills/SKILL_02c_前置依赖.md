# SKILL 02c: 前置依赖 — 知识点先修关系图

> 构建分子生物学课程的知识点前置依赖网络，定义学习路径，识别关键节点。

---

## 一、核心概念

### 1.1 前置依赖定义

前置依赖是指学习某一知识点之前必须先掌握的其他知识点。这种关系形成有向无环图（DAG），指导学习顺序。

```
知识点A ──前置──→ 知识点B
（必须先学A，才能学B）
```

### 1.2 依赖类型

| 类型 | 标记 | 说明 | 示例 |
|------|------|------|------|
| **强依赖** | `required` | 必须掌握，否则无法理解 | DNA结构 → DNA复制 |
| **推荐依赖** | `recommended` | 有助于理解，但非必须 | 有机化学 → 生物化学 |
| **类比依赖** | `analogy` | 概念相似，可类比迁移 | DNA复制 → RNA转录 |
| **应用依赖** | `application` | 理论→应用 | 复制原理 → PCR技术 |

---

## 二、依赖关系识别

### 2.1 识别规则

依赖关系通过以下方式识别：

| 规则 | 触发条件 | 示例 |
|------|----------|------|
| 术语引用 | 概念A的定义中引用概念B | "DNA聚合酶**在复制叉处**..." → 复制叉是前置 |
| 逻辑顺序 | 过程A在过程B之前发生 | 复制起始 → 复制延伸 |
| 结构组成 | A是B的组成部分 | 核苷酸 → DNA |
| 功能依赖 | A的功能依赖B | 翻译 → 转录（需要mRNA） |
| 数学依赖 | 需要数学概念 | 化学计量 → 反应动力学 |

### 2.2 依赖强度评估

```python
def calculate_dependency_strength(from_concept, to_concept, text):
    """计算两个概念间的依赖强度"""
    score = 0
    
    # 直接引用 +3
    if from_concept in get_prerequisites(to_concept, text):
        score += 3
    
    # 同一句中出现 +2
    if cooccur_in_sentence(from_concept, to_concept, text):
        score += 2
    
    # 同一段中出现 +1
    if cooccur_in_paragraph(from_concept, to_concept, text):
        score += 1
    
    # 距离越近分数越高
    distance = get_concept_distance(from_concept, to_concept, text)
    score += max(0, 3 - distance // 100)
    
    return score
```

**依赖强度分级**：
- 7-9分：强依赖（required）
- 4-6分：推荐依赖（recommended）
- 1-3分：弱相关（related）
- 0分：无依赖

---

## 三、依赖图构建

### 3.1 图结构定义

```json
{
  "dependency_graph": {
    "nodes": [
      {
        "id": "C01.02",
        "name": "DNA双螺旋结构",
        "chapter": "01",
        "level": "core",
        "difficulty": 2,
        "estimated_time": 30  // 分钟
      },
      {
        "id": "C02.01",
        "name": "DNA复制",
        "chapter": "02",
        "level": "core",
        "difficulty": 3,
        "estimated_time": 45
      },
      {
        "id": "C02.03",
        "name": "DNA聚合酶",
        "chapter": "02",
        "level": "core",
        "difficulty": 3,
        "estimated_time": 40
      }
    ],
    "edges": [
      {
        "from": "C01.02",
        "to": "C02.01",
        "type": "required",
        "strength": 8,
        "reason": "理解DNA复制必须先理解DNA结构"
      },
      {
        "from": "C02.01",
        "to": "C02.03",
        "type": "required",
        "strength": 7,
        "reason": "DNA聚合酶是DNA复制的执行者"
      },
      {
        "from": "C02.01",
        "to": "C03.01",
        "type": "analogy",
        "strength": 5,
        "reason": "转录与复制机制相似"
      }
    ]
  }
}
```

### 3.2 可视化表示

```
                    ┌─────────────┐
                    │ DNA双螺旋   │
                    │  C01.02     │
                    └──────┬──────┘
                           │ required
                           ▼
                    ┌─────────────┐
                    │ DNA复制     │◄──────────┐
                    │  C02.01     │           │ analogy
                    └──────┬──────┘           │
           ┌───────────────┼───────────────┐  │
           │ required      │ required      │  │
           ▼               ▼               ▼  │
    ┌─────────────┐ ┌─────────────┐ ┌─────────┴─┐
    │ DNA聚合酶   │ │ 复制叉      │ │ RNA转录   │
    │  C02.03     │ │  C02.04     │ │  C03.01   │
    └──────┬──────┘ └─────────────┘ └───────────┘
           │
           ▼
    ┌─────────────┐
    │ PCR技术     │
    │  A02.01     │
    └─────────────┘
```

---

## 四、学习路径生成

### 4.1 拓扑排序

基于依赖图生成学习顺序：

```python
def topological_sort(graph):
    """生成拓扑有序的学习路径"""
    visited = set()
    path = []
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        
        # 先学习所有前置知识点
        for prereq in get_prerequisites(node, graph):
            dfs(prereq)
        
        path.append(node)
    
    for node in graph.nodes:
        dfs(node)
    
    return path
```

### 4.2 最短学习路径

```python
def shortest_learning_path(target, graph):
    """计算到达目标知识点的最短学习路径"""
    # Dijkstra算法
    distances = {node: float('inf') for node in graph.nodes}
    distances[target] = 0
    
    pq = [(0, target)]
    while pq:
        dist, node = heapq.heappop(pq)
        
        for prereq in get_prerequisites(node, graph):
            new_dist = dist + get_learning_time(prereq)
            if new_dist < distances[prereq]:
                distances[prereq] = new_dist
                heapq.heappush(pq, (new_dist, prereq))
    
    return distances
```

### 4.3 个性化学习路径

```json
{
  "learning_path": {
    "student_profile": {
      "background": "生物学本科",
      "known_concepts": ["C01.01", "C01.02"],
      "target_concepts": ["C02.01", "C02.03", "A02.01"],
      "available_time": 120,  // 分钟
      "preferred_difficulty": "medium"
    },
    "generated_path": [
      {
        "step": 1,
        "concept": "C02.01",
        "name": "DNA复制",
        "estimated_time": 45,
        "reason": "目标概念，前置知识已掌握"
      },
      {
        "step": 2,
        "concept": "C02.03",
        "name": "DNA聚合酶",
        "estimated_time": 40,
        "reason": "DNA复制的核心执行者"
      },
      {
        "step": 3,
        "concept": "A02.01",
        "name": "PCR技术",
        "estimated_time": 35,
        "reason": "基于DNA复制原理的应用技术"
      }
    ],
    "total_time": 120,
    "coverage": "100%"
  }
}
```

---

## 五、关键节点识别

### 5.1 枢纽概念

枢纽概念是被大量其他概念依赖的核心概念：

```python
def find_hub_concepts(graph, top_n=10):
    """识别枢纽概念（高入度节点）"""
    in_degrees = {}
    for node in graph.nodes:
        in_degrees[node] = len(get_dependents(node, graph))
    
    return sorted(in_degrees.items(), 
                  key=lambda x: x[1], 
                  reverse=True)[:top_n]
```

**典型枢纽概念**：

| 概念 | 被依赖数 | 说明 |
|------|----------|------|
| DNA结构 | 15 | 后续所有DNA相关概念的基础 |
| 中心法则 | 12 | 遗传信息流动的核心框架 |
| 基因表达 | 10 | 转录和翻译的上位概念 |
| DNA聚合酶 | 8 | 多种技术的理论基础 |

### 5.2 瓶颈概念

瓶颈概念是通往多个高级概念的必经之路：

```python
def find_bottleneck_concepts(graph):
    """识别瓶颈概念（高介数中心性）"""
    betweenness = calculate_betweenness_centrality(graph)
    return sorted(betweenness.items(),
                  key=lambda x: x[1],
                  reverse=True)
```

### 5.3 前置链长度

```python
def prerequisite_chain_length(concept, graph, memo={}):
    """计算概念的前置链长度"""
    if concept in memo:
        return memo[concept]
    
    prereqs = get_prerequisites(concept, graph)
    if not prereqs:
        memo[concept] = 0
        return 0
    
    max_length = max(prerequisite_chain_length(p, graph, memo) 
                     for p in prereqs)
    memo[concept] = max_length + 1
    return memo[concept]
```

**前置链长度分布**：
- 0级：基础概念（如"细胞"、"分子"）
- 1级：直接依赖基础概念
- 2级：依赖1级概念
- 3级+：高级概念

---

## 六、依赖图验证

### 6.1 环检测

依赖图必须是无环的（DAG）：

```python
def detect_cycles(graph):
    """检测依赖图中的环"""
    visited = set()
    rec_stack = set()
    cycles = []
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in get_dependents(node, graph):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                # 发现环
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
        
        path.pop()
        rec_stack.remove(node)
    
    for node in graph.nodes:
        if node not in visited:
            dfs(node, [])
    
    return cycles
```

### 6.2 完整性检查

```python
def validate_dependencies(graph):
    """验证依赖图的完整性"""
    issues = []
    
    # 检查1：所有被依赖的概念都存在
    for edge in graph.edges:
        if edge.from not in graph.nodes:
            issues.append(f"缺失节点: {edge.from}")
        if edge.to not in graph.nodes:
            issues.append(f"缺失节点: {edge.to}")
    
    # 检查2：无环
    cycles = detect_cycles(graph)
    if cycles:
        issues.append(f"发现环: {cycles}")
    
    # 检查3：所有概念可达（从基础概念出发）
    roots = [n for n in graph.nodes if not get_prerequisites(n, graph)]
    if not roots:
        issues.append("无根节点（所有概念都有前置）")
    
    # 检查4：依赖强度合理
    for edge in graph.edges:
        if edge.strength < 1 or edge.strength > 9:
            issues.append(f"依赖强度异常: {edge}")
    
    return issues
```

---

## 七、工具链

### 7.1 脚本一览

| 脚本 | 位置 | 功能 |
|------|------|------|
| `prereq_extract.py` | scripts/ | 从标注文本提取依赖关系 |
| `prereq_graph_build.py` | scripts/ | 构建依赖图 |
| `prereq_analyze.py` | scripts/ | 分析依赖图（枢纽、瓶颈） |
| `learning_path_gen.py` | scripts/ | 生成学习路径 |
| `lint_prereq.py` | scripts/ | 依赖图验证 |

### 7.2 处理流程

```bash
# 1. 提取依赖关系
python scripts/prereq_extract.py

# 2. 构建依赖图
python scripts/prereq_graph_build.py

# 3. 分析依赖图
python scripts/prereq_analyze.py

# 4. 生成学习路径
python scripts/learning_path_gen.py --target C02.03

# 5. 验证
python scripts/lint_prereq.py
```

---

## 八、质量检查

### 8.1 lint_prereq.py 检查项

**依赖图结构检查**：
- 无环（DAG）
- 所有节点可达
- 依赖强度合理（1-9）

**依赖逻辑检查**：
- 无冗余依赖（A→B→C，则不需要A→C）
- 无矛盾依赖（A依赖B，B又依赖A）
- 难度递增（前置概念难度 ≤ 后置概念难度）

**常见问题及修复**：

| 问题 | 表现 | 修复方式 |
|------|------|---------|
| 依赖环 | A→B→C→A | 识别并打破环 |
| 孤立节点 | 无前置也无后置 | 检查是否为孤立概念，或补充依赖 |
| 难度倒置 | 前置比后置更难 | 调整难度评级或依赖方向 |
| 冗余依赖 | 存在传递闭包中的直接边 | 删除冗余边 |

---

## 九、扩展到其他课程

| 课程类型 | 典型依赖链 | 特殊考虑 |
|----------|------------|----------|
| 数学课程 | 定理依赖、证明链 | 严格顺序，少并行 |
| 编程课程 | 语法→算法→项目 | 实践依赖理论 |
| 语言课程 | 词汇→语法→阅读 | 技能并行发展 |
| 实验课程 | 理论→操作→分析 | 安全前置要求 |

---

*本SKILL文档基于分子生物学课程的前置依赖构建经验提炼。*
*核心产出：~450知识点，~600依赖边，平均前置链长度2.5。*
