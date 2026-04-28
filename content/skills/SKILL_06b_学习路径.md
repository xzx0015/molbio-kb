# SKILL 06b: 个性化学习路径系统

> 基于知识依赖图谱和学习者状态的个性化学习路径生成与优化系统。

---

## 一、系统概述

### 1.1 设计目标

- **个性化路径**：根据学习者当前状态生成定制化学习路径
- **依赖感知**：严格遵循知识前置依赖关系
- **灵活策略**：支持最短路径、最完整路径等多种策略
- **薄弱识别**：自动识别学习薄弱环节并推荐强化

### 1.2 核心功能

```
┌─────────────────────────────────────────────────────────────────┐
│                     个性化学习路径系统                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │ 掌握度评估   │  │ 路径生成    │  │ 薄弱识别    │  │ 进度追踪│ │
│  │             │  │             │  │             │  │        │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 最短路径    │  │ 最完整路径  │  │ 自适应调整  │             │
│  │             │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、知识点掌握度评估

### 2.1 评估维度

| 维度 | 说明 | 权重 |
|------|------|------|
| **测试正确率** | 该知识点相关题目的正确率 | 40% |
| **学习时长** | 实际学习时长与建议时长的比例 | 20% |
| **学习次数** | 学习该知识点的次数 | 15% |
| **前置掌握** | 前置知识的平均掌握度 | 15% |
| **最近学习** | 最近学习的时间衰减 | 10% |

### 2.2 掌握度计算模型

```python
class MasteryCalculator:
    """
    知识点掌握度计算模型
    """
    
    def calculate_mastery(self, user_id: str, concept_id: str) -> float:
        """
        计算用户对某知识点的掌握度 (0-1)
        """
        # 1. 获取学习数据
        study_data = self.get_study_data(user_id, concept_id)
        
        # 2. 计算各维度得分
        test_score = self._calc_test_score(study_data['test_results'])
        time_score = self._calc_time_score(study_data['study_time'], study_data['recommended_time'])
        count_score = self._calc_count_score(study_data['study_count'])
        prereq_score = self._calc_prerequisite_score(user_id, concept_id)
        recency_score = self._calc_recency_score(study_data['last_study_time'])
        
        # 3. 加权求和
        mastery = (
            test_score * 0.40 +
            time_score * 0.20 +
            count_score * 0.15 +
            prereq_score * 0.15 +
            recency_score * 0.10
        )
        
        return min(mastery, 1.0)
    
    def _calc_test_score(self, test_results: list) -> float:
        """计算测试正确率得分"""
        if not test_results:
            return 0.0
        
        # 加权平均，最近测试权重更高
        weights = [0.5 ** i for i in range(len(test_results))]
        weights.reverse()
        
        weighted_sum = sum(r['correct'] * w for r, w in zip(test_results, weights))
        total_weight = sum(weights)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _calc_time_score(self, actual_time: int, recommended_time: int) -> float:
        """计算学习时长得分"""
        if recommended_time == 0:
            return 0.5
        
        ratio = actual_time / recommended_time
        # 达到建议时长得满分，不足按比例，超过不加分
        return min(ratio, 1.0)
    
    def _calc_count_score(self, study_count: int) -> float:
        """计算学习次数得分"""
        # 学习1次得0.3，2次得0.6，3次及以上得1.0
        if study_count >= 3:
            return 1.0
        return study_count * 0.3
    
    def _calc_prerequisite_score(self, user_id: str, concept_id: str) -> float:
        """计算前置知识掌握度得分"""
        prereqs = self.get_prerequisites(concept_id)
        if not prereqs:
            return 1.0
        
        prereq_masteries = [self.calculate_mastery(user_id, p) for p in prereqs]
        return sum(prereq_masteries) / len(prereq_masteries)
    
    def _calc_recency_score(self, last_study_time: datetime) -> float:
        """计算最近学习时间得分（时间衰减）"""
        if last_study_time is None:
            return 0.0
        
        days_since = (datetime.now() - last_study_time).days
        # 7天内得1.0，30天内线性衰减，超过30天得0.3
        if days_since <= 7:
            return 1.0
        elif days_since <= 30:
            return 1.0 - (days_since - 7) / 23 * 0.7
        else:
            return 0.3
