# 第 4 回 daisu-column / 制約と勾配 — リサーチノート

> 本ファイルは執筆前のリサーチノート(中間)。daisu-column/CLAUDE.md §7「リサーチの徹底ルール」に従ってここに材料を集めてから本文を組み立てる。本文では『大学への数学』『解法の探求』等の東京出版系を一切引用しない(§0-X)。

---

## メタ情報

- **スラグ**: `constraints-and-gradients`
- **タイトル**: 制約と勾配 — Constraints and Gradients
- **副題候補(ヒーローリード冒頭の構造説明)**: 達成点はどこにあるか / 制約付き極値の必要条件
- **英訳サブタイトル**: Constraints and Gradients
- **カテゴリ**: 数学・解析(制約付き最大最小・凸最適化)
- **配色**: Charcoal × Gold(`templates/palettes.md` §テーマ 5、本記事で初使用)
- **公開予定**: 2026-05-23 前後(要 ユーザー確認)
- **位置づけ**: 第 3 回「評価と達成」の正統続編。Weierstrass が「達成は存在する」を保証するのに対し、本稿は「達成点はどこにあるか」を語る

---

## 0. 縦糸の整理(既出 3 本との接続)

| 回 | 大学定理 | 本稿との接続 |
|---|---|---|
| 第 1 回(次元と方程式) | 階数・退化次数定理 | 制約 $g=0$ が 1 本ふえるごとに自由度が 1 落ちる、という幾何の延長線上に Lagrange の方法がある |
| 第 2 回(包絡線と特異解) | ディスクリミナント集合 | 「等高線が制約に接する」幾何は、第 2 回の「メンバー曲線が共通の接線を持つ」と双対的に対比できる |
| 第 3 回(評価と達成) | Weierstrass 最大値定理 / Heine-Borel | コンパクト集合上の連続関数が最大値を達成することは保証された。**ではその達成点はどこにあるのか**、を引き継ぐ |

第 3 回末尾の補章で「線形計画の双対性、関数空間のコンパクト性」を予告済み。本稿の §6 双対の風景がその回収にあたる。

---

## 1. 中心テーゼ(章 02 末で掲げる)

> 制約 $g(x, y) = 0$ のもとで $f(x, y)$ の最大点に立ったとき、目的関数の等高線は制約曲線にぴたりと接する。
> 言いかえれば、**最大点では $\nabla f$ と $\nabla g$ が平行になる**。

## 2. 大学定理への翻訳一行(§1-6 必須)

> この一行は、解析の言葉では **ラグランジュ未定乗数法 (method of Lagrange multipliers)** に当たる。$n$ 変数の関数 $f$ を等式制約 $g_1 = \cdots = g_m = 0$ のもとで極値化するとき、極値点 $x^*$ では実数 $\lambda_1, \ldots, \lambda_m$ が存在して
> $$\nabla f(x^*) = \lambda_1 \nabla g_1(x^*) + \cdots + \lambda_m \nabla g_m(x^*)$$
> が成り立つ(制約集合が正則な場合)。$\lambda_i$ を **ラグランジュ未定乗数** と呼ぶ。

---

## 3. 大学定理の精密ステートメント

### 3-1. ラグランジュ未定乗数法(等式制約版)

**ステートメント**:
$U \subseteq \mathbb{R}^n$ を開集合、$g: U \to \mathbb{R}^m$ を $C^1$ 写像、$M = g^{-1}(0)$ とする。$x^* \in M$ で $\mathrm{rank}\, Dg(x^*) = m$ と仮定する(制約の正則性、constraint qualification, LICQ)。$f: U \to \mathbb{R}$ が $C^1$ で、$x^*$ が $f|_M$ の局所極値点であれば、$\lambda \in \mathbb{R}^m$ が存在して
$$\nabla f(x^*) = Dg(x^*)^\top \lambda = \sum_{i=1}^m \lambda_i \nabla g_i(x^*)$$
が成り立つ。

**幾何的意味**: $\nabla f(x^*)$ は制約多様体 $M$ の $x^*$ における **法空間** $N_{x^*} M$ に属する。

