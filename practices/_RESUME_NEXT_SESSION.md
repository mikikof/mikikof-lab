---
updated: 2026-09-10（03-09「2進数と論理演算」を新規作成。codex audit 中・未 push。03-08 は 8/3 に作成済みだが index 未登録だったので 9/10 に登録）
prev_session: "03-09 2進数と論理演算（例題 7 ＋ 演習 13・self 型主軸）を _build_0309.py で生成。原本図 46 枚を assets/ に抽出、解答は計算で独立検算"
---

# practices(Interactive Practice Lab)— 次セッション復帰ガイド

## 30秒 status
ベストフィット問題集準拠の演習用Web教材を単元ごとに量産中。直近で **02-07「デジタル化された情報とその表し方」** と **思考のステップ2「加法混色と減法混色」** を新規作成し、それぞれ audit-review まで通して **commit & push 済み**(submodule mikikof-lab 937105f / 親 my-company 1140f6d)。次に作るなら **2章 思考のステップ3、または 3章08 ハードウェアとソフトウェア** が自然な続き。

## 完成済み単元(articles/)
- 01-01 情報とメディア / 01-02 問題解決 / 01-03 知的財産権 / 01-04 セキュリティと法規 / 01 思考のステップ1
- 02-05 情報デザインの基礎 / 02-06 情報デザインの応用
- **02-07 デジタル化された情報とその表し方** — 計算主体。おさらい7領域(例題30-38凝縮)+ 演習14問(類題54-61 + 練習62-67)。self型13 + multi自動採点1(問58)。原本図3枚 + 自作SVG5点(デジタル化マップ/標本化・量子化波形/混色mix-blend/フィルムストリップ/ランレングス)。`_build_0207.py` 同梱。
- **02-thinking-step-2 加法混色と減法混色(本セッション新規)** — 共通テスト型の色彩思考。おさらい3領域(L/M/S錐体表・加法/減法混色・インク吸収)+ 演習2問(問ア〜エ=self×4 / 解いて定着=single 5択)。原本図2枚(シアン=赤吸収/マゼンタ+イエロー=緑青吸収)+ 混色SVG(mix-blend)再利用 + 錐体表(HTML)。`_build_ss2.py` 同梱。`<p>`分離は `<div` も検出する版に改良。

