# -*- coding: utf-8 -*-
"""
思考のステップ4「真理値表」ビルダー
- ベース = 02-thinking-step-2/index.html(self/single 型・エンジン内蔵)を読み、<main> と JS データ配列だけ差し替えて ./index.html に書く
- エンジン(CSS/JS)保全
- 原本: ベストフィット 3章 思考のステップ4(問題 docx)/ 解答 docx p.63「思考のステップ4 解いて定着!」
- 図: 問題 docx の word/media を抽出して assets/ に置いた(fig1〜fig11。対応は下の fig_box / img の呼び出しを参照)
"""
import re, pathlib
HERE = pathlib.Path(__file__).parent
BASE = HERE.parent / "02-thinking-step-2" / "index.html"
OUT = HERE / "index.html"
html = BASE.read_text(encoding="utf-8")

# ---------- ヘルパー(02-thinking-step-2 と同じ組み方) ----------
def fig_box(src, alt, cap, maxw=320, imgw=280):
    return (f'<figure style="margin: 0.7rem auto; padding: 0.8rem 1rem; background: var(--bg-card); '
            f'border: 1px solid var(--line); border-radius: 8px; display: inline-block; max-width: {maxw}px; text-align: center;">'
            f'<img src="assets/{src}" alt="{alt}" style="display: block; width: 100%; height: auto; max-width: {imgw}px; margin: 0 auto;">'
            f'<figcaption style="margin-top: 0.5rem; font-family: var(--f-mono); font-size: 0.74rem; color: var(--ink-mute); line-height:1.5;">{cap}</figcaption>'
            f'</figure>')

def img(src, alt, maxw=300):
    return f'<img src="assets/{src}" alt="{alt}" style="display:block;width:100%;max-width:{maxw}px;height:auto;margin:0.35rem 0 0.1rem;">'

PH = "数や語、出力を書いてみてください(任意)"
def self_row(sub, q, model_html, ph=PH):
    return f'''        <div class="self-row" data-sub="{sub}">
          <div class="self-q"><span class="self-sub-label">{q[0]}</span>{q[1]}</div>
          <textarea class="self-input" rows="2" placeholder="{ph}"></textarea>
          <button type="button" class="self-reveal" data-action="self-reveal">模範解答を見る</button>
          <div class="self-model">
            <div class="self-model-label">模範解答</div>
            {model_html}
            <div class="self-rate">
              <span class="self-rate-q">模範解答と照らして:</span>
              <button type="button" class="self-rate-btn ok" data-mark="ok">書けた ○</button>
              <button type="button" class="self-rate-btn no" data-mark="no">まだ △</button>
            </div>
          </div>
        </div>'''

def M(ans, kaisetsu):
    return f'<p><strong>{ans}</strong><br>{kaisetsu}</p>'

def _split_lead(lead_html):
    mm = re.search(r'<figure|<blockquote|<div|<p ', lead_html)
    if not mm: return lead_html, ""
    i = mm.start(); return lead_html[:i].rstrip(), "\n      " + lead_html[i:]

def stage_self(probid, qnum, idx, total, src, kakko, title, lead_html, rows_html, fb_html):
    lead_html, block = _split_lead(lead_html)
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
    lead_html, block = _split_lead(lead_html)
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

BX = lambda s: f'<span style="display:inline-block;min-width:1.6em;text-align:center;border:1.5px solid var(--action);border-radius:4px;padding:0 0.3em;margin:0 0.15em;font-weight:700;color:var(--action);">{s}</span>'

