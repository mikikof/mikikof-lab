---
name: interactive-practice
description: ベストフィット問題集を原本に演習用Web教材を制作するときに使う skill。情報Ⅰ・情報数理入門などの節単位で、PCとスマホで動く隙間時間学習ツールを単一HTMLで作る。青基調のクールトーン、教科書フォント、Q&A形式のおさらい、6種の入力タイプ、自動注入リトライ、左サイドバータイムライン、原本完全準拠、ビジュアル必須を標準装備する。新しい単元の依頼、既存単元の修正、類似の演習教材作成のときにこの skill を読み込む。
---

# interactive-practice / 演習用 Web 教材制作 skill

このスキルは `practices/` ツール内で、実際に演習サイトを作るための**技術仕様と落とし穴**を定義する。

---

## 使うとき

- ベストフィット問題集 1章03 のような **節単位の演習教材** を新規作成
- 既存単元の **部分修正・追加**
- 類似形式の **採点付き Web 演習ツール** を作成

---

## 前提

作業着手前に**必ず**以下を順に読むこと:

1. `practices/CLAUDE.md` ― 制作哲学・禁止事項・チェックリスト(「何を・なぜ」側)
2. 本ファイル(`SKILL.md`) ― 技術仕様と落とし穴(「どう」側)
3. `components.md` ― 部品カタログ(コピペ元)
4. `examples/01-03-intellectual-property.html` ― **動いている完成品リファレンス**
5. `practices/_source/ベストフィット問題/` の対応 docx + `practices/_source/ベストフィット解答/` の対応問題範囲 ― **正本**

---

## 1. 全体構成(標準: 14ステージ)

過去の 01-03 知的財産権を基準とした標準構成:

```
Stage 0  Welcome              単元概要・流れ
Stage 1  Visual Digest        Q&A 形式のおさらい(6モジュール)
Stage 2  例題 9               お手本ツアー1
Stage 3  例題 10              お手本ツアー2
Stage 4  例題 11              お手本ツアー3
Stage 5  練習 Q15            演習1
Stage 6  練習 Q16            演習2
...
Stage 12 練習 Q22            演習8
Stage 13 Summary             結果サマリ
```

問題数は単元により変動するが、**Welcome + Digest + 例題群 + 練習群 + Summary** の5部構成は固定。

### 標準装備(必ず外さないこと)

- **左サイドバータイムライン**:全環境で開閉可能なドロワー
  - PC: 初期表示で開、`body.sb-open` が `padding-left: 280px` で本文を右にずらす
  - モバイル: 初期は閉、ハンバーガーボタンで開く、背景タップで閉じる
  - M キー / Esc / 内部× ボタン / 背景タップ で開閉
- **進捗バー**:topbar 下のグラデ帯、現在ステージをリアルタイム反映
- **ステップ送り**:前 / 次 ボタン(footnav)、矢印キー、スワイプ
- **タップターゲット**: モバイル 44px+、デスクトップ 38px+
- **iPhone セーフエリア**: `viewport-fit=cover` + `env(safe-area-inset-bottom)`

---

## 2. Design Tokens(絶対に守る — 青基調・クール・低ストレス)

CSS 変数で統一管理する。問題ごと・モジュールごとに色を変えない。

