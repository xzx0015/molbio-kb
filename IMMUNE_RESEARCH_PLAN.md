# Phase 1 免疫线研究方案 v2.0 — 计算驱动

> **核心问题**：WGD 产生的免疫基因冗余如何催生先天免疫的功能创新？
> **策略**：85% 公共数据挖掘 + 15% 关键实验验证
> **对标论文**：*BMC Biology* (2025) 草鱼 IFNf / *Fish Shellfish Immunol* (2026) 草鱼 NF-κB

---

## 零、公共数据资源摸底

### 已确认可用

| 资源 | 规模 | 用途 |
|------|------|------|
| **SRA RNA-seq** | **1,826 个草鱼数据集** | 表达图谱 + 病原响应 + 共表达网络 |
| 其中 GCRV 攻毒 | 259 个 | 抗病毒响应时间序列 |
| 其中细菌/LPS | 45+ 个 | 抗菌免疫 |
| **T2T 基因组** | 无缺口 (2025) | 全基因组基因鉴定 |
| **斑马鱼对照** | 数千个公开数据集 | 一轮 WGD 参照系 |
| **鲤/鲫/鲢基因组** | 多个近缘种已测序 | 鲤科内比较 |

### 可快速获取

| 资源 | 方法 |
|------|------|
| 草鱼 vs 斑马鱼同源基因对 | Ensembl Compara / OrthoFinder |
| 编码区 dN/dS | PAML codeml 批量计算 |
| 启动子序列 | T2T 基因组 ±2kb upstream 提取 |
| 转录因子结合位点预测 | JASPAR 数据库 + FIMO 扫描 |
| 蛋白质结构预测 | AlphaFold3 / ColabFold |

---

## 一、计算管线（四条并行线）

### Pipeline 1：免疫基因全基因组鉴定与进化分析

**对标论文**：*BMC Biology* (2025) PMID 40619370 — IFNf；*Fish Shellfish Immunol* (2026) PMID 41903594 — NF-κB

**方法**：

```bash
# 步骤1: 基因家族鉴定
以斑马鱼已知免疫基因为 query → tblastn 草鱼 T2T 基因组
→ 提取 hit 区域 → 基因预测 (Augustus) → 结构域验证 (InterProScan)

# 步骤2: 系统发育树 + 共线性
Muscle 比对 → IQ-TREE 建树 → MCScanX 共线性
→ 区分 WGD 来源 (ohnolog) vs 串联重复 vs 反转录转座

# 步骤3: 选择压力
PAML codeml: branch-site model (branch A: 草鱼特异拷贝)
→ 检测正向选择位点 (dN/dS > 1)
```

**目标基因家族**（按优先级）：

| 优先级 | 基因家族 | 预期 | 斑马鱼拷贝数 | 草鱼预测拷贝数 |
|--------|---------|------|------------|-------------|
| **P0** | I 型 IFN | 已确认 8 种 | ~4 | 8 ✓ |
| **P0** | IRF 家族 | IRF1-10，重点 IRF3/IRF7 | ~9 | 预测 13-15 |
| **P1** | TLR 家族 | TLR1-22 | ~19 | 预测 25-30 |
| **P1** | RLR (RIG-I/MDA5/LGP2) | 病毒感知 | 3 | 预测 5-6 |
| **P1** | NLR 家族 | 胞内病原感知 | ~200 | 预测 250-300 |
| **P2** | cGAS-STING 轴 | 胞质 DNA 感知 | 2 | 预测 3-4 |
| **P2** | 负调控因子 (SIRT, SOCS, DUSP) | 免疫刹车 | ~30 | 预测 40-50 |

**产出**：一份草鱼先天免疫基因目录，标注每个基因的 WGD 来源、拷贝数、选择压力证据。

---

### Pipeline 2：公共 RNA-seq 元分析 → 功能推断

**对标论文**：*Front Immunol* (2024) PMID 39606227 — DUSP 在黄颡鱼中的全基因组表达分析

**方法**：