```

### 2.3 掌握度等级划分

| 掌握度 | 等级 | 颜色 | 说明 |
|--------|------|------|------|
| 0.0 - 0.3 | 未掌握 | 🔴 | 需要系统学习 |
| 0.3 - 0.5 | 初步了解 | 🟠 | 需要加强练习 |
| 0.5 - 0.7 | 基本掌握 | 🟡 | 可以进阶学习 |
| 0.7 - 0.9 | 熟练掌握 | 🟢 | 可以应用实践 |
| 0.9 - 1.0 | 精通 | 🔵 | 可以教授他人 |

### 2.4 掌握度可视化

```
┌─────────────────────────────────────────────────────────────┐
│  知识点掌握度总览                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DNA复制                                    [████████░░] 85%│
│  ├── 半保留复制                             [██████████] 95%│
│  ├── 复制叉                                 [███████░░░] 70%│
│  ├── DNA聚合酶                              [████████░░] 80%│
│  ├── 冈崎片段                               [████░░░░░░] 40%│  ⚠️ 薄弱
│  └── 引物酶                                 [░░░░░░░░░░]  0%│  ⚠️ 未学习
│                                                             │
│  转录                                       [██████░░░░] 60%│
│  ├── 转录起始                               [████████░░] 85%│
│  ├── RNA聚合酶                              [█████░░░░░] 50%│
│  └── 转录因子                               [░░░░░░░░░░]  0%│  ⚠️ 未学习
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、学习路径生成

### 3.1 路径生成算法

#### 3.1.1 拓扑排序基础

```python
from collections import defaultdict, deque

def topological_sort(concepts: list, dependencies: dict) -> list:
    """
    基于前置依赖的拓扑排序
    concepts: 知识点列表
    dependencies: {concept_id: [prereq_ids]} 依赖关系
    """
    # 计算入度
    in_degree = {c: 0 for c in concepts}
    for concept, prereqs in dependencies.items():
        in_degree[concept] = len(prereqs)
    
    # 初始化队列（入度为0的节点）
    queue = deque([c for c in concepts if in_degree[c] == 0])
    result = []
    
    while queue:
        concept = queue.popleft()
        result.append(concept)
        
        # 更新依赖此知识点的入度
        for c, prereqs in dependencies.items():
            if concept in prereqs:
                in_degree[c] -= 1
                if in_degree[c] == 0:
                    queue.append(c)
    
    return result
```

#### 3.1.2 最短路径算法

```python
import heapq
from dataclasses import dataclass

@dataclass
class PathNode:
    concept_id: str
    cost: float  # 学习成本（时间）
    mastery_gain: float  # 掌握度提升

def shortest_learning_path(
    user_id: str,
    target_concept: str,
    mastery_threshold: float = 0.7
) -> list:
    """
    生成从当前状态到目标知识点的最短学习路径
    考虑已掌握的知识点，只学习未掌握的前置知识
    """
    # 1. 获取目标知识点的所有前置依赖
    all_prereqs = get_all_prerequisites(target_concept)
    
    # 2. 过滤已掌握的知识点
    concepts_to_learn = [
        c for c in all_prereqs 
        if get_mastery(user_id, c) < mastery_threshold
    ]
    concepts_to_learn.append(target_concept)
    
    # 3. 构建依赖图
    graph = build_dependency_graph(concepts_to_learn)
    
    # 4. 使用Dijkstra算法找最短路径
    # 边的权重 = 建议学习时长 / 难度系数
    return dijkstra_path(graph, start=None, target=target_concept)

def dijkstra_path(graph: dict, start: str, target: str) -> list:
    """
    Dijkstra最短路径算法
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    
    pq = [(0, start)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current == target:
            break
        
        if current_dist > distances[current]:
            continue
        
        for neighbor, weight in graph[current].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    # 重建路径
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path
```