**証明スケッチ**(陰関数定理経由):
1. $x^*$ の近傍で陰関数定理により $M$ は $n - m$ 次元の滑らかな部分多様体
2. 接空間 $T_{x^*} M = \ker Dg(x^*)$
3. $x^*$ が $f|_M$ の極値点 $\Rightarrow$ 任意の接ベクトル $v \in T_{x^*} M$ について $df(x^*)(v) = 0$
4. つまり $\nabla f(x^*) \perp T_{x^*} M$、すなわち $\nabla f(x^*) \in (T_{x^*} M)^\perp = N_{x^*} M = \mathrm{span}\{\nabla g_i(x^*)\}_{i=1}^m$

### 3-2. ラグランジュ関数(Lagrangian)

定義: $L(x, \lambda) = f(x) - \sum_{i=1}^m \lambda_i g_i(x)$

すると未定乗数の条件は **$\nabla_x L = 0$** に集約される。$\nabla_\lambda L = -g(x) = 0$ で制約も自動的に組み込まれる。これにより、制約付き極値問題は無制約の鞍点問題へと変換される。

### 3-3. KKT 条件(Karush-Kuhn-Tucker, 不等式制約版)

**問題**: 制約 $g_i(x) \le 0$ ($i = 1, \ldots, m$), $h_j(x) = 0$ ($j = 1, \ldots, k$) のもとで $f(x)$ を最小化。

**ステートメント**:
$x^*$ が局所最小点で、適切な制約資格(LICQ, MFCQ, Slater のいずれか)を満たすなら、$\lambda \in \mathbb{R}^m$, $\mu \in \mathbb{R}^k$ が存在して次の 4 つが成り立つ:

1. **Stationarity(定常性)**:
   $\nabla f(x^*) + \sum_i \lambda_i \nabla g_i(x^*) + \sum_j \mu_j \nabla h_j(x^*) = 0$
2. **Primal feasibility(主実行可能性)**:
   $g_i(x^*) \le 0, \quad h_j(x^*) = 0$
3. **Dual feasibility(双対実行可能性)**:
   $\lambda_i \ge 0$
4. **Complementary slackness(補集合性)**:
   $\lambda_i g_i(x^*) = 0$ for all $i$

**補集合性の意味**: アクティブでない制約 ($g_i(x^*) < 0$) では乗数 $\lambda_i = 0$。アクティブな制約 ($g_i(x^*) = 0$) でのみ乗数が非ゼロになりうる。

**歴史**: 公表は Kuhn-Tucker 1951(*Proceedings of 2nd Berkeley Symposium*)。同じ条件を独立に導いた Karush 1939(Univ. Chicago 修士論文、長年未公刊)が遡る形になり、後年 KKT と並べて呼ばれるようになった。

### 3-4. 双対定理(線形計画)

**主問題 (P)**: $\max c^\top x$ subject to $A x \le b, \ x \ge 0$
**双対問題 (D)**: $\min b^\top y$ subject to $A^\top y \ge c, \ y \ge 0$

**弱双対性 (weak duality)**: $x$ が (P) 実行可能、$y$ が (D) 実行可能なら $c^\top x \le b^\top y$。

**強双対性 (strong duality)**: (P) または (D) が有界な最適解を持つとき、最適値は一致する($c^\top x^* = b^\top y^*$)。

非線形・凸の場合は Slater 条件のもとで Lagrange 双対と主の最適値が一致(零双対ギャップ)。

### 3-5. von Neumann のミニマックス定理(1928)

$X \subseteq \mathbb{R}^n$, $Y \subseteq \mathbb{R}^m$ を空でない有界閉凸集合、$K: X \times Y \to \mathbb{R}$ が連続で $y$ を固定したとき $x$ について凹、$x$ を固定したとき $y$ について凸(saddle 性質)とする。このとき
$$\max_{x \in X} \min_{y \in Y} K(x, y) = \min_{y \in Y} \max_{x \in X} K(x, y).$$

この共通値は **鞍点値**。2 人零和ゲームの混合戦略均衡が常に存在することを意味する。

---

## 4. 数学的正確性で慎重に書くべき点(CLAUDE.md §6 と並ぶ本稿固有の注意)

