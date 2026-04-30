---
name: interactive-lecture
description: 授業用インタラクティブHTMLスライドサイトを制作するときに使う skill。情報Ⅰ・情報数理入門などの単元解説を、単一HTMLファイルで投影と復習の両方に使える形で作る。紺・青系フォーマルなデザイン、クリック展開式の答え隠し、学習ノート対応、最新実例の取り込みに加え、**学習ノート全 POINT 項目に SVG アイコン(law-illust)とインタラクティブ図解(interactive-svg-node / comparison-visual / flow-diagram / tree-diagram)を必須で併設する** ビジュアル重視運用を標準装備する。新しい単元 (例: 第3回 コンピュータの仕組み) を作る依頼、既存単元の修正、あるいは類似のインタラクティブ教材の作成を頼まれたときに、この skill を読み込んで使用する。
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
5. `lectures/_source/` の対応章Word + 解答PDFの対応ページ ― **問題と答えの正本**。これを開かずに問題・選択肢・解説を書くと、結論や根拠フレームが原本とズレて事故る(`lectures/CLAUDE.md` §4.8 / §6 [5] 参照)

「なぜ」側と「どう」側、そして「正本」の3つを読まないと良いものは作れない。

---

## 1. 全体構成(標準:15〜25スライド)

過去の06情報に関する法規・07情報セキュリティをベースとした標準構成:

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

### 標準装備(template.html に含まれる・外さないこと)

- **進捗バー**(topbar 直下の細いグラデーション帯、現在位置をリアルタイム反映)
- **スライド目次ドロワー**(topbar右端の `MENU` / `M` キー):セクションごとに自動グルーピング、PRACTICE/INTERACTIVE/REVIEW の自動タグ付け、現在スライドをハイライト、項目タップでジャンプ
- **インタラクション一括リセット**(ドロワー内の赤点線ボタン):note-blank・quiz・practice・case・answers-grid・review を初期化(単元固有のインタラクションは `onResetHook` に登録)
- **PC+スマホ ユニバーサル対応**:同一URLでPC(投影)は横長スライド、スマホ(復習)は縦に最適化された表示
- **キーボード**:← → / SPACE / PageUp / PageDown / Home / End / F(全画面) / M(メニュー) / ESC(メニュー閉じる)
- **タッチスワイプ**:水平40px以上かつ水平>垂直、800ms以内で左右送り。縦スクロールは干渉しない

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
.slide-title, .title-main, .section-heading { font-family: '游教科書体 横', 'YuKyokasho Yoko', 'UD デジタル 教科書体 N-R', 'Klee One', 'Noto Serif JP', serif; }
.eyebrow, .page-indicator { font-family: 'JetBrains Mono', monospace; }
```

`<head>` の Google Fonts link には Klee One を含める(macOS/iOS 以外で教科書体フォールバックが効くように):

```html
<link href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Noto+Serif+JP:wght@400;500;600;700;900&family=Noto+Sans+JP:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

#### 書体の使い分けルール

- **教科書体(游教科書体 横 → UD デジタル教科書体 → Klee One → Noto Serif JP の順でフォールバック)**:「見出し」「スライドタイトル」「定義用語名」「セクション大見出し」「実習の問題文」など、<strong>視線を止めて読む短い要素</strong> に限定。macOS/iOS は游教科書体 横、Windows 10+ は UD デジタル教科書体、Android その他は Klee One(Webフォント)、最終フォールバックが Noto Serif JP(明朝)。
- **Noto Sans JP(ゴシック)**:本文、解説、事例の長文、タイムラインのセル本文、メニュー項目など、<strong>連続して読む全ての長文</strong>。連続文に教科書体・明朝を使うとスマホ・低解像度投影で読みづらくなるため禁止。
- **JetBrains Mono**:ラベル・メタ情報・ページ番号・コード系の等幅表示専用。

#### 標準フォントサイズ・太さ(2026年改訂・投影視認性基準)

本文系は以下を下回らない:

| 要素 | サイズ | 太さ | 備考 |
|---|---|---|---|
| `.body-text` | 19px | 500 | 本文段落 |
| `.def-box .def-desc` | 16px | 500 | 定義ボックスの説明 |
| `.practice-text` | 16px | 500 | 実習の問題文 |
| `.case-content` | 16px | 500 | 事例展開の本文 |
| `.quiz-question` | 19px | 600 | クイズの問題文 |
| `.quiz-option` | 16.5px | 500 | クイズの選択肢 |
| `.quiz-feedback` | 16px | 500 | 解説 |
| `.slide-subtitle` | clamp(17, 1.7vw, 22)px | 500 | リード文 |
| `.section-heading` | 30px | 700 | 節見出し |

