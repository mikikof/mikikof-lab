# カラーパレット辞典

各記事は `templates/base.html` のデザインをそのまま使用し、**CSS変数の値だけ**を以下のパレットから選んで差し替えます。

差し替える変数は以下:
- `--accent-primary`(大陸法相当・主系統)
- `--accent-primary-deep` / `--accent-primary-bright` / `--accent-primary-pale` / `--accent-primary-wash`
- `--accent-secondary`(英米法相当・対比系統)
- `--accent-secondary-deep` / `--accent-secondary-bright` / `--accent-secondary-pale` / `--accent-secondary-wash`
- `--bg` / `--bg-card` / `--bg-soft` / `--bg-tint`
- `--ink` / `--text` / `--mute`

背景(`--bg`, `--bg-card`, `--bg-soft`, `--bg-tint`, `--ink`系)は**全テーマ共通**で、変更しません。差し替えるのは `--accent-primary*` と `--accent-secondary*` の計10変数のみです。

---

## テーマ1: Indigo × Coral(歴史・政治・法律系)

今回の法サイトの配色。デフォルト。

```css
--accent-primary-deep: #102a56;
--accent-primary: #1e3a8a;
--accent-primary-bright: #2e5cd6;
--accent-primary-pale: #dae6fa;
--accent-primary-wash: #edf2fc;

--accent-secondary-deep: #7a2810;
--accent-secondary: #d9451c;
--accent-secondary-bright: #f2663a;
--accent-secondary-pale: #fde0d0;
--accent-secondary-wash: #fdf0e8;
```

適合題材: 歴史・法律・政治・社会史・制度論

---

## テーマ2: Indigo × Cyan(情報科学・数学・論理系)

クリアで知的な印象。情報科目のデフォルトとして使う。

```css
--accent-primary-deep: #0f1f4d;
--accent-primary: #2746a8;
--accent-primary-bright: #3b6ee0;
--accent-primary-pale: #d6e1f7;
--accent-primary-wash: #ecf1fb;

--accent-secondary-deep: #065563;
--accent-secondary: #0891a8;
--accent-secondary-bright: #22b8cf;
--accent-secondary-pale: #c5ebf2;
--accent-secondary-wash: #e5f6fa;
```

適合題材: アルゴリズム・暗号・AI・数学・論理学・計算理論

---

## テーマ3: Navy × Amber(物理・化学系)

重厚な紺に、理科実験を思わせる琥珀色のアクセント。

```css
--accent-primary-deep: #0b1a3a;
--accent-primary: #1c357a;
--accent-primary-bright: #3357cc;
--accent-primary-pale: #cfdaf2;
--accent-primary-wash: #e8eef8;

--accent-secondary-deep: #6b3d00;
--accent-secondary: #c17900;
--accent-secondary-bright: #e89a1a;
--accent-secondary-pale: #f7e1b3;
--accent-secondary-wash: #faeed1;
```

適合題材: 物理学・化学・地学・エネルギー・素材科学

---

## テーマ4: Forest × Coral(生物・医学・環境系)

深い緑に温度感のあるコーラル。生命科学らしい落ち着きと躍動感。

```css
--accent-primary-deep: #0f3d2e;
--accent-primary: #1f6148;
--accent-primary-bright: #389070;
--accent-primary-pale: #d3e9dc;
--accent-primary-wash: #ebf4ef;

--accent-secondary-deep: #7a2810;
--accent-secondary: #d9451c;
--accent-secondary-bright: #f2663a;
--accent-secondary-pale: #fde0d0;
--accent-secondary-wash: #fdf0e8;
```

適合題材: 生物学・医学・生態系・環境科学・公衆衛生

---

## テーマ5: Charcoal × Gold(経済・ビジネス・金融系)

硬質なチャコールに、金融街の重みを出すゴールドのアクセント。

```css
--accent-primary-deep: #1a1d22;
--accent-primary: #2e343e;
--accent-primary-bright: #545b68;
--accent-primary-pale: #d5d8de;
--accent-primary-wash: #ededef;

--accent-secondary-deep: #6b4f00;
--accent-secondary: #b28a1c;
--accent-secondary-bright: #dbab2b;
--accent-secondary-pale: #f3e3b4;
--accent-secondary-wash: #f8efd3;
```

適合題材: 経済学・金融・マクロ経済・企業史・産業論

---

## テーマ6: Burgundy × Cream(哲学・文学・思想系)

ワインレッドの深みに、教養を感じさせるクリームのやわらぎ。

```css
--accent-primary-deep: #4a0f1e;
--accent-primary: #7a2034;
--accent-primary-bright: #a83c58;
--accent-primary-pale: #ecd1da;
--accent-primary-wash: #f5e6ea;

--accent-secondary-deep: #5c4a20;
--accent-secondary: #a68b3e;
--accent-secondary-bright: #c9a95b;
--accent-secondary-pale: #ecdfb8;
--accent-secondary-wash: #f5edd3;
```

適合題材: 哲学・思想史・文学・言語学・美学

---

## テーマ7: Ocean × Sunset(時事・国際・ジャーナリズム系)

ディープブルーの海にサンセットのオレンジ。世界に向けた眼差し。

```css
--accent-primary-deep: #052c4a;
--accent-primary: #0c4a7c;
--accent-primary-bright: #1e7bbf;
--accent-primary-pale: #c8dcee;
--accent-primary-wash: #e4eff7;

--accent-secondary-deep: #8a2a0a;
--accent-secondary: #e05a1a;
--accent-secondary-bright: #f4833d;
--accent-secondary-pale: #fbd7bf;
--accent-secondary-wash: #fde9db;
```

適合題材: 時事・国際情勢・地政学・ジャーナリズム・現代史

---

## パレットを追加する場合

記事の題材がどの既存パレットにも合わないと判断したときのみ、新パレットを追加してよい。その場合:

1. 新パレット名を決め、上記のフォーマットで本ファイルに追記
2. 背景・テキスト系の変数は**共通のものを流用**。アクセント系10変数のみ定義
3. 追加した理由と、適合する題材ジャンルを併記
4. コミットメッセージに「Add palette: {name}」と明記

---

## 色選びのガイドライン

- `primary`は記事の「基軸」となる対象の色(例: 大陸法、情報科学の中心概念)
- `secondary`は「対比」または「躍動」を担う色(例: 英米法、アクセント・感情)
- 2色のコントラストが明確であること。同系色でまとめるのは避ける
- `pale` と `wash` は、必ずその色相の**最も明るい段階**に揃える。濁らせない
