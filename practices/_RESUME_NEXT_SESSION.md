---
updated: 2026-06-20
prev_session: "02-06「情報デザインの応用」を新規作成 → brushup/visual/audit-review まで完走・push 済み"
---

# practices(Interactive Practice Lab)— 次セッション復帰ガイド

## 30秒 status
ベストフィット問題集準拠の演習用Web教材を単元ごとに量産中。直近で **02-06「情報デザインの応用」** を新規作成し、brushup・visual・audit-review まで通して **commit & push 済み**(submodule mikikof-lab 756f1bb / 親 my-company 8934f3a)。次に作るなら **02-07「デジタル化された情報とその表し方」** が自然な続き。

## 完成済み単元(articles/)
- 01-01 情報とメディア / 01-02 問題解決 / 01-03 知的財産権 / 01-04 セキュリティと法規 / 01 思考のステップ1
- 02-05 情報デザインの基礎
- **02-06 情報デザインの応用(本セッション新規)** — HTML/CSS/Webサイト構造。例題2 + 練習6 + おさらい6モジュール + 図SVG3点(タグ構造/ボックスモデル/HTML+CSS=完成ページ)+ 原本図4枚。

## 確定事項 / この単元で増えた資産
- **新 input type `self`(記述式・模範解答 reveal + 自己採点○/△)** を engine に追加済み。`gradeStage` に `else if (self)` 分岐、`retryStage` の boxes 配列に `'self'`、CSS `.self-*` / `.code-listing`、wiring ブロック。記述問題はこの型を流用する。
- ベース・規約は不変: 新規単元は `skills/interactive-practice/examples/01-01-information-and-media.html` を cp してコンテンツ層のみ差替。青基調トークン・モバイルUI v2(spotlight/haptic/カウントアップ/カルーセル)8フックは絶対に消さない。
- 原本図がある単元は §4.10b 必須: `unzip docx → word/media/*` を Read で目視 → `assets/figN-{desc}.jpeg` にリネーム配置。

## 次にやること(02-07 を作る場合)チェックリスト
- [ ] 原本パース: `_source/ベストフィット問題/BF情1New-2章07デジタル化された情報とその表し方-問題（Python）.docx` + 解答は `_source/ベストフィット解答/BF情1New-2章-解答（Python）.docx` の「07」節(問題54〜60、本セッションの audit prompt 構築スクリプトで `07　デジタル化された情報` 以降を抽出した範囲)
- [ ] 構成案を AskUserQuestion で合意してから着手(CLAUDE.md §6 [2])。02-07 は 2進数/16進数・標本化/量子化・色階調・fps など**計算問題**が多い → fill / single / match で組む。記述があれば `self` 型。
- [ ] 01-01 を cp → `articles/02-07-{slug}/index.html`、title/slug/TIMELINE_ENTRIES/PROBLEMS/分母 を差替
- [ ] 全問 原本docx と1問ずつ照合 → index.html カード追加 → examples/ 凍結
- [ ] /brushup /visual で図補強 → /audit-review(kind=lecture, profile=review, web禁止・原本準拠)

## 実行環境 / コマンド(コピペ可)
```bash
cd /Users/mikiokofune/my-company/.company/education/high-school/mikikof-lab/practices
# 原本パース(02-07)
rm -rf /tmp/bf0207 && unzip -q "_source/ベストフィット問題/BF情1New-2章07デジタル化された情報とその表し方-問題（Python）.docx" -d /tmp/bf0207
ls /tmp/bf0207/word/media/   # 図の有無
# headless 目視(必ず article ディレクトリ内に一時HTMLを書く。/tmp だと assets が解決しない)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --window-size=900,2000 \
  --default-background-color=FFFFFFFF --screenshot=/tmp/out.png "file://$PWD/articles/02-07-xxx/index.html"
# 構文ゲート
node --check <(python3 -c "import re;print(re.search(r'<script>(.*)</script>',open('articles/02-07-xxx/index.html').read(),re.S).group(1))")
```

## 作業方針(厳守)
- 原本完全準拠(問題文一字一句・正答順)。正答・解説は `_source/ベストフィット解答/` を Read で照合してから書く。
- 子供っぽい誘導・過剰な褒め・AI臭メタファー禁止(CLAUDE.md §4.7 / §4.8)。
- audit は教科書準拠(web検索禁止・原本同梱・正答1問ずつ照合明示)。text抽出を渡すと図の入れ子が潰れ誤検知が出る → 実機で裏取りして却下([[feedback_verify_before_overruling_audit]])。

## ポインタ
- 直近 commit: submodule `756f1bb` / 親 `8934f3a`(両方 push 済み)
- audit ログ: `.company/audit/reviews/2026-06-20/1239-practices-02-06-info-design-app/`
- 制作哲学=`practices/CLAUDE.md` / 技術=`skills/interactive-practice/SKILL.md` / 部品=`components.md`
