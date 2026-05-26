---
updated: 2026-05-26
prev_session: lec11 完成・push済 + miki.com ナビ機能群実装 + lecture 一発制作の指示系統(NEW-LECTURE-PLAYBOOK)整備完了
---

# 次セッション resume — mikikof-lab / lectures

## 30 秒 status
- **lec11「アナログとデジタル」(POINT 11) 完成・push 済**(submodule `b6eec18` / 親 `991409c`)。miki.com ナビ機能群も全部入り。
- **新規単元の作り方が「lec11 を cp して中身だけ差し替える」に確立**。最上位ドキュメント = `skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md`。
- **次の一手 = lec12「情報のデジタル化」(POINT 12)** を、そのプレイブックに従って制作する。

## 確定事項
- **canonical = `examples/11-analog-and-digital.html`**(= `articles/11-analog-and-digital/index.html`)。新規単元はこれをコピーして出発。
- **2 層分離**:標準インタラクション層(エンジン=1文字も変えず継承)/ コンテンツ層(差替)。
- lec11 の標準インタラクション層 = miki.com NPC バー / hosoku 補足 / POINT スポットライト+リッチ動く解説ポップ(miki 表示時のみ)/ P 文字ポップ(くすみ8色ランダム・フォーカス連動3段階)/ Space でつづき+もどすボタン+吹き出しタップ(スマホ)。
- 差替データ構造: `HOSOKU_SUPP`(チップと1:1)/ `MIKI_GUIDE`(キー=スライド data-title 完全一致)/ `MIKI_TERM` / `iconData` / `POINT_ILLUST`(キー=data-key)/ `reviewPool` / `MD_STEPS` / スライド本体 / 単元固有 CSS·JS / `resetAllInteractions` 固有部 / topbar。
- 指示系統: `lectures/CLAUDE.md` §3・§6、`SKILL.md` §7・§11・§15、`components.md` 末尾、永続メモリ `reference_new_lecture_playbook` をすべて lec11 canonical へ更新済。

## 次にやる候補(優先順)
- [ ] **lec12「情報のデジタル化」(POINT 12)** を新規制作。解答PDF は 2章「12 情報のデジタル化⑴⑵」(**p.26 / p.28**)。核心=標本化・量子化・符号化、音/画像/動画のデジタル化、文字コード、データ量計算。
  - 目玉インタラクション候補: 標本化→量子化→符号化のステップ実演 / 標本化周波数・量子化ビット数スライダー(波形→階段→ビット列が連動)/ データ量計算機 / 画素・階調の可視化。
- [ ] miki.com / hosoku / スポットライト を lec01〜09 へ横展開(共通エンジン化の検討)。

## lec12 制作手順(プレイブック準拠・そのまま実行)
```bash
cd ~/my-company/.company/education/high-school/mikikof-lab/lectures
# 1) 素材抽出(POINT 12 の項番・実習)
python3 - <<'PY'
import zipfile; from xml.etree import ElementTree as ET
ns='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
f='_source/学習ノート_問題/高校情1学習ノート（p.18～33）-2章コミュニケーションと情報デザイン-問題Word.docx'
root=ET.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
for i,p in enumerate(root.iter(ns+'p')):
    t=''.join(n.text or '' for n in p.iter(ns+'t'))
    if t.strip(): print(i,t)
PY
# 2) 解答PDF p.26/p.28 を Read で開いて正答を正本確認(web検索禁止)
pdftotext -layout _source/高校情1学習ノート-解答PDF.pdf /tmp/ans.txt   # 該当ページ抜粋
# 3) scaffold
cp skills/interactive-lecture/examples/11-analog-and-digital.html articles/12-digitization/index.html
# 4) コンテンツ差替(プレイブック §2 インベントリ)→ /hosoku → /brushup → /visual → /audit-review ×2
```
- 構造/JS チェック(編集後・プレイブック §6):
```bash
cd articles/12-digitization
python3 -c "s=open('index.html').read();print(s.count('<div'),s.count('</div>'),s.count('<svg'),s.count('</svg>'))"
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
```

## 方針 / 申し送り
- **必読の順**: NEW-LECTURE-PLAYBOOK.md → CLAUDE.md → SKILL.md §15 → canonical(lec11) → 解答PDF 正本。
- 教材 audit は教科書準拠・web検索禁止(`feedback_audit_textbook_grounded`)。修正後は再 audit(`feedback_audit_rerun_after_fixes`)。
- **AI 臭を完全排除**:miki は講義トーン(です・ます)、見出しは問い/宣言で標語にしない、禁止リスト機械チェック(プレイブック §6・§7)。
- miki ナビ系の検証は headless Chrome + `--dump-dom` で `document.title` にフラグ出力(timing 非依存)。
- `const`(MIKI_GUIDE / POP_PALETTE / POINT_ILLUST 等)は呼出より前(TDZ で全停止)。

## ポインタ
- canonical: `articles/11-analog-and-digital/index.html` / 凍結 `examples/11-analog-and-digital.html`
- 指示系統: `skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md`(最上位)/ `SKILL.md §15`
- 直近 commit: submodule `b6eec18`(指示系統整備)/ 親 `991409c`
- audit ログ: `~/my-company/.company/audit/reviews/2026-05-24/1852-lec11-analog-digital/` + `1902-…-rev2/`
- 永続メモリ: `reference_new_lecture_playbook` / `reference_miki_npc_hosoku_lec10`
