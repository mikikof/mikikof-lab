# -*- coding: utf-8 -*-
"""
02-07「デジタル化された情報とその表し方」ビルダー
- ベース = 02-06 を cp した index.html(self 型のCSS/JS内蔵)
- エンジン(<head>/CSS/<script>)は保全し、<main> 本文と JS データ配列のみ差し替える
- 原本: ベストフィット 2章07(類題54-61 + 練習62-67)/ 図 fig1(文字コード表) fig2(16x16グリッド) fig3/4(筆算)
"""
import re, pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "index.html"
html = SRC.read_text(encoding="utf-8")

# ============================================================
# ヘルパー
# ============================================================
def self_row(sub, q, model_html):
    return f'''        <div class="self-row" data-sub="{sub}">
          <div class="self-q"><span class="self-sub-label">{q[0]}</span>{q[1]}</div>
          <textarea class="self-input" rows="2" placeholder="自分の答え・式を書いてみてください(任意)"></textarea>
          <button type="button" class="self-reveal" data-action="self-reveal">模範解答を見る</button>
          <div class="self-model">
            <div class="self-model-label">模範解答</div>
            {model_html}
            <div class="self-rate">
              <span class="self-rate-q">模範解答と照らして:</span>
              <button type="button" class="self-rate-btn ok" data-mark="ok">解けた ○</button>
              <button type="button" class="self-rate-btn no" data-mark="no">まだ △</button>
            </div>
          </div>
        </div>'''

def stage_self(probid, qnum, idx, total, src, kakko, title, lead_html, rows_html, fb_html):
    # 図/引用ブロックは <p> の外へ分離(p 内に figure/blockquote を入れない = HTML妥当性)
    block = ""
    mm = re.search(r'<figure|<blockquote', lead_html)
    if mm:
        i = mm.start()
        block = "\n      " + lead_html[i:]
        lead_html = lead_html[:i].rstrip()
    return f'''  <section class="stage" data-stage-name="練習 {qnum}" data-prob-id="{probid}">
    <div class="problem-meta">
      <span class="problem-tag practice">PRACTICE {idx} / {total}</span>
      <span class="problem-tag self">記述・自己採点</span>
      <span class="problem-source">ベストフィット {src}</span>
    </div>
    <div class="problem-q-num"><span class="q">Q</span>{qnum}</div>
    <h3 class="problem-title">{kakko}{title}</h3>
    <div class="problem-card">
      <p class="problem-q lead">{lead_html}</p>{block}
      <div class="self-list" data-input="self">
{rows_html}
      </div>
      <div class="actions-inline">
        <button class="btn-grade" data-action="grade">自己採点する <span class="arrow">→</span></button>
      </div>
{fb_html}
    </div>
  </section>'''

def stage_multi(probid, qnum, idx, total, src, kakko, title, lead_html, opts, correct, fb_html):
    # opts: list of (letter, text); correct: list of indices
    o = "\n".join(
        f'        <label class="opt"><input type="checkbox"><span class="opt-mark checkbox"></span>'
        f'<span class="opt-text"><span class="opt-letter">{l}</span>{t}</span></label>'
        for (l, t) in opts)
    return f'''  <section class="stage" data-stage-name="練習 {qnum}" data-prob-id="{probid}">
    <div class="problem-meta">
      <span class="problem-tag practice">PRACTICE {idx} / {total}</span>
      <span class="problem-tag multi">MULTI</span>
      <span class="problem-source">ベストフィット {src}</span>
    </div>
    <div class="problem-q-num"><span class="q">Q</span>{qnum}</div>
    <h3 class="problem-title">{kakko}{title}</h3>
    <div class="problem-card">
      <p class="problem-q lead">{lead_html}</p>
      <div class="multi-hint">複数選択 — 該当するものすべて</div>
      <div class="opts" data-input="multi" data-correct="{','.join(map(str,correct))}">
{o}
      </div>
      <div class="actions-inline">
        <button class="btn-grade" data-action="grade">採点する <span class="arrow">→</span></button>
      </div>
{fb_html}
    </div>
  </section>'''

def fb(banner_label, body_html, score_tag=True):
    st = '<span class="score-tag"></span>' if score_tag else ''
    return f'''      <div class="feedback" data-feedback>
        <div class="fb-banner ok"><span class="icon">✓</span><span>{banner_label}</span>{st}</div>
        <div class="fb-body">
{body_html}
        </div>
      </div>'''

def sec(title, inner):
    return f'''          <div class="fb-section">
            <div class="fb-section-title">{title}</div>
            <div class="fb-explain">{inner}</div>
          </div>'''

def correct_line(text):
    return f'''          <div class="fb-section">
            <div class="fb-section-title">正答</div>
            <div class="fb-correct-line">{text}</div>
          </div>'''

# 図 figure(問題文 lead 下に独立配置)
def fig_box(src, alt, cap, maxw=360, imgw=320):
    return (f'<figure style="margin: 0.8rem auto; padding: 0.8rem 1rem; background: var(--bg-card); '
            f'border: 1px solid var(--line); border-radius: 8px; display: block; max-width: {maxw}px; text-align: center;">'
            f'<img src="assets/{src}" alt="{alt}" style="display: block; width: 100%; height: auto; max-width: {imgw}px; margin: 0 auto;">'
            f'<figcaption style="margin-top: 0.5rem; font-family: var(--f-mono); font-size: 0.74rem; color: var(--ink-mute);">{cap}</figcaption>'
            f'</figure>')

# 数式・内訳の簡易ボックス viz
def calc_viz(label, caption, rows_html):
    return f'''          <div class="viz">
            <span class="viz-label">{label}</span>
            <div class="viz-caption">{caption}</div>
            {rows_html}
          </div>'''

# ============================================================
# SVG ビジュアル(brushup/visual)
# tokens: action#4A78C8 anchor#122E55 ok#41A38C gold#D4A852 ink#1A2B47
#         ink-soft#475673 ink-mute#75839B line#D8E2EE line-strong#B8C5D7
# ============================================================
import math
def svg_map():
    media = [
        ("数値", "2進数に変換", "#4A78C8"),
        ("文字", "文字コード", "#2E5894"),
        ("音", "標本化→量子化→符号化", "#41A38C"),
        ("画像", "画素 × 階調(RGB)", "#A37A1F"),
        ("動画", "静止画 × フレーム", "#C84A60"),
    ]
    lanes = ""
    y0, dy = 44, 60
    for i, (m, meth, col) in enumerate(media):
        y = y0 + i * dy
        cy = y + 22
        lanes += f'''
      <line x1="170" y1="{cy}" x2="250" y2="{cy}" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="556" y1="{cy}" x2="636" y2="{cy}" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="92" y="{y}" width="78" height="44" rx="10" fill="{col}"/>
      <text x="131" y="{cy+6}" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="19" font-weight="700" fill="#FFFFFF">{m}</text>
      <rect x="250" y="{y}" width="306" height="44" rx="10" fill="#FAFCFF" stroke="{col}" stroke-width="1.5"/>
      <text x="403" y="{cy+6}" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="16" font-weight="500" fill="#1A2B47">{meth}</text>'''
    ytop, ybot = y0 + 22, y0 + 4 * dy + 22
    return f'''        <div class="viz">
          <span class="viz-label">THE BIG MAP — 0と1への変換</span>
          <div class="viz-caption">どんな情報も、種類ごとの方法で変換され、最後はみな0と1の並びになる。</div>
          <div class="family-tree-wrap">
            <svg class="family-tree-svg" viewBox="0 0 720 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="数値・文字・音・画像・動画が、それぞれの方法でデジタル化され0と1の並びになる地図">
      <line x1="46" y1="{ytop}" x2="46" y2="{ybot}" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="46" y1="{ytop}" x2="92" y2="{ytop}" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="46" y1="{ybot}" x2="92" y2="{ybot}" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="2" y="160" width="44" height="44" rx="10" fill="#122E55"/>
      <text x="24" y="177" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">情報</text>
      <text x="24" y="192" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">の源</text>
      {lanes}
      <line x1="636" y1="{ytop}" x2="636" y2="{ybot}" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="636" y="158" width="80" height="48" rx="12" fill="#1A2B47"/>
      <text x="676" y="181" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="20" font-weight="700" fill="#D4A852">0 1</text>
      <text x="676" y="197" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" font-weight="500" fill="#E8F0F9">デジタル</text>
            </svg>
          </div>
        </div>'''