def tt_html(heads, rows, out_from=None, wrong=None, cap=''):
    th = ''.join(f'<th style="padding:0.35rem 0.65rem;font-family:var(--f-la);font-size:0.82rem;letter-spacing:0.06em;color:var(--ink-mute);border-bottom:1.5px solid var(--line);">{h}</th>' for h in heads)
    tr = ''
    for r, row in enumerate(rows):
        tds = ''
        for c, v in enumerate(row):
            st = 'text-align:center;font-family:var(--f-mono);font-weight:700;padding:0.28rem 0.65rem;border-top:1px solid var(--line-soft);'
            if out_from is not None and c >= out_from: st += 'color:var(--action);'
            if wrong and (r, c) in wrong: st += 'color:#C8102E;background:rgba(200,16,46,0.08);text-decoration:line-through;'
            tds += f'<td style="{st}">{v}</td>'
        tr += f'<tr>{tds}</tr>'
    return ('<div style="overflow-x:auto;"><table style="border-collapse:collapse;margin:0.4rem auto;font-size:0.92rem;background:var(--bg-card);border:1px solid var(--line);border-radius:8px;">'
            f'<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            + (f'<div class="viz-caption" style="margin-top:0.4rem;">{cap}</div>' if cap else ''))

def svg_symbols():
    ink = "#1A2B47"
    w = lambda d: f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>'
    AND = w("M20,40 H60") + w("M20,70 H60") + f'<path d="M60,25 h30 a30,30 0 0 1 0,60 h-30 z" fill="#fff" stroke="{ink}" stroke-width="3"/>' + w("M120,55 H150")
    OR = w("M190,40 H236") + w("M190,70 H236") + f'<path d="M225,25 Q262,25 290,55 Q262,85 225,85 Q243,55 225,25 Z" fill="#fff" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>' + w("M290,55 H320")
    NOT = w("M360,55 H395") + f'<path d="M395,32 L440,55 L395,78 Z" fill="#fff" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/><circle cx="446" cy="55" r="6" fill="#fff" stroke="{ink}" stroke-width="3"/>' + w("M452,55 H490")
    return (f'<svg class="viz-svg wide" viewBox="0 0 510 110" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="左から論理積回路(AND回路)、論理和回路(OR回路)、否定回路(NOT回路)の図記号">{AND}{OR}{NOT}</svg>')

# ---------- 検算(原本の解答と一致させる) ----------
R2 = [(a, b) for a in (0, 1) for b in (0, 1)]
R3 = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
X2 = [1 if a == b else 0 for a, b in R2]                              # 図2(同じ側で点灯)
X3 = [1 if (a ^ c) == b else 0 for a, b, c in R3]                     # 図4(C=1 で交差)
assert X2 == [1, 0, 0, 1] and X3 == [1, 0, 0, 1, 0, 1, 1, 0]          # 解答 docx p.63 の表
Q1 = {  # 問1 ⓪〜③(問題 docx の図を読んだ構成)
    "⓪": [(a | (1 - b)) | (a & (1 - b)) for a, b in R2],
    "①": [(a | b) & ((1 - a) | (1 - b)) for a, b in R2],
    "②": [1 - ((a | b) & (1 - (a & b))) for a, b in R2],
    "③": [((a | b) & (1 - a)) | (1 - b) for a, b in R2],
}
assert [k for k, v in Q1.items() if v == X2] == ["②"]                  # 解答: ア ②
assert Q1["⓪"] == [1, 0, 1, 1] and Q1["①"] == [0, 1, 1, 0] and Q1["③"] == [1, 1, 1, 0]   # 解答の消去の順と一致

# ---------- digest ----------
_ICON = {
    "01": '<path d="M4 6h7a6 6 0 0 1 0 12H4z"/><path d="M1 9.5h3M1 14.5h3M17 12h5"/>',
    "02": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M12 4v16"/>',
    "03": '<path d="M5 5l11 7-11 7z"/><circle cx="18.5" cy="12" r="1.8"/>',
}
def dg_icon(num):
    p = _ICON.get(num, "")
    return ('<span class="dg-ico" aria-hidden="true" style="display:inline-flex;width:18px;height:18px;color:var(--action);flex:none;align-items:center;justify-content:center;margin-right:0.15rem;">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%;height:100%">{p}</svg></span>') if p else ""

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
      <span class="num">03</span>
      <span>3章 思考のステップ4</span>
    </div>
    <h1 class="welcome-title-en">Truth<br>Tables<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">真理値表</h2>
    <p class="welcome-lede">
      一つの電灯を2か所のスイッチで点けたり消したりする3路スイッチの配線を題材に、0と1のすべての組合せを重複や漏れなく並べて真理値表を作る手順を、共通テスト型の思考問題で確かめる。そのうえで、同じ結果になる論理回路を入力の組合せごとに絞り込み、4路スイッチを加えた3入力の真理値表まで作る。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">review</div>
        <div class="welcome-meta-value">3<span class="unit">領域</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">3<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">25<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">3章 思考ステップ4</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー 基本の論理回路・真理値表・図記号を確認(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>演習</strong>ー 問(考えて納得の空欄と出力X)と問2を自己採点、問1を4択で採点</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>結果</strong>ー 完答数と間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>'''

# ============================================================
# REVIEW(3 モジュール・演習の答えは出さない)
# ============================================================
M01_BODY = ('''        <div class="viz">
          <span class="viz-label">BASIC GATES — 三つの基本の論理回路</span>
          <div class="viz-caption">コンピュータで演算や制御を行う回路を論理回路という。基本になるのは次の三つ。</div>
          <div class="bd-grid">
            <div class="bd-card"><div class="key">論理積回路（AND回路）</div><span class="bound">ともに1で1</span><div class="desc">二つの入力と一つの出力をもつ回路で，二つの入力がともに1のときだけ，出力が1になる回路。</div>'''
  + tt_html(["A", "B", "X"], [[a, b, a & b] for a, b in R2], out_from=2) + '''</div>
            <div class="bd-card"><div class="key">論理和回路（OR回路）</div><span class="bound">いずれか一方が1で1</span><div class="desc">二つの入力と一つの出力をもつ回路で，入力のいずれか一方が1であれば，出力が1になる回路。</div>'''
  + tt_html(["A", "B", "X"], [[a, b, a | b] for a, b in R2], out_from=2) + '''</div>
            <div class="bd-card"><div class="key">否定回路（NOT回路）</div><span class="bound">反転</span><div class="desc">一つの入力と一つの出力をもつ回路で，入力した信号を反転した値を出力信号とする回路。</div>'''
  + tt_html(["A", "X"], [[0, 1], [1, 0]], out_from=1) + '''</div>
          </div>
        </div>
        <div class="bd-warn"><strong>OR回路の読み方:</strong> 「いずれか一方が1であれば」なので、両方が1のときも出力は1になる。</div>''')

M02_BODY = '''        <div class="viz">
          <span class="viz-label">TRUTH TABLE — 入力の組合せと出力の一覧</span>
          <div class="viz-caption">すべての入力の組合せと，対応する出力の関係を示す表を真理値表という。</div>
          <div class="compare">
            <div class="compare-col left">
              <h5>見出し</h5>
              <div class="row"><span class="k">入力</span><span class="v">A、B など(入力の数だけ列を作る)</span></div>
              <div class="row"><span class="k">出力</span><span class="v">X など</span></div>
            </div>
            <div class="compare-col right">
              <h5>行</h5>
              <div class="row"><span class="k">1行</span><span class="v">入力の組合せ1つ分</span></div>
              <div class="row"><span class="k">出力の欄</span><span class="v">その組合せのときの出力(0か1)</span></div>
            </div>
          </div>
        </div>
        <div class="bd-warn"><strong>並べる順番:</strong> 組合せを思いついた順に書くと、同じ行を2回書いたり、1行抜けたりしやすい。決まった手順で並べる方法を、演習の「考えて納得！」で確かめる。</div>'''

M03_BODY = ('''        <div class="viz">
          <span class="viz-label">SYMBOLS — 図記号の見分け方</span>
          <div class="viz-caption">ベストフィット例題48:「ANDはD，ORはR（丸み『）』）がある」と覚える。</div>
          <div class="viz-svg-wrap">''' + svg_symbols() + '''</div>
          <div style="display:flex;justify-content:space-around;gap:0.4rem;font-size:0.8rem;font-weight:700;color:var(--ink-soft);text-align:center;margin-top:0.3rem;"><span>論理積回路<br>(AND回路)</span><span>論理和回路<br>(OR回路)</span><span>否定回路<br>(NOT回路)</span></div>
        </div>
        <div class="bd-warn"><strong>○ は否定:</strong> 図記号の出力側に付いた ○ は否定(反転)を表す。論理和回路（OR回路）の図記号に ○ が付いたものを否定論理和回路（NOR回路）、論理積回路（AND回路）の図記号に ○ が付いたものを否定論理積回路（NAND回路）と呼ぶ。回路の図は、入力側から順に、線の上に0と1を書き込みながらたどる。</div>''')

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
    digest_mod("01", "Basic Gates", "AND・OR・NOT はそれぞれ何を出す?", "基本の論理回路", "入力の0と1に対して出力が決まる回路。基本は論理積回路・論理和回路・否定回路の三つ。", M01_BODY, hero=True),
    digest_mod("02", "Truth Table", "真理値表には何を書く?", "真理値表", "すべての入力の組合せと、対応する出力の関係を示す表。", M02_BODY),
    digest_mod("03", "Gate Symbols", "論理回路の図はどう読む?", "図記号の見分け方", "AND は D の形、OR は丸みがある。出力側の ○ は否定を表す。", M03_BODY),
]) + '''
    </div>
  </section>'''