スマホでは `@media (max-width: 720px)` で各要素が一段階縮小(本文15px、問題文14.5px など)。template.html にベース実装済み。

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

## 3.3 ユニバーサル対応(PC投影 + スマホ復習)

同一URLで以下を満たすこと。template.html にベースは入っているが、単元固有の新しいコンポーネントを追加したときは必ずモバイル対応を書き足す:

### Viewport + セーフエリア

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

iPhoneのホームインジケータに隠されないよう、bottombar と slide は `env(safe-area-inset-bottom)` を使って自動で余白を確保している。

### ブレイクポイント

- **> 1100px** : PC・投影向け(2カラム以上のグリッド、フル装飾)
- **720–1100px** : タブレット・狭いラップトップ(1カラムに畳む)
- **≤ 720px** : スマホ縦画面(topbarサブタイトル非表示、slide-title-small非表示、本文1段階縮小、全グリッドを1カラムに、SVGもmax-width縮小)
- **≤ 380px** : iPhone SE など超狭幅(更に調整)
- **`(max-height: 500px) and (orientation: landscape)`** : スマホ横向き

新規コンポーネントを作るときは、`@media (max-width: 720px)` で以下を必ず書く:

1. 2カラム以上のグリッドは `grid-template-columns: 1fr` に畳む
2. SVGや固定幅の図は `max-width` を 280〜300px 程度に
3. 本文は 14.5〜15px、太字を500以上に
4. 余白(padding/gap)は縦方向に余裕を残す(bottombar に隠されないよう)

### スマホ時のUI差分

- topbar: 40pxに縮小、サブタイトル非表示、MENUボタン小型化
- bottombar: slide-title-small・keyboard-hint 非表示、前後ボタン+ページ番号のみ
- スライド送り:左右スワイプが有効(水平40px以上・800ms以内・縦スクロールと干渉しない)

### 納品前の検証

- 1100px幅のラップトップ、720pxのタブレット、375pxのiPhone 14、320pxのiPhone SE、landscape phoneで崩れないこと
- Safari レスポンシブモード(⌃⌘R)または `python3 -m http.server 8000` + 実機で確認

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

### 基本パターン
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

### ビジュアル必須パターン(2026-04 追加・lec06/lec07 標準)

**学習ノートの全 POINT 項目には基本パターンに加えて、以下から最低 1 つを併設すること**(`lectures/CLAUDE.md` §4.9 参照)。

| パターン | 用途 | 動作 |
|---|---|---|
| **law-illust**(18) | def-box 上部の SVG アイコン(法律・概念の象徴的なポンチ図) | 静的(視覚的補強用) |
| **judgment-chip**(19) | 正解 chip と不正解 chip を混ぜた判定型 | タップ → ○✕ + 個別fb / 全判定後に総括 verdict / RESET 可 |
| **interactive-svg-node**(20) | N 者関係の図(三角形・三方向保護など) | ノードタップ → 下部 info パネルに解説表示 |
| **comparison-visual**(21) | 二項対比図(紙 vs 電磁的・黒 vs 白リスト など) | 静的 + 場合により判定 chip 連動 |
| **flow-diagram**(22) | 処理の順序を可視化(ログイン・オプトイン・期間バー) | 各ステップタップ → 役割解説、または静的可視化 |
| **tree-diagram**(23) | 階層・分類(マルウェア家系・法のピラミッド) | ノードタップ → 解説表示 |

**各パターンは必ず `components.md` から該当コードをコピーして使う**。自己流で作り直さない。

### トグル標準(2026-04 追加・全インタラクション必須)

**問題の解答や、タップで開く解説・判定はすべて、もう一度タップで「初期状態に戻せる」こと**。一度タップして反応しなくなる UI は禁止。リセットボタンに頼らず、個別の操作で戻せるようにする。

