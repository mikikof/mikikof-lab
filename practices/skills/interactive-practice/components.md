# components.md — 部品カタログ(コピペ用)

このファイルは新しい単元を作るときに、目的別の HTML をコピペするための辞書です。
各部品は `examples/01-01-information-and-media.html`(最新)および `examples/01-03-intellectual-property.html` から抽出したもので、CSS は SKILL.md 記載のクラスに依存しています。新規単元のコピー元は **01-01** を使う。

---

## 1. ステージのシェル

### 1.1 Welcome ステージ(Stage 0)

```html
<section class="stage active" data-stage-name="START">
  <div class="welcome-kicker">
    <span class="num">{{章番号}}</span>
    <span>{{章 第N節}}</span>
  </div>
  <h1 class="welcome-title-en">{{Title}}<br>{{Subtitle}}<span class="accent">.</span></h1>
  <h2 class="welcome-title-jp">{{単元の日本語タイトル}}</h2>
  <p class="welcome-lede">
    {{単元の概要 — 何を扱うかを2-3文で}}
  </p>
  <div class="welcome-meta">
    <div class="welcome-meta-item">
      <div class="welcome-meta-label">examples</div>
      <div class="welcome-meta-value">{{例題数}}<span class="unit">問</span></div>
    </div>
    <div class="welcome-meta-item">
      <div class="welcome-meta-label">practice</div>
      <div class="welcome-meta-value">{{練習問題数}}<span class="unit">問</span></div>
    </div>
    <div class="welcome-meta-item">
      <div class="welcome-meta-label">est. time</div>
      <div class="welcome-meta-value">{{所要分}}<span class="unit">分</span></div>
    </div>
    <div class="welcome-meta-item">
      <div class="welcome-meta-label">source</div>
      <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">{{章番号}}</span></div>
    </div>
  </div>
  <div class="flow-strip">
    <div class="flow-strip-title">本セットの流れ</div>
    <div class="flow-list">
      <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー Q&A 形式で単元の地図を確認(タップで展開)</div></div>
      <div class="flow-item"><span class="flow-num">2</span><div><strong>例題ツアー</strong>ー 模範解法を{{例題数}}問追跡(採点なし)</div></div>
      <div class="flow-item"><span class="flow-num">3</span><div><strong>演習</strong>ー {{練習問題数}}問に挑戦。回答 → 採点 → 解説</div></div>
      <div class="flow-item"><span class="flow-num">4</span><div><strong>結果</strong>ー 正答率と間違えた問題の再確認</div></div>
    </div>
  </div>
</section>
```

### 1.2 例題ステージ(reveal 型)

```html
<section class="stage" data-stage-name="例題 {{N}}" data-prob-id="ex{{N}}">
  <div class="problem-meta">
    <span class="problem-tag">EXAMPLE {{i}} / {{total}}</span>
    <span class="problem-source">ベストフィット 例題{{N}}</span>
  </div>
  <div class="problem-q-num"><span class="q">Q</span>{{N}}</div>
  <h3 class="problem-title">{{問題タイトル}}</h3>
  <div class="problem-card">
    <p class="problem-q lead">{{問題文}}</p>

    [入力UI(§2)]

    <div class="actions-inline">
      <button class="btn-reveal" data-action="reveal">解答を見る</button>
    </div>

    [フィードバックブロック(§4)]
  </div>
</section>
```

### 1.3 練習問題ステージ(grade 型)

```html
<section class="stage" data-stage-name="練習 {{N}}" data-prob-id="p{{N}}">
  <div class="problem-meta">
    <span class="problem-tag practice">PRACTICE {{i}} / {{total}}</span>
    <span class="problem-tag {{type-class}}">{{TYPE-LABEL}}</span>
    <span class="problem-source">ベストフィット {{原本問題番号}}</span>
  </div>
  <div class="problem-q-num"><span class="q">Q</span>{{N}}</div>
  <h3 class="problem-title">{{問題タイトル}}</h3>
  <div class="problem-card">
    <p class="problem-q lead">{{問題文}}</p>

    [入力UI(§2)]

    <div class="actions-inline">
      <button class="btn-grade" data-action="grade">採点する <span class="arrow">→</span></button>
    </div>

    [フィードバックブロック(§4)]
  </div>
</section>
```

