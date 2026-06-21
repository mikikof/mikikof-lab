# -*- coding: utf-8 -*-
"""
思考のステップ2「加法混色と減法混色」ビルダー
- ベース = 02-07 を cp した index.html(self/single 型・混色SVG・エンジン内蔵)
- エンジン(CSS/JS)保全、<main> と JS データ配列のみ差替
- 原本: ベストフィット 2章 思考のステップ2 / 図 fig1(シアン=赤吸収) fig2(マゼンタ+イエロー=緑青吸収)
"""
import re, pathlib
HERE = pathlib.Path(__file__).parent
SRC = HERE / "index.html"
html = SRC.read_text(encoding="utf-8")

# ---------- ヘルパー ----------
def fig_box(src, alt, cap, maxw=320, imgw=280):
    return (f'<figure style="margin: 0.7rem auto; padding: 0.8rem 1rem; background: var(--bg-card); '
            f'border: 1px solid var(--line); border-radius: 8px; display: inline-block; max-width: {maxw}px; text-align: center;">'
            f'<img src="assets/{src}" alt="{alt}" style="display: block; width: 100%; height: auto; max-width: {imgw}px; margin: 0 auto;">'
            f'<figcaption style="margin-top: 0.5rem; font-family: var(--f-mono); font-size: 0.74rem; color: var(--ink-mute); line-height:1.5;">{cap}</figcaption>'
            f'</figure>')

def self_row(sub, q, model_html):
    return f'''        <div class="self-row" data-sub="{sub}">
          <div class="self-q"><span class="self-sub-label">{q[0]}</span>{q[1]}</div>
          <textarea class="self-input" rows="2" placeholder="解答群から番号を選んでみてください(任意)"></textarea>
          <button type="button" class="self-reveal" data-action="self-reveal">模範解答を見る</button>
          <div class="self-model">
            <div class="self-model-label">模範解答</div>
            {model_html}
            <div class="self-rate">
              <span class="self-rate-q">模範解答と照らして:</span>
              <button type="button" class="self-rate-btn ok" data-mark="ok">選べた ○</button>
              <button type="button" class="self-rate-btn no" data-mark="no">まだ △</button>
            </div>
          </div>
        </div>'''

def M(ans, kaisetsu):
    return f'<p><strong>{ans}</strong><br>{kaisetsu}</p>'

def stage_self(probid, qnum, idx, total, src, kakko, title, lead_html, rows_html, fb_html):
    block = ""
    mm = re.search(r'<figure|<blockquote|<div', lead_html)
    if mm:
        i = mm.start(); block = "\n      " + lead_html[i:]; lead_html = lead_html[:i].rstrip()
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

def stage_single(probid, qnum, idx, total, src, kakko, title, lead_html, opts, correct, fb_html):
    block = ""
    mm = re.search(r'<figure|<blockquote|<div', lead_html)
    if mm:
        i = mm.start(); block = "\n      " + lead_html[i:]; lead_html = lead_html[:i].rstrip()
    o = "\n".join(
        f'        <label class="opt"><input type="radio" name="{probid}"><span class="opt-mark"></span>'
        f'<span class="opt-text"><span class="opt-letter">{l}</span>{t}</span></label>'
        for (l, t) in opts)
    return f'''  <section class="stage" data-stage-name="練習 {qnum}" data-prob-id="{probid}">
    <div class="problem-meta">
      <span class="problem-tag practice">PRACTICE {idx} / {total}</span>
      <span class="problem-tag single">SINGLE</span>
      <span class="problem-source">ベストフィット {src}</span>
    </div>
    <div class="problem-q-num"><span class="q">Q</span>{qnum}</div>
    <h3 class="problem-title">{kakko}{title}</h3>
    <div class="problem-card">
      <p class="problem-q lead">{lead_html}</p>{block}
      <div class="opts" data-input="single" data-correct="{correct}">
{o}
      </div>
      <div class="actions-inline">
        <button class="btn-grade" data-action="grade">採点する <span class="arrow">→</span></button>
      </div>
{fb_html}
    </div>
  </section>'''

