---
updated: 2026-09-12
prev_session: 第4回（POINT 17 コンピュータの構成と動作）の授業用3点・lec17・practices 03-10 を作り、codex 監査を 2 巡で収束させ、manifest を done にし、4 リポジトリへ push した
---

# 情報Ⅰ 2学期 — 次セッション resume（第5回を作る）

## 1. 30 秒 status

- 第1〜4回（POINT 14・15・16・17）の授業用3点と、個人学習用の lectures（lec14〜17）・
  practices（03-08・03-09・03-10・思考のステップ4）がそろった。manifest は 4 回すべて `done`。
- 第4回は 4 リポジトリとも push 済み（§7 のハッシュ）。保全の残りは無い。
- 次は第5回。並びは確定していて **POINT 20⑴「プログラミングの基本⑴」**（本人が 9/12 に
  「あと6回以上」と回答 → 17 → 20⑴ → 20⑵ → 22 → 25 → 26）。入口は `/joho-2gakki`。

## 2. 確定事項（変えない前提）

- 授業 50 分＝解説ツール 25 分／印刷プリント 15 分／スピードテスト 10 分。一回一難所。
  難所を 1 文で決めてから作る（`_ops/nansho-guide.md`）。
- 2学期は学習ノートの順に POINT 14〜26。回数別の取り方は `_ops/theme-plan.md` §2b。
  残りの並び（確定）: **第5回 20⑴ → 第6回 20⑵ → 第7回 22 → 第8回 25 → 第9回 26**
- 台帳は `_ops/manifest.toml` だけ。回フォルダは `build_kai.py` で組む派生物（手で育てない）。
- 語尾: 解説ツール＝丁寧体／プリント＝常体・設問「答えなさい」／速テスト＝常体「選べ・答えよ」／
  lectures＝丁寧体（実習の問題文は原文を引用枠で）／practices＝常体（問題文は原本一字一句）。
- 正解は原本（学習ノート・解答 PDF・ベストフィット）で裏取りし、web 検索しない。
  数値は独立に検算し、生成器に assert を置く。
- **原本の問題文を写している箇所は、言い回しを直さない。** 第4回のプリント大問1 は学習ノート実習2 の
  原文そのままで、監査の「言い換えろ」を原本 p40 で確認して却下した（`kai/04` の「用語の線」に記録）。
  原本に誤植があるときは直して記録する（練習93 の括弧落ちは `_build_0310.py` にコメント）。
- mikikof-lab は public。push 前に `check_public.py` が exit 0。
- codex 監査は `-p review-paper` で 2 本（授業用3点／lectures＋practices）。事実台帳を同梱する。
  5 件以上直したら次の巡を回す。**2 巡目は「直した箇所の一覧」と「却下した指摘とその根拠」を渡す**
  （第4回の rev2 はこの形で要修正 0 に収束した）。指摘は採否の前にコード・原本の図・実機で裏を取る。
- lectures: POINT 番号＝lec 番号。新しい lec は lec16 の index.html を外枠にして内容レイヤだけ差し替える。
  デスクトップの miki.con の窓対策の余白（lec16 の CSS）を入れ、復習の正解の位置は散らす
  （lec17 は 16 問を ア4・イ4・ウ4・エ4）。
- **見出し・キーメッセージは、その回の発展部分で反証されないかを確かめる。**
  第4回は当初「途中結果はレジスタに置いたままにできない」だったが、同じ回の章末5（レジスタ 2 つ）で
  反証されるので「同じレジスタに読み込めば、途中結果は消える」に差し替えた。
- 検査は実物のボタンを座標で押す（押す点が覆われていないかを elementFromPoint で確かめてから）。
  検査が 0 を返したら、まず**検査側のセレクタ名**を疑う（第4回で `side-item` という無い名前を使って
  偽陰性を出した。正しくは `sb-section`）。

## 3. 実行環境 / コマンド

```bash
HUB="/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/情報Ⅰ_2学期"
WEB="/Users/mikiokofune/my-company/.company/media/webツール/情報"
cd "$HUB"
# Phase 0: 回ファイルを起こす（manifest の [[kai]] no = 5 も足す）
cp _templates/kai.template.md _ops/kai/05-<slug>.md
# Phase 1: 原本 docx のテキスト抽出（w:t・m:t・上下付き・画像アンカー）。出力は公開リポに置かない
mkdir -p /tmp/genpon && python3 _ops/docx2txt2.py /tmp/genpon \
  "/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/lectures/_source/学習ノート_問題/高校情1学習ノート（p.34～45）-3章コンピュータの仕組み-問題Word.docx"
# 学習ノート 問題PDF を直接読む（pdftotext がある。POINT 17 は p40 だった）
pdftotext -layout "$HUB/../lectures/_source/高校情1学習ノート-問題PDF.pdf" - | less
# Phase 2c: 速テストのセット一覧と正解位置の分布（次は set_index 8）
node -e 'const fs=require("fs"),vm=require("vm");
const s=vm.runInNewContext(fs.readFileSync("'"$WEB"'/スピードクイズ/data/questions.js","utf8")+"\n;window.QUIZ_SETS",{window:{}});
s.forEach((x,i)=>{const mc=x.questions.filter(q=>q.type==="mc"),d={};
mc.forEach(q=>{const k="アイウエ"[q.answer];d[k]=(d[k]||0)+1});
console.log(i,x.id,JSON.stringify(d))})'
# Phase 5: 回フォルダを組む → 公開安全ゲート
cd "$HUB" && python3 _ops/build_kai.py 5 && python3 _ops/check_public.py
```

