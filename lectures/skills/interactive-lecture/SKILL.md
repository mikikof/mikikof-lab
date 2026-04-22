---
name: interactive-lecture
description: 授業用インタラクティブHTMLスライドサイトを制作するときに使う skill。情報Ⅰ・情報数理入門などの単元解説を、単一HTMLファイルで投影と復習の両方に使える形で作る。紺・青系フォーマルなデザイン、クリック展開式の答え隠し、学習ノート対応、最新実例の取り込みを標準装備する。新しい単元 (例: 第3回 コンピュータの仕組み) を作る依頼、既存単元の修正、あるいは類似のインタラクティブ教材の作成を頼まれたときに、この skill を読み込んで使用する。
---

# interactive-lecture / 授業用インタラクティブHTMLスライドサイト制作 skill

このスキルは `lectures/` ツールの内側で、実際にスライドサイトを作るための**技術仕様と制作手順**を定義する。

---

## 使うとき

- 情報Ⅰ・情報数理入門などの**単元解説スライドサイト**を新規作成
- 既存サイトの**部分修正・追加**
- 類似形式の**復習用Webツール**を作成

---

## 前提

作業着手前に**必ず**以下を順に読むこと:

1. `lectures/CLAUDE.md` ― 制作哲学・禁止事項・チェックリスト(「何を・なぜ」側)
2. 本ファイル(`SKILL.md`) ― 技術仕様と落とし穴(「どう」側)
3. `components.md` ― 部品カタログ
4. `examples/` の最新完成品 ― 生きた参照実装

「なぜ」側と「どう」側の両方を読まないと良いものは作れない。

---

## 1. 全体構成(標準:15〜20スライド)

過去の07情報セキュリティをベースとした標準構成:

```
┌────────────────────────────────────────────────┐
│ 01  タイトルスライド       (title-slide)         │
│ 02  アジェンダ             「このサイトで扱う内容」│
│ 03  セクション1 仕切り     (section-divider)    │
│ 04  セクション1 解説1       学習ノート対応       │
│ 05  セクション1 解説2       学習ノート対応       │
│ 06  セクション1 クイズ/実習 答え後出し          │
│ 07  セクション2 仕切り                           │
│ 08  セクション2 解説                             │
│ 09  セクション2 インタラクティブ要素             │
│ 10  セクション2 クイズ/実習                      │
│ 11  セクション3 仕切り                           │
│ 12  セクション3 解説+事例展開                   │
│ 13  セクション4 仕切り                           │
│ 14  セクション4 解説                             │
│ 15  セクション4 実習                             │
│ 16  学習ノート答え合わせ   (穴埋め一括表示)      │
│ 17  まとめ(ツリー図)                             │
│ 18  復習チャレンジ(10問ランダム)                 │
│ 19  エンドカード(COVEREDラベルのみ)              │
└────────────────────────────────────────────────┘
```

セクション数は単元により 2〜5 に変動する。

---

## 2. Design Tokens(絶対に守る)

CSS変数で統一管理する。スライド単位で色を変えない。

```css
:root {
  --navy-darkest: #0F2847;    /* 見出し、タイトル背景最濃 */
  --navy-dark: #1B3A5B;       /* バー背景 */
  --navy: #2C5F8D;            /* メイン紺 */
  --navy-light: #4A7FA8;      /* 補助 */
  --navy-pale: #D4E1EF;       /* 境界線、穴埋め背景 */
  --navy-bg: #F3F6FB;         /* ライト背景 */

  --accent-red: #C8102E;      /* 警告・NG・eyebrowラベル */
  --accent-red-dark: #8B0A1F;
  --accent-gold: #C9A961;     /* アクセント・正解・コールアウト */

  --text-main: #1A2332;
  --text-sub: #5A6378;
  --white: #FFFFFF;
}
```

### フォント

```css
body { font-family: 'Noto Sans JP', sans-serif; }
.slide-title, .title-main, .section-heading { font-family: 'Noto Serif JP', serif; }
.eyebrow, .page-indicator { font-family: 'JetBrains Mono', monospace; }
```

Google Fonts は以下で読み込む:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700;900&family=Noto+Sans+JP:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

---

## 3. レイアウト設計の核

### 3.1 スライドコンテナ(変更禁止)