# ============================================================
# 練習(3問)
# ============================================================
T = 3
# --- 練習1: 問(図2 の真理値表)+ 考えて納得の空欄 A〜D ---
KANGAETE = ('<div class="option-legend" style="margin:0.9rem 0 0.6rem;">'
  '<div class="option-legend-title">考えて納得！</div>'
  '<div style="font-size:0.93rem;line-height:1.95;color:var(--ink-soft);">'
  '<p>次のようにすると，0と1のすべての組合せを重複や漏れがなく作成できる。</p>'
  f'<p><strong>Step 1</strong>…論理回路の入力と出力の数に応じて，真理値表の一番上に見出しを作る<br>さらに，入力の数に応じて，行数を設定した表枠を作る<br>入力の数は，AとBの2なので，表の行数は 2<sup>{BX("A")}</sup> ＝{BX("B")}となる。</p>'
  f'<p><strong>Step 2</strong>…入力の枠に0と1のすべての組合せを書く<br>①　一つ目の入力（A）について<br>行の{BX("C")}に0を，{BX("D")}に1を書く。<br>②　次の入力（B）について<br>①で0を書いた行の{BX("C")}に0を，{BX("D")}に1を書く。<br>①で1を書いた行の{BX("C")}に0を，{BX("D")}に1を書く。</p>'
  '<p><strong>Step 3</strong>…入力に応じた出力を一つずつ考えて記入する<br>「入力A（スイッチA）が0，入力B（スイッチB）が0のとき，出力X（電灯）は1（点灯）」</p>'
  '</div></div>')