`{{type-class}}` と `{{TYPE-LABEL}}` の組み合わせ:
- match → `match` / `MATCH`
- ox → `ox` / `○ × 判定`
- multi → `multi` / `MULTI`
- multi_per_sub → `multi` / `MULTI × {{N}}`
- fill → `fill` / `FILL`
- single → (無し or `single` / `SINGLE`)

### 1.4 サマリステージ(末尾)

```html
<section class="stage" data-stage-name="RESULT">
  <div class="section-divider">
    <span class="num">02</span>
    <div class="text">
      <div class="label">Section 2 — Result</div>
      <div class="name">演習結果</div>
    </div>
  </div>
  <div class="summary-hero">
    <div class="summary-grade" id="summary-grade">—<span class="denom">/{{練習問題数}}</span></div>
    <div class="summary-headline" id="summary-headline">演習結果</div>
    <div class="summary-subline" id="summary-subline">{{練習問題数}}問の練習問題のうち、何問完答できたか。</div>
    <div class="summary-stats">
      <div class="summary-stat">
        <div class="summary-stat-label">完答</div>
        <div class="summary-stat-value" id="stat-full">0<span class="unit">問</span></div>
      </div>
      <div class="summary-stat">
        <div class="summary-stat-label">部分正解</div>
        <div class="summary-stat-value" id="stat-partial">0<span class="unit">問</span></div>
      </div>
      <div class="summary-stat">
        <div class="summary-stat-label">未着手</div>
        <div class="summary-stat-value" id="stat-skipped">0<span class="unit">問</span></div>
      </div>
      <div class="summary-stat">
        <div class="summary-stat-label">小問正答率</div>
        <div class="summary-stat-value" id="stat-rate">—<span class="unit">%</span></div>
      </div>
    </div>
  </div>
  <div class="summary-list-title">問題別 — タップで該当ページへ</div>
  <div class="summary-list" id="summary-list"></div>
  <button class="btn-restart" id="btn-restart-bottom">最初からやり直す</button>
</section>
```

JS の `PROBLEMS` 配列と `TIMELINE_ENTRIES` 配列も新しい問題群に合わせて更新する必要がある(詳細は §6 参照)。

---

## 2. 入力 UI(6種)

### 2.1 single — 単一選択(ラジオ)

```html
<div class="opts" data-input="single" data-correct="{{正解index 0始まり}}">
  <label class="opt"><input type="radio" name="{{prob-id}}"><span class="opt-mark"></span><span class="opt-text"><span class="opt-letter">(ア)</span>{{選択肢1}}</span></label>
  <label class="opt"><input type="radio" name="{{prob-id}}"><span class="opt-mark"></span><span class="opt-text"><span class="opt-letter">(イ)</span>{{選択肢2}}</span></label>
  <label class="opt"><input type="radio" name="{{prob-id}}"><span class="opt-mark"></span><span class="opt-text"><span class="opt-letter">(ウ)</span>{{選択肢3}}</span></label>
  <label class="opt"><input type="radio" name="{{prob-id}}"><span class="opt-mark"></span><span class="opt-text"><span class="opt-letter">(エ)</span>{{選択肢4}}</span></label>
</div>
```

### 2.2 multi — 複数選択(チェックボックス)

```html
<div class="multi-hint">複数選択 — 該当するものすべて</div>
<div class="opts" data-input="multi" data-correct="{{正解indices カンマ区切り、例: 1,2,5}}">
  <label class="opt"><input type="checkbox"><span class="opt-mark checkbox"></span><span class="opt-text"><span class="opt-letter">(ア)</span>{{選択肢1}}</span></label>
  ...
</div>
```

### 2.3 match — マッチング(各小問に選択肢から1つ)