- [ ] 「等式制約 1 本ふえると次元 1 下がる」は **rank が満ちている** ときの話(§6-2 等式 vs 不等式)
- [ ] LICQ(線形独立性)が破れる例: $g_1 = x^2 + y^2 - 1$, $g_2 = x - 1$ の交点 $(1, 0)$ では $\nabla g_1 = (2, 0), \nabla g_2 = (1, 0)$ で平行 → ラグランジュ条件が極値点を捕捉できない
- [ ] KKT は **必要条件**。十分条件にするには凸性または 2 階条件(SOSC)が要る
- [ ] 制約資格を持たない例(尖った制約)では KKT が破綻 → Fritz John 条件(乗数 $\lambda_0 \ge 0$ を $f$ にもつける弱版)を補章で軽く触れてよい
- [ ] 「ラグランジュ乗数 = shadow price(影の価格)」は **強双対性が成り立つときの感度解釈**($\lambda = \partial f^* / \partial b$)、無条件ではない
- [ ] von Neumann ミニマックスは **凸性必須**。非凸では成立しない反例(2 × 2 の混合戦略未許可ゲーム等)
- [ ] LP の弱双対は無条件、強双対は **基底解の存在** に依存(退化を含む扱いに注意)

---

## 5. 入試問題候補(出典確定はリサーチ段階で詰める)

> 大学名・年度・前期/後期/文系/理系・第何問 まで正確に。**取り違えは codex audit-review で必ず指摘されるので執筆時に確実にする**(CLAUDE.md §7-6)。

### 第一級候補(精査して採用)

1. **京都大学 2014 年 文系 第 4 問** — 三角形の周長一定下での面積最大化(ヘロンの公式と相加相乗)。要出典確認
2. **東京大学 2003 年 理科 第 4 問** — 楕円と直線の接触条件。要出典確認
3. **東京工業大学 2018 年 第 4 問** — 楕円に内接する四角形の面積最大化。要出典確認
4. **一橋大学 2012 年 第 1 問** — 共通テスト型線形計画の発展版(複数制約の最大値問題)。要出典確認
5. **京都大学 2008 年 理系 第 5 問** — 球面上の三角形の最大面積。要出典確認

### 第二級候補(代替案)

6. **東北大学 2015 年 前期 理系** — 半径一定の円柱に内接する直方体の体積最大化
7. **大阪大学 2009 年 後期 理系** — $x^2 + y^2 = 1$ 上で $x + y + xy$ の最大値
8. **名古屋大学 2017 年 前期 理系** — Cauchy-Schwarz 不等式の等号成立位置

### 採用基準

- 制約が **等式 1 本** で済む(章 04 KKT の前に置く)
- 受験生が **相加相乗・コーシーシュワルツ・微分** の標準解法で解ける(本音併走の解説で「ラグランジュなら一行」を示す)
- 図にしやすい(2D 平面で等高線と制約曲線が引ける)

### リサーチ手順

```bash
# 京大の年度別過去問 PDF(京大数理解析の公開)で検索
# 駿台・河合塾・東進の年度別過去問 DB(web search で実題ヒット確認)
# 「2014 京大 文系 第 4 問」型クエリで検索 → 数値確認
```

問題文の数値・条件・問題番号は **最低 2 出典でクロスチェック**。1 つは大学の公式公開、もう 1 つは予備校の解答公開。

---

## 6. 章構成(7 章モデル)

```
ヒーロー
  - タイトル「制約と勾配」
  - リード文 3 行
    1. 第 3 回(評価と達成)で最大値の「存在」は保証された。
    2. 本稿は最大点が「どこにあるか」を語る、Weierstrass の続編。
    3. 受験の典型問題から出発し、ラグランジュ未定乗数法・KKT・双対・SVM までを一直線でつなぐ。

01. 受験での顔                  — Where We Already Met Constraints
    └─ 領域内最大最小、共通テスト線形計画、相加相乗の等号成立位置
02. 受験での解き直し             — Re-Solving with Level Sets and Gradients
    └─ 等高線と接触、勾配の向き、円と直線の接触条件
    └─ 章末: 中心テーゼ「∇f ∥ ∇g」+ ラグランジュ未定乗数法への翻訳一行
03. 大学からの読み返し           — Lagrange Multipliers
    └─ 法空間としての勾配、Lagrangian、陰関数定理経由の証明スケッチ
04. 不等式制約への拡張           — The KKT Conditions
    └─ アクティブ集合、補集合性の幾何、Karush 1939 と Kuhn-Tucker 1951
05. 入試問題で確かめる           — Verification on Entrance Exams
    └─ 京大 2014 文・東大 2003 理 等の 2〜3 題を Lagrange/標準解法で並行解説
06. 双対の風景                   — Duality
    └─ 線形計画双対(弱・強)、Lagrange 双対関数、Slater 条件、影の価格
07. 補章 ─ 応用の場面集          — Applications of the Multipliers
    7-1. サポートベクターマシン   — Margin Maximization
    7-2. 効用最大化と限界代替率   — Marginal Rate of Substitution
    7-3. ミニマックスとゲーム理論 — von Neumann 1928
    7-4. 等周不等式               — Isoperimetric Inequality
         (変分法の入口、Euler-Lagrange の制約付き版)

参考文献
フッター
```

