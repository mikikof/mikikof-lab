---
updated: 2026-09-13
prev_session: 第6回（配列と添字）と第7回（二分探索）を一晩で通しで作り、各回3巡の監査（codex → /persona 6体 → 2巡目）を当て、4リポすべて push・配信して 200 を実測した。両回とも done
---

# 情報Ⅰ 2学期 — 次セッション resume（第8回 POINT 25 から）

## 1. 30 秒 status

- **第1〜7回すべて `status = "done"`。** 第6回＝POINT 20⑵（配列と添字・型D）、
  第7回＝POINT 22（二分探索・型A）。どちらも授業内3点がそろい、配信まで終わっている。
- **次は第8回 ＝ POINT 25。** 8 回で組む並びは `_ops/theme-plan.md` L90（… 第7回 22 → 第8回 25 → 第9回 26）。
  難所の候補と原本の重みは同ファイル §3 の 25 の行を見る（ここには写さない）。
- **第7回のアンカー教材は未作成**（lectures lec22 / practices 04-13）。第8回に入る前に作るかは本人判断。

## 2. 保全の状態（やり直さないこと）

| | 版 | 状態 |
|---|---|---|
| submodule (mikikof-lab) | `2a0f740` 第6・7回を追加、公開ゲートに §3 | **push 済み** |
| 親リポ (my-company) | `cee1f498` 第6・7回の本体 / `509f65d0` ORG.md | **どちらも push 済み** |
| joho-explainer | `a4063c0` 解説ツール 2 本を追加（11 カード） | **push 済み・200 実測** |
| joho-quiz | `767de19` セット 2 つを追加（11 セット） | **push 済み・200 実測** |

**公開の実測（9/13）**: 解説ツール 2 本、`?s=9` / `?s=10`、回のランディング 2 本とも 200。
**`02_プリント/` と `_teacher/` は 404**（非公開のまま）を確認済み。

**残るローカル commit はこの resume だけ**（push しない仕様）。

## 3. 確定事項（変えない前提）

- **語尾は3点で分ける。** 解説ツール＝丁寧体／プリント＝常体「答えなさい」／速テスト＝常体「選べ・答えよ」。
  **統一しない。**
- **読点は「、」で通す。** 印刷の生成器に、出力へ「，」が出たら throw するゲートが入っている。
- **速テストの set_index は 9（第6回）・10（第7回）。** 次は 11。
- **添字の起点は「その問題が与える」と書く。**「いつも 0 から」と言い切らない（`theme-plan.md` L82）。
- **二分探索で中央を残すと止まるのは、配列に無い値すべてと末尾の値だけ。**
  末尾の一つ手前は 3 回で見つかる。「末尾に近い値」「無い値のときだけ」はどちらも誤り。

## 4. オープン（本人の判断待ち・私からは動かさない）

- [ ] **第7回プリントの分量。** 15 分に対して記入 48 マス・手でたどる 18 手で、実測 1.3 倍。
  原本の実習を削らずに減らす道がない。記入表 B を問二の直下へ移して「時間切れで落ちるのが問二」の形だけ
  先に解消してある。**授業で測ってから決める。**
- [ ] **push 済みの 01〜05 台帳に残る解答 PDF の引用**（02 に 2 件）。作業ツリーは直せるが履歴からは消えない。
- [ ] **lec22 / practices 04-13 を作るか**（第7回のアンカー教材）。

## 5. 実行環境 / コマンド（コピペで動く）

```bash
HUB=~/my-company/.company/education/high-school/mikikof-lab/情報Ⅰ_2学期
W=~/my-company/.company/media/webツール/情報

# 回フォルダを組む（派生物。手で育てない）
cd "$HUB" && python3 _ops/build_kai.py 8

# 公開安全ゲート（§3 で台帳の中身も読む）。exit 0 でなければ push しない
cd "$HUB" && python3 _ops/check_public.py

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

# 配信
~/joho-explainer/sync_from_dev.sh && cd ~/joho-explainer && git add -- <files> && git commit && git push
cp "$W/スピードクイズ/data/questions.js" ~/joho-quiz/data/ && cd ~/joho-quiz && git commit -- data/questions.js && git push
```

## 6. 残工程チェックリスト（第8回に入るとき）

- [ ] Phase 0: `_ops/theme-plan.md` §3 の 25 の行を読み、**難所を 1 つ確定**してから `_ops/kai/08-<slug>.toml` を先に置く
- [ ] Phase 1: 数理を独立に検算し、原本で裏取りする（**web 検索しない**）
- [ ] Phase 2: 授業内3点（解説ツール → 印刷プリント → 速テスト）
- [ ] Phase 4: `../CLAUDE.md` §7 の整合ゲート 7 項目
- [ ] Phase 5: `build_kai.py 8`
- [ ] Phase 6: 配信（joho-explainer → joho-quiz）
- [ ] Phase 7: `/audit-review` → 5 件以上直したら再監査 → `check_public.py` exit 0 → push（submodule → 親）

## 7. 作業方針（前回の反省から）

- **監査を起動したら対象を凍結する。** 走行中に直し続けたので、2 巡目の 8 件中 2 件が
  「直す前の版への指摘」になった。待っている間は監査が読まない範囲を進める。
- **動く成果物には「実物を操作する」体を必ず入れる。** 前回の最重要の誤り（図が探索対象を含む半分を
  捨てていた）は、何も溢れないので機械ゲートは全部緑、抜粋を読む 5 体も届かなかった。
- **直しは穴を開ける。** 5 件以上直したら再監査、は形式ではない。
- **公開台帳に解答と原本の逐語を書かない。** `check_public.py` §3 が読む。自分の追記にも当てる。
- **`git add -A` を使わない。** 親リポは別セッションと同居していて、作業ツリーに 100 件超の他人の変更がある。

## 8. ポインタ

- 回の設計と進行台本: `_ops/kai/06-nuketa-ato-no-soeji.md` / `07-nibun-tansaku-han-i.md`
- 答えと数値の正本（非公開）: `$W/{edu-explainer-kit,印刷教材,スピードクイズ}/specs/`
- 監査ログ（2026-09-13）: `~/my-company/.company/audit/reviews/2026-09-13/` の
  `0443`(第6回 codex) / `0508`(第6回 persona) / `0516`(第7回 codex) /
  `0545`(第6回 rev2) / `0550`(第7回 persona 6体) / `0642`(第7回 rev2)
- 規則の正本: `../CLAUDE.md`（このハブ）／各キットの `CLAUDE.md` と `reference/reproduction-regime.md`
