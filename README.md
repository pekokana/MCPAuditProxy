# MCP Audit Proxy

*MCP向け 監査・説明責任プロキシ*


## MCP Audit Proxy とは(What is MCP Audit Proxy?)


### 日本語
MCP Audit Proxy は、Model Context Protocol (MCP) を利用した AI ツール連携において、
**「誰が・いつ・何を要求し・何が返されたか」** を
改ざん不能な形で記録するための監査・統制向けプロキシです。

本プロジェクトは以下を目的としています。

- AI と社内データのやり取りを「説明可能」にする
- 個人情報を保存せずに監査証跡を残す
- 事後改ざん・否認を技術的に不可能にする

詳細な設計思想・イベント定義・法務観点は [docs/](/docs) を参照してください。

### English

MCP Audit Proxy is a governance-focused proxy for MCP-based AI systems,
designed to provide **accountability, traceability, and tamper-evident audit logs**
without storing raw sensitive data.

This project aims to:

- Make AI interactions auditable and explainable
- Prevent repudiation through cryptographic hash chains
- Support legal and compliance requirements by design

For detailed architecture and audit design, see the [docs/](/docs) directory.




## なぜ MCP Audit Proxy が必要なのか(Why MCP Audit Proxy is needed)


### 日本語

MCP は柔軟で拡張性の高い AI 連携を可能にしますが、
以下のような **統制・責任の定義を持っていません**。

* AI が生成したレスポンスの最終責任は誰が持つのか
* リクエスト／レスポンスが改ざんされていないことをどう証明するのか
* ログが本当に「嘘をついていない」と言えるのか
* 監査・法的調査にどう対応するのか

これらが定義されていない限り、
MCP を **業務システムや規制環境で使うのは難しい**のが現実です。


### English
While MCP enables flexible and extensible AI integrations,
it does **not define governance or accountability**, such as:

* Who is responsible for an AI-generated response
* How request/response integrity can be proven
* Whether logs can detect tampering
* How audit or legal investigations can be supported

Without these guarantees, MCP is difficult to adopt
in enterprise, compliance, or regulated environments.


## 設計目標(Design Goals)


### 日本語
* MCP通信に対する **改ざん検知可能な監査ログ**を提供する
* AIレスポンスの **最終責任点（Final Responsibility Point）** を明確にする
* 監査・コンプライアンス・インシデント調査を支援する
* 個人情報・機密情報の露出を最小化する
* 既存の MCP クライアント／サーバと互換性を保つ


### English
* Provide tamper-evident audit logs for MCP interactions
* Define a clear *final responsibility point* for AI responses
* Support legal audit, compliance, and incident investigation
* Minimize exposure of personal or sensitive information
* Remain compatible with existing MCP clients and servers




## 中核概念：説明責任の境界としての Proxy(Core Concept: Proxy as Accountability Boundary)

### 日本語

この Proxy は単なる中継サーバではありません。

以下を定義する **説明責任の境界** です。

* MCP リクエストを「正式に受理した」地点
* MCP レスポンスを「確定させて返却した」地点
* そのレスポンスに対する責任が成立する地点

Proxy は
「何が要求され、何が返され、いつ行われたか」
の **唯一の信頼できる記録点** になります。

内部動作や監査イベントの考え方については、
[Conceptual Overview](docs/concepts.md) を参照してください。

### English
This proxy is not just a network relay.

It defines the boundary where:

* An MCP request is formally accepted
* An MCP response is finalized and delivered
* Responsibility for that response is established

The proxy becomes the **single source of truth**
for what was requested, what was answered, and when.

For a conceptual explanation of how MCP Audit Proxy works internally,
see [Conceptual Overview](docs/concepts.md).

## イベントベース監査チェーン(Event-based Audit Chain)

### 日本語
各 MCP 通信は、複数の **監査イベント** として記録され、
それらは **暗号学的ハッシュチェーン** によって連結されます。

代表的なイベント例：

* `request_received`（要求受信）
* `response_received`（上流サーバ応答受信）
* `response_sent`（応答送信・最終責任点）
* `error_occurred`（エラー発生）

過去ログの改ざんは **必ず検知可能** です。

### English
Each MCP interaction is recorded as a sequence of audit events,
linked using a cryptographic hash chain.

Typical events include:

* `request_received`
* `response_received`
* `response_sent` (final responsibility point)
* `error_occurred`

Any modification of past events can be detected.


## 法務・コンプライアンス観点(Legal & Compliance Perspective)

### 日本語
本プロジェクトは以下を前提に設計します。

* 監査人が読める証跡の生成
* ロールベースアクセス制御（RBAC）
* 個人情報と監査証跡の分離
* 削除要求（GDPR / 個人情報保護法）への対応

**「後付けのログ」ではなく、最初から監査前提**です。

### English
This project explicitly considers:

* Auditor-readable evidence generation
* Role-based access control (RBAC)
* Separation of personal data and audit proofs
* Compliance with deletion requests (GDPR / privacy laws)

Auditability is treated as a **first-class requirement**,
not an afterthought.


## プロジェクト状況(Project Status)

### 日本語

本リポジトリは現在、以下を中心に進めています。

* 設計ドキュメント
* JSON Schema 定義
* アーキテクチャ図
* 最小構成の PoC 実装

**設計が先、実装は後**です。

### English
This repository currently focuses on:

* Design documentation
* JSON Schema definitions
* Architecture diagrams
* Minimal proof-of-concept implementation

Implementation follows design, not the other way around.


## やらないこと(Non-Goals)

### 日本語
* MCP サーバの置き換えは目的ではありません
* AIの品質評価は行いません
* フル機能のログ基盤（SIEM）を目指しません


### English
* This is not a replacement for MCP servers
* This does not evaluate AI output quality
* This is not a full SIEM or logging platform


## License

TBD (likely Apache-2.0 or MIT)