```css
:root {
  /* Background — cool blue-white */
  --bg-cream:  #F4F8FC;       /* メイン背景 */
  --bg-card:   #FFFFFF;       /* カード背景 */
  --bg-soft:   #E8F0F9;       /* ソフト面(セクション・サブ) */
  --bg-paper:  #FAFCFF;       /* ペーパー(問題文ボックス・ホバー時) */

  /* Ink — deep navy */
  --ink:       #1A2B47;       /* 主役テキスト・大見出し */
  --ink-soft:  #475673;       /* 本文・解説 */
  --ink-mute:  #75839B;       /* 補助・メタ */
  --ink-faint: #B0BAC9;       /* 罫線・薄字 */

  /* Action: refined medium blue */
  --action:       #4A78C8;    /* 主役のアクション(プライマリボタン・選択中) */
  --action-deep:  #2E5894;    /* hover */
  --action-pale:  #DAE6F5;    /* 背景タグ・パレット薄 */
  --action-pale2: #B8CDE6;    /* 罫線アクセント */

  /* Anchor: deep navy */
  --anchor:      #122E55;     /* 重い見出し・基準色 */
  --anchor-mid:  #2A4A78;
  --anchor-pale: #DDE7F2;

  /* Success: muted teal-green */
  --ok:      #41A38C;
  --ok-pale: #C5E2D9;
  --ok-deep: #2E826F;

  /* Error: muted rose */
  --ng:      #C84A60;
  --ng-pale: #F0D5DB;
  --ng-deep: #8E3344;

  /* Highlight: sophisticated amber(寒色のみだと冷たいのでワンポイントだけ) */
  --gold:      #D4A852;
  --gold-pale: #F5E5BB;
  --gold-deep: #A37A1F;

  /* Lines — cool light blue-grey */
  --line:        #D8E2EE;
  --line-soft:   #E8EFF7;
  --line-strong: #B8C5D7;

  /* Typography */
  --f-display:    'Fraunces', 'Playfair Display', Georgia, serif;
  --f-jp-display: 'YuKyokasho Yoko', 'YuKyokasho', '游教科書体 横用', '游教科書体', 'Klee One', 'UD Digi Kyokasho N-R', 'Hiragino Mincho ProN', 'Yu Mincho', '游明朝', serif;
  --f-jp-body:    'Zen Kaku Gothic New', 'Hiragino Sans', sans-serif;
  --f-mono:       'JetBrains Mono', monospace;
  --f-la:         'DM Sans', system-ui, sans-serif;

  --ease: cubic-bezier(0.22, 0.61, 0.36, 1);
  --shadow-card:        0 14px 30px -12px rgba(26, 43, 71, 0.12), 0 2px 8px -2px rgba(26, 43, 71, 0.06);
  --shadow-card-hover:  0 22px 44px -14px rgba(74, 120, 200, 0.18), 0 4px 12px -2px rgba(26, 43, 71, 0.08);
}
```

### Google Fonts の読み込み

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;1,9..144,400;1,9..144,600;1,9..144,800&family=Klee+One:wght@400;600&family=Zen+Kaku+Gothic+New:wght@300;400;500;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

### フォントの使い分け

| 要素 | フォント | 用途 |
|---|---|---|
| 単元タイトル英 / Q番号 / 引用符 / モジュール番号 | `--f-display`(Fraunces italic) | 視線を惹くイタリック装飾 |
| 単元タイトル日 / 問題タイトル / セクション見出し / 用語ラベル / SVG内の権利名 | `--f-jp-display`(YuKyokasho 系教科書体) | 教科書らしい柔らかな見出し |
| 本文・解説・選択肢・サブ問題テキスト・SVGの説明文 | `--f-jp-body`(Zen Kaku Gothic New) | 読み続ける長文 |
| ラベル・年数・進捗番号・チップ | `--f-mono`(JetBrains Mono) | メタ情報の等幅 |
| 英数小ラベル(LIVE / TAP / EXAMPLE 1/3) | `--f-la`(DM Sans) | 英ラベル小文字 |

**禁止**: 連続文に明朝を使うことは禁止(スマホで読みづらくなる)。明朝は短い見出し・用語名にのみ使う。

### 標準フォントサイズ・太さ

| 要素 | サイズ | 太さ | 備考 |
|---|---|---|---|
| `.problem-q` / `.problem-q.lead` | 16px(1rem) | 500 | 問題文 |
| `.opt-text` / `.match-text` / `.ox-text` | 16px(0.96rem) | 500 | 選択肢・小問 |
| `.fb-explain` / `.fb-bestfit` | 14.7px(0.92rem) | 500 | 解説本文 |
| `.problem-title` | clamp(1.3, 3vw, 1.7)rem | 900 | 単元のタイトル |
| `.problem-q-num` | 3.6rem | 800 | Q番号(Fraunces italic) |
| `.welcome-title-en` | clamp(2.2, 6vw, 3.4)rem | 800 | ウェルカム英タイトル |
| `.welcome-title-jp` | clamp(1.4, 3.5vw, 2)rem | 900 | ウェルカム日タイトル |

スマホ(`@media (max-width: 720px)`)では各要素を 1段階縮小。

---

## 3. レイアウト設計の核

### 3.1 サイドバー + メインコンテンツ

