# MCP Audit Proxy – Conceptual Overview
（MCP Audit Proxy 概念説明）



## 1. MCP Audit Proxyで何が起きているのか(What Happens Inside MCP Audit Proxy?)

### 日本語

MCP Audit Proxy は、**1回の MCP ツール呼び出し**に対して、
内部的には次のような 1 往復の通信を仲介します。

```
[ MCP Client ]
  |
  | (JSON-RPC Request)
  v
[ MCP Audit Proxy ]
  |
  | (Forward)
  v
[ Real MCP Server ]
  |
  | (JSON-RPC Response)
  v
[ MCP Audit Proxy ]
  |
  | (Return)
  v
[ MCP Client ]
```

この **1 往復の中で何が起きたのか** を、
後から第三者（監査人・法務・管理者）が
**嘘なく説明できるようにする**ことが、この Proxy の目的です。

---

### English

For a single MCP tool invocation, the MCP Audit Proxy mediates
a single request–response round trip:

```
[ MCP Client ]
  |
  | (JSON-RPC Request)
  v
[ MCP Audit Proxy ]
  |
  | (Forward)
  v
[ Real MCP Server ]
  |
  | (JSON-RPC Response)
  v
[ MCP Audit Proxy ]
  |
  | (Return)
  v
[ MCP Client ]
```


The purpose of the proxy is to ensure that **what actually happened**
during this round trip can be explained truthfully
to auditors, legal teams, and system owners.



## 2. 「監査的に意味のある瞬間」とは何か(What Are Audit-Meaningful Moments?)

### 日本語

監査人が後から知りたいことは、実は多くありません。

| 監査の問い | 意味 |
|-----------|------|
| 本当に要求は来たのか？ | 捏造防止 |
| 実際に外部へ送ったのか？ | 情報流出確認 |
| 結果として何を返したのか？ | 被害範囲特定 |

これらの問いに答えるために必要なのは、
**通信のすべて**ではなく、
**責任が確定する瞬間**だけです。

> この「否定できない瞬間」を **監査イベント（Audit Event）** と呼びます。

---

### English

Auditors typically need answers to only a few core questions:

| Audit Question | Meaning |
|---------------|---------|
| Did the request really exist? | Anti-forgery |
| Did data leave the boundary? | Data exposure |
| What was ultimately returned? | Impact analysis |

To answer these, we do not need full traffic logs.
We only need **moments where accountability is established**.

> These moments are called **Audit Events**.



## 3. なぜ「ログ」ではなく「イベント」なのか(Why Events Instead of Raw Logs?)

### 日本語

通常のログには次の問題があります。

* 量が多すぎて人が読めない
* 後から削除・改ざんできてしまう
* 「どこが責任点か」が分からない

MCP Audit Proxy は、
**後から否定されたら困る事実だけ**を
**順序付き・改ざん不能**に残します。


### English

Traditional logs often suffer from:

* Excessive volume
* Weak tamper resistance
* Unclear accountability points

MCP Audit Proxy records only **non-deniable facts**
and links them using a cryptographic hash chain.


## 4. Proxyは「説明責任の境界」である(Proxy as an Accountability Boundary)

### 日本語

この Proxy は単なる中継サーバではありません。

ここで次のことが確定します。

* MCP リクエストを「正式に受理した」地点
* MCP レスポンスを「確定させて返却した」地点
* そのレスポンスに対する責任が成立する地点

Proxy は  
**「何が・いつ・誰に渡ったか」**の  
**唯一の信頼できる記録点**になります。


### English

This proxy is not just a relay.

It defines the boundary where:

* Requests are formally accepted
* Responses are finalized
* Responsibility is established

It becomes the **single source of truth**
for MCP interactions.



## 5. イベントはチェーンとして記録される(Event-Based Hash Chain)

### 日本語

各 MCP 通信は、複数の監査イベントとして記録され、
それらは暗号学的ハッシュチェーンで連結されます。

これにより：

* 過去イベントの改ざんは検知可能
* イベントの順序が保証される
* 否認が技術的に困難になる


### English

Each MCP interaction is recorded as a sequence of audit events,
linked via a cryptographic hash chain.

This ensures:

* Tamper detection
* Event ordering
* Non-repudiation


## 6. 次に読むべきもの(Where to Go Next)

### 日本語

次のドキュメントでは、
**具体的にどのイベントが存在するのか**を定義します。

> [Audit Events Definition](docs/audit-events.md)


### English

The next document defines **which audit events exist**
and what each one means.

> [Audit Events Definition](docs/audit-events.md)

