---
updated: 2026-05-28
prev_session: lec11/12 engine 改修(miki.com→miki.con + mikibar セリフ専用 文字サイズバー + サイト本体 transform: scale バー の 2 系統) + 本文 audit rev3-6 で計 14 件適用(両 lec 完全収束)。submodule + 親リポともに全 push 済(adcb835 / be6cd36)。
---

# lectures 次セッション resume

## 30 秒 status
- **lec01〜lec12 まで公開済 + 全 push 済**(submodule HEAD = `adcb835`、親リポ pointer 同期済)。
- 本日(2026-05-28)は lec11/lec12 の **engine 層を大幅強化** + **本文 audit を完全収束**まで進めた(下記)。
- 新規制作の **次は lec13「データの圧縮」(POINT 13)** が自然な続き(プレイブック手順は不変、ただし継承元 canonical は新 engine 含む形に進化済)。

## 本日の確定変更(canonical = lec11 が継承元、lec13+ は自動で取り込む)

### engine 改修 (commit `adcb835`)
- **NPC 名: `miki.com` → `miki.con`** に統一(全 lec11/12 本文・examples・skill docs `SKILL.md`/`NEW-LECTURE-PLAYBOOK.md`/`components.md`)。lec10 は当時の名前で据置(再 audit 回避)。
- **文字サイズ調整 2 系統(各 5 段階 90/100/110/125/150%)**:
  | 系統 | スコープ | 配置 | コントローラ |
  |---|---|---|---|
  | `--fs` | miki.con セリフ専用(`#mikibar .mb-say` + `.md-say` の font-size のみ乗算) | mikibar の titlebar 右側 | `.mb-fs` / `fsStep` |
  | `--fs-site` | サイト本体全体(`.slide-container` に `transform: scale()`, 中央 origin) — テキスト・SVG・アイコン・余白すべて proportional | topbar の chapter と MENU の間 | `.tb-fs` / `siteFsStep` |
- mikibar / topbar / bottombar は body 直下 sibling のため scale の影響を受けない。
- 実装要点(コピペで継承可):
  - `:root { --fs: 1; --fs-site: 1; }`
  - `.slide-container { transform: scale(var(--fs-site, 1)); transform-origin: center center; transition: transform 0.18s ease; }`
  - `.mb-fs` には `onpointerdown="event.stopPropagation()"` を付けてバーのドラッグ伝播を遮断(忘れると titlebar ドラッグと競合)。

### 本文 audit 完全収束(commit `adcb835` + 親リポ `be6cd36` に log)
- lec11: rev3(5 件) → rev4(1 件・**Accept/stop**) — 2 ラウンドで収束、累計 **6 件**。
- lec12: rev3(4 件) → rev4(2 件・rev3 regression)→ rev5(2 件・rev4 regression)→ rev6(**Accept**) — 4 ラウンドで収束、累計 **8 件**。
- 主要訂正:
  - lec11 参考C「2 の補数」の論理破綻訂正(残りビット=大きさ は符号付き絶対値の説明だった)。「先頭ビットの重み = −2^(n−1)」明示 + 例 `1101 = −8+4+0+1 = −3`。
  - lec12「文字も含めて標本化→量子化→符号化」過剰一般化を 8 か所横断で訂正(「文字は文字コード」「音・画像は三段階」に分離)。
- **CMYK 据置**(学習ノート POINT 12 の枠を守るためユーザー判断)。本文の CMY 説明と矛盾なし confirmed by codex。
- ログ: `.company/audit/reviews/2026-05-28/` 配下 6 フォルダ(1853 lec11/12 rev3 / 1913 lec11/12 rev4 / 1928 lec12 rev5 / 1933 lec12 rev6)。

## 確定事項(lec13+ で守るべき前提)
- **canonical = `articles/11-analog-and-digital/index.html`(= examples/11-analog-and-digital.html)**。新規単元はこれを cp して**コンテンツ層だけ差替**(2 系統文字サイズコントローラ + miki.con + hosoku + POINT スポットライト + P 文字ポップ + Space/もどす を verbatim 継承)。
- 補足モーダルの `sh-title`/`sh-sub` は **innerHTML**(`<b>` 太字対応)。`textContent` だと literal 表示バグ。lec10/11/12 は修正済。
- **発展(参考/APPENDIX)スライドは `.appx`(ヒーロー図+視覚的動線+構造化ポイント)で作る**。deep-card 羅列は禁止。論理順序(なぜ→手順)・1 トピック 1 スライド・概念は双対提示・動きは意味あるときだけ。canonical = lec11 参考 A〜F。
- POINT 番号 = 学習ノート POINT 番号(lec11=POINT11, lec12=POINT12)。lec13=POINT13。
- **教材本文では「標本化→量子化→符号化」を文字まで含めて書かない**(lec12 audit 4 ラウンドで確立した規範)。文字は文字コード、音・画像はアナログ量で三段階、と分離する。
- **2 の補数の説明では「残りビット = 大きさ」と書かない**(符号付き絶対値の説明と混同する)。「先頭ビットの重み = −2^(n−1)」と書く(lec11 参考C 規範)。

