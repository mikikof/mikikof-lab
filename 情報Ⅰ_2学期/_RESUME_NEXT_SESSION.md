---
updated: 2026-09-13
prev_session: 第5回の個人学習教材（lectures lec20 / practices 04-12）を作り、codex 監査 3 件を全件適用し、submodule を push して配信まで確認した。第5回は完了
---

# 情報Ⅰ 2学期 — 次セッション resume（第6回 POINT 20⑵ から）

## 1. 30 秒 status

- **第5回は完了・配信済み。** 授業内3点（9/12 push）＋ **lec20** ＋ **practices 04-12** がそろい、
  `manifest.toml` は第1〜5回すべて `status = "done"`。ハブの一覧から「準備中」が消えた。
- **公開 URL は生きている**（9/13 03:29 実測・どちらも 200、監査の修正が反映された版）。
  一覧も `lectures = 18 UNITS` / `practices = 14 units` に増えている。
- 次は **第6回 ＝ POINT 20⑵（配列）**。アンカー教材は両方そろっているので**授業内3点だけ**作ればよい。

## 2. 保全の状態（やり直さないこと）

| | 版 | 状態 |
|---|---|---|
| submodule (mikikof-lab) | `6d1af39` 第5回: 個人学習教材 lec20 と practices 04-12 を保全 | **push 済み** |
| 親リポ (my-company) | `211f38ae` submodule 参照の追随 / `e0b8513e` 締め（ORG.md・決定事項） | **どちらも push 済み** |

**親リポの push の経緯**: 本人の判断で私からは push しなかった（当時、別セッションの未 push が混ざっており、
git はブランチ単位でしか押せないため）。その後、別セッションが親リポを push したので、私の 2 件も origin に載った。
**残っているローカル commit は submodule の `fa1ec5f`（この resume）だけ**で、これは push しない仕様。

**並行セッションのこと（9/13 深夜）**
- 親リポの `ee4e5966`（別セッションの persona 保存）に、**私の監査ログ 5 件が巻き込まれている**
  （`0115-joho2-kai05-jishu/` の 00〜03 と `_run.log`）。内容は正しいがコミットメッセージが実態と合わない。
  他セッションのコミットなので手を出していない。
- submodule では `b9de14c`「回の台帳を1回1ファイルに割る」が積まれ、**すでに push 済み**。
  `_ops/kai/*.md` → `*.toml` 化と `build_kai.py`・`CLAUDE.md` の書き換え。
  **`manifest.toml` には触れていない**ので第5回の `done` と `[existing]` は無傷。

## 3. 次にやること — 第6回（POINT 20⑵ 配列）

入口は **`/joho-2gakki`**。難所はまだ決めていない。

**★ 台帳の作りが変わった（9/13 に別セッションが移行済み。確認は済んでいる）**:

- 回の台帳は **`_ops/kai/NN-<slug>.toml`**、進行台本は同名の **`.md`**。
- `manifest.toml` は共有の設定（paths / hubs / anchor_map）だけで、**回は書かない**。
  `[[kai]]` や `[existing]` を残すと `build_kai.py` が明示的に止まる。
- 出荷ゲートの条件も **`_ops/kai/NN-<slug>.toml` の `status = "done"`** に変わった（ハブ `CLAUDE.md` §8）。
- 第1〜5回はすべて `.toml` 側で `done` に移行済み。一覧の「準備中」は 0 件。

材料はもう手元にある（lec20 で 20⑵ 全体を扱ったため）:
- 学習ノート 20⑵ の POINT ①配列（リスト）②要素（＋添字）③一次元配列 ④二次元配列、実習1〜5 の正答
- 4 章 章末2（while を抜けたあとの添字は 1 つ先）
- ベストフィット 04-12 の例題57・58、類題102・103（配列の問題群）
- **難所の候補**: 「添字は 0 から」（型C 似て非なる：何番目 vs 添字）、
  「くり返しを抜けたあとの変数は 1 つ先を指す」（型D 数えると合わない・章末2）

## 4. 残工程チェックリスト

第6回（POINT 20⑵）:

