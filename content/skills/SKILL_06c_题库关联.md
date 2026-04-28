# SKILL 06c: 知识点-题库关联系统

> 基于知识图谱的题目多标签标注、难度分级和知识点覆盖分析系统。

---

## 一、系统概述

### 1.1 设计目标

- **精准标注**：每道题目精确标注考查的知识点和认知层次
- **难度分级**：科学的难度评估和自适应调整机制
- **覆盖分析**：全面分析题库对知识点的覆盖情况
- **智能推荐**：基于薄弱知识点的个性化题目推荐

### 1.2 核心功能

```
┌─────────────────────────────────────────────────────────────────┐
│                     知识点-题库关联系统                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │ 多标签标注   │  │ 难度分级    │  │ 覆盖分析    │  │ 智能推荐│ │
│  │             │  │             │  │             │  │        │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 题目录入    │  │ 标签管理    │  │ 统计分析    │             │
│  │             │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、题目多标签标注

### 2.1 标签体系

#### 2.1.1 知识点标签

```python
# 知识点标签结构
question_tags = {
    "primary_concept": "主要考查知识点",      # 1个
    "secondary_concepts": ["次要知识点"],     # 0-n个
    "prerequisite_concepts": ["涉及的前置知识"], # 0-n个
    "application_concepts": ["应用知识点"]     # 0-n个
}
```

**标注示例**：

```yaml
题目: "DNA复制时，后随链上合成的短片段被称为什么？"

知识点标签:
  primary_concept: "冈崎片段"              # 直接考查
  secondary_concepts:                      # 相关考查
    - "DNA复制"
    - "后随链"
  prerequisite_concepts:                   # 需要了解
    - "DNA结构"
    - "碱基配对"
  application_concepts: []                  # 无应用拓展

认知层次标签:
  bloom_level: "记忆"                      # 布鲁姆认知层次
  cognitive_depth: 1                       # 认知深度 1-5
  
难度标签:
  difficulty: "L2"                         # L1-L5
  discrimination: 0.65                     # 区分度
  
题型标签:
  question_type: "单选题"
  answer_type: "概念识别"
```

#### 2.1.2 认知层次标签（布鲁姆分类法）

| 层次 | 说明 | 关键词 | 示例 |
|------|------|--------|------|
| **记忆** | 回忆事实、术语 | 是什么、定义、名称 | DNA的全称是？ |
| **理解** | 解释概念、原理 | 为什么、解释、说明 | 为什么DNA复制是半保留的？ |
| **应用** | 在新情境使用知识 | 如何、应用、举例 | 如何设计PCR引物？ |
| **分析** | 分解、比较、关联 | 比较、区别、分析 | 比较DNA复制与转录的异同 |
| **评价** | 判断、评估 | 评价、判断、选择 | 评价该实验设计的合理性 |
| **创造** | 综合、设计、创新 | 设计、提出、构建 | 设计一个验证半保留复制的实验 |

#### 2.1.3 题型标签

| 一级分类 | 二级分类 | 说明 |
|---------|---------|------|
| **客观题** | 单选题 | 只有一个正确答案 |
| | 多选题 | 多个正确答案 |
| | 判断题 | 正确/错误判断 |
| | 填空题 | 填写关键术语 |
| **主观题** | 简答题 | 简要回答概念 |
| | 论述题 | 详细阐述原理 |
| | 计算题 | 数值计算 |
| | 案例分析 | 分析实际案例 |
| **实验题** | 实验设计 | 设计实验方案 |
| | 实验分析 | 分析实验结果 |

### 2.2 标注流程

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ 题目录入 │ ──→│ 自动标注 │ ──→│ 人工审核 │ ──→│ 质量检查 │ ──→│ 发布入库 │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                    │               │               │
                    ↓               ↓               ↓
              ┌─────────┐     ┌─────────┐     ┌─────────┐
              │NLP实体识别│     │专家审核  │     │一致性检查│
              │关键词匹配│     │标签修正  │     │完整性检查│
              └─────────┘     └─────────┘     └─────────┘
```

**自动标注实现**：