```html
<div class="option-legend">
  <div class="option-legend-title">選択肢</div>
  <div class="option-legend-list">
    <span class="option-legend-item"><span class="let">(ア)</span>{{凡例1}}</span>
    <span class="option-legend-item"><span class="let">(イ)</span>{{凡例2}}</span>
    <span class="option-legend-item"><span class="let">(ウ)</span>{{凡例3}}</span>
    <span class="option-legend-item"><span class="let">(エ)</span>{{凡例4}}</span>
  </div>
</div>
<div class="match-list" data-input="match" data-options="ア,イ,ウ,エ" data-correct="{{各小問の正解index、例: 3,0,1,2}}">
  <div class="match-row" data-sub="0">
    <span class="match-sub-label">⑴</span>
    <div class="sub-content">
      <span class="match-text">{{小問1の文章}}</span>
      <div class="match-pills"></div>  <!-- JSが自動で選択肢ピルを生成 -->
    </div>
  </div>
  <div class="match-row" data-sub="1">
    <span class="match-sub-label">⑵</span>
    <div class="sub-content">
      <span class="match-text">{{小問2の文章}}</span>
      <div class="match-pills"></div>
    </div>
  </div>
  ...
</div>
```

### 2.4 ox — ○×

```html
<div class="ox-list" data-input="ox" data-correct="{{各小問の正解、例: o,x,o,x,o}}">
  <div class="ox-row" data-sub="0">
    <span class="ox-sub-label">⑴</span>
    <span class="ox-text">{{小問1の文章}}</span>
    <div class="ox-buttons"><button class="ox-btn maru" data-val="o">○</button><button class="ox-btn batsu" data-val="x">×</button></div>
  </div>
  <div class="ox-row" data-sub="1">
    <span class="ox-sub-label">⑵</span>
    <span class="ox-text">{{小問2の文章}}</span>
    <div class="ox-buttons"><button class="ox-btn maru" data-val="o">○</button><button class="ox-btn batsu" data-val="x">×</button></div>
  </div>
  ...
</div>
```

### 2.5 fill — 語群穴埋め

```html
<div class="fill-bullets" data-input="fill">
  <div class="fill-line">{{文章前半}}<span class="fill-blank" data-blank="0"><span class="fill-blank-label">①</span></span>{{文章後半}}</div>
  <div class="fill-line">{{文章}}<span class="fill-blank" data-blank="1"><span class="fill-blank-label">②</span></span>{{...}}</div>
  ...
</div>
<div class="fill-bank">
  <div class="fill-bank-title">語群({{N}}語) — タップで空欄に入れる</div>
  <button class="fill-chip" data-word="{{語1}}">{{語1}}</button>
  <button class="fill-chip" data-word="{{語2}}">{{語2}}</button>
  ...
</div>
<div class="actions-inline">
  <button class="btn-grade" data-action="grade" data-fill-correct="{{各空欄の正解語をカンマ区切り、例: 公表,必然性,明確,主,従,必要,明示}}">採点する <span class="arrow">→</span></button>
</div>
```

### 2.6 multi_per_sub — 各小問に複数選択

```html
<div class="mps-list" data-input="multi_per_sub" data-options="ア,イ,ウ,エ" data-correct="{{小問ごとの正解、例: 0,1|0,2|0,1,3}}">
  <div class="mps-row" data-sub="0">
    <span class="match-sub-label">⑴</span>
    <div class="sub-content">
      <span class="mps-text">{{小問1の文章}}</span>
      <div class="match-pills"></div>
    </div>
  </div>
  <div class="mps-row" data-sub="1">
    <span class="match-sub-label">⑵</span>
    <div class="sub-content">
      <span class="mps-text">{{小問2の文章}}</span>
      <div class="match-pills"></div>
    </div>
  </div>
  ...
</div>
```

`data-correct` は `|`(パイプ)で小問区切り、各小問内の複数正解は `,` 区切り。

---

## 3. ビジュアル(viz)

すべて `.fb-body` 内に配置する。フィードバックの解説の直後に置く。

### 3.1 IP rich card grid(4種カード)