def svg_sampling():
    x0, x1 = 48, 556
    ytop, ybot = 28, 206
    n = 9
    pts = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        v = 3.5 + 3.2 * math.sin(i / (n - 1) * math.pi * 1.6 + 0.4)
        v = max(0.2, min(7.0, v))
        y = ybot - (ybot - ytop) * v / 7.0
        q = round(v)
        yq = ybot - (ybot - ytop) * q / 7.0
        pts.append((x, y, yq, q))
    fine = []
    for k in range(0, 121):
        t = k / 120.0
        ii = t * (n - 1)
        v = 3.5 + 3.2 * math.sin(ii / (n - 1) * math.pi * 1.6 + 0.4)
        v = max(0.2, min(7.0, v))
        x = x0 + (x1 - x0) * t
        y = ybot - (ybot - ytop) * v / 7.0
        fine.append(f"{x:.1f},{y:.1f}")
    wave = "M " + " L ".join(fine)
    grid = ""
    for l in range(8):
        gy = ybot - (ybot - ytop) * l / 7.0
        grid += f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="#E8EFF7" stroke-width="1"/>'
        grid += f'<text x="{x0-8}" y="{gy+4:.1f}" text-anchor="end" font-family="monospace" font-size="11" fill="#75839B">{l}</text>'
    verts = dots = qdots = ""
    for (x, y, yq, q) in pts:
        verts += f'<line x1="{x:.1f}" y1="{ytop}" x2="{x:.1f}" y2="{ybot}" stroke="#DAE6F5" stroke-width="1"/>'
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#4A78C8"/>'
        qdots += f'<rect x="{x-4.5:.1f}" y="{yq-4.5:.1f}" width="9" height="9" rx="2" fill="#41A38C"/>'
    return f'''        <div class="viz">
          <span class="viz-label">SAMPLING &amp; QUANTIZATION — 波形のデジタル化</span>
          <div class="viz-caption">縦線の間隔が標本化周期。曲線上の●を最も近い段階値(■)に丸めるのが量子化。</div>
          <div class="viz-svg-wrap">
            <svg class="viz-svg wide" viewBox="0 0 600 248" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="アナログ波形を一定間隔で標本化し、各標本点を8段階の最も近い値へ量子化する図">
      {grid}
      {verts}
      <path d="{wave}" fill="none" stroke="#C84A60" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>
      {qdots}
      {dots}
      <text x="48" y="230" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="500" fill="#475673">時間 →</text>
      <circle cx="356" cy="226" r="4.5" fill="#4A78C8"/><text x="368" y="230" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" fill="#475673">標本点(取り出した値)</text>
      <rect x="500" y="221.5" width="9" height="9" rx="2" fill="#41A38C"/><text x="514" y="230" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" fill="#475673">量子化後</text>
            </svg>
          </div>
        </div>'''

def svg_filmstrip():
    """Q60: 動画=静止画×フレームレート(フィルムストリップ)"""
    frames = ""
    for i in range(6):
        x = 60 + i * 78
        frames += f'<rect x="{x}" y="60" width="62" height="78" rx="5" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>'
        frames += f'<rect x="{x+10}" y="74" width="42" height="34" rx="3" fill="#DAE6F5"/>'
        frames += f'<circle cx="{x+22}" cy="118" r="3" fill="#75839B"/><circle cx="{x+40}" cy="118" r="3" fill="#75839B"/>'
    # 上下のパーフォレーション
    perf = ""
    for i in range(13):
        px = 56 + i * 38
        perf += f'<rect x="{px}" y="46" width="14" height="8" rx="2" fill="#B8C5D7"/>'
        perf += f'<rect x="{px}" y="146" width="14" height="8" rx="2" fill="#B8C5D7"/>'
    return f'''          <div class="viz">
            <span class="viz-label">FRAMES PER SECOND — 動画は静止画の連続</span>
            <div class="viz-caption">1秒間に流す静止画(フレーム)の枚数がフレームレート[fps]。フレーム数 = フレームレート × 時間。</div>
            <div class="viz-svg-wrap">
              <svg class="viz-svg wide" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="フィルムのように並ぶ6枚の静止画フレーム。1秒あたりの枚数がフレームレート">
        <rect x="44" y="42" width="540" height="116" rx="8" fill="#1A2B47"/>
        {perf}
        {frames}
        <text x="314" y="186" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="500" fill="#475673">← 1秒間に並ぶフレーム(この枚数が fps) →</text>
              </svg>
            </div>
          </div>'''

def svg_runlength():
    """Q60/M07: ランレングス圧縮 before→after(1行16画素の例)"""
    # 例の1行: ■■■□□□□□□□□□□□■■(任意の塗り分け)を「色+連続数」に圧縮
    row = list("WWWGGGGGGGGWWWWW")  # 16画素
    cw = 26
    x0 = 60
    before = ""
    for i, c in enumerate(row):
        fill = "#41A38C" if c == "G" else "#FAFCFF"
        before += f'<rect x="{x0+i*cw}" y="44" width="{cw}" height="{cw}" fill="{fill}" stroke="#B8C5D7" stroke-width="1"/>'
    # 連続区画に圧縮
    runs = []
    j = 0
    while j < len(row):
        k = j
        while k < len(row) and row[k] == row[j]:
            k += 1
        runs.append((row[j], k - j))
        j = k
    after = ""
    ax = x0
    for (c, n) in runs:
        w = n * cw / 2  # 圧縮後は1区画固定幅で表現(8bit)
        w = max(64, 0) + 0  # 固定幅
        w = 86
        fill = "#41A38C" if c == "G" else "#FAFCFF"
        after += f'<rect x="{ax}" y="120" width="{w}" height="34" rx="4" fill="{fill}" stroke="#4A78C8" stroke-width="1.5"/>'
        lab = ("緑" if c == "G" else "白") + f"×{n}"
        tcol = "#FFFFFF" if c == "G" else "#1A2B47"
        after += f'<text x="{ax+w/2:.0f}" y="141" text-anchor="middle" font-family="\'Zen Kaku Gothic New\',sans-serif" font-size="13" font-weight="700" fill="{tcol}">{lab}</text>'
        after += f'<text x="{ax+w/2:.0f}" y="170" text-anchor="middle" font-family="monospace" font-size="11" fill="#75839B">8 bit</text>'
        ax += w + 10
    return f'''          <div class="viz">
            <span class="viz-label">RUN-LENGTH — 連続を「色 + 個数」にまとめる</span>
            <div class="viz-caption">同じ色が続くほど区画が減り，データ量が小さくなる。各区画は「色4bit + 個数4bit = 8bit」。</div>
            <div class="viz-svg-wrap">
              <svg class="viz-svg wide" viewBox="0 0 600 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="16画素の1行が、連続する同色のまとまりごとに色と個数の区画へ圧縮される図">
        <text x="46" y="36" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="1">BEFORE — 16画素 × 4bit</text>
        {before}
        <text x="300" y="106" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="16" fill="#4A78C8">▼ 圧縮</text>
        <text x="46" y="106" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="1">AFTER — 区画ごとに 8bit</text>
        {after}
              </svg>
            </div>
          </div>'''

def svg_colormix():
    def circles(cx, cy, r, cols, blend):
        return "".join(
            f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{c}" style="mix-blend-mode:{blend}"/>'
            for (c, dx, dy) in cols)
    R, G, B = "#E23B3B", "#2FB35F", "#3B6FE2"
    C, M, Y = "#27C0CE", "#D24E9E", "#F2D23A"
    add = circles(150, 150, 58, [(R, 0, -34), (G, -30, 22), (B, 30, 22)], "screen")
    sub = circles(450, 150, 58, [(C, 0, -34), (M, -30, 22), (Y, 30, 22)], "multiply")
    return f'''        <div class="viz">
          <span class="viz-label">COLOR MIXING — 光の三原色 と 色の三原色</span>
          <div class="viz-caption">重なりが新しい色を作る。光(RGB)は混ぜるほど明るく、色(CMY)は混ぜるほど暗くなる。</div>
          <div class="viz-svg-wrap">
            <svg class="viz-svg wide" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="左は光の三原色RGBの加法混色で中央が白、右は色の三原色CMYの減法混色で中央が黒になる図">
      <rect x="20" y="34" width="260" height="232" rx="14" fill="#10182B"/>
      <g style="isolation:isolate">{add}</g>
      <text x="150" y="290" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#1A2B47">光の三原色(加法混色)</text>
      <text x="150" y="26" text-anchor="middle" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="2">DISPLAY · R G B</text>
      <rect x="320" y="34" width="260" height="232" rx="14" fill="#FAFCFF" stroke="#D8E2EE" stroke-width="1.5"/>
      <g style="isolation:isolate">{sub}</g>
      <text x="450" y="290" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#1A2B47">色の三原色(減法混色)</text>
      <text x="450" y="26" text-anchor="middle" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="2">PRINTER · C M Y</text>
            </svg>
          </div>
          <div class="viz-caption" style="margin-top:0.6rem;">重なりの色 — 赤=M+Y、緑=C+Y、青=C+M。だからYのインクが切れると、緑はC・赤はMになる。</div>
        </div>'''