P1_LEAD = ('一つの電灯を2か所のスイッチで点灯または消灯できるようにするため，図1のような「3路スイッチ」が使用される。例えば，階段下の1階のスイッチで電灯を点灯し，上にあがって2階のスイッチで電灯を消灯する場合や，廊下の一端のスイッチで電灯を点灯し，廊下を歩いていき，もう一方の端のスイッチで電灯を消灯する場合がこれにあたる。'
  '<div style="text-align:center;">' + fig_box("fig1-three-way-switch.jpeg", "3路スイッチの図。スイッチを切り替えると、左の端子につながる配線が上側と下側で切り替わる。", "図1　3路スイッチ", 440, 420) + '</div>'
  '<p class="problem-q">この回路の配線は，図2のようになっている。3路スイッチはAとBの二つあり，上側に切り替わったときは0，下側に切り替わったときは1とし，電灯Xが点灯したときは1，消灯したときは0とする。</p>'
  '<div style="text-align:center;">' + fig_box("fig2-three-way-wiring.jpeg", "電源、電灯X、スイッチA、スイッチBの配線図。AとBの間は上の配線(0)と下の配線(1)の2本でつながる。", "図2　配線の例", 480, 460) + '</div>'
  '<p class="problem-q">このとき，入力をA・B，出力をXとして，図2の回路の真理値表を作成せよ。</p>'
  + KANGAETE)

