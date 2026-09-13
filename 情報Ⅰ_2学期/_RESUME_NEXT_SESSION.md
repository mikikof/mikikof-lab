---
updated: 2026-09-14
prev_session: 解説ツールを第6回から第1回まで逆順でシリーズ形へ移し、7 本すべてを「1回＝3ページ＋回ハブ」にそろえた。共有部品の欠陥 2 件（ダークの判定バナー・図の折り返し）を出荷済みのぶんまで遡って修正。第7回の残欠陥と孤立ファイルも解消。3 リポとも push し、公開 URL 7 本 200 を実測。授業内3点の中身（数理・プリント・速テスト）は触っていない。
---

# 情報Ⅰ 2学期 — 次セッション resume（第8回 POINT 25 から）

## 1. 30 秒 status

- **第1〜7回すべて `status = "done"`。** 授業内3点がそろい、配信まで終わっている。
- **解説ツールは 7 本ともシリーズ形**（1回＝3ページ＋回ハブ）になった。
  `_ops/kai/*.toml` の `explainer` は 7 本ともディレクトリ形（`<slug>/`）。
  旧の単一 HTML は回フォルダ・中間層・配布リポの 3 か所とも削除済み。
- **次は第8回 ＝ POINT 25。** 8 回で組む並びは `_ops/theme-plan.md` L90（… 第7回 22 → 第8回 25 → 第9回 26）。
  難所の候補と原本の重みは同ファイル §3 の 25 の行を見る（ここには写さない）。
- **第6回・第7回のアンカー教材は未作成**（lectures lec22 / practices 04-13）。第8回に入る前に作るかは本人判断。

## 2. 保全の状態（やり直さないこと）

| | 版 | 状態 |
|---|---|---|
| submodule (mikikof-lab) | `368cec2` 第7回の図の直し（第1〜7回のシリーズ化を含む） | **push 済み** |
| 親リポ (my-company) | `562fb3cc` ORG.md ／ `e7765e6c` 第7回の図と残骸 | **どちらも push 済み** |
| joho-explainer | `3fe2a03` 7 本ともディレクトリ形 | **push 済み・200 実測** |
| joho-quiz | `767de19` セット 11 個（第7回まで） | **push 済み**（今回は触っていない） |

**公開の実測（9/14）**: 解説ツール 7 本とハブが 200。置き換えた旧 `<slug>.html` は 7 本とも 404。
`02_プリント/` と `_teacher/` が 404（非公開）であることは 9/13 に確認済み。

**残るローカル commit はこの resume だけ**（push しない仕様）。

## 3. 確定事項（変えない前提）

- **語尾は3点で分ける。** 解説ツール＝丁寧体／プリント＝常体「答えなさい」／速テスト＝常体「選べ・答えよ」。
  **統一しない。**
- **読点は「、」で通す。** 印刷の生成器に、出力へ「，」が出たら throw するゲートが入っている。
- **速テストの set_index は 9（第6回）・10（第7回）。次は 11。**
- **添字の起点は「その問題が与える」と書く。**「いつも 0 から」と言い切らない（`theme-plan.md` L82）。
- **二分探索で中央を残すと止まるのは、配列に無い値すべてと末尾の値だけ。**
  末尾の一つ手前は 3 回で見つかる。「末尾に近い値」「無い値のときだけ」はどちらも誤り。
- **解説ツールはシリーズ形で作る**（1回＝3ページ＋回ハブ）。版面の正本は
  `media/webツール/情報/edu-explainer-kit/_series/REGIME.md`。
  **制作の詳細な再開メモは `edu-explainer-kit/_RESUME_NEXT_SESSION.md`**（ゲートの回し方・
  撮影の道具・7 本そろえる過程で足した規律が入っている）。
- **`_src` は配布しない。** `series.toml` に授業の時間配分と非公開の答え台帳のパスが入っている。
  `build_kai.py` の `ignore_patterns` と `sync_from_dev.sh` の `rm -rf .../_src` の**両方**で止めてある。