# ============================================================
# WELCOME (Stage 0)
# ============================================================
WELCOME = '''  <section class="stage active" data-stage-name="START">
    <div class="welcome-kicker">
      <span class="num">02</span>
      <span>2章 第7節</span>
    </div>
    <h1 class="welcome-title-en">Digital Data<br>Representation<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">デジタル化された情報とその表し方</h2>
    <p class="welcome-lede">
      数値・文字・音・画像・動画を，すべて0と1の組合せで表す仕組みを順に確認する。2進数と16進数の変換，標本化・量子化・符号化，解像度と階調，データ量の計算，そして圧縮までを一続きで扱う。計算問題が中心の節である。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">review</div>
        <div class="welcome-meta-value">7<span class="unit">領域</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">14<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">45<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">2章07</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー 例題30〜38の要点と解法を，Q&amp;A形式の7領域で確認(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>演習</strong>ー 類題54〜61・練習62〜67の計14問。計算問題は自己採点(模範解答と照合)</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>結果</strong>ー 完答数と間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>'''

# ============================================================
# おさらい(REVIEW Digest)— 例題30-38 + 基本表 を 7 モジュールに凝縮
# ============================================================
_ICON_PATHS = {
    "01": '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><line x1="7" y1="11" x2="17" y2="7"/><line x1="7" y1="13" x2="17" y2="17"/>',
    "02": '<rect x="3" y="5" width="18" height="14" rx="2"/><line x1="9" y1="9" x2="9" y2="15"/><circle cx="15" cy="12" r="2.4"/>',
    "03": '<polyline points="4 8 18 8 14.5 4.5"/><polyline points="20 16 6 16 9.5 19.5"/>',
    "04": '<path d="M6 18 L10.5 6 L15 18"/><line x1="7.6" y1="14" x2="13.4" y2="14"/>',
    "05": '<polyline points="3 12 6 12 8 5 11 19 14 9 16 14 21 14"/>',
    "06": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.5" cy="10" r="1.6"/><polyline points="5 17 10 12 13 15 16 12 19 16"/>',
    "07": '<polyline points="9 4 9 9 4 9"/><polyline points="15 20 15 15 20 15"/><line x1="4" y1="20" x2="9" y2="15"/><line x1="20" y1="4" x2="15" y2="9"/>',
}
def dg_icon(num):
    p = _ICON_PATHS.get(num, "")
    if not p:
        return ""
    return ('<span class="dg-ico" aria-hidden="true" style="display:inline-flex;width:18px;height:18px;color:var(--action);flex:none;align-items:center;justify-content:center;margin-right:0.15rem;">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%;height:100%">{p}</svg></span>')

def digest_mod(num, en, q, title, lede, body, hero=False):
    cls = "digest-mod hero" if hero else "digest-mod"
    return f'''    <div class="{cls}">
      <button class="digest-prompt" type="button">
        <div class="digest-prompt-head">
          <span class="digest-num">{num}</span>
          {dg_icon(num)}<span class="digest-en">{en}</span>
          <span class="digest-toggle"><span class="plus">+</span></span>
        </div>
        <div class="digest-q">{q}</div>
      </button>
      <div class="digest-answer">
        <div class="digest-title">{title}</div>
        <p class="digest-lede">{lede}</p>
{body}
      </div>
    </div>'''

# M01 全体像
M01_BODY = '''        <div class="viz">
          <span class="viz-label">THE BIG MAP — 0と1への変換</span>
          <div class="viz-caption">どんな情報も，最後は0と1の並びになる。変換のしかたが種類ごとに違う。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">数値</div><span class="bound">2進数</span><div class="desc">10進数を2で割り続け，余りを並べる。桁の重み(…8,4,2,1)で元に戻す。</div></div>
            <div class="bd-card"><div class="key">文字</div><span class="bound">文字コード</span><div class="desc">文字を2進数に対応づける取り決め。英数字は1バイト，漢字は2バイト以上。</div></div>
            <div class="bd-card"><div class="key">音</div><span class="bound">標本化→量子化→符号化</span><div class="desc">連続する波を一定間隔で区切り，段階値に直し，2進数にする。</div></div>
            <div class="bd-card"><div class="key">画像</div><span class="bound">画素×階調</span><div class="desc">画素ごとに光の三原色(RGB)の明るさを段階値で表す。</div></div>
            <div class="bd-card"><div class="key">動画</div><span class="bound">静止画×時間</span><div class="desc">静止画(フレーム)を連続表示。1秒間の枚数がフレームレート。</div></div>
          </div>
        </div>'''

# M02 情報量・データ量の単位
M02_BODY = '''        <div class="viz">
          <span class="viz-label">BITS &amp; BYTES — 量の数え方</span>
          <div class="viz-caption">nビットで表せる状態の数は 2<sup>n</sup> 通り。これがすべての計算の土台になる。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">1ビット</div><span class="bound">2通り</span><div class="desc">2<sup>1</sup>=2</div></div>
            <div class="bd-card"><div class="key">2ビット</div><span class="bound">4通り</span><div class="desc">2<sup>2</sup>=4</div></div>
            <div class="bd-card"><div class="key">3ビット</div><span class="bound">8通り</span><div class="desc">2<sup>3</sup>=8</div></div>
            <div class="bd-card"><div class="key">8ビット</div><span class="bound">256通り</span><div class="desc">2<sup>8</sup>=256=1バイト</div></div>
          </div>
        </div>
        <div class="viz">
          <span class="viz-label">UNITS — 単位の繰り上がり</span>
          <div class="viz-caption">情報量は 8 と 1024 で繰り上がる。</div>
          <div class="compare">
            <div class="compare-col left">
              <h5>ビット → バイト</h5>
              <div class="row"><span class="k">8 bit</span><span class="v">= 1 B</span></div>
              <div class="row"><span class="k">B→KB→MB</span><span class="v">×1024 ずつ</span></div>
            </div>
            <div class="compare-col right">
              <h5>大きい単位</h5>
              <div class="row"><span class="k">1 KB</span><span class="v">1024 B</span></div>
              <div class="row"><span class="k">1 MB</span><span class="v">1024 KB</span></div>
              <div class="row"><span class="k">1 GB</span><span class="v">1024 MB</span></div>
            </div>
          </div>
        </div>'''

# M03 基数変換
M03_BODY = '''        <div class="origin-compare three-col">
          <div class="origin-side industrial">
            <h5>10進数 → n進数</h5>
            <div class="tag-en">divide &amp; remainder</div>
            <div class="origin-flow"><span class="origin-step">商が0になるまで n で割る</span><span class="origin-step fill">余りを下から並べる</span></div>
            <span class="origin-key">余りを下から読む</span>
            <p class="note">2進数なら最後の商は1。16進数では余りの10〜15を A〜F で表す。</p>
          </div>
          <div class="origin-side industrial">
            <h5>n進数 → 10進数</h5>
            <div class="tag-en">positional weight</div>
            <div class="origin-flow"><span class="origin-step">各桁 × 桁の重み</span><span class="origin-step fill">総和をとる</span></div>
            <span class="origin-key">…,8,4,2,1 の重み</span>
            <p class="note">2進数なら 1,2,4,8,16,32,64,128 …。</p>
          </div>
          <div class="origin-side copyright">
            <h5>16進数 ⇄ 2進数</h5>
            <div class="tag-en">4-bit nibble</div>
            <div class="origin-flow"><span class="origin-step">16進1桁 = 2進4桁</span><span class="origin-step fill">4桁ずつ束ねる</span></div>
            <span class="origin-key">1桁 ↔ 4ビット</span>
            <p class="note">例: A=1010，C=1100。</p>
          </div>
        </div>
        <div class="viz">
          <span class="viz-label">WORKED — 10進数を2で割り続ける(39の例)</span>
          <div class="viz-caption">余り(右の …1, …0)を下から読むと 100111<sub>(2)</sub> になる。</div>
          ''' + fig_box("fig3-base-conversion-39.png", "39を2で割り続ける筆算。余りを下から読むと100111になる。", "39 → 100111<sub>(2)</sub>", maxw=240, imgw=180) + '''
        </div>'''