```css
.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: 280px;
  transform: translateX(-100%);  /* 初期は閉 */
  transition: transform 0.35s var(--ease);
  z-index: 60;
}
.sidebar.open { transform: translateX(0); }

@media (min-width: 1100px) {
  body { transition: padding-left 0.35s var(--ease); }
  body.sb-open { padding-left: 280px; }   /* PC で開のとき本文を右にずらす */
  .footnav { transition: left 0.35s var(--ease); left: 0; }
  body.sb-open .footnav { left: 280px; }
  .sidebar-backdrop { display: none !important; }  /* PC では背景フィルター不要 */
}
```

PC は初期表示で `body.sb-open` を JS でつけて開く。モバイルは閉のまま。

### 3.2 トップバー

```css
.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(244, 248, 252, 0.92);  /* 半透明 + blur */
  backdrop-filter: saturate(180%) blur(14px);
  border-bottom: 1px solid var(--line);
}
```

中身: メニューボタン + ブランド + 進捗バー + リスタートボタン

### 3.3 ステージコンテナ

```css
.stage { display: none; animation: stageEnter 0.4s var(--ease); }
.stage.active { display: block; }
@keyframes stageEnter {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
```

ステージ間遷移は `stages[currentStage].classList.add('active')` で切り替え + 上にスクロール。

### 3.4 フッターナビ

```css
.footnav {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: rgba(244, 248, 252, 0.94);
  backdrop-filter: ...;
  z-index: 40;
  padding-bottom: env(safe-area-inset-bottom);  /* iPhone ホームインジケータ対応 */
}
```

中身: 前ボタン + 進捗テキスト + 次ボタン

---

## 4. ナビゲーション(全ステージ共通)

```javascript
const stages = Array.from(document.querySelectorAll('.stage'));
const totalStages = stages.length;
let currentStage = 0;

function goToStage(n) {
  if (n < 0 || n >= totalStages) return;
  stages[currentStage].classList.remove('active');
  currentStage = n;
  stages[currentStage].classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  updateUI();
  if (currentStage === totalStages - 1) renderSummary();
}

document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'Escape' && sidebar.classList.contains('open')) { closeSidebar(); return; }
  if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); goToStage(currentStage + 1); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); goToStage(currentStage - 1); }
  else if (e.key === 'Home') goToStage(0);
  else if (e.key === 'End') goToStage(totalStages - 1);
  else if (e.key === 'm' || e.key === 'M') toggleSidebar();
});

// Touch swipe (ボタン要素は除外、スマホで誤動作させない)
document.addEventListener('touchend', (e) => {
  if (!touchStart) return;
  const dx = e.changedTouches[0].clientX - touchStart.x;
  const dy = e.changedTouches[0].clientY - touchStart.y;
  const dt = Date.now() - touchTime;
  if (dt < 800 && Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    const target = e.target;
    if (target.closest('button, label, input, .opt, .ox-row, .match-pill, .fill-chip, .fill-blank')) return;
    if (dx < 0) goToStage(currentStage + 1);
    else goToStage(currentStage - 1);
  }
  touchStart = null;
}, { passive: true });
```

---

## 5. 入力タイプ(6種類)

すべて `data-input` 属性で識別する。詳細 HTML は `components.md` を見る。

| タイプ | 用途 | data-correct の形式 |
|---|---|---|
| `single` | 4択から1つ選ぶ(例題9, 11) | `data-correct="0"`(0始まりインデックス) |
| `multi` | 複数選択(例題10, Q20) | `data-correct="1,2,5,6,7"` |
| `match` | 各小問に選択肢から1つマッチ(Q15, Q16, Q19) | `data-options="ア,イ,ウ,エ"` + `data-correct="3,0,1,2"` |
| `ox` | 各小問に ○ × 判定(Q17, Q18) | `data-correct="o,x,o,x,o"` |
| `fill` | 語群穴埋め(Q21) | グレードボタンに `data-fill-correct="公表,必然性,..."` |
| `multi_per_sub` | 各小問に複数マッチ(Q22 CCマーク) | `data-options="ア,イ,ウ,エ"` + `data-correct="0,1\|0,2\|0,1,3"`(`\|` で小問区切り) |

### 採点ロジック

`gradeStage(stage, isExample)` 関数が各タイプを処理。基本ルール:

- **single**: 1点満点。userIdx が correct と一致で1点。
- **multi**: correct の長さが満点。正しいピック数 - 誤ピック数(min 0)が score。
- **match**: 小問数が満点。各小問で userIdx === correctIdx なら +1 点。
- **ox**: 小問数が満点。各小問で userVal が ○/× の正解と一致なら +1 点。
- **fill**: 空欄数が満点。各空欄が正解語と一致なら +1 点。
- **multi_per_sub**: 小問数が満点。各小問で `userPicks` の集合が `correctSubs[i]` の集合と完全一致なら +1 点(部分正解は不可)。