P1 = stage_self("p1", "問", 1, T, "思考のステップ4 問・考えて納得！", "〈真理値表〉", "3路スイッチの真理値表", P1_LEAD,
    "\n".join([
        self_row(0, ("A", "Step 1 の空欄 A に入る数。"), M("2", "入力はAとBの二つなので、2の2乗の「2」が入る。")),
        self_row(1, ("B", "Step 1 の空欄 B に入る数(表の行数)。"), M("4", "2<sup>2</sup> = 4。入力が二つなら組合せは4通りなので、表は4行になる。")),
        self_row(2, ("C", "Step 2 の空欄 C に入る語。"), M("上半分", "一つ目の入力Aは、4行のうち上半分の2行に0を書く。")),
        self_row(3, ("D", "Step 2 の空欄 D に入る語。"), M("下半分", "下半分の2行に1を書く。次の入力Bも、Aが0の2行とAが1の2行のそれぞれで、上半分に0、下半分に1を書く。")),
        self_row(4, ("X", "図2の回路の真理値表の出力Xを、上の行(A=0・B=0)から順に4つ。"), M("1・0・0・1", "AとBが同じ側(00、11)に切り替わっていると、上の配線か下の配線のどちらかで電源と電灯がつながり、点灯する。違う側(01、10)では、配線がスイッチBのところで切れて消灯する。")),
    ]),
    fb("解説", sec("考えて納得(筋道)", '''<ul>
        <li><strong>Step 1</strong> 入力はAとBの二つなので、表の行数は 2<sup>2</sup> = 4(A=2、B=4)。見出しに入力A・Bと出力Xを書き、4行の表枠を作る。</li>
        <li><strong>Step 2</strong> 一つ目の入力Aは、行の上半分に0、下半分に1(C=上半分、D=下半分)。次の入力Bは、Aが0の2行とAが1の2行のそれぞれで、上半分に0、下半分に1。これで 00・01・10・11 がそろう。</li>
        <li><strong>Step 3</strong> 図2の配線で、行ごとに電灯が点灯するかを確かめてXを書く。AとBが同じ側(00、11)なら点灯して1、違う側(01、10)なら消灯して0。</li>
      </ul><div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-top:0.5rem;">'''
       + fig_box("fig5-step1-frame.png", "見出し(入力A・B、出力X)と4行の空の表枠。", "Step 1　見出しと4行の表枠", 280, 250)
       + fig_box("fig6-step2-first-input.png", "Aの列の上半分2行に0、下半分2行に1を書いた表。", "Step 2 ①　Aは上半分に0・下半分に1", 280, 250)
       + fig_box("fig7-step2-second-input.png", "Aが0の2行のうち、上の行のBに0、下の行のBに1を書いた表。", "Step 2 ②　Bもまとまりごとに上半分0・下半分1", 280, 250)
       + '</div>')
       + correct_line("A 2 ／ B 4 ／ C 上半分 ／ D 下半分 ／ X 上から 1・0・0・1")
       + sec("図2の回路の真理値表", tt_html(["A", "B", "X"], [[a, b, X2[i]] for i, (a, b) in enumerate(R2)], out_from=2, cap="AとBが同じ側で点灯(1)、違う側で消灯(0)。"))
       + '''          <div class="fb-section">
            <div class="fb-section-title">配線をたどる</div>
            <div class="fb-explain"><div class="compare">
              <div class="compare-col left"><h5>同じ側(00・11)</h5><div class="row"><span class="k">A=0・B=0</span><span class="v">上の配線で電源と電灯がつながる → 点灯</span></div><div class="row"><span class="k">A=1・B=1</span><span class="v">下の配線でつながる → 点灯</span></div></div>
              <div class="compare-col right"><h5>違う側(01・10)</h5><div class="row"><span class="k">A=0・B=1</span><span class="v">上の配線とスイッチBがつながらない → 消灯</span></div><div class="row"><span class="k">A=1・B=0</span><span class="v">下の配線とスイッチBがつながらない → 消灯</span></div></div>
            </div></div>
          </div>'''))