# M04 文字のデジタル化
M04_BODY = '''        <div class="viz">
          <span class="viz-label">CHARACTER CODE — 文字コード表(JISコードの一部)</span>
          <div class="viz-caption">横が上位桁，縦が下位桁。両者をつなげた値がその文字のコードになる。</div>
          ''' + fig_box("fig1-character-code-table.jpeg", "文字コード表(JISコードの一部)。横方向が上位桁、縦方向が下位桁を表す。", "上位(横) と 下位(縦) をつなげて読む", maxw=560, imgw=520) + '''
        </div>
        <div class="viz">
          <span class="viz-label">HOW TO READ — 読み方と種類</span>
          <div class="viz-caption"></div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">読み方</div><span class="bound">上位+下位</span><div class="desc">例: E は上位0100・下位0101 → 16進で 45。</div></div>
            <div class="bd-card"><div class="key">制御コード</div><span class="bound">上位0000・0001</span><div class="desc">文字ではなく，改行(LF/CR)などの制御に使われる。</div></div>
            <div class="bd-card"><div class="key">日本語</div><span class="bound">JIS / シフトJIS / EUC</span><div class="desc">日本語に対応した文字コード。</div></div>
            <div class="bd-card"><div class="key">世界共通</div><span class="bound">Unicode</span><div class="desc">世界中の言語を統一して扱う文字コード。</div></div>
          </div>
        </div>'''

# M05 音のデジタル化
M05_BODY = '''        <div class="origin-compare three-col">
          <div class="origin-side industrial">
            <h5>① 標本化</h5>
            <div class="tag-en">sampling</div>
            <div class="origin-flow"><span class="origin-step fill">一定間隔で値を取り出す</span></div>
            <span class="origin-key">標本点・標本化周期</span>
            <p class="note">周期が小さいほど元の波形に近い。1秒間の回数が標本化周波数[Hz]で，周期とは逆数。</p>
          </div>
          <div class="origin-side industrial">
            <h5>② 量子化</h5>
            <div class="tag-en">quantization</div>
            <div class="origin-flow"><span class="origin-step fill">最も近い段階値に直す</span></div>
            <span class="origin-key">量子化ビット数で段階数</span>
            <p class="note">ビット数が多いほど段階が細かく，元の波形に近い。ずれは量子化誤差。</p>
          </div>
          <div class="origin-side copyright">
            <h5>③ 符号化</h5>
            <div class="tag-en">coding</div>
            <div class="origin-flow"><span class="origin-step fill">段階値を2進数にする</span></div>
            <span class="origin-key">0と1の並びへ</span>
            <p class="note">3ビットなら段階値を3桁の2進数で表す。</p>
          </div>
        </div>
        <div class="bd-warn"><strong>標本化定理:</strong> 元の波形を再現するには，元の波形の最大周波数の<strong>2倍を超える</strong>標本化周波数が必要。</div>'''

# M06 画像のデジタル化
M06_BODY = '''        <div class="viz">
          <span class="viz-label">IMAGE — 細かさと色</span>
          <div class="viz-caption">画素(ピクセル)の数で細かさが，1画素の色数で色の豊かさが決まる。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">解像度</div><span class="bound">横×縦 の画素数</span><div class="desc">ラスタ形式は拡大するとジャギー(ギザギザ)が出る。ベクタ形式は座標・角度で表し変形に強い。</div></div>
            <div class="bd-card"><div class="key">光の三原色</div><span class="bound">R・G・B(加法混色)</span><div class="desc">ディスプレイ用。混ぜるほど明るく白に近づく。</div></div>
            <div class="bd-card"><div class="key">色の三原色</div><span class="bound">C・M・Y(減法混色)</span><div class="desc">プリンタ用。混ぜるほど暗く黒に近づく。</div></div>
            <div class="bd-card"><div class="key">階調</div><span class="bound">nビットで 2<sup>n</sup> 階調</span><div class="desc">各色8ビット(256階調)が24ビットフルカラー。各色の階調を3つ掛けた数(階調×階調×階調)だけ色を作れる。</div></div>
          </div>
        </div>'''

# M07 データ量と圧縮
M07_BODY = '''        <div class="viz">
          <span class="viz-label">DATA SIZE — データ量の3つの式</span>
          <div class="viz-caption">[bit]→[B] は 8 で割る，[B]→[KB]→[MB] は 1024 で割る。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">音声</div><span class="bound">bit/秒 × 時間</span><div class="desc">量子化ビット数[bit] × 標本化周波数[Hz] × 時間[s] × チャンネル数(モノラル1・ステレオ2)</div></div>
            <div class="bd-card"><div class="key">静止画</div><span class="bound">1画素 × 画素数</span><div class="desc">1画素のデータ量[bit] × 総画素数</div></div>
            <div class="bd-card"><div class="key">動画</div><span class="bound">1枚 × 枚数</span><div class="desc">1フレームのデータ量[bit] × フレームレート[fps] × 時間[s]</div></div>
          </div>
        </div>
        <div class="viz">
          <span class="viz-label">COMPRESSION — 圧縮の2方式</span>
          <div class="viz-caption">圧縮率(%) = 圧縮後 ÷ 圧縮前 ×100。値が小さいほど、元より大きく圧縮できている。</div>
          <div class="compare">
            <div class="compare-col left">
              <h5>可逆圧縮</h5>
              <div class="row"><span class="k">戻り方</span><span class="v">完全に元へ</span></div>
              <div class="row"><span class="k">例</span><span class="v">ZIP</span></div>
            </div>
            <div class="compare-col right">
              <h5>非可逆圧縮</h5>
              <div class="row"><span class="k">戻り方</span><span class="v">元に戻らない</span></div>
              <div class="row"><span class="k">例</span><span class="v">AAC / JPEG / MPEG-4</span></div>
            </div>
          </div>
        </div>'''

REVIEW = '''  <section class="stage" data-stage-name="REVIEW">
    <div class="section-divider">
      <span class="num">01</span>
      <div class="text">
        <div class="label">Section 1 — Visual Digest</div>
        <div class="name">ひと目でわかる おさらい</div>
      </div>
    </div>
    <div class="digest">
''' + "\n".join([
    digest_mod("01", "The Big Map", "どんな情報も，最後はどう表される?", "すべての情報は 0 と 1", "数値・文字・音・画像・動画。種類ごとに変換のしかたは違うが，行き着く先はみな0と1の並びになる。", svg_map() + "\n" + M01_BODY, hero=True),
    digest_mod("02", "Bits &amp; Bytes", "「nビットで何通り」「バイトはどう繰り上がる」?", "情報量とデータ量の単位", "nビットで表せる状態は 2<sup>n</sup> 通り。情報量の単位は 8 と 1024 で繰り上がる。", M02_BODY),
    digest_mod("03", "Base Conversion", "2進数・10進数・16進数をどう行き来する?", "3つの基数の変換", "10進→n進は割り算，n進→10進は桁の重み，16進⇄2進は4桁ずつの束ね。", M03_BODY),
    digest_mod("04", "Character Code", "文字コード表はどう読む?", "文字のデジタル化", "横の上位桁と縦の下位桁をつなげた値が，その文字のコードになる。", M04_BODY),
    digest_mod("05", "Sound", "アナログの波形をどうデジタルに直す?", "音のデジタル化", "標本化→量子化→符号化の3段階。細かく区切る・細かい段階で測るほど元の波形に近づく。", svg_sampling() + "\n" + M05_BODY),
    digest_mod("06", "Image", "画像の細かさと色は何で決まる?", "画像のデジタル化", "画素数で細かさが，1画素の階調で色数が決まる。ディスプレイはRGB，プリンタはCMY。", svg_colormix() + "\n" + M06_BODY),
    digest_mod("07", "Size &amp; Compression", "データ量はどう計算し，どう圧縮する?", "データ量の計算と圧縮", "音声・静止画・動画それぞれの式で求め，8と1024で単位を直す。圧縮には可逆と非可逆がある。", M07_BODY),
]) + '''
    </div>
  </section>'''

# ============================================================
# 練習 14 問(類題54-61 + 練習62-67)
# ============================================================
T = 14  # 練習問題数
P = []   # 各ステージHTML(順に p1..p14)

def M(ans, kaisetsu):
    return f'<p><strong>{ans}</strong><br>{kaisetsu}</p>'

