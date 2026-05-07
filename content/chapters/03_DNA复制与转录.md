# 第三章：DNA复制与转录

## 3.1 DNA复制概述

### 半保留复制

<concept id="semiconservative_replication">半保留复制</concept>是DNA复制的核心机制：

```
亲代DNA:    5'-ATGC-3'      3'-TACG-5'
                ↓ 解旋
子代DNA1:   5'-ATGC-3'  +  新合成: 3'-TACG-5'
子代DNA2:   新合成: 5'-ATGC-3'  +  3'-TACG-5'
```

**实验证明**：<entity type="人物">Meselson</entity>和<entity type="人物">Stahl</entity>（1958）的¹⁵N同位素标记实验

### 复制起点与复制叉

| 概念 | 说明 |
|------|------|
| <entity type="概念">复制起点</entity>（Origin） | DNA复制开始的特定序列 |
| <entity type="概念">复制叉</entity>（Replication fork） | Y形结构，双链解开的区域 |
| <entity type="概念">复制子</entity>（Replicon） | 从一个起点复制的DNA单位 |

**原核生物**：通常单一起点（如<entity type="概念">OriC</entity>）
**真核生物**：多个起点，形成<entity type="概念">复制泡</entity>

## 3.2 DNA复制机制

### 复制过程中的关键酶

| 酶 | 功能 | 特点 |
|---|------|------|
| <entity type="酶">解旋酶</entity>（Helicase） | 解开双链 | ATP供能，双向移动 |
| <entity type="酶">单链结合蛋白</entity>（SSB） | 稳定单链 | 防止复性、降解 |
| <entity type="酶">拓扑异构酶</entity> | 缓解超螺旋 | I型切断单链，II型切断双链 |
| <entity type="酶">DNA聚合酶</entity> | 合成新链 | 5'→3'方向，需引物 |
| <entity type="酶">引物酶</entity>（Primase） | 合成RNA引物 | 提供3'-OH末端 |
| <entity type="酶">DNA连接酶</entity> | 连接片段 | 连接Okazaki片段 |

### 前导链与后随链

<concept id="leading_lagging">前导链与后随链</concept>：

- **前导链**（Leading strand）：连续合成，方向与复制叉移动相同
- **后随链**（Lagging strand）：不连续合成，形成<entity type="概念">冈崎片段</entity>

> **半不连续复制**：一条连续，一条不连续

### DNA聚合酶特性

**原核生物**（以<entity type="生物">大肠杆菌</entity>为例）：

| 聚合酶 | 功能 | 特点 |
|--------|------|------|
| <entity type="酶">Pol I</entity> | 修复、切除RNA引物 | 5'→3'外切活性 |
| <entity type="酶">Pol II</entity> | 修复 | SOS修复 |
| <entity type="酶">Pol III</entity> | 主要复制酶 | 高保真、高速度 |

**真核生物**：
- <entity type="酶">Pol α</entity>：合成RNA-DNA引物
- <entity type="酶">Pol δ</entity>：合成后随链
- <entity type="酶">Pol ε</entity>：合成前导链

## 3.3 DNA复制的调控

### 复制起始调控

**原核生物**：
- <entity type="蛋白">DnaA</entity>蛋白结合OriC的9bp重复序列
- ATP-DnaA促进双链解开
- <entity type="蛋白">DnaC</entity>协助<entity type="蛋白">DnaB</entity>解旋酶加载

**真核生物**：
- 复制起点识别复合物<entity type="复合物">ORC</entity>
- <entity type="蛋白">Cdc6</entity>和<entity type="蛋白">Cdt1</entity>招募<entity type="蛋白">MCM</entity>解旋酶
- <entity type="激酶">CDK</entity>和<entity type="激酶">DDK</entity>激酶激活复制起始

### 复制检查点

<concept id="replication_checkpoint">复制检查点</concept>确保DNA完整复制：

- **S期检查点**：监测复制叉进展
- **DNA损伤检查点**：<entity type="激酶">ATM/ATR</entity>激酶通路
- **复制许可**：每轮细胞周期只复制一次

