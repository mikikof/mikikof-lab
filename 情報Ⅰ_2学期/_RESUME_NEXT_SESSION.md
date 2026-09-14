---
updated: 2026-09-14
prev_session: 第8回（POINT 25 更新の順序）と第9回（POINT 26 待ち行列の開始時刻）を授業内3点そろえて作り切り、codex 監査を 6 巡回した。図の検査を 4 本から 7 本へ増やし、単元固有の判定照合を 1 本足した。4 リポとも push 済み、公開 URL 9 本 200 を実測。これで2学期の授業回は全部終わった。
---

# 情報Ⅰ 2学期 — 次セッション resume

## 1. 30 秒 status

- **2学期の授業回は第9回で完結した。** `_ops/theme-plan.md` L90 の「8 回のときの並び」は
  第2回 15 → 第3回 16 → 第4回 17 → 第5回 20⑴ → 第6回 20⑵ → 第7回 22 → 第8回 25 → **第9回 26** で終わり。
  POINT 26 は同ファイルで「2学期の締め」と書かれている。**第10回は無い。**
- **第1〜9回すべて `status = "done"`。** 授業内3点（解説 25 分／プリント 15 分／速テスト 10 分）が
  そろい、配信まで終わっている。回の一覧から「準備中」の札も外れた（14:56 に公開版で確認）。
- **次にやることは 2 系統。** ①3学期（5章・6章）を起こす ②2学期で作らなかった自習用の
  アンカー教材を作る。どちらを先にするかは本人判断（§4）。

## 2. 保全の状態（やり直さないこと）

| | 版 | 状態 |
|---|---|---|
| submodule (mikikof-lab) | `7839db3` 第8回・第9回を done にし、台本の status を台帳へ揃えた | **push 済み** |
| 親リポ (my-company) | `cf038c99` 第8回・第9回 done ＋ 公開ゲートの穴の記録 | **push 済み** |
| joho-explainer | `cf6479f` 第8回・第9回の解説ツールを公開 | **push 済み・200 実測** |
| joho-quiz | `75a11ac` セット 11・12 を追加（全 13 セット） | **push 済み** |

**公開の実測（9/14 14:4x〜14:56）**
```
200  https://mikikof.github.io/joho-explainer/
200  https://mikikof.github.io/joho-explainer/update-order/          （00-ichidan も 200）
200  https://mikikof.github.io/joho-explainer/queue-start-time/      （01-osoi も 200）
200  https://mikikof.github.io/joho-quiz/
200  https://mikikof.github.io/mikikof-lab/情報Ⅰ_2学期/              （「準備中」0 件）
200  .../情報Ⅰ_2学期/第08回_koushin-no-junjo/01_解説/update-order/
200  .../情報Ⅰ_2学期/第09回_osoi-hou-wo-toru/01_解説/queue-start-time/
```

**出荷時のゲートの値（第8回・第9回）**
```
gate_all NG 0 / knobs 0 dead / present 0 NG・0 err / draw_bounds 0-9 / bounds_stages 0-33
text_overlap 0-66（390・820・1440 の 3 幅）/ text_on_shape 0-168・0-215 / check_verdict 0-63
印刷 A4 上限 1123px：更新の順序 781・1016 / 986・1043　待ち行列 848・1038 / 875・920・644
check_public.py exit 0（§1）
```

**残るローカル commit はこの resume だけ**（push しない仕様）。

## 3. 確定事項（変えない前提）

- **語尾は3点で分ける。** 解説ツール＝丁寧体／プリント＝常体「答えなさい」／速テスト＝常体「選べ・答えよ」。
  **統一しない。** 解説ツールの中はさらに3層（散文＝丁寧体／`.hk-num` の数値台帳＝常体／
  図の中の文字＝常体）。正本は `edu-explainer-kit/_series/REGIME.md`。
- **読点は「、」で通す。** ただし**出力に「，」が出たら throw するゲート `gateJP` は、
  印刷の生成器 9 本のうち 4 本にしか入っていない**（二分探索の範囲・待ち行列の開始時刻・
  更新の順序・配列と添字のずれ）。実際 `繰り返しの範囲_問題.html`（第5回）に「，」が 3 件残っている。
- **速テストの set_index は 11（第8回）・12（第9回）で、全 13 セット。**
- **解説ツールはシリーズ形**（1回＝3ページ＋回ハブ）。`_src/` が正本で、出力 HTML は手で直さない。
- **`_src` は配布しない。** `build_kai.py` の `ignore_patterns` と `sync_from_dev.sh` の
  `rm -rf .../_src` の**両方**で止めてある。
