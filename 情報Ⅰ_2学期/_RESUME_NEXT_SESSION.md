---
updated: 2026-09-12
prev_session: 第2回（POINT 15 補数）と第3回（POINT 16 論理回路）の授業用3点・lec15/16・practice 03-09/思考のステップ4 を作り、codex 監査を収束させ、4 リポジトリに push した
---

# 情報Ⅰ 2学期 — 次セッション resume（第4回を作る）

## 1. 30 秒 status

- 第1〜3回（POINT 14・15・16）の授業用3点と、個人学習用の lectures（lec14〜16）・practices（03-08・03-09・思考のステップ4）がそろい、公開も済んでいる。
- 次は第4回。最初に POINT を決める（§4 の 1 行目）。入口は `/joho-2gakki`。

## 2. 確定事項（変えない前提）

- 授業 50 分＝解説ツール 25 分／印刷プリント 15 分／スピードテスト 10 分。一回一難所。難所を 1 文で決めてから作る（`_ops/nansho-guide.md`）。
- 2学期は学習ノートの順に POINT 14〜26。回数別の取り方は `_ops/theme-plan.md` §2b。
  - 8 回の並び: 第4回 17 → 第5回 20⑴ → 第6回 20⑵ → 第7回 22 → 第8回 25 → 第9回 26
  - 5 回の並び: 第4回 20⑴ → 第5回 20⑵ → 第6回 26
- 台帳は `_ops/manifest.toml` だけ。回フォルダは `build_kai.py` で組む派生物（手で育てない）。
- 語尾: 解説ツール＝丁寧体／プリント＝常体・設問「答えなさい」／速テスト＝常体「選べ・答えよ」／lectures＝丁寧体（実習の問題文は原文を引用枠で）／practices＝常体（問題文は原本一字一句）。
- 正解は原本（学習ノート・解答 PDF・ベストフィット）で裏取りし、web 検索しない。数値は独立に検算し、生成器に assert を置く。
- mikikof-lab は public。push 前に `check_public.py` が exit 0。push は submodule mikikof-lab → my-company → `~/joho-explainer` → `~/joho-quiz` の順。`git add -A` を使わず、ファイルを名前で指定する。
- codex 監査は `-p review-paper` で 2 本（授業用3点／lectures＋practices）。事実台帳（原本の抜粋と図の構成）を同梱する。5 件以上直したら次の巡を回す。指摘は採否の前にコード・原本の図・実機で裏を取る。
- lectures: POINT 番号＝lec 番号。新しい lec は lec16 の index.html を外枠にして内容レイヤだけ差し替える。デスクトップの miki.con の窓対策の余白（lec16 の CSS）を入れ、復習の正解の位置は散らす。
- 検査は実物のボタンを座標で押す（押す点が覆われていないかを elementFromPoint で確かめてから）。

## 3. 実行環境 / コマンド

```bash
HUB="/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/情報Ⅰ_2学期"
WEB="/Users/mikiokofune/my-company/.company/media/webツール/情報"
cd "$HUB"
# Phase 0: 回ファイルを起こす（manifest の [[kai]] no = 4 も足す）
cp _templates/kai.template.md _ops/kai/04-<slug>.md
# Phase 1: 原本 docx のテキスト抽出（w:t・m:t・上下付き・画像アンカー）。出力は公開リポに置かない
mkdir -p /tmp/genpon && python3 _ops/docx2txt2.py /tmp/genpon "/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/practices/_source/ベストフィット問題/BF情1New-3章10コンピュータの構成と動作-問題（Python）.docx" "/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/lectures/_source/学習ノート_問題/高校情1学習ノート（p.34～45）-3章コンピュータの仕組み-問題Word.docx"
# Phase 2c: 速テストのセット一覧（次は set_index 7）
cd "$WEB/スピードクイズ" && node -e 'global.window={};require("./data/questions.js");console.log(window.QUIZ_SETS.map((s,i)=>i+" "+s.id).join("\n"))'
# Phase 5: 回フォルダを組む → 公開安全ゲート
cd "$HUB" && python3 _ops/build_kai.py 4 && python3 _ops/check_public.py
```

