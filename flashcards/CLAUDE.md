# flashcards/ — Claude Code 運用指示書(HTML 単一ファイル一問一答)

このフォルダは、**生徒が自分の端末で開いて使う、HTML 単一ファイルの一問一答 / 単語帳**を配置するツール枠です。

`quiz/`(GAS による Google フォーム小テスト作成キット)とは別物。両者の使い分けは:

| 観点 | quiz/(GAS) | **flashcards/(本ツール)** |
|---|---|---|
| 成果物 | Google フォーム(クイズモード) | **HTML 単一ファイル**(GitHub Pages 公開) |
| 利用シーン | 単元テスト・採点・成績集計 | **生徒の自習・通学中の語句確認** |
| 進捗保存 | スプレッドシートに集約 | **localStorage(端末ごと)** |
| データ正本 | `quiz/gas/questions.gs` | **HTML 内の `rawData` JS リテラル** |

---

## 1. 現状

- `index.html` — 情報社会(Society 5.0 周辺、45 問・7 カテゴリ)の一問一答 / 単語帳

将来、別単元の一問一答を追加する場合は、`flashcards/articles/{slug}/index.html` のサブフォルダ構造に切り替え、`flashcards/index.html` をポータル化する。現時点(ツール 1 件)では単一ファイルで運用。

---

## 2. データ構造(`index.html` 内の `<script>` 部)

```js
const categories = [
  { id: 'all', label: 'すべて' },
  { id: 'A', label: '情報と社会' },
  ...
];

const rawData = [
  { id: 1, cat: 'A', diff: 3, q: '...', a: '...' },
  ...
];
```

- `id` — 連番(1 始まり)。途中で詰めると localStorage の習得状態がずれるので、**設問を消す場合も id は再利用しない**(欠番のまま)
- `cat` — カテゴリ ID(`categories` 配列と一致)
- `diff` — 難易度 1〜3。`isFocusMode = true` で `diff >= 2` のみ表示。`diff === 3` は最重要バッジ表示
- `q` / `a` — 問題文と答え

### localStorage キー

```js
const STORAGE_KEY = 'info-society-quiz:v3:mastered';
```

別教材を追加する場合は **教材ごとに別キー**にする(衝突回避)。例: `kanji-quiz:v1:mastered`。

---

## 3. 文章トーン

ルート `CLAUDE.md` の文章トーンを適用。具体的には:

- **設問本文**: 学習ノート / 教科書の記述に準拠した平易な疑問文。「〜を何と呼ぶか。」「〜を何というか。」で統一する
- **答え**: 用語そのもの。注釈は括弧書きで最小限(例: `Society 5.0(超スマート社会)`)
- **キャッチー禁止**: ページ内見出し・ボタン文言で「立体化」「紐解く」「学びのハブ」「深掘り」「凝縮」のたぐいは使わない

設問の正答に迷ったら、独自推論せず `lectures/_source/高校情1学習ノート-解答PDF.pdf` の対応ページを Read で開いて確認(`lectures/CLAUDE.md` §4.8 と同じ原則)。

---

## 4. 動作要件

- 単一 HTML(外部依存は CDN の Tailwind と Google Fonts のみ)。GitHub Pages 配信前提
- localStorage が使える環境(主要モバイルブラウザで動作確認済み)
- キーボード: `/` 検索、`S` シャッフル、`R` リセット、`F` 単語帳、矢印 / Space / `M` / Esc(単語帳モード)
- 単語帳モードはタッチスワイプで前後移動

---

## 5. Git 運用

コミットプレフィックスは `flashcards:` を使う:

```
flashcards: 情報社会 一問一答 45 問を新設
flashcards: 設問 #5 の表現を学習ノート準拠に修正
```

---

## 6. 公開 URL

- `https://mikikof.github.io/mikikof-lab/flashcards/`
