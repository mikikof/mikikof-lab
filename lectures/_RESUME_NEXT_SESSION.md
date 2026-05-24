---
updated: 2026-05-24
prev_session: lec11「アナログとデジタル」(POINT 11) を新規制作し、/audit-review → /brushup → /visual → /audit-review を完走。publish 可・未 push。
---

# 次セッション resume — mikikof-lab / lectures

## 30 秒 status
- **lec11「アナログとデジタル」(POINT 11) 完成・audit clean(publish 可)。ただし未 commit / 未 push。**
- lec10「Web ページ」(POINT 10) も完成済(submodule `49c5e9b` / 親 `de188e5`)。
- **最優先の残作業 = lec11 の保全(commit & push)**。submodule(mikikof-lab)→ 親リポ の順。push 前に整合性レポートで承認(`feedback_git_push_confirmation`)。

## lec11 で確定したこと
- `articles/11-analog-and-digital/index.html`(25 スライド)。学習ノート POINT 11・解答PDF p.24 と全問照合済(codex 二重確認)。`examples/11-analog-and-digital.html` に凍結。`index.html` に CHAPTER 11 カード(11 UNITS)。
- lec10 の design system + hosoku(7 補足: DEGRADE/VOLTAGE/HEX4/BIT2/TERNARY/STAIR/COMPLEMENT)+ miki.com NPC + P 文字ポップ を踏襲。
- **固有インタラクション 4**: 8ビット変換機(`bcBuild/bcRender/bcSet`)/ 10進→2進ステッパー(miki.com, `MD_STEPS`)/ 2ⁿスライダー(`powUpdate/powSet`)/ 数値変換表(14マス, `cv-blank`+`toggleSelBlank`)。
- **深掘り副題 3**: 参考A なぜ2進数か / 参考B 情報量の階段(1024倍) / 参考C 補数で負の数。
- **visual 追加**: 実習3 にニブル分割図(`.nibble-fig`: 11011→0001 1011→1B)。
- audit log: `audit/reviews/2026-05-24/1852-lec11-analog-digital/`(rev1, 5件適用)+ `1902-...-rev2/`(clean)。

## 実行環境 / 確認コマンド
```bash
cd ~/my-company/.company/education/high-school/mikikof-lab/lectures
python3 -m http.server 8000
# → http://localhost:8000/articles/11-analog-and-digital/ を Chrome/Safari で確認
```
- 構造チェック: `python3 -c "s=open('articles/11-analog-and-digital/index.html').read();print(s.count('<div'),s.count('</div>'),s.count('<svg'),s.count('</svg>'))"`(現在 384/384, 58/58)
- JS: `python3 -c "s=open('articles/11-analog-and-digital/index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js`

## lec11 残工程チェックリスト(実機で見ると良い点)
- [ ] 保全: submodule で commit → push、親リポで参照更新 commit → push(承認後)
- [ ] 実機: 8ビット変換機(プリセット 27/65/255/クリア、ビットタップ)/ 2ⁿスライダー(n=1..16, dots)/ 変換表(14マス後出し)/ ニブル分割図
- [ ] 実機: miki.com 10進→2進ステッパー(次へ/戻る/最初から)、コード実演スライドはバー非表示・スライド内 miki 表示
- [ ] 実機: hosoku 7 チップ開閉・P マーカー走査、P で POINT 用語の文字ポップ、H で miki 表示切替

## 次にやる候補(lec11 の先)
- [ ] **lec11 を commit & push**(最優先)
- [ ] **lec12「情報のデジタル化」(POINT 12)** を新規。解答PDF は 2章「12 情報のデジタル化⑴⑵」(p.26/p.28)。lec11 を雛形に同じ design system + hosoku + miki.com で。標本化・量子化・符号化、音/画像/動画のデジタル化、文字コード、データ量計算が核心。
- [ ] miki.com / hosoku を lec01〜09 へ横展開(共通エンジン化検討)。

## 方針 / 申し送り
- 教材 audit は教科書(学習ノート)準拠・web 検索禁止(`feedback_audit_textbook_grounded`)。正答は `_source/高校情1学習ノート-解答PDF.pdf` を正本に。
- miki.com の口調は NPC でも講義トーン(です・ます)。P は文字自体のポップ(`charPop`)。
- JS の `const`(GUIDE 等)は呼び出し箇所より前。視覚バグは headless Chrome の screenshot で特定。
- lec11 で確立: 数学寄り単元では「変換機・スライダー・変換表」など手を動かす HTML インタラクションが効く。ニブル分割図のような手順可視化が変換練習に有効。

## ポインタ
- lec11: `articles/11-analog-and-digital/index.html` / 凍結 `examples/11-analog-and-digital.html`
- audit ログ: `~/my-company/.company/audit/reviews/2026-05-24/1852-lec11-analog-digital/` + `1902-...-rev2/`
- 意思決定: `~/my-company/.company/secretary/notes/2026-05-24-decisions.md`(lec11 節)
