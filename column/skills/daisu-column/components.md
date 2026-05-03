# components.md — daisu-column 部品カタログ(コピペ可能な完成版)

> 本ファイルは daisu-column スキルで使う HTML/CSS 部品の **コピペ可能な完成版** です。新しい記事を書くときは、本ファイルから必要な部品を抜き出して `articles/{slug}/index.html` に貼り付けます。
>
> 凍結リファレンス [`examples/dimension-and-equations.html`](examples/dimension-and-equations.html) と完全に同じ仕様で書かれています。
>
> **共通部品**(ヒーロー、目次、サイドレール、モバイルドロワー、フッター、参考文献): [`../visual-column/components.md`](../visual-column/components.md) を流用します。本ファイルは**数学コラム特有の部品**だけを扱います。

---

## 1. KaTeX の `<head>` 組み込み(必須)

```html
<!-- KaTeX (math typesetting) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
  onload="renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '\\[', right: '\\]', display: true},
      {left: '$',  right: '$',  display: false},
      {left: '\\(', right: '\\)', display: false}
    ],
    throwOnError: false,
    ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option', 'svg']
  });"></script>
```

> **重要**: `ignoredTags` に必ず `'svg'` を含めること。SVG 内に誤って `\(...\)` や `$...$` が残っても、KaTeX が処理せず文字化けを防ぐ。

---

## 2. 数学コラム CSS フルセット

`<style>` タグ内に以下を追加(visual-column の CSS の後ろに):