| 種別 | 必要な挙動 |
|---|---|
| 開閉系(case-expander, rights-pole, access-card 等) | `classList.toggle('open')` で素直にトグル |
| 答え後出し系(note-blank, answer-row) | 再タップで初期テキストに戻す(`revealed` クラスをトグル) |
| 選択問題(quiz-option, case-inline-opt, term-pick-opt) | 同じ選択肢を再タップ → 全選択肢を初期化。別の選択肢をタップ → 前回をリセットして新しい解答を反映 |
| 判定型(practice-item, scope-chip, judgment-chip) | 再タップで判定(○/×・適切/不適切)を非表示に戻す。スコア・カウンタも自動再計算 |
| 段階的処理(pickPyr 等の確定型) | 正解で確定した状態を再タップで撤回(層リセット・選択肢再有効化) |
| 検出系(hitPhish 等のスキャン型) | 再タップで found 解除 + メーター減算 |

**実装上の禁止事項**:
- `pointerEvents = 'none'` でロックしない(再タップを潰す)
- 「すでに判定済みなら return」のような early-return もトグル off の処理に置き換える

**ユーザー選択を追跡するクラス**:選択問題では `chosen` クラスでユーザーが実際にタップした選択肢を追跡する。不正解時に自動付与される正答ハイライト(`correct`)とは区別する。これにより「再タップで撤回」と「別選択肢へ切替」の両動作を破綻なく実装できる。

**`resetAllInteractions` の同期**:新しいトグル対応クラス(`chosen` など)を導入したら、リセット関数の `classList.remove(...)` リストにも追加する。漏れるとリセット後に状態が残る。

**例外的にトグル対象外にする UI**:
- `answerReview`(章末レビューの自動次問送り)— 連続実技フローのため意図的にロック
- `selectPfNode` / `selectPymTier` / `switchFilter` 等の排他選択タブ — 別ノード選択で自動切替する仕様
- 多択提出系(`submitMulti`)— 「集計→確認→明示的リセット」の二段階フローを意図的に維持

### SVG 文字サイズの最小ルール(2026-04 追加)

law-illust など `viewBox="0 0 100 100"`(表示 92×92 px、モバイル 80×80 px)の SVG 内で:

- **漢字 1 文字(円・盾の中)**:`font-size 11+`、`font-weight 900` 推奨
- **英文ラベル**:`font-size 9+`(JetBrains Mono は字面が小さいので 10+ 推奨)
- **数字バッジ**:`font-size 14+`(目立たせる)
- **5px 以下は禁止**(モバイル表示で完全に潰れる)

過去事故:CIA 盾の `font-size 7-8` 文字「読めない」と指摘され全面修正。容器の円・盾は文字サイズに合わせて余裕をもって設計する(円は r=9+、盾は幅 36+ など)。

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

### 9.7 クイズ選択肢が一度答えたら反応しなくなる(2026-04 方針転換)
- **症状**: 答えてから「やっぱり違う選択肢も試したい」と思っても再タップが効かない。`pointerEvents = 'none'` でロックされている
- **原因(旧)**: 「判定後はロックすべき」という前提でロックを掛けていた
- **対策(新)**: §5「トグル標準」に準拠。`pointerEvents` ロックは廃止。`chosen` クラスでユーザー選択を追跡し、(a) 同じ選択肢の再タップ → 全選択肢を初期化、(b) 別の選択肢タップ → 前回をリセットして新しい解答を反映、の双方向動作にする。canonical 実装は `components.md` 06 の `answerQuiz` 参照

### 9.8 本文に教科書体・明朝体を使うと読みづらい(特にスマホ)
- **原因**: 教科書体フォールバックチェーン(`'游教科書体 横', ..., 'Noto Serif JP', serif`)を case-content や dm-cell-head のような連続読み要素に適用していた
- **対策**: 教科書体・明朝は見出し・用語名・問題文などの短い要素のみに限定。連続文はすべて Noto Sans に(3.2節 書体の使い分けルール参照)

### 9.9 語群(候補リスト)で正解が先に色付きで見えている
- **原因**: 正解にうっかり赤・太字スタイルをインラインで付けて「ハイライト」にしてしまう
- **対策**: 語群の全候補は同じ中立スタイル。答えは「クリック展開の先」だけに表示させる。制作後、必ず <strong>他人が見て答えが判別不能か</strong> チェック

### 9.10 分類ゲームなどで一度配置したら戻せない
- **原因**: カードに `.placed` を付けて `pointer-events: none` にしていた
- **対策**: 配置後のチップをクリックで取り戻せる(undo)実装を標準に。高校生は試行錯誤しながら理解するので、全て一方通行UIは学習効率を下げる

