---
updated: 2026-09-13
prev_session: 第5回（POINT 20⑴ 繰り返しの範囲）の授業用3点を作り、codex を 2 巡回して収束させ、配信して 4 リポジトリとも push した。lectures lec20 と practices 04-12 は未着手
---

# 情報Ⅰ 2学期 — 次セッション resume（第5回の lec20・practices 04-12 を作る）

## 1. 30 秒 status

- 第1〜5回の**授業内3点**（解説ツール・印刷プリント・速テスト）がそろった。第5回ぶんは
  4 リポジトリとも push 済みで、**GitHub Pages の反映まで確認した**（§6 のハッシュ）。保全の残りは無い。
- **第5回だけ manifest が `building` のまま**。lectures lec20 と practices 04-12 が未作成のため。
  この 2 本を作れば第5回は done になる。
- 個人学習用の在庫: lectures は lec01〜17、practices は 03-10 までと思考のステップ4。
- 第6回以降の並び（確定）: **第6回 20⑵ → 第7回 22 → 第8回 25 → 第9回 26**。

## 2. 次にやること — lec20 と practices 04-12

### lec20（学習ノート POINT 20 全体）

**本人の決定（2026-09-12）**: **POINT 20⑴⑵ の全体に加えて、章末1・2 も参考に入れる。**
lec17 が章末5 を参考A に入れたのと同じ作り。26〜30 枚の見込み。

- 入口は `lectures/skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md`（最上位。矛盾したらこれが勝つ）。
  **canonical = `examples/11-analog-and-digital.html` を cp し、コンテンツ層だけ差し替える。**
  標準インタラクション層（miki.con / hosoku / スポットライト / P 文字ポップ / Space+もどす）は 1 文字も変えない。
- 差し替えるデータ構造: `HOSOKU_SUPP`（チップと 1:1）／`MIKI_GUIDE`（キー = 各スライドの `data-title` 完全一致）／
  `MIKI_TERM`／`iconData`／`POINT_ILLUST`／`reviewPool`／`MD_STEPS`／`resetAllInteractions` の単元固有部。
- **POINT 番号 = lec 番号。** 章番号とは無関係。
- 直近 2 本の実績: lec17 は 2345 行・スライド 21 枚・参考 3 本・reviewPool 16 問・iconData 9。lec16 は 313KB。
- **復習の正解の位置は散らす**（lec17 は 16 問を ア4・イ4・ウ4・エ4）。lec15 で 16 問中 14 問が「ア」に
  偏った前科がある。
- **デスクトップで miki.con の窓が下部を覆う問題**の余白（lec16 の CSS）を必ず入れる。
- 内容の芯（第5回の難所と揃える）: 20⑴ は「止まる合図の値は処理されない」、20⑵ は「添字は 0 から」と
  「繰り返しを抜けた後の変数は 1 つ先を指している」（章末2）。**「終了値」という語は使わない**（§3）。
- 終わったら `lectures/index.html` に `CHAPTER · 20` のカードを追加し、
  `skills/interactive-lecture/examples/20-*.html` に凍結コピーを置く。

### practices 04-12（ベストフィット 4章12「プログラミング」）

- **生成器方式。** 直近の 03-10 は `_build_0310.py`（1123 行）→ `index.html`（5123 行）。
  エンジン（CSS / JS ハーネス / サイドバー / トップバー / フッタ）は
  `skills/interactive-practice/examples/02-07-digital-info-representation.html` を**1 文字も変えずに流用**し、
  差し替えるのは `<main id="stages">` の中身と `TIMELINE_ENTRIES` / `PROBLEMS` / サマリの分母・閾値だけ。
- **収録範囲は原本どおり全部**: 例題55〜59・類題99〜104・練習105〜106 の 13 問。
  関数（例題59・類題104）はベストフィットでは 12 節に入っているので**外さない**
  （学習ノートでは POINT 21 だが、節の切り方が原本で違う）。
- **原本の図 5 枚は抽出済み**。`unzip -q "practices/_source/ベストフィット問題/BF情1New-4章12プログラミング-問題（Python）.docx" -d /tmp/extract-0412`
  → `word/media/image1〜5.jpeg`。image1〜3 = 中学までの復習の 3 構造（順次・分岐・反復）、
  image4 = 変数の図、image5 = **類題99 のフローチャート（本文が「右のフローチャート」と参照している）**。
  `articles/04-12-programming/assets/fig{N}-{slug}.jpeg` に置いて `<img>` で載せる。
  テキストの注記で代替しない（§4.10b）。
- **問題文は一字一句変えない**（「，」→「、」の置換だけは 03-10 でやっている）。独自に問題を足さない。
- 解答 docx に解説が無い小問は自前で補強する（§4.3）。全問にビジュアルを添える（§4.4）。
- 終わったら `practices/index.html` にエントリを追加し、`skills/interactive-practice/examples/` に凍結。

## 3. 確定事項（変えない前提）

- 授業 50 分＝解説ツール 25 分／印刷プリント 15 分／スピードテスト 10 分。一回一難所。
- 台帳は `_ops/manifest.toml` だけ。回フォルダは `build_kai.py` で組む派生物（手で育てない）。
- 語尾: 解説ツール＝丁寧体／プリント＝常体・設問「答えなさい」／速テスト＝常体「選べ・答えよ」／
  lectures＝丁寧体（miki.con も講義トーン）／practices＝原本の問題文は原文のまま。