```css
/* ============ Math content blocks ============ */
.math-display {
  margin: 2rem 0;
  text-align: center;
  font-size: 1.05rem;
  overflow-x: auto;
}
.math-numbered {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2.25rem 0;
}
.math-numbered .math-display { margin: 0; flex: 1; text-align: center; }
.math-numbered .math-num {
  font-family: 'Fraunces', Georgia, serif;
  font-style: italic;
  color: var(--accent-secondary-deep);
  font-size: 0.95rem;
  white-space: nowrap;
}

/* Definition / Theorem / Example boxes */
.def-box, .thm-box, .ex-box {
  margin: 2.5rem 0;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-left: 5px solid var(--accent-primary);
  border-radius: 0 4px 4px 0;
  padding: 1.5rem 1.8rem;
}
.def-box header, .thm-box header, .ex-box header {
  font-family: var(--f-la-body);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--accent-secondary-deep);
  margin-bottom: 0.85rem;
  padding-bottom: 0.55rem;
  border-bottom: 1px solid var(--line-soft);
}
.thm-box { border-left-color: var(--accent-secondary); }
.ex-box  { border-left-color: var(--accent-primary-bright); }
.def-box p, .thm-box p, .ex-box p {
  font-size: 1rem; line-height: 2;
  margin-bottom: 0.85rem; color: var(--ink);
}
.def-box p:last-child, .thm-box p:last-child, .ex-box p:last-child { margin-bottom: 0; }
.ex-box .ex-source {
  font-family: var(--f-la-body);
  font-size: 0.78rem;
  color: var(--mute);
  margin-top: 0.5rem;
  letter-spacing: 0.04em;
}

/* "When/How" two-column hint */
.when-how {
  margin: 2.5rem 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.when-how > div {
  padding: 1.4rem 1.6rem;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 4px;
}
.when-how .wh-label {
  font-family: var(--f-la-body);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  color: var(--accent-secondary-deep);
  margin-bottom: 0.65rem;
  padding-bottom: 0.45rem;
  border-bottom: 1px solid var(--line-soft);
}
.when-how .wh-body {
  font-family: var(--f-jp-display);
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.04em;
  color: var(--ink);
  line-height: 1.85;
}
@media (max-width: 600px) { .when-how { grid-template-columns: 1fr; } }

/* "iff" decomposition (necessary/sufficient pairs) */
.iff-decomp {
  margin: 2.5rem 0;
  padding: 1.6rem 1.8rem;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 4px;
}
.iff-head {
  font-family: var(--f-jp-display);
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--ink);
  letter-spacing: 0.04em;
  margin-bottom: 0.5rem;
  text-align: center;
}
.iff-eq {
  text-align: center;
  font-family: var(--f-la-display);
  font-size: 1.4rem;
  font-style: italic;
  color: var(--accent-secondary-deep);
  margin: 0.5rem 0;
}
.iff-list { list-style: none; padding-left: 0; margin: 0; }
.iff-list li {
  padding: 0.5rem 0 0.5rem 2.4rem;
  position: relative;
  font-size: 1rem;
  line-height: 1.85;
  color: var(--ink);
}
.iff-list li::before {
  content: '①';
  position: absolute;
  left: 0;
  font-family: var(--f-la-display);
  font-weight: 700;
  color: var(--accent-secondary-deep);
}
.iff-list li:nth-child(2)::before { content: '②'; }
.iff-list li:nth-child(3)::before { content: '③'; }

/* Meta-note (small annotation, used for "厳密にはこの条件が必要" etc.) */
.ch-body .meta-note {
  font-size: 0.88rem;
  color: var(--mute);
  border-left: 2px solid var(--line);
  padding: 0.4rem 1rem;
  margin: 1.5rem 0;
  line-height: 1.85;
  font-style: normal;
}

/* ============ FIGURE: legend layout (most-used pattern) ============ */
.dgm-content {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: 1.4rem;
  align-items: stretch;
  margin: 1.25rem 0 0.5rem;
}
.dgm-figure {
  background: var(--bg);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 1rem 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.dgm-figure svg { display: block; width: 100%; height: auto; }
.dgm-legend {
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 1.4rem 1.5rem;
}
.dgm-legend-title {
  font-family: var(--f-jp-display);
  font-weight: 700;
  font-size: 1rem;
  color: var(--ink);
  margin-bottom: 1rem;
  padding-bottom: 0.7rem;
  border-bottom: 1px solid var(--line-soft);
  letter-spacing: 0.06em;
}
.legend-list { list-style: none; margin: 0; padding: 0; }
.legend-item {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 0.75rem;
  margin-bottom: 0.95rem;
  font-size: 0.96rem;
  line-height: 1.7;
  color: var(--ink);
  align-items: baseline;
}
.legend-item:last-child { margin-bottom: 0; }
.legend-key {
  font-family: var(--f-jp-display);
  font-weight: 700;
  color: var(--ink);
  margin-right: 0.35em;
}
.legend-foot {
  margin-top: 1rem;
  padding-top: 0.85rem;
  border-top: 1px solid var(--line-soft);
  font-size: 0.96rem;
  color: var(--ink);
  font-weight: 700;
  text-align: center;
  font-family: var(--f-jp-display);
}
.legend-foot.eq {
  background: var(--accent-primary-wash);
  border: 1px solid var(--accent-primary-pale);
  border-radius: 4px;
  padding: 0.85rem 1rem;
  margin-top: 1rem;
}
@media (max-width: 760px) { .dgm-content { grid-template-columns: 1fr; } }

/* Symbol-key legend item: 図中の記号 → 説明 */
.legend-item.sym {
  grid-template-columns: minmax(58px, auto) 1fr;
  gap: 0.85rem;
}
.legend-sym {
  font-family: 'KaTeX_Math', 'Latin Modern Math', 'Cambria Math', Georgia, serif;
  font-style: italic;
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--accent-secondary-deep);
  text-align: center;
  padding: 0.15rem 0.55rem;
  background: var(--accent-secondary-wash);
  border-radius: 3px;
  min-width: 28px;
  display: inline-block;
}
.legend-sym.alt  { color: var(--accent-primary-deep); background: var(--accent-primary-wash); }
.legend-sym.ink  { color: var(--ink); background: var(--bg-tint); }
.legend-sym.warn { color: var(--warn); background: #fde0d0; }
.legend-sym.jp { font-family: 'Zen Kaku Gothic New', sans-serif; font-style: normal; }

/* ============ FIGURE: stack layout (multiple frames) ============ */
.dgm-stack {
  display: grid;
  gap: 0.85rem;
  margin: 1.25rem 0;
}
.dgm-stack-row {
  display: grid;
  grid-template-columns: minmax(0, 220px) 1fr;
  gap: 1.25rem;
  align-items: center;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 0.85rem 1.1rem;
}
.dgm-stack-fig {
  background: var(--bg);
  border-radius: 3px;
  padding: 0.4rem;
}
.dgm-stack-fig svg { display: block; width: 100%; height: auto; }
.dgm-stack-text { display: flex; flex-direction: column; gap: 0.35rem; }
.dgm-stack-tag {
  font-family: var(--f-la-body);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--accent-secondary-deep);
}
.dgm-stack-cond {
  font-family: var(--f-jp-display);
  font-weight: 700;
  font-size: 1.08rem;
  color: var(--ink);
}
.dgm-stack-desc {
  font-size: 0.9rem;
  color: var(--mute);
  line-height: 1.6;
}
@media (max-width: 600px) { .dgm-stack-row { grid-template-columns: 1fr; } }

/* ============ FIGURE: vertical timeline (pure HTML) ============ */
.tl-list {
  list-style: none;
  position: relative;
  padding-left: 2.4rem;
  margin: 1.5rem 0 0;
}
.tl-list::before {
  content: '';
  position: absolute;
  left: 0.65rem;
  top: 0.3rem; bottom: 0.3rem;
  width: 2px;
  background: linear-gradient(to bottom, var(--accent-primary-pale) 0, var(--accent-secondary-pale) 100%);
  border-radius: 1px;
}
.tl-item {
  position: relative;
  padding: 0.95rem 1.2rem;
  margin-bottom: 0.85rem;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent-primary);
  border-radius: 0 4px 4px 0;
}
.tl-item:last-child { margin-bottom: 0; }
.tl-item::before {
  content: '';
  position: absolute;
  left: -2.05rem;
  top: 50%;
  transform: translateY(-50%);
  width: 14px; height: 14px;
  border-radius: 50%;
  background: var(--accent-primary);
  border: 2.5px solid var(--bg-card);
  box-shadow: 0 0 0 1px var(--accent-primary);
}
.tl-item.cyan { border-left-color: var(--accent-secondary); }
.tl-item.cyan::before { background: var(--accent-secondary); box-shadow: 0 0 0 1px var(--accent-secondary); }
.tl-item.bright { border-left-color: var(--accent-secondary-bright); }
.tl-item.bright::before { background: var(--accent-secondary-bright); box-shadow: 0 0 0 1px var(--accent-secondary-bright); }
.tl-item.indigo-bright { border-left-color: var(--accent-primary-bright); }
.tl-item.indigo-bright::before { background: var(--accent-primary-bright); box-shadow: 0 0 0 1px var(--accent-primary-bright); }
.tl-item.ink { border-left-color: var(--ink); }
.tl-item.ink::before { background: var(--ink); box-shadow: 0 0 0 1px var(--ink); }
.tl-head { display: flex; align-items: baseline; gap: 0.85rem; flex-wrap: wrap; margin-bottom: 0.35rem; }
.tl-year {
  font-family: var(--f-la-display);
  font-style: italic;
  font-weight: 700;
  font-size: 1.15rem;
  color: var(--accent-secondary-deep);
  flex-shrink: 0;
}
.tl-name {
  font-family: var(--f-jp-display);
  font-weight: 700;
  font-size: 1.08rem;
  color: var(--ink);
  letter-spacing: 0.04em;
}
.tl-desc { font-size: 0.95rem; line-height: 1.7; color: var(--text); }
.tl-foot {
  margin-top: 1.5rem;
  padding: 1rem 1.25rem;
  background: var(--bg-soft);
  border-radius: 4px;
  text-align: center;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--ink);
}

/* ============ In-figure SVG label classes ============ */
.svg-label  { font-family: 'Zen Kaku Gothic New', sans-serif; font-weight: 700; font-size: 18px; fill: #0b1424; }
.svg-sub    { font-family: 'Zen Kaku Gothic New', sans-serif; font-weight: 500; font-size: 15px; fill: #2e3f5e; }
.svg-en     { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-size: 14px; fill: #2e3f5e; }

.fig-axis {
  font-family: 'Fraunces', Georgia, serif;
  font-style: italic;
  font-size: 14px;
  fill: #2e3f5e;
}
.fig-lbl {
  font-family: 'KaTeX_Math', 'Latin Modern Math', 'Cambria Math', Georgia, serif;
  font-style: italic;
  font-weight: 700;
  font-size: 16px;
  fill: #0b1424;
}
.fig-lbl.bold   { font-weight: 800; }
.fig-lbl.cyan   { fill: #065563; }
.fig-lbl.indigo { fill: #0f1f4d; }
.fig-lbl.warn   { fill: #7a2810; }
.fig-lbl-jp {
  font-family: 'Zen Kaku Gothic New', sans-serif;
  font-weight: 700;
  font-size: 13px;
  fill: #0f1f4d;
}
```