def fb(banner_label, body_html):
    return f'''      <div class="feedback" data-feedback>
        <div class="fb-banner ok"><span class="icon">✓</span><span>{banner_label}</span><span class="score-tag"></span></div>
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

# ---------- SVG(混色・再利用 + 吸収フロー) ----------
def svg_colormix():
    def circles(cx, cy, r, cols, blend):
        return "".join(
            f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{c}" style="mix-blend-mode:{blend}"/>'
            for (c, dx, dy) in cols)
    R, G, B = "#E23B3B", "#2FB35F", "#3B6FE2"
    C, Mg, Y = "#27C0CE", "#D24E9E", "#F2D23A"
    add = circles(150, 150, 58, [(R, 0, -34), (G, -30, 22), (B, 30, 22)], "screen")
    sub = circles(450, 150, 58, [(C, 0, -34), (Mg, -30, 22), (Y, 30, 22)], "multiply")
    return f'''        <div class="viz">
          <span class="viz-label">COLOR MIXING — 光の三原色 と 色の三原色</span>
          <div class="viz-caption">光(RGB)は重ねるほど明るく白へ(加法)、色(CMY)は重ねるほど暗く黒へ(減法)。</div>
          <div class="viz-svg-wrap">
            <svg class="viz-svg wide" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="左は光の三原色RGBの加法混色で中央が白、右は色の三原色CMYの減法混色で中央が黒">
      <rect x="20" y="34" width="260" height="232" rx="14" fill="#10182B"/>
      <g style="isolation:isolate">{add}</g>
      <text x="150" y="290" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#1A2B47">光の三原色(加法混色)</text>
      <text x="150" y="26" text-anchor="middle" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="2">LIGHT · R G B</text>
      <rect x="320" y="34" width="260" height="232" rx="14" fill="#FAFCFF" stroke="#D8E2EE" stroke-width="1.5"/>
      <g style="isolation:isolate">{sub}</g>
      <text x="450" y="290" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#1A2B47">色の三原色(減法混色)</text>
      <text x="450" y="26" text-anchor="middle" font-family="'DM Sans',sans-serif" font-size="12" font-weight="700" fill="#75839B" letter-spacing="2">INK · C M Y</text>
            </svg>
          </div>
          <div class="viz-caption" style="margin-top:0.6rem;">インクは「光を引く」。シアン=赤を吸収／マゼンタ=緑を吸収／イエロー=青を吸収。</div>
        </div>'''

# ---------- 錐体の表(HTML) ----------
def cone_table():
    rows = [
        ("×","×","×","黒","#1A2B47","#FFFFFF"),
        ("○","×","×","赤","#E23B3B","#FFFFFF"),
        ("×","○","×","緑","#2FB35F","#FFFFFF"),
        ("×","×","○","青","#3B6FE2","#FFFFFF"),
        ("×","○","○","シアン","#27C0CE","#10182B"),
        ("○","×","○","マゼンタ","#D24E9E","#FFFFFF"),
        ("○","○","×","イエロー","#F2D23A","#10182B"),
        ("○","○","○","白","#F4F8FC","#1A2B47"),
    ]
    tr = ""
    for (l, m, s, col, bg, fg) in rows:
        def cell(v):
            c = "var(--ok-deep)" if v == "○" else "var(--ink-faint)"
            return f'<td style="text-align:center;font-family:var(--f-mono);font-weight:700;color:{c};padding:0.3rem 0.2rem;border-top:1px solid var(--line-soft);">{v}</td>'
        tr += (f'<tr>{cell(l)}{cell(m)}{cell(s)}'
               f'<td style="padding:0.3rem 0.5rem;border-top:1px solid var(--line-soft);"><span style="display:inline-block;padding:0.12rem 0.6rem;border-radius:999px;background:{bg};color:{fg};font-weight:700;font-size:0.82rem;border:1px solid var(--line);">{col}</span></td></tr>')
    head = ('<th style="padding:0.4rem 0.2rem;font-family:var(--f-la);font-size:0.7rem;letter-spacing:0.1em;color:var(--ink-mute);">L錐体</th>'
            '<th style="padding:0.4rem 0.2rem;font-family:var(--f-la);font-size:0.7rem;letter-spacing:0.1em;color:var(--ink-mute);">M錐体</th>'
            '<th style="padding:0.4rem 0.2rem;font-family:var(--f-la);font-size:0.7rem;letter-spacing:0.1em;color:var(--ink-mute);">S錐体</th>'
            '<th style="padding:0.4rem 0.5rem;text-align:left;font-family:var(--f-la);font-size:0.7rem;letter-spacing:0.1em;color:var(--ink-mute);">見える光の色</th>')
    return ('<div style="overflow-x:auto;"><table style="border-collapse:collapse;margin:0.4rem auto;min-width:300px;font-size:0.9rem;">'
            f'<thead><tr>{head}</tr></thead><tbody>{tr}</tbody></table></div>'
            '<div class="viz-caption" style="margin-top:0.5rem;">○=刺激あり／×=刺激なし。赤→L・緑→M・青→S。3つすべて刺激で白に見える。</div>')

# ---------- digest ----------
_ICON = {
    "01": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    "02": '<circle cx="13.5" cy="6.8" r="1.2"/><circle cx="17.4" cy="10.6" r="1.2"/><circle cx="8.4" cy="7.6" r="1.2"/><circle cx="6.6" cy="12.4" r="1.2"/><path d="M12 21.5A9.5 9.5 0 1 1 12 2.5c5 0 9 3.4 9 7.8 0 2.9-2.4 3.9-3.9 3.9h-2.1a2 2 0 0 0-1.5 3.2 1.5 1.5 0 0 1-1.3 2.6z"/>',
    "03": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
}
def dg_icon(num):
    p = _ICON.get(num, "")
    if not p: return ""
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

# ============================================================
# WELCOME
# ============================================================
WELCOME = '''  <section class="stage active" data-stage-name="START">
    <div class="welcome-kicker">
      <span class="num">02</span>
      <span>2章 思考のステップ2</span>
    </div>
    <h1 class="welcome-title-en">Additive &amp;<br>Subtractive Color<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">加法混色と減法混色</h2>
    <p class="welcome-lede">
      人間が色を見る仕組み(L・M・S錐体)から出発し、ディスプレイの光の三原色(加法混色)とプリンタの色の三原色(減法混色)のちがいを、共通テスト型の思考問題で確かめる。インクが「どの光を吸収するか」を軸に、反射光と見える色を順に推論する。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">review</div>
        <div class="welcome-meta-value">3<span class="unit">領域</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">2<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">20<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">2章 思考ステップ2</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー 色を見る仕組み・加法/減法混色・インクの吸収を確認(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>演習</strong>ー 問(ア〜エ)を自己採点、解いて定着を5択で採点</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>結果</strong>ー 完答数と間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>'''