# ---- Q54 情報量(self×4) ----
P.append(stage_self("p1", "54", 1, T, "類題54", "〈情報量〉", "情報量", "次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "コインを3回投げるとき，裏表をすべて記録するには何ビットの情報量が必要か答えよ。"),
                 M("3ビット", "裏を0，表を1とすると，1回投げた結果は1ビットで表せる。3回ぶんで3ビット。")),
        self_row(1, ("⑵", "大小2個のサイコロを投げるとき，出た目の組合せをすべて表すには何ビットの情報量が必要か答えよ。"),
                 M("6ビット", "組合せは6×6＝36通り。2<sup>5</sup>＝32＜36≦64＝2<sup>6</sup> より，6ビット必要。")),
        self_row(2, ("⑶", "ジョーカーを除いた52枚のトランプを表すには，4種類のマークに何ビット，1〜13の数字に何ビットの情報量が必要かそれぞれ答えよ。"),
                 M("マークに2ビット，数字に4ビット", "マークは4通り → 2<sup>2</sup>＝4 で2ビット。数字は13通り → 2<sup>3</sup>＝8＜13≦16＝2<sup>4</sup> で4ビット。")),
        self_row(3, ("⑷", "1 MBは2の何乗バイトになるか，2<sup>n</sup>の形で答えよ。"),
                 M("2<sup>20</sup>バイト", "1 MB＝1024 KB＝1024×1024 B＝2<sup>10</sup>×2<sup>10</sup>＝2<sup>20</sup> B。")),
    ]),
    fb("解説", sec("ベストフィット", "nビットで表現できる状態は 2<sup>n</sup> 通りである。「○通りを表すのに何ビットか」は，2<sup>n</sup> がその通り数以上になる最小の n を探す。")
       + calc_viz("INFORMATION — 通り数とビット数", "必要なビット数は，状態の数を超える最小の 2<sup>n</sup> で決まる。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">マーク 4通り</div><span class="bound">2ビット</span><div class="desc">2<sup>2</sup>=4</div></div>
            <div class="bd-card"><div class="key">数字 13通り</div><span class="bound">4ビット</span><div class="desc">8&lt;13≦16=2<sup>4</sup></div></div>
            <div class="bd-card"><div class="key">サイコロ 36通り</div><span class="bound">6ビット</span><div class="desc">32&lt;36≦64=2<sup>6</sup></div></div>
            <div class="bd-card"><div class="key">1 MB</div><span class="bound">2<sup>20</sup> B</span><div class="desc">1024×1024</div></div>
          </div>'''))))

# ---- Q55 2進数・10進数の変換(self×4) ----
P.append(stage_self("p2", "55", 2, T, "類題55", "〈2進数・10進数の変換〉", "2進数・10進数の変換",
    "次の10進数は2進数に，2進数は10進数に変換せよ。",
    "\n".join([
        self_row(0, ("⑴", "299<sub>(10)</sub>"), M("100101011<sub>(2)</sub>", "2で割り続けると余りは下から 1,1,0,1,0,1,0,0,1。299＝256＋32＋8＋2＋1。")),
        self_row(1, ("⑵", "197<sub>(10)</sub>"), M("11000101<sub>(2)</sub>", "197＝128＋64＋4＋1。")),
        self_row(2, ("⑶", "01100110<sub>(2)</sub>"), M("102<sub>(10)</sub>", "0×128＋1×64＋1×32＋0×16＋0×8＋1×4＋1×2＋0×1＝102。")),
        self_row(3, ("⑷", "10100111<sub>(2)</sub>"), M("167<sub>(10)</sub>", "1×128＋0×64＋1×32＋0×16＋0×8＋1×4＋1×2＋1×1＝167。")),
    ]),
    fb("解説", sec("ベストフィット", "10進数→n進数は，商が1になるまでnで割り続け，商の1を先頭に余りを並べる。n進数→10進数は，各桁に桁の重みをかけて総和をとる。")
       + calc_viz("POSITIONAL WEIGHT — 2進数 各桁の重み", "8桁の2進数は，左から 128,64,32,16,8,4,2,1 の重み。1 の立つ桁だけ足す。",
            '''<div class="compare">
            <div class="compare-col left"><h5>桁の重み(8桁)</h5>
              <div class="row"><span class="k">上位4桁</span><span class="v">128 / 64 / 32 / 16</span></div>
              <div class="row"><span class="k">下位4桁</span><span class="v">8 / 4 / 2 / 1</span></div>
            </div>
            <div class="compare-col right"><h5>⑶ 01100110 の例</h5>
              <div class="row"><span class="k">1が立つ桁</span><span class="v">64・32・4・2</span></div>
              <div class="row"><span class="k">合計</span><span class="v">102</span></div>
            </div>
          </div>'''))))

# ---- Q56 16進数・2進数の変換(self×4) ----
P.append(stage_self("p3", "56", 3, T, "類題56", "〈16進数・2進数の変換〉", "16進数・2進数の変換",
    "次の16進数は2進数に，2進数は16進数に変換せよ。",
    "\n".join([
        self_row(0, ("⑴", "A4<sub>(16)</sub>"), M("10100100<sub>(2)</sub>", "A<sub>(16)</sub>＝1010<sub>(2)</sub>，4<sub>(16)</sub>＝0100<sub>(2)</sub>。")),
        self_row(1, ("⑵", "6E<sub>(16)</sub>"), M("01101110<sub>(2)</sub>", "6<sub>(16)</sub>＝0110<sub>(2)</sub>，E<sub>(16)</sub>＝1110<sub>(2)</sub>。")),
        self_row(2, ("⑶", "10001100<sub>(2)</sub>"), M("8C<sub>(16)</sub>", "下位から4桁ずつ。1000<sub>(2)</sub>＝8<sub>(16)</sub>，1100<sub>(2)</sub>＝C<sub>(16)</sub>。")),
        self_row(3, ("⑷", "11011011<sub>(2)</sub>"), M("DB<sub>(16)</sub>", "1101<sub>(2)</sub>＝D<sub>(16)</sub>，1011<sub>(2)</sub>＝B<sub>(16)</sub>。")),
    ]),
    fb("解説", sec("ベストフィット", "16進数→2進数は，各桁を4桁の2進数へ変換して並べる。2進数→16進数は，下位から4桁ずつ16進数へ変換して並べる。16進1桁と2進4桁が1対1で対応する。")
       + calc_viz("NIBBLE — 16進1桁 ⇄ 2進4桁", "10〜15は A〜F。4桁ずつ束ねるだけで行き来できる。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">A</div><span class="bound">1010</span><div class="desc">10</div></div>
            <div class="bd-card"><div class="key">C</div><span class="bound">1100</span><div class="desc">12</div></div>
            <div class="bd-card"><div class="key">D</div><span class="bound">1101</span><div class="desc">13</div></div>
            <div class="bd-card"><div class="key">E</div><span class="bound">1110</span><div class="desc">14</div></div>
          </div>'''))))

# ---- Q57 文字のデジタル化(self×3, fig1) ----
P.append(stage_self("p4", "57", 4, T, "類題57", "〈文字のデジタル化〉", "文字のデジタル化",
    "次の文字コード表(一部)において，次の問いに答えよ。" + fig_box("fig1-character-code-table.jpeg", "文字コード表(JISコードの一部)。横方向が上位桁、縦方向が下位桁を表す。", "文字コード表(JISコードの一部)。横=上位桁，縦=下位桁。", maxw=560, imgw=520),
    "\n".join([
        self_row(0, ("⑴", "「Q」に対応する文字コードを16進数で表せ。"), M("51<sub>(16)</sub>", "Qは上位0101(16進で5)，下位0001(16進で1)。つなげて 51<sub>(16)</sub>。")),
        self_row(1, ("⑵", "「G」に対応する文字コードを2進数で表せ。"), M("01000111<sub>(2)</sub>", "Gは上位0100，下位0111。つなげて 01000111<sub>(2)</sub>。")),
        self_row(2, ("⑶", "01100001<sub>(2)</sub>に対応する文字を答えよ。"), M("a", "上位0110・下位0001 の交点。表をたどると a。")),
    ]),
    fb("解説", sec("ベストフィット", "文字コードは，表の横方向の上位桁と，縦方向の下位桁をつなげたものになる。")
       + sec("補足", "この表はJISコードの一部である。上位0000・0001の列には文字ではなく制御コード(NUL，LF，CR など)が割り当てられている。"))))

