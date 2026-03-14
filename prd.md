# 原理图 Agent 系统 PRD

# 0  原始需求（口语转录版）


我们正在做agent 绘制原理图的开发。

## 流程是这样的：

Phase0: 用户和agent进行多轮对话，明确需求。这里需要agent 进行类似“scan" 的流程。注意，很多时候用户都会陷入 X-Y problem，即用户想做的是x,但是用户自己想了一个方案是 Y，而这个方案事实上并不好。因此这个阶段一定要帮助用户完成需求澄清、电气参数、输入输出、系统功能和设计约束等的评估。需要通过复述方法来确保agent  正确理解了用户的意图
Phase1: Agent 为用户设计实现方案。 交付之前启动 sub-agent  在干净的上下文中反复互相 review
Phase2: Agent  开始器件选型。这个阶段， Agent 需要使用网络工具搜索和对比需求的器件。并做出整体的选型。此阶段可以用并行 agent。选定器件过程中可能需要阅读和下载大量的datasheet pdf. 选定后删除无关的  pdf
Phase 3: Agent 深度阅读pdf，理解各个器件，总结一份 md 形式的设计手册。
Phase4: Agent 阅读各个器件的设计手册和需求文档，完成 json 形式的原理图互连设计。
Phase5: 将原理图设计喂给渲染器，渲染原理图。

## 预计会需要的依赖：

+ 主应用： Claude Code, OpenClaw
+ Skills: Web_Search, Browser Use, PDF, clawhub
+ 其他：无头浏览器， 原理图渲染引擎

## 需要的准则：

+ git based：显式要求使用 git 管理原理图工程
+ 文件落盘： 需求、计划、datasheet、绘制手册、设计、原理图文件等都需要落盘保存。并实时维护一个 Project_index
+ multi-agent:  需要隔离上下文的多  agent，只共享需求、当前任务，对彼此进行审查和修正。

## review 

1 你的“入口 skill 必须做的 7 件事” 中前三件事实上可以脚本化。没必要浪费token 2 同样是直接附带一份安装脚本就好 3 我们也可以提供脚本一键初始化项目。这样最节省token 4 状态机我们可以用 hooks? 5 skill 的模式 agent 应该可以通过状态机自己控制。 6 状态机最简单的实现就是用一个文件来存 7 change request要做，但你的流程问题本来是因为前期选型没选好，这本来就不应该出现 8 结构审查我们直接上脚本 9  我们直接留一个 make file  入口，到时候  agent 和用户都可以轻松调用脚本


## 1. 文档目的

本文档用于定义一个面向原理图设计任务的 Agent 系统产品需求。该系统的目标是：

1. 接收用户的自然语言需求。
2. 通过分阶段流程完成需求澄清、方案设计、器件选型、PDF 阅读、互连设计与原理图渲染。
3. 以文件为真源，以状态机驱动流程，以脚本完成确定性工作，以 Skill 完成高层决策与调度。
4. 最终输出可审查、可追溯、可回滚的原理图工程。

本文档只描述已确认的需求与设计原则，不额外扩展未确认功能。

---

## 2. 产品目标

### 2.1 核心目标

构建一套用于“Agent 绘制原理图”的工程化系统，具备以下能力：

1. 单入口调用。
2. 自动初始化项目。
3. 自动安装项目所需依赖。
4. 按阶段推进设计流程。
5. 支持多 Agent 协作与审查。
6. 所有关键产物均落盘保存。
7. 使用 git 管理工程。
8. 使用状态文件驱动流程。
9. 使用脚本与 hooks 实现低 token、确定性执行。

### 2.2 非目标

以下内容不在本版 PRD 范围内：

1. 不定义具体 GUI。
2. 不定义具体原理图渲染引擎内部实现。
3. 不定义具体 PCB 布局功能。
4. 不定义云端任务调度系统。
5. 不定义复杂数据库或服务端状态管理。

---

## 3. 用户与使用方式

### 3.1 目标用户

本系统面向以下使用者：

1. 希望通过 Agent 辅助完成原理图设计的工程用户。
2. 希望将原理图设计流程工程化、可复用化的开发者。
3. 希望将该系统作为上层 Agent 能力包调用的自动化系统。

### 3.2 使用入口

系统对用户与 Agent 提供统一入口：

* `Makefile`

用户和 Agent 均应优先通过 `make` 命令调用系统，而不是手工执行分散脚本。

---

## 4. 总体设计原则

本系统必须遵守以下原则：

### 4.1 Skill 只负责高层决策与调度

Skill 的职责仅包括：