# ============================================================
# REVIEW(3 モジュール)
# ============================================================
M01_BODY = '''        <p style="font-size:0.95rem;color:var(--ink-soft);line-height:1.9;margin-bottom:0.6rem;">人間の目は網膜の錐体細胞で色を感じる。おもに赤に反応するL錐体、緑に反応するM錐体、青に反応するS錐体の3種類があり、どれが刺激されるかの組合せで色が決まる。すべて刺激されると白に見える。なお、この表は問題を解くために、各錐体を「刺激あり／なし」の二状態に単純化したモデルである(実際の錐体の反応は連続的)。</p>
        ''' + cone_table()

M02_BODY = svg_colormix() + '''
        <div class="viz">
          <span class="viz-label">TWO WAYS — 足し算の色 / 引き算の色</span>
          <div class="viz-caption"></div>
          <div class="compare">
            <div class="compare-col left">
              <h5>加法混色(光)</h5>
              <div class="row"><span class="k">使う場所</span><span class="v">ディスプレイ</span></div>
              <div class="row"><span class="k">三原色</span><span class="v">赤・緑・青(RGB)</span></div>
              <div class="row"><span class="k">混ぜると</span><span class="v">明るく→白</span></div>
            </div>
            <div class="compare-col right">
              <h5>減法混色(色)</h5>
              <div class="row"><span class="k">使う場所</span><span class="v">プリンタ</span></div>
              <div class="row"><span class="k">三原色</span><span class="v">シアン・マゼンタ・イエロー(CMY)</span></div>
              <div class="row"><span class="k">混ぜると</span><span class="v">暗く→黒</span></div>
              <div class="row"><span class="k">実際の印刷</span><span class="v">黒(K)も併用</span></div>
            </div>
          </div>
        </div>'''