```bash
# 步骤1: SRA 数据批量下载 + 统一处理
从 1,826 个草鱼 SRA 数据集中筛选质量合格的
→ fastq-dump → Salmon 定量 (T2T 基因组索引)
→ 259 个 GCRV 攻毒数据集 + 100+ 个组织面板 + 50+ 个发育时间序列

# 步骤2: 组织表达图谱
合并所有对照组 RNA-seq → 构建 12 组织 × 基因表达矩阵
→ 聚类分析 (WGCNA)
→ 识别组织特异表达模块
→ 标注 WGD 来源的旁系同源基因对的表达域分化

# 步骤3: GCRV 响应时间序列
259 个 GCRV 数据 → 按时间点 (0/6/12/24/48/72h) 和 组织 (脾/肾/肝/鳃)
→ DESeq2 差异分析
→ 构建 基因-时间-组织 三维响应矩阵
→ 比较 WGD 旁系同源对的响应动力学差异

# 步骤4: 抗菌 vs 抗病毒比较
GCRV 数据 + 细菌攻毒数据 → 对比分析
→ 哪些 IFN/IRF 拷贝选择性响应病毒 vs 细菌？
```

**产出**：草鱼免疫基因在**真实病原挑战**下的功能图谱（基于已发表数据，零实验成本）。

---

### Pipeline 3：共表达网络 → 通路架构推断

**方法**：

```bash
# 步骤1: 加权基因共表达网络 (WGCNA)
全组织 RNA-seq → WGCNA → 识别共表达模块
→ 每个模块关联到通路 (KEGG/GO 富集)
→ 标注 WGD 旁系同源对是否在同一或不同模块

# 步骤2: 条件特异性网络
GCRV 攻毒前后各时间点 → 分别构建网络
→ 对比网络拓扑变化
→ 识别 WGD 拷贝间"条件性互斥"或"协同激活"

# 步骤3: 斑马鱼平行分析
斑马鱼公共 RNA-seq → 同样流程
→ 比较两种鱼的免疫网络架构
→ 回答：WGD 后的免疫网络是"更大"（更多节点），还是"更复杂"（不同的连接模式）？
```

**产出**：草鱼 vs 斑马鱼先天免疫网络的比较架构图，揭示 WGD 如何重塑通路结构。

---

### Pipeline 4：启动子进化 → 调控分歧推断

**方法**：

```bash
# 步骤1: 启动子提取
每个免疫基因 ±2kb upstream → 从 T2T 基因组提取
→ WGD 旁系同源对的启动子多序列比对

# 步骤2: 转录因子结合位点预测
JASPAR 2024 鱼类/脊椎动物矩阵 → FIMO 扫描所有启动子
→ 统计 WGD 旁系同源对之间共享/独特的 TFBS

# 步骤3: cis-regulatory 元件获得/丢失
比较草鱼特异的 IRF/NF-κB 结合位点在旁系同源对中的分布
→ 检测哪个拷贝获得了新的调控元件
```

**产出**：WGD 后 cis-regulatory divergence 的系统图谱——哪些免疫基因拷贝通过启动子重编程获得新功能。

---

## 三、最少湿实验验证（15%）

四条计算管线完成后，挑选 **3-5 个最强候选**进行实验验证：

| 实验 | 目的 | 工作量 |
|------|------|--------|
| **qPCR 验证** 关键基因的组织表达和 GCRV 响应 | 验证 RNA-seq 推断 | 2 周 |
| **双荧光素酶报告** 验证候选启动子的功能差异 | 验证 Pipeline 4 的 cis-regulatory 预测 | 3 周 |
| **1 个 CRISPR 敲除** 最关键的 IRF/IFN 拷贝 | 功能性验证 | 2 个月 |
| **1 次 GCRV 攻毒 + RNA-seq** (如果公共数据不足) | 补充时间点精度不够的数据 | 1 个月 |

---

## 四、论文产出路线（计算优先）

### Paper 1（12 个月）：草鱼先天免疫基因目录 + 进化分析

> **对标**：*BMC Biology* (2025) 草鱼 IFNf / *Fish Shellfish Immunol* (2026) 草鱼 NF-κB

| 章节 | 内容 | 数据来源 |
|------|------|---------|
| 全基因组鉴定 | 10+ 免疫基因家族系统鉴定 | Pipeline 1 |
| 系统发育 + 共线性 | WGD vs 串联重复 vs 反转座 | Pipeline 1 |
| 选择压力 | 正向选择位点 + 分支模型 | Pipeline 1 |
| 组织表达图谱 | 全组织 RNA-seq 元分析 | Pipeline 2 |
| GCRV 响应全景 | 259 数据集时间序列 | Pipeline 2 |
| 靶刊 | *BMC Biology* / *Genome Biology* / *Mol Biol Evol* |

### Paper 2（18 个月）：WGD 拷贝的功能分工——以 IRF/IFN 为核心的表达-调控网络