```html
<div class="viz">
  <span class="viz-label">{{ENG TITLE}} — {{日本語サブタイトル}}</span>
  <div class="viz-caption">{{1行のコンテキスト}}</div>
  <div class="ip-rich-grid">
    <div class="ip-rich patent">
      <div class="ip-rich-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          {{アイコンの SVG パス、例題9 の特許権アイコン参照}}
        </svg>
      </div>
      <div class="ip-rich-name">{{権利名}}</div>
      <div class="ip-rich-en">{{英名}}</div>
      <div class="ip-rich-period">{{期間ラベル}}</div>
      <div class="ip-rich-desc">{{保護対象の説明}}</div>
      <div class="ip-rich-ex"><span class="label">例</span>{{身近な実例 1〜2件}}</div>
    </div>
    <!-- utility / design / trademark も同様 -->
  </div>
</div>
```

色変種クラス: `.patent`(青) `.utility`(ティール) `.design`(アンバー) `.trademark`(ローズ) `.copyright`(ゴールド)

### 3.2 Right tree(階層図)

```html
<div class="viz">
  <span class="viz-label">{{LABEL}} — {{タイトル}}</span>
  <div class="viz-caption">{{サブ}}</div>
  <div class="right-tree">
    <div class="rt-row heading"><span class="rt-bracket">┃</span><span class="rt-name">{{ルート}}</span><span class="rt-note">{{注釈}}</span></div>
    <div class="rt-row indent"><span class="rt-bracket">├</span><span class="rt-name">{{第1階層 1}} <span class="pill dim">{{タグ}}</span></span><span class="rt-note">{{説明}}</span></div>
    <div class="rt-row indent2"><span class="rt-bracket">├</span><span class="rt-name small">{{第2階層 1}} <span class="pill">⑴</span></span><span class="rt-note">{{説明}}</span></div>
    <div class="rt-row indent2"><span class="rt-bracket">└</span><span class="rt-name small">{{第2階層 N}}</span><span class="rt-note">{{説明}}</span></div>
    <div class="rt-row indent"><span class="rt-bracket">└</span><span class="rt-name">{{第1階層 2}}</span><span class="rt-note">{{説明}}</span></div>
  </div>
</div>
```

`.rt-row.indent` / `.indent2` / `.indent3` で階層を表現。
`<span class="pill">⑴</span>` でその行に対応する小問番号を表示。

### 3.3 Compare 2-col(二項対比)

```html
<div class="viz">
  <span class="viz-label">{{LABEL}}</span>
  <div class="viz-caption">{{タイトル}}</div>
  <div class="compare">
    <div class="compare-col left">
      <h5>{{左の見出し}}</h5>
      <div class="row"><span class="k">{{ラベル1}}</span><span class="v">{{値1}}</span></div>
      <div class="row"><span class="k">{{ラベル2}}</span><span class="v">{{値2}}</span></div>
    </div>
    <div class="compare-col right">
      <h5>{{右の見出し}}</h5>
      <div class="row"><span class="k">{{ラベル1}}</span><span class="v">{{値1}}</span></div>
      <div class="row"><span class="k">{{ラベル2}}</span><span class="v">{{値2}}</span></div>
    </div>
  </div>
</div>
```

### 3.4 Lock vs Key(譲渡可否対比)

```html
<div class="viz">
  <span class="viz-label">{{LABEL}}</span>
  <div class="viz-caption">{{タイトル}}</div>
  <div class="lk-grid">
    <div class="lk-card locked">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </div>
      <h5>{{譲渡不可な権利の名}}</h5>
      <span class="stamp">譲渡 ×</span>
      <ul class="lk-list">
        <li><span>{{要素1}}</span></li>
        <li><span>{{要素2}}</span></li>
      </ul>
      <p class="lk-rules"><strong>本人だけ</strong>に帰属。{{死後の扱い}}</p>
    </div>
    <div class="lk-card transferable">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="7.5" cy="14.5" r="3.5"/>
          <path d="m10 12 9-9 3 3-3 3 2 2-3 3-2-2-3 3"/>
        </svg>
      </div>
      <h5>{{譲渡可な権利の名}}</h5>
      <span class="stamp">譲渡・相続 ○</span>
      <ul class="lk-list">
        <li><span>{{要素1}}</span></li>
        <li><span>{{要素2}}</span></li>
      </ul>
      <p class="lk-rules">{{ルール説明}}</p>
    </div>
  </div>
</div>
```