## 3.4 端粒与端粒酶

### 端粒结构

<entity type="结构">端粒</entity>（Telomere）：染色体末端的保护结构

- 序列：人类为<entity type="序列">TTAGGG</entity>重复（5-15 kb）
- 结构：<entity type="结构">T环</entity>（T-loop），3'端回折
- 功能：防止染色体末端被识别为DNA损伤

### 端粒酶

<entity type="酶">端粒酶</entity>（Telomerase）：
- <entity type="复合物">核糖核蛋白</entity>复合物
- <entity type="分子">RNA组分</entity>（<entity type="RNA">TERC</entity>）：模板序列
- <entity type="蛋白">蛋白质组分</entity>（<entity type="蛋白">TERT</entity>）：逆转录酶活性

**机制**：
```
端粒DNA 3'端 → 端粒酶结合 → 以RNA为模板延伸 → 移位 → 重复
```

### 端粒与衰老

**端粒缩短**：
- 正常体细胞：端粒酶活性低，端粒逐代缩短
- <entity type="概念">Hayflick极限</entity>：细胞分裂约50-60次后衰老

**端粒酶与癌症**：
- 85-90%的癌细胞端粒酶重新激活
- 维持端粒长度，获得无限增殖能力

## 3.5 DNA损伤与修复

### 损伤类型

| 诱变剂 | 损伤类型 |
|--------|---------|
| <entity type="诱变剂">UV</entity> | 嘧啶二聚体（CPD、6-4光产物） |
| <entity type="诱变剂">电离辐射</entity> | 双链断裂、碱基氧化 |
| <entity type="诱变剂">烷化剂</entity> | 碱基烷基化 |

### 主要修复机制

**直接修复**：
- <entity type="修复">光修复</entity>：<entity type="酶">光裂合酶</entity>裂解嘧啶二聚体

**切除修复**：
- <entity type="修复">BER</entity>（碱基切除修复）：修复单个损伤碱基
- <entity type="修复">NER</entity>（核苷酸切除修复）：修复大的螺旋扭曲

**双链断裂修复**：
- <entity type="修复">同源重组</entity>（HRR）：高保真，需要同源模板
- <entity type="修复">非同源末端连接</entity>（NHEJ）：易错，不需要模板

## 本章小结

- DNA半保留复制确保遗传信息精确传递
- 复制是半不连续的，需要多种酶协同
- 复制起始受严格调控，确保每周期只复制一次
- 端粒酶维持染色体末端，与衰老和癌症相关
- DNA损伤修复机制维持基因组稳定性

## 思考题

1. 为什么DNA复制需要RNA引物？
2. 前导链和后随链的合成有什么不同？
3. 端粒酶在癌症治疗中有什么潜在应用？

---

## 3.6 转录概述

### 转录的基本概念

<concept id="transcription">转录</concept>：以DNA为模板合成RNA的过程

```
DNA:    3'-TACG-5'  →  RNA:  5'-AUGC-3'
```

**关键特征**：
- 转录不需要引物
- 转录是局部的（基因选择性表达）
- RNA合成后释放，不保持双链
- 只有一条DNA链作为模板（模板链/反义链）

### 转录与复制的比较

| 特征 | DNA复制 | 转录 |
|------|---------|------|
| 模板 | 双链DNA | 单链DNA |
| 产物 | DNA | RNA |
| 引物 | 需要RNA引物 | 不需要 |
| 原料 | dNTPs | NTPs |
| 碱基配对 | A-T, G-C | A-U, G-C |
| 保真性 | 高 | 较低 |

## 3.7 RNA聚合酶

### 原核生物RNA聚合酶

<entity type="酶">RNA聚合酶</entity>组成：
- **核心酶**：α₂ββ'ω（催化活性）
- **全酶**：核心酶 + σ因子（识别启动子）