### 採点後のロック

- `lockBox(input)` で `data-locked="true"` を設定 → クリック handler で `box.dataset.locked === 'true'` のとき入力を無視
- フィードバックを `.show` クラスで表示
- `gradeStage` の最後に retry / next ボタンを `showFeedback` 内で **動的注入**(冪等)

---

## 6. ビジュアル(viz)タイプ

各問題の解説後に必ず添える。`components.md` から該当パターンをコピーする。

| パターン | 用途 | クラス |
|---|---|---|
| **IP rich card grid** | 4種マッチング(産業財産権4種) | `.ip-rich-grid` + `.ip-rich.{patent\|utility\|design\|trademark}` |
| **Right tree** | 階層構造(著作者の権利ツリー) | `.right-tree` + `.rt-row.indent[2\|3]` |
| **Compare 2-col** | 二項対比(産業 vs 著作 / 人格権 vs 財産権 / 著作者 vs 伝達者) | `.compare` + `.compare-col.{left\|right}` |
| **Lock vs Key** | 譲渡可否対比 | `.lk-grid` + `.lk-card.{locked\|transferable}` |
| **Boundary cards** | キーワード境界線(例外規定) | `.bd-grid` + `.bd-card` |
| **Checklist** | 要件チェックリスト(引用7要件) | `.checklist` + `.cl-item` |
| **CC mark grid** | CC マーク組み合わせ | `.cc-grid` + `.cc-row` + `.cc-mark.{by\|nc\|nd\|sa}` |
| **Origin compare flow** | 発生方式対比(出願主義 vs 無方式) | `.origin-compare` + `.origin-flow` + `.origin-step` |
| **SVG protection timeline** | 保護期間ガントチャート(産業財産権) | `<svg class="viz-svg wide" viewBox="0 0 600 240">` |
| **SVG judgment flow** | 判定フローチャート(著作権侵害) | `<svg class="viz-svg wide" viewBox="0 0 600 300">` |
| **SVG family tree** | 知的財産権の体系図(おさらい用) | `<svg class="family-tree-svg" viewBox="0 0 760 380">` |

ワイドな SVG は `.viz-svg-wrap` でラップし、`min-width: 580px` を持たせて narrow viewport では横スクロール。

---

## 7. おさらい(REVIEW Digest)の Q&A 構造

★ ここの構造を間違えると入れ子バグが出る。`§9.1` 参照。

```html
<section class="stage" data-stage-name="REVIEW">
  <div class="section-divider">...</div>
  <div class="digest">

    <div class="digest-mod hero">
      <button class="digest-prompt" type="button">
        <div class="digest-prompt-head">
          <span class="digest-num">01</span>
          <span class="digest-en">The Big Map</span>
          <span class="digest-toggle"><span class="plus">+</span></span>
        </div>
        <div class="digest-q">知的財産権はどう分類される?</div>
      </button>
      <div class="digest-answer">
        <div class="digest-title">知的財産権 ファミリーツリー</div>
        <p class="digest-lede">…</p>
        [visual content here]
      </div>
    </div>

    <div class="digest-mod">  <!-- 02 — 兄弟関係(入れ子しない) -->
      ...
    </div>

    [04, 05, 06 も同じ構造で兄弟関係]

  </div>
</section>
```

**重要**:
- すべての `.digest-mod` は `.digest` の **直接の子**(兄弟関係)。入れ子にしない
- 各 `.digest-mod` は3要素: `<button class="digest-prompt">` + `<div class="digest-answer">` + 自身の closing `</div>`
- JS は **独立トグル**(アコーディオンにしない、ユーザーの好み)

```javascript
document.querySelectorAll('.digest-prompt').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    btn.parentElement.classList.toggle('open');
  });
  // <button> は Enter/Space で自動的に click を発火するため、keydown 不要
});
```

### 標準的な6モジュール構成

