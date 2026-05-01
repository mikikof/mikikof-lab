---
description: 教材 HTML(lectures/column/practices/quiz)をリッチデザイン+追加要素でブラッシュアップする
argument-hint: [path or slug] [重点項目]
---

# /brushup — 教材のリッチデザイン化ブラッシュアップ

このコマンドは、対象の教材 HTML を **「リッチデザイン化」** + **「不足の補強」** で 1 段ブラッシュアップする。一度作った教材に対して、ユーザーが「もっと良くして」と感じたタイミングで明示的に呼ぶ。

---

## 1. 対象の決定

`$ARGUMENTS` の内容で分岐する。

### 引数あり

- **完全パス**: `lectures/articles/01-information-and-media/index.html` / `lectures/articles/01-information-and-media` → そのまま使用
- **スラッグだけ**: `01-information-and-media` / `04-intellectual-property` → `articles/{slug}/index.html` を **lectures / practices / column** の順で探索して特定
- **ツール名 + スラッグ**: `practices/03-intellectual-property` のような形式も解釈
- **2 つ目以降の引数**: 重点項目のヒントとして扱う(例: `インタラクション強化のみ` / `深掘りスライド追加` / `Phosphor 化のみ`)

### 引数なし

**会話文脈から直近の編集対象を推定する。**

