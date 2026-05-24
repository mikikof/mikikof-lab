---
updated: 2026-05-24
prev_session: lec10「Web ページ」を新規制作し、miki.com を NPC 化(対話/ドラッグ/リサイズ/文字ポップ)まで仕上げて push 済み
---

# 次セッション resume — mikikof-lab / lectures

## 30 秒 status
- **lec10「Web ページ」(POINT 10) は完成・push 済み**(submodule commit `49c5e9b`、親 `de188e5`)。
- 残るのは **ブラウザ実機確認のみ**(下記チェックリスト)。内容・コードはレビュー/検算済み。
- このセッションで **再利用可能な部品**(hosoku 補足 / miki.com NPC バー / P 文字ポップ)が lec10 に揃った。他の単元へ横展開できる。

## 確定事項
- lec10 = `articles/10-web-pages/index.html`(24 スライド)。学習ノート POINT 10・解答PDF p.22 と全問照合済み。`examples/10-web-pages.html` に凍結。`index.html` に CHAPTER 10 カード(10 UNITS)。
- **hosoku 7 補足**: エンジンは `~/.claude/skills/hosoku/`(supp.css/supp.js を verbatim 注入)+ `window.HOSOKU_SUPP` にコンテンツ。チップ `.supp-chip[data-supp]` と 1:1。
- **miki.com NPC**(lec10 内に実装、横展開時はここから抽出):
  - 常駐バー `#mikibar` + `MIKI_GUIDE`(data-title→{tag, say})。`say` は文字列/配列(配列=「▶ つづき」送り)。
  - 用語カードタップ→`mikiTermTalk`(同じ用語の連続クリックで会話前進)、○×→`mikiQuizReact`。
  - タイプライター表示、ドラッグ移動(タイトルバー/顔)、PC 四隅リサイズ、スマホ compact 最適化、顔タップで最小化(=miki アイコンのみ)。
  - 口調は**講義トーン(です・ます)**。口は ε、常時微横揺れ。
- **キー操作**(lec10): `H`=miki 表示/非表示、`P`=POINT 用語(`.icon-card-name`)を **文字ポップ波**(`@keyframes charPop` + `.char` 分割 + 80ms 順次)。用語名は Zen Maru Gothic 700 + ゴールド下線で常時強調。

## 実行環境 / 確認コマンド
```bash
cd ~/my-company/.company/education/high-school/mikikof-lab/lectures
python3 -m http.server 8000
# → http://localhost:8000/articles/10-web-pages/ を Chrome/Safari で開く
```
- 構造チェック(編集後):
```bash
cd articles/10-web-pages
python3 -c "import re;s=open('index.html').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'))"
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
```
- ヘッドレス確認(任意): `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --screenshot=/tmp/s.png --window-size=1300,880 --virtual-time-budget=3500 "file://$PWD/index.html"`

## 残工程チェックリスト(lec10)
- [ ] 実機: 7 つの hosoku チップ → 開閉・図が動く・P でマーカー走査・Esc/×/背景で閉じる
- [ ] 実機: miki.com — スライド送りで解説が切替 / 用語タップで会話 + 連続クリックで前進 / 「▶ つづき」/ ドラッグ移動 / 四隅リサイズ(PC) / 顔タップで最小化(アイコンのみ) / H で表示切替
- [ ] 実機: `P` で POINT 用語が左→右に文字ポップ(ハイライトでなく文字自体が跳ねる)
- [ ] 実機(スマホ): miki ウィンドウが本文に干渉しないか、コード実演ステッパーが縦積みで読めるか
- [ ] 気になれば: miki の揺れ幅/速度、ポップの大きさ/速度(80ms/0.72s)、ε 位置の微調整

## 次にやる候補(lec10 の先)
- [ ] **lec11「アナログとデジタル」(POINT 11)** を新規(解答PDF p.24)。lec10 を雛形に同じ design system + hosoku + miki.com で。
- [ ] **miki.com / hosoku を lec01〜09 へ横展開**(共通エンジン化を検討: supp.* は drop-in 済、miki は lec10 から抽出して shared 化すると良い)。

## 方針 / 申し送り
- 教材 audit は**教科書(学習ノート)準拠・web 検索禁止**(`feedback_audit_textbook_grounded`)。正答は `_source/高校情1学習ノート-解答PDF.pdf` を正本に。
- miki.com の口調は **NPC でも「だよ」等のくだけた語を使わず講義トーン**(ユーザー指摘で確定)。
- P の波打ちは**ハイライト出現でなく文字自体のポップ**(superelite/オリエン正本 `charPop` に統一)。
- JS で `const`(GUIDE 等)は**呼び出し箇所より前**に置く(後置で TDZ → スクリプト全停止を踏んだ)。
- 視覚バグ/JS 停止は**ヘッドレス Chrome の screenshot/dump-dom** で特定するのが有効。

## ポインタ
- submodule commit: `49c5e9b`(lec10 + miki NPC)/ 親: `de188e5`(ポインタ + audit)
- audit ログ: `~/my-company/.company/audit/reviews/2026-05-23/1616-lec10-web-pages/`
- 意思決定の逐次記録: `~/my-company/.company/secretary/notes/2026-05-23-decisions.md`(lec10 / hosoku / miki の各節)