# ---- Q58 音のデジタル化(multi すべて選べ) ----
P.append(stage_multi("p5", "58", 5, T, "類題58", "〈音のデジタル化〉", "音のデジタル化",
    "音のデジタル化に関する次の(ア)〜(オ)の記述のうち，適当なものをすべて選べ。",
    [("(ア)", "標本化周期が小さいほど，元のアナログ波形に近くなる。"),
     ("(イ)", "標本化周期が小さいほど，データ量は小さくなる。"),
     ("(ウ)", "標本化周波数は，標本化周期の逆数になっている。"),
     ("(エ)", "量子化ビット数が多いほど，元のアナログ波形に近くなる。"),
     ("(オ)", "元のアナログ波形の最大周波数が50 Hzの場合，100 Hzより大きい標本化周波数でデジタル化すればよい。")],
    [0, 2, 3, 4],
    fb("解説", correct_line("(ア)，(ウ)，(エ)，(オ)")
       + sec("各記述の検討", '''<ul>
        <li><strong>(ア) 適当</strong> 標本化周期が小さい＝細かく標本化 → 元の波形に近づく。</li>
        <li><strong>(イ) 適当でない</strong> 周期が小さいと1秒間の標本化回数が増える → データ量は<strong>大きく</strong>なる。</li>
        <li><strong>(ウ) 適当</strong> 標本化周波数は標本化周期の逆数。</li>
        <li><strong>(エ) 適当</strong> 量子化ビット数が多い＝段階が細かい → 元の波形に近づく。</li>
        <li><strong>(オ) 適当</strong> 標本化定理より，最大周波数の2倍(＝100 Hz)を超える標本化周波数なら波形を再現できる。</li>
      </ul>''')
       + calc_viz("SAMPLING — 周期と周波数は逆数", "細かく測る(周期↓ = 周波数↑)ほど精密だが，データ量は増える。",
            '''<div class="compare">
            <div class="compare-col left"><h5>標本化周期 ↓</h5>
              <div class="row"><span class="k">精度</span><span class="v">波形に近い ○</span></div>
              <div class="row"><span class="k">データ量</span><span class="v">大きい</span></div>
            </div>
            <div class="compare-col right"><h5>量子化ビット数 ↑</h5>
              <div class="row"><span class="k">段階</span><span class="v">細かい</span></div>
              <div class="row"><span class="k">精度</span><span class="v">波形に近い ○</span></div>
            </div>
          </div>'''))))

# ---- Q59 画像のデジタル化(self×2) ----
P.append(stage_self("p6", "59", 6, T, "類題59", "〈画像のデジタル化〉", "画像のデジタル化",
    "カラー画像を構成する画素の赤，緑，青それぞれの明るさを表現するために，2ビットずつ割り当てたとき，次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "各色の明るさの段階は何階調になるか。"), M("4階調", "2ビット → 2<sup>2</sup>＝4 階調。")),
        self_row(1, ("⑵", "全部で何色の色を表現できるか。"), M("64色", "各色4階調なので，組合せは 4×4×4＝4<sup>3</sup>＝64 色。")),
    ]),
    fb("解説", sec("ベストフィット", "各色 n 階調のとき，表現できる色は n×n×n 色。各色の明るさの段階数を階調という。")
       + calc_viz("COLORS — 各色の階調 → 全体の色数", "1画素はR・G・Bの3色。各色の階調を掛け合わせた数だけ色を作れる。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">各色 2ビット</div><span class="bound">4階調</span><div class="desc">2<sup>2</sup>=4</div></div>
            <div class="bd-card"><div class="key">R×G×B</div><span class="bound">4×4×4</span><div class="desc">4<sup>3</sup></div></div>
            <div class="bd-card"><div class="key">表現できる色</div><span class="bound">64色</span><div class="desc">=2<sup>6</sup></div></div>
          </div>'''))))

# ---- Q60 動画のデジタル化(self×3) ----
P.append(stage_self("p7", "60", 7, T, "類題60", "〈動画のデジタル化〉", "動画のデジタル化", "次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "3分間で4320フレームを再生する動画のフレームレートは何fpsか求めよ。"), M("24 fps", "4320 ÷ (3×60) ＝ 4320 ÷ 180 ＝ 24。")),
        self_row(1, ("⑵", "フレームレートが24 fpsで10分間の動画を構成するフレーム数を求めよ。"), M("14400フレーム", "24 × (10×60) ＝ 24 × 600 ＝ 14400。")),
        self_row(2, ("⑶", "ある防犯カメラが300000フレームの画像を保存できるとき，24時間分の動画を記録するためのフレームレートは何fpsか求めよ。ただし，フレームレートの値は整数とする。"), M("3 fps", "300000 ÷ (24×60×60) ＝ 300000 ÷ 86400 ≒ 3.47。300000フレーム内に収めるため，小数点以下を切り捨てて3 fps。")),
    ]),
    fb("解説", sec("ベストフィット", "フレームレート[fps]は，1秒間に再生するフレーム数。フレーム数 ＝ フレームレート × 時間[s] の関係を使い分ける。")
       + sec("補足", "⑶では割ると3.47…になるが，保存できる枚数(300000)を超えてはいけないので切り上げではなく切り捨てる。") + svg_filmstrip())))

# ---- Q61 情報のデータ量・圧縮(self×2) ----
P.append(stage_self("p8", "61", 8, T, "類題61", "〈情報のデータ量・圧縮〉", "情報のデータ量・圧縮", "次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "解像度512×256の24ビットフルカラー画像を1フレームとした28 fpsの20秒間の動画のデータ量は何MBか求めよ。"), M("210 MB", "24×512×256×28×20 ÷8 ÷1024 ÷1024 ＝ 210 MB。動画＝1画素のデータ量×画素数×フレームレート×時間。")),
        self_row(1, ("⑵", "⑴の動画を，ある圧縮方法で42 MBの圧縮動画ファイルへ変換した。この変換での圧縮率は何％か。ただし，圧縮率は，圧縮後のデータ量の元のデータ量に対する割合で求めよ。"), M("20 ％", "(42 ÷ 210) ×100 ＝ 20 ％。")),
    ]),
    fb("解説", sec("ベストフィット", "[bit]→[B] は8で割り，[B]→[KB]→[MB] は1024で割る。圧縮率(%) ＝ 圧縮後 ÷ 圧縮前 ×100。")
       + calc_viz("MOVIE SIZE — 動画データ量の組み立て", "1画素24ビット × 画素数 × フレームレート × 時間 を，8と1024で単位変換する。",
            '''<div class="compare">
            <div class="compare-col left"><h5>⑴ データ量</h5>
              <div class="row"><span class="k">1フレーム</span><span class="v">24×512×256 bit</span></div>
              <div class="row"><span class="k">×28fps×20s</span><span class="v">→ 210 MB</span></div>
            </div>
            <div class="compare-col right"><h5>⑵ 圧縮率</h5>
              <div class="row"><span class="k">42 ÷ 210</span><span class="v">×100</span></div>
              <div class="row"><span class="k">圧縮率</span><span class="v">20 ％</span></div>
            </div>
          </div>'''))))

# ---- Q62 情報量(self×2) ----
P.append(stage_self("p9", "62", 9, T, "練習62", "〈情報量〉", "情報量",
    "ある文字コードは，2バイトで文字や記号を表している。この文字コードに関する次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "この文字コードだけで構成された文書(テキストデータ)の3584文字分のデータ量は何KBか答えよ。"), M("7 KB", "1文字＝2バイト → 2×3584＝7168 B。7168 ÷ 1024 ＝ 7 KB。")),
        self_row(1, ("⑵", "この文字コードで2バイトの文字コードとして使用できるのは，16進数で表現した文字コードの最上位の桁の値が8，9，E，Fのものに限定される場合，何種類の文字や記号が表現できるか答えよ。"), M("16384種類", "2バイト＝4桁の16進数。下位3桁は16<sup>3</sup>＝4096通り。最上位は8・9・E・Fの4通り。4×4096＝16384種類。")),
    ]),
    fb("解説", sec("ベストフィット", "2バイト＝16ビット＝4桁の16進数。1桁の16進数は16通りを表せる。")
       + calc_viz("2-BYTE CODE — 4桁の16進数", "最上位の桁が4通りに限定されるので，全体の種類はそのぶん絞られる。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">3584文字</div><span class="bound">7 KB</span><div class="desc">2×3584÷1024</div></div>
            <div class="bd-card"><div class="key">下位3桁</div><span class="bound">4096通り</span><div class="desc">16<sup>3</sup></div></div>
            <div class="bd-card"><div class="key">最上位</div><span class="bound">4通り</span><div class="desc">8・9・E・F</div></div>
            <div class="bd-card"><div class="key">合計</div><span class="bound">16384種類</span><div class="desc">4×4096</div></div>
          </div>'''))))