## 4. オープン（本人の判断待ち・私からは動かさない）

- [ ] **第7回プリントの分量。** 15 分に対して記入 48 マス・手でたどる 18 手で、実測 1.3 倍。
  原本の実習を削らずに減らす道がない。記入表 B を問二の直下へ移して「時間切れで落ちるのが問二」の形だけ
  先に解消してある。**授業で測ってから決める。**
- [ ] **push 済みの 01〜05 台帳に残る解答 PDF の引用**（02 に 2 件）。作業ツリーは直せるが履歴からは消えない。
- [ ] **lec22 / practices 04-13 を作るか**（第6回・第7回のアンカー教材）。

## 5. 実行環境 / コマンド（コピペで動く）

```bash
HUB=~/my-company/.company/education/high-school/mikikof-lab/情報Ⅰ_2学期
W=~/my-company/.company/media/webツール/情報

# 回フォルダを組む（派生物。手で育てない）
cd "$HUB" && python3 _ops/build_kai.py 8

# 公開安全ゲート（§3 で台帳の中身も読む）。★ パイプを通さず exit code を直に見る
cd "$HUB" && python3 _ops/check_public.py

# 解説ツール（シリーズ形）を組む＋ゲート4本。詳細は edu-explainer-kit/_RESUME_NEXT_SESSION.md
cd "$W/edu-explainer-kit"
python3 _series/build_series.py <series>
python3 _series/qa/gate_all.py          <series>   # ★ 単独で先に（他のゲートが作る _*.html を拾う）
python3 _series/qa/check_knobs.py       <series>
python3 _series/qa/check_present.py     <series>
python3 _series/qa/check_draw_bounds.py <series>

# 印刷プリントを生成（内部検算と読点ゲートを通る）
cd "$W/印刷教材/dist" && node _gen_<単元>.js

# A4 に収まるかを実測（上限 1123px ＝ 297mm。overflow:hidden なので測らないと無音で切れる）
cd "$W/印刷教材/dist" && python3 - <<'PY'
import pathlib
inj = """<script>window.addEventListener('load',function(){
var st=document.createElement('style');
st.textContent='.sheet{width:210mm!important;height:auto!important;min-height:0!important;padding:15mm 16mm 14mm!important;overflow:visible!important;margin:0!important}';
document.head.appendChild(st);
var o=[].map.call(document.querySelectorAll('.sheet'),function(s,i){return 'S'+(i+1)+'='+Math.round(s.offsetHeight)});
document.title='MEAS|'+o.join('|');});</script>"""
for k in ("問題","解答"):
    p = pathlib.Path("<単元>_%s.html" % k)
    pathlib.Path("_m_%s.html" % k).write_text(p.read_text(encoding="utf-8").replace("</head>", inj+"</head>",1), encoding="utf-8")
PY
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-sandbox --virtual-time-budget=5000 \
  --dump-dom "file://$PWD/_m_問題.html" 2>/dev/null | grep -o 'MEAS|[^<]*'
rm -f _m_*.html

# 監査（web 禁止・教科書準拠。背景実行は < /dev/null 必須）
codex exec -p review-paper --sandbox read-only "$(cat <LOG>/01-prompt.md)" \
  < /dev/null > <LOG>/02-feedback.md 2>&1

# 配信（解説ツールは 中間層 → 配布 の 2 段。中間層を飛ばすと sync が止まる）
rsync -a --delete --exclude='_src' "$W/edu-explainer-kit/dist/<series>/" "$W/<series>/"
~/joho-explainer/sync_from_dev.sh && cd ~/joho-explainer && git add -- <files> && git commit && git push
cp "$W/スピードクイズ/data/questions.js" ~/joho-quiz/data/ && cd ~/joho-quiz && git commit -- data/questions.js && git push
```