1. 读取当前状态。
2. 判断当前所处阶段。
3. 选择对应阶段规则与 Agent 模板。
4. 执行需要推理、判断、抽象的任务。
5. 调用脚本、hooks、review 流程。

Skill 不负责：

1. 目录检查。
2. 环境安装。
3. 项目初始化。
4. 文件结构校验。
5. 状态迁移底层执行。

上述工作必须由脚本承担。

### 4.2 脚本负责确定性执行

脚本用于承担低 token、可重复、可验证的工作，包括但不限于：

1. 环境检查。
2. 依赖安装。
3. 项目初始化。
4. 状态读取。
5. 状态迁移。
6. 文件结构校验。
7. schema 校验。
8. 项目索引更新。
9. git checkpoint。

### 4.3 状态文件是流程真源

系统必须使用单独状态文件记录当前流程状态。

建议文件：

* `state.yaml`

该文件用于表达：

1. 当前 phase。
2. 当前任务状态。
3. 是否阻塞。
4. 待处理审查项。
5. 当前是否允许迁移到下一阶段。

### 4.4 项目索引文件是资产真源

系统必须使用单独索引文件记录项目产物与路径。

建议文件：

* `project_index.yaml`

该文件用于表达：

1. 已生成的文档。
2. 已生成的设计文件。
3. 已批准器件。
4. 已下载 datasheet。
5. 当前有效产物路径。

### 4.5 hooks 只负责守门，不作为状态机本体

hooks 可用于：

1. 执行 pre-check。
2. 执行 post-check。
3. 拦截非法阶段迁移。
4. 自动执行 validate。
5. 自动执行 checkpoint。

hooks 不负责保存完整状态机逻辑。状态机逻辑必须由状态文件和迁移脚本共同实现。

### 4.6 所有关键产物必须落盘

以下内容必须写入文件，而不能只存在聊天上下文中：

1. 需求文档。
2. 约束文档。
3. 开放问题。
4. 方案文档。
5. 器件选型结果。
6. datasheet 资产。
7. 器件设计手册。
8. 互连设计 JSON。
9. 渲染结果。
10. review 结果。
11. change request。

### 4.7 git 是强制要求

系统必须使用 git 管理项目工程。

git 用于：

1. 记录阶段性结果。
2. 支持回滚。
3. 支持 diff 审查。
4. 支持 review 后 checkpoint。

---

## 5. 系统分层

系统必须拆分为以下五层：

### 5.1 统一入口层

* `Makefile`

职责：

1. 提供统一命令入口。
2. 屏蔽底层脚本细节。
3. 供用户和 Agent 共同调用。

### 5.2 确定性执行层

* `scripts/*.sh`
* `scripts/*.py`

职责：

1. 执行环境准备。
2. 初始化项目。
3. 读取和更新状态。
4. 运行校验与迁移。
5. 维护索引。

### 5.3 流程控制层

* `state.yaml`
* `hooks/*`

职责：

1. 保存当前流程状态。
2. 限制非法迁移。
3. 在关键时机触发校验。

### 5.4 智能决策层

* `SKILL.md`
* `phases/*.md`
* `agents/*.md`

职责：

1. 做需求澄清。
2. 做设计权衡。
3. 做器件比较。
4. 做 PDF 理解。
5. 做互连设计。
6. 调用 review agent。

### 5.5 项目资产层

包含但不限于：

* `spec/`
* `architecture/`
* `sourcing/`
* `handbook/`
* `design/`
* `render/`
* `review/`

职责：

1. 保存各阶段产物。
2. 保存中间结果与最终结果。
3. 保存审查记录与变更记录。

---

## 6. 核心流程

系统应按照以下 phase 工作：

1. Phase0：需求澄清
2. Phase1：方案设计
3. Phase2：器件选型
4. Phase3：PDF 深读与设计手册生成
5. Phase4：JSON 互连设计
6. Phase5：原理图渲染

### 6.1 Phase0：需求澄清

目标：

将用户自然语言需求整理为结构化需求文档。

必须完成：

1. 识别用户真实目标。
2. 识别 X-Y problem。
3. 澄清电气参数。
4. 澄清输入输出。
5. 澄清系统功能。
6. 澄清设计约束。
7. 通过复述确认 Agent 理解无误。

输出文件至少包括：

* `spec/requirements.md`
* `spec/constraints.md`
* `spec/open_questions.md`
* `spec/assumptions.md`

### 6.2 Phase1：方案设计

目标：

根据需求文档形成系统实现方案。

必须完成：