### 3.5 Boundary cards(キーワード境界)

```html
<div class="viz">
  <span class="viz-label">{{LABEL}}</span>
  <div class="viz-caption">{{タイトル}}</div>
  <div class="bd-grid">
    <div class="bd-card">
      <div class="key">{{条件のキーワード1}}</div>
      <span class="bound">{{境界線の判定値}}</span>
      <div class="desc">{{何が中で何が外かの説明}}</div>
    </div>
    <!-- 残り3枚 -->
  </div>
  <div class="bd-warn">
    <strong>重要:</strong> {{付帯ルール・落とし穴}}
  </div>
</div>
```

### 3.6 Checklist(要件チェックリスト)

```html
<div class="viz">
  <span class="viz-label">{{LABEL}}</span>
  <div class="viz-caption">{{タイトル}}</div>
  <div class="checklist">
    <div class="cl-item"><span class="cl-num">①</span><span><span class="cl-key">{{要件キー}}</span>{{要件説明}}</span></div>
    <div class="cl-item"><span class="cl-num">②</span><span>{{...}}</span></div>
    <!-- 必要数まで繰り返し -->
  </div>
  <div style="margin-top: 0.85rem; padding: 0.7rem 0.95rem; background: var(--ng-pale); border-left: 3px solid var(--ng); border-radius: 0 6px 6px 0; font-size: 0.85rem; color: var(--ng-deep);">
    <strong>×&nbsp;{{違反時の説明}}</strong>
  </div>
</div>
```

### 3.7 CC marks grid(CCマーク組み合わせ)

```html
<div class="viz">
  <span class="viz-label">CC MARKS — 組み合わせビジュアル</span>
  <div class="viz-caption">塗りつぶされたマークがその条件を「適用」している</div>
  <div class="cc-grid">
    <div class="cc-row">
      <span class="lbl">⑴</span>
      <span class="desc">{{条件説明}}</span>
      <div class="cc-marks">
        <span class="cc-mark by active">BY</span>
        <span class="cc-mark nc active">NC</span>
        <span class="cc-mark nd">ND</span>
        <span class="cc-mark sa">SA</span>
      </div>
    </div>
    <!-- ⑵, ⑶ も同様。.active が付いているものが「適用中」 -->
  </div>
</div>
```

### 3.8 Origin compare flow(発生方式対比)

**2列対比**(デフォルト):

```html
<div class="origin-compare">
  <div class="origin-side industrial">
    <h5>{{左カテゴリ}}</h5>
    <div class="tag-en">{{英タグ}}</div>
    <div class="origin-flow">
      <span class="origin-step">{{ステップ1}}</span>
      <span class="origin-arrow">→</span>
      <span class="origin-step">{{ステップ2}}</span>
      <span class="origin-arrow">→</span>
      <span class="origin-step fill">{{最終ステップ}}</span>
    </div>
    <span class="origin-key">{{核心キーワード}}</span>
    <p class="note">{{解説}}</p>
  </div>
  <div class="origin-side copyright">
    <h5>{{右カテゴリ}}</h5>
    <div class="tag-en">{{英タグ}}</div>
    <div class="origin-flow">
      <span class="origin-step">{{ステップ1}}</span>
      <span class="origin-arrow">→</span>
      <span class="origin-step fill">{{最終}}</span>
    </div>
    <span class="origin-key">{{核心キーワード}}</span>
    <p class="note">{{解説}}</p>
  </div>
</div>
```

**3列対比**(`.three-col` 必須・inline style 禁止):