---

## 3. 図方式 A — 凡例方式(`.dgm-content`)

**HTML テンプレ**(SVG は図形のみ、ラベルは記号、凡例で説明):

```html
<div class="dgm">
  <div class="dgm-head">
    <div class="dgm-kicker">Diagram NN</div>
    <div class="dgm-title">図のタイトル</div>
  </div>
  <div class="dgm-content">
    <div class="dgm-figure">
      <svg viewBox="0 0 380 220" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#2746a8"/>
          </marker>
        </defs>
        <!-- 図形のみ。点・線・矢印・ポリゴンを書く -->
        <line x1="20" y1="180" x2="350" y2="50" stroke="#2746a8" stroke-width="2.5"/>
        <circle cx="155" cy="125" r="4.5" fill="#065563"/>
        <line x1="155" y1="125" x2="220" y2="80" stroke="#0f1f4d" stroke-width="2" marker-end="url(#arrow1)"/>
        <!-- 短い記号ラベル(英字 italic serif)。複雑な数式は SVG 内に書かない -->
        <text x="226" y="78" class="fig-lbl indigo">n</text>
        <text x="118" y="148" class="fig-lbl cyan">P</text>
        <text x="362" y="138" class="fig-axis">x</text>
        <text x="84" y="14" class="fig-axis">y</text>
      </svg>
    </div>
    <div class="dgm-legend">
      <div class="dgm-legend-title">図の凡例</div>
      <ul class="legend-list">
        <li class="legend-item sym"><span class="legend-sym ink">P</span><span><span class="legend-key">点</span>\((x_0, y_0)\)</span></li>
        <li class="legend-item sym"><span class="legend-sym alt">n</span><span><span class="legend-key">法線ベクトル</span>\(\vec{n} = (a, b)\) は直線に直交</span></li>
      </ul>
      <div class="legend-foot eq">\(ax + by = c\)</div>
    </div>
  </div>
  <div class="dgm-caption">
    本文での詳細な解説を 1〜2 文で。
  </div>
</div>
```

