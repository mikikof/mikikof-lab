# mikikof-lab

受験生のための学習ツール集を、一つの屋根の下にまとめたモノレポです。

## 構成

```
mikikof-lab/
├── index.html              ポータルトップ(全ツールへのリンク)
├── CLAUDE.md               Claude Code 運用指示(交通整理役)
├── column/                 ツール01:ビジュアル・エッセイ集
│   ├── index.html
│   ├── CLAUDE.md           コラム制作専用の指示書
│   ├── templates/
│   ├── scripts/
│   └── articles/
│       └── civil-vs-common-law/
├── lectures/               ツール02:授業用インタラクティブHTMLスライド
│   ├── index.html
│   ├── CLAUDE.md           授業サイト制作専用の指示書
│   ├── skills/
│   │   └── interactive-lecture/
│   │       ├── SKILL.md
│   │       ├── template.html
│   │       ├── components.md
│   │       └── examples/
│   └── articles/
│       └── 07-information-security/
└── (将来) quiz/             ツール03:一問一答(未実装)
```

## 公開URL(GitHub Pages)

- ポータル: `https://mikikof.github.io/mikikof-lab/`
- コラム集: `https://mikikof.github.io/mikikof-lab/column/`
- コラム記事: `https://mikikof.github.io/mikikof-lab/column/articles/{slug}/`
- 授業サイト: `https://mikikof.github.io/mikikof-lab/lectures/`
- 授業単元ページ: `https://mikikof.github.io/mikikof-lab/lectures/articles/{slug}/`

## 初回セットアップ

```bash
# 1. このリポジトリをクローン(または git init)
git clone https://github.com/mikikof/mikikof-lab.git
cd mikikof-lab

# 2. スクリプトに実行権限
chmod +x column/scripts/*.sh

# 3. 認証確認
gh auth status
```

GitHub Pages の有効化は、リポジトリの `Settings → Pages → Source: main branch / root` から。

## 新しい記事を作る(コラム集)

```bash
cd column/
bash scripts/new-article.sh "your-slug" "記事タイトル"
# → Claude Code が本文を埋め、scripts/check.sh → scripts/publish.sh の順に実行
```

詳しくは `column/CLAUDE.md` を参照。

## 新しい授業単元を作る(授業サイト)

```bash
cd lectures/
# Claude Code に「第N回 ○○ の授業サイトを作って、学習ノートは添付の通り」と依頼
# → skills/interactive-lecture/SKILL.md に従って articles/{slug}/index.html を生成
```

詳しくは `lectures/CLAUDE.md` を参照。

## 新しいツールを追加する

1. ルート直下に新ツール用のフォルダを作成(例: `quiz/`)
2. そのフォルダ内に `CLAUDE.md`、`index.html`、`templates/`、`scripts/` を配置
3. ルートの `index.html`(ポータル)に新ツールのカードを追加
4. ルートの `CLAUDE.md` の「収容ツール一覧」「判別ルール」に追記

## 設計上の判断

- **モノレポ構造**:複数ツールを一つの屋根にまとめ、共通のポータルから辿れるように
- **ツールごとに完全独立**:他ツールを壊さないよう配下のファイルは自己完結
- **コミットプレフィックス**:`column:`, `quiz:`, `root:` で変更範囲を明示
- **各記事は自己完結**:インライン CSS/JS で書き、将来の共通CSS変更が古い記事を壊さないように