# --- 練習2: 解いて定着! 問1(single 4択) ---
P2_LEAD = ('前ページの図2の回路と同じ結果が得られる論理回路を，次の⓪～③のうちから一つ選べ。'
  '<div style="text-align:center;">' + fig_box("fig2-three-way-wiring.jpeg", "電源、電灯X、スイッチA、スイッチBの配線図(再掲)。", "（再掲）図2　配線の例", 380, 360) + '</div>')
P2_OPTS = [
    ("⓪", img("fig8-q1-option0.jpeg", "AとNOT回路で反転したBをOR回路に、AとNOT回路で反転したBをAND回路に入れ、二つの出力をOR回路に入れてXを出す論理回路。")),
    ("①", img("fig9-q1-option1.jpeg", "AとBをOR回路に、NOT回路で反転したAとNOT回路で反転したBをOR回路に入れ、二つの出力をAND回路に入れてXを出す論理回路。")),
    ("②", img("fig10-q1-option2.jpeg", "AとBをOR回路に、AとBのAND回路の出力をNOT回路で反転したものと合わせてAND回路に入れ、その出力をNOT回路で反転してXを出す論理回路。")),
    ("③", img("fig11-q1-option3.jpeg", "AとBのOR回路の出力と、NOT回路で反転したAをAND回路に入れ、その出力とNOT回路で反転したBをOR回路に入れてXを出す論理回路。")),
]
ELIM_ROWS = [[a, b, X2[i]] + [Q1[k][i] for k in ["⓪", "①", "②", "③"]] for i, (a, b) in enumerate(R2)]
ELIM_WRONG = {(i, 3 + j) for i in range(4) for j, k in enumerate(["⓪", "①", "②", "③"]) if Q1[k][i] != X2[i]}
P2 = stage_single("p2", "問1", 2, T, "思考のステップ4 解いて定着！ 問1", "〈真理値表〉", "同じ結果になる論理回路", P2_LEAD, P2_OPTS, 2,
    fb("解説", correct_line("②")
       + sec("解説(ベストフィット)", '''<p>図2の真理値表は，AとBが00のとき1，01のとき0，10のとき0，11のとき1となる。</p>
        <p>まず，入力Aが0，入力Bが0の場合について，⓪～③の論理回路に当てはめていく。論理回路⓪は，入力Aが0，入力Bが0の場合，出力Xは1となる。同様に，論理回路①は0となり，論理回路②は1，論理回路③は1となる。よって，出力Xが0となった論理回路①は候補から外れる。</p>
        <p>次に，入力Aが0，入力Bが1の場合について，⓪，②，③の論理回路に当てはめていく。論理回路⓪は，入力Aが0，入力Bが1の場合，出力Xは0となる。同様に，論理回路②は0，論理回路③は1となる。よって，出力Xが1となった論理回路③は候補から外れる。</p>
        <p>次に，入力Aが1，入力Bが0の場合について，⓪，②の論理回路に当てはめていく。論理回路⓪は，入力Aが1，入力Bが0の場合，出力Xは1となる。同様に，論理回路②は0となる。よって，論理回路⓪は候補から外れ，残った論理回路②が該当する答えになる。</p>
        <p>なお，念のため入力Aが1，入力Bが1の場合の出力Xを確認すると，論理回路②の出力は1となり，真理値表と同じ結果が得られていることがわかる。</p>''')
       + sec("4つの回路の出力を並べる", tt_html(["A", "B", "図2のX", "⓪", "①", "②", "③"], ELIM_ROWS, out_from=2, wrong=ELIM_WRONG, cap="赤の取り消し線が、図2のXと食い違う出力。4行すべてが一致するのは②だけ。"))
       + sec("補足", "<p>②は、OR回路の出力と、AND回路の出力をNOT回路で反転したものをAND回路に入れている。ここまでで「一方のみ1のときだけ1」(0・1・1・0)になり、最後のNOT回路で反転して1・0・0・1、つまり「AとBが同じとき1」になる。1行ずつ当てはめて候補を外していくと、4つの回路の真理値表をすべて作らなくても答えが決まる。</p>")))