M03_BODY = '''        <div class="viz">
          <span class="viz-label">INK ABSORBS LIGHT — インクは光を引く</span>
          <div class="viz-caption">白色光(赤+緑+青)のうち、インクが特定の色を吸収し、残りを反射する。反射した光が錐体を刺激して色に見える。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">シアン</div><span class="bound">赤を吸収</span><div class="desc">緑+青を反射 → M錐体・S錐体を刺激 → シアンに見える。</div></div>
            <div class="bd-card"><div class="key">マゼンタ</div><span class="bound">緑を吸収</span><div class="desc">赤+青を反射 → L錐体・S錐体を刺激 → マゼンタに見える。</div></div>
            <div class="bd-card"><div class="key">イエロー</div><span class="bound">青を吸収</span><div class="desc">赤+緑を反射 → L錐体・M錐体を刺激 → イエローに見える。</div></div>
          </div>
        </div>
        <div class="bd-warn"><strong>重ね合わせ:</strong> マゼンタ+イエローは緑と青の両方を吸収するので、残る赤だけを反射する。だから赤(L錐体のみ)に見える。</div>'''

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
    digest_mod("01", "How We See Color", "色はどうやって見えている?", "色を見る仕組み(L・M・S錐体)", "目の3種類の錐体(赤=L・緑=M・青=S)が、どの組合せで刺激されるかで色が決まる。", M01_BODY, hero=True),
    digest_mod("02", "Additive vs Subtractive", "光の三原色と色の三原色は何がちがう?", "加法混色と減法混色", "光(RGB)は重ねるほど明るく白へ、色のインク(CMY)は重ねるほど暗く黒へ向かう。", M02_BODY),
    digest_mod("03", "Ink Absorbs Light", "インクの色はどう決まる?", "インクが光を吸収する仕組み", "インクは光を「引く」。何色の光を吸収し、何色を反射するかで見える色が決まる。", M03_BODY),
]) + '''
    </div>
  </section>'''

# ============================================================
# 練習(2問)
# ============================================================
T = 2
# --- 練習1: 問 ア〜エ(self×4) ---
GUNS = ('<div class="option-legend" style="margin:0.6rem 0;">'
        '<div class="option-legend-title">ア・ウ の解答群</div>'
        '<div class="option-legend-list">'
        '<span class="option-legend-item"><span class="let">⓪</span>L錐体のみ</span>'
        '<span class="option-legend-item"><span class="let">①</span>M錐体のみ</span>'
        '<span class="option-legend-item"><span class="let">②</span>S錐体のみ</span>'
        '<span class="option-legend-item"><span class="let">③</span>L錐体とM錐体</span>'
        '<span class="option-legend-item"><span class="let">④</span>M錐体とS錐体</span>'
        '<span class="option-legend-item"><span class="let">⑤</span>L錐体とS錐体</span>'
        '</div></div>'
        '<div class="option-legend" style="margin:0.6rem 0;">'
        '<div class="option-legend-title">イ の解答群</div>'
        '<div class="option-legend-list">'
        '<span class="option-legend-item"><span class="let">⓪</span>赤い光のみ</span>'
        '<span class="option-legend-item"><span class="let">①</span>緑の光のみ</span>'
        '<span class="option-legend-item"><span class="let">②</span>青い光のみ</span>'
        '<span class="option-legend-item"><span class="let">③</span>赤い光と緑の光</span>'
        '<span class="option-legend-item"><span class="let">④</span>緑の光と青の光</span>'
        '<span class="option-legend-item"><span class="let">⑤</span>赤い光と青い光</span>'
        '</div></div>'
        '<div class="option-legend" style="margin:0.6rem 0;">'
        '<div class="option-legend-title">エ の解答群</div>'
        '<div class="option-legend-list">'
        '<span class="option-legend-item"><span class="let">⓪</span>赤</span>'
        '<span class="option-legend-item"><span class="let">①</span>緑</span>'
        '<span class="option-legend-item"><span class="let">②</span>青</span>'
        '<span class="option-legend-item"><span class="let">③</span>シアン</span>'
        '<span class="option-legend-item"><span class="let">④</span>マゼンタ</span>'
        '<span class="option-legend-item"><span class="let">⑤</span>イエロー</span>'
        '</div></div>')

