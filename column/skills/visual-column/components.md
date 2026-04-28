# components.md — Visual Column 部品カタログ

> 本ファイルは、Visual Column で繰り返し使う構造を、**コピー&ペースト可能な HTML/CSS** として整理したものです。記事を組み立てるときは、ここの部品を必要なだけ持っていって中身を入れ替えてください。
>
> CSS の正本は `templates/base.html` および本ドキュメント末尾の追補 (§11) にあります。

---

## 0. レイアウト基本骨格

すべての記事は次の上から順に構成します。

```
<body>
  <nav class="topnav">           — トップナビ(スクロールで隠れる)
  <section class="hero">         — タイトル+サブ+リード+scroll cue
  <section class="toc-section">  — 目次(必須・ヒーロー直後)
  <aside class="rail">           — デスクトップ固定サイドレール
  <section class="chapter" id="ch0"> — 0章(任意・プレリュード)
  <section class="chapter" id="ch1">
  ...
  <section class="chapter" id="chN">
  <section class="refs">         — 参考文献(必須)
  <footer class="footer">        — フッター
  <button class="m-menu-btn">    — モバイルメニュー
  <div class="m-drawer">         — モバイル目次ドロワー
  <script>...</script>           — ナビ追従JS
</body>
```

---

## 1. 目次セクション(`.toc-section`)

ヒーロー直後に置きます。章数によって `grid-template-columns` を 1〜3列に調整。

### 1-1. HTML

```html
<section class="toc-section" id="contents">
  <div class="toc-kicker">Contents · 目次</div>
  <h2 class="toc-title">六章で読む<span class="en">in six chapters</span></h2>
  <p class="toc-note">気になる章から読み始めても、最初から順に追ってもかまいません。</p>
  <ol class="toc-list">
    <li>
      <a href="#ch0" class="toc-card">
        <span class="toc-num">00</span>
        <span>
          <span class="toc-text-title">章タイトル</span>
          <span class="toc-text-sub">章サブタイトル</span>
        </span>
        <span class="toc-arrow">→</span>
      </a>
    </li>
    <!-- 他の章も同様に -->
  </ol>
</section>
```

### 1-2. 列数の指針

| 章数 | grid-template-columns | レイアウト |
|---|---|---|
| 3 | `1fr` | 1×3(縦) |
| 4 | `repeat(2, 1fr)` | 2×2 |
| 5 | `repeat(2, 1fr)` | 2×2 + 1(中央寄せ) |
| 6 | `repeat(2, 1fr)` | 2×3 |
| 7 | `repeat(2, 1fr)` | 2×3 + 1 |

スマホ幅では `@media (max-width: 760px)` で `1fr` に折り返し。

---

## 2. 図表(`.dgm`)— ポンチ図/SVG解説

専門概念を SVG で図解する標準コンポーネント。0章では3〜4枚、本論章では1〜2枚を目安に。

### 2-1. 共通HTML

```html
<div class="dgm">
  <div class="dgm-head">
    <div class="dgm-kicker">Diagram 01 / カテゴリ名</div>
    <div class="dgm-title">図のタイトル</div>
  </div>
  <div class="dgm-svg-wrap">
    <svg viewBox="0 0 880 360" preserveAspectRatio="xMidYMid meet" role="img" aria-label="図の説明">
      <!-- SVG中身 -->
    </svg>
  </div>
  <div class="dgm-caption">
    図の解釈を1〜3文で。<strong>要点</strong>は太字に。
  </div>
</div>
```

### 2-2. SVG用のテキストクラス

```svg
<text class="svg-label">主要ラベル(13px 太字)</text>
<text class="svg-sub">補助説明(11px ミュート色)</text>
<text class="svg-en">English subtitle (Fraunces italic 11px)</text>
```

### 2-3. パターン: 二パネル比較(viewBox 880×360)

中央集権 vs 分散など、左右に並べる対比図。

```svg
<svg viewBox="0 0 880 360" preserveAspectRatio="xMidYMid meet">
  <g transform="translate(40,20)">
    <!-- 左パネル(横幅 ~360px) -->
    <text x="180" y="18" text-anchor="middle" class="svg-label">左タイトル</text>
    <text x="180" y="34" text-anchor="middle" class="svg-en">left subtitle</text>
    <!-- 内容 -->
  </g>
  <g transform="translate(480,20)">
    <!-- 右パネル -->
    <text x="180" y="18" text-anchor="middle" class="svg-label">右タイトル</text>
    <text x="180" y="34" text-anchor="middle" class="svg-en">right subtitle</text>
    <!-- 内容 -->
  </g>
</svg>
```