制作の手順メモ
- 解説ツール: 既存の `dist/<近い単元>.html` を cp して教材部分（MATERIAL）を差し替える。直すときは dist を直接。
- 印刷プリント: `印刷教材/dist/_gen_<単元>.js` を直して `node` で問題・解答 HTML を再生成 →
  headless Chrome の `--print-to-pdf` → `pdfinfo` で枚数、`pdftoppm -gray` で目視。
  狭いカラムに表を入れると縦潰れするので `table-layout:fixed` を当てる。
- lec の内容差し替えで**正規表現を使わない**。`window.X = {...}` は補足エンジンの説明コメント内にも
  同じ文字列があり、そちらに先にマッチしてエンジン本体を消す（第4回で 44,000 字を失った）。
  節単位＋行頭アンカー（`^`, `re.M`）で組み、置換は**件数アサート付きの python** で行う。

## 4. 残工程チェックリスト（第5回）

- [ ] Phase 0: manifest に `[[kai]] no = 5`（status building・anchor lec20・artifacts: explainer／print／
      quiz set_index 8／lecture 20／practice）、`_ops/kai/05-<slug>.md` に難所 1 文と型、
      25/15/10 の見取り図 → 本人の合意
- [ ] Phase 1: 原本の裏取り（学習ノート POINT 20⑴ の実習文と解答 PDF の該当ページ、
      ベストフィット 4章の該当節）→「共通の例と数値」の表と独立検算
- [ ] Phase 2: 解説ツール → 印刷プリント（A4 2 枚・グレースケール）→ 速テスト（`questions.js` に追記）
- [ ] Phase 3: 未作成のアンカーだけ作る（lec20 と practices の 4 章該当節。`[existing]` と突き合わせる）
- [ ] Phase 4〜7: 整合 → `build_kai.py 5` → 配信用コピー（`情報/`、`~/joho-explainer` の同期配列と
      カード、`~/joho-quiz`）→ codex 監査 2 本 → manifest を done → push

## 未決（本人の判断待ち）

- **速テストの正解位置が偏っている。** 第2回 `joho-binary-complement` は mc5 問すべて「ア」、
  第3回 `joho-logic-gates` は mc6 問すべて「ア」、`joho1-sample` は mc7 のうちイ6。
  生徒が「ア」を選び続けると第2回・第3回は全問正解になる。**両回は done で配信済み**なので直すか判断が要る
  （直すなら `情報/スピードクイズ/data/questions.js` と `~/joho-quiz/data/questions.js` の両方。
  原本の選択肢順を持つ問は据え置く）
- lectures（lec11〜15）をデスクトップで開くと、miki.con の窓が下部のボタンを覆う。lec16 と同じ余白を足すか
- 学習ノート 37 を lecture 2 本に割るか（theme-plan §5）

## 5. 作業方針（本人の指定）

- lectures・practices は個人学習用で、授業内では使わない。質は落とさない。
- 授業日程は台帳に書かない（本人が持つ）。
- 教材の日本語は AI 臭を避ける（演出語・決めぜりふ・「〜しよう」型の誘導を使わない）。

## 6. ポインタ

- 第4回の commit（すべて push 済み・2026-09-12）:
  mikikof-lab `ceff69e`／my-company `ad27e08a`／joho-explainer `d78c50d`／joho-quiz `ca41d4c`
  （この resume ファイル自身のコミットは mikikof-lab のローカルに 1 本だけ残る。次の push に同梱される）
- 回ファイルの手本: `_ops/kai/03-ronri-kairo.md`・`_ops/kai/04-register-taihi.md`
  （共通の例と数値・用語の線・使わないもの・却下した監査指摘の記録）
- 監査ログ: `.company/audit/reviews/2026-09-12/1840-joho2-kai04-3ten`・
  `1840-joho2-kai04-lec17-prac0310`・`2110-joho2-kai04-rev2`（2 巡目の渡し方の手本）
- 決定と TODO: `.company/secretary/notes/2026-09-12-decisions.md`、`.company/secretary/todos/2026-09-12.md`
- memory: `project_joho1_2gakki`、`feedback_headline_contradicted_by_own_material`、
  `feedback_lecture_review_pool_answer_position`、`feedback_miki_window_covers_desktop_controls`、
  `feedback_spliced_page_missing_close_tag`