| 番号 | Q | A の中身 |
|---|---|---|
| 01 | この単元のテーマはどう分類される?(全体俯瞰) | SVG family tree |
| 02 | (主要分類1) の各種は何を保護する? | カラフル4種カードグリッド |
| 03 | (発生・成立の対比軸) | フロー対比 / 比較ボックス |
| 04 | (二項対立的な構造) | 鍵 vs 譲渡 などの2列カード |
| 05 | (例外・境界線・条件) | キーワードカード + 警告ボックス |
| 06 | (実用的な早見表 / 補助情報) | 4色マークグリッド + 主要組み合わせ |

---

## 8. 各問題のリトライ機能

### 仕組み

`showFeedback` 関数内で、フィードバック表示時に retry / next ボタンを動的注入する(冪等):

```javascript
const fbBody = fb.querySelector('.fb-body');
if (fbBody && !fbBody.querySelector('.fb-retry')) {
  const wrap = document.createElement('div');
  wrap.className = 'fb-retry';
  const isExample = !!(opts && opts.example);
  const retryLabel = isExample ? 'もう一度確認' : 'もう一度解く';
  wrap.innerHTML =
    '<button class="btn-retry" data-action="retry"><span class="ico">↻</span>' + retryLabel + '</button>' +
    '<button class="btn-retry next" data-action="goto-next"><span>次の問題へ</span><span class="ico">→</span></button>';
  fbBody.appendChild(wrap);
  wrap.querySelector('[data-action="retry"]').addEventListener('click', () => retryStage(stage));
  wrap.querySelector('[data-action="goto-next"]').addEventListener('click', () => goToStage(currentStage + 1));
}
```

`retryStage` 関数は `data-locked` を解除、grade 状態を全クリア、解答ボタンを再表示、`probState[id]` を削除、タイムラインを更新、問題カード先頭にスクロール。

すべての入力タイプ(`single, multi, match, ox, fill, multi_per_sub`)に対応すること。

---

## 8.5 モバイルリッチ UI(spotlight / haptic / 横スワイプ snap カルーセル)

スマホ実機でリッチに感じる工夫。新規単元でもこの3つは必ず装備する。

### 8.5.1 スポットライト v2(タップで劇場的フォーカス)

`.ip-rich` `.bd-card` `.lk-card` `.cc-cat-item` のいずれかをタップすると、そのカードが大きく拡大(`scale(1.18)` PC / `scale(1.12)` モバイル)、ゴールド色のリング(`box-shadow 0 0 0 3px rgba(212,168,82,0.55)`)で縁取られ、画面全体が radial-gradient + backdrop-filter blur で暗転する(`body.has-spotlight-active .spotlight-backdrop`)。`spotPulse` キーフレームでタップの瞬間に少しオーバーシュートして落ち着く演出。フォーカスカードは自動でビューポート中央へスクロール。

解除条件: 同じカードを再タップ / バックドロップ(画面の暗い部分)タップ / 親グリッド外タップ / Esc キー。「タップで解除 ✕」の小さな丸い hint がモバイル底部に出る。

```javascript
const SPOT_SELECTOR = '.ip-rich, .bd-card, .lk-card, .cc-cat-item';
document.addEventListener('click', (e) => {
  if (e.target.closest('button, label, input, .digest-prompt')) return;
  const card = e.target.closest(SPOT_SELECTOR);
  if (!card) {
    document.querySelectorAll('.spotlight').forEach(el => el.classList.remove('spotlight'));
    document.querySelectorAll('.has-spotlight').forEach(el => el.classList.remove('has-spotlight'));
    return;
  }
  const grid = card.parentElement;
  const wasActive = card.classList.contains('spotlight');
  grid.querySelectorAll('.spotlight').forEach(el => el.classList.remove('spotlight'));
  if (wasActive) grid.classList.remove('has-spotlight');
  else { card.classList.add('spotlight'); grid.classList.add('has-spotlight'); haptic(8); }
}, { passive: true });
```

CSS:
```css
.has-spotlight > .ip-rich:not(.spotlight),
.has-spotlight > .bd-card:not(.spotlight),
.has-spotlight > .lk-card:not(.spotlight),
.has-spotlight > .cc-cat-item:not(.spotlight) {
  opacity: 0.34; filter: saturate(0.65);
}
.ip-rich.spotlight, .bd-card.spotlight, .lk-card.spotlight, .cc-cat-item.spotlight {
  transform: scale(1.04); z-index: 3; position: relative;
  box-shadow: 0 24px 50px -16px rgba(74, 120, 200, 0.28), 0 6px 14px -2px rgba(26, 43, 71, 0.14);
}
```