```python
import spacy
from typing import List, Dict

class QuestionAutoTagger:
    """题目自动标注器"""
    
    def __init__(self, concept_graph, nlp_model):
        self.concept_graph = concept_graph  # 知识图谱
        self.nlp = nlp_model                # NLP模型
    
    def auto_tag(self, question_text: str, answer_text: str = None) -> Dict:
        """
        自动标注题目
        """
        tags = {
            "primary_concept": None,
            "secondary_concepts": [],
            "prerequisite_concepts": [],
            "bloom_level": None,
            "question_type": None,
            "difficulty_estimate": None
        }
        
        # 1. 实体识别（知识点提取）
        doc = self.nlp(question_text)
        entities = [ent.text for ent in doc.ents if ent.label_ == "CONCEPT"]
        
        # 2. 匹配知识图谱
        matched_concepts = []
        for entity in entities:
            concept = self.concept_graph.find_concept(entity)
            if concept:
                matched_concepts.append(concept)
        
        # 3. 确定主要知识点
        if matched_concepts:
            tags["primary_concept"] = self._select_primary_concept(
                matched_concepts, question_text
            )
            tags["secondary_concepts"] = [
                c for c in matched_concepts 
                if c != tags["primary_concept"]
            ]
        
        # 4. 查找前置知识
        if tags["primary_concept"]:
            tags["prerequisite_concepts"] = self.concept_graph.get_prerequisites(
                tags["primary_concept"]
            )
        
        # 5. 判断认知层次
        tags["bloom_level"] = self._detect_bloom_level(question_text)
        
        # 6. 估计难度
        tags["difficulty_estimate"] = self._estimate_difficulty(
            question_text, tags
        )
        
        return tags
    
    def _select_primary_concept(self, concepts: List, question_text: str) -> str:
        """选择主要知识点"""
        # 优先选择在问题主干中出现的概念
        for concept in concepts:
            if concept in question_text.split("？")[0]:
                return concept
        return concepts[0]
    
    def _detect_bloom_level(self, question_text: str) -> str:
        """检测布鲁姆认知层次"""
        bloom_keywords = {
            "记忆": ["是什么", "定义", "名称", "全称", "谁发现"],
            "理解": ["为什么", "解释", "说明", "原理", "机制"],
            "应用": ["如何", "怎样", "应用", "举例", "设计"],
            "分析": ["比较", "区别", "分析", "异同", "关系"],
            "评价": ["评价", "判断", "选择", "合理性", "优缺点"],
            "创造": ["设计", "提出", "构建", "创新", "改进"]
        }
        
        for level, keywords in bloom_keywords.items():
            if any(kw in question_text for kw in keywords):
                return level
        
        return "记忆"  # 默认
    
    def _estimate_difficulty(self, question_text: str, tags: Dict) -> str:
        """估计题目难度"""
        score = 0
        
        # 基于认知层次
        bloom_scores = {"记忆": 1, "理解": 2, "应用": 3, "分析": 4, "评价": 5, "创造": 5}
        score += bloom_scores.get(tags["bloom_level"], 1)
        
        # 基于涉及知识点数量
        score += len(tags["secondary_concepts"]) * 0.5
        
        # 基于文本长度（信息复杂度）
        score += len(question_text) / 100
        
        # 映射到难度等级
        if score <= 2:
            return "L1"
        elif score <= 3:
            return "L2"
        elif score <= 4:
            return "L3"
        elif score <= 5:
            return "L4"
        else:
            return "L5"
```

### 2.3 标签管理界面

```
┌─────────────────────────────────────────────────────────────┐
│  题目标注编辑器                                    [保存]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  题目内容:                                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ DNA复制时，后随链上合成的短片段被称为什么？            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  参考答案: 冈崎片段                                         │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  📌 知识点标签                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 主要知识点: [冈崎片段                    ] [🔍搜索]   │ │
│  │                                                       │ │
│  │ 次要知识点: [DNA复制  ] [后随链  ] [+添加]            │ │
│  │                                                       │ │
│  │ 前置知识:   [DNA结构   ] [碱基配对] [+添加]            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  🧠 认知层次                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ( ) 记忆  (●) 理解  ( ) 应用  ( ) 分析  ( ) 评价      │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  📊 难度分级                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ L1(基础)  L2(简单)  L3(中等)  L4(较难)  L5(困难)      │ │
│  │         ●────┬────┬────┬────┬────                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  📝 题型                                                    │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ [单选题 ▼]  [概念识别 ▼]                              │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [自动标注]  [取消]  [保存并下一题]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、难度分级

### 3.1 难度等级定义

| 等级 | 名称 | 通过率 | 描述 | 适合阶段 |
|------|------|--------|------|---------|
| **L1** | 基础 | 90-100% | 直接记忆性题目 | 初学阶段 |
| **L2** | 简单 | 70-90% | 理解性题目 | 基础巩固 |
| **L3** | 中等 | 50-70% | 应用性题目 | 能力提升 |
| **L4** | 较难 | 30-50% | 分析性题目 | 进阶训练 |
| **L5** | 困难 | 0-30% | 综合性/创造性题目 | 挑战提高 |

### 3.2 难度校准（IRT模型）

```python
import numpy as np
from scipy.optimize import minimize