#### 3.1.3 最完整路径算法

```python
def comprehensive_learning_path(
    user_id: str,
    target_concept: str,
    include_optional: bool = True
) -> list:
    """
    生成最完整的学习路径
    包含所有前置知识、相关知识和推荐扩展
    """
    path = []
    
    # 1. 强依赖路径（必须学习）
    strong_prereqs = get_prerequisites(target_concept, level='strong')
    path.extend(topological_sort(strong_prereqs))
    
    # 2. 弱依赖路径（推荐学习）
    weak_prereqs = get_prerequisites(target_concept, level='weak')
    path.extend(topological_sort(weak_prereqs))
    
    # 3. 可选扩展（根据用户偏好）
    if include_optional:
        optional = get_related_concepts(target_concept, limit=5)
        path.extend(optional)
    
    # 4. 目标知识点
    path.append(target_concept)
    
    return path
```

### 3.2 路径策略对比

| 策略 | 适用场景 | 特点 | 示例 |
|------|---------|------|------|
| **最短路径** | 时间紧迫、考前冲刺 | 只学必要前置知识 | 学PCR只需掌握DNA复制基础 |
| **最完整路径** | 系统学习、深度学习 | 包含所有相关知识点 | 学PCR需学复制原理、引物设计、酶学等 |
| **推荐路径** | 日常学习 | 平衡深度和广度 | 根据掌握度动态调整 |
| **复习路径** | 查漏补缺 | 针对薄弱环节 | 只学掌握度<0.5的知识点 |

### 3.3 路径可视化

```
┌─────────────────────────────────────────────────────────────┐
│  个性化学习路径: DNA复制                                    │
│  预计总时长: 3小时30分钟  |  已掌握: 2/8 知识点            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  阶段 1: 前置基础 (45分钟)                                  │
│  ═══════════════════════════════════════════════════════   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ DNA结构     │───→│ 碱基配对    │───→│ 酶基础      │     │
│  │ [已掌握 ✓]  │    │ [已掌握 ✓]  │    │ [学习中 ▶]  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  阶段 2: 核心机制 (90分钟)                                  │
│  ═══════════════════════════════════════════════════════   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ 半保留复制  │───→│ 复制叉      │───→│ DNA聚合酶   │     │
│  │ [未开始 ○]  │    │ [未开始 ○]  │    │ [未开始 ○]  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         ↓                                                   │
│  ┌─────────────┐    ┌─────────────┐                         │
│  │ 冈崎片段    │───→│ DNA连接酶   │                         │
│  │ [未开始 ○]  │    │ [未开始 ○]  │                         │
│  └─────────────┘    └─────────────┘                         │
│                                                             │
│  阶段 3: 应用拓展 (45分钟)                                  │
│  ═══════════════════════════════════════════════════════   │
│  ┌─────────────┐    ┌─────────────┐                         │
│  │ 复制调控    │───→│ PCR技术     │                         │
│  │ [未开始 ○]  │    │ [未开始 ○]  │                         │
│  └─────────────┘    └─────────────┘                         │
│                                                             │
│  [开始学习]  [调整路径]  [导出计划]                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、薄弱环节识别

### 4.1 薄弱点检测算法

```python
def identify_weak_areas(user_id: str, concept_area: str = None) -> dict:
    """
    识别学习者的薄弱环节
    """
    weak_areas = {
        'concepts': [],      # 薄弱知识点
        'categories': [],    # 薄弱分类
        'dependencies': [],  # 依赖断裂点
        'patterns': []       # 薄弱模式
    }
    
    # 1. 识别掌握度低的知识点
    concepts = get_all_concepts(area=concept_area)
    for concept in concepts:
        mastery = get_mastery(user_id, concept)
        if mastery < 0.5:
            weak_areas['concepts'].append({
                'concept': concept,
                'mastery': mastery,
                'priority': calculate_priority(concept)
            })
    
    # 2. 识别薄弱分类
    category_masteries = {}
    for concept in concepts:
        category = get_category(concept)
        mastery = get_mastery(user_id, concept)
        if category not in category_masteries:
            category_masteries[category] = []
        category_masteries[category].append(mastery)
    
    for category, masteries in category_masteries.items():
        avg_mastery = sum(masteries) / len(masteries)
        if avg_mastery < 0.6:
            weak_areas['categories'].append({
                'category': category,
                'avg_mastery': avg_mastery,
                'concept_count': len(masteries)
            })
    
    # 3. 识别依赖断裂点
    for concept in concepts:
        mastery = get_mastery(user_id, concept)
        if mastery >= 0.7:  # 已掌握
            continue
        
        prereqs = get_prerequisites(concept)
        prereq_masteries = [get_mastery(user_id, p) for p in prereqs]
        
        # 如果前置知识掌握良好但当前知识薄弱
        if prereq_masteries and min(prereq_masteries) >= 0.6:
            weak_areas['dependencies'].append({
                'concept': concept,
                'prereq_mastery': sum(prereq_masteries) / len(prereq_masteries),
                'current_mastery': mastery
            })
    
    # 4. 识别薄弱模式
    weak_areas['patterns'] = analyze_weak_patterns(user_id)
    
    return weak_areas