**σ因子类型**：
| σ因子 | 识别的启动子 | 功能 |
|-------|-------------|------|
| σ⁷⁰ | 管家基因 | 主要σ因子 |
| σ³² | 热休克基因 | 应激反应 |
| σ⁵⁴ | 氮代谢基因 | 特殊代谢 |

### 真核生物RNA聚合酶

| 类型 | 定位 | 产物 | 对α-鹅膏蕈碱敏感性 |
|------|------|------|-------------------|
| <entity type="酶">RNA聚合酶I</entity> | 核仁 | rRNA（除5S） | 不敏感 |
| <entity type="酶">RNA聚合酶II</entity> | 核质 | mRNA、snRNA、miRNA | 高度敏感 |
| <entity type="酶">RNA聚合酶III</entity> | 核质 | tRNA、5S rRNA | 中度敏感 |

**RNA聚合酶II**：
- 最大、最复杂的聚合酶
- 包含12个以上亚基
- 负责蛋白质编码基因的转录

## 3.8 转录过程

### 起始阶段

**原核生物**：
1. **启动子识别**：σ因子识别-10区（TATAAT）和-35区（TTGACA）
2. **闭合复合物形成**：RNA聚合酶结合双链DNA
3. **开放复合物形成**：DNA解旋约14bp
4. **起始合成**：合成前10个核苷酸，σ因子释放

**真核生物**：
1. **启动子元件**：
   - <entity type="概念">TATA盒</entity>（-25至-30）：核心元件
   - <entity type="概念">起始子</entity>（Inr）：转录起始位点
   - <entity type="概念">上游激活序列</entity>（UAS）

2. **通用转录因子**（GTFs）：
   | 因子 | 功能 |
   |------|------|
   | TFIID | 识别TATA盒（含TBP） |
   | TFIIB | 桥接TFIID和RNA聚合酶II |
   | TFIIF | 招募RNA聚合酶II |
   | TFIIE | 招募TFIIH |
   | TFIIH | 解旋酶活性，启动子逃逸 |

### 延伸阶段

- RNA聚合酶沿DNA模板移动（3'→5'方向）
- RNA链以5'→3'方向合成
- 形成DNA-RNA杂合双链（约8-9bp）
- 拓扑异构酶缓解超螺旋

### 终止阶段

**原核生物**：
- **ρ因子非依赖终止**：发夹结构 + poly-U序列
- **ρ因子依赖终止**：ρ蛋白解旋酶活性

**真核生物**：
- <entity type="概念">poly(A)信号</entity>（AAUAAA）：切割和加尾信号
- <entity type="概念">终止子</entity>：转录终止序列
- 转录终止与3'端加工偶联

## 3.9 原核生物转录调控

### 操纵子模型

<concept id="operon">操纵子</concept>（Operon）是原核生物基因调控的基本单位：

```
启动子 - 操纵基因 - 结构基因群
   ↑         ↑
RNA聚合酶  阻遏蛋白
```

| 元件 | 功能 |
|------|------|
| <entity type="概念">启动子</entity> | RNA聚合酶结合位点 |
| <entity type="概念">操纵基因</entity>（Operator） | 阻遏蛋白结合位点 |
| <entity type="概念">结构基因</entity> | 编码功能蛋白 |
| <entity type="概念">调节基因</entity> | 编码调控蛋白 |

### 乳糖操纵子

<entity type="概念">乳糖操纵子</entity>（Lac operon）：

**负调控**（阻遏）：
- 无乳糖时：<entity type="蛋白">阻遏蛋白</entity>结合操纵基因，转录关闭
- 有乳糖时：乳糖作为<entity type="分子">诱导物</entity>，阻遏蛋白失活，转录开启

**正调控**（激活）：
- 葡萄糖缺乏时：<entity type="分子">cAMP</entity>升高，<entity type="蛋白">CAP蛋白</entity>（catabolite activator protein）激活转录
- 葡萄糖存在时：cAMP水平低，CAP不结合，转录水平低

### 色氨酸操纵子

<entity type="概念">色氨酸操纵子</entity>（Trp operon）：