```css
.slide {
  position: absolute;
  top: 47px;      /* topbar 44px + progressbar 3px を避ける */
  bottom: 52px;   /* bottombar 52px を避ける */
  left: 0;
  right: 0;
  padding: 4vh 5vw;
  opacity: 0;
  pointer-events: none;
  transform: translateX(30px);
  transition: opacity 0.4s ease, transform 0.4s ease;
  background: var(--white);
  overflow-y: auto;
}
.slide.active {
  opacity: 1;
  pointer-events: all;
  transform: translateX(0);
}
```

**注意**: `inset: 0` だと topbar/bottombar の下に潜り込むので、`top: 47px; bottom: 52px` を厳守。

### 3.2 セクション仕切りの縦中央配置

`.slide` の `overflow-y: auto` と `padding-bottom` が flex 縦中央揃えと衝突して下にずれるバグがあった。以下で強制する:

```css
.section-divider {
  display: flex !important;
  flex-direction: column;
  justify-content: center !important;
  align-items: center !important;
  background: linear-gradient(135deg, var(--navy-darkest) 0%, var(--navy) 100%);
  color: white;
  position: absolute;
  padding: 0 5vw !important;
  overflow: hidden !important;
  text-align: center;
}
.section-divider > * { position: relative; z-index: 2; }
```

---

## 4. ナビゲーション(全スライド共通)

```javascript
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
let currentSlide = 0;

function goToSlide(n) {
  if (n < 0 || n >= totalSlides) return;
  slides[currentSlide].classList.remove('active');
  currentSlide = n;
  slides[currentSlide].classList.add('active');
  slides[currentSlide].scrollTop = 0;
  updateUI();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
    e.preventDefault(); goToSlide(currentSlide + 1);
  } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
    e.preventDefault(); goToSlide(currentSlide - 1);
  } else if (e.key === 'Home') { goToSlide(0); }
  else if (e.key === 'End') { goToSlide(totalSlides - 1); }
  else if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); }
});

let touchStartX = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
}, { passive: true });
document.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(dx) > 60) {
    if (dx < 0) goToSlide(currentSlide + 1);
    else goToSlide(currentSlide - 1);
  }
}, { passive: true });

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {});
  } else {
    document.exitFullscreen().catch(() => {});
  }
}
```

---

## 5. インタラクション・パターン(必須装備)

詳細コードは `components.md` に。

| パターン | 用途 | 答え隠し |
|---|---|---|
| 穴埋め(note-blank) | 学習ノートの空欄(①②③...) | クリックで正解表示 |
| 事例展開(case-expander) | ニュース・事件の詳細 | クリックで展開 |
| 定義カード(def-box) | 用語と意味のペア | 必要に応じて穴埋め併用 |
| 分類カード(cia-grid) | 3要素など並列する概念 | クリックで詳細展開 |
| 選択問題(quiz-container) | 4択等 | クリックで正誤判定+解説 |
| 実習リスト(practice-list) | 5〜6個の評価問題 | 判定は「?」→クリックで適切/不適切 |
| 答え合わせグリッド(answers-grid) | 学習ノート ①〜⑬ の一括確認 | 個別 + 一括表示ボタン |
| 復習チャレンジ(review) | ランダム10問出題 | 即時採点 |
| インタラクティブ計算機 | 数値を動かして体感 | 実習計算問題と連動 |
| トグルタブ(filter-toggle) | 2つの概念の対比 | 切替式 + メリデメ展開 |
| 逆転クイズカード(malware-grid) | 説明→用語を当てる | クリックで用語展開 |

**各パターンは必ず `components.md` から該当コードをコピーして使う**。自己流で作り直さない。

---

## 6. 事例の扱い(case-expander)

### なぜ事例を入れるか
抽象的な定義だけでは学生の記憶に残らない。「CIAの可用性が破られた事件」と言うよりも「2025年のアサヒGHD事件で数週間ビール出荷が止まった」と言う方が刺さる。共通テストや大学入試でも時事絡みの出題が増えている。

### 事例選びの基準
- **最新性**:過去1〜3年以内の事件を優先
- **知名度**:学生が名前を聞いたことがある企業・サービス
- **教科書キーワードとの対応**:「マルウェア」「ランサムウェア」「セキュリティホール」等と明確に対応
- **社会的インパクト**:被害規模が大きく、議論を呼んだもの

### 事例の書式(メタ情報込み)
```
[年] 事件名 [カテゴリタグ]
├ 何が起きたか(2〜3文)
├ なぜ起きたか(侵入経路・原因)
└ メタ: 被害規模 / 侵入経路 / CIA対応 / 教訓
```

### 必ず裏取りする
記憶だけで事件の詳細(被害件数・日付)を書かない。web_search で確認、または `conversation_search` で過去セッションの調査結果を活用。**間違った事実を教材に載せると致命的**。

