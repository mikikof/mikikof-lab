---
description: 教材 HTML(lectures/column/practices)にビジュアル要素(SVG / イラスト / 関係図)を大量投入して「ビジュアル主体」へ転換する
argument-hint: [path or slug] [--create] [重点パターン]
---

# /visual — ビジュアル一点突破コマンド

`/brushup` が「全方向の総合改善」なら、`/visual` は **ビジュアル一点突破**。「文字主体」のスライドを「ビジュアル主体」へ転換することだけに集中する。

毎回作成・編集の度に「ビジュアル面の強化が弱い」と感じる根本原因を、コマンドで叩き直す。

---

## このコマンドが解決する根本問題

| 症状 | 原因 | このコマンドの対処 |
|---|---|---|
| デフォルトで「テキスト主体」になる | Claude の発想が文字に流れがち | ビジュアル要素密度を **機械的に走査** して不足を顕在化 |
| Phosphor 等を「あれば使う」程度 | 取得が後付け | Step 4 で **必要アイコンを最初に並列 curl 取得** |
| 「slide 1 枚にいくつ図があるべきか」が曖昧 | 定量基準なし | **slide 1 枚あたり SVG 2 個以上** を最低基準に |
| 同じパターンばかり | 引き出しが少ない | **§9 ビジュアルパターンカタログ 13 種** を内蔵 |
| 自作 SVG が増えて統一感が崩れる | OSS 辞書が手元にない | **§10 Phosphor 辞書 40 個** を内蔵 |

---

## 思想

- **ビジュアル・ファースト**: テキストより先に図解・イラストで意味を伝える
- **OSS アイコン大量採用**: Phosphor 中心に、1 単元 = **30-50 個** の SVG を目指す
- **design tokens で統一**: `icoNavy` / `icoGold` / `icoRed` / `icoSh` の 4 リソースを全 SVG が共通参照
- **slide 1 枚 = SVG 2 個以上**(section icon + 本文補強図)を最低基準
- **「文字 + アイコン」セット** をデフォルト構成にする(answer-row / quiz-option / list-item 等すべて)

---

## 引数

```
/visual [TARGET] [--create] [重点パターン...]
```

- 位置引数 TARGET: ファイルパス or スラッグ。なし → 直近対象を推定
- `--create`: 新規作成モード(対象が空 / 不在の場合、最初からビジュアル多めで叩き台生成)
- 2 つ目以降: 重点ビジュアルを `,` 区切りで指定(例: `hero,timeline,visual-map`)

---

## 実行手順

### Step 0: 環境確認

1. 対象が `lectures/articles/**/index.html` または `column/articles/**/index.html` または `practices/articles/**/index.html` であること
2. `curl` が利用可能(Phosphor 取得のため)
3. 既存 `<svg width="0" height="0">...</svg>` の **共通 defs(icoNavy/icoGold/icoRed/icoSh)** が body 直後にあるか確認。なければ Step 5 で挿入する

### Step 1: 対象走査(機械的、ビジュアル不足の定量化)

対象 HTML を Read し、以下を集計:

```python
import re
with open(path) as f: s = f.read()
slides = re.split(r'<!-- SLIDE \d+:|<div class="slide(?:\s|")', s)[1:]
for i, sl in enumerate(slides, 1):
    title = re.search(r'data-title="([^"]+)"', sl)
    svg_count = len(re.findall(r'<svg\b', sl))
    text_chars = len(re.sub(r'<[^>]+>', '', sl))  # タグ除去後の文字数
    has_hero = 'hero' in sl or 'section-icon' in sl
    print(f'SLIDE {i}: {title}, svg={svg_count}, chars={text_chars}, hero={has_hero}')
```

判定基準:

| 指標 | しきい値 | 判定 |
|---|---|---|
| SVG 数 | 0 個 | 🔴 致命(必須補強) |
| SVG 数 | 1 個(section icon のみ) | 🟡 不足(本文補強要) |
| SVG 数 | 2+ | ✅ OK |
| 文字数 / SVG 比 | > 800 文字/SVG | 🟡 過剰文字 |
| section divider に hero icon なし | (該当時) | 🟡 不足 |
| icon-card / answer-row 等 list 系で各行アイコンなし | (該当時) | 🟡 不足 |

走査結果を「**優先度付き不足リスト**」として出力。

### Step 2: 不足スライドに対する適用候補パターン提案

§9 ビジュアルパターンカタログから、各不足スライドに最適なパターンを 1-2 個推奨。

判断ロジック:

| スライド種類 | 推奨パターン |
|---|---|
| section divider | hero-icon-large(§9.13) |
| POINT 用語並列 | icon-card-grid(§9.2) |
| 階層概念(N 段の階段) | stairway / pyramid(§9.3) |
| プロセス N 段 | step-flow(§9.4) |
| N タイプ分類 | form-typology(§9.5) |
| 3 軸 × M タイプ表 | matrix-table(§9.6) |
| 時系列 | timeline(§9.7) |
| 用語俯瞰 | visual-map / constellation(§9.8) |
| 事例展開 | case-card-with-icon(§9.9) |
| 人物・要素関係 | relation-diagram(§9.10) |
| A vs B 対比 | comparison-visual(§9.11) |
| answer-row / quiz-option | small-icon-row(§9.12) |

### Step 3: ユーザー承認

```
不足スライド N 件、適用候補 M パターン、新規取得 Phosphor K 個。
Claude 推奨: 全 N 件適用(ビジュアル強化を一気に底上げ)。

進め方:
(a) 全件適用(推奨)
(b) 個別指定(優先度高のみ等)
(c) パターン指定(例: hero と timeline だけ)
(d) 却下
```

### Step 4: Phosphor 並列取得

§10 アイコン辞書を参照し、必要なアイコン名のリストを抽出。並列 curl で取得:

```bash
cd /tmp/phosphor && for icon in {NAMES}; do
  curl -sf "https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/${icon}.svg" -o "${icon}.svg" &
done && wait
```

取得後、各 SVG の inner content から `<rect width="256" height="256" fill="none"/>` を削除し、`stroke="currentColor"` を `stroke="url(#icoNavy)"` に置換。アクセント要素は `url(#icoGold)` に。最初の主要 path に `filter="url(#icoSh)"` を追加。

### Step 5: 共通 defs の確認 / 挿入

body 直後に共通 defs SVG がなければ追加:

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="icoNavy" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5d8eb3"/>
      <stop offset="100%" stop-color="#0F2847"/>
    </linearGradient>
    <linearGradient id="icoGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f4d995"/>
      <stop offset="100%" stop-color="#8a6d1f"/>
    </linearGradient>
    <linearGradient id="icoRed" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#e26375"/>
      <stop offset="100%" stop-color="#8B0A1F"/>
    </linearGradient>
    <filter id="icoSh" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="1.5"/>
      <feOffset dx="0.5" dy="2"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.35"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
</svg>
```

### Step 6: 適用(Edit ツールで順次)

各パターンに対応する CSS と HTML を順次挿入。

実装の優先順:
1. CSS 追加(まとめて 1 回の Edit)
2. 共通 defs 確認 / 追加
3. 各スライドの HTML 編集(優先度高から順次)
4. JS 関数(必要時、選択 / トグル等)を追加

### Step 7: 構文チェック + commit 提案

```python
import re
with open(path) as f: s = f.read()
print('div', len(re.findall(r'<div\b', s)), '/', len(re.findall(r'</div>', s)))
print('svg', len(re.findall(r'<svg\b', s)), '/', len(re.findall(r'</svg>', s)))
print('script', len(re.findall(r'<script\b', s)), '/', len(re.findall(r'</script>', s)))
m = re.search(r'<script>(.*)</script>', s, re.DOTALL); js = m.group(1) if m else ''
print('JS {}', js.count('{'), '/', js.count('}'))
fns = set(re.findall(r'function\s+([A-Za-z_]\w*)\s*\(', js))
calls = set(re.findall(r'onclick="([A-Za-z_]\w*)\(', s))
print('missing onclick funcs:', calls - fns or 'NONE')
```

submodule 内なら submodule で commit → 親リポで参照更新コミット(memory `feedback_submodule_push_order.md` 準拠)。push は明示承認後(memory `feedback_git_push_confirmation.md`)。

### Step 8: 報告

報告には必ず以下を含める:

- before / after の SVG 数(数値で明示)
- 適用したパターン名と該当スライド番号
- 「ブラウザ実機確認推奨」(`python3 -m http.server` でローカル起動)
- 残る伸び代(あれば)

---

## 9. ビジュアルパターンカタログ(13 種)

各パターンは「使いどころ + HTML 雛形 + 必要 Phosphor」のセット。

### 9.1 hero(slide 上部の大型 illust + タイトル + 副題)

**使いどころ**: 各 slide の主題を視覚化(深掘り副題、最新事例、まとめ等)
**Phosphor**: トピックに合うものを 1 個

```html
<div class="visual-hero">  <!-- 既存 .literacy-hero 等と同じ -->
  <svg class="vh-svg" viewBox="0 0 256 256">[Phosphor inner]</svg>
  <div class="vh-text">
    <div class="vh-tag">SECTION TAG</div>
    <div class="vh-title">主題タイトル</div>
    <div class="vh-sub">短い動機文</div>
  </div>