- [ ] ハブ `CLAUDE.md` §11 を読む。**回番号は Phase 0 で先に取る**
      （`_ops/kai/06-<slug>.toml` を先に置く。同じ番号を 2 つのチャットが取ると `build_kai.py` が止まる）
- [ ] `_ops/theme-plan.md` §2b と `_ops/nansho-guide.md` を読み、**難所を 1 つ確定**する
- [ ] 台帳 `_ops/kai/06-<slug>.toml`（雛形 `_templates/kai.template.toml`）と
      進行台本 `_ops/kai/06-<slug>.md` を起こす（解答・原本の書き写しは入れない）
- [ ] 難所の数理を独立検算（原本で裏取り・**web 検索しない**）
- [ ] 解説ツール（25分・丁寧体）→ `media/webツール/情報/edu-explainer-kit/dist/`
- [ ] 印刷プリント（15分・常体）→ `media/webツール/情報/印刷教材/dist/`
- [ ] スピードテスト（10分・常体の指示）→ `スピードクイズ/data/questions.js` の `QUIZ_SETS[9]`
      （**正解の位置を散らす**。第2・3回で全問「ア」になった前科がある）
- [ ] 整合ゲート（ハブ `CLAUDE.md` §7）を 1 項目ずつ
- [ ] `python3 _ops/build_kai.py 6` → 進行台本を仕上げる
- [ ] 配信（`~/joho-explainer` / `~/joho-quiz` へ同期）
- [ ] `/audit-review`（web 禁止・教科書準拠・slug は `joho2-`）→ 必須指摘を適用（5 件以上なら再 audit）
- [ ] `python3 _ops/check_public.py` が exit 0
- [ ] `_ops/kai/06-<slug>.toml` の `status = "done"`（**manifest.toml には書かない**）

持ち越し（第5回の残り。急ぎではない）:

- [ ] `ee4e5966` に巻き込まれた監査ログ 5 件の扱い（コミットメッセージが実態と合わない）
- [ ] この resume 更新の commit は submodule にローカルで入れてある（未 push）

## 5. 実行環境 / コマンド

```bash
LAB="/Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab"
HUB="$LAB/情報Ⅰ_2学期"

# 回フォルダを組む / 一覧だけ作り直す / 公開安全ゲート
cd "$HUB" && python3 _ops/build_kai.py 6
cd "$HUB" && python3 _ops/build_kai.py --index
cd "$HUB" && python3 _ops/check_public.py          # exit 0 でなければ push しない

# 原本テキストの抽出（w:t と m:t の両方を拾う。w:t だけだと数式が落ちる）
python3 "$HUB/_ops/docx2txt2.py" /tmp/genpon \
  "$LAB/lectures/_source/学習ノート_問題/高校情1学習ノート（p.46～65）-4章プログラミングとシミュレーション-問題Word.docx" \
  "$LAB/practices/_source/ベストフィット問題/BF情1New-4章12プログラミング-問題（Python）.docx"
pdftotext -layout "$LAB/lectures/_source/高校情1学習ノート-解答PDF.pdf" - | less

# practices の生成器（04-12 が手本。検算を selfcheck() に内蔵）
cd "$LAB/practices/articles/04-12-programming" && python3 _build_0412.py

# 機械ゲート（HTML 共通）
F=<対象のindex.html>
python3 -c "s=open('$F').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'))"
python3 -c "s=open('$F').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
grep -oE 'font-size="[0-9.]+"' "$F" | grep -oE '[0-9.]+' | awk '$1<9{print "WARN <9px"}'

# 実機検査（★対象と同じディレクトリに検査用 HTML を置く。別の場所だと相対パスが切れる）
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1440,2700 --virtual-time-budget=10000 --screenshot=out.png "file://$F"

# codex 監査（プロファイルの実体は ~/.codex/<name>.config.toml。< /dev/null が必須）
cd .company/audit/reviews/$(date +%Y-%m-%d)/HHMM-joho2-kai06-3ten
codex exec -p review-paper --sandbox read-only "$(cat 01-prompt.md)" < /dev/null > 02-feedback.md 2>&1
grep -m1 -A6 "^model:" 02-feedback.md    # reasoning effort: high が出ていること
```