```html
<div class="origin-compare three-col">
  <div class="origin-side industrial">
    <h5>{{第1カテゴリ}}</h5>
    <div class="tag-en">{{英タグ}}</div>
    <div class="origin-flow">
      <span class="origin-step">{{ステップ1}}</span>
      <span class="origin-step">{{ステップ2}}</span>
    </div>
    <span class="origin-key">{{核心キーワード}}</span>
    <p class="note">{{解説}}</p>
  </div>
  <div class="origin-side industrial">
    <h5>{{第2カテゴリ}}</h5>
    ...
  </div>
  <div class="origin-side copyright">
    <h5>{{第3カテゴリ}}</h5>
    ...
  </div>
</div>
```

`.three-col` の挙動:
- **デスクトップ**: 3 列グリッド
- **モバイル(≤720px)**: 横スワイプ snap カルーセル(各カード 84vw)
- JS が自動で挿入: 上に「← 横にスワイプ →」hint、下に IntersectionObserver 連動のドットインジケーター
- `isInsideHorizontalScroll` ガード対象なので、page-swipe との干渉なし
- 詳細は `SKILL.md` §8.5.3

### 3.9 SVG protection timeline(ガントチャート)

`examples/01-03-intellectual-property.html` の例題9 セクションを参照。横スクロール対応:

```html
<div class="viz-svg-wrap">
  <svg class="viz-svg wide" viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg">
    <!-- Axis + bars + labels -->
  </svg>
</div>
```

### 3.10 SVG judgment flow(判定フロー)

`examples/01-03-intellectual-property.html` の Q19 セクションを参照。フローチャート + 矢印マーカー使用。

### 3.11 SVG family tree(おさらいの大地図)

`examples/01-01-information-and-media.html` または `examples/01-03-intellectual-property.html` の REVIEW(Module 01)を参照。Linear gradient + 階層的な分岐構造。横スクロール対応(`.family-tree-wrap` で wrap、`min-width: 720-760px`)。

### 3.12 スポットライト対応カード(SKILL.md §8.5.1)

以下のカードクラスは「タップで暗転 + 拡大 + ゴールドリング」のスポットライト対象。

| クラス | 用途 | 親グリッド |
|---|---|---|
| `.ip-rich` | 4 種マッチング・3 種特性などの主役カード | `.ip-rich-grid` |
| `.bd-card` | 境界線・ルール早見カード | `.bd-grid` |
| `.lk-card` | 譲渡可否などの 2 項対比カード | `.lk-grid` |
| `.cc-cat-item` | CC マークなどのカテゴリカード | `.cc-cat` |

新しいカードクラスを viz パターンとして追加する場合は、`SKILL.md` §8.5.1 の `SPOT_SELECTOR` と CSS の `.has-spotlight > .X:not(.spotlight)` / `.X.spotlight` / モバイル `@media` 群すべてに新クラス名を追加すること。

---

## 4. フィードバックブロック

### 4.1 例題用(reveal 型)

```html
<div class="feedback" data-feedback>
  <div class="fb-banner ok">
    <span class="icon">✓</span>
    <span>正答: {{正答テキスト}}</span>
  </div>
  <div class="fb-body">
    <div class="fb-section">
      <div class="fb-section-title">ベストフィット</div>
      <div class="fb-bestfit">{{原本のベストフィット要点}}</div>
    </div>
    <div class="fb-section">
      <div class="fb-section-title">解説</div>
      <div class="fb-explain">
        <p>{{原本の解説}}</p>
      </div>
    </div>
    <div class="fb-section">
      <div class="fb-section-title">{{補足タイトル、例: なぜ〜なのか}}(補足)</div>
      <div class="fb-explain">
        <p>{{独自に補強した説明}}</p>
      </div>
    </div>

    [viz(§3)を必ず1つ以上添える]
  </div>
</div>
```

### 4.2 練習問題用(grade 型)

```html
<div class="feedback" data-feedback>
  <div class="fb-banner ok"><span class="icon">✓</span><span>解説</span><span class="score-tag"></span></div>
  <div class="fb-body">
    <div class="fb-section">
      <div class="fb-section-title">{{解説 / 正答 / 解説 — 適当でないもの — など}}</div>
      <div class="fb-explain">
        <ul>
          <li><strong>⑴</strong> {{各小問の解説}}</li>
          <li><strong>⑵</strong> {{...}}</li>
        </ul>
      </div>
    </div>
    <div class="fb-section">
      <div class="fb-section-title">{{補足タイトル}}</div>
      <div class="fb-explain">
        <p>{{独自補強}}</p>
      </div>
    </div>

    [viz(§3)を必ず1つ以上添える]
  </div>
</div>
```