### 2-4. パターン: 横長の連鎖図(viewBox 900×280)

ブロックチェーンの鎖、フロー図など、左から右へ流れる構造。

```svg
<svg viewBox="0 0 900 280" preserveAspectRatio="xMidYMid meet">
  <defs>
    <marker id="arrow1" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#2e343e"/>
    </marker>
  </defs>

  <!-- ブロック1 -->
  <g transform="translate(20,60)">
    <rect width="160" height="160" rx="3" class="svg-fill-card"/>
    <rect width="160" height="22" rx="3" fill="#2e343e"/>
    <text x="80" y="15" text-anchor="middle" fill="#fff"
          font-family="Fraunces, serif" font-style="italic"
          font-weight="700" font-size="11">BLOCK #001</text>
    <!-- 内容 -->
  </g>

  <!-- 矢印 -->
  <line x1="180" y1="140" x2="220" y2="140" stroke="#2e343e"
        stroke-width="1.5" marker-end="url(#arrow1)"/>

  <!-- ブロック2、3、…(transform で 220px 刻み) -->
</svg>
```

### 2-5. パターン: 価格チャート(viewBox 900×360)

折れ線 + ピーク注釈 + Y軸目盛 + 注釈点。

```svg
<svg viewBox="0 0 900 360" preserveAspectRatio="xMidYMid meet">
  <g transform="translate(40,30)">
    <text x="0" y="0" class="svg-label">価格曲線</text>
    <text x="0" y="18" class="svg-en">price chart, intraday</text>
    <g transform="translate(40,30)">
      <rect width="500" height="240" fill="#fff" stroke="#d6e0ee"/>
      <!-- Y軸ラベル: $5.00, $4.00, $3.00, $2.00, $1.00 -->
      <!-- 折れ線パス -->
      <path d="M0,228 L 30,224 ... L 500,236" fill="none"
            stroke="#b28a1c" stroke-width="2.2"/>
      <!-- ピークマーカー -->
      <circle cx="200" cy="28" r="4" fill="#b54316"/>
      <text x="208" y="22" font-family="Fraunces, serif"
            font-style="italic" font-weight="700" font-size="11"
            fill="#b54316">$4.50 peak</text>
    </g>
  </g>
</svg>
```

### 2-6. パターン: ドーナツ図(集中度・割合)

```svg
<g transform="translate(120,170)">
  <!-- 背景リング -->
  <circle r="70" fill="none" stroke="#ededef" stroke-width="22"/>
  <!-- セクション(stroke-dasharray で割合を表現) -->
  <!-- 全周 = 2π·70 ≈ 439.8。60% = 263.9、残り = 175.9 -->
  <circle r="70" fill="none" stroke="#b28a1c" stroke-width="22"
          stroke-dasharray="263.9 175.9" transform="rotate(-90)"/>
  <text x="0" y="-2" text-anchor="middle"
        font-family="Fraunces, serif" font-style="italic"
        font-weight="700" font-size="32" fill="#6b4f00">60%</text>
  <text x="0" y="20" text-anchor="middle" class="svg-sub">top 3 wallets</text>
</g>
```

---

## 3. 年表(`.timeline`)

時系列で並べる項目群。各行は「年 + 名前 + 詳細 + 統計バッジ」の4要素。

```html
<div class="timeline">
  <div class="tl-head">
    <div class="tl-kicker">Diagram 05 / 系譜</div>
    <div class="tl-title">十二年で、犬から首相へ</div>
  </div>
  <ul class="tl-list">
    <li class="tl-row">
      <div class="tl-year">2013<span class="tl-year-sub">December</span></div>
      <div>
        <div class="tl-name">名称 <span class="romaji">English</span></div>
        <div class="tl-detail">詳細を1〜3文で。固有名詞・年号・数字を温存する。</div>
        <span class="tl-stat">統計バッジ(高値・暴落率など)</span>
      </div>
    </li>
    <!-- 他の行 -->
  </ul>
</div>
```

---

## 4. 三層分類(`.tier`)

「合法/グレー/違法」「初級/中級/上級」など、3段階で分類するときの標準。色は緑/金/赤に固定。