## 6. 確定事項（変えない前提）

- 授業 50 分＝解説ツール 25 分／印刷プリント 15 分／スピードテスト 10 分。**一回一難所**。
- 回フォルダは `build_kai.py` で組む派生物。手で育てない。
- 語尾: 解説ツール＝丁寧体／プリント＝常体・設問「答えなさい」／速テスト＝常体「選べ・答えよ」／
  lectures＝丁寧体／practices＝原本の問題文は原文のまま。**統一しない。**
- **用語の線（第5回で確定・第6回でも守る）**: range の 2 番目の数を「終了値」と呼ばない。
  教科書の「値1・値2・増減値」＋「値2 は含まれない」を使う。
  **学習ノート 20⑴ 実習1 の選択肢 c も `range(値1, 値2, 増減値)` と書いている**（今回の新しい裏取り）。
  ただし **practices は原本の文をそのまま載せる場所**なので、ベストフィットの「終了値」はそこだけ原文どおり。
- 正解は原本で裏取りし、**web 検索しない**。
- mikikof-lab は public。push 前に `check_public.py` が exit 0。
- **並行セッションがいる前提で `git add` はパスを明示する**（`-A` を使わない）。

## 7. 今回の教訓（次も同じ罠を踏む）

- **生成器の区間置換は行頭アンカー（`^` + `re.M`）で当てる。** アンカー無しだと、宣言より前にある
  エンジンの説明コメントに食いつき、そこから本体末尾まで飲み込む。今回は hosoku 補足エンジンが
  約 360 行まるごと消え、**7 つの自己点検は全部緑のままだった**。
  → assert に「残す側の在庫」（エンジンのマーカー＋関数総数の下限）を足した。消える側だけ数えても検出できない。
- **検査対象の操作 API は docs でなく実物から取る。** practices のエンジンは IIFE で包まれ
  `window` に何も公開していない。`goToStage` を直接呼ぼうとして落ちた。実 UI を押すのが正しい。
- **`position: fixed` の要素に `offsetParent` は使えない**（常に null）。miki 窓の可視判定を誤り、
  本命の検査を一度も走らせないまま 0 件と報告しかけた。
- **headless は、操作で文書が伸びてからスクロールすると空フレームで撮り終わる。**
  白紙（7KB）を見たら `display` / `opacity` / `elementFromPoint` / `scrollY` で撮影側かページ側かを切り分ける。
- **機械が全部緑でも、実物を見ないと出ない欠陥がある。** 今回も目視で 2 件出た。

## 8. ポインタ

- 監査ログ: `.company/audit/reviews/2026-09-13/0115-joho2-kai05-jishu/`
  （`01-prompt.md` が**事実台帳つきの渡し方の手本**。`03-plan.md` に採否と却下理由、`04-applied.md` に適用結果）
- 生成器: `practices/articles/04-12-programming/_build_0412.py`（追跡される正本・検算内蔵）
  lec20 は scratchpad の `patch_lec20.py` + `lec20_slides.py` + `lec20_data.py` で組んだ。
  **scratchpad は消えるので、lec20 を直すときは canonical から組み直すか HTML を直接編集する。**
- 作業ログ: `.claude/session-logs/2026-09-13.md`
- 決定と TODO: `.company/secretary/notes/2026-09-13-decisions.md`
- memory: `project_joho1_2gakki`、`feedback_bulk_replace_leaves_fragments`（行頭アンカー）、
  `feedback_headless_click_and_clip_traps`（罠3・罠4）、`feedback_headline_contradicted_by_own_material`

## 未決（本人の判断待ち）

- **practices の `assets/` に原本の解答図が public リポで追跡されている。**
  03-09 の `ans75-*.png`・`ans81-*.jpeg` 等。practices は解説を載せるサイトなので設計どおりではあるが、
  版元著作物の図である点は変わらない。既存3単元の運用に 04-12 も揃えた。変えるなら履歴からの除去が要る。
- 学習ノート 37 を lecture 2 本に割るか（`_ops/theme-plan.md` §5）。3学期の話。