def analyze_weak_patterns(user_id: str) -> list:
    """
    分析薄弱模式（如：总是学不会某类概念）
    """
    patterns = []
    
    # 按题型分析
    question_type_stats = get_question_type_stats(user_id)
    for q_type, accuracy in question_type_stats.items():
        if accuracy < 0.5:
            patterns.append({
                'type': 'question_type',
                'detail': q_type,
                'accuracy': accuracy,
                'suggestion': f'建议加强{q_type}类型题目的练习'
            })
    
    # 按难度分析
    difficulty_stats = get_difficulty_stats(user_id)
    for diff, accuracy in difficulty_stats.items():
        if accuracy < 0.5:
            patterns.append({
                'type': 'difficulty',
                'detail': diff,
                'accuracy': accuracy,
                'suggestion': f'建议先巩固{diff}难度知识点'
            })
    
    return patterns
```

### 4.2 薄弱点报告

```
┌─────────────────────────────────────────────────────────────┐
│  薄弱环节分析报告                                           │
│  生成时间: 2025-03-17  |  学习者: 张同学                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 整体掌握度: 62% (中等偏下)                              │
│                                                             │
│  🔴 薄弱知识点 (掌握度 < 50%)                               │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. 冈崎片段                              掌握度: 40% │ │
│  │    └─ 建议: 复习DNA复制机制，重点理解后随链合成       │ │
│  │                                                       │ │
│  │ 2. 转录因子                              掌握度: 35% │ │
│  │    └─ 建议: 学习通用转录因子与特异性转录因子的区别    │ │
│  │                                                       │ │
│  │ 3. 密码子简并性                          掌握度: 30% │ │
│  │    └─ 建议: 理解摆动假说，练习密码子-氨基酸对应       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  🟠 薄弱分类 (平均掌握度 < 60%)                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ • 翻译后修饰                             平均: 45%     │ │
│  │   包含: 蛋白质折叠(40%), 糖基化(50%), 磷酸化(45%)     │ │
│  │                                                       │ │
│  │ • 转录调控                               平均: 52%     │ │
│  │   包含: 操纵子模型(55%), 乳糖操纵子(50%), 色氨酸操纵子│ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  🔗 依赖断裂点                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ • 已掌握"DNA聚合酶"但"冈崎片段"薄弱                   │ │
│  │   可能原因: 理解酶的功能但未掌握复制过程的连续性      │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  📈 薄弱模式                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ • 案例分析题正确率仅 35%，建议加强应用练习            │ │
│  │ • 高难度题目正确率仅 28%，建议先巩固基础              │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [生成强化计划]  [查看详情]  [导出报告]                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、用户交互流程