# --- 練習3: 解いて定着! 問2(8行の真理値表) ---
P3_LEAD = ('スイッチを一つ増やして，3か所のスイッチで点灯または消灯できるようにするためには，図3のような「4路スイッチ」が使用される。'
  '<div style="text-align:center;">' + fig_box("fig3-four-way-switch.jpeg", "4路スイッチの図。左の状態では2本の配線がまっすぐつながり、右の状態では交差してつながる。", "図3　4路スイッチ", 440, 420) + '</div>'
  '<p class="problem-q">この回路の配線は，図4のようになっている。3路スイッチはAとBの二つあり，上側に切り替わったときは0，下側に切り替わったときは1とし，4路スイッチはスイッチCとして設置し，図3の左の状態が0，右の状態が1とし，電灯Xが点灯したときは1，消灯したときは0とする。</p>'
  '<div style="text-align:center;">' + fig_box("fig4-four-way-wiring.jpeg", "電源、電灯X、スイッチA、スイッチC、スイッチBの配線図。AとCの間、CとBの間はそれぞれ上下2本の配線でつながる。", "図4　配線の例", 520, 500) + '</div>'
  '<p class="problem-q">このとき，入力をA，B，Cとし，出力をXとして，この図4の回路の真理値表を作成せよ。</p>')
P3 = stage_self("p3", "問2", 3, T, "思考のステップ4 解いて定着！ 問2", "〈真理値表〉", "4路スイッチの真理値表", P3_LEAD,
    "\n".join([
        self_row(0, ("入力", "A・B・Cの8行の並び(上の行から)。"), M("000・001・010・011・100・101・110・111", "行数は 2<sup>3</sup> = 8。Aは上半分の4行に0、下半分の4行に1。Bは、Aが同じ値の4行ずつで上半分に0、下半分に1。Cは1行ずつ0と1を交互に書く。")),
        self_row(1, ("X 上", "出力Xの上半分4行(A=0の行)。"), M("1・0・0・1", "AとBが同じ側(B=0)の2行では、C=0なら点灯、C=1なら消灯。AとBが違う側(B=1)の2行では、C=0なら消灯、C=1なら点灯。")),
        self_row(2, ("X 下", "出力Xの下半分4行(A=1の行)。"), M("0・1・1・0", "AとBが違う側(B=0)の2行では、C=0なら消灯、C=1なら点灯。AとBが同じ側(B=1)の2行では、C=0なら点灯、C=1なら消灯。")),
    ]),
    fb("解説", correct_line("入力は 000〜111 の8行 ／ X は上から 1・0・0・1・0・1・1・0")
       + sec("図4の回路の真理値表", tt_html(["A", "B", "C", "X"], [[a, b, c, X3[i]] for i, (a, b, c) in enumerate(R3)], out_from=3))
       + sec("解説(ベストフィット)", '''<p>このスイッチの図を見ると，入力AとBの図での配線の上下が揃っている（例えば00，11）ときは，入力Cが0（図での配線が平行）であれば，電灯は点灯する（出力Xが1）ことがわかる。</p>
        <p>逆に，入力AとBの図での配線の上下が揃っていない（例えば01，10）ときは，入力Cが1（図での配線がクロス）であれば，電灯は点灯する（出力Xが1）ことがわかる。</p>
        <p>よって，これらのことから，A：0，B：0，C：0→X：1，A：1，B：1，C：0→X：1，A：0，B：1，C：1→X：1，A：1，B：0，C：1→X：1　となり，それ以外の組合せは，電灯は点灯しない（出力Xが0）ことがわかる。</p>''')
       + '''          <div class="fb-section">
            <div class="fb-section-title">C の状態で分ける</div>
            <div class="fb-explain"><div class="compare">
              <div class="compare-col left"><h5>C=0(平行)</h5><div class="row"><span class="k">点灯する</span><span class="v">AとBが同じ側(000、110)</span></div><div class="row"><span class="k">消灯する</span><span class="v">AとBが違う側(010、100)</span></div></div>
              <div class="compare-col right"><h5>C=1(クロス)</h5><div class="row"><span class="k">点灯する</span><span class="v">AとBが違う側(011、101)</span></div><div class="row"><span class="k">消灯する</span><span class="v">AとBが同じ側(001、111)</span></div></div>
            </div></div>
          </div>'''
       + sec("補足", "<p>表を上から2行ずつ(A・Bはそのままで、Cだけが違う組)見ると、Xは1と0、0と1、0と1、1と0で、<strong>Cを切り替えるたびに点灯と消灯が入れ替わる</strong>。ほかの2つの入力をそのままにして、Aだけ、またはBだけを切り替えても、同じように入れ替わる。だから3か所のどこからでも電灯を点けたり消したりできる。</p>")))