### 9.11 bottombar に本文の最終行が隠される(スマホ)
- **原因**: `.slide { bottom: 44px }` のみだとiPhoneのホームインジケータ領域+最終行のマージン不足で下端に食い込む
- **対策**: `bottom: calc(44px + env(safe-area-inset-bottom))` + スライドの `padding-bottom: 40px` を最低確保。`<meta viewport-fit=cover>` も必須

### 9.12 SVG内のtextを書き換えると元のラベルが失われる
- **原因**: `label.textContent = answers[target]` で全置換してしまう
- **対策**: 複数語のラベル(例「政令・省令」)は書き換え時も全文を渡す。初期表示の `(2) · 省令` のような複合情報は書き換え対象外か、辞書に完全形を持たせる

### 9.13 SVG 内の文字が小さくて読めない(law-illust 共通)
- **原因**: `viewBox="0 0 100 100"` で表示が 92×92 px しかないのに、`font-size 6-8` で書いていた
- **対策**: `font-size 9+`(漢字 1 文字は 11+ + `font-weight 900`)を最低基準に。容器(円・盾)も文字に合わせて十分大きく(円は r=9+、盾は幅 36+)。詳細は §5「SVG 文字サイズの最小ルール」
- 過去事故:lec07 ① CIA 盾で `font-size 7-8`、ユーザーから「小さくて読めない」と指摘 → 全 law-illust を一斉修正

### 9.14 判定型 chip(scope-chip)の意図が不明・反応に見えない
- **原因**: 全 chip が `data-correct="true"` のみで、タップしても全て同じ色・同じ verdict が出るだけ。判定の感覚がない
- **対策**:
  - 各パネルに **正解 chip と不正解 chip を混ぜる**(モラル視点パネルなら、モラル正解 + シティズンシップ独自=不正解の引っかけ)
  - `judgeScope(chip)` で `data-correct` を読み、`judged-correct`(○ 緑)/`judged-wrong`(✕ 赤)を分岐
  - 個別 fb はその chip 専用テキストを `data-fb` から表示
  - 全 chip 判定後にようやく総括 verdict を出す
  - **RESET ボタンで再挑戦可**(タップ後フリーズ放置にしない)
- components.md `19. judgment-chip` 参照

### 9.15 タップ反応のフィードバックが弱い
- **原因**: クラスを add するだけで、視覚的変化が地味/無音
- **対策**:
  - `:hover` だけでなく `:active`、または `transform: translateY(-2px) + box-shadow` でタップ感を出す
  - 同じ要素を再タップ時はアニメ再再生(`void el.offsetWidth; el.classList.add('show')` で再トリガ)
  - info パネル系は `animation: fadeIn 0.3s` を付ける

### 9.16 スマホで下端が切れる/ダブルタップでズーム/タップ感が無い(2026-04 標準パッケージで対応)
- **症状**:
  - スマホによっては最後の行が bottombar/ホームインジケータに隠れる
  - 連続タップで意図せずダブルタップ ズームが効いてしまう
  - タップしても押した感がなく反応が分かりにくい
- **対策パッケージ(template.html / 全 lecture HTML に標準装備、§12 参照)**:
  - bottombar 高さを 44 → 52px、`.slide` の `bottom: calc(52px + safe-area-inset-bottom)` + `padding-bottom: 64px`(safe-area 非対応端末でも余裕)
  - `body { touch-action: manipulation }`(縦スクロール+ピンチ維持、ダブルタップ ズーム抑制)+ `* { -webkit-tap-highlight-color: transparent }`
  - iOS Safari 用に JS で 320ms 以内の連続 touchend を `preventDefault`(input/select/a/textarea は除外)
  - `navigator.vibrate` の触覚フィードバック(送り 8ms / 正解 20ms / 不正解 [40,30,40] / リセット [15,40,15])
  - `nav-btn` モバイル 30×30 → 40×40 px(Apple HIG の最低 44px に近づける)
  - 主要タップ要素に `:active { transform: scale(0.96) }`(0.08s で押した感)
  - 初回モバイル ロード時に「スワイプで送る」フローティング ヒント(3.2 秒で自動消滅)
  - 全体 `user-select: none`、本文 `p / li / .case-content / .practice-text / .def-desc / .quiz-question / .quiz-feedback / .ch-body p / .answer-text` のみ選択可

