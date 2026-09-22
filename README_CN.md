# AI Product Copilot

[English](README.md) | **简体中文**

> **AI 提出方案，AI 进行审查，人做最终决策。**

一个 Local-first 的 AI 产品工作流，将模糊的产品想法转化为
**结构化产品分析、显式产品决策，以及经过人工审核的 PRD**。

基于 **Qwen3:8B · Ollama · LangChain · Pydantic · Streamlit** 构建。

![AI Product Copilot](screenshots/v3-01.png)

---

## 🎬 产品 Demo

### 90 秒产品演示

https://github.com/user-attachments/assets/5d24b07e-2d55-48ec-8aab-f8a30b81782c

Demo 展示了一次完整的 AI 辅助产品工作流：

**Define → Analyze → Review → Decide → PRD**

产品经理首先输入一个模糊的产品想法，随后查看 AI 生成的结构化产品分析和质量风险，
做出明确的产品决策，最终生成一份经过人工审核的 PRD。

---

# 产品设计

普通的 LLM 产品需求生成工具通常是：

```text
产品想法
   ↓
  LLM
   ↓
生成 PRD
```

AI Product Copilot 在 AI 生成和最终 PRD 之间增加了
**审查与人工决策机制**：

```text
产品想法
   ↓
结构化 AI 分析
   ↓
AI Quality Review
   ↓
人工产品决策
   ↓
Human-Reviewed PRD
```

这个产品的目标并不是让 AI 自动决定“产品应该怎么做”。

它希望利用 AI 加速产品思考，同时让：

- 假设
- 产品范围
- AI 风险
- 不确定性
- 人工决策

在最终进入 PRD 之前变得更加可见。

---

# 1. Define & Analyze｜定义与分析

产品经理可以从一个并不完整的产品想法开始。

例如：

> 构建一个 AI 简历筛选功能，帮助招聘人员识别与职位描述匹配的候选人。

Qwen3 会将模糊需求转化为结构化产品分析：

- Problem｜核心问题
- Target Users｜目标用户
- User Stories｜用户故事
- MVP Features｜MVP 功能
- Acceptance Criteria｜验收标准
- Risks｜风险
- Assumptions｜假设
- Open Questions｜待验证问题

模型结果不是直接以自由文本返回。

系统使用 **Pydantic Schema** 对 LLM 输出结构进行约束，使结果能够稳定地被应用层读取和展示。

---

# 2. Review & Decide｜审查与决策

第二次 AI 调用会以 Reviewer 的角色审查第一次生成的产品分析。

主要检查：

- Unsupported Metrics｜无依据指标
- Unsupported Assumptions｜无依据假设
- MVP Scope Creep｜MVP 范围膨胀
- AI Risks｜AI 风险
- False Certainty｜错误的确定性表达
- Missing Considerations｜遗漏的重要问题

但这里有一个重要的产品设计原则：

> **AI Reviewer 只是顾问，不是真相裁判。**

产品经理需要进一步查看这些问题，并把 AI 建议转化成明确的产品决策。

![AI Quality Review and Product Decision Workspace](screenshots/v3-02.png)

在简历筛选案例中，产品经理最终决定：

- 移除自动候选人排名和相关性评分
- AI 匹配结果必须提供简历中的支持证据
- 最终候选人 shortlist 由招聘人员决定
- 将候选人隐私作为核心产品风险
- ATS 集成不进入 MVP

这一部分被设计成一个 **Product Decision Workspace（产品决策工作区）**，
而不是让用户继续通过一个大型 Prompt 输入框与 AI 交互。

---

# 3. Generate PRD｜生成经过人工审核的 PRD

最终 PRD 综合四类信息：

```text
原始产品想法
      +
结构化 AI 分析
      +
AI Quality Review
      +
人工产品决策
      ↓
最终 PRD
```

系统还会明确展示：

> **人工审核究竟改变了什么？**

![Human-Reviewed PRD](screenshots/v3-03.png)

### Human Review 前后对比

| AI 初始方案 | 人工审核后的产品决策 |
|---|---|
| 自动候选人排名 | 从 MVP 中移除 |
| Relevance Score | 移除 |
| AI 辅助 shortlist | 招聘人员保留最终决定权 |
| 匹配结果不强制提供证据 | 必须提供支持证据 |
| ATS 集成边界不明确 | 明确排除在 MVP 之外 |
| 隐私问题强调不足 | 明确列为核心产品风险 |

最终 PRD 可以导出为 Markdown 文件。

---

# 为什么做这个项目？

在项目早期测试中，我发现 LLM 可以非常快速地生成一份
**“看起来合理”**的产品需求。

但：

> 看起来合理，不代表产品判断可靠。

例如，模型曾经自行生成这样的 Acceptance Criteria：

