---
updated: 2026-06-20
prev_session: lec13「データの圧縮」(POINT 13) 新規制作 → codex audit r1(6件)/r2(5件)/r3(1件)収束 → brushup(ハフマン木図+モールスhosoku) → visual(実習2形式対応図+実習4対比バー)。submodule HEAD=b1cda52、親リポ=a19da77、いずれも push 済。lec01〜lec13 まで全公開。
---

# lectures 次セッション resume

## 30 秒 status
- **lec01〜lec13 まで公開済 + 全 push 済**(submodule HEAD = `b1cda52`、親 pointer = `a19da77` 同期済)。
- lec13「データの圧縮」は内容・engine・図表ともに publish 水準(codex audit 3世代収束)。
- 新規制作の **次は lec14「ハードウェアとソフトウェア」(POINT 14・学習ノート 3章 p.34)** が自然な続き。

## 確定事項(lec14+ で守る前提)
- **canonical = `articles/11-analog-and-digital/index.html`(= examples/11-analog-and-digital.html)**。新規単元はこれを cp し**コンテンツ層だけ差替**(2系統文字サイズ + miki.con + hosoku + POINTスポットライト + P文字ポップ + Space/もどす を verbatim 継承)。lec13 もこの方式で制作。
- **POINT 番号 = lec 番号**(lec13=POINT13, lec14=POINT14)。
- 補足モーダルの `sh-title`/`sh-sub` は **innerHTML**(`<b>` 太字対応)。
- 発展(参考/APPENDIX)は **`.appx`**(ヒーロー図+視覚的動線+構造化ポイント)。deep-card 羅列禁止。
- 答え・根拠は `_source/高校情1学習ノート-解答PDF.pdf` を正本に1問ずつ照合(CLAUDE.md §4.8)。3章は解答PDF の対応ページ(p.34〜45 = 3章)を Read で確認。

## lec13 制作で得た知見(再現の要点・lec14 で踏襲)
- **Python splice の終端アンカー**: データ構造ブロック間に**エンジンが挟まる**。例 `window.HOSOKU_SUPP = {` の後は MIKI_GUIDE ではなく **nav engine(haptic/slides/goToSlide/updateUI/swipe)** が来る。終端アンカーは次のブロックでなく `function haptic(ms)` のような**直後の実体**に取る。さもないとエンジンを巻き込み削除し `goToSlide is not defined` で全停止する(lec13 で2度踏んだ)。行頭アンカー(`\n` 前置)で comment 行の誤マッチも回避。
- **codex audit**: `review` プロファイルの既定 model は `gpt-5.3-codex`(ChatGPT アカウント非対応)。**`codex exec -p review -m gpt-5.5 --sandbox read-only "..." < /dev/null`** で起動。教材は web 禁止・教科書準拠、正本の正答を prompt に ground truth として貼る。修正後は再 audit(feedback_audit_rerun_after_fixes)。
- **ランレングス**: 「2個以上で 色+個数」方式は **2個=同長(BB→B2)、3個以上で短縮、1個はそのまま**。「2個以上で短くなる」は誤り(audit で捕捉)。単独を B1 と書く naive 版だけが「増える」。
- **概念定義の断定回避**(§4.14): 「圧縮=中身を保ったまま」は非可逆と矛盾 → 一般定義は「データ量を減らす」に留め、可逆/非可逆の分岐を補う。モールス信号は「間」で区切る方式で接頭符号(ハフマン)とは区切り機構が違う → 「同じ」でなく「よく似ている」。
- **実機確認**: headless Chrome に `setTimeout(()=>{goToSlide(N); …},600)` を inject(閉じタグは `</`+`script>` で、`<\/script>` のバックスラッシュ混入に注意)。`--virtual-time-budget=3000`。

## 標準ワークフロー(lec14 = 1本)
```bash
cd /Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/lectures
# 着手前に必ず読む(順序厳守)
#  1) skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md(最上位)
#  2) CLAUDE.md  3) SKILL.md §14/§15  4) components.md(.appx)
#  5) examples/11-analog-and-digital.html(canonical) または lec13 を参考に
#  6) _source/高校情1学習ノート-解答PDF.pdf の 3章 p.34〜 該当ページ
# scaffold
cp articles/11-analog-and-digital/index.html articles/14-hardware-and-software/index.html
# 機械ゲート(差替後・コピペで動く)
cd articles/14-hardware-and-software
python3 -c "s=open('index.html').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'),'script',s.count('<script>'),s.count('</script>'))"
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
# data-title ↔ MIKI_GUIDE 整合 / chip ↔ HOSOKU_SUPP 1:1 / <9px / AI臭 は lec13 のゲート参照
```

## 残工程チェックリスト(次の一手)
- [ ] **lec14「ハードウェアとソフトウェア」(POINT 14・3章 p.34)** を新規制作。`_source` 解答PDF 3章ページで正答照合。
  - 章は 14 ハードウェアとソフトウェア / 16 論理回路と論理演算 / 17 コンピュータの構成と動作 / 18 コンピュータの性能(15 は docx で要確認)。
  - 目玉インタラクション案: 論理回路の真理値表(タップ)、コンピュータ5大装置の構成図、性能(クロック/コア)電卓 など — ただし POINT 14 単元の射程に合わせて選ぶ。
- [ ] 手順: cp lec11 → §2 インベントリ差替 → /hosoku → /brushup → /visual → audit ×2(gpt-5.5) → examples 凍結 → index.html に CHAPTER·14(14 UNITS)。

## ポインタ
- 直近 submodule commit(push 済): `b1cda52`(lec13)。親 pointer: `a19da77`(submodule 参照 + 監査ログ r1-r3 + decisions)。
- lec13 監査ログ: `.company/audit/reviews/2026-06-11/{0228 r1, 0243 r2}` + `2026-06-20/1103 r3`。
- lec13 decisions: `.company/secretary/notes/{2026-06-10, 2026-06-20}-decisions.md`。
- 本日作業ログ: `.claude/session-logs/2026-06-20.md`。
- memory: `reference_new_lecture_playbook` / `reference_miki_npc_hosoku_lec10` / `feedback_lecture_appendix_infodesign` / `feedback_audit_rerun_after_fixes` / `feedback_audit_textbook_grounded` / `feedback_no_ai_tone_in_lectures` / `feedback_lectures_pointnum_equals_lecnum`。
- ⚠ 同 submodule に **別セッションの未コミット作業**(daisu-column/constraints-and-gradients、lectures/_source/本文PDF 2/)が残存。lec14 の commit 時も**名前指定 stage** で混ぜないこと。