- **`build_kai.py` は回番号を 1 つしか受け取らない。** `build_kai.py 8 9` と渡すと
  第8回だけ組んで第9回を**黙って捨てる**。1 つずつ渡すか `--all`。
- **`check_public.py` の場所は `情報Ⅰ_2学期/_ops/`。** リポジトリ直下ではない。
  **単独で呼び、exit code を読んでから、別のコマンドで push する。**
  9/14 にゲートと push を同じコマンドに繋ぎ、パス誤りでゲートが exit 2 で落ちたまま
  public リポへ push している（走らせ直して §1 は exit 0 だった）。

## 4. オープン（本人の判断待ち・私からは動かさない）

- [ ] **3学期に入るか、先にアンカー教材を作るか。**
      3学期（5章・6章）は `_ops/theme-plan.md` L93：必ず 37⑴・37⑵、回数があれば 28⑴ → 30 → 31 → 29。
      27・28⑵・32〜36 は自習。
- [ ] **未作成のアンカー教材 5 本。** lectures `lec22`（第7回）・`lec25`（第8回）・`lec26`（第9回）、
      practices `04-13`（第7回）・`04-15`（第8回・第9回で共用）。
      `build_kai.py` が毎回 `[未完]` で報告する。授業は済んでいるので、自習用として作るかどうか。
- [ ] **mikikof-lab（public）に追跡されている版元由来 62 件。**
      素材 55 件（ベストフィット問題33・同解答9・学習ノート問題8・daisu-column source3・lectures _source2）に加え、
      **同じ逐語を抱えた生成器 `practices/articles/*/_build_*.py` 7 本**。
      `_build_0309.py` には 40 字超の日本語リテラルが 186 本あり、全角カンマ「，」のままの文も残る。
      `check_public.py` §2 はパスで数えるので生成器を計上していない。
      履歴からの除去は public リポの書き換えなので**オーナー判断**。
      → `secretary/todos/2026-09-14.md`（期限 2026-09-21）
- [ ] **第7回プリントの分量。** 15 分に対して実測 1.3 倍。授業で測ってから決める。
- [ ] **push 済み 01〜05 台帳に残る解答 PDF の引用**（02 に 2 件）。履歴からは消えない。

## 5. 実行環境 / コマンド（コピペで動く）