```text
80% keyword matching
5-second processing time
```

但原始用户需求并没有提供这些指标，也没有任何：

- 用户研究
- 技术验证
- Benchmark
- 业务数据

能够支持这些数字。

这引出了这个项目真正想探索的问题：

> **如何利用 AI 加速产品需求分析，同时避免 AI 生成的假设在没有验证的情况下悄悄变成产品决策？**

最开始，我尝试通过 Structured Output 解决问题。

但实际测试发现：

**Structured Output 解决了一部分问题，同时暴露出了新的问题。**

---

# 关键 AI 产品设计决策

## 1. Structured Output，而不是 Free-form Generation

第一版 Prototype 直接让 LLM 返回 Markdown。

流程是：

```text
用户需求
   ↓
  Qwen
   ↓
Markdown
```

虽然可以运行，但应用层需要依赖模型不可预测的文本格式。

因此后续改成：

```text
LLM
 ↓
Pydantic Schema
 ↓
Validated Structured Data
 ↓
Application UI
```

例如：

```python
class ProductAnalysis(BaseModel):
    problem: str
    target_users: List[str]
    mvp_features: List[str]
    risks: List[str]
```

这样应用层可以直接读取：

```python
result.problem
result.target_users
result.risks
```

而不是从一整段 Markdown 中解析产品信息。

---

## 2. 结构正确 ≠ 产品判断正确

Pydantic 解决了输出结构稳定性。

但是测试过程中发现，模型仍然可能在一个**完全合法的 Schema** 中生成错误或无依据的内容。

例如：

```json
{
  "acceptance_criteria": [
    "The matching system should achieve 80% accuracy"
  ]
}
```

从 Schema 角度：

```text
✓ acceptance_criteria 存在
✓ 类型是 List
✓ 内容类型是 String
```

结构完全正确。

但是：

```text
80% accuracy
```

并没有任何依据。

因此：

> **Schema Validation 解决的是结构可靠性，而不是语义或产品判断的可靠性。**

这也是 Quality Reviewer 被加入系统的原因。

---

## 3. AI Reviewer 是 Advisor，而不是 Judge

系统增加了第二次 LLM 调用，用于审查第一次生成的产品分析。

但开发过程中出现了一个很有意思的问题：

Reviewer 正确发现了 Generator 编造的 accuracy target，

但随后 Reviewer 自己又建议了一个新的、同样没有依据的数字。

这说明：

```text
Generator 会 hallucinate

Reviewer
也可能 hallucinate
```

所以系统没有采用：

```text
AI Generate
    ↓
AI Review
    ↓
自动应用 Reviewer 建议
```

而是：

```text
AI Generate
    ↓
AI Critique
    ↓
Human Decision
```

Reviewer 的作用是：

> **帮助产品经理发现值得进一步思考的问题。**

而不是：

> **替产品经理决定正确答案。**

---

## 4. Human-in-the-loop 是产品交互，而不是免责声明

很多 AI 产品会在最后写一句：

> AI-generated content should be reviewed by humans.

但在这个项目中，Human Review 本身就是产品 Workflow 的一个步骤。

产品经理可以明确做出：

```text
Remove automated ranking from the MVP.

Require supporting evidence for AI-generated matches.

Keep the final shortlist decision with recruiters.

Treat candidate privacy as a key risk.
```

这些决策随后会作为独立输入进入 PRD Generator。

并且：

> **Human Product Decisions 的优先级高于 AI Reviewer Recommendation。**

因此 Human-in-the-loop 并不是页面底部的一句免责声明，而是实际影响最终产品产物的交互机制。

---

## 5. 为什么没有做成一条完整 Chain？

整个系统并不是一个不可中断的 Sequential Chain。

而是：

```text
Analyze Chain
     ↓
ProductAnalysis

Review Chain
     ↓
QualityReview

Human Decision
     ↓

PRD Generation Chain
     ↓
Final PRD
```

原因是：

### 中间结果本身就是产品功能

`ProductAnalysis` 需要给用户看。

`QualityReview` 也需要给用户看。

产品经理需要基于这些信息做决策，然后系统才能继续生成 PRD。

### 更容易测试和调试

如果最终 PRD 出现问题，可以分别检查：

```text
ProductAnalysis
      ↓
QualityReview
      ↓
Human Decision
      ↓
Final PRD
```

从而定位问题究竟来自哪个阶段。

### 更容易替换模型

未来可以变成：

```text
Analyzer       → Qwen
Reviewer       → Another LLM
PRD Generator  → Another LLM
```

而不需要重写整个产品 Workflow。

### 为什么暂时没有使用 LangGraph？

目前状态流仍然比较简单：

```text
Analyze
   ↓
Review
   ↓
Human Decision
   ↓
Generate PRD
```