```html
<div class="tier">
  <div class="tier-row legal">
    <div class="tier-head">
      <span class="tier-label">合法の領域</span>
      <span class="tier-en">Legal</span>
    </div>
    <div class="tier-body">
      ここで何が合法か。<strong>キーワード</strong>を太字に。
    </div>
  </div>
  <div class="tier-row gray">
    <div class="tier-head">
      <span class="tier-label">グレーの領域</span>
      <span class="tier-en">Gray</span>
    </div>
    <div class="tier-body">グレーの説明</div>
  </div>
  <div class="tier-row illegal">
    <div class="tier-head">
      <span class="tier-label">違法の領域</span>
      <span class="tier-en">Illegal</span>
    </div>
    <div class="tier-body">違法の説明</div>
  </div>
</div>
```

---

## 5. 二列比較(`.compare`)

二つのものを並べて見せるときの定番。中央に "vs" バッジが自動で入ります。

```html
<div class="compare">
  <div class="cmp-card primary">
    <div class="cmp-head">
      <div class="cmp-name">大陸法</div>
      <div class="cmp-label">Civil Law</div>
    </div>
    <div class="cmp-body">説明文をここに。</div>
    <div class="cmp-tag">明文化 <span class="arrow">→</span></div>
  </div>
  <div class="cmp-card secondary">
    <div class="cmp-head">
      <div class="cmp-name">英米法</div>
      <div class="cmp-label">Common Law</div>
    </div>
    <div class="cmp-body">説明文をここに。</div>
    <div class="cmp-tag">判例の積層 <span class="arrow">→</span></div>
  </div>
</div>
```

---

## 6. 統計カード列(`.stat-row`)

数字を3つ並べて目立たせるときに。

```html
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-num">$27M</div>
    <div class="stat-label">時価総額のピーク</div>
    <div class="stat-sub">2026年2月18日 +30min</div>
  </div>
  <div class="stat-card cyan">
    <div class="stat-num">−75%</div>
    <div class="stat-label">同日のうちの下落率</div>
    <div class="stat-sub">$4.50 → $0.20</div>
  </div>
  <div class="stat-card">
    <div class="stat-num">60%</div>
    <div class="stat-label">上位3アドレス保有率</div>
    <div class="stat-sub">on-chain analysis</div>
  </div>
</div>
```

---

## 7. 引用ブロック

### 7-1. 大きめの強調引用(`.pull-quote`)

```html
<div class="pull-quote">
  <p>引用したい一文を、ここに大きめの明朝で。</p>
  <div class="attribution">— 引用元の名前 / 出典</div>
</div>
```

### 7-2. 出典付きの直接引用(`blockquote.cite`)

```html
<blockquote class="cite" data-ref="2">
  引用本文をそのまま書きます。
  <footer>— 出典の名前(年月日)</footer>
</blockquote>
```

`data-ref="N"` の N は、参考文献リストの項番と一致させる。

---

## 8. デスクトップサイドレール(`.rail`)

```html
<aside class="rail" id="rail" aria-label="目次ナビゲーション">
  <ol class="rail-list">
    <li><a href="#ch0" class="rail-item" data-ch="0">
      <span class="rail-num">00</span>
      <span class="rail-title">章タイトル</span>
    </a></li>
    <!-- 他の章 -->
  </ol>
</aside>
```

CSS は `templates/base.html` 内の `/* SIDE RAIL */` セクション。表示は `@media (min-width: 1180px)` でのみ。

---

## 9. モバイルドロワー(`.m-drawer`)+ メニューボタン

```html
<button class="m-menu-btn" id="mMenuBtn" aria-label="目次を開く">
  <span></span><span></span><span></span>
</button>

<div class="m-drawer" id="mDrawer" role="dialog" aria-modal="true" aria-label="目次">
  <div class="m-drawer-panel">
    <div class="m-drawer-handle" aria-hidden="true"></div>
    <div class="m-drawer-head">
      <span class="m-drawer-title">目次<span class="en">contents</span></span>
      <button class="m-drawer-close" id="mDrawerClose" aria-label="閉じる">×</button>
    </div>
    <ol class="m-drawer-list">
      <li><a href="#ch0" data-ch="0">
        <span class="md-num">00</span>
        <span>
          <span class="md-title">章タイトル</span>
          <span class="md-sub">章サブタイトル</span>
        </span>
        <span class="md-arrow">→</span>
      </a></li>
      <!-- 他の章 -->
    </ol>
  </div>
</div>
```

