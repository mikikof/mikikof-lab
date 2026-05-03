# mikikof-lab — Claude Code 運用指示書(ルート)

このリポジトリは、受験生向けの複数の学習Webツールを一つの屋根の下にまとめた**モノレポ**です。

各ツールは独立した配下フォルダを持ち、それぞれに専用の CLAUDE.md が置かれています。**Claude Code はまず本ファイルを読み、ユーザーの依頼内容から該当ツールを判別したうえで、そのツール配下の CLAUDE.md に従って動いてください**。

---

## 収容ツール一覧

| ツール名 | フォルダ | 公開URL | 専用指示書 |
|---|---|---|---|
| **Visual Column**(法・歴史・経済・情報のエッセイ集) | `column/` | `/column/` | [column/CLAUDE.md](column/CLAUDE.md) |
| **Daisu Column**(受験↔大学の橋渡し数学コラム) | `daisu-column/` | `/daisu-column/` | [daisu-column/CLAUDE.md](daisu-column/CLAUDE.md) |
| **Interactive Lecture Lab**(授業用HTMLスライド) | `lectures/` | `/lectures/` | [lectures/CLAUDE.md](lectures/CLAUDE.md) |
| **Interactive Practice Lab**(演習用HTML教材) | `practices/` | `/practices/` | [practices/CLAUDE.md](practices/CLAUDE.md) |
| **Quiz Form Kit**(Google フォーム小テスト作成キット / GAS) | `quiz/` | `/quiz/` | [quiz/CLAUDE.md](quiz/CLAUDE.md) |
| (将来) その他ツール | — | — | — |

---

## 文章トーン(全ツール共通)

このリポジトリで書くすべての文章 — 記事本文だけでなく、ポータルや一覧ページの見出し・リード・カード説明・フッターの一行まで — は、**理路整然・抑制的・アカデミック**なトーンで統一します。

- **事実と構造で書く**。比喩や抽象名詞に依存しない
- **見出しをキャッチコピーにしない**。「〜を。」「〜に。」で止める標語調や、ポスター的な大口は使わない
- **誇張形容を削る**。「深掘り」「詰め込む」「満載」「凝縮」「余すところなく」は使用禁止
- **AI頻出メタファーを避ける**。「立体化する」「紐解く」「別のかたちで」「学びのハブ」は地雷
- **対象属性の明示をしない**。「受験生のための〜」「大学生向け〜」のような冠はつけず、内容ベースで記述する
- **上品であること**。硬すぎず、軽すぎず、宣伝文句にもならない。大学生の教養読み物として成立するトーンを、見出しやカード1枚の文言にまで貫く

具体的な禁止表現一覧と Before/After 事例は [`column/CLAUDE.md`](column/CLAUDE.md) §7(特に §7-2 と §7-6)を参照。`column/` 以外のツールでも、文章を書くすべての箇所にこの原則をそのまま適用します。

---

## 1. ツールの判別ルール

ユーザーの依頼が来たら、以下のキーワードでまずツールを識別してください。

### ▶ ビジュアル・エッセイ(column / visual-column)に行くキーワード

- 「コラム」「エッセイ」「記事」「ビジュアルエッセイ」「Visual Column」
- 「法」「歴史」「経済」「情報」「時事」「社会」「思想」「制度」一般のコラム依頼
- 「〜について解説して」「〜を読み解く記事を」
- 「PDFから記事を作って」「この資料で記事を書いて」
- 読み物系の成果物全般(数学コラム以外)

→ [`column/CLAUDE.md`](column/CLAUDE.md) を読み、以降はその指示に従う

### ▶ 数学コラム(daisu-column)に行くキーワード

- 「数学コラム」「Daisu Column」「数学の記事」
- 「数学」「受験数学」「大学数学」「東大京大」「数Ⅰ〜Ⅲ」「線形代数」「解析」「微分方程式」「証明」
- 受験数学と大学数学の橋渡しを意識した硬派な数学読み物の依頼

→ [`daisu-column/CLAUDE.md`](daisu-column/CLAUDE.md) を読み、以降はその指示に従う(本ツールは Opus 4.7 [1M] 死守 + ultrathink + codex は `-p review-paper`)

### ▶ 授業スライド(lectures)に行くキーワード

- 「授業」「スライド」「レクチャー」「単元」「情報Ⅰ」「情報数理入門」
- 「学習ノート」「共通テスト対策」「授業投影用」「生徒の復習用」
- 「インタラクティブ教材」「HTMLスライドサイト」
- 授業で使う Web教材全般

→ [`lectures/CLAUDE.md`](lectures/CLAUDE.md) を読み、以降はその指示に従う

### ▶ 演習教材(practices)に行くキーワード

- 「演習」「練習問題」「ベストフィット」「問題集」
- 「採点」「自走演習」「隙間時間で解ける」
- 「ベストフィット問題集の○○」「○○の練習問題を作って」

→ [`practices/CLAUDE.md`](practices/CLAUDE.md) を読み、以降はその指示に従う