**章末の翻訳一行(§1-6)**は章 02 必須。章 03 のリードでラグランジュ未定乗数法を主役に据えて精密化する。

---

## 7. 補章 7-1 ─ サポートベクターマシン(SVM)の詳細

線形分離可能な訓練データ $\{(x_i, y_i)\}_{i=1}^N$ ($y_i \in \{-1, +1\}$) に対し、**マージン(分離超平面と最近接点の距離)を最大化** する超平面 $w^\top x + b = 0$ を求める問題:

$$\min_{w, b} \tfrac{1}{2} \|w\|^2 \quad \text{s.t.} \quad y_i(w^\top x_i + b) \ge 1 \quad (i = 1, \ldots, N).$$

KKT 条件を適用すると、各制約に対応する乗数 $\alpha_i \ge 0$ が存在し、補集合性

$$\alpha_i\bigl[y_i(w^\top x_i + b) - 1\bigr] = 0$$

から **$\alpha_i > 0$ となる点 $x_i$ はマージン上にある(サポートベクター)**。$\alpha_i = 0$ となる点は分離超平面の決定に寄与しない。

定常性条件 $w = \sum_i \alpha_i y_i x_i$ により、最適超平面の法線ベクトル $w$ はサポートベクターの線形結合で表される。**「決め手は境界線上の少数の点のみ」** という SVM の核心が、KKT の補集合性から純粋に幾何的に出る。

(daisu-column では機械学習用語を多用しないが、「サポートベクター」「マージン」は標準術語として OK)

---

## 8. 補章 7-2 ─ 効用最大化(経済学)

消費者が 2 財 $(x, y)$ を価格 $(p, q)$ で買い、所得 $m$ のもとで効用 $U(x, y)$ を最大化:

$$\max U(x, y) \quad \text{s.t.} \quad p x + q y = m.$$

Lagrange 条件 $\nabla U = \lambda \nabla(px + qy - m)$ から
$$\frac{\partial U/\partial x}{\partial U/\partial y} = \frac{p}{q}.$$

左辺は **限界代替率 (marginal rate of substitution, MRS)**、右辺は価格比。「最適消費点では MRS = 価格比」が経済学の標準テーゼだが、その正体は単なる Lagrange 条件である。

さらに、ラグランジュ乗数 $\lambda = \partial U^* / \partial m$ は **所得の限界効用(shadow price)**。所得を 1 円増やしたとき効用が $\lambda$ だけ増える、という経済学的解釈が双対性から出る。

---

## 9. 補章 7-3 ─ von Neumann のミニマックス(1928)

2 人零和ゲームで、プレイヤー I が混合戦略 $p \in \Delta_n$(単体)、II が $q \in \Delta_m$ を選ぶ。利得行列 $A$ について期待利得は $K(p, q) = p^\top A q$。

I は $\max_p \min_q K$、II は $\min_q \max_p K$ を目指す。von Neumann 1928 はこの 2 つが一致することを示した:
$$\max_p \min_q p^\top A q = \min_q \max_p p^\top A q.$$

**証明の核心**: $\Delta_n$, $\Delta_m$ が有界閉凸、$K$ が saddle 性質(両側で線形 = 凹かつ凸)を持つから。これは Lagrange 双対の幾何そのもの — 主問題と双対問題の値が一致する条件。

経済学・統計学・機械学習(GAN, adversarial training)に再三登場する原型。

---

## 10. 補章 7-4 ─ 等周不等式と変分法

**等周問題**: 周長 $L$ が一定の閉曲線で囲まれる面積を最大化する曲線は何か?
**答え**: 円(面積は $L^2 / (4\pi)$)。

これは関数空間上の制約付き極値問題。曲線を $\gamma: [0, 1] \to \mathbb{R}^2$ とパラメータ表示すれば、

$$\max \int_0^1 \tfrac{1}{2}(x \dot y - y \dot x) \, dt \quad \text{s.t.} \quad \int_0^1 \sqrt{\dot x^2 + \dot y^2} \, dt = L.$$