ボタンは `@media (min-width: 1180px) { display: none; }` でデスクトップでは隠す。

---

## 10. ナビ追従用 JavaScript

サイドレール/ドロワーの `.active` 状態を IntersectionObserver で更新します。`<body>` の閉じタグ直前に配置。

```html
<script>
(function () {
  // ---- トップナビをスクロール下方向で隠す ----
  const nav = document.getElementById('topnav');
  let lastY = window.scrollY;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > 120 && y > lastY) nav.classList.add('hidden');
    else nav.classList.remove('hidden');
    lastY = y;
  }, { passive: true });

  // ---- 現在章の追従 ----
  const sections = document.querySelectorAll('section.chapter');
  const railItems = document.querySelectorAll('.rail-item');
  const drawerItems = document.querySelectorAll('.m-drawer-list a');

  const setActive = (id) => {
    railItems.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
    drawerItems.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
  };

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter(e => e.isIntersecting);
      if (visible.length === 0) return;
      visible.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      const top = visible[0];
      if (top.boundingClientRect.top < window.innerHeight * 0.55) {
        setActive(top.target.id);
      }
    }, { rootMargin: '-20% 0px -45% 0px', threshold: 0 });
    sections.forEach(s => observer.observe(s));
  }

  // ---- モバイルドロワー ----
  const btn = document.getElementById('mMenuBtn');
  const drawer = document.getElementById('mDrawer');
  const closeBtn = document.getElementById('mDrawerClose');

  const openDrawer = () => {
    drawer.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const closeDrawer = () => {
    drawer.classList.remove('open');
    document.body.style.overflow = '';
  };

  btn.addEventListener('click', openDrawer);
  closeBtn.addEventListener('click', closeDrawer);
  drawer.addEventListener('click', (e) => {
    if (e.target === drawer) closeDrawer();
  });
  drawerItems.forEach(a => a.addEventListener('click', () =>
    setTimeout(closeDrawer, 100)
  ));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
  });
})();
</script>
```

---

## 11. CSS 追補

`templates/base.html` に存在しない、本スキル固有のクラスは次のとおりです。base.html を更新せずに記事ごとに追加する場合は、各記事の `<style>` ブロックにコピーしてください。

> 凍結リファレンス [`examples/meme-coin-and-value.html`](examples/meme-coin-and-value.html) には、本ファイルで言及した全コンポーネントの CSS が完全な形で含まれています。新規記事で必要なクラスを抜き出すときの第一参照先にしてください。

主要な追加クラス:

- `/* TOC SECTION */` — `.toc-section`, `.toc-kicker`, `.toc-title`, `.toc-list`, `.toc-card`, `.toc-num`, `.toc-text-title`, `.toc-text-sub`, `.toc-arrow`
- `/* SIDE RAIL */` — `.rail`, `.rail-list`, `.rail-item`, `.rail-num`, `.rail-title`
- `/* MOBILE MENU + DRAWER */` — `.m-menu-btn`, `.m-drawer`, `.m-drawer-panel`, `.m-drawer-handle`, `.m-drawer-head`, `.m-drawer-title`, `.m-drawer-close`, `.m-drawer-list`, `.md-num`, `.md-title`, `.md-sub`, `.md-arrow`
- `/* DIAGRAMS */` — `.dgm`, `.dgm-head`, `.dgm-kicker`, `.dgm-title`, `.dgm-svg-wrap`, `.dgm-caption`, および SVG用 `.svg-label`, `.svg-sub`, `.svg-en`, `.svg-fill-card`, `.svg-fill-prim`, `.svg-fill-pale`, `.svg-stroke-dim`
- `/* TIMELINE */` — `.timeline`, `.tl-head`, `.tl-kicker`, `.tl-title`, `.tl-list`, `.tl-row`, `.tl-year`, `.tl-year-sub`, `.tl-name`, `.tl-detail`, `.tl-stat`
- `/* TIER */` — `.tier`, `.tier-row`, `.tier-row.legal`, `.tier-row.gray`, `.tier-row.illegal`, `.tier-head`, `.tier-label`, `.tier-en`, `.tier-body`

これらは `templates/base.html` の更新で追加済み(2026年4月以降の新規記事)。それ以前の記事は記事内インラインCSSで対応しています。
