# quiz/ — Claude Code 運用指示書(Google フォーム小テスト作成キット)

このフォルダは、**教師(オーナー)が Google Apps Script(GAS)で Google フォーム形式の小テストを半自動生成する**ためのキットです。生成物は Google フォーム(quiz mode)で、生徒は通常の Google アカウントから回答します。

ルートの `CLAUDE.md` から「クイズ」「小テスト」「Google フォーム」「GAS」関連の依頼が来たら、本ファイルの指示に従って作業してください。

---

## 1. このツールの位置づけ

### `lectures/` `practices/` との違い

| 観点 | lectures / practices(既存) | **quiz(本ツール)** |
|---|---|---|
| 利用者 | 生徒(投影・自習・演習) | **教師(フォームを作る側)+ 生徒(回答する側)** |
| 成果物 | 単一 HTML(GitHub Pages 公開) | **Google フォーム**(GAS が生成) |
| 公開 URL の役割 | 教材そのもの | **生成キットの説明 + 過去テストへのリンク集** |
| データの正本 | `_source/` の Word/PDF | **`gas/questions.gs` の JS リテラル**(設問・正答・解説) |
| 制作の自動化 | 手作業で HTML を組む | **GAS の `createQuiz()` 一発でフォーム化** |

### 公開 URL

- キットのトップ: `https://mikikof.github.io/mikikof-lab/quiz/`
- 過去テストへの公開リンク(任意): `quiz/index.html` 内に列挙

### 依頼の受け方(キーワード)

ルート CLAUDE.md の振り分けに従って、以下のキーワードでこのツールへ来る:

- 「小テスト」「単元テスト」「Google フォーム」「GAS でフォーム」「クイズ」
- 「採点付きフォームを作って」「N 問の選択式テストを作って」

> **注意**: 「一問一答」「フラッシュカード」のような**HTML 単一ファイルでの生徒向け一問一答**を作る依頼は本ツールではない。新ツールが必要になった時点でフォルダを分ける。現状(2026-05)、`quiz/` は Google フォーム小テスト用に確定運用。

---

## 2. ディレクトリ構成

```
quiz/
├── CLAUDE.md              本ファイル
├── README.md              人間向け使い方(GAS デプロイ手順)
├── index.html             キットのトップ(過去テストへのリンク集にもなる)
├── gas/                   GAS 本体(script.google.com にコピペするソース)
│   ├── createForm.gs      フォームを生成するメイン関数
│   ├── config.gs          テスト設定(タイトル・配点・各種フラグ)
│   └── questions.gs       設問データ(JS オブジェクト直書き)
└── question-bank/         設問の出どころメモ(レビュー用 markdown)
    ├── 04-intellectual-property.md
    ├── 05-personal-information.md
    ├── 06-information-law.md
    └── 07-information-security.md
```

### `gas/*.gs` と `question-bank/*.md` の役割分担

| ファイル | 役割 | 正本性 |
|---|---|---|
| `gas/questions.gs` | フォーム生成の入力。GAS が直接読む | **設問・正答・解説の正本** |
| `question-bank/*.md` | 単元別レビュー用の対応表(Q番号 / 出典項番 / 正答 / 解説) | レビュー補助。`gas/questions.gs` と乖離させない |

**矛盾が発見されたら必ず `gas/questions.gs` の側を正とする**。`question-bank/*.md` は人間レビュー用の控え。両者の更新は同じ commit でセットにすること。

---

## 3. 設問の出どころと検証フロー

### 設問の取り方(本ツールの方針)

各単元から、**既存問題ベース + 各単元 1〜2 問のオリジナル(穴埋め)** を混ぜる:

- **既存問題ベース**: `lectures/_source/学習ノート_問題/` の該当章 Word から、5択化しやすい問いを選ぶ。形式が違うものは 5 択穴埋めに変換
- **オリジナル(穴埋め)**: 各 lecture(`lectures/articles/0X-*/index.html`)の `def-box` 用語定義(学習ノート ① ② … に対応)を「___ に入る語句として正しいものを選べ」形式で 5 択化

### 配分(基本 25 問構成)

| 単元 | 既存ベース | オリジナル | 計 |
|---|---|---|---|
| 04 知的財産権 | 4 | 2 | 6 |
| 05 個人情報 | 4 | 2 | 6 |
| 06 情報社会の法律 | 4 | 2 | 6 |
| 07 情報セキュリティ | 5 | 2 | 7 |
| **計** | **17** | **8** | **25** |

> 配分は標準値。1回のテストで問数や単元構成を変える場合は `gas/config.gs` と `gas/questions.gs` の `unit` フィールドで調整する(設問は順序固定運用なので、`gas/questions.gs` 内の並びを直接変えれば良い)。

### 検証フロー(`lectures/CLAUDE.md` §4.8 §6 [5] と同じ原則)

設問を **1 問書くたびに**:

1. **正答の根拠を `_source/高校情1学習ノート-解答PDF.pdf` の該当ページで Read** して確認
2. 既存問題ベースの場合は、**選択肢の文言を改変したことで正答以外も「もっともらしい正解」になっていないか**を点検
3. オリジナル(lecture 由来)の場合は、`lectures/articles/0X-*/index.html` の **`def-box` 内の定義文と一致**するか確認(独自言い換えで意味がブレてないか)

> **「全問 ✓」の自己報告は信用しない**。Phase 2 着手時は、`question-bank/*.md` のレビュー対応表に「出典(章 p.X 第 N 問 / lec0X 学習ノート ①)」「正答」「解説の根拠フレーム」を全 25 問ぶん書き出し、それを正本 PDF と 1 行ずつ照合する。

---

## 4. GAS 仕様の要点

### `createQuiz()` が立てる Google フォームの状態