class IRTCalibrator:
    """
    基于项目反应理论(IRT)的难度校准
    使用1PL/Rasch模型或2PL模型
    """
    
    def __init__(self, model="2pl"):
        self.model = model
        self.parameters = {}
    
    def calibrate(self, responses: np.ndarray) -> Dict:
        """
        校准题目参数
        responses: shape (n_students, n_questions) 答题矩阵
        """
        n_students, n_questions = responses.shape
        
        # 初始化参数
        abilities = np.zeros(n_students)      # 学生能力
        difficulties = np.zeros(n_questions)  # 题目难度
        discriminations = np.ones(n_questions) if self.model == "2pl" else None
        
        # 联合极大似然估计
        def negative_log_likelihood(params):
            # 解包参数
            n = n_students
            abilities = params[:n]
            difficulties = params[n:n+n_questions]
            
            if self.model == "2pl":
                discriminations = params[n+n_questions:]
            
            # 计算概率
            if self.model == "1pl":
                prob = self._rasch_model(abilities, difficulties)
            else:
                prob = self._2pl_model(abilities, difficulties, discriminations)
            
            # 计算负对数似然
            ll = np.sum(responses * np.log(prob) + (1-responses) * np.log(1-prob))
            return -ll
        
        # 优化
        initial_params = np.concatenate([abilities, difficulties])
        if self.model == "2pl":
            initial_params = np.concatenate([initial_params, discriminations])
        
        result = minimize(negative_log_likelihood, initial_params, method='L-BFGS-B')
        
        # 提取校准后的参数
        self.parameters = {
            "abilities": result.x[:n_students],
            "difficulties": result.x[n_students:n_students+n_questions],
        }
        
        if self.model == "2pl":
            self.parameters["discriminations"] = result.x[n_students+n_questions:]
        
        return self.parameters
    
    def _rasch_model(self, abilities, difficulties):
        """Rasch模型 (1PL)"""
        # P(正确) = 1 / (1 + exp(-(ability - difficulty)))
        return 1 / (1 + np.exp(-(abilities[:, np.newaxis] - difficulties)))
    
    def _2pl_model(self, abilities, difficulties, discriminations):
        """2PL模型"""
        # P(正确) = 1 / (1 + exp(-a * (ability - difficulty)))
        return 1 / (1 + np.exp(
            -discriminations * (abilities[:, np.newaxis] - difficulties)
        ))
    
    def estimate_difficulty_level(self, difficulty: float) -> str:
        """
        将连续难度值映射到离散等级
        """
        if difficulty < -1.5:
            return "L1"
        elif difficulty < -0.5:
            return "L2"
        elif difficulty < 0.5:
            return "L3"
        elif difficulty < 1.5:
            return "L4"
        else:
            return "L5"
```

### 3.3 区分度计算

```python
def calculate_discrimination(responses: list, total_scores: list) -> float:
    """
    计算题目的区分度（点二列相关系数）
    
    responses: 该题的答题情况 (0/1)
    total_scores: 每个学生的总分
    """
    # 按总分分组（高分组 vs 低分组）
    n = len(responses)
    sorted_indices = np.argsort(total_scores)
    
    # 取前27%和后27%
    high_group = sorted_indices[int(n*0.73):]
    low_group = sorted_indices[:int(n*0.27)]
    
    # 计算通过率
    high_pass_rate = np.mean([responses[i] for i in high_group])
    low_pass_rate = np.mean([responses[i] for i in low_group])
    
    # 区分度 = 高分组通过率 - 低分组通过率
    discrimination = high_pass_rate - low_pass_rate
    
    return discrimination