# ---- Q63 文字のデジタル化(self×1, 会話文) ----
P.append(stage_self("p10", "63", 10, T, "練習63", "〈文字のデジタル化〉", "文字のデジタル化",
    '例題33において一部が表記されている文字コードには，「制御文字」と呼ばれる，ディスプレイやプリンタでの文字の表示の制御などに使用される特殊な文字コードがあり，その多くは16進数で表現した文字コードで上位桁に0または1が割り当てられている。あるコンピュータシステムでは，文字コード 0A<sub>(16)</sub> の「LF」と 0D<sub>(16)</sub> の「CR」の二つをセットにして「改行」を行っている。また，文字コード 20<sub>(16)</sub> の「（空白）」は半角スペースである。このことを踏まえて，次の会話文のテキストデータのデータ量は何Bか答えよ。'
    + '<blockquote style="margin: 0.8rem 0 0.4rem; padding: 0.9rem 1.1rem; background: var(--bg-soft); border-left: 4px solid var(--action-pale2); border-radius: 0 8px 8px 0; font-family: var(--f-mono); font-size: 0.92rem; line-height: 1.9; color: var(--ink);">Where is the station?<br>It\'s over there.<br>Thank you.</blockquote>',
    self_row(0, ("", "上の会話文のテキストデータのデータ量は何Bか。"), M("51 B", "1文字＝1バイト。空白を除く見える文字・記号は41文字＝41 B。半角スペース6個＝6 B。改行2つはそれぞれLF＋CRの2文字ぶんなので 2×2＝4 B。合計 41＋6＋4＝51 B。")),
    fb("解説", sec("ベストフィット", "1文字が1バイトなので，文字数(記号・空白を含む)＋改行ぶんのバイト数を数える。改行はLFとCRの2文字で1回ぶん。")
       + calc_viz("TEXT SIZE — 文字・空白・改行の内訳", "見える文字だけでなく，スペースと改行もデータ量に含める。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">見える文字・記号</div><span class="bound">41 B</span><div class="desc">41文字</div></div>
            <div class="bd-card"><div class="key">半角スペース</div><span class="bound">6 B</span><div class="desc">6個</div></div>
            <div class="bd-card"><div class="key">改行(LF+CR)</div><span class="bound">4 B</span><div class="desc">2回×2 B</div></div>
            <div class="bd-card"><div class="key">合計</div><span class="bound">51 B</span><div class="desc">41+6+4</div></div>
          </div>'''))))

# ---- Q64 音の情報量(self×1) ----
P.append(stage_self("p11", "64", 11, T, "練習64", "〈音の情報量〉", "音の情報量",
    "標本化周波数96 kHz，量子化ビット数24ビット，ステレオで記録されている60分間の音声データが複数あり，これらをメモリーカードへコピーする。このとき，32 GBのメモリーカードにコピーできる音声データの最大数は何個か答えよ。ただし，これらの音声データは非圧縮とする。",
    self_row(0, ("", "32 GBのメモリーカードにコピーできる音声データの最大数は何個か。"), M("16個", "音の情報量＝量子化ビット数 × 標本化周波数 × 時間 × チャンネル数。1個＝24×96000×(60×60)×2 bit ≒ 1.93 GB。32 ÷ 1.93 ≒ 16.58 より，最大16個。")),
    fb("解説", sec("ベストフィット", "音のデータ量は，量子化ビット数[bit] × 標本化周波数[Hz] × 時間[s] × チャンネル数。ステレオはチャンネル数2。")
       + calc_viz("AUDIO SIZE — 1個の容量から個数へ", "1個の容量を求め，カード容量を割って小数点以下を切り捨てる。",
            '''<div class="compare">
            <div class="compare-col left"><h5>1個の容量</h5>
              <div class="row"><span class="k">24bit×96kHz</span><span class="v">×3600s×2</span></div>
              <div class="row"><span class="k">÷8÷1024<sup>3</sup></span><span class="v">≒ 1.93 GB</span></div>
            </div>
            <div class="compare-col right"><h5>コピー個数</h5>
              <div class="row"><span class="k">32 ÷ 1.93</span><span class="v">≒ 16.58</span></div>
              <div class="row"><span class="k">最大</span><span class="v">16個</span></div>
            </div>
          </div>'''))))

# ---- Q65 画像のデジタル化(self×3) ----
P.append(stage_self("p12", "65", 12, T, "練習65", "〈画像のデジタル化〉", "画像のデジタル化",
    "赤(R)，緑(G)，青(B)の光の三原色の混色によって512色を表現するカラー画像について次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "このカラー画像の1画素当たりの情報量は何ビットになるか答えよ。"), M("9ビット", "2<sup>9</sup>＝512 より，9ビット。")),
        self_row(1, ("⑵", "⑴の情報量を赤，緑，青の各色の階調を表現するため均等に割り当てたとき，各色の明るさは何階調になるか答えよ。"), M("8階調", "9 ÷ 3＝3ビットずつ。2<sup>3</sup>＝8 階調。")),
        self_row(2, ("⑶", "このカラー画像の解像度が1920×1080であるとき，データ量は何MBか答えよ。ただし，データ量は小数第2位を四捨五入して小数第1位まで答えよ。"), M("2.2 MB", "9 × 1920 × 1080 ÷8 ÷1024 ÷1024 ≒ 2.2 MB。")),
    ]),
    fb("解説", sec("ベストフィット", "1画素の情報量[bit] × 総画素数 が静止画のデータ量。色数から1画素のビット数を逆算する(2<sup>n</sup>＝色数)。")
       + calc_viz("PIXEL — 512色 → 1画素9ビット", "色数からビット数を求め，3色に均等配分。最後に画素数を掛けて単位変換。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">512色</div><span class="bound">9ビット</span><div class="desc">2<sup>9</sup></div></div>
            <div class="bd-card"><div class="key">3色に均等</div><span class="bound">3ビットずつ</span><div class="desc">8階調</div></div>
            <div class="bd-card"><div class="key">1920×1080</div><span class="bound">2.2 MB</span><div class="desc">9×画素数÷8÷1024<sup>2</sup></div></div>
          </div>'''))))

# ---- Q66 画像のデジタル化(self×2: 選択+計算) ----
P.append(stage_self("p13", "66", 13, T, "練習66", "〈画像のデジタル化〉", "画像のデジタル化",
    "シアン(C)，マゼンタ(M)，イエロー(Y)の色の三原色の重ね合わせで印刷するカラープリンタについて次の問いに答えよ。",
    "\n".join([
        self_row(0, ("⑴", "このカラープリンタでイエロー(Y)のインクが切れたときに起きることについて，次の(ア)〜(オ)の記述のうち，適当なものをすべて選べ。<br>(ア) 緑(G)で印刷される部分がシアン(C)になる。<br>(イ) 青(B)で印刷される部分が緑(G)になる。<br>(ウ) シアン(C)で印刷される部分が青(B)になる。<br>(エ) 赤(R)で印刷される部分がマゼンタ(M)になる。<br>(オ) マゼンタ(M)で印刷される部分が青(B)になる。"),
                 M("(ア)，(エ)", "緑(G)＝Y＋Cの混色，赤(R)＝M＋Yの混色。Yが切れると，もう一方のインクの色だけが残る → Gの部分はC，Rの部分はMになる。")),
        self_row(1, ("⑵", "このカラープリンタで多くの色を表現するためには，色の三原色それぞれの濃淡を調整して印刷すればよい。全部で64色が印刷できるようにするためには，各色の濃淡を何段階に調整すればよいか答えよ。"),
                 M("4段階", "各色 n 段階なら表現できる色は n<sup>3</sup> 色。n<sup>3</sup>＝64 より n＝4 段階。")),
    ]),
    fb("解説", sec("ベストフィット", "色の三原色(CMY)は減法混色。混色でできる色は，2色のインクの重ね合わせ。各色 n 段階で n<sup>3</sup> 色を表せる。")
       + calc_viz("CMY — 混色とインク切れ", "緑=Y+C，赤=M+Y。片方が切れると，もう片方のインクの色になる。",
            '''<div class="compare">
            <div class="compare-col left"><h5>Yが切れると</h5>
              <div class="row"><span class="k">緑(Y+C)</span><span class="v">→ C</span></div>
              <div class="row"><span class="k">赤(M+Y)</span><span class="v">→ M</span></div>
            </div>
            <div class="compare-col right"><h5>⑵ 64色</h5>
              <div class="row"><span class="k">n<sup>3</sup>=64</span><span class="v">n=4</span></div>
              <div class="row"><span class="k">各色</span><span class="v">4段階</span></div>
            </div>
          </div>'''))))