★ 練習問題の banner には `<span class="score-tag"></span>` を必ず置く(JSが採点後に "完答 X/Y" を埋める)。例題には不要(置いてもよいが空のままでよい)。

### 4.3 多選択(multi)で正答リストを示すパターン

```html
<div class="fb-section">
  <div class="fb-section-title">正答</div>
  <div class="fb-correct-line">{{(イ)、(ウ)、(エ)}}</div>
</div>
```

### 4.4 fill の正答行

```html
<div class="fb-section">
  <div class="fb-section-title">正答</div>
  <div class="fb-correct-line">① {{語1}} / ② {{語2}} / ③ {{語3}} / ...</div>
</div>
```

---

## 5. おさらい(Visual Digest)Q&A モジュール

★ 必ず `.digest-mod` を兄弟関係で並べる(SKILL.md §9.1 の入れ子バグ参照)。

```html
<section class="stage" data-stage-name="REVIEW">
  <div class="section-divider">
    <span class="num">01</span>
    <div class="text">
      <div class="label">Section 1 — Visual Digest</div>
      <div class="name">ひと目でわかる おさらい</div>
    </div>
  </div>

  <div class="digest">

    <!-- Module 1 (Hero) -->
    <div class="digest-mod hero">
      <button class="digest-prompt" type="button">
        <div class="digest-prompt-head">
          <span class="digest-num">01</span>
          <span class="digest-en">{{The Big Map}}</span>
          <span class="digest-toggle"><span class="plus">+</span></span>
        </div>
        <div class="digest-q">{{Q. 〜?}}</div>
      </button>
      <div class="digest-answer">
        <div class="digest-title">{{答えのタイトル}}</div>
        <p class="digest-lede">{{解説のリード文}}</p>
        [SVG family tree 等の大ビジュアル]
      </div>
    </div>

    <!-- Module 2 -->
    <div class="digest-mod">
      <button class="digest-prompt" type="button">
        <div class="digest-prompt-head">
          <span class="digest-num">02</span>
          <span class="digest-en">{{Subtitle}}</span>
          <span class="digest-toggle"><span class="plus">+</span></span>
        </div>
        <div class="digest-q">{{Q. 〜?}}</div>
      </button>
      <div class="digest-answer">
        <div class="digest-title">{{タイトル}}</div>
        <p class="digest-lede">{{リード}}</p>
        [4色カードグリッド等]
      </div>
    </div>

    <!-- Module 3〜6 も同じ構造で兄弟関係 -->

  </div>
</section>
```

### 標準の6モジュール構成

| 番号 | Q の例 | A のビジュアル |
|---|---|---|
| 01 | 〜はどう分類される?(全体俯瞰) | SVG family tree |
| 02 | 〜の各種は何を保護する? | 4色カードグリッド(`.ip-rich-grid`) |
| 03 | 発生・成立の対比軸は? | フロー対比(`.origin-compare`) |
| 04 | 二項対立的な構造は? | Lock vs Key(`.lk-grid`) or Compare(`.compare`) |
| 05 | 例外・境界線・条件は? | キーワードカード(`.bd-grid`) + 警告ボックス |
| 06 | 実用的な早見表は? | マークグリッド(`.cc-grid` 風) |

---

## 6. JS 連携(問題追加時の必須更新)

新しい単元を作るときは、JS 内の以下の配列を更新する:

### 6.1 TIMELINE_ENTRIES(サイドバー目次)

```javascript
const TIMELINE_ENTRIES = [
  { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
  { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
  { idx: 2,  group: 'examples', num: '例{{N}}',  label: '{{例題タイトル}}', probId: 'ex{{N}}' },
  // ... 例題分繰り返し
  { idx: {{i}}, group: 'practice', num: 'Q{{N}}', label: '{{練習タイトル}}', probId: 'p{{N}}' },
  // ... 練習問題分繰り返し
  { idx: {{last}}, group: 'result', num: '✓', label: '結果サマリ' }
];
```

