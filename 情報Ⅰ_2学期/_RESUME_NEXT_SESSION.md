---
updated: 2026-09-13
prev_session: 第5回の個人学習教材（lectures lec20 / practices 04-12）を作り、codex 監査 3 件を全件適用して第5回を done にした。push は未
---

# 情報Ⅰ 2学期 — 次セッション resume（第6回 POINT 20⑵ から）

## 1. 30 秒 status

- **第5回は完了。** 授業内3点（9/12 に push 済み）＋ lec20 ＋ practices 04-12 がそろい、
  `manifest.toml` は**第1〜5回すべて `status = "done"`**。ハブの一覧から「準備中」が消えた。
- **保全だけが残っている。** 下の §2 が最初の一手。
- 個人学習用の在庫: lectures は lec01〜17 と **lec20**、practices は 03-10 まで＋思考のステップ4＋**04-12**。
- 第6回以降の並び（確定）: **第6回 20⑵ → 第7回 22 → 第8回 25 → 第9回 26**。

## 2. 最初にやること — push（自セッション分だけ・submodule → 親の順）

2026-09-13 の作業は**まだ push していない**。整合性を報告して承認を取ってから、この順で。

```
[1] submodule (mikikof-lab) で commit → push
[2] 親リポ (my-company) で submodule 参照を更新して commit → push
```

対象（14 件。すべて 9/13 分）:

| 群 | ファイル |
|---|---|
| A lectures | `articles/20-programming-basics/index.html`(新) / `skills/interactive-lecture/examples/20-programming-basics.html`(新・凍結) / `index.html`(18 UNITS へ) |
| B practices | `articles/04-12-programming/index.html`(新) / 同 `_build_0412.py`(新・生成器) / 同 `assets/fig1〜5`(新・原本の図) / `index.html`(14 units へ) |
| C ハブ | `_ops/manifest.toml`(第5回 done・`[existing]` 更新) / `第05回_.../index.html` / 同 `04_個人学習/README.md` / `index.html`(一覧) |

親リポ側の自セッション分は 3 件だけ（submodule ポインタ / `audit/reviews/2026-09-13/0115-joho2-kai05-jishu/` /
`secretary/notes/2026-09-13-decisions.md`）。**親リポには他案件の未コミットが 120 件余りあるので巻き込まない。**

※ **joho-explainer / joho-quiz への同期は不要。** 今回の2本は mikikof-lab で配信される
（`https://mikikof.github.io/mikikof-lab/lectures/articles/20-programming-basics/` と
`.../practices/articles/04-12-programming/`）。授業内3点は 9/12 に同期済み。

## 3. 次にやること — 第6回

**第6回 ＝ POINT 20⑵「プログラミングの基本⑵」（配列）。** 入口は `/joho-2gakki`。
難所はまだ決めていない。`_ops/theme-plan.md` と `_ops/nansho-guide.md` を読んでから決める。

材料はもう手元にある（今回 lec20 で 20⑵ 全体を扱ったため）:
- 学習ノート 20⑵ の POINT ①配列（リスト）②要素（＋添字）③一次元配列 ④二次元配列、実習1〜5 の正答
- 4 章 章末2（while を抜けたあとの添字は 1 つ先）
- ベストフィット 04-12 の例題57・58、類題102・103（配列の問題群）
- **候補になる難所**: 「添字は 0 から」（型C 似て非なる：何番目 vs 添字）、
  「くり返しを抜けたあとの変数は 1 つ先を指す」（型D 数えると合わない・章末2）

**アンカー教材は両方とも作成済み**（lec20 / practices 04-12）。第6回は**授業内3点だけ**を作ればよい。

## 4. 確定事項（変えない前提）

- 授業 50 分＝解説ツール 25 分／印刷プリント 15 分／スピードテスト 10 分。一回一難所。
- 台帳は `_ops/manifest.toml` だけ。回フォルダは `build_kai.py` で組む派生物。
- **用語の線（第5回で確定・第6回でも守る）**: range の 2 番目の数を「終了値」と呼ばない。
  教科書の「値1・値2・増減値」＋「値2 は含まれない」を使う。
  **学習ノート 20⑴ 実習1 の選択肢 c も `range(値1, 値2, 増減値)` と書いている**（今回の新しい裏取り）。
  ただし **practices は原本の文をそのまま載せる場所**なので、ベストフィットの「終了値」はそこだけ原文どおり（7 件）。