## 6. 残工程チェックリスト（第8回に入るとき）

- [ ] Phase 0: `_ops/theme-plan.md` §3 の 25 の行を読み、**難所を 1 つ確定**してから `_ops/kai/08-<slug>.toml` を先に置く
- [ ] Phase 1: 数理を独立に検算し、原本で裏取りする（**web 検索しない**）
- [ ] Phase 2: 授業内3点（解説ツール → 印刷プリント → 速テスト）。
      **解説ツールはシリーズ形**（`edu-explainer-kit/_RESUME_NEXT_SESSION.md` の手順に従う）
- [ ] Phase 3: 実寸の目視（PC 1440 / スマホ 390 は iframe / 補足モーダル / ダーク）。
      **機械のゲートが全部緑でも、ここで実欠陥が出る。**
- [ ] Phase 4: `../CLAUDE.md` §7 の整合ゲート 7 項目
- [ ] Phase 5: `build_kai.py 8`
- [ ] Phase 6: 配信（中間層 → joho-explainer → joho-quiz）
- [ ] Phase 7: `/audit-review` → 5 件以上直したら再監査 → `check_public.py` exit 0 → push（submodule → 親）

## 7. 作業方針（前回までの反省から）

- **監査を起動したら対象を凍結する。** 走行中に直し続けると「直す前の版への指摘」が返る。
- **動く成果物には「実物を操作する」体を必ず入れる。** 機械ゲートが全部緑でも、
  実寸で見ると欠陥が出る。7 本そろえた回では**目視だけで実欠陥が 34 件**出た。
  最も多かったのは**名前と中身のずれ**（凡例に緑と書いてあるのに図に緑が無い／
  入力が 1 つになったのに指標が「いまの組合せ」のまま）で、どの検査も原理的に鳴らない。
- **検査そのものが壊れていないかを疑う。** 撮影が段階を切り替えられず、
  **空振りしても撮影は成功する**ので 2 ページの場面 2 以降が一度も目視されていなかった。
  はみ出し検査は**最悪の 1 件しか名指ししない**ので、1 つ直すと次が出る。
- **直しは穴を開ける。** 5 件以上直したら再監査、は形式ではない。
- **公開台帳に解答と原本の逐語を書かない。** `check_public.py` §3 が読む。自分の追記にも当てる。
  （「1 回＝ 3 ページ」の「＝ 3」が等式として警告に出るが、これは誤検出）
- **`git add -A` を使わない。** 親リポは別セッションと同居していて、作業ツリーに他人の変更がある。
- **日本語の一括置換は python で行う。** `perl -CSD -pi -e` は `-e` の中の日本語リテラルを復号せず、
  **置換が黙って何もしない**。置換後は読み直して確かめる。

## 8. ポインタ

- 回の設計と進行台本: `_ops/kai/01〜07-*.md`（01・02・03・07 には 2026-09-14 の「改訂の記録」がある）
- 答えと数値の正本（非公開）: `$W/{edu-explainer-kit,印刷教材,スピードクイズ}/specs/`
- 解説ツールの制作再開メモ: **`$W/edu-explainer-kit/_RESUME_NEXT_SESSION.md`**（2026-09-14）
- 版面の正本: `$W/edu-explainer-kit/_series/REGIME.md`
- 監査ログ（2026-09-13）: `~/my-company/.company/audit/reviews/2026-09-13/` の
  `0443`(第6回 codex) / `0508`(第6回 persona) / `0516`(第7回 codex) /
  `0545`(第6回 rev2) / `0550`(第7回 persona 6体) / `0642`(第7回 rev2)
  ※ 2026-09-14 のシリーズ化では監査を回していない（版面の作業で、内容は変えていないため）
- 作業ログ: `~/my-company/.claude/session-logs/2026-09-14.md`
- 規則の正本: `../CLAUDE.md`（このハブ）／各キットの `CLAUDE.md` と `reference/reproduction-regime.md`