### ▶ Google フォーム小テスト(quiz)に行くキーワード

- 「小テスト」「単元テスト」「Google フォーム」「GAS でフォーム」「クイズ」
- 「採点付きフォーム」「N 問の選択式テスト」
- フォーム自動生成キットへの依頼全般

→ [`quiz/CLAUDE.md`](quiz/CLAUDE.md) を読み、以降はその指示に従う

> 注: 旧「一問一答(HTML 単一ファイルのフラッシュカード)」は本ツールとは別物。`quiz/` 枠は 2026-05 から **GAS による Google フォーム小テスト作成キット** で確定運用。HTML 単一ファイルの一問一答が必要になった場合は別フォルダ(例: `flashcards/`)で新設する。

### ▶ ツールが判別できない場合

ユーザーに確認を取ります。例:

> 「コラム記事」「一問一答」など、どのツールでの作成をご希望ですか? それとも別の形式でしょうか。

---

## 2. 作業ディレクトリのルール

ツールを判別したら、以降は**必ずそのツールのフォルダ内で作業**してください。

```bash
# コラムの場合
cd column/
# 以降の作業はすべて column/ 配下で完結
```

スクリプトの実行パスや相対パスは、各ツールのCLAUDE.md内で定義されています。屋根(ルート)の都合を混ぜないこと。

---

## 3. ルート直下のファイルについて

このリポジトリの**ルート直下**にあるものは、すべてのツールに横串で関わるものだけです:

- `index.html` — ポータルページ(全ツールへのリンク集)
- `README.md` — リポジトリ全体の説明(人間向け)
- `CLAUDE.md` — 本ファイル
- `.gitignore` — Git 管理除外設定

新しいツールを追加する時以外、ルートのファイルは原則編集しません。

---

## 4. 新しいツールを追加する手順

将来、新しい学習ツールを追加する時は次の手順で:

1. ルート直下に新しいフォルダを作成(例: `quiz/`)
2. そのフォルダ内に以下を配置:
   - `index.html`(ツールのトップページ)
   - `CLAUDE.md`(ツール固有の運用指示)
   - `templates/`、`scripts/` など必要に応じて
3. ルートの `index.html`(ポータル)にツールへのリンクを追加
4. ルートの本 `CLAUDE.md` の「収容ツール一覧」と「判別ルール」に追記

---

## 5. Git 運用のルール

コミットメッセージには**どのツールに対する変更か**を prefix として明記:

```
column: 法の二大系統の記事を追加
daisu-column: 包絡線と特異解を公開
quiz: 情報社会の確認問題を追加
root: ポータルページのデザイン調整
```

push 先は常に `origin main`。ブランチ運用はせず、main 直接運用で問題ありません(個人開発のため)。

---

## 6. 公開URL構造

GitHub Pages で公開される際のURL:

- ポータル: `https://mikikof.github.io/mikikof-lab/`
- コラム集トップ: `https://mikikof.github.io/mikikof-lab/column/`
- コラム記事: `https://mikikof.github.io/mikikof-lab/column/articles/{slug}/`
- 数学コラムトップ: `https://mikikof.github.io/mikikof-lab/daisu-column/`
- 数学コラム記事: `https://mikikof.github.io/mikikof-lab/daisu-column/articles/{slug}/`
- 授業スライドトップ: `https://mikikof.github.io/mikikof-lab/lectures/`
- 授業スライド単元: `https://mikikof.github.io/mikikof-lab/lectures/articles/{番号}-{slug}/`
- 演習教材トップ: `https://mikikof.github.io/mikikof-lab/practices/`
- 演習教材単元: `https://mikikof.github.io/mikikof-lab/practices/articles/{番号}-{slug}/`
- (将来)クイズ: `https://mikikof.github.io/mikikof-lab/quiz/`

各ツール内のリンク構造は、この階層を前提に組むこと。

---

## 7. 困ったときは

- 「どのツールで作業すべきか」で迷ったら、ユーザーに確認
- ツールをまたぐ変更が必要な時は、変更範囲をユーザーに報告してから着手
- ルート直下の何かを編集する必要が出た時は、必ず事前に一声かける

---

## Appendix: 現在の状態

- [x] Visual Column(法・歴史・経済・情報のエッセイ集) — 稼働中
- [x] Daisu Column(受験↔大学の橋渡し数学コラム) — 稼働中(2026-05 に column/ から独立。第 1 回「空間と図形の次元」+ 第 2 回「包絡線と特異解」)
- [x] Interactive Lecture Lab(授業用HTMLスライド) — 稼働中
- [x] Interactive Practice Lab(演習用HTML教材) — 稼働中(1単元: 1章03 知的財産権の扱い)
- [x] Quiz Form Kit(Google フォーム小テスト作成キット / GAS) — 稼働中(Phase 2 完了: 25 問構成 / 04 知財 6 + 05 個人情報 6 + 06 情報法 6 + 07 セキュリティ 7)
- [ ] その他のツール — 未定

統合予定のツールがあれば、ユーザーに「今のタイミングで統合しますか?」と確認してから着手。