- 正解は原本で裏取りし、**web 検索しない**。
- mikikof-lab は public。push 前に `check_public.py` が exit 0。
- codex 監査は `-p review-paper`。**プロファイルの実体は `~/.codex/<name>.config.toml`**（`config.toml` の
  `[profiles.X]` ではない）。`< /dev/null` を付けないと stdin 待ちになる。
  効いている証拠は出力冒頭の `reasoning effort: high` / `reasoning summaries: detailed`。

## 5. 今回の教訓（次も同じ罠を踏む）

- **置換のアンカーは行頭に取る。** `window\.HOSOKU_SUPP = \{.*?\n\};` を行頭アンカー無しで当てたら、
  エンジンの説明コメント（`//   - 内容は window.HOSOKU_SUPP = { ... } を…`）に食いつき、
  そこから本体末尾までの約 360 行、つまり **hosoku 補足エンジンごと消えた**。
  7 つの自己点検は全部緑だった（「差し替わったか」は見ていたが「エンジンが生き残ったか」を見ていなかった）。
  → 書き出し前の assert に**残す側の在庫**（エンジン 17 マーカー＋関数総数の下限）を足した。
- **検査対象の API は docs でなく実物から取る。** practices のエンジンは IIFE で包まれ
  `window` に何も出していない。`goToStage` を直接呼ぼうとして落ちた。実 UI（`.tl-item[data-target]`）を押す。
- **fixed 要素に `offsetParent` は使えない**（常に null）。miki 窓の可視判定を誤り、
  本命の「窓が下部を覆うか」を一度も測らないまま 0 件と報告しかけた。
- **headless は、操作で文書が伸びてからスクロールすると空フレームで撮り終わる。**
  白紙（7KB）を見たら、まず `display` / `opacity` / `elementFromPoint` / `scrollY` で
  構造破壊と切り分ける。撮るときは**スクロールせずに済む縦長ビューポート**にする。
- **機械が全部緑でも、実物を見ないと出ない欠陥がある。** 今回も目視で 2 件出た
  （参考A のコードに余分なカンマ、見出しの折返しで 2 行目が 1 文字だけ）。

## 6. ポインタ

- 回ファイル: `_ops/kai/05-kurikaeshi-han-i.md`（設計・進行台本。**答えは書いていない**）
- 監査ログ: `.company/audit/reviews/2026-09-13/0115-joho2-kai05-jishu/`
  （`01-prompt.md` は**事実台帳つきの渡し方の手本**。`03-plan.md` に採否と却下理由、`04-applied.md` に適用結果）
- 生成器: `practices/articles/04-12-programming/_build_0412.py`（追跡される・正本）
  lec20 の組み立ては scratchpad の `patch_lec20.py` + `lec20_slides.py` + `lec20_data.py`
  （**scratchpad は消えるので、lec20 を直すときは canonical から組み直すか HTML を直接編集する**）
- 独立検算: scratchpad `verify20.py`（PASS 52 件）。同等の検算は `_build_0412.py` の `selfcheck()` に内蔵
- 公開 URL: lec20 `https://mikikof.github.io/mikikof-lab/lectures/articles/20-programming-basics/`
  practices `https://mikikof.github.io/mikikof-lab/practices/articles/04-12-programming/`
- 決定と TODO: `.company/secretary/notes/2026-09-13-decisions.md`
- memory: `project_joho1_2gakki`、`feedback_bulk_replace_leaves_fragments`（行頭アンカー）、
  `feedback_headless_click_and_clip_traps`（罠3・罠4）、`feedback_headline_contradicted_by_own_material`

## 未決（本人の判断待ち）

- **practices の `assets/` に原本の解答図が public リポで追跡されている。**
  03-09 の `ans75-*.png`・`ans81-*.jpeg` 等。practices は解説を載せるサイトなので設計どおりではあるが、
  版元著作物の図である点は変わらない。既存3単元で確立した運用なので 04-12 も同じ形に揃えた。
  方針を変えるなら履歴からの除去が要る。
- 学習ノート 37 を lecture 2 本に割るか（`_ops/theme-plan.md` §5）。3学期の話。
