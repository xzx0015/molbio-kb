# SKILL 05: 本体构建 — 分子生物学课程知识图谱

> 构建分子生物学课程的 OWL/RDF 本体体系，支持知识检索、学习路径规划和智能教学应用。

---

## 一、本体概览

### 1.1 设计目标

- **概念层次化**：从中心法则到具体机制的完整分类体系
- **学习路径化**：支持基础→进阶→应用的学习轨迹
- **知识关联化**：前置依赖、相关知识点、应用场景的语义关联
- **教学智能化**：支撑自适应学习、薄弱点诊断、题库推荐

### 1.2 核心本体结构

```
MolBioOntology (分子生物学本体)
├── Concept (概念本体) — 知识内容分类
├── LearningPath (学习路径本体) — 学习轨迹与进度
├── Prerequisite (前置依赖本体) — 知识点依赖图谱
├── Assessment (评估本体) — 题目、难度、掌握度
└── User (用户本体) — 学习者画像与状态
```

---

## 二、概念本体 (Concept Ontology)

### 2.1 分类树结构

```
MolBioConcept (分子生物学概念)
├── CentralDogma (中心法则)
│   ├── DNAReplication (DNA复制)
│   │   ├── ReplicationMechanism (复制机制)
│   │   │   ├── SemiConservativeReplication (半保留复制)
│   │   │   ├── ReplicationFork (复制叉)
│   │   │   ├── LeadingStrand (前导链)
│   │   │   ├── LaggingStrand (后随链)
│   │   │   └── OkazakiFragment (冈崎片段)
│   │   ├── ReplicationEnzymes (复制相关酶)
│   │   │   ├── DNAHelicase (解旋酶)
│   │   │   ├── DNAPolymerase (DNA聚合酶)
│   │   │   │   ├── DNAPolymeraseI (DNA聚合酶I)
│   │   │   │   ├── DNAPolymeraseII (DNA聚合酶II)
│   │   │   │   └── DNAPolymeraseIII (DNA聚合酶III)
│   │   │   ├── Primase (引物酶)
│   │   │   ├── DNA Ligase (DNA连接酶)
│   │   │   └── Topoisomerase (拓扑异构酶)
│   │   ├── ReplicationRegulation (复制调控)
│   │   │   ├── OriginOfReplication (复制起点)
│   │   │   ├── ReplicationLicensing (复制许可)
│   │   │   └── CellCycleControl (细胞周期控制)
│   │   └── ReplicationErrors (复制错误与修复)
│   │       ├── MismatchRepair (错配修复)
│   │       ├── NucleotideExcisionRepair (核苷酸切除修复)
│   │       └── BaseExcisionRepair (碱基切除修复)
│   │
│   ├── Transcription (转录)
│   │   ├── TranscriptionMechanism (转录机制)
│   │   │   ├── Initiation (起始)
│   │   │   ├── Elongation (延伸)
│   │   │   └── Termination (终止)
│   │   ├── RNA Polymerase (RNA聚合酶)
│   │   │   ├── RNAPolymeraseI (RNA聚合酶I)
│   │   │   ├── RNAPolymeraseII (RNA聚合酶II)
│   │   │   └── RNAPolymeraseIII (RNA聚合酶III)
│   │   ├── TranscriptionFactors (转录因子)
│   │   │   ├── GeneralTranscriptionFactors (通用转录因子)
│   │   │   │   ├── TFIID (TFIID复合物)
│   │   │   │   ├── TFIIB (TFIIB)
│   │   │   │   └── TFIIF (TFIIF)
│   │   │   └── SpecificTranscriptionFactors (特异性转录因子)
│   │   ├── PostTranscriptionalModification (转录后修饰)
│   │   │   ├── Capping (5'端加帽)
│   │   │   ├── Splicing (剪接)
│   │   │   │   ├── Spliceosome (剪接体)
│   │   │   │   ├── Intron (内含子)
│   │   │   │   └── Exon (外显子)
│   │   │   └── Polyadenylation (多聚腺苷酸化)
│   │   └── RegulationOfTranscription (转录调控)
│   │       ├── OperonModel (操纵子模型)
│   │       ├── LacOperon (乳糖操纵子)
│   │       └── TrpOperon (色氨酸操纵子)
│   │
│   └── Translation (翻译)
│       ├── TranslationMechanism (翻译机制)
│       │   ├── Initiation (起始)
│       │   ├── Elongation (延伸)
│       │   └── Termination (终止)
│       ├── Ribosome (核糖体)
│       │   ├── SmallSubunit (小亚基)
│       │   ├── LargeSubunit (大亚基)
│       │   ├── A Site (A位点)
│       │   ├── P Site (P位点)
│       │   └── E Site (E位点)
│       ├── tRNA (转运RNA)
│       │   ├── Anticodon (反密码子)
│       │   ├── Aminoacylation (氨酰化)
│       │   └── WobbleHypothesis (摆动假说)
│       ├── GeneticCode (遗传密码)
│       │   ├── Codon (密码子)
│       │   ├── StartCodon (起始密码子)
│       │   ├── StopCodon (终止密码子)
│       │   └── Degeneracy (简并性)
│       └── PostTranslationalModification (翻译后修饰)
│           ├── ProteinFolding (蛋白质折叠)
│           ├── Glycosylation (糖基化)
│           └── Phosphorylation (磷酸化)
│
├── GeneExpressionRegulation (基因表达调控)
│   ├── Epigenetics (表观遗传学)
│   │   ├── DNAMethylation (DNA甲基化)
│   │   ├── HistoneModification (组蛋白修饰)
│   │   └── ChromatinRemodeling (染色质重塑)
│   ├── NonCodingRNA (非编码RNA)
│   │   ├── miRNA (微小RNA)
│   │   ├── siRNA (小干扰RNA)
│   │   └── lncRNA (长链非编码RNA)
│   └── SignalTransduction (信号转导)
│       ├── Receptor (受体)
│       ├── SecondMessenger (第二信使)
│       └── TranscriptionFactorActivation (转录因子激活)
│
├── MolecularTechniques (分子生物学技术)
│   ├── PCR (聚合酶链式反应)
│   │   ├── StandardPCR (标准PCR)
│   │   ├── RTPCR (逆转录PCR)
│   │   └── RealTimePCR (实时定量PCR)
│   ├── Electrophoresis (电泳技术)
│   │   ├── GelElectrophoresis (凝胶电泳)
│   │   └── CapillaryElectrophoresis (毛细管电泳)
│   ├── Sequencing (测序技术)
│   │   ├── SangerSequencing (桑格测序)
│   │   ├── NextGenerationSequencing (二代测序)
│   │   └── ThirdGenerationSequencing (三代测序)
│   ├── Cloning (克隆技术)
│   │   ├── RestrictionEnzyme (限制性内切酶)
│   │   ├── Vector (载体)
│   │   └── Transformation (转化)
│   └── CRISPR (基因编辑)
│       ├── Cas9 (Cas9蛋白)
│       ├── gRNA (向导RNA)
│       └── OffTargetEffects (脱靶效应)
│
└── ApplicationDomain (应用领域)
    ├── MedicalApplication (医学应用)
    │   ├── GeneticDisease (遗传病)
    │   ├── CancerBiology (肿瘤生物学)
    │   └── GeneTherapy (基因治疗)
    ├── AgriculturalApplication (农业应用)
    │   ├── GMO (转基因生物)
    │   └── MolecularBreeding (分子育种)
    └── IndustrialApplication (工业应用)
        ├── SyntheticBiology (合成生物学)
        └── Biopharmaceuticals (生物制药)
```