- 最後に Edit / Read / Write した HTML
- 直前のユーザー発言で言及された教材
- 直前にスクリーンショット([Image #N])で見せられた教材

推定が一意でない場合のみ、ユーザーに「どれですか?」と短く確認。1 つに絞れる場合は確認せず即実行する。

---

## 2. 着手前チェック

1. 対象 HTML を Read。先頭〜末尾まで構造を把握(slide 数、SVG 数、interactive 要素の種類)
2. 該当ツールの `CLAUDE.md`(lectures なら `lectures/CLAUDE.md`)+ skill(`skills/interactive-lecture/SKILL.md`)を Read。最新の規約・落とし穴を把握
3. 対応する `_source/` 正本を Read で確認(教材改修時は答え誤りリスク回避のため必須)

---

## 3. ブラッシュアップ項目(順に実行)

各項目を **走査 → 不足リスト化 → ユーザーに見せて承認 → 修正適用** の流れで実行する。承認なしに大規模改修しない。

### Step 1. デザイン規約点検 (lectures CLAUDE.md §4 + SKILL.md §9 / §13 / §14)

- [ ] **SVG 内に `<rect width="..." height="..." fill="..."/>` の背景矩形が残っていないか** → 削除して透過に(SKILL.md §9.19)
- [ ] **`.law-illust` / `.def-box` の background が不透明色になっていないか** → 透過 / コンテナ任せに
- [ ] **SVG 内 `<text>` で「② POINT」「残存性」など役割テキストを書いていないか** → HTML 側の `.icon-card-tag` `.icon-card-name` に逃がす(SKILL.md §9.20 / §14)
- [ ] **自作 SVG が残っていないか** → Phosphor / Lucide / Heroicons / Tabler / Material Symbols から借りた SVG path に置換(1 単元 = 1 ライブラリ)
- [ ] **design tokens が外れていないか** — `icoNavy` (5d8eb3→0F2847) / `icoGold` (f4d995→8a6d1f) / `icoSh` (drop-shadow filter) を全 SVG 共通で使用
- [ ] **フォントサイズ・太さ**(SKILL.md §2 投影視認性基準): 本文 19px/500、def-desc 16px/500、quiz-question 19px/600 等を満たすか
- [ ] **ラベルが要素のリング線・縁と被っていないか** — SVG 円・楕円の枠と text 位置の衝突を点検

### Step 2. 構成の深掘り検討

学習ノートの単元内容だけだと「浅い」可能性がある領域を判定。以下に該当するなら **1〜4 スライドの追加副題** を提案する:

| 元の単元 | 候補となる深掘り副題 |
|---|---|
| 情報の定義 | DIKW 階層(データ→情報→知識→知恵) |
| 印象操作・統計 | グラフ基本 6 型 / 印象操作 9 技法(目盛り/視覚効果/比較) |
| 知的財産 | 著作権の歴史的経緯 / Creative Commons 4 種ライセンス |
| 個人情報 | 個人情報保護法の改正史 / 海外法(GDPR)との比較 |
| 情報法 | 法のピラミッド(憲法→法律→政令→省令)|
| 情報セキュリティ | CIA トライアド / ゼロトラスト / 最新インシデント事例 |
| 問題発見と解決 | PPDAC / トレードオフ / 演繹と帰納の厳密化(SKILL.md §4.10) |

判断基準: **共通テスト・大学入試・実生活で問われる射程**を持つか。学習指導要領に明記されていなくても、教材として薄ければ補強する。

### Step 3. インタラクション強化

- 各 POINT に **少なくとも 1 つのインタラクション**(タップ展開 / 判定 / 解説パネル)があるか
- 静的な def-box だけになっている POINT があれば、`comparison-visual` / `judgment-chip` / `tree-diagram` / `case-expander` 等を追加
- `復習チャレンジ` の問題プールが 10 問未満なら追加(目標 12-15 問)

### Step 4. リッチ要素の追加

- **最新事例**(過去 1〜3 年): web_search で 3〜5 件取得し、case-expander で 1〜2 件埋め込む(SKILL.md §6 事例の扱い参照)
- **答え合わせ・まとめツリー**に Phosphor アイコンを各項目に小さく埋め込み
- **セクション仕切り**に視覚的アクセント(該当節を象徴する小 SVG)
- **lectures/index.html の単元カード**の説明文・タグに新規追加内容を反映

### Step 5. 完了報告

報告には必ず以下を含める:

1. **変更サマリ**: どのスライドにどんな変更を入れたか箇条書き
2. **解答 PDF と全問照合済みかどうか**(改修で問題を触った場合)
3. **「次にユーザーが気にしそうなポイント」を先回り列挙** — レイアウト崩れ・特定 POINT の追加要望・更なる事例追加など、想定される次の要望を 2〜3 件
4. **submodule 関連**: ファイルが submodule 内にある場合、commit & push の必要性を明示。整合性レポート + 承認取得後に push 実施(メモリ `feedback_git_push_confirmation.md` 参照)

---

## 4. やらないこと

- 学習ノート問題の **正答・解説の根拠フレーム** を勝手に変えない(lectures CLAUDE.md §4.8)
- 大規模リファクタ(ファイル分割・別単元への影響)はユーザー承認なしに行わない
- 自作 SVG での「リッチ化」を試みない — 必ず OSS アイコンライブラリから借りる
- 規約に反する装飾(子供っぽい絵文字・標語調見出し・対象属性明示)を追加しない(lectures CLAUDE.md §4.4 / §4.5 / §4.7)

---

## 5. 引数 example

```bash
/brushup
# → 直近の編集対象を推定して全 5 ステップ実行

/brushup lectures/articles/01-information-and-media
# → 01 情報とメディアを対象に全 5 ステップ実行

/brushup 04-intellectual-property
# → スラッグから lectures/articles/04-intellectual-property/ を探索

/brushup 01-information-and-media デザイン規約点検のみ
# → Step 1 だけ実行(Phosphor 化・SVG bg 削除 等の機械的修正)

/brushup 01-information-and-media 深掘りスライド追加
# → Step 2 を中心に提案 → 承認 → 実装

/brushup practices/03-intellectual-property
# → practices ツールの教材を対象に
```

---

## 6. 完了の判定

- HTML タグバランス OK(Python の HTMLParser でチェック)
- 解答 PDF と全問照合済み(問題を触った場合)
- ブラウザでの実機確認は **ユーザーに依頼**(私からは「`python3 -m http.server` で確認してください」と伝える)
- ユーザーが「OK」と返した時点で完了