# ---- Q67 データの圧縮(self×2: 計算+選択, fig2) ----
P.append(stage_self("p14", "67", 14, T, "練習67", "〈データの圧縮〉", "データの圧縮",
    "ランレングス圧縮について次の問いに答えよ。" + fig_box("fig2-runlength-grid.jpeg", "解像度16×16の静止画。中央を十字に塗りつぶしたパターン。", "解像度16×16の静止画(右図)", maxw=300, imgw=240),
    "\n".join([
        self_row(0, ("⑴", "ランレングス圧縮は，データの中で同じ値が横方向に連続する部分を，その値と連続する回数で表現することでデータを圧縮している。上の解像度16×16の静止画を圧縮したときの圧縮率は何％か答えよ。ただし，圧縮率は小数第2位を四捨五入して小数第1位まで答えよ。また，圧縮前のデータ量は1画素当たり4ビット，圧縮後のデータは，色が連続する部分について，「色の表現のデータ4ビット」と「その色が連続する画素数のデータ4ビット」で構成される。"),
                 M("34.4 ％", "圧縮前＝4×16×16＝1024 bit。圧縮後は塗りつぶしの区画ごとに8ビット。1行目と16行目は1区画＝8 bit，2〜15行目は3区画＝8×3＝24 bit。合計＝8＋24×14＋8＝352 bit。圧縮率＝(352 ÷ 1024)×100 ≒ 34.4 ％。")),
        self_row(1, ("⑵", "ランレングス圧縮に関する次の(ア)〜(オ)の記述のうち，適当なものをすべて選べ。<br>(ア) 写真のように色が微妙に変化する画像の圧縮に向いている。<br>(イ) 同じ色で塗りつぶされている面が大きいほど，データ量を小さくできる。<br>(ウ) 塗りつぶしのパターンによっては，データ量が圧縮前より大きくなってしまう場合がある。<br>(エ) 伸長したデータは，圧縮前のデータと完全に同じものにはならない。<br>(オ) カラー画像は，256色までしか扱えない。"),
                 M("(イ)，(ウ)", "(ア)×同じ色の面が大きい画像向き。(エ)×可逆圧縮なので完全に元へ戻る。(オ)×扱える色数とは無関係。連続が少ないと(ウ)のように増えることもある。")),
    ]),
    fb("解説", sec("ベストフィット", "ランレングス圧縮は，連続する同じ色を「色＋連続回数」にまとめる可逆圧縮。同色が長く続くほど縮む。")
       + svg_runlength()
       + calc_viz("RUN-LENGTH — 区画ごとに8ビット", "各行を「色4bit＋連続数4bit＝8bit」の区画に分ける。区画が少ない行ほど小さい。",
            '''<div class="bd-grid">
            <div class="bd-card"><div class="key">圧縮前</div><span class="bound">1024 bit</span><div class="desc">4×16×16</div></div>
            <div class="bd-card"><div class="key">1・16行目</div><span class="bound">8 bit</span><div class="desc">1区画</div></div>
            <div class="bd-card"><div class="key">2〜15行目</div><span class="bound">24 bit</span><div class="desc">3区画×8</div></div>
            <div class="bd-card"><div class="key">圧縮率</div><span class="bound">34.4 ％</span><div class="desc">352÷1024</div></div>
          </div>'''))))

PRACTICE = "\n\n".join(P)

# ============================================================
# SUMMARY(末尾)
# ============================================================
SUMMARY = '''  <section class="stage" data-stage-name="RESULT">
    <div class="section-divider">
      <span class="num">02</span>
      <div class="text">
        <div class="label">Section 2 — Result</div>
        <div class="name">演習結果</div>
      </div>
    </div>
    <div class="summary-hero">
      <div class="summary-grade" id="summary-grade">—<span class="denom">/14</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">14問の練習問題のうち，何問完答できたか。</div>
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
  </section>'''

# ============================================================
# <main> 組み立て + splice
# ============================================================
NEW_MAIN = "<main id=\"stages\">\n\n" + WELCOME + "\n\n" + REVIEW + "\n\n" + PRACTICE + "\n\n" + SUMMARY + "\n\n</main>"
# 句読点をキット慣例(、。)へ正規化(原本の全角カンマ，→ 読点、。02-06 と統一)
NEW_MAIN = NEW_MAIN.replace("，", "、")

m0 = html.index("<main id=\"stages\">")
m1 = html.index("</main>") + len("</main>")
html = html[:m0] + NEW_MAIN + html[m1:]

# title
html = html.replace("<title>情報デザインの応用 | Practice Lab</title>",
                    "<title>デジタル化された情報とその表し方 | Practice Lab</title>")

# ---- JS: TIMELINE_ENTRIES ----
TL = '''  const TIMELINE_ENTRIES = [
    { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
    { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2,  group: 'practice', num: 'Q54', label: '〈情報量〉', probId: 'p1' },
    { idx: 3,  group: 'practice', num: 'Q55', label: '〈2進・10進変換〉', probId: 'p2' },
    { idx: 4,  group: 'practice', num: 'Q56', label: '〈16進・2進変換〉', probId: 'p3' },
    { idx: 5,  group: 'practice', num: 'Q57', label: '〈文字のデジタル化〉', probId: 'p4' },
    { idx: 6,  group: 'practice', num: 'Q58', label: '〈音のデジタル化〉', probId: 'p5' },
    { idx: 7,  group: 'practice', num: 'Q59', label: '〈画像のデジタル化〉', probId: 'p6' },
    { idx: 8,  group: 'practice', num: 'Q60', label: '〈動画のデジタル化〉', probId: 'p7' },
    { idx: 9,  group: 'practice', num: 'Q61', label: '〈データ量・圧縮〉', probId: 'p8' },
    { idx: 10, group: 'practice', num: 'Q62', label: '〈情報量〉', probId: 'p9' },
    { idx: 11, group: 'practice', num: 'Q63', label: '〈文字のデジタル化〉', probId: 'p10' },
    { idx: 12, group: 'practice', num: 'Q64', label: '〈音の情報量〉', probId: 'p11' },
    { idx: 13, group: 'practice', num: 'Q65', label: '〈画像のデジタル化〉', probId: 'p12' },
    { idx: 14, group: 'practice', num: 'Q66', label: '〈画像のデジタル化〉', probId: 'p13' },
    { idx: 15, group: 'practice', num: 'Q67', label: '〈データの圧縮〉', probId: 'p14' },
    { idx: 16, group: 'result',   num: '✓',   label: '結果サマリ' }
  ];'''
html = re.sub(r"  const TIMELINE_ENTRIES = \[.*?\];", TL, html, count=1, flags=re.S)

# ---- JS: footer score '/6' → '/14' ----
html = html.replace("if (sbScore) sbScore.textContent = full + '/6';",
                    "if (sbScore) sbScore.textContent = full + '/14';")

# ---- JS: PROBLEMS ----
PROBS = '''  const PROBLEMS = [
    { id: 'p1',  label: 'Q54', name: '〈情報量〉', stageIdx: 2 },
    { id: 'p2',  label: 'Q55', name: '〈2進・10進変換〉', stageIdx: 3 },
    { id: 'p3',  label: 'Q56', name: '〈16進・2進変換〉', stageIdx: 4 },
    { id: 'p4',  label: 'Q57', name: '〈文字のデジタル化〉', stageIdx: 5 },
    { id: 'p5',  label: 'Q58', name: '〈音のデジタル化〉', stageIdx: 6 },
    { id: 'p6',  label: 'Q59', name: '〈画像のデジタル化〉', stageIdx: 7 },
    { id: 'p7',  label: 'Q60', name: '〈動画のデジタル化〉', stageIdx: 8 },
    { id: 'p8',  label: 'Q61', name: '〈データ量・圧縮〉', stageIdx: 9 },
    { id: 'p9',  label: 'Q62', name: '〈情報量〉', stageIdx: 10 },
    { id: 'p10', label: 'Q63', name: '〈文字のデジタル化〉', stageIdx: 11 },
    { id: 'p11', label: 'Q64', name: '〈音の情報量〉', stageIdx: 12 },
    { id: 'p12', label: 'Q65', name: '〈画像のデジタル化〉', stageIdx: 13 },
    { id: 'p13', label: 'Q66', name: '〈画像のデジタル化〉', stageIdx: 14 },
    { id: 'p14', label: 'Q67', name: '〈データの圧縮〉', stageIdx: 15 }
  ];'''
html = re.sub(r"  const PROBLEMS = \[.*?\];", PROBS, html, count=1, flags=re.S)

# ---- JS: renderSummary 分母 + 閾値(14問用: s-high≥11, s-mid≥7) ----
html = html.replace("animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/6</span>');",
                    "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/14</span>');")
html = html.replace("    if (fullCount >= 5) grade.classList.add('s-high');\n    else if (fullCount >= 3) grade.classList.add('s-mid');",
                    "    if (fullCount >= 11) grade.classList.add('s-high');\n    else if (fullCount >= 7) grade.classList.add('s-mid');")

SRC.write_text(html, encoding="utf-8")
print("built:", SRC)
print("practice stages:", len(P))
print("len html:", len(html))