</div>
```

### 9.2 icon-card-grid(POINT 用語の並列カタログ)

**使いどころ**: N 個の用語を並列に紹介、タップで定義表示
**Phosphor**: 各用語に 1 個 = N 個

```html
<div class="icon-cards cols-3">
  <div class="icon-card" data-key="..." onclick="selectIcon('panel','...')">
    <div class="icon-card-tag">① POINT</div>
    <svg class="icon-card-svg" viewBox="0 0 256 256">[Phosphor]</svg>
    <div class="icon-card-name">用語名</div>
    <div class="icon-card-sub">サブ説明</div>
  </div>
</div>
<div class="icon-info-panel" id="panel">▲ タップで定義</div>
```

### 9.3 stairway / pyramid(段階性概念)

**使いどころ**: 階層概念(通信 → 伝達 → 共有 → 相互理解 など)
**Phosphor**: 不要(色とインデントで段階性を表現)

```html
<div class="stairway">
  <div class="stair-step s1"><span class="ss-tag">STEP 1</span><span class="ss-name">基底</span><span class="ss-desc">説明</span></div>
  <div class="stair-step s2">...</div>
  <div class="stair-step s3">...</div>
  <div class="stair-step s4">...</div>  <!-- 頂点は gold アクセント -->
</div>
```

s1〜s4 の `margin-left/right` を段階的に増やしてピラミッド形状に。

### 9.4 step-flow(プロセス N 段の横並び)

**使いどころ**: シャノン flow、命令実行サイクル、ログイン手順 等
**Phosphor**: 各 step に 1 個 = N 個

```html
<div class="flow-row">
  <div class="flow-step"><svg>[icon]</svg><div class="fs-tag">STEP 01</div><div class="fs-name">名前</div></div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">...</div>
</div>
```

中間 step に `noise` クラスを付けると red 強調。

### 9.5 form-typology(N タイプ分類視覚化)

**使いどころ**: 4 タイプ分類(個別 / マスコミ / 逆マス / 会議 等)
**Phosphor**: 各タイプに 1 個 = N 個

```html
<div class="form-typology">  <!-- grid-template-columns: repeat(N, 1fr) -->
  <div class="form-type-card">
    <svg viewBox="0 0 256 256">[Phosphor]</svg>
    <div class="ft-name">タイプ名</div>
    <div class="ft-arrow">関係記号(1↔1 / 1→多 等)</div>
  </div>
</div>
```

### 9.6 matrix-table(N 軸 × M タイプ表)

**使いどころ**: 形態 12 セル、論理回路真理値表
**Phosphor**: 行 / 列 header に 1 個ずつ

各セルにタップ → info-panel 展開のインタラクション付き。`fc-eg` の textContent は初期 `タップ`、`data-eg` 属性に答え保持(CLAUDE.md §4.1「答えは後出し」準拠)。

### 9.7 timeline(時系列視覚化)

**使いどころ**: 通信サービス進歩、歴史、変遷
**Phosphor**: 各ノードに 0-1 個(数が多いとごちゃつくので任意)

```html
<div class="timeline-wrap">
  <div class="timeline-line">
    <div class="tl-node fixed" style="left: 5%;" data-key="..." onclick="revealTl(this,'key')">
      <span class="tl-blank-mark">⑴</span>
      <div class="tl-dot"></div>
      <div class="tl-label">短いラベル</div>
    </div>
    ...
  </div>
  <div class="tl-info-panel" id="tlInfo">▲ ノードタップで時代背景・具体例</div>
</div>
```

各ノードに **タップで「日本での年代 + 説明 + 具体例」を info-panel に表示** するインタラクションを必ず付ける(教材的に説明が必須)。

### 9.8 visual-map / constellation(用語の俯瞰)

**使いどころ**: 答え合わせ slide の上に「視覚的索引」、まとめスライド
**Phosphor**: N 個(各 POINT に 1 個)

```html
<div class="points-map">  <!-- grid-template-columns: repeat(4, 1fr) -->
  <div class="pm-cell"><svg viewBox="0 0 256 256">[Phosphor]</svg><div class="pm-num">①</div><div class="pm-name">用語</div></div>
  ...