1. 系统模块划分。
2. 功能边界定义。
3. 关键接口设计。
4. 风险点识别。
5. review agent 反复审查。

输出文件至少包括：

* `architecture/system_overview.md`
* `architecture/interface_matrix.md`
* `architecture/risk_register.md`

### 6.3 Phase2：器件选型

目标：

通过网络工具搜索、对比并确定器件方案。

必须完成：

1. 搜索候选器件。
2. 对比候选器件。
3. 选择最终器件。
4. 下载相关 datasheet PDF。
5. 保留有效 datasheet 资产。
6. 删除无关 PDF。

本阶段可使用并行 Agent。

输出文件至少包括：

* `sourcing/candidate_parts.csv`
* `sourcing/approved_parts.yaml`
* `sourcing/selection_notes.md`
* `sourcing/datasheets/`

### 6.4 Phase3：PDF 深读与设计手册生成

目标：

对选定器件进行深度阅读，并形成器件设计手册。

必须完成：

1. 阅读 datasheet。
2. 理解供电、时钟、复位、接口、保护与约束。
3. 总结成 md 形式设计手册。

输出文件至少包括：

* `handbook/*.md`

### 6.5 Phase4：JSON 互连设计

目标：

基于需求文档和器件设计手册，输出结构化原理图互连设计。

必须完成：

1. 阅读需求文档。
2. 阅读设计手册。
3. 生成 JSON 形式互连设计。

输出文件至少包括：

* `design/interconnect.json`
* `design/design_notes.md`

### 6.6 Phase5：原理图渲染

目标：

将 JSON 互连设计输入渲染器，生成原理图文件。

必须完成：

1. 调用渲染器。
2. 产出渲染结果。
3. 记录渲染日志。

输出文件至少包括：

* `render/schematic_output/*`
* `render/render_log.md`

---

## 7. 多 Agent 协作要求

系统必须支持多 Agent，且多 Agent 必须隔离上下文。

### 7.1 多 Agent 共享内容

多 Agent 仅共享：

1. 当前需求。
2. 当前任务。
3. 当前阶段所需输入文件。

### 7.2 多 Agent 不共享内容

多 Agent 不应共享完整长上下文，不应共享无关阶段的冗余信息。

### 7.3 多 Agent 用途

多 Agent 主要用于：

1. 方案审查。
2. 选型并行对比。
3. review 与修正。

### 7.4 审查要求

在交付前必须启动 sub-agent，在隔离上下文中反复 review。

---

## 8. Skill 设计要求

### 8.1 入口 Skill

系统必须提供单文件 Skill 入口，作为 Agent 的统一调用入口。

入口 Skill 的职责仅包括：

1. 调用状态读取逻辑。
2. 判断当前 phase。
3. 加载对应阶段规则。
4. 调用对应 Agent 模板。
5. 在关键节点调用脚本、validate、review、checkpoint。

入口 Skill 不负责目录初始化、安装依赖、底层迁移与校验逻辑。

### 8.2 阶段 Skill

系统应按 phase 提供独立规则文件，供入口 Skill 按阶段读取。

建议包括：

* `phases/phase0.md`
* `phases/phase1.md`
* `phases/phase2.md`
* `phases/phase3.md`
* `phases/phase4.md`
* `phases/phase5.md`

### 8.3 Agent 模板

系统应提供各类 Agent 模板，用于规范不同 Agent 行为。

建议包括：

* `agents/clarifier.md`
* `agents/architect.md`
* `agents/sourcer.md`
* `agents/reviewer.md`

---

## 9. 状态机要求

### 9.1 状态机实现方式

状态机必须通过单一状态文件实现。

建议文件：

* `state.yaml`

### 9.2 状态机控制方式

Agent 应通过读取状态文件自主控制流程，而不是依赖额外模式切换。

### 9.3 状态迁移实现

状态迁移必须由脚本实现，不应仅通过 Skill 文本控制。

建议脚本：

* `scripts/transition.py`

### 9.4 hooks 与状态机关系

hooks 可用于状态迁移前后守门，但 hooks 不是状态机本体。

---

## 10. 脚本与 Makefile 要求

### 10.1 Makefile 作为统一入口

系统必须提供 `Makefile`，供用户和 Agent 调用。

### 10.2 Makefile 最小能力

至少应支持以下目标：

* `make bootstrap`
* `make init`
* `make status`
* `make validate`
* `make review`
* `make checkpoint`
* `make phase0`
* `make phase1`
* `make phase2`
* `make phase3`
* `make phase4`
* `make phase5`
* `make render`