### 9.17 法則 SVG が「平面ポリゴン + 白字テキスト」でチープに見える(2026-04 lec03 制作で発覚)

- **症状**: ユーザーから「文字が背景に同化して読めない」「全体的にビジュアル面がチープ」とのフィードバック。SVG 外周(viewBox 端の余白部分)に置いた `fill="white"` テキストが SVG 描画面の白に被って消える、opacity 0.4 等の透過 polygon に被るとさらに悲惨
- **原因**:
  - `<defs>` を使わず flat color の polygon + 直接 text を並べていた
  - text を SVG 外周(色のない余白部分)に置いて canvas の白と同化させていた
  - 透過 polygon に text を被せて視認性を捨てていた
- **対策(2026-04 lec03 で確立した SVG ビジュアル標準)**:
  - **`<defs>` で `<linearGradient>` を 2〜3 種類定義**(top-light → bottom-dark のグラデーション)。主要な polygon / rect は gradient 塗り
  - **`<filter>` で drop-shadow を仕込む**(`feGaussianBlur stdDeviation="0.7-2.2"` + `feOffset dx="0.5" dy="1.3"` + `feComponentTransfer slope="0.35-0.45"`)。主要素に `filter="url(#sh)"` を当てる
  - **上端 2-3px のホワイトハイライト線**(`fill="#FFFFFF" opacity="0.25-0.35"`)で立体感
  - **テキストは可能な限り SVG 外に逃がす**: 説明は `law-illust-tag`(SVG 直下のキャプション)と `def-desc`(def-box 本文)で。SVG 内テキストは「GAP」「?」のような **超短いシンボル** に限定
  - SVG 内テキストを置く場合、**必ず塗りのある rect / circle / polygon の上**に置く(canvas 余白に置かない)
  - `law-illust-tag` の文字列は **1 単語**(`DEDUCTIVE` / `TRADE-OFF` / `IDEAL ⇄ ACTUAL` 程度)に短縮。`SPECIFIC→GENERAL` のような 2 単語以上は letter-spacing 0.2em と相まって 92px 幅で切れる
- **canonical 参照**: `articles/03-problem-solving/index.html` の 5 つの law-illust SVG(山+ギャップ / 階段 / 天秤 / 漏斗 / 逆漏斗)。同単元のメイン天秤 (slide 6) と演繹/帰納 cmp-svg (slide 15) も同じ流儀
- 過去事故: lec03 初版で ②階段 SVG「課題=各段の踏み石」白字 on 白背景で消失、①山 SVG「理想/現状」テキスト同化、⑤逆漏斗「個別事実」白字が透過 polygon に被って読めず、`law-illust-tag` の `INDUCTIVE · SPECIFIC→GENERA…` 切れ → ユーザー指摘で全 5 SVG 再設計

### 9.18 単元内 SVG が「それぞれ違う作家が描いた」ようにバラバラに見える(2026-04 lec02 制作で発覚)

- **症状**: ユーザーから「全体的にチープ」「フリー素材でいいのでもっと **統一感** のあるおしゃれでわかりやすいイラストが良い」とのフィードバック。9.17 を守って各 SVG 単体は破綻していなくても、**SVG 同士の design language が揃っていない** と単元全体が素人くさく見える
- **原因**:
  - SVG ごとに独自の色・グラデ ID・形状言語(角を尖らせるか / 丸めるか、線か面か)を採用
  - 主役要素の色が SVG ごとに変わる(slide A は青系、slide B は赤系、slide C は金系...)
  - icon の概念表現が個別最適(円・矩形・自由曲線のミックス)で、見比べたときに「家族」に見えない