---

## 7. 標準作業フロー

```
[1] 要件把握
   └ ユーザーから学習ノート画像/PDF受領
   └ 項番・実習・POINT を洗い出す
   └ 対象単元番号・スラッグ・授業のコマ数を確認

[2] 構成案の提示と合意
   └ カバー範囲、スライド数、インタラクション要素
   └ ask_user_input_v0 で選択肢提示
   └ 合意前にコード書き始めない

[3] 事例・最新情報のリサーチ(必要な場合)
   └ web_search で最新事件を確認
   └ 3〜5件の事例候補をピックアップ

[4] 実装
   └ template.html をコピーして articles/<番号>-<スラッグ>/index.html に
   └ components.md から必要パーツをコピーして中身を入れる
   └ デザイントークンは絶対に変えない

[5] 構文チェック
   └ 中括弧バランス、<script>タグ、<div>タグの対応
   └ 既知の落とし穴(セクション9)に照らす

[6] ユーザーへの報告・フィードバックループ
   └ 変更サマリ + 気になりそうな点を先回りで報告
   └ 投影してのフィードバックに基づき修正

[7] 完成凍結
   └ 完成版を examples/ にも <番号>-<スラッグ>.html でコピー
   └ lectures/index.html の単元一覧に追加
   └ git commit -m "lectures: ..." でコミット
```

---

## 8. 表現の禁止リスト

以下は使わない。見つけたら修正する:

- 「やってみよう」「頑張ろう」「みんなで考えてみよう」
- 「東大受験生向け」「難関大志望者へ」などの対象特定表現
- 「完璧!」「素晴らしい!」など過剰な褒め言葉(復習チャレンジの結果コメントは短く中立)
- ❤️🎉🚀 等の装飾絵文字(💡 ● ▸ など機能的記号は可)
- 「○○の全論点をカバーしました」のような自画自賛

---

## 9. 既知の落とし穴(はまった罠の記録)

### 9.1 セクション仕切りが下にずれる
- **原因**: `.slide` の `padding-bottom` + `overflow-y: auto` + `.section-divider` の flex 縦中央が衝突
- **対策**: `.section-divider` に `!important` で flex/overflow を強制、`padding: 0 5vw` で上下対称に

### 9.2 スライドコンテンツがバーの下に潜る
- **原因**: `.slide { inset: 0; }` だと topbar/bottombar の範囲にも展開される
- **対策**: `top: 47px; bottom: 52px` で明示的にバーを避ける

### 9.3 答えが先に見えてしまう
- **原因**: verdict やラベルに最初から「適切」「不適切」等の文字を入れている
- **対策**: デフォルトは `?` または「クリックで確認」、`revealed` クラス付与時に JS でテキストを書き換える

### 9.4 パスワード強度計算機の表示が溢れる
- **原因**: `Math.pow(95, 16)` のような巨大数値をそのまま表示
- **対策**: `fmtNum()` で 百万/億/兆/京/指数 に段階切替

### 9.5 iPad Safari でスワイプが効かない
- **原因**: `touchend` で `preventDefault` しているとスクロールと競合
- **対策**: `{ passive: true }` でリスナー登録、スクロールを妨げない

### 9.6 Google Fonts が遅い/読み込まれない
- **対策**: `preconnect` を2行先に入れる

### 9.7 クイズ選択肢を2回以上クリックできてしまう
- **原因**: 判定後に `pointer-events: none` を付けていない
- **対策**: `answerQuiz()` 内で全 option に `pointerEvents = 'none'`

---

## 10. 納品前の最終確認

`lectures/CLAUDE.md` セクション7のチェックリストに準拠:

- [ ] 学習ノート全項番 + 全実習の網羅
- [ ] 答え後出し徹底
- [ ] デザイントークン遵守
- [ ] セクション仕切りが中央配置
- [ ] バーとの衝突なし
- [ ] 矢印/スペース/タッチ/F キー全て動作
- [ ] 幅1100px以下で崩れない
- [ ] NG表現なし
- [ ] 最新事例が含まれている(該当する場合)
- [ ] examples/ に凍結コピー
- [ ] lectures/index.html の一覧に追加

---

## 11. 参照ファイル

| ファイル | 内容 |
|---|---|
| `template.html` | 空の骨組みHTML(コピーして articles/ に配置) |
| `components.md` | 13種の再利用可能パーツカタログ |
| `examples/07-information-security.html` | 完成例(情報セキュリティ) |