# 区分度评价标准
DISCRIMINATION_LEVELS = {
    "excellent": (0.4, 1.0),    # 优秀，保留
    "good": (0.3, 0.4),         # 良好，保留
    "fair": (0.2, 0.3),         # 一般，需修改
    "poor": (0.0, 0.2),         # 较差，需修改或删除
    "invalid": (-1.0, 0.0)      # 异常（负区分度），删除
}
```

---

## 四、知识点覆盖分析

### 4.1 覆盖度指标

```python
class CoverageAnalyzer:
    """知识点覆盖度分析器"""
    
    def __init__(self, concept_graph, question_bank):
        self.concept_graph = concept_graph
        self.question_bank = question_bank
    
    def analyze_coverage(self, area: str = None) -> Dict:
        """
        分析题库对知识点的覆盖情况
        """
        # 获取该领域所有知识点
        concepts = self.concept_graph.get_concepts(area=area)
        
        coverage = {
            "overall": {},
            "by_category": {},
            "by_difficulty": {},
            "by_bloom": {},
            "gaps": []
        }
        
        # 1. 总体覆盖度
        covered_concepts = set()
        for question in self.question_bank:
            covered_concepts.update(question.get_concepts())
        
        coverage["overall"] = {
            "total_concepts": len(concepts),
            "covered_concepts": len(covered_concepts),
            "coverage_rate": len(covered_concepts) / len(concepts),
            "total_questions": len(self.question_bank)
        }
        
        # 2. 按分类覆盖
        for category in self.concept_graph.get_categories():
            cat_concepts = self.concept_graph.get_concepts(category=category)
            cat_covered = len(set(cat_concepts) & covered_concepts)
            coverage["by_category"][category] = {
                "total": len(cat_concepts),
                "covered": cat_covered,
                "rate": cat_covered / len(cat_concepts) if cat_concepts else 0
            }
        
        # 3. 按难度覆盖
        for level in ["L1", "L2", "L3", "L4", "L5"]:
            questions = [q for q in self.question_bank if q.difficulty == level]
            coverage["by_difficulty"][level] = len(questions)
        
        # 4. 识别覆盖缺口
        coverage["gaps"] = self._identify_gaps(concepts, covered_concepts)
        
        return coverage
    
    def _identify_gaps(self, all_concepts: list, covered_concepts: set) -> list:
        """识别覆盖缺口"""
        gaps = []
        
        for concept in all_concepts:
            if concept not in covered_concepts:
                gaps.append({
                    "concept": concept,
                    "type": "no_questions",
                    "priority": self.concept_graph.get_importance(concept)
                })
            else:
                # 检查题目数量是否充足
                question_count = self.question_bank.count_questions(concept)
                if question_count < 3:  # 少于3题认为覆盖不足
                    gaps.append({
                        "concept": concept,
                        "type": "insufficient_questions",
                        "current_count": question_count,
                        "recommended_count": 5,
                        "priority": self.concept_graph.get_importance(concept)
                    })
        
        # 按优先级排序
        gaps.sort(key=lambda x: x["priority"], reverse=True)
        return gaps
```

### 4.2 覆盖度报告

```
┌─────────────────────────────────────────────────────────────┐
│  题库知识点覆盖分析报告                                     │
│  题库: 分子生物学题库  |  题目总数: 1,250  |  生成时间      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 总体覆盖度                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │   知识点总数: 156    已覆盖: 142    覆盖率: 91.0%    │ │
│  │                                                       │ │
│  │   ████████████████████████████████████████░░░░░ 91%  │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  📈 分类覆盖度                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ DNA复制        ████████████████████████████████ 95%  │ │
│  │ 转录           ██████████████████████████████░░░ 92%  │ │
│  │ 翻译           █████████████████████████████░░░░ 88%  │ │
│  │ 基因调控       ████████████████████████░░░░░░░░░ 75%  │ │
│  │ 分子技术       ████████████████████████████░░░░░ 85%  │ │
│  │ 应用领域       ██████████████████░░░░░░░░░░░░░░░ 65%  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  📊 难度分布                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ L1(基础):  ████████████████ 312题 (25%)              │ │
│  │ L2(简单):  ██████████████████████ 425题 (34%)        │ │
│  │ L3(中等):  ██████████████ 312题 (25%)                │ │
│  │ L4(较难):  ████████ 156题 (12%)                      │ │
│  │ L5(困难):  ████ 45题 (4%)                            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  🔴 覆盖缺口 (14个知识点)                                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 高优先级:                                               │ │
│  │ • 染色质重塑 (核心) - 无题目                           │ │
│  │ • CRISPR脱靶效应 (重要) - 仅1题                        │ │
│  │                                                         │ │
│  │ 中优先级:                                               │ │
│  │ • 三代测序技术 - 无题目                                │ │
│  │ • 合成生物学应用 - 仅2题                               │ │
│  │                                                         │ │
│  │ [查看全部] [生成补题建议]                               │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [导出报告] [生成补题计划]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、智能推荐