### 10.3 脚本范围

脚本至少应覆盖以下能力：

1. 检查环境。
2. 安装依赖。
3. 初始化项目。
4. 读取状态。
5. 执行状态迁移。
6. 执行结构审查。
7. 更新项目索引。
8. 执行 git checkpoint。

---

## 11. 依赖与初始化要求

### 11.1 依赖安装

系统应提供安装脚本，而不是让 Skill 消耗 token 解释安装过程。

建议至少提供：

* `scripts/bootstrap.sh`

### 11.2 项目初始化

系统应提供一键初始化脚本，而不是让 Skill 手工创建项目结构。

建议至少提供：

* `scripts/init_project.sh`

### 11.3 初始化内容

初始化项目时至少生成：

1. 标准目录结构。
2. `state.yaml`
3. `project_index.yaml`
4. `Makefile`
5. `.gitignore`
6. 模板文档。
7. git 仓库。

---

## 12. 文件与目录要求

项目至少应包含如下目录：

```text
spec/
architecture/
sourcing/
handbook/
design/
render/
review/
scripts/
hooks/
phases/
agents/
```

项目至少应包含如下关键文件：

* `state.yaml`
* `project_index.yaml`
* `Makefile`
* `SKILL.md`

---

## 13. 审查与校验要求

### 13.1 结构审查

结构审查必须由脚本执行，而不是依赖 Agent。

结构审查应包括：

1. 文件是否存在。
2. 文件结构是否完整。
3. schema 是否通过。
4. 当前阶段产物是否齐全。
5. 状态文件与索引文件是否更新。

### 13.2 语义审查

语义审查由 Agent 执行。

语义审查应关注：

1. 需求理解是否准确。
2. 方案是否合理。
3. 选型是否合理。
4. 风险是否遗漏。
5. 输出是否自洽。

### 13.3 review 执行时机

每阶段完成后都必须进行 validate 与 review，再决定是否进入下一阶段。

---

## 14. Change Request 要求

系统必须支持 Change Request。

### 14.1 Change Request 的目的

用于记录流程中的显式变更，而不是依赖隐式修改旧文件。

### 14.2 Change Request 触发场景

当已有阶段结论需要回退、修改或重做时，应创建 Change Request。

### 14.3 Change Request 落盘形式

建议保存在：

* `review/change_requests/`

每个 Change Request 必须至少记录：

1. 触发原因。
2. 受影响阶段。
3. 受影响文件。
4. 建议动作。
5. 当前状态。

---

## 15. git 管理要求

系统必须基于 git 管理工程。

### 15.1 使用要求

每个关键阶段完成后，应执行 checkpoint。

### 15.2 checkpoint 触发时机

建议在以下时机触发：

1. 初始化完成后。
2. 每个 phase validate 通过后。
3. 每个 review 通过后。
4. 每次重要 Change Request 应用后。

---

## 16. 示例项目与模板要求

系统应提供：

1. 各类 Agent 模板。
2. 各阶段规则模板。
3. 项目初始化模板。
4. 示例项目结构。

模板与示例项目的目的：

1. 降低 Agent 初始实现成本。
2. 规范输出结构。
3. 为后续扩展提供基线。

---

## 17. 最小可用版本范围

本系统第一版最小可用范围应优先覆盖以下内容：

1. 单入口 Skill。
2. `Makefile`。
3. `state.yaml`。
4. 项目初始化脚本。
5. 依赖安装脚本。
6. Phase0。
7. Phase1。
8. review 机制。
9. validate 机制。
10. git checkpoint。
11. 一个示例项目。

---

## 18. 验收标准

若系统满足以下条件，则视为满足本版 PRD：

1. 用户或 Agent 可以通过统一入口初始化项目。
2. 系统可自动生成标准工程结构。
3. 系统可通过 `state.yaml` 驱动 phase 流程。
4. Skill 只承担调度与高层决策。
5. 确定性任务由脚本执行。
6. 每个阶段产物可落盘保存。
7. 每个阶段可 validate、review、checkpoint。
8. 多 Agent 可在隔离上下文中协作。
9. 系统支持 Change Request。
10. 项目全程由 git 管理。

---

## 19. 附录：术语

### Skill

用于高层决策、调度与阶段控制的 Agent 能力入口。

### hook

在关键节点执行的自动守门逻辑。

### state.yaml

用于保存当前流程状态的状态文件。

### project_index.yaml

用于保存项目资产索引的索引文件。

### checkpoint

一次 git 阶段性提交。

### Change Request

对既有阶段结论进行显式变更的记录文件。