**バリアント**:
- `.legend-sym` のクラス: 既定(secondary 色) / `.alt`(primary 色) / `.ink`(墨色) / `.warn`(警告色) / `.jp`(日本語)
- `.legend-foot` を `.legend-foot.eq` にすると主要式を強調枠で囲む

**1 つの dgm に複数の `.dgm-content` を入れることも可能**(例: 2D と 3D を別パネルで並べる)。各 `.dgm-content` の間に `style="margin-top:0.85rem;"` を入れる。

---

## 4. 図方式 B — stack 方式(`.dgm-stack`)

**HTML テンプレ**(複数フレームを縦積み、各 row に小 SVG + 短いテキスト):

```html
<div class="dgm">
  <div class="dgm-head">
    <div class="dgm-kicker">Diagram NN</div>
    <div class="dgm-title">パラメータの個数と、図形の次元</div>
  </div>
  <div class="dgm-stack">
    <div class="dgm-stack-row">
      <div class="dgm-stack-fig">
        <svg viewBox="0 0 200 170" xmlns="http://www.w3.org/2000/svg">
          <!-- 小さな図(SVG) -->
        </svg>
      </div>
      <div class="dgm-stack-text">
        <span class="dgm-stack-tag" style="color:#065563;">DIM 2 — 2 次元の領域</span>
        <span class="dgm-stack-cond">\(s, t \ge 0,\ s + t \le 1\)</span>
        <span class="dgm-stack-desc">三角形 OAB の内部</span>
      </div>
    </div>
    <!-- 続けて何 row でも -->
  </div>
  <div class="dgm-caption">
    本文での解説。
  </div>
</div>
```

---

## 5. 図方式 C — 縦タイムライン(`.tl-list`、純 HTML)

```html
<div class="dgm">
  <div class="dgm-head">
    <div class="dgm-kicker">Diagram NN</div>
    <div class="dgm-title">時系列タイトル</div>
  </div>
  <ol class="tl-list">
    <li class="tl-item cyan">
      <div class="tl-head"><time class="tl-year">1877</time><span class="tl-name">Cantor</span></div>
      <div class="tl-desc">区間 \([0, 1]\) と正方形 \([0, 1]^2\) の間に全単射 — 線分と正方形は同じ濃度を持つ。</div>
    </li>
    <li class="tl-item bright">
      <div class="tl-head"><time class="tl-year">1890</time><span class="tl-name">Peano</span></div>
      <div class="tl-desc">空間充填曲線。1 次元の連続曲線で 2 次元の正方形を埋め尽くせる。</div>
    </li>
    <!-- ... -->
  </ol>
  <div class="tl-foot">
    全体を貫くテーマを 1〜2 文で。
  </div>
</div>
```

