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
.slide-title, .title-main, .section-heading { font-family: 'Noto Serif JP', serif; }
.eyebrow, .page-indicator { font-family: 'JetBrains Mono', monospace; }
```

#### 書体の使い分けルール

- **Noto Serif JP(明朝)**:「見出し」「スライドタイトル」「定義用語名」「セクション大見出し」「実習の問題文」など、<strong>視線を止めて読む短い要素</strong> に限定。
- **Noto Sans JP(ゴシック)**:本文、解説、事例の長文、タイムラインのセル本文、メニュー項目など、<strong>連続して読む全ての長文</strong>。連続文に明朝を使うとスマホ・低解像度投影で読みづらくなるため禁止。
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

### 9.8 本文に明朝体を使うと読みづらい(特にスマホ)
- **原因**: `font-family: 'Noto Serif JP'` を case-content や dm-cell-head のような連続読み要素に適用していた
- **対策**: 明朝は見出し・用語名・問題文などの短い要素のみに限定。連続文はすべて Noto Sans に(3.2節 書体の使い分けルール参照)

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
- [ ] 本文・連続文にNoto Serif JP(明朝)を使っていない
- [ ] NG表現なし
- [ ] 最新事例が含まれている(該当する場合)
- [ ] examples/ に凍結コピー
- [ ] lectures/index.html の一覧に追加

---

## 11. 参照ファイル

| ファイル | 内容 |
|---|---|
| `template.html` | 空の骨組みHTML(メニュー・リセット・スマホ対応を含む完成済み基盤。コピーして articles/ に配置) |
| `components.md` | 再利用可能パーツカタログ(標準+2026年追加分) |
| `examples/06-information-law.html` | **最新リファレンス**(情報に関する法規)。メニュー・リセット・スマホ対応・リッチインタラクション6種の完全実装例 |
| `examples/07-information-security.html` | 旧リファレンス(情報セキュリティ)。レイアウト確認用 |

新規単元を作るときは必ず `examples/06-information-law.html` を開いて、以下の実装を参照すること:

- インタラクション多数(穴埋め・分類ゲーム・タイムライン比較・シミュレーター)と `onResetHook` の連動
- スマホ時のタイムライン縦積み表示
- SVGの選択ハイライト(pym-tier.selected の金枠+グロー)
- フィッシング風スマホUIのCSS専用実装
- case-expander 内部に quiz を連動させるパターン
- 「県立聖女学院」のような覚え方カード(暗記術)

この単元で確立された新パターンは、今後の単元にも積極的に転用する。