### 5.1 路径生成流程

```
用户选择学习目标
      ↓
系统评估当前掌握度
      ↓
分析前置依赖关系
      ↓
选择路径策略
┌─────────┬─────────┬─────────┐
↓         ↓         ↓         ↓
最短路径  最完整路径 推荐路径  复习路径
      ↓
生成个性化路径
      ↓
展示路径可视化
      ↓
用户确认/调整
      ↓
开始学习
```

### 5.2 进度追踪流程

```
用户完成学习/练习
      ↓
更新知识点掌握度
      ↓
检查路径进度
      ↓
是否需要调整?
      ↓
是 → 重新计算路径 → 推荐调整
      ↓
否 → 继续下一知识点
      ↓
生成学习报告
```

---

## 六、API接口设计

### 6.1 路径生成接口

```yaml
POST /api/learning-paths/generate
参数:
  user_id: 用户ID
  target_concept: 目标知识点ID
  strategy: 路径策略 (shortest|comprehensive|recommended|review)
  time_budget: 时间预算(分钟, 可选)
返回:
  path_id: 路径ID
  path_name: 路径名称
  total_time: 预计总时长
  stages: 学习阶段列表
    - stage_id: 阶段ID
      stage_name: 阶段名称
      concepts: 知识点列表
        - concept_id: 知识点ID
          name: 名称
          estimated_time: 预计时长
          mastery_required: 目标掌握度
  prerequisites_summary: 前置知识概况

GET /api/learning-paths/{path_id}
返回:
  path详情
  progress: 当前进度
  completed_concepts: 已完成知识点
  current_concept: 当前学习知识点
  next_concepts: 待学习知识点

POST /api/learning-paths/{path_id}/adjust
参数:
  reason: 调整原因 (time_constraint|difficulty|interest)
  preferences: 调整偏好
返回:
  adjusted_path: 调整后的路径
```

### 6.2 掌握度接口

```yaml
GET /api/users/{user_id}/mastery
参数:
  concept_id: 知识点ID(可选, 不传则返回全部)
返回:
  concept_id: 知识点ID
  mastery_level: 掌握度(0-1)
  mastery_grade: 掌握等级
  last_study: 最后学习时间
  study_count: 学习次数
  test_accuracy: 测试正确率

POST /api/users/{user_id}/mastery/update
参数:
  concept_id: 知识点ID
  study_time: 本次学习时长
  test_result: 测试结果(可选)
返回:
  updated_mastery: 更新后的掌握度
  mastery_change: 掌握度变化
  next_recommendation: 下一步建议
```

### 6.3 薄弱点接口

```yaml
GET /api/users/{user_id}/weak-areas
参数:
  area: 知识领域(可选)
  threshold: 掌握度阈值(默认0.5)
返回:
  weak_concepts: 薄弱知识点列表
  weak_categories: 薄弱分类列表
  dependency_gaps: 依赖断裂点
  weak_patterns: 薄弱模式
  recommendations: 强化建议

POST /api/users/{user_id}/strengthen-plan
参数:
  weak_areas: 薄弱点列表
  time_budget: 时间预算
返回:
  plan_id: 计划ID
  plan_name: 计划名称
  daily_tasks: 每日任务
  expected_improvement: 预期提升
```

---

## 七、总结

个性化学习路径系统的核心特性：

1. **多维度掌握度评估**：综合考虑测试成绩、学习时长、学习次数、前置掌握和最近学习
2. **智能路径生成**：支持最短路径、最完整路径、推荐路径和复习路径四种策略
3. **薄弱点精准识别**：从知识点、分类、依赖和模式四个维度识别薄弱环节
4. **动态路径调整**：根据学习进度实时调整路径，确保学习效率
5. **可视化展示**：清晰的路径图和掌握度热力图，直观展示学习状态