**阻遏型操纵子**：
- 无色氨酸时：转录开启
- 有色氨酸时：色氨酸作为<entity type="分子">辅阻遏物</entity>，阻遏蛋白激活，转录关闭

**衰减作用**（Attenuation）：
- 前导序列含有4个可互补配对的区域
- 前导肽的翻译影响转录终止
- 转录-翻译偶联的精细调控机制

## 3.10 真核生物转录调控

### 顺式作用元件

<concept id="cis_element">顺式作用元件</concept>：DNA上的调控序列

| 元件 | 位置 | 功能 |
|------|------|------|
| <entity type="概念">启动子</entity> | 转录起始点附近 | 基础转录装置组装 |
| <entity type="概念">增强子</entity>（Enhancer） | 远端（1kb-1Mb） | 显著增强转录效率 |
| <entity type="概念">沉默子</entity>（Silencer） | 远端 | 抑制转录 |
| <entity type="概念">绝缘子</entity>（Insulator） | 边界 | 阻断增强子/沉默子作用 |

### 反式作用因子

<concept id="trans_factor">反式作用因子</concept>：调控蛋白

**转录因子结构域**：
- <entity type="结构">DNA结合域</entity>：识别特定序列
- <entity type="结构">转录激活域</entity>：招募转录 machinery
- <entity type="结构">二聚化结构域</entity>：形成同源/异源二聚体

**常见DNA结合域**：
| 结构域 | 特征 | 代表因子 |
|--------|------|---------|
| <entity type="结构">同源异型域</entity> | 螺旋-转角-螺旋变体 | HOX蛋白 |
| <entity type="结构">锌指</entity> | Zn²⁺稳定 | SP1、TFIIIA |
| <entity type="结构">碱性亮氨酸拉链</entity> | bZIP二聚化 | AP-1、CREB |
| <entity type="结构">螺旋-环-螺旋</entity> | HLH二聚化 | MyoD、E47 |

### 染色质与转录

**核小体与转录**：
- 核小体阻碍RNA聚合酶前进
- <entity type="复合物">染色质重塑复合物</entity>（SWI/SNF等）协助核小体滑动

**组蛋白修饰**：
- <entity type="修饰">H3K4me3</entity>：激活转录标记
- <entity type="修饰">H3K27me3</entity>：抑制转录标记
- <entity type="修饰">组蛋白乙酰化</entity>：通常激活转录

## 3.11 RNA加工

### 5'端加帽

<entity type="修饰">5'帽结构</entity>：
- 结构：m⁷G(5')ppp(5')N
- 酶：<entity type="酶">鸟苷酰转移酶</entity>
- 功能：保护mRNA、促进翻译起始、参与mRNA输出

### 3'端加尾

<entity type="修饰">poly(A)尾</entity>：
- 长度：100-250个腺苷酸
- 酶：<entity type="酶">poly(A)聚合酶</entity>
- 功能：稳定mRNA、促进翻译、调控降解

### RNA剪接

**剪接过程**：
- 切除<entity type="概念">内含子</entity>，连接<entity type="概念">外显子</entity>
- <entity type="复合物">剪接体</entity>（spliceosome）执行
- 涉及snRNP（U1、U2、U4/U6、U5）

**选择性剪接**：
- 一个基因产生多种mRNA异构体
- 人类约95%的基因存在选择性剪接
- 增加蛋白质组多样性

## 本章小结

- 转录以DNA为模板合成RNA，不需引物
- 原核生物一个RNA聚合酶，真核生物有三种
- 转录分起始、延伸、终止三个阶段
- 原核生物以操纵子为单位进行调控
- 真核生物通过顺式元件和反式因子精细调控
- RNA加工（加帽、加尾、剪接）是真核mRNA成熟的关键步骤

## 思考题

1. 为什么真核生物需要三种RNA聚合酶？
2. 比较乳糖操纵子和色氨酸操纵子的调控机制。
3. 选择性剪接有什么生物学意义？