### 6.2 PROBLEMS(サマリ用)

```javascript
const PROBLEMS = [
  { id: 'p{{N}}', label: 'Q{{N}}', name: '{{練習問題タイトル}}', stageIdx: {{stage番号}} },
  // 練習問題分繰り返し
];
```

### 6.3 サマリの分母とカウントアップ閾値

```html
<div class="summary-grade" id="summary-grade">—<span class="denom">/{{練習問題数}}</span></div>
<div class="summary-subline">{{練習問題数}}問の練習問題のうち、何問完答できたか。</div>
```

```javascript
// renderSummary 内
animateCounter(grade, 0, fullCount, 1100, '<span class="denom">/{{練習問題数}}</span>');

// updateTimeline 内のサイドバースコア
if (sbScore) sbScore.textContent = full + '/{{練習問題数}}';

// 評価帯の閾値(問題数に応じて手で調整)
if (fullCount >= {{Hi 閾値}}) grade.classList.add('s-high');
else if (fullCount >= {{Mid 閾値}}) grade.classList.add('s-mid');
else grade.classList.add('s-low');
```

| 練習問題数 | s-high | s-mid |
|-----------|--------|-------|
| 6 | ≥ 5 | ≥ 3 |
| 8 | ≥ 7 | ≥ 4 |
| 10 | ≥ 8 | ≥ 5 |

### 6.4 触ってはいけない JS フック群(コピー元から絶対消さない)

新規単元のコピー元(`examples/01-01-information-and-media.html`)に内蔵されている下記の JS は、ユニット内容と独立。差し替えで触らない:

- `isInsideHorizontalScroll(el)` — 水平スクロール領域内タッチを page-swipe から除外(`.viz-svg-wrap` `.family-tree-wrap` および overflow-x:auto を持つ任意の要素を検知)
- `haptic(ms)` — `navigator.vibrate` ラッパー、try-catch で iOS で安全に no-op
- `function animateCounter(el, from, to, duration, suffix)` — easeOutCubic でカウントアップ
- スポットライトハンドラ(`SPOT_SELECTOR` + click delegation + backdrop 注入)
- カルーセル hint + dot インジケーター注入(`.origin-compare.three-col` 検知 + IntersectionObserver)
- 採点後スクロールの sticky topbar 補正(`showFeedback` / `retryStage` 内)
- ステージ遷移時の `haptic(6)`
- ボタン data-action へのデリゲート haptic
- `touch-action: manipulation` を当てる CSS

これらが残っているか確認するシンプルな grep:

```bash
grep -c 'isInsideHorizontalScroll\|function haptic\|function animateCounter\|SPOT_SELECTOR\|spotlight-backdrop\|carousel-dots\|three-col\|touch-action: manipulation' articles/{{番号}}-{{slug}}/index.html
# 期待: 8 つすべて hit すれば OK
```

---

## 7. 編集の最小手順(チートシート)

1. `examples/01-01-information-and-media.html` を `articles/{{番号}}-{{slug}}/index.html` にコピー
2. `<title>` と Welcome stage のメタ情報を更新
3. **おさらいセクションの6モジュール**: 新単元のテーマに合わせて Q&A を書き直し、ビジュアルもテーマに沿ったものに差し替える
4. **例題ステージ**: 問題数に合わせて追加/削除、内容差し替え。各例題に「補足」+ viz を追加
5. **練習ステージ**: 問題数・問題タイプに合わせて追加/削除、内容差し替え。各練習に viz を追加
6. **JS の TIMELINE_ENTRIES と PROBLEMS** を新しい問題群に合わせて更新
7. **サマリの分母**(2箇所)を新しい練習問題数に更新
8. `practices/index.html` の単元一覧にカードを追加
9. 動作確認 → コミット → `examples/{{番号}}-{{slug}}.html` に凍結コピー