Lagrange の方法を **関数空間** に拡張すると、Euler-Lagrange 方程式の制約付き版が出る。曲率一定 $\kappa = 1/R$($R = L/(2\pi)$)の曲線、すなわち円が解。

これは Lagrange の方法が **有限次元最適化** から **変分問題** へ自然に拡張される姿の最古の例(Bernoulli, Euler 18 世紀)。「Lagrange の方法は変分法と地続きである」という構造の予告。

---

## 11. 図の方針(daisu-column §4 三方式に従う)

| 章 | 図 | 方式 | 内容 |
|---|---|---|---|
| 01 | Diagram 01 | 凡例方式 | 共通テスト型線形計画(三角領域 + 等高線) |
| 02 | Diagram 02 | 凡例方式 | 円 $x^2+y^2=1$ 上の $x+y$ 最大化(等高線が接する瞬間) |
| 02 | Diagram 03 | stack 方式 | 等高線が制約曲線に近づいて接触する 3 段階 |
| 03 | Diagram 04 | 凡例方式 | 法空間 $N_{x^*}M$ と $\nabla f, \nabla g$ の位置関係 |
| 03 | Diagram 05 | 凡例方式 | Lagrangian の鞍点幾何(凸 × 凹) |
| 04 | Diagram 06 | 凡例方式 | KKT の補集合性(アクティブ制約とアクティブでない制約) |
| 05 | Diagram 07-08 | 凡例方式 | 入試題の図示(2 題分) |
| 06 | Diagram 09 | 凡例方式 | LP 双対の頂点と影の価格 |
| 06 | Diagram 10 | stack 方式 | 主問題 → Lagrange 緩和 → 双対の三段 |
| 07-1 | Diagram 11 | 凡例方式 | SVM のマージン + サポートベクター |
| 07-3 | Diagram 12 | 凡例方式(または stack) | ミニマックス点の幾何(凸 × 凹の鞍点) |

合計 11〜12 図。第 1 回(11 図)第 2 回(10 図)第 3 回(13 図?要確認)の系列内。

---

## 12. 配色 — Charcoal × Gold

`templates/palettes.md` §テーマ 5(経済・ビジネス・金融系)を初使用。

- `--accent-primary` 灰青系 → 等高線・制約曲線・最適化の硬質さ
- `--accent-secondary` 金 → 勾配ベクトル・極値点・サポートベクター・乗数 $\lambda$ の存在

「最適化と双対性」という主題に金融配色が意味的に適合する(本稿の補章で経済学・SVM が出る)。

---

## 13. 参考文献候補(東京出版系は除外)

### 一次・二次資料(数学)
- 杉浦光夫『解析入門 I, II』東京大学出版会、1980
- 齋藤正彦『線型代数入門』東京大学出版会、1966
- 小平邦彦『解析入門 I, II』岩波書店、1976
- 松本幸夫『多様体の基礎』東京大学出版会、1988(陰関数定理・部分多様体)

### 最適化・凸解析
- Boyd, S. & Vandenberghe, L. *Convex Optimization*, Cambridge UP, 2004
- Bertsekas, D. *Nonlinear Programming*, 3rd ed., Athena Scientific, 2016
- Rockafellar, R. T. *Convex Analysis*, Princeton UP, 1970
- Luenberger, D. & Ye, Y. *Linear and Nonlinear Programming*, 4th ed., Springer, 2016

### 一次資料(原典)
- Lagrange, J. L. *Mécanique Analytique*, 1788
- Karush, W. "Minima of Functions of Several Variables with Inequalities as Side Conditions", MS Thesis, Univ. Chicago, 1939
- Kuhn, H. W. & Tucker, A. W. "Nonlinear Programming", *Proc. 2nd Berkeley Symp. on Math. Stat. and Probab.*, 1951
- von Neumann, J. "Zur Theorie der Gesellschaftsspiele", *Mathematische Annalen* 100, 1928

### 応用(機械学習・経済学)
- Vapnik, V. *The Nature of Statistical Learning Theory*, Springer, 1995(SVM)
- Mas-Colell, A., Whinston, M. D. & Green, J. R. *Microeconomic Theory*, Oxford UP, 1995(効用最大化)

### 入試問題(出典確定後に追加)
- 各大学の年度別過去問(公式公開分・予備校解答公開分)