P1_LEAD = ('人間は物の色を光の反射によって見ている。例えば、赤のインクは当てられた光の中から赤い光だけを反射して、ほかの色の光は吸収するため赤く見える。'
           'あるカラープリンタは、色の三原色であるシアン、マゼンタ、イエローの3色のインクと、その重ね合わせによって色を表現している。'
           'シアンのインクは、光の三原色である赤、緑、青の光を重ね合わせて当てたときに、赤い光を吸収する性質があり、このインクが反射した光は <strong>ア</strong> を刺激するため、シアンに見える。'
           'また、マゼンタとイエローのインクを重ね合わせると、それぞれのインクが <strong>イ</strong> を吸収し、反射した光は <strong>ウ</strong> を刺激するため、<strong>エ</strong> に見えることになる。'
           '<div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-top:0.4rem;">'
           + fig_box("fig1-cyan-absorption.jpeg", "シアンのインクが赤い光を吸収し、緑と青の光を反射してM錐体とS錐体を刺激する図。", "シアン:赤を吸収 → 緑・青を反射", 300, 270)
           + fig_box("fig2-magenta-yellow-absorption.jpeg", "マゼンタとイエローのインクが緑と青の光を吸収し、赤の光を反射してL錐体を刺激する図。", "マゼンタ+イエロー:緑・青を吸収 → 赤を反射", 300, 270)
           + '</div>' + GUNS)

P1 = stage_self("p1", "問", 1, T, "思考のステップ2 問", "〈加法混色と減法混色〉", "物の色の見え方", P1_LEAD,
    "\n".join([
        self_row(0, ("ア", "シアンのインクが反射した光が刺激するもの。"), M("④ M錐体とS錐体", "シアンは赤い光を吸収し、緑と青の光を反射する。緑→M錐体、青→S錐体を刺激する。")),
        self_row(1, ("イ", "マゼンタとイエローのインクが、それぞれ吸収する光。"), M("④ 緑の光と青の光", "マゼンタは緑の光を吸収し、イエローは青の光を吸収する。")),
        self_row(2, ("ウ", "マゼンタ+イエローが反射した光が刺激するもの。"), M("⓪ L錐体のみ", "緑と青が吸収されるので、残る赤の光だけが反射する。赤→L錐体のみを刺激する。")),
        self_row(3, ("エ", "そのとき見える色。"), M("⓪ 赤", "反射するのは赤の光だけなので、赤に見える。")),
    ]),
    fb("解説", sec("考えて納得(筋道)", '''<ul>
        <li><strong>Step 1</strong> シアンのインクは白(赤+緑+青)の光から赤を吸収し、緑と青を反射する。緑と青は M錐体とS錐体 を刺激する(=ア)。</li>
        <li><strong>Step 2</strong> マゼンタは緑を、イエローは青を吸収する(=イ)。重ねると緑と青がともに吸収され、残る赤だけが反射する。赤は L錐体のみ を刺激し(=ウ)、赤に見える(=エ)。</li>
      </ul>''')
       + correct_line("ア ④ ／ イ ④ ／ ウ ⓪ ／ エ ⓪")
       + svg_colormix()))

# --- 練習2: 解いて定着(single 5択) ---
P2_LEAD = ('カラーコピー機は、画像を赤、緑、青のフィルタを通して読み取り、色分解することによって、シアン、マゼンタ、イエローの各色のインク(トナー)の濃度を調整している。'
           '赤のフィルタを通して画像を見た場合、フィルタによって反射光の中の赤い光のみが透過され、ほかの色の反射光は吸収するため、このとき黒くなっている部分の反射光は緑と青であるといえる。'
           '赤、緑、青のフィルタを通して読み取った画像の黒の濃淡とシアン、マゼンタ、イエローの各色のインク(トナー)の濃度の関係について述べたものとして最も適当なものを、次の⓪〜④のうちから一つ選べ。')