**色クラス**: `.cyan` / `.bright` / `.indigo-bright` / `.ink`(無指定は accent-primary)

---

## 6. 番号付きディスプレイ式

```html
<div class="math-numbered">
  <div class="math-display">$$\vec{\mathrm{OP}} = s\,\vec{\mathrm{OA}} + t\,\vec{\mathrm{OB}}$$</div>
  <div class="math-num">(★)</div>
</div>
```

---

## 7. 定義 / 定理 / 例題ボックス

```html
<aside class="def-box">
  <header>定義</header>
  <p>...</p>
</aside>

<aside class="thm-box">
  <header>定理</header>
  <p>...</p>
</aside>

<div class="ex-box">
  <header>例題</header>
  <p>問題文</p>
  <div class="ex-source">出典: 大学名 年度 文系数学 第 N 問</div>
</div>
```

---

## 8. 「いつ / どのように」二項提示

```html
<div class="when-how">
  <div>
    <div class="wh-label">いつ</div>
    <div class="wh-body">和を積で評価したいとき</div>
  </div>
  <div>
    <div class="wh-label">どのように</div>
    <div class="wh-body">積が一定になるよう変形して使う</div>
  </div>
</div>
```

---

## 9. 必要十分の二点分解(`iff-decomp`)

```html
<div class="iff-decomp">
  <div class="iff-head">滑らかな図形 \(X\) が \(n\) 次元であるとは</div>
  <div class="iff-eq">⇔</div>
  <ul class="iff-list">
    <li>任意の点 \(p \in X\) の十分小さな近傍が、\(n\) 次元の開球と滑らかに対応している</li>
    <li>そのような近傍たちが、\(X\) 全体で整合的に貼り合わさっている</li>
  </ul>
</div>
```

---

## 10. メタ脇注(`<p class="meta-note">`)

数学的に厳密化が必要だが、本文に踏み込むとテンポが乱れる事項を、薄いボックスで補足:

```html
<p class="meta-note">これは大学初年次で習う <strong>多様体</strong> の素朴な定義そのものです。一般の集合に対する次元論(ハウスドルフ次元、被覆次元など)はこれとは別の流儀で、第 5 章の余韻で軽く触れます。</p>
```

---

## 11. ベクトル図の幾何学的注意(SVG コーディング時の必須計算)

**法線ベクトル**(直線・面に直交)を描くとき、必ず内積で確認:

```
直線: (x1, y1) → (x2, y2)
方向ベクトル: (x2-x1, y2-y1)
法線方向: (-(y2-y1), x2-x1) または (y2-y1, -(x2-x1))
内積で 0 を確認: 方向 · 法線 = 0
```

**例**: 直線 (20, 180) → (350, 50)
- 方向 = (330, -130)
- 法線(左上向き) = (-130, -330) を正規化して長さ 50 に → 約 (-19, -48)
- 中点 (185, 115) から (185-19, 115-48) = (166, 67) へ矢印

```html
<line x1="185" y1="115" x2="166" y2="67" stroke="#0f1f4d" stroke-width="2" marker-end="url(#arrow1)"/>
<text x="170" y="56" class="fig-lbl indigo">n</text>
```

---

## 11-bis. 3D 平面交差図のテンプレ(オブリーク投影)

「$3$ 次元空間で式の本数だけ図形の次元が落ちる」を視覚化するときの標準テンプレ。Diagram 04(stack 方式)で確立。

### 投影の定数

```
原点: (cx, cy) = (60, 150)
単位: 32px
z 方向のずれ: (-12.8, -12.8) per unit
投影式:
  screen_x = 60 + 32*x - 12.8*z
  screen_y = 150 - 32*y - 12.8*z
viewBox: "0 0 200 180"  (.dgm-stack-fig 220px に収まる)
軸長: 3.75 単位
平面: x = 1.5, y = 1.5, z = 1.5(中央で交わるよう統一)
```

### 主要座標(算出済み)

| 物体 | corners (screen) |
|---|---|
| 軸 X 終点 | (180, 150) |
| 軸 Y 終点 | (60, 30) |
| 軸 Z 終点 | (12, 102) |
| $\pi_1$ (y=1.5) | (60,102) (156,102) (118,64) (22,64) |
| $\pi_2$ (x=1.5) | (108,150) (108,54) (70,16) (70,112) |
| $\pi_3$ (z=1.5) | (41,131) (137,131) (137,35) (41,35) |
| $\pi_1 \cap \pi_2$ 交線 | (108,102) → (70,64) |
| $\pi_1 \cap \pi_3$ 交線 | (41,83) → (137,83) |
| $\pi_2 \cap \pi_3$ 交線 | (89,131) → (89,35) |
| 三平面交点 | (89, 83) |

