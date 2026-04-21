# mikikof-lab

受験生のための学習ツール集を、一つの屋根の下にまとめたモノレポです。

## 構成

```
mikikof-lab/
├── index.html              ポータルトップ(全ツールへのリンク)
├── CLAUDE.md               Claude Code 運用指示(交通整理役)
├── essays/                 ツール01:ビジュアル・エッセイ集
│   ├── index.html
│   ├── CLAUDE.md           コラム制作専用の指示書
│   ├── templates/
│   ├── scripts/
│   └── articles/
│       └── civil-vs-common-law/
└── (将来) quiz/             ツール02:一問一答(未実装)
```

## 公開URL(GitHub Pages)

- ポータル: `https://mikikof.github.io/mikikof-lab/`
- コラム集: `https://mikikof.github.io/mikikof-lab/essays/`
- コラム記事: `https://mikikof.github.io/mikikof-lab/essays/articles/{slug}/`

## 初回セットアップ

```bash
# 1. このリポジトリをクローン(または git init)
git clone https://github.com/mikikof/mikikof-lab.git
cd mikikof-lab

# 2. スクリプトに実行権限
chmod +x essays/scripts/*.sh

# 3. 認証確認
gh auth status
```

GitHub Pages の有効化は、リポジトリの `Settings → Pages → Source: main branch / root` から。

## 新しい記事を作る(コラム集)

```bash
cd essays/
bash scripts/new-article.sh "your-slug" "記事タイトル"
# → Claude Code が本文を埋め、scripts/check.sh → scripts/publish.sh の順に実行
```

詳しくは `essays/CLAUDE.md` を参照。

## 新しいツールを追加する

1. ルート直下に新ツール用のフォルダを作成(例: `quiz/`)
2. そのフォルダ内に `CLAUDE.md`、`index.html`、`templates/`、`scripts/` を配置
3. ルートの `index.html`(ポータル)に新ツールのカードを追加
4. ルートの `CLAUDE.md` の「収容ツール一覧」「判別ルール」に追記

## 設計上の判断

- **モノレポ構造**:複数ツールを一つの屋根にまとめ、共通のポータルから辿れるように
- **ツールごとに完全独立**:他ツールを壊さないよう配下のファイルは自己完結
- **コミットプレフィックス**:`essays:`, `quiz:`, `root:` で変更範囲を明示
- **各記事は自己完結**:インライン CSS/JS で書き、将来の共通CSS変更が古い記事を壊さないように