因此使用 Python + Streamlit Session State 已经足够。

如果未来加入：

- 条件路由
- 自动 Retry
- Research Agent
- RAG
- Tool Calling
- 多轮 Review
- Dynamic Routing

再迁移到 Graph-based orchestration 会更加合理。

---

# 系统架构

![AI Product Copilot Architecture](docs/architecture.png)

### Product Workflow

```text
                         Product Idea
                              │
                              ▼
                    Requirement Analyzer
                              │
                              ▼
                     ProductAnalysis
                    (Pydantic Schema)
                              │
                              ▼
                     Quality Reviewer
                              │
                              ▼
                       QualityReview
                              │
                              ▼
                    ┌─────────────────┐
                    │  Human Product  │
                    │    Decision     │
                    └────────┬────────┘
                             │
                             ▼
                       PRD Generator
                             │
                             ▼
                         Final PRD
                             │
                             ▼
                      Markdown Export
```

### Local AI Runtime

```text
Streamlit
    ↓
LangChain
    ↓
Ollama
    ↓
Qwen3:8B
```

当前 Prototype 的模型推理完全通过 Ollama 在本地运行。

---

# 技术栈

| Layer | Technology | 用途 |
|---|---|---|
| LLM | Qwen3:8B | 产品分析、Review 和 PRD 生成 |
| Local Inference | Ollama | 本地模型运行 |
| LLM Orchestration | LangChain | Prompt + Model Pipeline |
| Structured Output | Pydantic | 结构化 AI 输出 |
| UI | Streamlit | 产品交互界面 |
| Core Language | Python | 应用逻辑 |

---

# 项目结构

```text
ai-product-copilot/
│
├── app.py
├── README.md
├── README_CN.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── llm.py
│   ├── prompts.py
│   ├── schemas.py
│   └── workflow.py
│
├── docs/
│   └── architecture.png
│
├── screenshots/
│   ├── v3-01.png
│   ├── v3-02.png
│   └── v3-03.png
│
└── sample_data/
```

---

# 本地运行

## 环境要求

- Python 3.10+
- Ollama
- Qwen3:8B

拉取模型：

```bash
ollama pull qwen3:8b
```

Clone：

```bash
git clone https://github.com/Anonymous2127/ai-product-copilot.git
cd ai-product-copilot
```

创建虚拟环境：

```bash
python -m venv .venv
```

Windows PowerShell 激活：

```powershell
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动：

```bash
streamlit run app.py
```

然后打开终端显示的本地 Streamlit 地址。

---

# 当前限制

这个项目目前是一个用于探索 AI-assisted Product Workflow 的 MVP，
而不是生产级 PRD 平台。

当前限制包括：

- AI 生成的产品分析仍可能包含无依据假设。
- Quality Reviewer 本身也是 LLM，因此同样可能产生错误判断。
- Structured Output 可以提高格式可靠性，但不能保证事实正确。
- 如果没有提供真实研究材料，生成的产品需求并没有真实 User Research Grounding。
- 当前 Decision Workspace 使用的是针对 Resume Screening Demo 设计的决策模板。
- 当前 Workflow 尚未从用户访谈、Research Documents 或内部知识库中检索证据。
- 本地模型的推理速度受到设备硬件性能影响。

这些限制也是为什么：

> **Human Review 仍然是整个产品架构的一部分。**

---

# 下一步会做什么？

相比为了展示技术而继续增加 Autonomous Agent，
下一阶段我会优先解决两个问题：

## 1. Evidence-grounded Product Analysis

允许 PM 上传：

- 用户访谈
- Research Notes
- Existing PRD
- Customer Feedback
- Competitive Research

然后通过 RAG：

```text
Research Evidence
       ↓
Retrieval
       ↓
Product Analysis
       ↓
Source Citation
```

让产品需求能够追溯到支持它的真实证据。

## 2. Dynamic Decision Workspace

当前版本使用 Demo-specific Decision Template。

未来可以让：

```text
QualityReview
      ↓
Extract Product Decisions
      ↓
Generate Context-Specific Options
      ↓
PM Accept / Reject / Defer
```

从而让 Decision Workspace 可以适用于不同产品场景。

## 3. Evaluation

构建一个小型 Evaluation Dataset，评估：

- Unsupported Metric Detection
- Unsupported Assumption Detection
- Scope Creep Detection
- Human Instruction Adherence
- PRD Consistency

---

# 产品设计原则

> **AI 应该加速产品思考，而不是悄悄取代产品判断。**

AI Product Copilot 的目标并不是自动生成一份所谓“正确”的 PRD。

它真正希望解决的是：

> **如何让产品经理在获得 AI 效率提升的同时，仍然能够看见并控制假设、风险、不确定性和最终产品决策。**