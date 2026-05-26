# 新規単元 一発制作プレイブック(lec11 canonical / 2026-05 確立)

このファイルは、**新しい授業単元を「一発で lec11 と同等クオリティ」に仕上げる**ための指示系統の最上位ドキュメントである。
`SKILL.md`(技術仕様)・`components.md`(部品)・`CLAUDE.md`(制作哲学)はこのプレイブックの下位に位置づけ、矛盾したらこのプレイブックを優先する。

> **canonical = `examples/11-analog-and-digital.html`(= `articles/11-analog-and-digital/index.html`)。**
> lec11 は miki.com NPC / hosoku 補足 / POINT スポットライト / P 文字ポップ / Space+もどす を全部備えた最新の完成形。
> **新規単元は「ゼロから組む」のではなく「lec11 をコピーして中身だけ差し替える」**。これが一発再現の核心。

---

## 0. 大原則 — 「エンジンは触らず、コンテンツだけ差し替える」

lec11 の `index.html` は大きく 2 層に分かれる。

| 層 | 中身 | 新規単元での扱い |
|---|---|---|
| **標準インタラクション層(エンジン)** | ナビ / メニュー / miki.com NPC / hosoku モーダル / スポットライト / P 文字ポップ / Space+もどす / a11y / スワイプ / 触覚 | **1 文字も変えずコピー**(verbatim) |
| **コンテンツ層** | タイトル・スライド本体・各データ構造(下記 §2)・単元固有インタラクションの CSS/JS | **単元の学習ノートに合わせて差し替え** |

エンジンを書き直すと品質が毎回ブレる。**エンジンは lec11 から byte 単位で受け継ぐ**こと。これが「一発で同クオリティ」の唯一の担保。

---

## 1. 着手前に必ず読む(順序厳守)

1. このプレイブック(全体の段取り)
2. `CLAUDE.md` — 制作哲学・答え後出し・原本照合(§4.8)・トーン
3. `SKILL.md` §2 Design Tokens / §9 落とし穴 / §13 アイコン / §14 標準インタラクション層
4. `examples/11-analog-and-digital.html` — **canonical。これを開いて構造を体に入れる**
5. **`_source/高校情1学習ノート-解答PDF.pdf` の該当ページ** — 正答の正本(これを読まずに書くと事故る)
6. 該当章の `_source/学習ノート_問題/*.docx` — POINT・実習の項番を python-docx で抽出

> **POINT 番号 = lec 番号**(`feedback_lectures_pointnum_equals_lecnum`)。章番号とは無関係。

---

## 2. コンテンツ差し替えインベントリ(これだけ替えれば一発)

lec11 をコピーした後、**以下のブロックだけ**を新単元用に差し替える。grep アンカーを添える。

### 2.1 HTML(head + topbar)
- `<title>…</title>`
- `.topbar-title` / `.topbar-subtitle`(`学習ノート POINT NN | p.XX`)/ `.topbar-chapter`(`CHAPTER · NN`)
- `.menu-head-sub`(`CHAPTER · NN`)

### 2.2 スライド本体(`<div class="slide-container">` 〜 その閉じ `</div>`)
- タイトルスライド / アジェンダ / 各セクション(仕切り + POINT + 実習)/ 答え合わせ / まとめツリー / 復習 / エンドカード
- 構成テンプレは `SKILL.md §1`。**POINT 項目ごとに「law-illust(SVGアイコン)+ タップ展開」+ 1スライド1リッチインタラクション**(`CLAUDE.md §4.9`)
- データ可視化が要る単元は **手を動かす HTML インタラクション**(lec11 の 8ビット変換機 / 2ⁿスライダー / 変換表 / ニブル分割図が手本)を「単元の目玉」として 1〜2 個必ず入れる

### 2.3 JS データ構造(grep して中身を入れ替える)
| 構造 | grep | 役割 | キー整合 |
|---|---|---|---|
| `window.HOSOKU_SUPP` | `window.HOSOKU_SUPP = {` | 難所の補足(7±2 件) | チップ `data-supp="KEY"` と 1:1 |
| `MIKI_GUIDE` | `const MIKI_GUIDE = {` | スライド毎の miki ナレーション | **キー = 各スライドの `data-title` 完全一致** |
| `MIKI_TERM` | `const MIKI_TERM = {` | 用語タップ時の miki 台詞 | キー = icon-card の `data-key` |
| `iconData` | `const iconData = {` | 用語定義(info パネル) | キー = `data-key` |
| `POINT_ILLUST` | `const POINT_ILLUST = {` | スポットライト時の動く解説 | キー = `data-key` |
| `reviewPool` | `const reviewPool = [` | 復習チャレンジ(16 問プール) | `a` は正答 index |
| `MD_STEPS` | `const MD_STEPS = [` | miki コード/計算ステッパー | スライド内 `.mdc-line`/`.mdp-line` の `data-i` と整合 |
| `resetAllInteractions` の単元固有部 | `function resetAllInteractions` | 単元固有要素の初期化 | 追加した interactive を必ず登録 |