### 行 1(平面 1 枚)

```html
<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3次元空間内の1平面">
  <defs>
    <marker id="ax04a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M0 0 L10 5 L0 10 z" fill="#94a3b8"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="200" height="180" fill="#ffffff" stroke="#d6e0ee" stroke-width="1.2"/>
  <g stroke="#94a3b8" stroke-width="1" fill="none">
    <line x1="60" y1="150" x2="180" y2="150" marker-end="url(#ax04a)"/>
    <line x1="60" y1="150" x2="60" y2="30" marker-end="url(#ax04a)"/>
    <line x1="60" y1="150" x2="12" y2="102" marker-end="url(#ax04a)"/>
  </g>
  <g font-family="'Fraunces', Georgia, serif" font-size="13" font-style="italic" fill="#64748b">
    <text x="184" y="154">X</text>
    <text x="52" y="26">Y</text>
    <text x="2" y="100">Z</text>
  </g>
  <path d="M 60 102 L 156 102 L 118 64 L 22 64 Z" fill="#6366f1" fill-opacity="0.22" stroke="#4338ca" stroke-width="1.5"/>
</svg>
```

### 行 2(2 平面 → 交線)

行 1 の中身に以下を追加(プレートの直後)し、軸グループの marker id を `ax04b` にする:

```html
<path d="M 108 150 L 108 54 L 70 16 L 70 112 Z" fill="#06b6d4" fill-opacity="0.20" stroke="#0891a8" stroke-width="1.3"/>
<line x1="108" y1="102" x2="70" y2="64" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
```

行 1 の $\pi_1$ の `fill-opacity` も 0.20、stroke-width 1.3 に揃える(2 枚以上ある場合は弱めに)。

### 行 3(3 平面 → 交点)

行 2 の構造に、$\pi_3$、3 つの対偶交線(ダッシュ薄色)、交点(濃色 dot)を追加。各 fill-opacity は 0.18 に下げる:

```html
<path d="M 41 131 L 137 131 L 137 35 L 41 35 Z" fill="#14b8a6" fill-opacity="0.18" stroke="#0d9488" stroke-width="1.2"/>
<g stroke="#475569" stroke-width="1.4" stroke-dasharray="3 2" opacity="0.7" fill="none">
  <line x1="108" y1="102" x2="70" y2="64"/>
  <line x1="41" y1="83" x2="137" y2="83"/>
  <line x1="89" y1="131" x2="89" y2="35"/>
</g>
<circle cx="89" cy="83" r="6" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
```

### 投影を変えるとき

平面の傾きや位置を変えたい場合は、投影式に新しい (x, y, z) を入れて screen 座標を計算してから path を組み立てる。**目視で「だいたいこんなもん」で書かない** — 内積計算と同じく、必ず数値で出す(SKILL.md §6-10 の方針を 3D に拡張)。

---

## 12. 配色テーマ(Indigo × Cyan の例)

```css
:root {
  --bg: #f7fafd;
  --bg-card: #ffffff;
  --bg-soft: #eff4fb;
  --bg-tint: #e0ecf9;
  --bg-deep: #0a2540;
  --bg-wash: #dce8f6;

  --accent-primary-deep:  #0f1f4d;
  --accent-primary:       #2746a8;
  --accent-primary-bright:#3b6ee0;
  --accent-primary-light: #7c95d6;
  --accent-primary-pale:  #d6e1f7;
  --accent-primary-wash:  #ecf1fb;

  --accent-secondary-deep:  #065563;
  --accent-secondary:       #0891a8;
  --accent-secondary-bright:#22b8cf;
  --accent-secondary-light: #6dd0dd;
  --accent-secondary-pale:  #c5ebf2;
  --accent-secondary-wash:  #e5f6fa;

  --ink: #0b1424;
  --text: #1a2541;
  --mute: #5b6a82;
  --mute-soft: #8594ae;
  --line: #d6e0ee;
  --line-soft: #e8edf5;
  --warn: #b54316;
  --gold: #f4b93a;
  --white: #ffffff;
}
```

他の数学テーマ用パレット候補(`templates/palettes.md` 参照):
- 確率・統計: Charcoal × Gold
- 解析・微積分: Forest × Coral
- 代数・整数論: Burgundy × Cream