- **対策(2026-04 lec02 で確立した design system)**:
  - **共通の `<defs>` セットを全 SVG で使い回す**: 各 SVG の `<defs>` 内で同じ ID 名(または lec 単位で一意な接頭辞)で定義
    ```svg
    <linearGradient id="icoNavy" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5d8eb3"/>
      <stop offset="100%" stop-color="#0F2847"/>
    </linearGradient>
    <linearGradient id="icoGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f4d995"/>
      <stop offset="100%" stop-color="#8a6d1f"/>
    </linearGradient>
    <radialGradient id="icoBg" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F6FB"/>
    </radialGradient>
    <filter id="icoSh"><feGaussianBlur in="SourceAlpha" stdDeviation="0.7"/><feOffset dx="0.4" dy="1.2"/><feComponentTransfer><feFuncA type="linear" slope="0.4"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    ```
  - **役割を色で固定**:
    - **navy グラデ** = 主役・概念の本体
    - **gold グラデ / 単色** = アクセント・正解・「中心の重要要素」
    - **red グラデ / 単色** = 対比・警告・「逆側」
    - **navy-pale 単色 / opacity 0.3-0.5** = 補助線・connection
    - 中間色を作りたくなったら opacity で表現する
  - **背景は radialGradient で統一**(`#FFFFFF` 中心 → `#F3F6FB` 周辺)。flat な `#F3F6FB` よりわずかな立体感が出る
  - **シルエット重視**: 「目を細めて見ても何か分かる」レベルのアウトラインを最初に決める。詳細は後から
  - **同じ単元の全 SVG を並べて見比べる**: 「同じデザイナーが描いた」と感じるか?感じなければ揃え直す
- **フリー素材という選択肢**: 自作で揃えるのが難しい場合、確立された **オープンソース アイコン ライブラリ** から SVG path を借りるのが筋。**§13 アイコン ライブラリ ガイド** 参照
- **canonical 参照**: `articles/02-society-and-it/index.html` の 9 法則 SVG(SNS / IoT / ビッグデータ / サイバー犯罪 / 情報格差 / AI / 自律他律 / フレーム問題 / 生成AI)。すべて同じ navy + gold + 部分 red の三色制で統一されている
- 過去事故: lec02 初版で 9 SVG 各自が異なる color scheme(SNS=赤・IoT=赤箱・3V=円柱に文字・AI=脳の輪郭・フレーム=多重円)を採用。ユーザー指摘で全 9 SVG を design system で再設計

---

## 10. 納品前の最終確認

`lectures/CLAUDE.md` セクション7のチェックリストに準拠:

- [ ] 学習ノート全項番 + 全実習の網羅
- [ ] 答え後出し徹底(語群・一覧でも正解色付けしない)
- [ ] デザイントークン遵守
- [ ] セクション仕切りが中央配置
- [ ] バーとの衝突なし(モバイルは safe-area 対応)
- [ ] 矢印/スペース/F/M/ESC キー全て動作
- [ ] スワイプで前後移動(スマホ/タブレット)
- [ ] MENU ドロワーが開閉、目次から任意スライドに飛べる
- [ ] インタラクション全リセットが機能する(単元固有要素は `onResetHook` に登録)
- [ ] 幅 1100px / 720px / 380px / landscape phone すべてで崩れない
- [ ] 本文・連続文に教科書体フォールバックチェーン(`'游教科書体 横', ..., 'Noto Serif JP', serif`)を使っていない(短い見出しのみ教科書体)
- [ ] NG表現なし
- [ ] 最新事例が含まれている(該当する場合)
- [ ] examples/ に凍結コピー
- [ ] lectures/index.html の一覧に追加

---

## 11. 参照ファイル

| ファイル | 内容 |
|---|---|
| `template.html` | 空の骨組みHTML(メニュー・リセット・スマホ対応を含む完成済み基盤。コピーして articles/ に配置) |
| `components.md` | 再利用可能パーツカタログ(標準 17 種 + 2026-04 追加 6 種) |
| `examples/06-information-law.html` | **最新リファレンス**(情報に関する法規)。メニュー・リセット・スマホ対応・リッチインタラクション + ビジュアル必須6パターン全実装 |
| `examples/07-information-security.html` | **同等リファレンス**(情報セキュリティ)。CIA三角・ログインフロー・マルウェア家系・フィルタ比較を実装 |
| `articles/03-problem-solving/index.html` | **2026-04-30 SVG ビジュアル標準のリファレンス**(問題の発見と解決)。5 つの law-illust 全てに gradient + drop-shadow + 上端ハイライトを実装、テキストは SVG 外(law-illust-tag)に逃がし、main 天秤と演繹/帰納 cmp-svg にも同じ流儀。`§9.17` 参照 |
| `articles/02-society-and-it/index.html` | **2026-04-30 SVG design system 統一のリファレンス**(情報技術による社会の変化)。9 法則 SVG(SNS / IoT / ビッグデータ / サイバー犯罪 / 情報格差 / AI / 自律他律 / フレーム問題 / 生成AI)が共通の `<defs>`(icoNavy / icoGold / icoBg / icoSh)で完全統一。色役割固定(navy=主役、gold=アクセント、red=対比)。`§9.18` `§13` 参照。さらに IoT スライドには **センサ⇄アクチュエータの 4 段階閉ループ infographic**(560×230)+ 12 種の具体例カードを配置、本格的なインフォグラフィックの参考実装 |