> **コード実演スライド**(MD ステッパー)の `data-title` は **MIKI_GUIDE に登録しない**。そうすると下部 miki バーが消え、スライド内 miki(`.md-miki`)が主役になる(lec11 の「miki.com と 10進→2進」がこれ)。

### 2.4 単元固有インタラクションの CSS/JS
- lec11 では `/* ===== lec11 固有: … ===== */` でマーキング(8ビット変換機 / 2ⁿスライダー / 変換表 / ニブル分割図 / スポットライトは共通層)
- 新単元では同じ流儀で `/* ===== lecNN 固有: … ===== */` として追加。**Design Tokens(navy/gold/red)と hosoku の手描き世界観(sf-flow/pulse/float/grow, 紙方眼, いびつ枠)を踏襲**

### 2.5 公開導線
- `lectures/index.html` に `CHAPTER · NN` カードを追加し、`N UNITS AVAILABLE` を +1

---

## 3. 標準インタラクション層(=触らない。動作だけ把握)

新単元で「勝手に作り直さない」対象。lec11 から verbatim で来る。

- **miki.com NPC バー**(`#mikibar`):スライド送りで `MIKI_GUIDE` を読み上げ(タイプライター)/ 用語タップで `mikiTermTalk` / ○×・判定で `mikiQuizReact` / ドラッグ移動・四隅リサイズ(PC)/ 顔タップで最小化 / **H で表示切替**。口調は**講義トーン(です・ます)死守**。
- **会話操作**:**Space で「つづき」**(会話が尽きたら次スライド)/ **もどすボタン**(1 行戻る)/ **吹き出しタップで進む**(スマホ)。
- **hosoku 補足**(`/hosoku` のエンジン drop-in):チップ `.supp-chip[data-supp]` クリックで手描きポップなモーダル。表示中 **P で本文マーカーが順に走る**。図は `suppFig` + `.sf-box`(動く SVG)。
- **POINT スポットライト + リッチ解説**(miki 表示時のみ):用語タップ → その用語を金リングで強調 + 周囲暗転 + `POINT_ILLUST` の動く図ポップ。**miki バーは暗転の上に残る(ナビ役)**。拡大ポップのタップ/×/Esc = **縮小のみ(選択は保持)**、資料の他所タップ = **選択解除**。
- **P 文字ポップ**(`kbSweep`):**くすんだ 8 色パレットから毎回ランダム**配色。対象は**フォーカス連動**で 3 段階 — ①拡大ポップ表示中 → ポップ内の強調語(名前+太字)/ ②縮小済みだが選択中 → その用語名 / ③未選択 → タイトル + 見出しの重要語。
- **共通基盤**:MENU ドロワー / 一括リセット / ユニバーサル(PC+スマホ)/ スワイプ / 触覚 / a11y。

> エンジンの内部実装・落とし穴は `SKILL.md §14`。`const`(GUIDE 等)は呼出より前に置く(TDZ で全停止する)。

---

## 4. 一発制作パイプライン(この順で回す)

```
[1] 素材確認     学習ノート docx + 解答PDF 該当ページを読み、POINT・実習・正答を抽出
[2] 構成案合意   カバー範囲・スライド数・目玉インタラクションをユーザーに提示 → 合意(コード前に)
[3] scaffold     cp examples/11-analog-and-digital.html articles/NN-slug/index.html
[4] コンテンツ差替  §2 のインベントリだけを差し替え(エンジンは触らない)
                  └ 書きながら解答PDFを傍に置き、正答・根拠フレームを1問ずつ照合(CLAUDE.md §4.8)
[5] /hosoku      難所スライドにリッチ補足を一括実装(下記 §5)
[6] /brushup     7軸(デザイン/インタラ/日本語/動くアイコン/正確さ/図表/例え)で底上げ
[7] /visual      ビジュアル密度を上げる(手順可視化の図など。lec11 のニブル分割図が手本)
[8] /audit-review  codex 教科書準拠audit(web検索禁止)。修正必須を適用
[9] /audit-review  ★ 修正後に再audit(feedback_audit_rerun_after_fixes)。clean になるまで
[10] 凍結+導線   examples/ にコピー、index.html にカード追加、構造/JSチェック
[11] 保全        submodule → 親リポの順で commit & push(push前に整合性レポート承認)
```