---

## 14. 章 02 末「翻訳一行」の精度確認

§1-6 の三段(テーゼ → 定理名 → 定理の精密内容)を踏まえた書き方:

> 制約 $g(x, y) = 0$ のもとで $f(x, y)$ の極値点を $x^*$ とする。すると、最大点・最小点では目的関数の等高線が制約曲線に接する。すなわち $\nabla f(x^*) \parallel \nabla g(x^*)$。この一行は、解析の言葉では **ラグランジュ未定乗数法 (method of Lagrange multipliers)** に当たる。$n$ 変数の関数 $f$ を等式制約 $g_1 = \cdots = g_m = 0$ のもとで極値化するとき、制約集合が正則な極値点では $\lambda_1, \ldots, \lambda_m \in \mathbb{R}$ が存在して
> $$\nabla f = \lambda_1 \nabla g_1 + \cdots + \lambda_m \nabla g_m$$
> が成り立つ、というものである。

「$\nabla f \parallel \nabla g$」(直感) → 「ラグランジュ未定乗数法」(定理名) → 「$\nabla f = \sum \lambda_i \nabla g_i$」(精密内容)の三段が明確に通る。

---

## 15. 公開前のタスクリスト

- [ ] 入試問題 5 題の出典確定(大学名・年度・前期/後期・第何問)
- [ ] 各定理の精密ステートメント検証(特に制約資格の言い回し)
- [ ] LICQ が破れる例の単純な反例構成
- [ ] 図 11〜12 個の構成案(凡例 SVG + 凡例 HTML)
- [ ] `base.html` から `articles/constraints-and-gradients/index.html` をコピー
- [ ] 配色 CSS 変数を Charcoal × Gold へ差し替え
- [ ] §10 公開前チェックリスト(自誌引用 0 件、§6 11 項目、SVG 内 KaTeX 0 件、Unicode subscript 0 件)
- [ ] `/audit-review -p review-paper` で codex レビュー → キュレーション → 修正適用
- [ ] 修正 5 件以上なら再 audit(memory: audit 再起動が有効)
- [ ] daisu-column/index.html のカードリストに新カード追加
- [ ] commit & push: `daisu-column: 第 4 回「制約と勾配」を公開`

---

## 16. 想定 audit 指摘の事前防衛(本稿固有)

第 1〜3 回の audit 履歴から類推して、本稿で指摘されそうな致命級を事前に潰す。

| 想定指摘 | 事前対策 |
|---|---|
| 「ラグランジュ条件は必要条件であって十分条件でない」明示の不足 | §3-1 の冒頭 + 章 03 本文で必ず断る |
| 「制約資格(LICQ/MFCQ/Slater)の言及なし」 | §3-1 と §3-3 で簡潔に触れる(高校生に過剰負荷にならない範囲) |
| 「乗数の符号(KKT で $\lambda_i \ge 0$)の理由不明」 | §3-3 の dual feasibility で「不等式制約を緩めるほど最適値が改善する → 価値の符号が一意」と幾何説明 |
| 「Karush の優先権について Kuhn-Tucker の単独命名は誤解を招く」 | §3-3 歴史節で Karush 1939 を明記 |
| 「von Neumann 1928 の論文の原タイトルとジャーナル」 | §13 で *Math. Ann.* 100 と正確に |
| 「等周問題の解の一意性は別問題」 | §10 で「曲率一定 → 円」とし、一意性証明には Wirtinger inequality 等が必要、と一言 |
| 「効用最大化で凹効用関数の前提が暗黙になっている」 | §8 で「$U$ が凹で内点解の場合」と明記 |

---

## 17. 本稿の hidden message(著者の本音)

> 受験で「制約付き最大最小」は微分・置換・相加相乗の組合せ問題に見えるが、その背後には常に同じ 1 つの幾何 — **目的関数の等高線が制約に接する瞬間** — がある。Lagrange 未定乗数法はその幾何の代数的表現であり、KKT・双対・SVM・経済学・ゲーム理論はすべて同じ枝の上の葉である。受験で 30 通り暗記する代わりに、この 1 つの幾何を持っておけば、大学以降の数学・経済学・機械学習の最適化の風景がすべてここから始まる。

本文では直接書かない(自誇張・標語を避ける)が、章構成・節分割・例の選び方でこの hidden message が読者に届く形にする。
