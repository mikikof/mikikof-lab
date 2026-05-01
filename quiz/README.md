# Google フォーム小テスト作成キット

GAS(Google Apps Script)で、情報Ⅰ の小テストを Google フォームとして自動生成するキットです。

設問・正答・解説は `gas/questions.gs` に JS オブジェクトとして定義。`createQuiz()` を実行すると、25 問・100 点・選択肢シャッフルありの Google フォームが立ち上がります。

---

## 仕様(既定)

- **問数**: 25 問
- **配点**: 1 問 4 点(計 100 点)
- **形式**: 5 択選択(空欄穴埋めを含む)
- **氏名・出席番号**: 設問本体の前に必須項目として収集
- **メール収集**: ON(Google アカウントから自動取得)
- **回答制限**: 1 アカウント 1 回まで(サインイン必須)
- **設問順**: 固定(単元バランスを保つため)
- **選択肢順**: 生成時にランダムシャッフル
- **正答 / 解説**: 回答送信後に表示

---

## A. 初回セットアップ

### A-1. Google Apps Script プロジェクトを作る

1. ブラウザで <https://script.google.com/> を開く
2. 「**新しいプロジェクト**」をクリック
3. プロジェクト名を「mikikof-lab quiz」など分かりやすい名前に変更

### A-2. 既定の `Code.gs` を消す

- 左サイドバー「ファイル」→ `Code.gs` の右の「⋮」→ 「**ファイルを削除**」

### A-3. 3 つのファイルを作って中身を貼る

左サイドバー「ファイル」→ 「+」 → **スクリプト** で以下 3 つを順に作成し、本リポジトリの内容をそのままコピペする:

| 作成するファイル名 | コピペ元 |
|---|---|
| `config` | `gas/config.gs` |
| `questions` | `gas/questions.gs` |
| `createForm` | `gas/createForm.gs` |

> GAS のファイル名に `.gs` を入れる必要はない(自動で付く)。

### A-4. Drive の権限を許可

1. 上部の「実行する関数」を `createQuiz` に切り替え
2. 「実行」ボタンを押す
3. 初回のみ「権限の確認」が出る → アカウントを選択 →「詳細」→「(プロジェクト名) に移動(安全ではないページ)」→「許可」

これで GAS が Drive 上にフォームを作る権限を取得します。以降、`createQuiz()` を実行するだけでフォームが生成されます。

---

## B. テストを 1 本作る

### B-1. 設問を入れ替える(初回 / 改訂時)

1. 本リポジトリで `gas/questions.gs` を編集 — 25 問の設問・正答・解説を確定
2. `gas/config.gs` を編集 — タイトル(例: `情報I 小テスト 第1回`)、説明、公開予定日などを設定
3. 編集後の中身を、GAS エディタの該当ファイルに**全文コピペで上書き**
4. ⌘S(or Ctrl+S)で保存

### B-2. 実行してフォームを生成

1. 上部の「実行する関数」を `createQuiz` に
2. 「実行」をクリック
3. 下部「実行ログ」に `Edit URL: https://docs.google.com/forms/d/.../edit` が出力される
4. その URL をブラウザで開く

### B-3. ⚠ フォーム編集画面で**必ず手動切替**する設定

GAS の API では切り替えられない設定があります。フォームを開いたら以下を必ず実施:

1. 右上「設定」タブ
2. 「**テストにする**」セクションの中:
   - 「成績の表示」 → **「送信直後」** に切替
   - 「回答者が見ることのできる項目」 → 以下 3 つすべて ON:
     - **間違えた質問**
     - **正解**
     - **点数**

これをやらないと、正解・解説・点数が**回答者にすぐに表示されない**(教師が手動公開するまで非表示のまま)。

### B-4. 自分で 1 回試す

1. フォーム右上「目のアイコン(プレビュー)」で実回答画面を開く
2. 自分の Google アカウントで適当に回答 → 送信
3. 確認:
   - メールアドレスが収集されているか
   - 氏名・出席番号が必須項目になっているか
   - 解説と点数が送信直後に表示されるか
   - 同じアカウントで再度開くと「すでに回答済」になるか

問題があれば `gas/*.gs` を直して **GAS エディタに再コピペ → 再実行**(古いフォームは Drive から削除して OK)。

### B-5. 生徒に公開

1. フォーム右上「**送信**」ボタン
2. リンクタブで短縮 URL を取得 → 配布
3. 必要なら本リポジトリの `quiz/index.html` の「過去のテスト」一覧にも追記

---

## C. 既知の不具合と対処

### メール収集モードについて

既定は **Verified モード**: サインイン済み Google アカウントから自動取得する。回答者が手入力する欄は出ず、組織アカウント等のメールが確実に記録される。

`gas/createForm.gs` は次の分岐で動く:

```javascript
if (typeof FormApp.EmailCollectionType !== 'undefined') {
  form.setEmailCollectionType(FormApp.EmailCollectionType.VERIFIED);
} else {
  form.setCollectEmail(true);  // 古い GAS 環境のフォールバック(手入力欄)
}
```

`FormApp.EmailCollectionType` が未定義の古い環境では旧 API にフォールバックし、その場合は**回答者がメールアドレスを手入力**する形になる。新しい GAS 環境では Verified が自動で選択される。

### 任意収集 (RESPONDER_INPUT) に切り替えたい場合

「サインインしていない外部の生徒も受験させたい」など、Verified 制限を外したい場合は `createForm.gs` を以下に変更:

```javascript
form.setEmailCollectionType(FormApp.EmailCollectionType.RESPONDER_INPUT);
```

ただしこの場合、`setLimitOneResponsePerUser(true)` の 1 回制限は機能しなくなる。

### `setLimitOneResponsePerUser` が効かない(複数回回答できる)

これは API の不具合ではなく仕様: 回答者が Google アカウントでサインインしていない場合、この制限は機能しない。**フォーム側の「サインインを必須にする」設定**(設定 > 全般 > 「回答を 1 回に制限する」)が ON になっているか確認。

栄東高校で Google Workspace を使っている場合は、上記設定で ON にすれば組織内アカウント必須になり、自然に 1 回制限が効く。

### 「成績を送信直後に表示」を毎回設定するのが面倒

API では切り替えられないが、フォームを**テンプレート化**することで省略できる:

1. 一度きちんと設定した空フォーム(設問なし)を「テンプレ」として保存
2. `createQuiz()` の冒頭で `FormApp.openById(TEMPLATE_ID).copy(...)` してから設問を追加する

ただし手間に対して効果が小さいので、Phase 1 では未対応。需要があれば Phase 3 以降で実装する。

---

## D. ファイルレイアウト

```
quiz/
├── README.md          本ファイル
├── CLAUDE.md           Claude Code 向け運用指示書
├── index.html          GitHub Pages の公開トップ
├── gas/                GAS にコピペするソース
│   ├── config.gs
│   ├── questions.gs
│   └── createForm.gs
└── question-bank/      設問の出どころメモ(レビュー用)
    ├── 04-intellectual-property.md
    ├── 05-personal-information.md
    ├── 06-information-law.md
    └── 07-information-security.md
```

設問の正本は `gas/questions.gs` です。`question-bank/*.md` はレビュー補助なので、両者を必ず同期させてください。
