# components.md / 再利用部品カタログ

このファイルは、`template.html` に組み込んで使うパーツ集。コピペして使えるように、**CSS + HTML + JS の3点セット**で書かれている。

新しい単元を作るときは、必要なパーツだけここから拾って `template.html` に追加する。自己流で作り直さない。

---

## 目次

- [01. agenda-grid](#01-agenda-grid) ― アジェンダ(4項目グリッド)
- [02. note-blank](#02-note-blank) ― 穴埋めクリック展開(template.html に実装済み)
- [03. def-box](#03-def-box) ― 用語定義ボックス(template.html に実装済み)
- [04. cia-grid / classification-cards](#04-cia-grid--classification-cards) ― 3分類カード
- [05. case-expander](#05-case-expander) ― 事例の展開式カード
- [06. quiz-container](#06-quiz-container) ― 選択問題
- [07. practice-list](#07-practice-list) ― 実習評価リスト
- [08. malware-grid (quiz-card)](#08-malware-grid-quiz-card) ― 3カードクイズ
- [09. pw-calc](#09-pw-calc) ― インタラクティブ計算機(パスワード強度例)
- [10. filter-toggle](#10-filter-toggle) ― 2項対比タブ(メリ/デメ展開付き)
- [11. answers-grid](#11-answers-grid) ― 学習ノート答え合わせ一括表示
- [12. summary-tree](#12-summary-tree) ― まとめツリー図
- [13. review-container](#13-review-container) ― 復習チャレンジ(ランダム10問)
- [14. sort-game](#14-sort-game) ― 分類ゲーム(undo対応、タップでゾーン配置)
- [15. compare-timeline](#15-compare-timeline) ― 旧/新の対比タイムライン(モバイルは縦積み)
- [16. featured-card](#16-featured-card) ― 3カード中央を強調するフィーチャーパターン
- [17. slider-sim](#17-slider-sim) ― スライダー+ドロップダウン型シミュレーター

※ メニュー(目次ドロワー)とリセットは template.html に標準装備済み。コピーは不要。

---

## 01. agenda-grid

アジェンダ(全体構成)の4項目グリッド。

### CSS
```css
.agenda-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 30px;
}
.agenda-item {
  padding: 24px 28px;
  background: var(--navy-bg);
  border-left: 4px solid var(--navy);
  border-radius: 4px;
  transition: all 0.3s;
  display: flex; gap: 20px; align-items: flex-start;
}
.agenda-item:hover { background: var(--navy-pale); transform: translateX(4px); }
.agenda-num {
  font-family: 'Noto Serif JP', serif;
  font-size: 36px; font-weight: 700;
  color: var(--accent-red);
  line-height: 1; min-width: 50px;
}
.agenda-content h3 {
  font-family: 'Noto Serif JP', serif;
  font-weight: 600; font-size: 20px;
  color: var(--navy-darkest); margin-bottom: 6px;
}
.agenda-content p { font-size: 14px; color: var(--text-sub); line-height: 1.5; }

@media (max-width: 1100px) { .agenda-grid { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="agenda-grid">
  <div class="agenda-item">
    <div class="agenda-num">01</div>
    <div class="agenda-content">
      <h3>[[項目タイトル]]</h3>
      <p>[[概要1行]]</p>
    </div>
  </div>
  <!-- 04まで繰り返し -->
</div>
```

---

## 04. cia-grid / classification-cards

並列する3つの概念を見せるカード(CIA、三権分立、3種類の記憶など)。

### CSS
```css
.cia-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 30px;
}
.cia-card {
  background: linear-gradient(160deg, var(--white) 0%, var(--navy-bg) 100%);
  border: 2px solid var(--navy-pale);
  border-radius: 8px;
  padding: 28px;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.cia-card:hover {
  border-color: var(--accent-red);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(15,40,71,0.15);
}
.cia-card::before {
  content: ''; position: absolute; top: 0; left: 0;
  width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--navy) 0%, var(--accent-red) 100%);
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.4s;
}
.cia-card:hover::before { transform: scaleX(1); }
.cia-letter {
  font-family: 'Noto Serif JP', serif; font-weight: 900;
  font-size: 72px; color: var(--accent-red);
  line-height: 0.9; margin-bottom: 4px; opacity: 0.9;
}
.cia-eng {
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-sub); font-size: 11px;
  letter-spacing: 0.15em; margin-bottom: 4px; font-weight: 700;
}
.cia-jp {
  font-family: 'Noto Serif JP', serif; font-weight: 700;
  font-size: 24px; color: var(--navy-darkest); margin-bottom: 14px;
}
.cia-desc {
  font-size: 14px; line-height: 1.7;
  color: var(--text-main);
  padding-top: 14px; border-top: 1px solid var(--navy-pale);
}
.cia-example {
  margin-top: 14px; padding: 10px 12px;
  background: rgba(200,16,46,0.05);
  border-left: 3px solid var(--accent-red);
  font-size: 12px; color: var(--text-sub); line-height: 1.5;
}
.cia-example strong { color: var(--accent-red-dark); }

@media (max-width: 1100px) { .cia-grid { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="cia-grid">
  <div class="cia-card">
    <div class="cia-letter">C</div>
    <div class="cia-eng">[[ENGLISH LABEL]]</div>
    <div class="cia-jp">[[日本語名]]</div>
    <div class="cia-desc">[[定義文]]</div>
    <div class="cia-example"><strong>例:</strong>[[具体例]]</div>
  </div>
  <!-- I, A も同様 -->
</div>
```

---

## 05. case-expander

実例・事件の展開カード。クリックで詳細が開く。

### CSS
```css
.case-expander {
  background: var(--white);
  border: 1px solid var(--navy-pale);
  border-radius: 6px;
  margin-bottom: 10px;
  overflow: hidden;
  transition: all 0.3s;
}
.case-expander.open {
  border-color: var(--accent-red);
  box-shadow: 0 4px 20px rgba(200,16,46,0.1);
}
.case-head {
  padding: 14px 20px;
  cursor: pointer;
  display: flex; align-items: center; gap: 14px;
  background: var(--navy-bg);
  transition: background 0.2s;
}
.case-head:hover { background: var(--navy-pale); }
.case-year {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700; font-size: 13px;
  color: var(--accent-red); min-width: 50px;
}
.case-title {
  font-family: 'Noto Serif JP', serif; font-weight: 600;
  font-size: 16px; color: var(--navy-darkest); flex: 1;
}
.case-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 0.1em;
  color: var(--navy); background: var(--navy-pale);
  padding: 3px 8px; border-radius: 3px; font-weight: 700;
}
.case-toggle {
  color: var(--navy); font-size: 14px;
  transition: transform 0.3s;
  font-family: 'JetBrains Mono', monospace; font-weight: 700;
}
.case-expander.open .case-toggle { transform: rotate(45deg); }
.case-body {
  max-height: 0; overflow: hidden;
  transition: max-height 0.4s ease;
}
.case-expander.open .case-body { max-height: 500px; }
.case-content {
  padding: 16px 20px 18px 20px;
  font-size: 14px; line-height: 1.75;
  color: var(--text-main);
  border-top: 1px solid var(--navy-pale);
}
.case-content p { margin-bottom: 8px; }
.case-content strong { color: var(--accent-red-dark); }
.case-meta {
  display: flex; gap: 18px; margin-top: 10px; padding-top: 10px;
  border-top: 1px dashed var(--navy-pale);
  font-size: 12px; color: var(--text-sub);
  font-family: 'JetBrains Mono', monospace;
}
.case-meta-item strong {
  display: block; color: var(--navy);
  font-size: 9px; letter-spacing: 0.1em;
  text-transform: uppercase; margin-bottom: 2px;
}
```

### HTML
```html
<div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.15em; color: var(--accent-red); font-weight: 700; margin-bottom: 12px;">実際の事例 / CLICK TO EXPAND</div>

<div class="case-expander">
  <div class="case-head" onclick="toggleCase(this)">
    <span class="case-year">[[YYYY]]</span>
    <span class="case-title">[[事件名]]</span>
    <span class="case-tag">[[カテゴリ]]</span>
    <span class="case-toggle">+</span>
  </div>
  <div class="case-body"><div class="case-content">
    <p>[[事件の概要 2-3文]]</p>
    <p>[[原因・影響の追加説明]]</p>
    <div class="case-meta">
      <div class="case-meta-item"><strong>被害規模</strong>[[数値・範囲]]</div>
      <div class="case-meta-item"><strong>侵入経路</strong>[[手段]]</div>
      <div class="case-meta-item"><strong>教訓</strong>[[ポイント]]</div>
    </div>
  </div></div>
</div>
```

### JS
```javascript
function toggleCase(headEl) {
  headEl.parentElement.classList.toggle('open');
}
```

---

## 06. quiz-container

選択問題(4択)とフィードバック。

### CSS
```css
.quiz-container { max-width: 900px; margin: 30px auto 0; }
.quiz-question {
  background: var(--navy-darkest); color: white;
  padding: 20px 28px;
  border-radius: 6px 6px 0 0;
  font-size: 18px; line-height: 1.6;
  font-family: 'Noto Serif JP', serif; font-weight: 500;
}
.quiz-question-num {
  font-family: 'JetBrains Mono', monospace;
  color: var(--accent-gold);
  font-size: 11px; letter-spacing: 0.2em;
  margin-bottom: 8px; display: block;
}
.quiz-options {
  background: var(--white);
  border: 1px solid var(--navy-pale); border-top: none;
  border-radius: 0 0 6px 6px; padding: 18px;
}
.quiz-option {
  padding: 14px 18px; margin-bottom: 8px;
  background: var(--navy-bg);
  border: 2px solid transparent;
  border-radius: 4px; cursor: pointer;
  transition: all 0.2s;
  display: flex; gap: 14px; align-items: flex-start;
  font-size: 15px;
}
.quiz-option:hover { border-color: var(--navy); background: var(--navy-pale); }
.quiz-option:last-child { margin-bottom: 0; }
.quiz-option-letter {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700; color: var(--navy);
  min-width: 24px;
}
.quiz-option.correct {
  background: rgba(30,130,76,0.1);
  border-color: #1E824C;
}
.quiz-option.correct .quiz-option-letter { color: #1E824C; }
.quiz-option.incorrect {
  background: rgba(200,16,46,0.08);
  border-color: var(--accent-red);
  opacity: 0.6;
}
.quiz-feedback {
  display: none; margin-top: 14px;
  padding: 16px 20px; background: var(--navy-bg);
  border-left: 4px solid var(--accent-gold);
  font-size: 14px; line-height: 1.7;
  border-radius: 0 4px 4px 0;
}
.quiz-feedback.show { display: block; animation: fadeIn 0.4s; }
.quiz-feedback strong { color: var(--navy-darkest); }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### HTML
```html
<div class="quiz-container">
  <div class="quiz-question">
    <span class="quiz-question-num">QUESTION · [[ラベル]]</span>
    [[問題文 HTMLタグ可]]
  </div>
  <div class="quiz-options">
    <div class="quiz-option" onclick="answerQuiz(this, false)"><span class="quiz-option-letter">ア</span><span>[[選択肢1]]</span></div>
    <div class="quiz-option" onclick="answerQuiz(this, false)"><span class="quiz-option-letter">イ</span><span>[[選択肢2]]</span></div>
    <div class="quiz-option" onclick="answerQuiz(this, true)"><span class="quiz-option-letter">ウ</span><span>[[選択肢3 ← 正解]]</span></div>
    <div class="quiz-option" onclick="answerQuiz(this, false)"><span class="quiz-option-letter">エ</span><span>[[選択肢4]]</span></div>
  </div>
  <div class="quiz-feedback">
    <strong>正解:[[正解ラベル]]</strong><br>
    [[解説文]]
  </div>
</div>
```

### JS
```javascript
function answerQuiz(el, isCorrect) {
  const options = el.parentElement.querySelectorAll('.quiz-option');
  options.forEach(o => { o.style.pointerEvents = 'none'; });
  if (isCorrect) {
    el.classList.add('correct');
  } else {
    el.classList.add('incorrect');
    options.forEach(o => {
      if (o.onclick && o.onclick.toString().includes('true')) o.classList.add('correct');
    });
  }
  const fb = el.closest('.quiz-container').querySelector('.quiz-feedback');
  if (fb) fb.classList.add('show');
}
```

---

## 07. practice-list

5〜6個の評価問題(適切 or 不適切)を答え後出しで見せるリスト。

### CSS
```css
.practice-list { margin-top: 24px; }
.practice-item {
  display: flex; gap: 18px;
  padding: 16px 20px;
  background: var(--white);
  border: 1px solid var(--navy-pale);
  border-radius: 6px;
  margin-bottom: 10px;
  transition: all 0.25s;
  cursor: pointer;
  align-items: flex-start;
}
.practice-item:hover { background: var(--navy-bg); }
.practice-letter {
  font-family: 'Noto Serif JP', serif;
  font-weight: 700; color: var(--navy);
  min-width: 32px; font-size: 18px;
}
.practice-text { flex: 1; font-size: 14px; line-height: 1.7; }
.practice-verdict {
  padding: 4px 12px;
  border-radius: 3px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.1em; white-space: nowrap;
  min-width: 56px; text-align: center;
  background: transparent; color: var(--navy);
  border: 1px dashed var(--navy-light);
  transition: all 0.3s;
}
.practice-item.revealed .practice-verdict {
  border-style: solid; letter-spacing: 0.15em;
}
.practice-item.revealed.ok .practice-verdict {
  background: #1E824C; color: white; border-color: #1E824C;
}
.practice-item.revealed.ng .practice-verdict {
  background: var(--accent-red); color: white; border-color: var(--accent-red);
}
.practice-item.revealed .practice-reason {
  display: block; margin-top: 8px;
  padding: 10px 14px;
  background: var(--navy-bg);
  border-left: 3px solid var(--accent-gold);
  font-size: 12px; color: var(--text-sub);
  line-height: 1.6; width: 100%;
}
.practice-reason { display: none; }
```

### HTML
```html
<div class="practice-list">
  <div class="practice-item" onclick="revealPractice(this)">
    <span class="practice-letter">ア</span>
    <div class="practice-text">
      [[問題文(状況・行動の説明)]]
      <div class="practice-reason"><strong>[[判定キーワード]]</strong>[[理由の解説]]</div>
    </div>
    <span class="practice-verdict" data-ok="[[true or false]]">？</span>
  </div>
  <!-- イ、ウ、エ、オと続ける -->
</div>
```

### JS
```javascript
function revealPractice(item) {
  const verdict = item.querySelector('.practice-verdict');
  const ok = verdict.dataset.ok === 'true';
  item.classList.add('revealed');
  item.classList.add(ok ? 'ok' : 'ng');
  verdict.textContent = ok ? '適切' : '不適切';
}
```

---

## 08. malware-grid (quiz-card)

説明文 → クリックで用語名が出る逆転クイズ。3カード並び。

### CSS
```css
.malware-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 20px;
}
.malware-card {
  background: var(--white);
  border: 2px solid var(--navy-pale);
  border-radius: 8px;
  padding: 22px;
  transition: all 0.3s;
}
.malware-card:hover { border-color: var(--navy); transform: translateY(-2px); }
.malware-card.quiz-card { cursor: pointer; position: relative; }
.malware-card.quiz-card .malware-answer { display: none; }
.malware-card.quiz-card.revealed .malware-answer {
  display: block; animation: fadeIn 0.4s;
}
.malware-card.quiz-card.revealed .malware-hint { display: none; }
.malware-hint {
  margin-top: 10px; padding-top: 10px;
  border-top: 1px dashed var(--navy-pale);
  text-align: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.15em;
  color: var(--navy-light); font-weight: 700;
}
.malware-card.quiz-card.revealed {
  border-color: var(--accent-red);
  background: linear-gradient(160deg, var(--white) 0%, rgba(201,169,97,0.05) 100%);
}
.malware-type {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 0.2em;
  color: var(--accent-red); margin-bottom: 6px; font-weight: 700;
}
.malware-name {
  font-family: 'Noto Serif JP', serif; font-weight: 700;
  font-size: 20px; color: var(--navy-darkest); margin-bottom: 10px;
}
.malware-desc { font-size: 13px; line-height: 1.7; color: var(--text-main); }

@media (max-width: 1100px) { .malware-grid { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="malware-grid">
  <div class="malware-card quiz-card" onclick="this.classList.toggle('revealed')">
    <div class="malware-type">[[ラベル 例: 総称]]</div>
    <div class="malware-desc" style="margin-bottom: 12px;">[[説明文(問題文)]]</div>
    <div class="malware-answer">
      <div class="malware-name">[[正解の用語]]</div>
      <div style="font-size: 12px; color: var(--text-sub); line-height: 1.6;">[[補足]]</div>
    </div>
    <div class="malware-hint">クリックで正解</div>
  </div>
  <!-- 2枚目、3枚目 -->
</div>
```

### JS
HTML内 `onclick` で完結するので追加不要。

---

## 09. pw-calc

インタラクティブ計算機(パスワード強度例)。2つのスライダー + リアルタイム結果表示。

### CSS
```css
.pw-calc {
  background: linear-gradient(160deg, var(--navy-darkest) 0%, var(--navy-dark) 100%);
  border-radius: 10px;
  padding: 36px;
  color: white;
  margin-top: 24px;
  box-shadow: 0 12px 40px rgba(15,40,71,0.3);
}
.pw-calc-title {
  font-family: 'Noto Serif JP', serif;
  font-size: 22px; margin-bottom: 20px;
  color: var(--accent-gold);
}
.pw-sliders {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px; margin-bottom: 28px;
}
.pw-slider-group label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.15em;
  color: rgba(255,255,255,0.7); margin-bottom: 8px;
}
.pw-slider-val {
  font-family: 'Noto Serif JP', serif;
  font-size: 40px; font-weight: 700;
  color: var(--accent-gold);
  margin-bottom: 10px; line-height: 1;
}
.pw-slider-val .unit {
  font-size: 16px; color: rgba(255,255,255,0.5);
  margin-left: 6px; font-weight: 400;
}
input[type="range"] {
  -webkit-appearance: none;
  width: 100%; height: 4px;
  background: rgba(255,255,255,0.2);
  border-radius: 2px; outline: none;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px; height: 20px;
  background: var(--accent-gold);
  border-radius: 50%; cursor: pointer;
  border: 3px solid var(--navy-darkest);
  transition: transform 0.15s;
}
input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.2); }
input[type="range"]::-moz-range-thumb {
  width: 14px; height: 14px;
  background: var(--accent-gold);
  border-radius: 50%; cursor: pointer;
  border: 3px solid var(--navy-darkest);
}
.pw-results {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,0.15);
}
.pw-result { text-align: center; }
.pw-result-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 0.2em;
  color: rgba(255,255,255,0.6); margin-bottom: 8px;
  text-transform: uppercase;
}
.pw-result-val {
  font-family: 'Noto Serif JP', serif;
  font-size: 32px; font-weight: 700;
  color: white; line-height: 1;
}
.pw-result-val.warn { color: var(--accent-red); }
.pw-result-val.ok { color: #5ED47C; }
.pw-result-val.gold { color: var(--accent-gold); }
.pw-result-sub {
  font-size: 11px; color: rgba(255,255,255,0.5);
  margin-top: 6px;
}
.pw-formula {
  margin-top: 18px; padding: 12px 16px;
  background: rgba(0,0,0,0.3); border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: rgba(255,255,255,0.8);
  line-height: 1.6;
}

@media (max-width: 1100px) {
  .pw-sliders, .pw-results { grid-template-columns: 1fr; }
}
```

### HTML
```html
<div class="pw-calc">
  <div class="pw-calc-title">[[計算機のタイトル]]</div>
  <div class="pw-sliders">
    <div class="pw-slider-group">
      <label>使用可能な文字種(種類数)</label>
      <div class="pw-slider-val"><span id="charsetVal">50</span><span class="unit">種</span></div>
      <input type="range" id="charset" min="10" max="95" value="50" step="1">
      <div class="pw-result-sub">10=数字 / 26=英字 / 50=英数記号 / 95=全ASCII</div>
    </div>
    <div class="pw-slider-group">
      <label>パスワード長(文字数)</label>
      <div class="pw-slider-val"><span id="lenVal">3</span><span class="unit">文字</span></div>
      <input type="range" id="length" min="1" max="16" value="3" step="1">
      <div class="pw-result-sub">共通テストでは 3〜6 文字がよく題材に</div>
    </div>
  </div>
  <div class="pw-results">
    <div class="pw-result">
      <div class="pw-result-label">組み合わせ総数</div>
      <div class="pw-result-val gold" id="combiVal">125,000</div>
      <div class="pw-result-sub" id="combiFormula">50<sup>3</sup> = 125,000 通り</div>
    </div>
    <div class="pw-result">
      <div class="pw-result-label">最大解析時間 (5,000通り/秒)</div>
      <div class="pw-result-val" id="timeVal">25 秒</div>
      <div class="pw-result-sub" id="timeLabel">瞬時に突破される</div>
    </div>
  </div>
  <div class="pw-formula" id="pwFormulaText">
    💭 [[ヒント文]]
  </div>
</div>
```

### JS
```javascript
const charsetInput = document.getElementById('charset');
const lengthInput = document.getElementById('length');

function fmtNum(n) {
  if (n < 1e6) return n.toLocaleString();
  if (n < 1e9) return (n / 1e6).toFixed(2) + ' 百万';
  if (n < 1e12) return (n / 1e8).toFixed(2) + ' 億';
  if (n < 1e16) return (n / 1e12).toFixed(2) + ' 兆';
  if (n < 1e20) return (n / 1e16).toFixed(2) + ' 京';
  return n.toExponential(2) + ' 通り';
}

function fmtTime(sec) {
  if (sec < 1) return { val: '< 1秒', label: '瞬時に突破される', cls: 'warn' };
  if (sec < 60) return { val: Math.round(sec) + ' 秒', label: '極めて脆弱', cls: 'warn' };
  if (sec < 3600) return { val: (sec / 60).toFixed(1) + ' 分', label: '非常に弱い', cls: 'warn' };
  if (sec < 86400) return { val: (sec / 3600).toFixed(1) + ' 時間', label: '弱い', cls: 'warn' };
  if (sec < 86400 * 365) return { val: (sec / 86400).toFixed(1) + ' 日', label: 'やや弱い', cls: 'gold' };
  if (sec < 86400 * 365 * 100) return { val: (sec / (86400 * 365)).toFixed(1) + ' 年', label: '実用的に安全', cls: 'ok' };
  if (sec < 86400 * 365 * 1e6) return { val: (sec / (86400 * 365)).toExponential(1) + ' 年', label: '事実上解析不能', cls: 'ok' };
  return { val: '宇宙の年齢超', label: '理論的に不可能', cls: 'ok' };
}

function updatePwCalc() {
  const c = parseInt(charsetInput.value);
  const l = parseInt(lengthInput.value);
  document.getElementById('charsetVal').textContent = c;
  document.getElementById('lenVal').textContent = l;
  const total = Math.pow(c, l);
  const sec = total / 5000;
  document.getElementById('combiVal').textContent = fmtNum(total);
  document.getElementById('combiFormula').innerHTML = c + '<sup>' + l + '</sup> = ' + total.toExponential(3) + ' 通り';
  const t = fmtTime(sec);
  const timeEl = document.getElementById('timeVal');
  timeEl.textContent = t.val;
  timeEl.className = 'pw-result-val ' + t.cls;
  document.getElementById('timeLabel').textContent = t.label;
}
charsetInput.addEventListener('input', updatePwCalc);
lengthInput.addEventListener('input', updatePwCalc);
updatePwCalc();
```

---

## 10. filter-toggle

2つの概念を切り替えて比較するタブ式UI(ブラックリスト vs ホワイトリスト等)。メリット/デメリットを展開式にする。

### CSS
```css
.filter-toggle {
  display: inline-flex;
  background: var(--navy-bg);
  border-radius: 40px;
  padding: 5px;
  margin: 20px 0;
  border: 1px solid var(--navy-pale);
}
.filter-toggle button {
  padding: 10px 28px;
  background: transparent; border: none;
  cursor: pointer;
  font-family: 'Noto Serif JP', serif;
  font-weight: 600; font-size: 15px;
  color: var(--text-sub);
  border-radius: 30px;
  transition: all 0.25s;
}
.filter-toggle button.active {
  background: var(--navy-darkest); color: white;
}
.filter-display {
  background: var(--white);
  border: 1px solid var(--navy-pale);
  border-radius: 8px;
  padding: 24px 28px;
  margin-top: 14px;
}
.filter-display h4 {
  font-family: 'Noto Serif JP', serif;
  font-size: 20px; color: var(--navy-darkest);
  margin-bottom: 10px;
}
.filter-tagline {
  font-size: 14px; color: var(--text-sub);
  margin-bottom: 18px; line-height: 1.6;
}
.filter-pros-cons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px; margin-top: 14px;
}
.filter-box {
  padding: 14px 18px;
  border-radius: 6px;
  font-size: 13px; line-height: 1.7;
}
.filter-box.pros {
  background: rgba(30,130,76,0.08);
  border-left: 3px solid #1E824C;
}
.filter-box.cons {
  background: rgba(200,16,46,0.06);
  border-left: 3px solid var(--accent-red);
}
.filter-box h5 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 0.2em;
  margin-bottom: 8px;
}
.filter-box.pros h5 { color: #1E824C; }
.filter-box.cons h5 { color: var(--accent-red); }
.filter-guess {
  cursor: pointer; position: relative;
  transition: all 0.25s;
}
.filter-guess:hover { transform: translateY(-2px); }
.filter-guess .filter-answer { display: none; }
.filter-guess.revealed .filter-answer { display: block; animation: fadeIn 0.4s; }
.filter-guess.revealed .filter-hidden { display: none; }
.filter-hidden {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.15em;
  color: var(--text-sub);
  text-align: center; padding: 6px 0;
  font-weight: 700; opacity: 0.7;
}

@media (max-width: 1100px) { .filter-pros-cons { grid-template-columns: 1fr; } }
```

### HTML
```html
<div style="display: flex; justify-content: center;">
  <div class="filter-toggle">
    <button class="active" onclick="switchFilter('a', this)">[[選択肢A]]</button>
    <button onclick="switchFilter('b', this)">[[選択肢B]]</button>
  </div>
</div>

<div id="filterA" class="filter-display">
  <h4>[[選択肢Aタイトル]]</h4>
  <p class="filter-tagline">[[選択肢Aの説明]]</p>
  <div style="font-size: 13px; color: var(--text-sub); margin: 14px 0 10px; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em;">◆ メリット・デメリットを考えてみよう</div>
  <div class="filter-pros-cons">
    <div class="filter-box pros filter-guess" onclick="this.classList.toggle('revealed')">
      <h5>● メリット</h5>
      <div class="filter-hidden">クリックして確認</div>
      <div class="filter-answer">[[メリット文]]</div>
    </div>
    <div class="filter-box cons filter-guess" onclick="this.classList.toggle('revealed')">
      <h5>● デメリット</h5>
      <div class="filter-hidden">クリックして確認</div>
      <div class="filter-answer">[[デメリット文]]</div>
    </div>
  </div>
</div>

<div id="filterB" class="filter-display" style="display: none;">
  <!-- 選択肢Bも同様に -->
</div>
```

### JS
```javascript
function switchFilter(type, btn) {
  document.querySelectorAll('.filter-toggle button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('filterA').style.display = type === 'a' ? 'block' : 'none';
  document.getElementById('filterB').style.display = type === 'b' ? 'block' : 'none';
}
```

---

## 11. answers-grid

学習ノート①〜⑬の答え合わせ一括表示グリッド。

### CSS
```css
.answers-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 28px;
}
.answer-row {
  display: flex; align-items: center;
  padding: 12px 16px;
  background: var(--navy-bg);
  border-radius: 4px; gap: 12px;
  border-left: 3px solid var(--navy);
  cursor: pointer;
  transition: all 0.2s;
}
.answer-row:hover { background: var(--navy-pale); }
.answer-num {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700; color: var(--accent-red);
  font-size: 13px; min-width: 28px;
}
.answer-text {
  flex: 1; font-size: 14px;
  font-weight: 600; color: var(--navy-darkest);
}
.answer-reveal {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; padding: 4px 10px;
  background: var(--navy-dark); color: white;
  border-radius: 3px;
  letter-spacing: 0.08em;
  transition: all 0.3s;
}
.answer-row.revealed .answer-reveal {
  background: var(--accent-gold);
  color: var(--navy-darkest);
  font-weight: 700;
}

@media (max-width: 1100px) { .answers-grid { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="answers-grid">
  <div class="answer-row" onclick="revealAnswer(this)">
    <span class="answer-num">①</span>
    <span class="answer-text">[[ヒント文]]</span>
    <span class="answer-reveal" data-ans="[[正解]]">クリック</span>
  </div>
  <!-- ②〜⑬ と続ける -->
</div>

<div style="margin-top: 24px; display: flex; gap: 10px; justify-content: center;">
  <button onclick="revealAll()" style="background: var(--navy-darkest); color: white; border: none; padding: 10px 28px; font-family: 'Noto Serif JP', serif; font-weight: 600; border-radius: 30px; cursor: pointer; font-size: 14px;">すべて一括表示</button>
  <button onclick="hideAll()" style="background: transparent; color: var(--navy-darkest); border: 2px solid var(--navy); padding: 10px 28px; font-family: 'Noto Serif JP', serif; font-weight: 600; border-radius: 30px; cursor: pointer; font-size: 14px;">すべて隠す</button>
</div>
```

### JS
```javascript
function revealAnswer(row) {
  const reveal = row.querySelector('.answer-reveal');
  if (row.classList.contains('revealed')) {
    row.classList.remove('revealed');
    reveal.textContent = 'クリック';
  } else {
    row.classList.add('revealed');
    reveal.textContent = reveal.dataset.ans;
  }
}
function revealAll() {
  document.querySelectorAll('.answer-row').forEach(r => {
    r.classList.add('revealed');
    const reveal = r.querySelector('.answer-reveal');
    reveal.textContent = reveal.dataset.ans;
  });
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => {
    r.classList.remove('revealed');
    r.querySelector('.answer-reveal').textContent = 'クリック';
  });
}
```

---

## 12. summary-tree

まとめ用のツリー図(中央ノード + 4ブランチ)。

### CSS
```css
.summary-tree {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 20px;
}
.tree-center {
  background: var(--navy-darkest); color: white;
  padding: 22px 36px; border-radius: 8px;
  font-family: 'Noto Serif JP', serif;
  font-size: 26px; font-weight: 700;
  position: relative;
  box-shadow: 0 8px 24px rgba(15,40,71,0.25);
}
.tree-branches {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px; margin-top: 40px;
}
.tree-branch {
  background: var(--white);
  border: 2px solid var(--navy-pale);
  border-radius: 6px; padding: 18px;
  position: relative;
  transition: all 0.25s;
}
.tree-branch:hover { border-color: var(--accent-red); transform: translateY(-3px); }
.tree-branch::before {
  content: ''; position: absolute;
  top: -20px; left: 50%;
  width: 2px; height: 20px;
  background: var(--navy-pale);
}
.tree-branch h4 {
  font-family: 'Noto Serif JP', serif;
  font-size: 17px; color: var(--navy-darkest);
  margin-bottom: 8px;
}
.tree-branch ul {
  list-style: none;
  font-size: 12px; line-height: 1.8;
  color: var(--text-sub);
}
.tree-branch li::before { content: '▸ '; color: var(--accent-red); }

@media (max-width: 1100px) { .tree-branches { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="summary-tree">
  <div class="tree-center">[[中央概念]]</div>
</div>
<div class="tree-branches">
  <div class="tree-branch">
    <h4>[[分野1]]</h4>
    <ul>
      <li>[[項目]]</li>
      <li>[[項目]]</li>
    </ul>
  </div>
  <!-- 4ブランチまで -->
</div>
```

---

## 13. review-container

復習チャレンジ(ランダム10問出題 + 即時採点)。

### CSS
```css
.review-container {
  max-width: 800px;
  margin: 20px auto 0;
  text-align: center;
}
.review-intro {
  font-size: 15px; color: var(--text-sub);
  margin-bottom: 24px; line-height: 1.8;
}
.review-start-btn {
  background: var(--navy-darkest); color: white;
  border: none; padding: 14px 40px;
  font-size: 16px;
  font-family: 'Noto Serif JP', serif; font-weight: 600;
  border-radius: 50px; cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 6px 20px rgba(15,40,71,0.25);
}
.review-start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(15,40,71,0.35);
  background: var(--navy);
}
.review-q-area { display: none; margin-top: 24px; }
.review-q-area.active { display: block; }
.review-progress {
  font-family: 'JetBrains Mono', monospace;
  color: var(--navy);
  font-size: 12px; letter-spacing: 0.15em;
  margin-bottom: 14px;
}
.review-result {
  font-family: 'Noto Serif JP', serif;
  font-size: 48px; font-weight: 700;
  color: var(--accent-red);
  margin: 20px 0 10px;
}
.review-result-sub {
  font-size: 14px; color: var(--text-sub);
  margin-bottom: 24px;
}
.review-retry-btn {
  background: transparent;
  border: 2px solid var(--navy);
  color: var(--navy-darkest);
  padding: 10px 24px;
  font-family: 'Noto Serif JP', serif; font-weight: 600;
  border-radius: 30px; cursor: pointer;
  transition: all 0.2s;
}
.review-retry-btn:hover {
  background: var(--navy-darkest); color: white;
}
```

### HTML
```html
<div class="review-container">
  <div id="reviewStart">
    <p class="review-intro">学習ノートと本サイトの内容から10問を出題します。<br>即時採点で、自分の理解度を可視化しましょう。</p>
    <button class="review-start-btn" onclick="startReview()">▶ 開始する</button>
  </div>
  <div id="reviewQuiz" class="review-q-area">
    <div class="review-progress" id="reviewProgress">QUESTION 1 / 10</div>
    <div class="quiz-container" style="margin: 0;">
      <div class="quiz-question" id="reviewQText"></div>
      <div class="quiz-options" id="reviewQOpts"></div>
    </div>
  </div>
  <div id="reviewDone" class="review-q-area" style="text-align: center;">
    <div style="font-family: 'JetBrains Mono', monospace; color: var(--navy); font-size: 12px; letter-spacing: 0.2em; margin-bottom: 14px;">RESULT</div>
    <div class="review-result" id="reviewScore">0 / 10</div>
    <div class="review-result-sub" id="reviewComment"></div>
    <button class="review-retry-btn" onclick="startReview()">もう一度</button>
  </div>
</div>
```

### JS
```javascript
// 問題プールは単元ごとに書き換える(10問以上用意するとランダム性が出る)
const reviewPool = [
  {q: '[[問題文]]', opts: ['[[選択肢1]]', '[[選択肢2]]', '[[選択肢3]]', '[[選択肢4]]'], a: 0 /* 正解indexは0-3 */},
  // ... 12問以上推奨
];

let reviewQuestions = [];
let reviewIdx = 0;
let reviewScore = 0;

function startReview() {
  reviewQuestions = [...reviewPool].sort(() => Math.random() - 0.5).slice(0, 10);
  reviewIdx = 0;
  reviewScore = 0;
  document.getElementById('reviewStart').style.display = 'none';
  document.getElementById('reviewDone').classList.remove('active');
  document.getElementById('reviewQuiz').classList.add('active');
  showReviewQ();
}

function showReviewQ() {
  const q = reviewQuestions[reviewIdx];
  document.getElementById('reviewProgress').textContent = 'QUESTION ' + (reviewIdx + 1) + ' / 10';
  document.getElementById('reviewQText').innerHTML =
    '<span class="quiz-question-num">Q' + (reviewIdx + 1) + '</span>' + q.q;
  const opts = document.getElementById('reviewQOpts');
  opts.innerHTML = '';
  const letters = ['ア', 'イ', 'ウ', 'エ'];
  q.opts.forEach((opt, i) => {
    const div = document.createElement('div');
    div.className = 'quiz-option';
    div.innerHTML = '<span class="quiz-option-letter">' + letters[i] + '</span><span>' + opt + '</span>';
    div.onclick = () => answerReview(div, i === q.a);
    opts.appendChild(div);
  });
}

function answerReview(el, isCorrect) {
  const options = el.parentElement.querySelectorAll('.quiz-option');
  options.forEach(o => { o.style.pointerEvents = 'none'; });
  const q = reviewQuestions[reviewIdx];
  if (isCorrect) {
    el.classList.add('correct');
    reviewScore++;
  } else {
    el.classList.add('incorrect');
    options[q.a].classList.add('correct');
  }
  setTimeout(() => {
    reviewIdx++;
    if (reviewIdx < 10) showReviewQ();
    else showReviewResult();
  }, 900);
}

function showReviewResult() {
  document.getElementById('reviewQuiz').classList.remove('active');
  document.getElementById('reviewDone').classList.add('active');
  document.getElementById('reviewScore').textContent = reviewScore + ' / 10';
  const comments = {
    10: '完璧。共通テスト余裕レベル。',
    9: '素晴らしい。あと一歩で満点。',
    8: '合格ライン。理解はほぼ十分。',
    7: 'もう一歩。苦手項目を復習しよう。',
    6: '6割ライン。スライドを見返そう。'
  };
  let msg = comments[reviewScore] || '基礎から見直そう。学習ノートを手元に。';
  document.getElementById('reviewComment').textContent = msg;
}
```

---

## 14. sort-game

8〜10枚の「行為カード」を4ゾーンに振り分ける分類ゲーム。**undo対応**(配置後のチップをクリックで取り戻せる)で、何度でも再配置可能。法律の適用先判断・概念マッピングなど幅広く応用可。

### CSS
```css
.sort-game { margin-top: 16px; }
.sort-stack {
  display: flex; flex-wrap: wrap; gap: 10px;
  padding: 14px; background: var(--navy-bg);
  border-radius: 8px; margin-bottom: 14px;
  min-height: 70px; border: 1px dashed var(--navy-pale);
}
.sort-card {
  padding: 11px 16px;
  background: white; border: 2px solid var(--navy-pale);
  border-radius: 6px; font-size: 15px;
  cursor: pointer; transition: all 0.25s;
  font-weight: 500; max-width: 300px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  line-height: 1.5;
}
.sort-card:hover { border-color: var(--navy); transform: translateY(-2px); }
.sort-card.selected {
  border-color: var(--accent-gold);
  background: rgba(201,169,97,0.12);
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 6px 16px rgba(201,169,97,0.25);
}
.sort-card.placed { display: none; }
.sort-zones {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;
}
.sort-zone {
  background: white; border: 2px dashed var(--navy-pale);
  border-radius: 8px; padding: 14px;
  min-height: 120px; cursor: pointer;
  transition: all 0.25s;
}
.sort-zone:hover { border-color: var(--navy); background: var(--navy-bg); }
.sort-zone.highlight {
  border-color: var(--accent-gold); border-style: solid;
  background: rgba(201,169,97,0.08);
}
.sort-zone-head {
  font-family: 'Noto Serif JP', serif; font-weight: 700;
  font-size: 16px; color: var(--navy-darkest); margin-bottom: 6px;
}
.sort-zone-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.1em;
  color: var(--text-sub); margin-bottom: 12px; font-weight: 700;
}
.sort-placed-list { display: flex; flex-wrap: wrap; gap: 6px; }
.sort-placed-chip {
  padding: 6px 12px; font-size: 13px;
  border-radius: 12px; font-weight: 600;
  line-height: 1.5; cursor: pointer;
  transition: all 0.2s;
}
.sort-placed-chip:hover { transform: scale(0.97); filter: brightness(0.92); }
.sort-placed-chip::after {
  content: ' ✕'; opacity: 0;
  font-size: 11px; margin-left: 2px;
  transition: opacity 0.2s;
}
.sort-placed-chip:hover::after { opacity: 1; }
.sort-placed-chip.ok {
  background: rgba(30,130,76,0.12); color: var(--ok-green);
  border: 1px solid var(--ok-green);
}
.sort-placed-chip.ng {
  background: rgba(200,16,46,0.1); color: var(--accent-red);
  border: 1px solid var(--accent-red);
}
.sort-status {
  display: flex; justify-content: space-between;
  align-items: center; margin-top: 16px;
  padding: 12px 18px; background: var(--navy-darkest);
  color: white; border-radius: 6px; font-size: 14px;
  font-weight: 500;
}
.sort-status-score {
  font-family: 'JetBrains Mono', monospace; font-weight: 700;
  color: var(--accent-gold); font-size: 16px;
}
.sort-reset {
  padding: 6px 16px; background: transparent;
  color: white; border: 1px solid rgba(255,255,255,0.3);
  border-radius: 14px; cursor: pointer; font-size: 13px;
  font-family: 'Noto Serif JP', serif; font-weight: 600;
}
.sort-reveal-row {
  display: none; margin-top: 14px;
  padding: 14px 16px;
  background: var(--navy-bg);
  border-left: 3px solid var(--accent-gold);
  font-size: 14px; line-height: 1.75;
  border-radius: 0 4px 4px 0; font-weight: 500;
}
.sort-reveal-row.show { display: block; }

@media (max-width: 1100px) { .sort-zones { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="sort-game">
  <div class="sort-stack" id="sortStack"><!-- JS populates --></div>
  <div class="sort-zones">
    <div class="sort-zone" onclick="dropCard('zoneA')">
      <div class="sort-zone-head">[[ゾーンA タイトル]]</div>
      <div class="sort-zone-sub">[[英字タグ]]</div>
      <div class="sort-placed-list" data-list="zoneA"></div>
    </div>
    <!-- B, C, D と続ける -->
  </div>
  <div class="sort-status">
    <span>カードを選ぶ → ゾーンをタップで分類</span>
    <span>正解:<span class="sort-status-score" id="sortScore">0 / N</span></span>
    <button class="sort-reset" onclick="resetSort()">リセット</button>
  </div>
  <div class="sort-reveal-row" id="sortReveal"></div>
</div>
```

### JS
```javascript
const sortDeck = [
  { text: '[[行為1]]', zone: 'zoneA', explain: '[[解説]]' },
  // 8〜10 件
];
const sortZoneLabels = { zoneA: '[[ゾーンA]]', zoneB: '[[ゾーンB]]', zoneC: '[[ゾーンC]]', zoneD: '[[ゾーンD]]' };
const sortTotal = sortDeck.length;
let sortSelected = null;
let sortCorrect = 0;

function buildSort() {
  const stack = document.getElementById('sortStack');
  stack.innerHTML = '';
  sortCorrect = 0;
  const order = sortDeck.map((_, i) => i).sort(() => Math.random() - 0.5);
  order.forEach(i => {
    const card = document.createElement('div');
    card.className = 'sort-card';
    card.textContent = sortDeck[i].text;
    card.dataset.idx = i;
    card.onclick = () => pickSort(card);
    stack.appendChild(card);
  });
  Object.keys(sortZoneLabels).forEach(z => {
    const list = document.querySelector('[data-list="' + z + '"]');
    if (list) list.innerHTML = '';
  });
  document.getElementById('sortScore').textContent = '0 / ' + sortTotal;
  document.getElementById('sortReveal').classList.remove('show');
}
function pickSort(card) {
  if (card.classList.contains('placed')) return;
  document.querySelectorAll('.sort-card.selected').forEach(c => c.classList.remove('selected'));
  document.querySelectorAll('.sort-zone.highlight').forEach(z => z.classList.remove('highlight'));
  card.classList.add('selected');
  sortSelected = card;
  document.querySelectorAll('.sort-zone').forEach(z => z.classList.add('highlight'));
}
function dropCard(zone) {
  if (!sortSelected) return;
  const idx = parseInt(sortSelected.dataset.idx);
  const item = sortDeck[idx];
  const correct = item.zone === zone;
  const list = document.querySelector('[data-list="' + zone + '"]');
  const chip = document.createElement('div');
  chip.className = 'sort-placed-chip ' + (correct ? 'ok' : 'ng');
  chip.textContent = item.text;
  chip.dataset.cardIdx = idx;
  chip.title = (correct ? '正解:' : '不正解。正解は「' + sortZoneLabels[item.zone] + '」 ') + item.explain + ' ─ クリックで戻す';
  chip.onclick = () => undoChip(chip);
  list.appendChild(chip);
  sortSelected.classList.add('placed');
  sortSelected.classList.remove('selected');
  document.querySelectorAll('.sort-zone.highlight').forEach(z => z.classList.remove('highlight'));
  sortSelected = null;
  if (correct) sortCorrect++;
  updateSortStatus();
}
function undoChip(chip) {
  const idx = parseInt(chip.dataset.cardIdx);
  if (chip.classList.contains('ok')) sortCorrect = Math.max(0, sortCorrect - 1);
  chip.remove();
  const card = document.querySelector('.sort-card[data-idx="' + idx + '"]');
  if (card) card.classList.remove('placed');
  document.getElementById('sortReveal').classList.remove('show');
  updateSortStatus();
}
function updateSortStatus() {
  const placed = document.querySelectorAll('.sort-card.placed').length;
  document.getElementById('sortScore').textContent = sortCorrect + ' / ' + sortTotal;
  if (placed === sortTotal) {
    const rev = document.getElementById('sortReveal');
    rev.innerHTML = '<strong>結果:' + sortCorrect + '/' + sortTotal + ' 正解。</strong>チップをクリックで戻して再配置できる。';
    rev.classList.add('show');
  }
}
function resetSort() { buildSort(); }
buildSort();
// onResetHook に buildSort を登録
```

---

## 15. compare-timeline

旧/新など2系列のタイムラインを横並びで比較。モバイルでは自動で縦積みに変わり、各セルに「旧法」「新法」のラベルが付く。

### CSS
```css
.cmt-timeline { margin-top: 18px; }
.cmt-head {
  display: grid; grid-template-columns: 80px 1fr 1fr;
  gap: 10px; margin-bottom: 8px;
}
.cmt-head > div {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 0.15em;
  font-weight: 700; text-align: center;
  padding: 8px 12px; border-radius: 4px;
}
.cmt-head-step { background: transparent; }
.cmt-head-old { background: rgba(200,16,46,0.12); color: var(--accent-red-dark); }
.cmt-head-new { background: rgba(30,130,76,0.12); color: var(--ok-green); }

.cmt-step {
  display: grid; grid-template-columns: 80px 1fr 1fr;
  gap: 10px; margin-bottom: 6px;
  align-items: stretch;
}
.cmt-step-num {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: var(--navy-darkest); color: var(--accent-gold);
  border-radius: 6px; padding: 8px;
  font-family: 'Noto Serif JP', serif;
  font-weight: 700; font-size: 20px;
}
.cmt-step-num small {
  display: block; font-size: 9px;
  color: rgba(255,255,255,0.5);
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.15em; margin-bottom: 2px;
}
.cmt-cell {
  padding: 12px 16px;
  border-radius: 6px; cursor: pointer;
  transition: all 0.25s;
  font-size: 14px; line-height: 1.65;
  font-weight: 500;
}
.cmt-cell-old { background: rgba(200,16,46,0.06); border: 1px solid rgba(200,16,46,0.18); }
.cmt-cell-new { background: rgba(30,130,76,0.05); border: 1px solid rgba(30,130,76,0.18); }
.cmt-cell-head {
  font-family: 'Noto Sans JP', sans-serif; font-weight: 700;
  font-size: 15.5px; color: var(--navy-darkest);
  margin-bottom: 6px; line-height: 1.45;
}
.cmt-cell-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: var(--text-sub);
  margin-top: 6px; letter-spacing: 0.05em; font-weight: 600;
}
.cmt-cell-detail {
  display: none; margin-top: 10px;
  padding-top: 10px; border-top: 1px dashed var(--navy-pale);
  font-size: 13.5px; color: var(--text-main); line-height: 1.75;
}
.cmt-cell.open .cmt-cell-detail { display: block; }

/* タブレット(1100px以下)では新法を省略 */
@media (max-width: 1100px) {
  .cmt-step, .cmt-head { grid-template-columns: 60px 1fr; }
  .cmt-cell-new, .cmt-head-new { display: none; }
}

/* スマホ(720px以下)では縦積みで両方表示 */
@media (max-width: 720px) {
  .cmt-head { display: none; }
  .cmt-step { display: block; margin-bottom: 18px; }
  .cmt-step-num {
    display: inline-flex; width: auto; padding: 6px 14px 6px 10px;
    flex-direction: row; gap: 8px; margin-bottom: 10px; font-size: 16px;
  }
  .cmt-cell-old, .cmt-cell-new { display: block; margin-bottom: 8px; }
  .cmt-cell-old::before {
    content: '[[旧法ラベル]]'; display: inline-block;
    font-family: 'JetBrains Mono', monospace; font-size: 9.5px;
    color: var(--accent-red); font-weight: 700; letter-spacing: 0.12em;
    background: rgba(200,16,46,0.12); padding: 3px 9px;
    border-radius: 3px; margin-bottom: 8px;
  }
  .cmt-cell-new::before {
    content: '[[新法ラベル]]'; display: inline-block;
    font-family: 'JetBrains Mono', monospace; font-size: 9.5px;
    color: var(--ok-green); font-weight: 700; letter-spacing: 0.12em;
    background: rgba(30,130,76,0.12); padding: 3px 9px;
    border-radius: 3px; margin-bottom: 8px;
  }
}
```

### HTML
```html
<div class="cmt-timeline">
  <div class="cmt-head">
    <div class="cmt-head-step">STEP</div>
    <div class="cmt-head-old">[[旧系列タイトル]]</div>
    <div class="cmt-head-new">[[新系列タイトル]]</div>
  </div>
  <div class="cmt-step">
    <div class="cmt-step-num"><small>STEP</small>1</div>
    <div class="cmt-cell cmt-cell-old" onclick="this.classList.toggle('open')">
      <div class="cmt-cell-head">[[旧STEP1 見出し]]</div>
      <div>[[本文]]
      <div class="cmt-cell-meta">[[メタ情報]]</div></div>
      <div class="cmt-cell-detail">[[展開時の詳細]]</div>
    </div>
    <div class="cmt-cell cmt-cell-new" onclick="this.classList.toggle('open')">
      <!-- 新 STEP1 同様 -->
    </div>
  </div>
  <!-- STEP 2, 3, ... -->
</div>
```

### JS
HTML内 `onclick` で完結。追加不要。

---

## 16. featured-card

3枚カードのうち中央の1枚を「重要」として強調するパターン。紺のグラデ背景+金バッジ+内部に追加解説ブロック(callout)を仕込める。

### CSS
```css
.feat-grid {
  display: grid;
  grid-template-columns: 1fr 1.7fr 1fr;
  gap: 14px;
  align-items: stretch;
}
.feat-card {
  background: var(--navy-bg);
  padding: 18px 20px;
  border-radius: 8px;
  border-left: 3px solid var(--accent-red);
}
.feat-card.featured {
  background: linear-gradient(160deg, var(--navy-darkest) 0%, var(--navy-dark) 100%);
  color: white;
  border-left: 4px solid var(--accent-gold);
  box-shadow: 0 12px 32px rgba(15,40,71,0.3);
  position: relative;
  padding: 24px 26px 20px;
}
.feat-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--accent-red);
  letter-spacing: 0.15em; font-weight: 700; margin-bottom: 8px;
}
.feat-card.featured .feat-tag { color: var(--accent-gold); }
.feat-name {
  font-family: 'Noto Serif JP', serif; font-weight: 700;
  font-size: 17px; color: var(--navy-darkest);
  margin-bottom: 10px; line-height: 1.35;
}
.feat-card.featured .feat-name {
  color: white; font-size: 23px; margin-bottom: 4px;
}
.feat-alias {
  font-size: 13.5px; color: rgba(255,255,255,0.8);
  margin-bottom: 12px; font-weight: 500;
  padding-bottom: 10px;
  border-bottom: 1px dashed rgba(255,255,255,0.15);
}
.feat-desc {
  font-size: 14px; line-height: 1.75;
  color: var(--text-main); font-weight: 500;
}
.feat-card.featured .feat-desc {
  color: rgba(255,255,255,0.92); font-size: 14.5px;
}
.feat-badge {
  position: absolute; top: -12px; right: 16px;
  background: var(--accent-gold);
  color: var(--navy-darkest);
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 11px; font-weight: 700;
  padding: 5px 12px; border-radius: 14px;
  box-shadow: 0 4px 12px rgba(201,169,97,0.4);
}
.feat-callout {
  margin-top: 14px; padding: 14px 16px;
  background: rgba(201,169,97,0.12);
  border-left: 3px solid var(--accent-gold);
  border-radius: 0 4px 4px 0;
  font-size: 13.5px; line-height: 1.75;
  color: rgba(255,255,255,0.92);
  font-weight: 500;
}
.feat-callout strong { color: var(--accent-gold); font-weight: 700; }

@media (max-width: 1100px) { .feat-grid { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="feat-grid">
  <div class="feat-card">
    <div class="feat-tag">[[タグA]]</div>
    <div class="feat-name">[[用語A]]</div>
    <div class="feat-desc">[[説明A]]</div>
  </div>
  <div class="feat-card featured">
    <div class="feat-badge">KEY · [[強調理由]]</div>
    <div class="feat-tag">[[タグ中央]]</div>
    <div class="feat-name">[[重要用語]]</div>
    <div class="feat-alias">通称:<strong>[[別名]]</strong></div>
    <div class="feat-desc">[[本体解説]]</div>
    <div class="feat-callout">
      <strong>[[有名事例名]]</strong> — [[事例の要点]]
    </div>
  </div>
  <div class="feat-card">
    <!-- カードC -->
  </div>
</div>
```

---

## 17. slider-sim

ドロップダウン+スライダーを動かすと、リアルタイムに結果が変化するシミュレーター。`pw-calc` の発展形。クーリング・オフ判定(契約種別×経過日数)、統計計算、物理シミュレーションなどに応用可。

### CSS
```css
.ssm {
  background: linear-gradient(160deg, var(--navy-darkest) 0%, var(--navy-dark) 100%);
  border-radius: 10px; padding: 28px 32px;
  color: white; margin-top: 16px;
  box-shadow: 0 12px 40px rgba(15,40,71,0.3);
}
.ssm-title {
  font-family: 'Noto Serif JP', serif;
  font-size: 22px; margin-bottom: 20px;
  color: var(--accent-gold); font-weight: 700;
}
.ssm-controls { display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; margin-bottom: 22px; }
.ssm-group label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; letter-spacing: 0.15em;
  color: rgba(255,255,255,0.8); margin-bottom: 10px; font-weight: 700;
}
.ssm-select {
  width: 100%; padding: 12px 14px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  color: white; font-size: 16px;
  font-family: 'Noto Sans JP', sans-serif;
  cursor: pointer; font-weight: 500;
}
.ssm-select option { background: var(--navy-darkest); color: white; }
.ssm-slider-val {
  font-family: 'Noto Serif JP', serif;
  font-size: 36px; font-weight: 700;
  color: var(--accent-gold);
  margin-bottom: 10px; line-height: 1;
}
.ssm-slider-val .unit {
  font-size: 16px; color: rgba(255,255,255,0.6);
  margin-left: 6px; font-weight: 500;
}
input[type="range"].ssm-range {
  -webkit-appearance: none; width: 100%; height: 4px;
  background: rgba(255,255,255,0.2);
  border-radius: 2px; outline: none;
}
input[type="range"].ssm-range::-webkit-slider-thumb {
  -webkit-appearance: none; width: 18px; height: 18px;
  background: var(--accent-gold); border-radius: 50%;
  cursor: pointer; border: 3px solid var(--navy-darkest);
}
.ssm-result {
  padding: 22px 24px;
  background: rgba(0,0,0,0.25);
  border-radius: 8px;
  border-left: 4px solid var(--accent-gold);
  margin-top: 8px;
}
.ssm-verdict {
  font-family: 'Noto Serif JP', serif;
  font-size: 30px; font-weight: 700;
  margin-bottom: 8px;
}
.ssm-verdict.ok { color: #5ED47C; }
.ssm-verdict.warn { color: var(--accent-gold); }
.ssm-verdict.ng { color: var(--accent-red); }
.ssm-detail {
  font-size: 15px; color: rgba(255,255,255,0.85);
  line-height: 1.8; font-weight: 500;
}
.ssm-detail strong { color: var(--accent-gold); font-weight: 700; }
.ssm-note {
  margin-top: 16px; padding: 12px 16px;
  background: rgba(201,169,97,0.1);
  border-left: 3px solid var(--accent-gold);
  font-size: 14px; color: rgba(255,255,255,0.85);
  border-radius: 0 4px 4px 0;
  line-height: 1.75; font-weight: 500;
}

@media (max-width: 1100px) { .ssm-controls { grid-template-columns: 1fr; } }
```

### HTML
```html
<div class="ssm">
  <div class="ssm-title">◆ [[シミュレーターのタイトル]]</div>
  <div class="ssm-controls">
    <div class="ssm-group">
      <label>[[カテゴリ選択ラベル]]</label>
      <select class="ssm-select" id="ssmType">
        <option value="v1" data-x="[[パラメータ1]]">[[選択肢1]]</option>
        <option value="v2" data-x="[[パラメータ2]]">[[選択肢2]]</option>
      </select>
    </div>
    <div class="ssm-group">
      <label>[[数値ラベル]]</label>
      <div class="ssm-slider-val"><span id="ssmValN">0</span><span class="unit">[[単位]]</span></div>
      <input type="range" class="ssm-range" id="ssmN" min="0" max="30" value="0" step="1">
    </div>
  </div>
  <div class="ssm-result">
    <div class="ssm-verdict" id="ssmVerdict">[[判定]]</div>
    <div class="ssm-detail" id="ssmDetail">[[詳細説明]]</div>
  </div>
  <div class="ssm-note" id="ssmNote">⚠ [[注意書き]]</div>
</div>
```

### JS
```javascript
function updateSSM() {
  const type = document.getElementById('ssmType').value;
  const n = parseInt(document.getElementById('ssmN').value);
  document.getElementById('ssmValN').textContent = n;
  // 判定ロジック - 単元固有で書き換える
  const verdict = document.getElementById('ssmVerdict');
  const detail = document.getElementById('ssmDetail');
  // …
}
document.getElementById('ssmType').addEventListener('change', updateSSM);
document.getElementById('ssmN').addEventListener('input', updateSSM);
updateSSM();
// onResetHook で updateSSM をリセットに含めること
```

---

## 部品の組み合わせ例

典型的なスライドの中身は、上記パーツの組み合わせで作れる:

- **定義スライド**: `def-box` × 複数
- **3分類スライド**: `cia-grid`(CIA、三権分立、記憶階層など)
- **歴史/事件解説**: `body-text` + `case-expander` × 3〜5
- **対比スライド**: `filter-toggle` + 展開式メリデメ
- **強調カードスライド**: `feat-grid`(中央のカードを大きく目立たせる)
- **計算体感スライド**: `pw-calc` / `slider-sim`(応用可:指数関数、速度計算、確率計算)
- **分類ゲームスライド**: `sort-game`(8〜10枚を4ゾーンに振り分け、undo対応)
- **対比タイムライン**: `compare-timeline`(旧/新・Before/After・2系列を可視化)
- **答え合わせスライド**: `answers-grid` + 一括表示ボタン
- **まとめスライド**: `summary-tree`
- **復習スライド**: `review-container` + 12問プール

新しい部品が必要になったら、**ここに追記してから使う**。その場限りの一発屋スタイルは避ける。

## onResetHook との連動(リセット対応)

template.html の `resetAllInteractions()` は、以下の共通コンポーネントを自動リセットする:

- `.note-blank.reveal`、`.case-expander.open`、`.case-inline-opt`、`.case-inline-fb`
- `.quiz-option`(correct/incorrect)、`.quiz-feedback.show`
- `.practice-item.revealed`、`.answer-row.revealed`
- review-container の開始状態

**単元固有のインタラクション**(sort-game、slider-sim、compare-timeline、featured-card 内のクイズなど)は、template.html 末尾の `if (typeof onResetHook === 'function') onResetHook();` に対応する `onResetHook` 関数を定義して登録する:

```javascript
function onResetHook() {
  buildSort();          // sort-game をリセット
  updateSSM();          // slider-sim をリセット
  document.querySelectorAll('.cmt-cell.open').forEach(c => c.classList.remove('open'));
  // ...
}
```