## この単元で確立した知見(次回必読)
- **計算問題は `self`型を主軸に**。原本の正答が「計算結果の数値」の場合、自動採点は表記ゆれで破綻するので self(模範解答reveal+自己採点○/△)が正解。すべて選べ系のみ `multi` 自動採点。
- **★docx 抽出は数式(m:t)を必ず含める**。`<w:t>` だけ抽出すると数式オブジェクト内の数値・文字コード値(例: 練習63の `0A(16)`/`0D(16)`/`20(16)`、55/56の変換対象、例題の 2進/16進値)が**まるごと欠落**する。欠落すると「文字コードの『LF』との『CR』」のような不自然な文も生む。抽出スクリプトは `<m:t>` も拾うこと(本単元の audit#1 でこの脱落を codex に検出された)。
- **おさらいの一般化記述は数学的に正しく**。教科書の「10進→n進=商が1になるまで割る」は2進専用で16進では破綻する。おさらい(自前合成)では「商が0になるまで割り、余りを下から並べる」と一般形で書く(audit#2 指摘)。
- **`<p>` の中に `<figure>`/`<blockquote>` を入れない**。stage_self は図/引用を `</p>` の外へ分離する実装にした(HTML妥当性)。新ステージでも踏襲。
- 句読点はキット慣例の **「、。」に統一**(原本の全角カンマ「，」→「、」)。02-06 以前と統一。ビルダーは NEW_MAIN を `.replace("，","、")` で正規化。

## 制作の不変ルール(従来どおり)
- ベース: 新規は `examples/01-01-...html` を cp が原則。ただし **`self`型を多用する単元は 02-06/02-07 を cp**(01-01 に self 型は無い)。
- 青基調トークン・モバイルUI v2(spotlight/haptic/カウントアップ/カルーセル)8フックは絶対に消さない。
- 原本図は §4.10b: `unzip docx → word/media/*` を Read で目視 → `assets/figN-{desc}.{ext}`。未使用の抽出図はコミットしない。
- self型カードは `digest_mod` のアイコン自動付与・viz必須(全問にviz)。Q60 のように viz 漏れに注意。

## 次にやること(新単元を作る場合)チェックリスト
- [ ] 原本パース: 問題 docx + 解答 docx の該当節。**m:t 込みで抽出**(上記知見)。
- [ ] 構成案を AskUserQuestion で合意(CLAUDE.md §6[2])。例題の扱い(おさらい凝縮 or 例題ステージ)とスコープを確認。
- [ ] `_build_0207.py` を雛形に流用(self/multi 型ヘルパー・SVG・splice・JS配列差替・句読点正規化が入っている)。エンジンCSS/JSは保全。
- [ ] 全問 原本と1問ずつ照合 → headless 実機目視 → /brushup /visual → /audit-review ×2(教科書準拠・web禁止)→ examples凍結 → index登録 → submodule→親の順で push。

## ポインタ
- 直近 commit: submodule `b249661` / 親 `d7d14c8`(両方 push 済み)
- audit ログ: `.company/audit/reviews/2026-06-21/0319-practices-0207-digital-info/`(r1)・`0341-practices-0207-digital-info-rev2/`(r2)
- 制作哲学=`practices/CLAUDE.md` / 技術=`skills/interactive-practice/SKILL.md` / 部品=`components.md` / 02-07 ビルダー=`articles/02-07-digital-info-representation/_build_0207.py`

## 2026-09-10 追記 — 03-09「2進数と論理演算」

- 生成器 `articles/03-09-binary-and-logic/_build_0309.py`（02-07 の例を SRC に、03-08 と同じ差し替え方式）。**例題は 03-08 と同じ「例題ツアー」の段**（おさらいに畳まない）。計算・記述は self 型、選べる問題（例題48 match／類題80・練習86・87 single）は自動採点。
- docx 抽出は `m:t` と下付き（`w:vertAlign`）と画像アンカー（`a:blip` → rels）まで拾う版（scratchpad `p0309/docx2txt2.py`。**次はこの版を practices 側へ置くこと**）。ド・モルガンの上線は `text-decoration: overline` で再現。
- 原本図は問題 docx 36 枚＋解答 docx 10 枚（類題75 の筆算 6・類題81 の解答回路 2・練習86 の値入り回路 2）。図記号の選択肢は `<img>` を選択肢の中に入れる（`inline_img`）。
- 落とし穴: `.self-q` は flex なので、問いの文に `<figure>` を並べると図が横に押し込まれる。`<div style="flex:1 1 auto;min-width:0">` で包む。2 進数リテラルは `white-space:nowrap`。17 列の表は 2 段に割る（横スクロールにしない）。
- index.html に 03-08・03-09 のカードを足した（03-08 は 8/3 の回で漏れていた）。凍結コピーは examples/03-09-binary-and-logic.html。

## 2026-09-12 追記 — 03-thinking-step-4「真理値表」

- 生成器 `articles/03-thinking-step-4/_build_ss4.py`。**02-thinking-step-2 の index.html を読んで `<main>` と JS 配列だけ差し替え、自分の index.html に書く**（自分自身を読み直さないので何度でも回せる）。数値は 3 路・4 路の表と問1 の 4 回路を assert で原本の解答と照合してから組む。
- 演習 3 問: 問（考えて納得の空欄 A〜D と図2 の X を self 型）／問1（single・正答 ②・回路図は選択肢の中に `<img>`）／問2（4 路スイッチ 8 行を self 型）。おさらい 3 領域（基本の回路・真理値表・図記号）には演習の答えを出さない。
- 原本図は問題 docx の media から 11 枚（fig1〜fig11）。考えて納得の解答図（image6）は使わず、解説では HTML の表で出す。
- 解答の解説は原文を引用した。数式画像が抜けて「」になっている文（行数 2^3 の行）は引用せず、自分の言葉の補足に回した。
- `情報Ⅰ_2学期/_ops/build_kai.py` が slug の無いフォルダを未作成と判定していたので直した。
- index.html に 3.S4 のカードを足し「12 units」に。凍結コピーは skills/interactive-practice/examples/03-thinking-step-4.html。