### 5.1 推荐策略

```python
class QuestionRecommender:
    """智能题目推荐器"""
    
    def __init__(self, question_bank, user_model):
        self.question_bank = question_bank
        self.user_model = user_model
    
    def recommend(self, user_id: str, strategy: str = "adaptive", 
                  count: int = 10) -> list:
        """
        推荐题目
        
        strategy: 推荐策略
          - adaptive: 自适应难度
          - weak_focus: 薄弱点强化
          - comprehensive: 综合练习
          - exam_simulation: 模拟考试
        """
        if strategy == "adaptive":
            return self._adaptive_recommend(user_id, count)
        elif strategy == "weak_focus":
            return self._weak_focus_recommend(user_id, count)
        elif strategy == "comprehensive":
            return self._comprehensive_recommend(user_id, count)
        elif strategy == "exam_simulation":
            return self._exam_simulation(user_id, count)
    
    def _adaptive_recommend(self, user_id: str, count: int) -> list:
        """
        自适应难度推荐
        根据用户能力动态调整题目难度
        """
        # 获取用户当前能力估计
        ability = self.user_model.estimate_ability(user_id)
        
        # 选择难度与用户能力匹配的题目
        # P(正确)在60-80%的题目
        candidates = []
        for question in self.question_bank:
            prob_correct = self._irt_probability(ability, question.difficulty)
            if 0.6 <= prob_correct <= 0.8:
                candidates.append((question, prob_correct))
        
        # 按信息量和多样性排序
        candidates = self._diversify(candidates, count)
        
        return [q for q, _ in candidates[:count]]
    
    def _weak_focus_recommend(self, user_id: str, count: int) -> list:
        """
        薄弱点强化推荐
        针对掌握度低的知识点推荐题目
        """
        # 获取薄弱知识点
        weak_concepts = self.user_model.get_weak_concepts(user_id)
        
        recommendations = []
        for concept in weak_concepts[:5]:  # 取前5个薄弱点
            # 获取该知识点的题目
            questions = self.question_bank.get_questions(
                concept=concept,
                exclude_answered=True
            )
            
            # 按难度排序（从易到难）
            questions.sort(key=lambda q: q.difficulty_level)
            
            recommendations.extend(questions[:2])  # 每个薄弱点2题
        
        return recommendations[:count]
    
    def _diversify(self, candidates: list, count: int) -> list:
        """
        多样性排序
        确保推荐的题目覆盖不同知识点和认知层次
        """
        selected = []
        concept_coverage = set()
        bloom_coverage = set()
        
        for question, prob in sorted(candidates, key=lambda x: abs(x[1]-0.7)):
            # 优先选择覆盖新知识点和新认知层次的题目
            concept = question.primary_concept
            bloom = question.bloom_level
            
            novelty = 0
            if concept not in concept_coverage:
                novelty += 1
            if bloom not in bloom_coverage:
                novelty += 0.5
            
            if novelty > 0 or len(selected) < count // 2:
                selected.append((question, prob))
                concept_coverage.add(concept)
                bloom_coverage.add(bloom)
            
            if len(selected) >= count:
                break
        
        return selected
```

### 5.2 推荐界面