</div>
```

または円形配置(SVG 内に絶対座標)。

### 9.9 case-card-with-icon(事例の左にアイコン)

**使いどころ**: case-expander の case-head 左
**Phosphor**: 各 case に 1 個

```html
<div class="case-expander" onclick="toggleCase(this)">
  <div class="case-head">
    <svg class="case-icon" viewBox="0 0 256 256">[Phosphor]</svg>
    <span class="case-year">2020</span>
    <span class="case-title">事例タイトル</span>
    <span class="case-toggle">+</span>
  </div>
  <div class="case-body">本文</div>
</div>
```

### 9.10 relation-diagram(人物・要素関係図)

**使いどころ**: メール To/CC/BCC、ネットワーク図、組織関係
**Phosphor**: 不要(SVG 内に circle + text で人物配置 + 矢印で関係)

矢印の種別で関係を区別:
- 太線: 主要関係(To)
- 細線: 副次関係(CC)
- 点線: 隠れた関係(BCC)

### 9.11 comparison-visual(A vs B 対比)

**使いどころ**: 直接 vs 間接、同期 vs 非同期、紙 vs 電磁的
**Phosphor**: 各側に 1 個 = 2 個

```html
<div class="comparison-grid">
  <div class="cmp-side a-side">
    <svg>[Phosphor A]</svg>
    <h4>A 側</h4>
    <p>説明</p>
  </div>
  <div class="cmp-vs">vs</div>
  <div class="cmp-side b-side">
    <svg>[Phosphor B]</svg>
    <h4>B 側</h4>
    <p>説明</p>
  </div>
</div>
```

### 9.12 small-icon-row(リスト各行の左にアイコン)

**使いどころ**: answer-row、quiz-option、practice-list、list-item
**Phosphor**: 各行に 1 個 = N 個

```html
<div class="answer-row" onclick="revealAnswer(this)">
  <svg class="ar-icon" viewBox="0 0 256 256">[Phosphor]</svg>
  <span class="answer-num">①</span>
  <span class="answer-text">ヒント</span>
  <span class="answer-reveal" data-ans="...">クリック</span>