- **タイトル / 説明**: `config.gs` で指定
- **クイズモード ON**: `setIsQuiz(true)`
- **メール収集**: `setCollectEmail(true)`
- **1 回のみ回答**: `setLimitOneResponsePerUser(true)`(Google サインイン必須)
- **再回答リンク非表示**: `setShowLinkToRespondAgain(false)`
- **設問順**: 固定(`shuffleQuestions: false` 既定)。単元バランス配分が崩れるためシャッフル無し
- **選択肢順**: ランダム(`shuffleChoices: true` 既定)。コピペ対策で生成時にシャッフル
- **氏名・出席番号**: 設問本体の前に Text item として固定で挿入(必須)
- **配点**: 各 `MultipleChoiceItem.setPoints(4)`(計 100 点)
- **正答 / 解説**: `setFeedbackForCorrect/Incorrect` で「正解: X / 解説: …」を表示

### GAS で API 化されておらず、フォーム UI で手動設定が要るもの

- **「成績を回答後すぐに表示」**: GAS の `FormApp` には API がない。生成後にフォーム編集画面 → 設定 → クイズ → 「成績の表示」を「送信後すぐに表示」へ切替(README.md 手順の §B-3 参照)
- **「正解 / 不正解 / 配点」を回答後に表示するチェック**: 同じ画面の「回答者に表示する内容」3 項目をすべて ON

これは生成スクリプトに含められないので、README で**運用手順として明記**する。

### 既知の制約・注意

- `setLimitOneResponsePerUser(true)` は **回答者が Google アカウントでサインインしている前提**。栄東が Google Workspace でない場合 / 外部公開する場合は機能しない
- `setCollectEmail` は近年 API 名が揺れている。`setCollectEmail(true)` で動かない場合は `setEmailCollectionType(FormApp.EmailCollectionType.VERIFIED)` にフォールバック(README で対処を案内)
- フォームの**フォルダ位置**: 既定では実行ユーザーの My Drive 直下に作成される。整理が必要なら `DriveApp.getFolderById(...).addFile(...)` で移動するヘルパを足す

---

## 5. 標準ワークフロー(新規テスト 1 本)

### [1] 仕様の合意

- 対象単元 / 問数 / 配点 / 公開予定日をユーザーと確定
- 既定(4 単元 / 25 問 / 4 点)から外れる場合は `config.gs` の値も変える

### [2] 設問の準備(Phase 2 相当)

- `_source/学習ノート_問題/` の該当章 Word と `_source/...解答PDF.pdf` を Read
- 各 lecture HTML(`lectures/articles/0X-*/index.html`)の `def-box` を読み、穴埋め化候補を抽出
- `question-bank/0X-*.md` にレビュー用の対応表(Q番号 / 出典 / 正答 / 解説)を起こす
- 内容に合意できたら `gas/questions.gs` に JS オブジェクト形式で転記

### [3] 動作確認(GAS 実行)

- README.md §B の手順で `gas/*.gs` を script.google.com にコピペ
- `createQuiz()` を実行 → 生成された Edit URL を開く
- フォーム UI で「成績を送信後すぐに表示」「正解 / 不正解 / 配点 を表示」を ON にする
- テスト用に自分のアカウントで一度回答してみる(配点 / 解説 / メール収集 / 出席番号バリデーションの確認)

### [4] 公開

- フォームの「送信」ボタンから公開 URL を取得
- `quiz/index.html` の「過去のテスト」セクションに 1 行追加(任意)
- ユーザーに公開 URL を返す

### [5] 振り返り

- 回答結果(スプレッドシート)から、選択肢のばらつきや正答率を確認
- 設問の弱点(正答率が極端に高い / 低い / 選ばれない選択肢)を `question-bank/*.md` に追記し、次回改訂に活かす

---

## 6. 文章トーン

ルート `CLAUDE.md` の「文章トーン」、`column/CLAUDE.md` §7 を本ツールにも適用する。具体的には:

- **設問本文**: 受験で扱う水準の堅さで書く。冗長な「説明的書き出し」は避ける。「次の文の ___ に入る最も適切な語句を、選択肢から 1 つ選びなさい。」のような誘導文は不要(設問の慣例で自明)
- **解説**: 1 問あたり 60〜120 字。条文番号 / 法則名 / 論じ方を明示する。「〜だから当然 X」と言い切らず、根拠(条文・概念)を示す
- **`index.html` のリード文**: 標語調(「〜を。」「〜に。」止め)禁止。ポスター文ではなく事実ベースの平易な一文で書く
- **キャッチー禁止**: 「立体化」「紐解く」「学びのハブ」「深掘り」「凝縮」のたぐいは使わない

---

## 7. Git 運用

コミットプレフィックスは `quiz:` を使う:

```
quiz: Phase 1 ツール枠とサンプル設問を作成
quiz: 第1回小テスト 25問を questions.gs に登録
quiz: 解説の根拠フレームを解答PDF と整合(audit 適用)
```

`gas/questions.gs` と `question-bank/*.md` を別 commit にしないこと(乖離が起きる)。

---

## 8. 困ったとき

- GAS の API 名で迷ったら公式リファレンス(`https://developers.google.com/apps-script/reference/forms`)を確認
- 設問の正答 / 解説で迷ったら独自推論せず、必ず `_source/高校情1学習ノート-解答PDF.pdf` の対応ページを Read で開いて確認(`lectures/CLAUDE.md` §4.8 と同じ原則)
- `setCollectEmail` / `setLimitOneResponsePerUser` の挙動変化は GAS の更新で起きうるので、README.md §C「既知の不具合と対処」を都度更新する
- **公開前に**(任意)`/audit-review` で codex CLI に設問監査を依頼するのも可。設問の正答 / 解説の根拠が原本と整合しているか、第三者の目で点検できる
