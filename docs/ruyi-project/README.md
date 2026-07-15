# RuyiDify 项目文档

> **目的**：为人类和 AI 提供项目架构、配置、知识库链路和验证记录的统一参考。
> **维护原则**：所有文档带时间戳，AI 先读 `.metadata.yaml` 判断时效，再决定是否深入源码。

---

## 📖 文档导航

| 序号 | 文档 | 内容 | 最后更新 | 状态 |
|:----:|------|------|:--------:|:----:|
| 0 | [.metadata.yaml](.metadata.yaml) | 机器可读元数据（AI 入口） | 2026-07-15 | ✅ |
| 1 | [01-architecture.md](01-architecture.md) | 项目定位、技术栈、目录职责、运行架构 | 2026-07-15 | ✅ |
| 2 | [02-configuration.md](02-configuration.md) | 所有配置文件、环境变量、作用说明 | 2026-07-15 | ✅ |
| 3 | [03-knowledge-base.md](03-knowledge-base.md) | 知识库端到端链路：数据模型→索引→检索→问答 | 2026-07-15 | ✅ |
| 4 | [04-examples-catalog.md](04-examples-catalog.md) | 29 个示例脚本分类与学习要点 | 2026-07-15 | ✅ |
| 5 | [05-startup-guide.md](05-startup-guide.md) | 全部启动方式审查：Docker/Make/dev 脚本 | 2026-07-15 | ✅ |
| 6 | [06-knowledge-api-reference.md](06-knowledge-api-reference.md) | 知识库 API 参考（37+ 端点，7 大类） | 2026-07-15 | ✅ |

## 🧪 验证报告

| 日期 | 报告 | 范围 | 结果 |
|:--------:|------|------|:----:|
| 2026-07-15 | [verification/2026-07-15-docker-compose.md](verification/2026-07-15-docker-compose.md) | Docker 环境 + API 健康检查 + Console CRUD | ✅ 11/11 通过 |

## 📝 变更记录

见 [CHANGELOG.md](CHANGELOG.md)

---

## 🤖 给 AI 的阅读指引

1. **先读** `.metadata.yaml` — 判断文档时效和已知 bug
2. **如果距今 > 30 天** 或代码有重大变更 → 建议重新全量分析
3. **如果距今 7–30 天** → 读 01–04 文档，按需定点验证
4. **如果距今 < 7 天** → 直接读目标文档即可

---

## 📂 目录规范

```
docs/ruyi-project/
├── README.md                  ← 你在这里
├── .metadata.yaml             ← 机器可读元数据
├── 01-architecture.md         ← 架构分析
├── 02-configuration.md        ← 配置参考
├── 03-knowledge-base.md       ← 知识库链路
├── 04-examples-catalog.md     ← 示例目录
├── CHANGELOG.md               ← 变更记录
└── verification/              ← 验证报告（按日期命名）
    └── YYYY-MM-DD-<topic>.md
```

**命名规则**：
- 主题文档：`NN-主题名.md`（数字前缀表示推荐阅读顺序）
- 验证报告：`verification/YYYY-MM-DD-主题.md`
- 所有文档顶部必须包含 `> 最后更新: YYYY-MM-DD` 和 `> 源码分析日期: YYYY-MM-DD`

**维护规则**：
- 新增验证 → 在 `verification/` 下新建文件，更新 `.metadata.yaml`
- 发现新 bug → 更新 `.metadata.yaml` 的 `known_issues`
- 修复 bug → 更新状态为 `closed`，记录修复日期
- 重新分析源码 → 更新 `.metadata.yaml` 的 `last_source_analysis`