新しい「短冊型カード」を viz パターンに加える場合は、必ず `SPOT_SELECTOR` と CSS の `.has-spotlight > .X:not(.spotlight)` 群に新クラス名を追加する。

### 8.5.2 haptic フィードバック

```javascript
function haptic(ms) {
  try { if (navigator.vibrate) navigator.vibrate(ms || 8); } catch (_) {}
}
// データアクション付きボタン全部に委譲
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-action="grade"], [data-action="reveal"], [data-action="retry"], [data-action="goto-next"]');
  if (t) haptic(10);
});
```

iOS Safari は Web Vibration API 非対応 → grace degrade して何も起きない(エラーにしない)。Android Chrome / 一部 PWA では実際に振動する。

### 8.5.3 3-col 比較を mobile 横スワイプ snap カルーセル + ドットインジケーターに変換

`.origin-compare` を 3 列にしたいとき、inline style ではなく `.three-col` クラスで指定する。デスクトップは 3 列、モバイルは横スワイプの snap カルーセル(各カード幅 84vw)に切り替わる。

```html
<div class="origin-compare three-col">
  <div class="origin-side ...">...</div>
  <div class="origin-side ...">...</div>
  <div class="origin-side ...">...</div>
</div>
```

JS が自動で挿入:
- 上に `<div class="carousel-hint">← 横にスワイプ →</div>`(モバイルのみ表示)
- 下に `<div class="carousel-dots">` ドットインジケーター。子の `.origin-side` 数だけ `.dot` を生成し、IntersectionObserver でカルーセルスクロールに連動して `active` クラスを切り替える(active 時は伸びるカプセル状)
- `isInsideHorizontalScroll` が `.three-col` の overflow-x:auto を検知するので、page-swipe ハンドラとも干渉しない

### 8.5.4 サマリスコアのカウントアップ

サマリ画面に到達したら、`summary-grade` `stat-full` `stat-partial` `stat-skipped` `stat-rate` の値を 0 から実際の値へ easeOutCubic でカウントアップ(`animateCounter(el, from, to, duration, suffix)`)。完答 5/6 のような結果が「数字が積み上がっていく」感覚で出る。

### 8.5.5 ステージ遷移の haptic

`goToStage` 内で 6ms vibrate(モバイル時のみ実際に振動)。ページ送りの手応えがほんの少しだけ加わる。

---

## 9. 既知の落とし穴(必ずチェック)

### 9.1 おさらい digest の入れ子バグ ★最重要
- **症状**: あるカードを開くと、後続のカード(N+1, N+2 ...)も全部展開される
- **原因**: 各 `.digest-mod` を正しく `</div>` で閉じていないため、後続が前のカード内にネストされる
- **対策**: 各 `.digest-mod` は3要素で完結する明示的な `</div>` を持たせる(本ファイル §7 参照)
- **再生産防止**: Python スクリプトで自動構造変換するときは、必ず DOM を depth カウンターで検証する

### 9.2 showFeedback の null reference バグ
- **症状**: 例題で「解答を見る」を押しても解説が表示されない
- **原因**: 例題の banner HTML には `.score-tag` 要素がないのに、`scoreTag.textContent = ''` を呼んで `TypeError`
- **対策**: すべての DOM 参照を null-safe にする
  ```javascript
  if (scoreTag) scoreTag.textContent = scoreLabel;
  const iconEl = banner ? banner.querySelector('.icon') : null;
  if (iconEl) iconEl.textContent = icon;
  ```

### 9.3 Enter/Space の二重発火
- **症状**: キーボードで操作したときトグルが効かない
- **原因**: `<button>` は Enter/Space で自動的に click を発火する。さらに keydown ハンドラで toggle を呼ぶと、合計2回トグルされて元に戻る
- **対策**: `<button>` 要素には click ハンドラだけを付ける。keydown ハンドラを別途付けない

### 9.4 スワイプとタップの干渉
- **症状**: 選択肢タップが意図せず次のステージに飛ぶ、または逆にスワイプが効かない
- **対策**: touchend ハンドラで以下を除外:
  ```javascript
  if (target.closest('button, label, input, .opt, .ox-row, .match-pill, .fill-chip, .fill-blank')) return;
  ```