PRACTICE = P1 + "\n\n" + P2 + "\n\n" + P3

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
      <div class="summary-grade" id="summary-grade">—<span class="denom">/3</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">3問の練習問題のうち、何問完答できたか。</div>
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

html, k = re.subn(r"<title>.*?</title>", "<title>真理値表(思考のステップ4) | Practice Lab</title>", html, count=1); assert k == 1

TL = '''  const TIMELINE_ENTRIES = [
    { idx: 0, group: 'overview', num: '00', label: 'スタート' },
    { idx: 1, group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2, group: 'practice', num: '問', label: '〈A〜D・X〉3路スイッチ', probId: 'p1' },
    { idx: 3, group: 'practice', num: '問1', label: '〈同じ結果の論理回路〉', probId: 'p2' },
    { idx: 4, group: 'practice', num: '問2', label: '〈4路スイッチ・8行〉', probId: 'p3' },
    { idx: 5, group: 'result',  num: '✓',  label: '結果サマリ' }
  ];'''
html, k = re.subn(r"  const TIMELINE_ENTRIES = \[.*?\];", TL, html, count=1, flags=re.S); assert k == 1

PROBS = '''  const PROBLEMS = [
    { id: 'p1', label: '問', name: '〈A〜D・X〉3路スイッチ', stageIdx: 2 },
    { id: 'p2', label: '問1', name: '〈同じ結果の論理回路〉', stageIdx: 3 },
    { id: 'p3', label: '問2', name: '〈4路スイッチ・8行〉', stageIdx: 4 }
  ];'''
html, k = re.subn(r"  const PROBLEMS = \[.*?\];", PROBS, html, count=1, flags=re.S); assert k == 1

for old, new in [
    ("if (sbScore) sbScore.textContent = full + '/2';", "if (sbScore) sbScore.textContent = full + '/3';"),
    ("animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/2</span>');", "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/3</span>');"),
    ("    if (fullCount >= 2) grade.classList.add('s-high');\n    else if (fullCount >= 1) grade.classList.add('s-mid');",
     "    if (fullCount >= 3) grade.classList.add('s-high');\n    else if (fullCount >= 2) grade.classList.add('s-mid');"),
]:
    assert html.count(old) == 1, old[:60]
    html = html.replace(old, new)

for leftover in ["加法混色", "シアン", "ステップ2", "錐体"]:
    assert leftover not in html, leftover

OUT.write_text(html, encoding="utf-8")
print("built:", OUT, "len:", len(html))