> **对标**：*Front Immunol* (2024) DUSP / *IJMS* (2024) Sirtuin 扩张

| 章节 | 内容 | 数据来源 |
|------|------|---------|
| WGD 旁系同源对的表达域分化 | 10 组织 × 时间序列 | Pipeline 2 |
| 共表达网络 | 条件特异性模块 | Pipeline 3 |
| 启动子 cis-regulatory divergence | TFBS 获得/丢失 | Pipeline 4 |
| 关键实验验证 | qPCR + 双荧光素酶 + 1 个 CRISPR KO | 湿实验 |
| 靶刊 | *PLoS Genetics* / *Mol Biol Evol* / *eLife* |

### Paper 3（24 个月）：旗舰——WGD 驱动的先天免疫网络复杂性演化

| 章节 | 内容 | 数据来源 |
|------|------|---------|
| 草鱼 vs 斑马鱼全免疫网络比较 | 架构差异定量 | Pipeline 3 |
| WGD 产生了"模块化免疫"？ | 条件特异性通路配置 | Pipeline 2+3 |
| 进化约束 vs 新功能化 | dN/dS + 表达 + 表型 | Pipeline 1+2+4 |
| 靶刊 | *Nature Ecology & Evolution* / *Science Advances* |

---

## 五、参考模板论文（2024-2026）

| PMID | 期刊 | 年份 | 标题 | 可借鉴 |
|------|------|------|------|--------|
| **40619370** | *BMC Biology* | 2025 | Genome-wide identification of IFN complex establishes IFNf in Cypriniformes | **黄金模板** — 同物种 + 同方法 |
| **41903594** | *Fish Shellfish Immunol* | 2026 | NF-κB family genome-wide identification in grass carp | 同物种 — 证明了"全基因组鉴定"模式可行 |
| **39606227** | *Front Immunol* | 2024 | DUSP genome-wide characterization in yellow catfish | 表达分析模板 |
| **38892461** | *IJMS* | 2024 | Sirtuin gene family expansion in gilthead sea bream | **SIRT3/SIRT7 的直接对标** |
| **39102972** | *Fish Shellfish Immunol* | 2024 | p62/SQSTM1 inhibits TBK1-IRF7 in triploid fish | 三倍体鱼免疫 — WGD 背景共鸣 |
| **38430414** | *Nat Ecol Evol* | 2024 | Gene retention patterns after WGD | 理论框架 |

---

## 六、时间线（计算驱动版）

```
Month 1-2: Pipeline 1 — 全基因组免疫基因鉴定
           → 产出: 草鱼免疫基因完整目录 (10+ 基因家族)

Month 3-4: Pipeline 2 — SRA 数据批量处理 + 表达矩阵
           → 产出: 全组织表达图谱 + GCRV 时间序列

Month 5-6: Pipeline 1+2 整合 → Paper 1 初稿
           → 选择压力 + 表达图谱 → 投 BMC Biology

Month 7-9: Pipeline 3 — 共表达网络 + 斑马鱼比较
           → 产出: 免疫网络比较架构

Month 10-12: Pipeline 4 — 启动子进化分析
            → 产出: cis-regulatory divergence 图谱

Month 13-15: Pipeline 2+3+4 整合 → Paper 2 初稿
            → 表达-调控-网络整合 → 投 PLoS Genetics / eLife

Month 16-18: 关键湿实验验证 (qPCR + 双荧光素酶报告 + 1 CRISPR)
            → 补充 Paper 1 和 Paper 2 的修订实验

Month 19-24: Pipeline 1-4 全整合 → Paper 3
            → 旗舰论文: WGD → 免疫网络复杂性
```

---

## 七、起步操作（Month 1，本周可做）

1. **下载 T2T 基因组** + 注释文件
2. **编写基因家族鉴定脚本** (以下为第一个目标)：
   - 斑马鱼 IRF1-10 蛋白序列 → tblastn 草鱼基因组
   - 提取 + Augustus 基因预测 + InterProScan
   - 比对 + IQ-TREE 建树
   - MCScanX 共线性分析区分 WGD vs 串联复制
3. **批量下载 259 个 GCRV SRA 数据的 metadata**
   - 按时间点、组织、测序平台分类
   - 评估直接可用性
4. **输出第一份数据**：草鱼 IRF 家族拷贝数、系统发育位置、WGD 来源

---

*本方案的核心优势：前 12 个月几乎不需要湿实验，基于公共数据即可产出 1-2 篇论文。*