### 9.4b 水平スクロール SVG とスワイプの干渉 ★スマホ実機で発覚
- **症状**: family-tree-svg や `.viz-svg-wrap` の中で SVG を横スクロールしようとすると、ページが次/前のステージへ遷移してしまう
- **原因**: 水平スクロールのジェスチャと page-swipe のジェスチャの形状が同じ。touchend の closest 除外リストにスクロール領域が含まれていない
- **対策**: touchstart の時点で「タッチ開始位置がスクロール可能領域の中か」を判定し、フラグを立てて touchend でスワイプ処理をスキップする
  ```javascript
  function isInsideHorizontalScroll(el) {
    if (!el) return false;
    if (el.closest && el.closest('.viz-svg-wrap, .family-tree-wrap')) return true;
    let node = el;
    while (node && node !== document.body) {
      const cs = window.getComputedStyle(node);
      if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && node.scrollWidth > node.clientWidth + 1) return true;
      node = node.parentElement;
    }
    return false;
  }
  // touchstart で touchInScrollable = isInsideHorizontalScroll(e.target) を保持
  // touchend で touchInScrollable が真ならスワイプ無視
  ```
- **教訓**: 横スクロールできる領域を新しく追加するときは、必ずクラス名を `isInsideHorizontalScroll` の closest 引数に追記する(generic な computed style 検査も走るが、明示的に書く方が安全)

### 9.4c 採点後のフィードバックが画面外上に飛ぶ ★スマホ実機で発覚
- **症状**: 採点ボタンを押すと、本来見たい「正答」バナーがビューポート外(上)に行ってしまい、ユーザーが上に戻る必要がある
- **原因**: `scrollIntoView({ block: 'center' })` を使うと、フィードバック全体が縦長のため中央寄せ時に先頭が画面外上に出る
- **対策**: 「banner を sticky topbar の直下に置く」ように手動でスクロール
  ```javascript
  setTimeout(() => {
    const banner = fb.querySelector('.fb-banner') || fb;
    const topbar = document.querySelector('.topbar');
    const topbarH = topbar ? topbar.getBoundingClientRect().height : 0;
    const rect = banner.getBoundingClientRect();
    const targetY = window.scrollY + rect.top - topbarH - 12;
    window.scrollTo({ top: Math.max(0, targetY), behavior: 'smooth' });
  }, 100);
  ```
- **同じ修正**: `retryStage` の「もう一度解く」スクロールも sticky topbar を考慮した同じ計算に揃える

### 9.4d iOS の二重タップズーム遅延
- **症状**: 採点ボタンや選択肢タップに 300ms ほどの遅延があり、もたつく
- **対策**: 主要なタップ要素に `touch-action: manipulation` を当てる(double-tap zoom を無効化、Safari 旧来の click delay も解消)
  ```css
  button, .opt, .ox-btn, .ox-row, .match-pill, .fill-chip, .fill-blank,
  .digest-prompt, .tl-item, [data-action], a.unit-card, .unit-card { touch-action: manipulation; }
  ```

### 9.5 クール基調にしたつもりが SVG 内のハードコード色が温色のまま
- **原因**: SVG の fill/stroke は CSS 変数を読まない(SVG 属性として直接指定すると、`currentColor` 以外は解釈されない)
- **対策**: SVG 内のハードコード hex 値は、Design Tokens 変更時に **個別に追従**(または class + CSS で持たせる)

### 9.6 サイドバー開閉でレイアウトが崩れる
- **症状**: PC で開閉時に topbar の中身が左寄せになる
- **対策**: body 全体に `padding-left: 280px` をかける(.topbar-inner などの個別 margin-left ではなく)。`.footnav` は `position: fixed` なので別途 `left: 280px` を指定する必要がある(body padding が効かない)

### 9.7 iPhone でフッタの最後の行が見切れる
- **対策**: `<meta name="viewport" content="..., viewport-fit=cover">` + `padding-bottom: env(safe-area-inset-bottom)` を body と footnav 両方に

### 9.8 例題が「正答が見える」状態で表示される
- **対策**: 例題の正答テキストは banner の文言(「正答: (ア)」など)に書いてあるが、`.feedback` は初期 `display: none` なので、ユーザーが「解答を見る」を押すまで非表示

### 9.9 単元 docx と解答 docx の問題範囲がずれる
- **症状**: 解答 docx は1章まとめなので、節別問題 docx の範囲を取り違えると違う問題の解説を載せてしまう
- **対策**: 必ず各小問の番号(類題15、練習問題18 など)を明示的に対応させて確認する