- **第5回で引いた用語の線（lec20・practices でも守る）**: range の 2 番目の数を**「終了値」と呼ばない**。
  原本どうしで指すものが逆（学習ノート解答は「終了値の**次の値**」、ベストフィット解答は「終了値」そのもの）。
  中立な教科書の「値1・値2・増減値」＋「値2 は含まれない」を使う。
  ただし **practices は原本の文をそのまま載せる場所**なので、ベストフィットの「終了値」はその中でだけ原文どおり。
- 正解は原本（学習ノート解答 PDF・ベストフィット解答 docx）で裏取りし、**web 検索しない**。
- mikikof-lab は public。push 前に `check_public.py` が exit 0。
- codex 監査は `-p review-paper`（`~/.codex/review-paper.config.toml` が実体。`config.toml` の
  `[profiles.X]` を探す旧仕様ではない）。実走ログ冒頭の `reasoning effort: high` /
  `reasoning summaries: detailed` で効いていることを確かめる。5 件以上直したら次の巡を回し、
  **2 巡目には「直した箇所の一覧」と「却下した指摘とその根拠」を渡す**。

## 4. 第5回で得た教訓（次も同じ罠を踏む）

- **実物でしか出ない欠陥が 14 件あった。** うち 2 件は出荷を止める種類で、
  ①図を出す関数の引数がずれて**問題用紙に答えの線が描かれていた**（キャプションに `false` が印字され、
  図番号のラベルも消えていた）、②**設問文が正解の数をそのまま書いていた**。
  どちらも機械チェックは緑のまま通っていた。**問題側の本文に答えの数が出ていないことを、
  タグを剥いだ本文で数える**のが効いた。
- **測り方そのものを 3 回間違えた。** スマホ幅を headless の `--window-size=390` で測ったが、
  実際は幅の下限で 500px にレイアウトされていた（**iframe に 390px で埋めて撮る**）。
  実行時に組み立てる数値を静的 grep で測ろうとした。誤答の型を一つの言い回しだけで検出した。
- **名前を直したら、その名前が指す計算も直す。** 監査の指摘でトグルを改名したが表示を直さず、
  増減値が負のときと 1 以外のときに名前と食い違っていた。**名前が崩れる方向へ振って実物を見る。**
- **監査の診断が誤りでも、引っかかった場所は当たっている。** 「2 に戻ります」の 2 は手順番号だが
  値と読み違えられた。診断は却下しつつ「手順 2」と明示した。

## 5. 実行環境 / コマンド

```bash
LAB="/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab"
HUB="$LAB/情報Ⅰ_2学期"
# lec20 の scaffold（canonical を cp してコンテンツ層だけ差し替える）
mkdir -p "$LAB/lectures/articles/20-programming-basics"
cp "$LAB/lectures/skills/interactive-lecture/examples/11-analog-and-digital.html" \
   "$LAB/lectures/articles/20-programming-basics/index.html"
# practices 04-12 の原本図を抽出
unzip -q "$LAB/practices/_source/ベストフィット問題/BF情1New-4章12プログラミング-問題（Python）.docx" -d /tmp/extract-0412
ls /tmp/extract-0412/word/media/
# 原本テキスト（w:t と m:t の両方を拾う。w:t だけだと数式が落ちる）
python3 "$HUB/_ops/docx2txt2.py" /tmp/genpon \
  "$LAB/practices/_source/ベストフィット問題/BF情1New-4章12プログラミング-問題（Python）.docx" \
  "$LAB/practices/_source/ベストフィット解答/BF情1New-4章-解答（Python）.docx"
# 学習ノート 20⑴⑵・章末1・2（問題 p.48-51 / p.64、解答 PDF p.14 / p.18）
pdftotext -layout "$LAB/lectures/_source/高校情1学習ノート-解答PDF.pdf" - | less
# lec の機械チェック（プレイブック §6）と、回フォルダの組み直し
cd "$HUB" && python3 _ops/build_kai.py 5 && python3 _ops/check_public.py
```

## 6. ポインタ

- 第5回の commit（すべて push 済み・Pages 反映も確認・2026-09-12）:
  mikikof-lab `e597005`／my-company `cb9ae93c`／joho-explainer `03fbad3`／joho-quiz `d339be7`
- 公開 URL: 解説ツール `https://mikikof.github.io/joho-explainer/loop-range.html`／
  速テスト `https://mikikof.github.io/joho-quiz/?s=8`（配布は teacher.html でクラスと課題名を入れて作る）
- 回ファイル: `_ops/kai/05-kurikaeshi-han-i.md`（設計・進行台本・監査の採否。**答えは書いていない**）
- 答えと数値の台帳（非公開側）: `media/webツール/情報/edu-explainer-kit/specs/loop-range.spec.md`、
  `media/webツール/情報/印刷教材/specs/繰り返しの範囲.spec.md`
- 監査ログ: `.company/audit/reviews/2026-09-12/2310-joho2-kai05-3ten`（1 巡目）・
  `2340-joho2-kai05-3ten-rev2`（2 巡目。**渡し方の手本**）
- 決定と TODO: `.company/secretary/notes/2026-09-12-decisions.md`
- 回ファイルの手本: `_ops/kai/04-register-taihi.md`・`_ops/kai/05-kurikaeshi-han-i.md`
- memory: `project_joho1_2gakki`、`feedback_renamed_label_must_match_what_it_shows`、
  `feedback_headless_mobile_width_floor`、`feedback_codex_review_profile_removed`、
  `feedback_lecture_review_pool_answer_position`、`feedback_miki_window_covers_desktop_controls`

## 未決（本人の判断待ち）

- 学習ノート 37 を lecture 2 本に割るか（`_ops/theme-plan.md` §5）。
  単元の切り方＝カリキュラムの設計判断で、欠陥の修正ではない。3学期の話。
