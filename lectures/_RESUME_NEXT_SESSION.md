---
updated: 2026-05-27
prev_session: lec12「情報のデジタル化」新規制作 + lec11 改修(補足/APPENDIX情報デザイン/発展3p) + 指示系統ブラッシュアップ。submodule 全 push 済(2fe23c6)。
---

# lectures 次セッション resume

## 30 秒 status
- **lec01〜lec12 まで公開済**。最新の lec12「情報のデジタル化」(POINT 12)は完成・push 済。
- lec11「アナログとデジタル」は今セッションで大幅強化(補足エンジン修正・INFO補足・APPENDIX 情報デザイン刷新・負数/小数 発展3p)。
- 指示系統(PLAYBOOK/components/SKILL/CLAUDE)を現行品質に同期済。**次は lec13「データの圧縮」(POINT 13)** が自然な続き。

## 確定事項
- **canonical = `articles/11-analog-and-digital/index.html`(= examples/11-analog-and-digital.html)**。新規単元はこれを cp して**コンテンツ層だけ差替**(エンジン verbatim 継承)。
- 補足モーダルの `sh-title`/`sh-sub` は **innerHTML**(`<b>` 太字対応)。`textContent` だと literal 表示バグ。lec10/11/12 は修正済。
- **発展(参考/APPENDIX)スライドは `.appx`(ヒーロー図+視覚的動線+構造化ポイント)で作る**。deep-card 羅列は禁止。論理順序(なぜ→手順)・1トピック1スライド・概念は双対提示・動きは意味あるときだけ。canonical = lec11 参考A〜F。
- POINT 番号 = 学習ノート POINT 番号(lec11=POINT11, lec12=POINT12)。lec13=POINT13。

## 残工程チェックリスト(次の一手)
- [ ] **lec13「データの圧縮」(POINT 13・学習ノート p.30)** を新規制作。`_source/高校情1学習ノート-解答PDF.pdf`(「13 データの圧縮」)と 2章docx で正答照合。
  - 内容: 圧縮/圧縮率/伸張、可逆圧縮/非可逆圧縮、ランレングス(連長)圧縮、ハフマン符号(符号長×出現回数の計算あり: 1×4+2×3+…=53 等)。
  - 目玉インタラクション案: ランレングス圧縮の実演(BBBWBW…→B3W1B1W1…)、ハフマン木の構築ステッパー、圧縮率電卓。
  - 発展は `.appx` で。/hosoku は難所5〜10件(可逆と非可逆の違い/なぜ写真は非可逆/ハフマンが最短になる理由 等)。
- [ ] 手順: `cp articles/11-analog-and-digital/index.html articles/13-data-compression/index.html` → §2 インベントリ差替 → /hosoku → /brushup → /visual → audit×2 → examples 凍結 → index.html に CHAPTER·13(13 UNITS)。

## 実行環境 / コマンド
```bash
cd /Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/lectures
# 着手前に必ず読む(順序厳守)
#  1) skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md(最上位・§5.5 発展=情報デザイン)
#  2) CLAUDE.md  3) SKILL.md §15  4) components.md(.appx ほか)
#  5) examples/11-analog-and-digital.html(canonical)  6) _source/ 解答PDF 該当ページ
# scaffold
cp articles/11-analog-and-digital/index.html articles/13-data-compression/index.html
# 機械ゲート(差替後)
cd articles/13-data-compression
python3 -c "s=open('index.html').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'))"
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
# headless 実機: goToSlide(n) / 補足は [data-supp=KEY].click() を inject して撮る
```

## 作業 / 執筆方針(ユーザー明示)
- **AI 臭を完全に避ける**: スローガン調・抽象メタファー・**同一フレーズの反復(「鋭く言えば」を全補足に貼らない)**・砕けた口語(「余裕で」「化ける」)を排除。言い回しは都度変える。
- **/hosoku を適宜入れる**(難所に目から鱗の補足)。図は意味があるときだけ動かす。
- 解答・根拠は `_source/解答PDF` を正本に1問ずつ照合(CLAUDE.md §4.8)。
- 発展スライドは必ず情報デザイン(`.appx`)で。
- このクオリティを「一発」で出せるよう指示系統は更新済 → **PLAYBOOK に従えば再現可能**。

## ポインタ
- 直近 submodule commit: `2fe23c6`(指示系統更新)/ `7059dec`(lec11 発展3p)/ `4e0436b`(APPENDIX刷新)/ `971ed7f`(INFO)/ lec12 群。全て origin/main 済。
- 親リポ my-company の submodule ポインタ = `2fe23c6`(push 済)。
- memory: `feedback_lecture_appendix_infodesign` / `reference_new_lecture_playbook` / `reference_hosoku_command` / `feedback_no_ai_tone_in_lectures`。
- ⚠ 同 repo で**並行セッション(paper-003/superelite)稼働中**: `git add`/index 共有で `--amend` が他者ステージを巻き込む。pointer commit は `git restore --staged .` でクリア後に該当ファイルだけ add → 新規 commit。