### 2.2 OWL/RDF 表示规范

#### 命名空间

```turtle
@prefix mb: <http://molbio.edu/ontology/2025/1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

#### 类定义示例

```turtle
# 顶层类
mb:CentralDogma a owl:Class ;
    rdfs:label "中心法则"@zh, "Central Dogma"@en ;
    rdfs:comment "分子生物学的核心理论框架，描述遗传信息从DNA到RNA到蛋白质的流动"@zh .

# 子类定义
mb:DNAReplication a owl:Class ;
    rdfs:subClassOf mb:CentralDogma ;
    rdfs:label "DNA复制"@zh, "DNA Replication"@en ;
    rdfs:comment "DNA分子自我复制的过程"@zh .

mb:ReplicationMechanism a owl:Class ;
    rdfs:subClassOf mb:DNAReplication ;
    rdfs:label "复制机制"@zh, "Replication Mechanism"@en .

# 实例定义（具体知识点）
mb:SemiConservativeReplication a mb:ReplicationMechanism ;
    rdfs:label "半保留复制"@zh, "Semi-conservative Replication"@en ;
    rdfs:comment "DNA复制时，每条亲代链作为模板合成新的互补链，形成两个子代DNA分子，每个子代分子包含一条亲代链和一条新链"@zh ;
    mb:hasDifficulty "basic" ;
    mb:estimatedStudyTime "30"^^xsd:integer ;
    mb:hasImportance "core" .