- [6]〜[7] は順不同・反復可。`feedback_cascade_brushup_lecture_decks`(自発カスケード ≥4-5周)の精神で、**言われる前に**詰める。
- 各編集後の機械チェック(§6)を必ず通す。

---

## 5. /hosoku の入れどころ(適宜・必須)

`/hosoku`(`reference_hosoku_command`)は難所に「目から鱗」の補足を一括で入れるためのもの。**lec11 では 7 件**(劣化/電圧と0と1/16進4桁/1ビット2通り/3進数/1024/補数)。

入れるべき箇所の目安(1単元 **5〜8 件**):
- 「なぜそうなるか」が問われる概念(原理・直観)
- つまずきやすい計算・記法(検算できる具体数値で示す)
- 共通テスト・実生活への接続(射程を広げる発展)
- 用語の混同しやすい区別

補足の中身は **動く図(sf-flow/pulse/float/grow)+ 鋭い具体数値 + 1 行の「鋭く言えば」**。チップ文言は問い形(「なぜ〜?」「〜って何?」)。

---

## 6. 品質ゲート(機械チェック・全部通す)

```bash
cd articles/NN-slug
# タグ/SVG/script バランス
python3 -c "s=open('index.html').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'),'script',s.count('<script>'),s.count('</script>'))"
# JS 構文
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
# data-title と MIKI_GUIDE キーの整合(コード実演スライドを除き未登録ゼロ)
# SVG 内 9px 未満の文字がないか
grep -oE 'font-size="[0-9.]+"' index.html | grep -oE '[0-9.]+' | awk '$1<9{print "WARN <9px"}'
# AI臭・スローガン・子供っぽさ(空であること)
grep -noE '(武器|叩き台|軸となる|やってみよう|頑張ろう|みんなで|立ち上が|湧き上が|紐解く|深掘り|詰め込|凝縮|完璧|素晴らし)' index.html
```
- 視覚確認は **headless Chrome の screenshot** で。スライド遷移は `goToSlide(n)` を inject して撮る(`reference_miki_npc_hosoku_lec10`)。
- 実機(`python3 -m http.server`)確認はユーザーに依頼。

---

## 7. 文章トーン(AI 臭を完全に断つ)— 最重要

教材本文・スライド見出し・カード説明・miki 台詞・hosoku 補足、**書く全ての文字**に適用する。

**禁止(`SKILL.md §8` + `feedback_no_ai_tone_in_lectures` + `feedback_natural_spoken_japanese_for_lectures`):**
- スローガン調・誇大:「武器」「叩き台」「軸」「選ばれし」「深掘り」「詰め込む」「凝縮」「余すところなく」
- AI 頻出メタファー:「立ち上がる」「湧き上がる」「浮かび上がる」「紐解く」「立体化」「学びのハブ」
- 子供っぽさ:「やってみよう」「頑張ろう」「みんなで」/ 装飾絵文字
- 標語見出し:「〜を。」「〜に。」で止める体言止めのキャッチコピー
- 対象属性の明示:「受験生向け」「東大志望者へ」
- 過剰カタカナ(英語直訳):漢語+やまと言葉で書けないか自問

**正(目標):**
- 事実と構造で、淡々と。大学講義・教材として自然な体。
- miki.com は **講義トーン(です・ます)**。NPC でも「だよ」等のくだけた語は使わない。
- 見出しは「なぜ 16 進法も使うのか」「何ビットあれば足りるか」のような**問い・宣言**で、標語にしない。

> 迷ったら `/audit-review`(教科書準拠・web検索禁止)で外部レビューを取り、断定の弱化・概念の締め直しを行う(`CLAUDE.md §4.14`)。

---

## 8. 参照

- canonical 実装:`examples/11-analog-and-digital.html`
- 技術仕様:`SKILL.md`(特に §14 標準インタラクション層)
- 部品カタログ:`components.md`
- 制作哲学・チェックリスト:`../../CLAUDE.md`(= `lectures/CLAUDE.md`)
- 横展開元の経緯:memory `reference_miki_npc_hosoku_lec10` / `reference_hosoku_command`