</div>
```

CSS で `.ar-icon` に `padding: 4px; background: rgba(201,169,97,0.15); border-radius: 6px;` で背景パッド。revealed 時に green に。

### 9.13 hero-icon-large(section divider の大型イラスト)

**使いどころ**: 各節の section-divider
**Phosphor**: 1 個(節を象徴する)

```html
<div class="slide section-divider">
  <div class="section-number">SECTION · 0N</div>
  <svg class="section-icon" viewBox="0 0 256 256">
    [Phosphor inner、stroke="rgba(255,255,255,0.9)" + 一部 url(#icoGold)]
  </svg>
  <h2 class="section-title-big">節タイトル</h2>
  <p class="section-tagline">副題</p>
</div>
```

navy 背景のため stroke は **白半透明**(`rgba(255,255,255,0.9)`)。アクセント要素のみ `url(#icoGold)`。

---

## 10. Phosphor アイコン辞書(よく使う 40 個)

URL pattern: `https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/{name}.svg`

### 10.1 人・組織
- `user` 1 人
- `users` 2-3 人
- `users-three` 3 人(横並び)
- `handshake` 握手・合意
- `person-simple` 棒人間
- `buildings` 建物・組織

### 10.2 通信・コミュニケーション
- `chats-circle` 双方向対話
- `chats-teardrop` 単方向吹き出し
- `paper-plane-tilt` 送信・配信
- `envelope-simple` メール
- `phone` 電話
- `megaphone-simple` 拡声・発信
- `microphone` 集音・受信

### 10.3 メディア・配信
- `broadcast` 放送・電波
- `waveform` 波形・音声
- `video-camera` 映像
- `radio` ラジオ

### 10.4 時間
- `clock` 時計
- `clock-clockwise` 同期・周期
- `calendar` 日付
- `hourglass` 経過時間

### 10.5 場所・移動
- `globe` 世界・グローバル
- `map-pin` 位置
- `arrows-left-right` 双方向
- `arrow-right` 単方向
- `arrow-clockwise` 循環

### 10.6 データ・計算
- `chart-bar` 棒グラフ・量
- `chart-line` 線グラフ・推移
- `database` データベース
- `cloud` クラウド・蓄積
- `cube` 立方体・モジュール

### 10.7 AI・コンピュータ
- `cpu` プロセッサ
- `brain` 脳・知能
- `lightning` 高速・電撃
- `sparkle` 生成・創発
- `device-mobile-camera` スマートフォン

### 10.8 セキュリティ・法律
- `lock-key` 鍵・暗号
- `shield` 防御・セキュリティ
- `eye` 監視・公開
- `scales` 公平・法
- `gavel` 法令・判決

### 10.9 UI・操作
- `gear` 設定
- `magnifying-glass` 検索・吟味
- `link-simple` リンク・参照
- `squares-four` 分類・ダッシュボード

---

## 11. design tokens(必須)

全 SVG が以下の 4 リソースを参照(body 直後の共通 defs で 1 度定義、Step 5):

| ID | 種類 | 色 | 用途 |
|---|---|---|---|
| `icoNavy` | linearGradient | 5d8eb3 → 0F2847 | 主役 path の stroke |
| `icoGold` | linearGradient | f4d995 → 8a6d1f | アクセント・重要要素 |
| `icoRed` | linearGradient | e26375 → 8B0A1F | 警告・対比 |
| `icoSh` | filter | drop-shadow | 主要 path に立体感 |

各 SVG の編集ルール:
1. 冒頭の `<rect width="256" height="256" fill="none"/>` を **削除**(SKILL.md §9.19)
2. `stroke="currentColor"` を `stroke="url(#icoNavy)"` に置換(基本)
3. アクセントしたい要素のみ `stroke="url(#icoGold)"` に
4. 最初の主要 path に `filter="url(#icoSh)"` を追加
5. SVG 内に `<text>` で役割ラベルを書かない(SKILL.md §9.20、HTML 化)

`section-divider`(navy 背景)上の SVG は例外: stroke を `rgba(255,255,255,0.9)` + アクセント `url(#icoGold)` に。

---

## 12. やらないこと(アンチパターン)

- ❌ **自作 SVG での「リッチ化」** — 必ず Phosphor 等 OSS から借りる(§13.6 SKILL.md の「ライブラリ風 line-art に揃える」は例外手段)
- ❌ **個別 unique gradient id**(g1, g2, ... )— 共通 defs に統一
- ❌ **SVG 内 `<text>` で役割ラベル** — HTML 化(`.icon-card-tag` / `.pm-num` 等)
- ❌ **絵文字を本文に使う** — 装飾目的の絵文字は SKILL.md §8 で禁止
- ❌ **`<rect width="256" height="256" fill="none"/>` を残す** — SKILL.md §9.19
- ❌ **slide 1 枚に SVG 0 個** — section icon だけでも必ず 1 個入れる
- ❌ **answer-row / quiz-option 各行にアイコンなし** — 視覚的検索性が落ちる、必ず small-icon-row パターン

---

## 13. 引数 example

```bash
/visual
# 直近編集対象を推定し、不足スライドを抽出 → 全部適用

/visual lectures/articles/08-communication-and-media
# 対象を明示

/visual --create lectures/articles/12-NEW-UNIT
# 新規作成モード(空 / 不在ディレクトリから叩き台生成、ビジュアル多め)

/visual 08 hero,timeline
# 重点パターン指定(hero と timeline だけ追加)

/visual 09-information-design comparison
# スラッグ + 重点パターン
```

---

## 14. 完了の判定

- ビジュアル要素密度が「全 slide で SVG 2 個以上」を満たす
- HTML タグバランス OK(div / svg / script)
- JS バランス OK(`{}()[]`)、関数参照欠落 0
- before / after で SVG 数が **+50% 以上** 増加(目安)
- ブラウザ実機確認はユーザーに依頼

ユーザーが「OK」「次へ」と返した時点で完了。

---

## 15. /brushup との使い分け

| シナリオ | 使うコマンド |
|---|---|
| 教材を一通り作った直後の総合改善 | `/brushup` |
| デザイン規約点検(自作 SVG → OSS 等) | `/brushup` |
| 「ビジュアルが足りない」と感じた時 | **`/visual`** |
| 新規単元を作る時(ビジュアル多めスケルトン) | **`/visual --create`** |
| 構成深掘り(深掘り副題追加) | `/brushup` |
| インタラクション強化(quiz / case-expander 追加) | `/brushup` |
| アクセシビリティ(ARIA / キーボード) | `/brushup`(将来) |

`/visual` で骨格(ビジュアル)を入れた後 `/brushup` で全方向チェック、または `/brushup` で構成を整えた後 `/visual` で見栄え強化、どちらの順でも有効。