```
┌─────────────────────────────────────────────────────────────┐
│  智能练习推荐                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 当前状态                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 整体掌握度: 68%  |  今日已练习: 15题  |  正确率: 73% │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  🎯 推荐练习 (共10题，预计20分钟)                          │
│  ═══════════════════════════════════════════════════════   │
│                                                             │
│  基于您的薄弱点推荐:                                        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. [单选] 冈崎片段的形成机制                          │ │
│  │    难度: ⭐⭐  |  知识点: DNA复制 > 复制机制          │ │
│  │    💡 您在该知识点的掌握度为40%，建议加强练习         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 2. [填空] DNA聚合酶的校对功能                         │ │
│  │    难度: ⭐⭐⭐  |  知识点: DNA复制 > 复制酶          │ │
│  │    💡 相关知识点，有助于理解复制准确性                │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 3. [判断] 前导链的合成是连续的                        │ │
│  │    难度: ⭐  |  知识点: DNA复制 > 复制机制            │ │
│  │    💡 基础概念，巩固理解                              │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ... 还有7题 ...                                            │
│                                                             │
│  [开始练习]  [换一批]  [自定义筛选]                         │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  🎮 其他练习模式                                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ [自适应练习] [薄弱点强化] [章节测试] [模拟考试]       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 六、API接口设计

### 6.1 题目管理接口

```yaml
# 创建题目
POST /api/questions
参数:
  content: 题目内容
  answer: 参考答案
  explanation: 解析
  options: 选项(选择题)
  tags: 标签
    - primary_concept: 主要知识点
    - secondary_concepts: 次要知识点
    - bloom_level: 认知层次
    - difficulty: 难度
    - question_type: 题型
返回:
  question_id: 题目ID
  auto_tags: 自动标注结果

# 更新题目标签
PUT /api/questions/{id}/tags
参数:
  tags: 标签更新
返回:
  updated_tags: 更新后的标签

# 批量导入题目
POST /api/questions/batch
参数:
  questions: 题目列表
  auto_tag: 是否自动标注
返回:
  imported_count: 导入数量
  failed_count: 失败数量
  errors: 错误列表
```

### 6.2 标签查询接口

```yaml
# 按标签查询题目
GET /api/questions
参数:
  concept: 知识点ID
  difficulty: 难度(L1-L5)
  bloom_level: 认知层次
  question_type: 题型
  limit: 数量
  offset: 偏移
返回:
  total: 总数
  questions: 题目列表

# 获取题目标签
GET /api/questions/{id}/tags
返回:
  primary_concept: 主要知识点
  secondary_concepts: 次要知识点
  prerequisite_concepts: 前置知识
  bloom_level: 认知层次
  difficulty: 难度
  difficulty_params: 难度参数(IRT)
```

### 6.3 覆盖分析接口

```yaml
# 获取覆盖分析报告
GET /api/coverage/analysis
参数:
  area: 知识领域
返回:
  overall: 总体覆盖度
  by_category: 分类覆盖度
  by_difficulty: 难度分布
  gaps: 覆盖缺口

# 获取补题建议
GET /api/coverage/gaps/recommendations
参数:
  priority: 优先级筛选
返回:
  recommendations: 补题建议列表
    - concept: 知识点
      type: 缺口类型
      recommended_count: 建议题目数
      recommended_difficulties: 建议难度分布
      recommended_bloom: 建议认知层次分布
```

### 6.4 推荐接口

```yaml
# 获取推荐题目
GET /api/questions/recommendations
参数:
  user_id: 用户ID
  strategy: 策略(adaptive|weak_focus|comprehensive|exam)
  count: 数量
  exclude_answered: 排除已答题
返回:
  recommendations: 推荐题目列表
    - question: 题目
      reason: 推荐理由
      expected_difficulty: 预期难度

# 提交答案并获取反馈
POST /api/questions/{id}/submit
参数:
  user_id: 用户ID
  answer: 答案
  time_spent: 用时(秒)
返回:
  correct: 是否正确
  explanation: 解析
  concept_mastery: 知识点掌握度更新
  next_recommendation: 下一题推荐
```

---

## 七、总结

知识点-题库关联系统的核心特性：

1. **多维度标签体系**：知识点标签、认知层次标签、难度标签、题型标签
2. **智能自动标注**：基于NLP的自动标注，提高标注效率
3. **科学难度分级**：基于IRT模型的难度校准，确保难度客观准确
4. **全面覆盖分析**：多维度覆盖度分析，识别题库缺口
5. **个性化推荐**：基于用户能力和薄弱点的智能题目推荐
6. **数据驱动优化**：通过答题数据持续优化题目参数和推荐效果