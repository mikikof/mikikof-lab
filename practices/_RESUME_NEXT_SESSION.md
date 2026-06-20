---
updated: 2026-06-21
prev_session: "02-07「デジタル化された情報とその表し方」を新規作成 → brushup/visual/audit-review×2 まで完走・push 済み"
---

# practices(Interactive Practice Lab)— 次セッション復帰ガイド

## 30秒 status
ベストフィット問題集準拠の演習用Web教材を単元ごとに量産中。直近で **02-07「デジタル化された情報とその表し方」** を新規作成し、brushup・visual・audit-review を2巡通して **commit & push 済み**(submodule mikikof-lab b249661 / 親 my-company d7d14c8)。次に作るなら **2章の残り(思考のステップ2 など)または 3章** が自然な続き。

## 完成済み単元(articles/)
- 01-01 情報とメディア / 01-02 問題解決 / 01-03 知的財産権 / 01-04 セキュリティと法規 / 01 思考のステップ1
- 02-05 情報デザインの基礎 / 02-06 情報デザインの応用
- **02-07 デジタル化された情報とその表し方(本セッション新規)** — 計算主体。おさらい7領域(例題30-38凝縮)+ 演習14問(類題54-61 + 練習62-67)。self型13 + multi自動採点1(問58)。原本図3枚(文字コード表/16×16グリッド/2進筆算)+ 自作SVG5点(デジタル化マップ/標本化・量子化波形/混色mix-blend/フィルムストリップ/ランレングス)。再現ビルダー `_build_0207.py` 同梱。

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