新規単元を作るときは必ず `examples/06-information-law.html`(または `07-information-security.html`)を開いて、以下の実装を参照すること:

- 学習ノート POINT 項目ごとの **law-illust(SVG アイコン)+ インタラクティブ図解** の併設パターン
- インタラクション多数(穴埋め・分類ゲーム・タイムライン比較・シミュレーター)と `onResetHook` の連動
- スマホ時のタイムライン縦積み表示
- SVGの選択ハイライト(`.pf-node.selected` / `.cia-vertex.selected` の金枠)
- 対話型 SVG の info パネル(`#pfInfo` / `#ciaInfo` / `#malwareInfo` 等)+ JS の Map 構造
- フィッシング風スマホUIのCSS専用実装(07)
- case-expander 内部に quiz を連動させるパターン
- 「県立聖女学院」のような覚え方カード(暗記術)
- judgment-chip の正解/不正解混在 + RESET ボタン
- §12 のモバイル UX 強化パッケージ(haptic / dblclick prevent / :active scale / swipe hint)

---

## 12. モバイル UX 強化パッケージ(2026-04 標準・全 lecture 共通)

スマホでの「下端切れ・ダブルタップ ズーム・タップ感の弱さ」を解消する標準パッケージ。
**template.html に組み込み済み、新規単元はそのまま継承される**。既存単元には perl/Python で一括投入(本パッケージの全 lec への展開コミットを参照)。

### 12.1 含まれる対策

| 対策 | 実装場所 | 効果 |
|---|---|---|
| bottombar 44 → 52px / `.slide bottom: calc(52px + safe-area)` / padding-bottom 40 → 64px | CSS @media (≤720px) | 下端コンテンツが bar/ホームインジケータに隠れない。safe-area 非対応端末でも安全マージン |
| `* { -webkit-tap-highlight-color: transparent }` | CSS グローバル | iOS の青タップハイライト除去 |
| `body { touch-action: manipulation }` + `.slide { touch-action: pan-y pinch-zoom }` | CSS | ダブルタップ ズーム抑制(縦スクロール+ピンチ維持) |
| 320ms 以内の連続 touchend を `preventDefault`(input 等は除外) | JS グローバル | iOS Safari でも確実にダブルタップ無効化 |
| `navigator.vibrate` 触覚フィードバック(送り 8ms / 正解 20ms / 不正解 [40,30,40] / リセット [15,40,15]) | JS | Android で押した感 |
| `nav-btn` モバイル 30 → 40px | CSS @media | タップ精度向上(Apple HIG 44px に近づく) |
| `:active { transform: scale(0.96) }` (button / [onclick] / .nav-btn / .menu-toggle) | CSS @media | タップ視覚反応 |
| `.swipe-hint` フローティング バッジ(初回モバイル ロード時のみ・3.2秒) | CSS + JS | 初見ユーザーへのスワイプ操作の暗示 |
| 全体 `user-select: none` + 本文系のみ `user-select: text` | CSS | 誤選択防止 + 必要箇所のコピペは可能 |

### 12.2 標準コードの場所

- CSS の主要部分:`* { ... -webkit-tap-highlight-color: transparent; }` / `html, body { ... touch-action: manipulation; user-select: none; }` / `@media (max-width: 720px)` ブロック内の `.bottombar` / `.slide` / `.nav-btn` / `:active` / `.swipe-hint`
- JS の主要部分:`<script>` 直後に `isMobile()` / `haptic(ms)` / `touchend dblclick prevent`、`goToSlide` 内に `haptic(8)`、`answerQuiz` の正誤分岐に `haptic`、`resetAllInteractions` 冒頭に `haptic`、`</script>` 直前に swipe-hint init

具体的な実装は `template.html` の対応箇所、または `examples/07-information-security.html` を参照。

### 12.3 新規 lecture 制作時の確認

- `template.html` をコピーすれば 12.1 の対策はすべて入る
- 単元固有のコンポーネント(scope-chip 等)を追加した場合、`onclick` を持つ要素なら自動で `:active scale` が効く(汎用 CSS のため)
- `answerQuiz` 以外の判定系関数を新規に追加した場合は、関数内で `haptic(20)` / `haptic([40,30,40])` を呼ぶこと