```

### 2.3 属性定义

```turtle
# 数据属性
mb:hasDifficulty a owl:DatatypeProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range xsd:string ;
    rdfs:label "难度等级"@zh ;
    rdfs:comment "知识点的难度等级：basic(基础), intermediate(进阶), advanced(高级)"@zh .

mb:estimatedStudyTime a owl:DatatypeProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range xsd:integer ;
    rdfs:label "建议学习时长(分钟)"@zh .

mb:hasImportance a owl:DatatypeProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range xsd:string ;
    rdfs:label "重要程度"@zh ;
    rdfs:comment "core(核心), important(重要), supplementary(补充)"@zh .

# 对象属性
mb:hasSubConcept a owl:ObjectProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "包含子概念"@zh .

mb:isPartOf a owl:ObjectProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "属于"@zh ;
    owl:inverseOf mb:hasSubConcept .
```

---

## 三、学习路径本体 (Learning Path Ontology)

### 3.1 学习阶段定义

```turtle
mb:LearningStage a owl:Class ;
    rdfs:label "学习阶段"@zh .

mb:FoundationStage a mb:LearningStage ;
    rdfs:label "基础阶段"@zh ;
    rdfs:comment "掌握基本概念和原理"@zh .

mb:IntermediateStage a mb:LearningStage ;
    rdfs:label "进阶阶段"@zh ;
    rdfs:comment "理解机制细节和调控"@zh .

mb:AdvancedStage a mb:LearningStage ;
    rdfs:label "应用阶段"@zh ;
    rdfs:comment "能够应用知识解决问题"@zh .
```

### 3.2 学习路径定义

```turtle
mb:LearningPath a owl:Class ;
    rdfs:label "学习路径"@zh .

mb:hasStage a owl:ObjectProperty ;
    rdfs:domain mb:LearningPath ;
    rdfs:range mb:LearningStage .

mb:hasConcept a owl:ObjectProperty ;
    rdfs:domain mb:LearningStage ;
    rdfs:range mb:MolBioConcept .

# 示例：DNA复制的学习路径
mb:DNAReplicationPath a mb:LearningPath ;
    rdfs:label "DNA复制学习路径"@zh ;
    mb:hasStage mb:DNAReplicationFoundation ;
    mb:hasStage mb:DNAReplicationIntermediate ;
    mb:hasStage mb:DNAReplicationAdvanced .

mb:DNAReplicationFoundation a mb:LearningStage ;
    rdfs:label "DNA复制-基础阶段"@zh ;
    mb:hasConcept mb:SemiConservativeReplication ;
    mb:hasConcept mb:ReplicationFork ;
    mb:hasConcept mb:DNAPolymerase .

mb:DNAReplicationIntermediate a mb:LearningStage ;
    rdfs:label "DNA复制-进阶阶段"@zh ;
    mb:hasConcept mb:LeadingStrand ;
    mb:hasConcept mb:LaggingStrand ;
    mb:hasConcept mb:OkazakiFragment ;
    mb:hasConcept mb:Primase .

mb:DNAReplicationAdvanced a mb:LearningStage ;
    rdfs:label "DNA复制-应用阶段"@zh ;
    mb:hasConcept mb:ReplicationRegulation ;
    mb:hasConcept mb:MismatchRepair .
```

---

## 四、前置依赖本体 (Prerequisite Ontology)

### 4.1 依赖关系定义

```turtle
mb:requires a owl:ObjectProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "前置知识"@zh ;
    rdfs:comment "学习此知识点前必须先掌握的前置知识"@zh .

mb:isPrerequisiteFor a owl:ObjectProperty ;
    rdfs:domain mb:MolBioConcept ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "是...的前置知识"@zh ;
    owl:inverseOf mb:requires .

mb:requiresLevel a owl:DatatypeProperty ;
    rdfs:domain mb:requires ;
    rdfs:range xsd:string ;
    rdfs:label "依赖程度"@zh ;
    rdfs:comment "strong(强依赖), weak(弱依赖), recommended(推荐)"@zh .
