# 操作日志

> 按时间线记录所有知识库操作：ingest（摄入新内容）、update（更新已有）、lint（健康检查）、build（构建部署）。  
> 格式：`## [日期] 操作类型 | 描述`  
> 用 `grep "^## \[" log.md | tail -10` 查看最近 10 条。

---

## [2026-05-21] setup | 初始化 index.md + log.md + lint 脚本

- 创建 `index.md`：全局目录，含 8 章节摘要 + 12 实体分类统计
- 创建 `log.md`：操作日志
- 创建 `scripts/lint_wiki.py`：健康检查脚本
- 当前状态：252 实体，5,718 关系，8 章节

---

## [2026-05-08] setup | molbio-kb 记忆重建

- 实体数 162（当时计数），关系 215
- 确认 8 章节结构、build_site.py 的 CHAPTER_NAMES 常量
- 恢复周度文献监测 cron（周一 8:00 → 微信）