### 12.4 既存 lecture に後付けする場合

`/tmp/mobile_ux_patch.py`(または同等の共通スクリプト)を流す。CSS は文字列が完全一致するなら一括置換可能。JS は `<script>` 直後と関数内で個別 Edit が必要(各 lec によりコメント体裁が違うため)。

この単元で確立された新パターンは、今後の単元にも積極的に転用する。

---

## 13. アイコン・イラスト ライブラリ ガイド(2026-04 lec02 制作で確立)

「自作 SVG が単元内でバラバラに見える」問題(§9.18)を解決する選択肢として、**確立された OSS アイコン ライブラリ** を活用する。

### 13.1 採用基準

- **ライセンス**: MIT / CC0 / Apache 2.0 など、商用・教育用途で使えるもの
- **デザインの一貫性**: 同じライブラリ内の任意の 2 アイコンを並べて、明らかに「同じ家族」と感じられる
- **網羅性**: 教材で使う概念(SNS / AI / IoT / 法律 / セキュリティ / 文章構造 等)が一通り揃う
- **SVG エクスポート可**: コピペで HTML に埋め込める

### 13.2 推奨ライブラリ

| ライブラリ | 特徴 | URL | 推奨用途 |
|---|---|---|---|
| **Lucide** | clean line-art、stroke-width 統一、24×24 viewBox、MIT | <https://lucide.dev/> | 抽象概念の標準アイコン(全般) |
| **Phosphor** | 6 weight(thin/light/regular/bold/fill/duotone)、MIT | <https://phosphoricons.com/> | デュオトーンが教材に映える。法学・統計・心理など |
| **Heroicons** | Tailwind 製、outline / solid 2 種、MIT | <https://heroicons.com/> | UI 寄りのシンプルさ重視 |
| **Tabler Icons** | 4000+ 個、line-art、MIT | <https://tabler-icons.io/> | 専門用語まで揃う豊富さ |
| **Material Symbols** | Google 製、3 fill レベル、Apache 2.0 | <https://fonts.google.com/icons> | 共通テスト系の馴染みやすさ |

### 13.3 単元内の運用ルール

- **1 単元 = 1 ライブラリ** が原則。混ぜるとデザインがバラつく
- 例外: 自作 SVG とライブラリ icon を併用するときは、**自作側を library 側のスタイルに寄せる**(同じ stroke-width、同じ角丸半径、同じ余白)
- アイコンの色は library のデフォルト(currentColor)に依存させず、**`fill="url(#icoNavy)"` 等で本リポの design tokens に揃える**(§9.18 参照)

### 13.4 取り込み方

1. ライブラリの web で対象アイコンを開く
2. 「Copy SVG」または `viewBox` と `path d="..."` をコピー
3. `viewBox="0 0 100 100"`(本リポ標準)に合わせて scaling
4. `fill` / `stroke` を本リポの design token(`url(#icoNavy)`, `#C9A961` 等)に置換
5. `<filter>` で drop-shadow を当てる(§9.17)

### 13.5 自作で揃える場合

ライブラリを使わず自作する場合も、**§9.18 の design system** を厳守:

- 共通 `<defs>`(navy / gold / red の linearGradient + radialGradient bg + filter shadow)
- 役割を色で固定(navy = 主役 / gold = アクセント / red = 対比)
- 同じ stroke-width(line-art の場合は 2-3、面の場合は filter shadow で代替)
- 同じ「枠の使い方」(viewBox 余白の取り方)

canonical 参照: `articles/02-society-and-it/index.html` の 9 法則 SVG(自作だが design system で統一)。

### 13.6 アイコンが「カバーしきれない」概念への対処

学習指導要領の専門概念(「フレーム問題」「Society 5.0」「PPDAC サイクル」など)は、汎用ライブラリにアイコンが無い。その場合は:

1. ライブラリのアイコンを **組み合わせる**(例: Lucide の `cpu` + `infinity` を重ねて「フレーム問題」)
2. ライブラリのアイコンを **下絵**として、本リポの design tokens で補修
3. 完全自作する場合も、ライブラリ風の line-art 言語(stroke 2-3、丸めた角、ミニマル)に揃える

「全部自作するのがしんどい」「ライブラリだけだと足りない」のあいだで、**柔軟に組み合わせて統一感を保つ** のが現実的なスイートスポット。