```bash
HUB=~/my-company/.company/education/high-school/mikikof-lab/情報Ⅰ_2学期
W=~/my-company/.company/media/webツール/情報

# 回フォルダを組む（派生物。手で育てない）★ 回番号は 1 つずつ。複数渡すと黙って捨てられる
cd "$HUB" && python3 _ops/build_kai.py 10
cd "$HUB" && python3 _ops/build_kai.py --all     # 全回を組み直す
cd "$HUB" && python3 _ops/build_kai.py --index   # ハブの一覧だけ

# 公開安全ゲート ★ 単独で呼び、exit を読んでから push する（push と同じコマンドに繋がない）
cd "$HUB" && python3 _ops/check_public.py ; echo "exit=$?"

# 解説ツール（シリーズ形）を組む＋検査 7 本
cd "$W/edu-explainer-kit"
python3 _series/build_series.py <series>
python3 _series/qa/gate_all.py          <series>   # ★ 単独で先に（他の検査が作る _*.html を拾う）
python3 _series/qa/check_knobs.py       <series>
python3 _series/qa/check_present.py     <series>
python3 _series/qa/check_draw_bounds.py <series>
python3 _series/qa/bounds_stages.py     <series>           # 段階ごとのはみ出し
python3 _series/qa/text_overlap.py      <series> --widths=390,820,1440
python3 _series/qa/text_on_shape.py     <series>           # 文字を描かず下地の画素を読む
# 撮影（目視用）。★ dist に一時ファイルを書くので、検査と同時に走らせない
python3 _series/qa/shot.py              <series>

# 第9回だけの判定照合（決め方3×調理3×人7＝63 組。印と色の両方を見る）
cd "$W/edu-explainer-kit" && python3 dist/queue-start-time/_src/check_verdict.py

# 印刷プリントを生成（内部検算と読点ゲートを通る）★ gateJP は 9 本中 4 本にしか入っていない
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

## 6. 残工程チェックリスト（新しい回に入るとき）

- [ ] Phase 0: `_ops/theme-plan.md` を読み、**難所を 1 つ確定**してから `_ops/kai/<回>-<slug>.toml` を先に置く
- [ ] Phase 1: 数理を独立に検算し、原本で裏取りする（**web 検索しない**）
- [ ] Phase 2: 授業内3点（解説ツール → 印刷プリント → 速テスト）。
      解説ツールはシリーズ形（`edu-explainer-kit/_RESUME_NEXT_SESSION.md` の手順に従う）
- [ ] Phase 3: 実寸の目視（PC 1440 / スマホ 390 は iframe / 補足モーダル / ダーク）。
      **機械の検査が全部緑でも、ここで実欠陥が出る。**
- [ ] Phase 4: `../CLAUDE.md` §7 の整合ゲート 7 項目
- [ ] Phase 5: `build_kai.py <回>`（1 つずつ）
- [ ] Phase 6: 配信（中間層 → joho-explainer → joho-quiz）
- [ ] Phase 7: `/audit-review` → 5 件以上直したら再監査 → `check_public.py` を**単独で**走らせ
      exit 0 を読む → push（submodule → 親）

## 7. 作業方針（実測した反省から）

- **同じ量を計算している場所は、1 か所直して終わりにならない。**
  第8回の「足りなくなったら止める」は段階①②③と補足の 4 か所にあり、rev2→rev3→rev4 と
  3 巡かけて全部に行き渡った。直す前に、その量を計算している行を grep で全部数える。
  同じ型が 9/14 だけで 3 件（他 2 件はゲートと push の連結、台帳と台本の status 二重管理）。
- **「走らせたつもり」は走らせたことにならない。** 出力に「やった」と書かれた行が
  **期待した数だけあるか**を数える。`build_kai.py 8 9` は第9回を黙って捨てた。
- **「0 件」は「測っていないから 0」かもしれない。** `text_overlap.py` は末尾が `sys.exit()` なので
  `exec_module` で読み込むとラッパーごと死に、「重なり 0 件 / 測った段階 0」と出す。分母を先に見る。
- **判定は印と色の両方を照合する。** ✓ が warn 地の上に乗る組合せが 63 通り中 14 通りあった。
- **新しい検査は壊して鳴らす。** `check_knobs` は隠して NG 2、`check_verdict` は
  直す前のビルドで 14 件を検出させて、初めて信用した。
- **監査を起動したら対象を凍結する。** 走行中に直し続けると「直す前の版への指摘」が返る。
- **機械が緑でも実寸で見る。** 7 本そろえた回では目視だけで実欠陥が 34 件出た。
  最も多いのは**名前と中身のずれ**（凡例に緑と書いてあるのに図に緑が無い）で、どの検査も原理的に鳴らない。
- **検査の道具を同時に走らせない。** `shot.py` は `dist/` に一時ファイルを書き、
  `dist/*.html` を glob する検査がそれを測って落ちる。
- **`git add -A` を使わない。** 親リポは別セッションと同居していて、作業ツリーに他人の変更がある。
- **日本語の一括置換は python で行う。** `perl -CSD -pi -e` は `-e` の中の日本語リテラルを
  復号せず、**置換が黙って何もしない**。
- **公開台帳に解答と原本の逐語を書かない。** `check_public.py` §3 が読む。自分の追記にも当てる。

## 8. ポインタ

- 回の設計と進行台本: `_ops/kai/01〜09-*.md`（01・02・03・07 に 2026-09-14 の「改訂の記録」がある）
- 回の台帳（正本）: `_ops/kai/01〜09-*.toml`。**`status` は台本 .md の front-matter にも
  あるが読まれていない。** 消して 1 か所にするのは、次に台本の形を触るときに行う。
- 答えと数値の正本（非公開）: `$W/{edu-explainer-kit,印刷教材,スピードクイズ}/specs/`
- 解説ツールの制作再開メモ: **`$W/edu-explainer-kit/_RESUME_NEXT_SESSION.md`**（検査 7 本の回し方）
- 版面の正本: `$W/edu-explainer-kit/_series/REGIME.md`
- 監査ログ（2026-09-14・各 6 巡）: `~/my-company/.company/audit/reviews/2026-09-14/`
  `0700-joho2-kai08/` と `0700-joho2-kai09/`（`02-feedback` が 1 巡目、`14-rev6-feedback` が 6 巡目）
- 決定の記録: `~/my-company/.company/secretary/notes/2026-09-14-decisions.md`（533 行）
- 作業ログ: `~/my-company/.claude/session-logs/2026-09-14.md`
- 規則の正本: `../CLAUDE.md`（このハブ）／各キットの `CLAUDE.md` と `reference/reproduction-regime.md`