## 残工程チェックリスト(次の一手)
- [ ] **lec13「データの圧縮」(POINT 13・学習ノート p.30)** を新規制作。`_source/高校情1学習ノート-解答PDF.pdf`(「13 データの圧縮」)と 2 章 docx で正答照合。
  - 内容: 圧縮/圧縮率/伸張、可逆圧縮/非可逆圧縮、ランレングス(連長)圧縮、ハフマン符号(符号長 × 出現回数の計算あり: 1×4 + 2×3 + … = 53 等)。
  - 目玉インタラクション案: ランレングス圧縮の実演(BBBWBW…→B3W1B1W1…)、ハフマン木の構築ステッパー、圧縮率電卓。
  - 発展は `.appx` で。/hosoku は難所 5〜10 件(可逆と非可逆の違い / なぜ写真は非可逆 / ハフマンが最短になる理由 等)。
- [ ] 手順: `cp articles/11-analog-and-digital/index.html articles/13-data-compression/index.html` → §2 インベントリ差替 → /hosoku → /brushup → /visual → audit ×2 → examples 凍結 → `lectures/index.html` に CHAPTER·13(13 UNITS)。
- [ ] (任意・余力あれば)新 engine の実機検証: 5 段階の `[a]/[A]` ボタン挙動、`--fs` セリフのみ拡縮、`--fs-site` でサイト全体拡縮、両者独立動作。Safari / Chrome 実機で確認。

## 実行環境 / コマンド
```bash
cd /Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/lectures
# 着手前に必ず読む(順序厳守)
#  1) skills/interactive-lecture/NEW-LECTURE-PLAYBOOK.md(最上位・§5.5 発展=情報デザイン)
#  2) CLAUDE.md  3) SKILL.md §15  4) components.md(.appx ほか)
#  5) examples/11-analog-and-digital.html(canonical = 新 engine 含む) 6) _source/ 解答PDF 該当ページ
# scaffold
cp articles/11-analog-and-digital/index.html articles/13-data-compression/index.html
# 機械ゲート(差替後)
cd articles/13-data-compression
python3 -c "s=open('index.html').read();print('div',s.count('<div'),s.count('</div>'),'svg',s.count('<svg'),s.count('</svg>'))"
python3 -c "s=open('index.html').read();sc=s[s.find('<script>')+8:s.rfind('</script>')];open('/tmp/c.js','w').write(sc)" && node --check /tmp/c.js
# headless 実機(両 fs バーが topbar 右と mikibar 上部にあるか):
# Chrome 起動 → mikibar 表示 → topbar 右の TEXT a/100/A と mikibar 上の a/100/A を確認
```

## 作業 / 執筆方針(ユーザー明示)
- **AI 臭を完全に避ける**: スローガン調・抽象メタファー・**同一フレーズの反復(「鋭く言えば」を全補足に貼らない)**・砕けた口語(「余裕で」「化ける」)を排除。言い回しは都度変える。
- **/hosoku を適宜入れる**(難所に目から鱗の補足)。図は意味があるときだけ動かす。
- 解答・根拠は `_source/解答PDF` を正本に 1 問ずつ照合(CLAUDE.md §4.8)。
- 発展スライドは必ず情報デザイン(`.appx`)で。
- **audit は教科書準拠 / web 検索禁止**(`feedback_audit_textbook_grounded`)。**修正後は必ず再 audit を回す**(`feedback_audit_rerun_after_fixes` — 本日 lec12 で 3 ラウンド連続 regression を捕捉した実例)。
- このクオリティを「一発」で出せるよう指示系統は更新済 → **PLAYBOOK に従えば再現可能**。

## ポインタ
- 直近 submodule commit(全 push 済): `adcb835`(engine + audit 14 件) / `8fa7816`(skill docs miki.con) / `f825549`(前回 resume) / `2fe23c6`(指示系統)。
- 親リポ my-company の submodule ポインタ = `adcb835`(push 済 `be6cd36`)。
- 本日の audit ログ(親リポ): `.company/audit/reviews/2026-05-28/{1853 rev3 × 2, 1913 rev4 × 2, 1928 rev5, 1933 rev6}/`。
- memory: `reference_miki_npc_hosoku_lec10`(2 系統文字サイズ + miki.con 詳細を反映済) / `reference_new_lecture_playbook` / `feedback_lecture_appendix_infodesign` / `feedback_audit_rerun_after_fixes` / `feedback_audit_textbook_grounded` / `feedback_no_ai_tone_in_lectures`。
- ⚠ 同 repo で**並行セッション(paper-003/superelite/dst-deck)稼働中**: `git add`/index 共有で `--amend` が他者ステージを巻き込む。pointer commit は `git restore --staged .` でクリア後に該当ファイルだけ add → 新規 commit。