```

### 4.2 依赖图谱示例

```
DNA复制
├── 前置：DNA结构 (强依赖)
├── 前置：碱基配对原则 (强依赖)
├── 前置：酶的基本概念 (弱依赖)
└── 是以下知识的前置：
    ├── 复制错误修复 (强依赖)
    ├── PCR技术 (强依赖)
    └── 细胞周期调控 (弱依赖)

转录
├── 前置：DNA结构 (强依赖)
├── 前置：RNA与DNA的区别 (强依赖)
├── 前置：DNA复制 (推荐)
└── 是以下知识的前置：
    ├── 转录调控 (强依赖)
    ├── 转录后修饰 (强依赖)
    └── 翻译 (弱依赖)

翻译
├── 前置：转录 (强依赖)
├── 前置：RNA结构 (强依赖)
├── 前置：遗传密码 (强依赖)
└── 是以下知识的前置：
    ├── 翻译后修饰 (强依赖)
    └── 蛋白质功能 (弱依赖)
```

### 4.3 RDF表示

```turtle
# DNA复制的前置依赖
mb:DNAReplication mb:requires mb:DNAStructure ;
    mb:requiresLevel "strong" .

mb:DNAReplication mb:requires mb:BasePairing ;
    mb:requiresLevel "strong" .

mb:DNAReplication mb:requires mb:EnzymeBasic ;
    mb:requiresLevel "weak" .

# DNA复制是后续知识的前置
mb:MismatchRepair mb:requires mb:DNAReplication ;
    mb:requiresLevel "strong" .

mb:PCR mb:requires mb:DNAReplication ;
    mb:requiresLevel "strong" .
```

---

## 五、评估本体 (Assessment Ontology)

### 5.1 题目类型定义

```turtle
mb:Question a owl:Class ;
    rdfs:label "题目"@zh .

mb:SingleChoice a mb:Question ;
    rdfs:label "单选题"@zh .

mb:MultipleChoice a mb:Question ;
    rdfs:label "多选题"@zh .

mb:FillInBlank a mb:Question ;
    rdfs:label "填空题"@zh .

mb:ShortAnswer a mb:Question ;
    rdfs:label "简答题"@zh .

mb:Calculation a mb:Question ;
    rdfs:label "计算题"@zh .

mb:CaseAnalysis a mb:Question ;
    rdfs:label "案例分析题"@zh .
```

### 5.2 题目属性

```turtle
mb:hasQuestionText a owl:DatatypeProperty ;
    rdfs:domain mb:Question ;
    rdfs:range xsd:string ;
    rdfs:label "题目内容"@zh .

mb:hasAnswer a owl:DatatypeProperty ;
    rdfs:domain mb:Question ;
    rdfs:range xsd:string ;
    rdfs:label "参考答案"@zh .

mb:questionDifficulty a owl:DatatypeProperty ;
    rdfs:domain mb:Question ;
    rdfs:range xsd:string ;
    rdfs:label "题目难度"@zh ;
    rdfs:comment "L1(基础), L2(简单), L3(中等), L4(较难), L5(困难)"@zh .

mb:discriminationIndex a owl:DatatypeProperty ;
    rdfs:domain mb:Question ;
    rdfs:range xsd:float ;
    rdfs:label "区分度"@zh .

mb:testConcept a owl:ObjectProperty ;
    rdfs:domain mb:Question ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "考查知识点"@zh .

mb:requiresConcepts a owl:ObjectProperty ;
    rdfs:domain mb:Question ;
    rdfs:range mb:MolBioConcept ;
    rdfs:label "涉及知识点"@zh .
```

---

## 六、用户本体 (User Ontology)

### 6.1 学习者画像

```turtle
mb:Learner a owl:Class ;
    rdfs:label "学习者"@zh .

mb:hasLearnerProfile a owl:ObjectProperty ;
    rdfs:domain mb:Learner ;
    rdfs:range mb:LearnerProfile .

mb:LearnerProfile a owl:Class ;
    rdfs:label "学习者画像"@zh .

mb:learningStyle a owl:DatatypeProperty ;
    rdfs:domain mb:LearnerProfile ;
    rdfs:range xsd:string ;
    rdfs:label "学习风格"@zh ;
    rdfs:comment "visual(视觉型), auditory(听觉型), kinesthetic(动觉型), reading(阅读型)"@zh .

mb:currentLevel a owl:DatatypeProperty ;
    rdfs:domain mb:LearnerProfile ;
    rdfs:range xsd:string ;
    rdfs:label "当前水平"@zh ;
    rdfs:comment "beginner(初学者), intermediate(中级), advanced(高级)"@zh .
