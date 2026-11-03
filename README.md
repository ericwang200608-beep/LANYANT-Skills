# LANYANT Skills

用于 AI 辅助软件开发与项目交付的技能库。每个技能目录包含 `SKILL.md`，部分附带参考文档、模板和脚本。

## 开始使用

从 [ask-eric](ask-eric/SKILL.md) 开始，描述当前目标、项目现状、完成标准和授权范围。它会选择适用的技能和工作顺序。

也可以直接要求代理读取某个技能的 `SKILL.md` 并执行。使用时保留完整目录结构，供技能读取相邻技能和参考文件。

示例请求：

> 使用 ask-eric，检查当前项目已有资料，完成订单取消功能。验证权限、状态变化和重复请求。允许修改本地代码并运行测试，不推送、不部署。

## 技能目录

| 用途 | 技能 |
| --- | --- |
| 入口与原则 | [ask-eric](ask-eric/SKILL.md)、[engineering-principles](engineering-principles/SKILL.md)、[project-principles](project-principles/SKILL.md) |
| 想法与需求 | [idea-assessment](idea-assessment/SKILL.md)、[business-discovery](business-discovery/SKILL.md)、[decision-mapping](decision-mapping/SKILL.md) |
| 原型与规划 | [workflow-prototype](workflow-prototype/SKILL.md)、[technical-design](technical-design/SKILL.md)、[delivery-planning](delivery-planning/SKILL.md) |
| 环境与开发 | [project-environment](project-environment/SKILL.md)、[feature-implementation](feature-implementation/SKILL.md)、[test-driven-development](test-driven-development/SKILL.md)、[multi-agent-delivery](multi-agent-delivery/SKILL.md) |
| 调查与重构 | [codebase-investigation](codebase-investigation/SKILL.md)、[bug-diagnosis](bug-diagnosis/SKILL.md)、[performance-investigation](performance-investigation/SKILL.md)、[refactoring](refactoring/SKILL.md) |
| 审查与验证 | [code-review](code-review/SKILL.md)、[adversarial-review](adversarial-review/SKILL.md)、[system-verification](system-verification/SKILL.md)、[verification-harness](verification-harness/SKILL.md) |
| 交付与维护 | [pr-delivery](pr-delivery/SKILL.md)、[delivery-proof](delivery-proof/SKILL.md)、[project-release](project-release/SKILL.md)、[project-maintenance](project-maintenance/SKILL.md) |
| 协作与改进 | [issue-triage](issue-triage/SKILL.md)、[session-continuity](session-continuity/SKILL.md)、[technical-writing](technical-writing/SKILL.md)、[process-improvement](process-improvement/SKILL.md) |

## 使用边界

技能之间通过库内相对路径衔接，无需额外安装同名上游技能。Git、Python、Bun、模型检查工具等运行依赖按对应技能的要求准备。扩展管理器、预设管理器及带有占位符的命令是适配示例，执行前需确认真实工具和配置。

## 来源与许可

本库包含整合与改编的材料。各目录保留了原有 `LICENSE` 和版权声明，包括 Matt Pocock、Lauren Tan、DietrichGebert 和 GitHub, Inc. 的署名。使用、修改或再分发时，请遵守对应目录的许可并保留要求的声明。