P2 = stage_single("p2", "定着", 2, T, "思考のステップ2 解いて定着", "〈加法混色と減法混色〉", "色分解とインク濃度", P2_LEAD,
    [("⓪", "赤のフィルタを通して読み取った画像の黒の濃度が薄い部分には、マゼンタのインク(トナー)を濃く印刷する。"),
     ("①", "青のフィルタを通して読み取った画像の黒の濃度が濃い部分には、シアンのインク(トナー)を薄く印刷する。"),
     ("②", "緑のフィルタを通して読み取った画像の黒の濃度が濃い部分には、マゼンタのインク(トナー)を濃く印刷する。"),
     ("③", "赤のフィルタを通して読み取った画像の黒の濃度が薄い部分には、イエローのインク(トナー)を薄く印刷する。"),
     ("④", "緑のフィルタを通して読み取った画像の黒の濃度が濃い部分には、シアンのインク(トナー)を濃く印刷する。")],
    2,
    fb("解説", correct_line("②")
       + sec("考え方", "この問題の単純化したRGB/CMYモデルで考える。あるフィルタを通して黒く見える部分は、その色の光が少なく、ほかの2色の光が反射している部分にあたる。")
       + sec("各フィルタの黒い部分の色", '''<ul>
        <li><strong>赤フィルタ</strong>の黒い部分 → 反射光は緑+青 = <strong>シアン</strong> → シアンを濃く印刷。</li>
        <li><strong>緑フィルタ</strong>の黒い部分 → 反射光は赤+青 = <strong>マゼンタ</strong> → マゼンタを濃く印刷。これが②。</li>
        <li><strong>青フィルタ</strong>の黒い部分 → 反射光は赤+緑 = <strong>イエロー</strong> → イエローを濃く印刷。</li>
      </ul>よって、緑フィルタの黒が濃い部分にマゼンタを濃く印刷する②が正しい。''')
       + svg_colormix()))

PRACTICE = P1 + "\n\n" + P2

# ============================================================
# SUMMARY
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
      <div class="summary-grade" id="summary-grade">—<span class="denom">/2</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">2問の練習問題のうち、何問完答できたか。</div>
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
# 組み立て + splice
# ============================================================
NEW_MAIN = "<main id=\"stages\">\n\n" + WELCOME + "\n\n" + REVIEW + "\n\n" + PRACTICE + "\n\n" + SUMMARY + "\n\n</main>"
NEW_MAIN = NEW_MAIN.replace("，", "、")

m0 = html.index("<main id=\"stages\">")
m1 = html.index("</main>") + len("</main>")
html = html[:m0] + NEW_MAIN + html[m1:]

html = html.replace("<title>デジタル化された情報とその表し方 | Practice Lab</title>",
                    "<title>加法混色と減法混色(思考のステップ2) | Practice Lab</title>")

TL = '''  const TIMELINE_ENTRIES = [
    { idx: 0, group: 'overview', num: '00', label: 'スタート' },
    { idx: 1, group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2, group: 'practice', num: '問', label: '〈ア〜エ〉色の見え方', probId: 'p1' },
    { idx: 3, group: 'practice', num: '定着', label: '〈色分解とインク〉', probId: 'p2' },
    { idx: 4, group: 'result',  num: '✓',  label: '結果サマリ' }
  ];'''
html = re.sub(r"  const TIMELINE_ENTRIES = \[.*?\];", TL, html, count=1, flags=re.S)

html = html.replace("if (sbScore) sbScore.textContent = full + '/14';",
                    "if (sbScore) sbScore.textContent = full + '/2';")

PROBS = '''  const PROBLEMS = [
    { id: 'p1', label: '問', name: '〈ア〜エ〉色の見え方', stageIdx: 2 },
    { id: 'p2', label: '定着', name: '〈色分解とインク〉', stageIdx: 3 }
  ];'''
html = re.sub(r"  const PROBLEMS = \[.*?\];", PROBS, html, count=1, flags=re.S)

html = html.replace("animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/14</span>');",
                    "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/2</span>');")
html = html.replace("    if (fullCount >= 11) grade.classList.add('s-high');\n    else if (fullCount >= 7) grade.classList.add('s-mid');",
                    "    if (fullCount >= 2) grade.classList.add('s-high');\n    else if (fullCount >= 1) grade.classList.add('s-mid');")

SRC.write_text(html, encoding="utf-8")
print("built:", SRC)
print("len:", len(html))
print("helpers ready")