制作の手順メモ（第3回で使ったやり方）
- 解説ツール: `edu-explainer-kit/assets/template.html` の `<body>` までに教材を足して `dist/<name>.html`。直すときは dist を直接直す（教材部分は dist にそのまま入っている）。
- 印刷プリント: `印刷教材/dist/_gen_<単元>.js` を直して `node` で問題・解答 HTML を再生成 → headless Chrome の `--print-to-pdf` → `pdfinfo` で 2 枚、`pdftoppm -gray` で目視。
- 監査: `.company/audit/reviews/2026-09-12/_build_kai03_r1.py` がプロンプト組み立ての雛形（原本の抽出テキストのパスは次回作り直す）。

## 4. 残工程チェックリスト（第4回）

- [ ] 2学期の残りの授業回数を本人に聞き、第4回の POINT を決める（8 回以上の並び＝17「コンピュータの構成と動作」／5〜7 回＝20⑴「プログラミングの基本⑴」）。力点と型は theme-plan.md §2b の表をそのまま使う
- [ ] Phase 0: manifest に `[[kai]] no = 4`（status building・anchor・artifacts: explainer／print／quiz set_index 7／lecture／practice）、`_ops/kai/04-<slug>.md` に難所 1 文と型、25/15/10 の見取り図 → 本人の合意
- [ ] Phase 1: 原本の裏取り（学習ノート該当 POINT の実習文と解答 PDF の該当ページ、ベストフィット該当節の問題と解答）→「共通の例と数値」の表と独立検算
- [ ] Phase 2: 解説ツール → 印刷プリント（A4 2 枚・グレースケール）→ 速テスト（`questions.js` に追記）
- [ ] Phase 3: 未作成のアンカーだけ作る。17 なら lec17 と practices 03-10・思考のステップ5、20⑴ なら lec20 と practices 04-12（`[existing]` と突き合わせる）
- [ ] Phase 4〜7: 整合 → `build_kai.py 4` → 配信用コピー（`情報/`、`~/joho-explainer` の同期配列とカード、`~/joho-quiz`）→ codex 監査 2 本 → manifest を done → push

## 未決（本人の判断待ち）

- lec15 の復習チャレンジで、16 問中 14 問の正解が「ア」に偏っている。直すか
- lectures（lec11〜15）をデスクトップで開くと、miki.con の窓が下部のボタンを覆う。lec16 と同じ余白を足すか
- manifest の第01回が `status = "building"` のまま（成果物は 8/3 に保全済み）。done にするか
- 学習ノート 37 を lecture 2 本に割るか（theme-plan §5）

## 5. 作業方針（本人の指定）

- lectures・practices は個人学習用で、授業内では使わない。質は落とさない。
- 授業日程は台帳に書かない（本人が持つ）。
- 教材の日本語は AI 臭を避ける（演出語・決めぜりふ・「〜しよう」型の誘導を使わない）。

## 6. ポインタ

- 直近 commit（push 済み）: mikikof-lab b3ca2ed・8ecd355、my-company 2985d48c・8d96e697、joho-explainer 7257682、joho-quiz ea7b5b3
- 回ファイルの手本: `_ops/kai/02-hosuu-genzan.md`・`_ops/kai/03-ronri-kairo.md`（共通の例と数値・用語の線・使わないもの）
- 監査ログ: `.company/audit/reviews/2026-09-10/1300-joho2-kai02-*`、`.company/audit/reviews/2026-09-12/0230-joho2-kai03-*`
- 決定と TODO: `.company/secretary/notes/2026-09-12-decisions.md`、`.company/secretary/todos/2026-09-12.md`
- lectures・practices の制作メモ: `lectures/_RESUME_NEXT_SESSION.md`・`practices/_RESUME_NEXT_SESSION.md` の 9/12 追記
- memory: `project_joho1_2gakki`、`feedback_miki_window_covers_desktop_controls`、`feedback_lecture_review_pool_answer_position`、`feedback_spliced_page_missing_close_tag`