```

### 6.2 学习状态追踪

```turtle
mb:ConceptMastery a owl:Class ;
    rdfs:label "知识点掌握度"@zh .

mb:forConcept a owl:ObjectProperty ;
    rdfs:domain mb:ConceptMastery ;
    rdfs:range mb:MolBioConcept .

mb:masteryLevel a owl:DatatypeProperty ;
    rdfs:domain mb:ConceptMastery ;
    rdfs:range xsd:float ;
    rdfs:label "掌握程度(0-1)"@zh .

mb:lastStudied a owl:DatatypeProperty ;
    rdfs:domain mb:ConceptMastery ;
    rdfs:range xsd:dateTime ;
    rdfs:label "最后学习时间"@zh .

mb:studyCount a owl:DatatypeProperty ;
    rdfs:domain mb:ConceptMastery ;
    rdfs:range xsd:integer ;
    rdfs:label "学习次数"@zh .

mb:testAccuracy a owl:DatatypeProperty ;
    rdfs:domain mb:ConceptMastery ;
    rdfs:range xsd:float ;
    rdfs:label "测试正确率"@zh .
```

---

## 七、完整本体文件结构

```
molbio-ontology/
├── molbio.ttl              # 主本体文件
├── concepts/
│   ├── central_dogma.ttl   # 中心法则概念
│   ├── replication.ttl     # DNA复制概念
│   ├── transcription.ttl   # 转录概念
│   ├── translation.ttl     # 翻译概念
│   ├── regulation.ttl      # 调控概念
│   ├── techniques.ttl      # 技术概念
│   └── applications.ttl    # 应用概念
├── learning/
│   ├── paths.ttl           # 学习路径定义
│   └── stages.ttl          # 学习阶段定义
├── prerequisites/
│   └── dependencies.ttl    # 前置依赖关系
├── assessment/
│   └── question_types.ttl  # 评估相关定义
└── user/
    └── learner.ttl         # 用户相关定义
```

---

## 八、使用示例

### 8.1 SPARQL查询示例

```sparql
# 查询DNA复制的所有子概念
SELECT ?concept ?label
WHERE {
    ?concept rdfs:subClassOf mb:DNAReplication .
    ?concept rdfs:label ?label .
    FILTER(LANG(?label) = "zh")
}

# 查询某知识点的前置知识
SELECT ?prereq ?label ?level
WHERE {
    mb:DNAReplication mb:requires ?prereq .
    OPTIONAL { ?prereq rdfs:label ?label }
    OPTIONAL { mb:DNAReplication mb:requiresLevel ?level }
}

# 查询学习路径中的所有知识点
SELECT ?stage ?concept ?label
WHERE {
    mb:DNAReplicationPath mb:hasStage ?stage .
    ?stage mb:hasConcept ?concept .
    ?concept rdfs:label ?label .
    FILTER(LANG(?label) = "zh")
}
ORDER BY ?stage
```

### 8.2 Python使用示例

```python
from rdflib import Graph, Namespace, RDF, RDFS

# 加载本体
g = Graph()
g.parse("molbio-ontology/molbio.ttl", format="turtle")

MB = Namespace("http://molbio.edu/ontology/2025/1/")

# 获取DNA复制的所有子概念
subconcepts = g.subjects(RDFS.subClassOf, MB.DNAReplication)
for concept in subconcepts:
    label = g.value(concept, RDFS.label, None, default=concept)
    print(f"{concept}: {label}")

# 获取某知识点的前置依赖
prereqs = g.objects(MB.DNAReplication, MB.requires)
for prereq in prereqs:
    label = g.value(prereq, RDFS.label)
    print(f"前置知识: {label}")
```

---

## 九、设计原则总结

1. **自底向上构建**：从具体知识点归纳出类层次，而非从理论推演
2. **中间层最丰富**：顶层（中心法则）过粗，底层（具体酶）过细，中间层（复制机制/复制酶）承载核心分类信息
3. **多重继承支持**：某些概念可属于多个类（如PCR既是技术又涉及复制原理）
4. **依赖关系显式化**：前置知识关系是学习路径规划的核心
5. **教学属性完备**：难度、时长、重要程度等属性支撑智能推荐
6. **可扩展性**：模块化文件结构便于后续添加新概念和应用领域