### 9.10 hyperref / 記号の方言ズレ
- **症状**: 原本は `，`(全角西洋カンマ、教科書慣例)、自分は `、` で書きがち
- **判断**: 原本完全準拠を優先する場合は `，` に揃える。可読性優先なら `、`(現状)。**ユーザーに方針を確認**

### 9.11 docx unzip でテキストが run 単位で分かれている
- **対策**: `word/document.xml` を直接開かず、`<w:t>` 要素のテキストをすべて連結してから抽出(本ツール初期実装の Python スクリプトを参照)

---

## 10. レスポンシブ仕様

### ブレイクポイント

- **≥ 1100px**(PC・投影): サイドバー併用、本文は 920px max-width 中央寄せ
- **720–1099px**(タブレット): サイドバーはドロワー、本文 920px max-width
- **≤ 720px**(スマホ縦): 1カラム、タップターゲット 44px+、SVG は横スクロール
- **≤ 380px**(iPhone SE 等): さらに余白縮小、フッタの "X of Y" 非表示
- **landscape phone**(`(max-height: 500px) and (orientation: landscape)`): 縦スペース狭いので必要に応じてヘッダ縮小

### モバイル時のチェック

- 2カラム以上のグリッドは `grid-template-columns: 1fr` に畳む
- 比較ボックス(`.compare`)は1列に
- カードのパディングを縮小
- フォントを 1段階小さく
- ワイド SVG は `.viz-svg-wrap` で横スクロール
- bottombar の高さ + iPhone セーフエリアぶんを `padding-bottom` で確保

---

## 11. 標準作業フロー

```
[1] 素材の確認
    └ _source/ベストフィット問題/ から該当 docx を unzip
    └ python-docx か直接 XML パースでテキスト抽出
    └ _source/ベストフィット解答/ の対応する問題範囲を特定

[2] 構成案の提示と合意
    └ ユーザーに問題タイプ・例題/練習の振り分けを確認
    └ 合意前にコード書き始めない

[3] 実装
    └ examples/01-03-intellectual-property.html を articles/{番号}-{slug}/index.html にコピー
    └ 各ステージの中身(問題文・選択肢・解答・解説・viz)を差し替え
    └ TIMELINE_ENTRIES を新しい問題群に合わせて更新
    └ Welcome のメタ情報(章番号・所要時間・問題数)を更新
    └ Summary の PROBLEMS 配列も更新

[4] 答えの照合(原本との突き合わせ)
    └ 全問の正答・選択肢・解説の根拠フレームを原本 docx と1問ずつ照合
    └ 「ベストフィット問題 X〜Y / 解答 docx と全問照合済み」をユーザーへ報告

[5] 解説補完 + ビジュアル付与
    └ 原本に解説がない小問にも独自に補強
    └ 全例題・全練習問題に viz を添える

[6] 構文チェック
    └ HTML 入れ子(特に digest-mod の兄弟関係)
    └ JS 中括弧・括弧バランス
    └ 4ブレイクポイントで崩れない
    └ §9 の落とし穴をすべてチェック

[7] ユーザーへの報告
    └ 変更サマリ + 気になりそうな点を先回り

[8] 凍結
    └ examples/{番号}-{slug}.html にコピー
    └ practices/index.html の単元一覧に追加
    └ git commit -m "practices: ..." でコミット
```

---

## 12. 表現の禁止リスト

- 「やってみよう」「頑張ろう」「サクッと」「みんなで考えてみよう」
- 「素晴らしい!」「完璧!」「お見事!」「いいね!」(過剰な褒め)
- 「東大受験生向け」「難関大志望者へ」(対象特定)
- 「深掘り」「立体化」「紐解く」「学びのハブ」「別のかたちで」(AI頻出メタファー)
- ❤️🎉🚀(装飾絵文字。✓ ○ × ⊕ ⟲ など機能記号は可)
- 「全論点をカバーしました」のような自画自賛

---

## 13. 参照ファイル

| ファイル | 内容 |
|---|---|
| `components.md` | コピペ可能な部品カタログ(stage, 入力UI, viz, Q&A モジュール, フィードバック) |
| `examples/01-03-intellectual-property.html` | 動いている完成リファレンス(コピーしてそこから編集) |

新規単元を作るときは必ず examples の最新完成品をコピーしてから内容を差し替えること。ゼロから書こうとしない。
