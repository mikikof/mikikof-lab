#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
practices 03-09「2進数と論理演算」ビルダ

- エンジン(CSS / JS ハーネス / サイドバー / トップバー / フッタ)は
  examples/02-07-digital-info-representation.html を 1 文字も変えずに流用する(03-08 と同じ)。
- 差し替えるのは <main id="stages"> の中身と、JS の TIMELINE_ENTRIES / PROBLEMS /
  サマリ分母・閾値 だけ。
- 問題文・選択肢・解答・原本解説は _source の docx から逐語(「，」→「、」のみ)。
  下付きの (2) は <sub>(2)</sub>、べきは <sup>n</sup> で組む。
- 原本の図は assets/ に抽出済み(問題 docx 36 枚 + 解答 docx 10 枚)。
- 解答の数値はすべて計算で独立に検算してから書いた(末尾 selfcheck)。
"""
import re
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PRACTICES = HERE.parent.parent
SRC = PRACTICES / "skills/interactive-practice/examples/02-07-digital-info-representation.html"
OUT = HERE / "index.html"


# ============================================================
# 記法
# ============================================================
def b(s):
    """2 進数の下付き(リテラルの途中で折り返さない)"""
    return '<span style="white-space:nowrap;">%s<sub>(2)</sub></span>' % s


def d(s):
    return '%s<sub>(10)</sub>' % s


def pw(base, n):
    return '%s<sup>%s</sup>' % (base, n)


def ov(s):
    """補集合(上線)"""
    return '<span style="text-decoration: overline;">%s</span>' % s


def blank(label):
    return ('<span style="display:inline-block; min-width:2.4em; padding:0 0.3em; border-bottom:2px solid var(--action); '
            'text-align:center; font-weight:700; color:var(--action);">%s</span>' % label)


# ============================================================
# 共通パーツ(03-08 と同じ)
# ============================================================
def figure(src, alt, caption, fw=360, iw=320):
    return (
        '<figure style="margin: 0.85rem auto 0.2rem; padding: 0.8rem 1rem; background: var(--bg-card); '
        'border: 1px solid var(--line); border-radius: 8px; display: block; max-width: %dpx; text-align: center;">\n'
        '  <img src="%s" alt="%s" style="display: block; width: 100%%; height: auto; max-width: %dpx; margin: 0 auto;">\n'
        '  <figcaption style="margin-top: 0.5rem; font-family: var(--f-mono); font-size: 0.74rem; color: var(--ink-mute); line-height: 1.6;">%s</figcaption>\n'
        '</figure>\n' % (fw, src, alt, iw, caption)
    )


def fig_row(figs):
    """複数の図を横に並べる(スマホでは折り返す)"""
    return ('<div style="display:flex; flex-wrap:wrap; gap:0.6rem; justify-content:center; align-items:flex-start;">\n%s</div>\n'
            % "".join(figs))


def inline_img(src, alt, h=60):
    return ('<img src="%s" alt="%s" style="display:inline-block; height:%dpx; width:auto; vertical-align:middle; '
            'background:#fff; border:1px solid var(--line); border-radius:6px; padding:3px 6px;">' % (src, alt, h))


def quote_box(inner):
    return (
        '<div style="margin: 0.7rem 0 1.1rem; padding: 0.95rem 1.1rem; background: var(--bg-soft); '
        'border-left: 4px solid var(--action-pale2); border-radius: 0 8px 8px 0; '
        'font-family: var(--f-jp-body); font-size: 0.95rem; line-height: 2.05; color: var(--ink);">\n%s</div>\n' % inner
    )


def legend(items, title="選択肢"):
    rows = "".join(
        '      <span class="option-legend-item"><span class="let">(%s)</span>%s</span>\n' % (l, t)
        for l, t in items
    )
    return (
        '<div class="option-legend">\n'
        '  <div class="option-legend-title">%s</div>\n'
        '  <div class="option-legend-list">\n%s'
        '  </div>\n'
        '</div>\n' % (title, rows)
    )


def opts_single(prob_id, correct, items):
    body = "".join(
        '  <label class="opt"><input type="radio" name="%s"><span class="opt-mark"></span>'
        '<span class="opt-text"><span class="opt-letter">(%s)</span>%s</span></label>\n' % (prob_id, l, t)
        for l, t in items
    )
    return '<div class="opts" data-input="single" data-correct="%d">\n%s</div>\n' % (correct, body)


def match_list(options, correct, items):
    rows = ""
    for i, (lbl, text) in enumerate(items):
        rows += (
            '  <div class="match-row" data-sub="%d">\n'
            '    <span class="match-sub-label">%s</span>\n'
            '    <div class="sub-content">\n'
            '      <span class="match-text">%s</span>\n'
            '      <div class="match-pills"></div>\n'
            '    </div>\n'
            '  </div>\n' % (i, lbl, text)
        )
    return ('<div class="match-list" data-input="match" data-options="%s" data-correct="%s">\n%s</div>\n'
            % (options, correct, rows))


def self_list(items):
    """items: [(label or None, question, model_html)]"""
    rows = ""
    for i, (lbl, q, model) in enumerate(items):
        sub = '<span class="self-sub-label">%s</span>' % lbl if lbl else ""
        rows += (
            '  <div class="self-row" data-sub="%d">\n'
            '    <div class="self-q">%s%s</div>\n'
            '    <textarea class="self-input" rows="2" placeholder="自分の答え・考え方を書いてみてください(任意)"></textarea>\n'
            '    <button type="button" class="self-reveal" data-action="self-reveal">模範解答を見る</button>\n'
            '    <div class="self-model">\n'
            '      <div class="self-model-label">模範解答</div>\n'
            '      %s\n'
            '      <div class="self-rate">\n'
            '        <span class="self-rate-q">模範解答と照らして:</span>\n'
            '        <button type="button" class="self-rate-btn ok" data-mark="ok">解けた ○</button>\n'
            '        <button type="button" class="self-rate-btn no" data-mark="no">まだ △</button>\n'
            '      </div>\n'
            '    </div>\n'
            '  </div>\n' % (i, sub, q, model)
        )
    return '<div class="self-list" data-input="self">\n%s</div>\n' % rows


def viz(label, caption, body):
    return ('<div class="viz">\n'
            '  <span class="viz-label">%s</span>\n'
            '  <div class="viz-caption">%s</div>\n'
            '%s</div>\n' % (label, caption, body))


def bd_grid(cards, warn=None):
    body = "".join(
        '    <div class="bd-card"><div class="key">%s</div><span class="bound">%s</span>'
        '<div class="desc">%s</div></div>\n' % (k, bb, dd) for k, bb, dd in cards
    )
    out = '  <div class="bd-grid">\n%s  </div>\n' % body
    if warn:
        out += '  <div class="bd-warn">%s</div>\n' % warn
    return out


def compare2(left, right):
    def col(side, head, rows):
        rr = "".join('      <div class="row"><span class="k">%s</span><span class="v">%s</span></div>\n' % (k, v)
                     for k, v in rows)
        return ('    <div class="compare-col %s">\n      <h5>%s</h5>\n%s    </div>\n' % (side, head, rr))
    return ('  <div class="compare">\n%s%s  </div>\n'
            % (col("left", left[0], left[1]), col("right", right[0], right[1])))


def checklist(items, warn=None):
    body = "".join(
        '    <div class="cl-item"><span class="cl-num">%s</span><span><span class="cl-key">%s</span>%s</span></div>\n'
        % (n, k, t) for n, k, t in items
    )
    out = '  <div class="checklist">\n%s  </div>\n' % body
    if warn:
        out += ('  <div style="margin-top: 0.85rem; padding: 0.7rem 0.95rem; background: var(--action-pale); '
                'border-left: 3px solid var(--action); border-radius: 0 6px 6px 0; font-size: 0.85rem; '
                'color: var(--anchor); line-height: 1.85;">%s</div>\n' % warn)
    return out


def note_box(html):
    return ('  <div style="margin-top: 0.85rem; padding: 0.7rem 0.95rem; background: var(--action-pale); '
            'border-left: 3px solid var(--action); border-radius: 0 6px 6px 0; font-size: 0.85rem; '
            'color: var(--anchor); line-height: 1.85;">%s</div>\n' % html)


def tbl(head, rows, caption=None, mono=False, small=False):
    """簡単な表(横に長ければスクロール)。head: [..] / rows: [[..],..]"""
    fs = "0.82rem" if small else "0.9rem"
    ff = "var(--f-mono)" if mono else "var(--f-jp-body)"
    th = "".join('<th style="padding:0.35rem 0.55rem; border:1px solid var(--line-strong); background:var(--action-pale); '
                 'color:var(--anchor); font-weight:700; white-space:nowrap;">%s</th>' % h for h in head)
    trs = ""
    for r in rows:
        tds = "".join('<td style="padding:0.35rem 0.55rem; border:1px solid var(--line); text-align:center; '
                      'white-space:nowrap;">%s</td>' % c for c in r)
        trs += "      <tr>%s</tr>\n" % tds
    cap = ('<div style="margin-top:0.4rem; font-family: var(--f-mono); font-size:0.74rem; color: var(--ink-mute);">%s</div>\n' % caption) if caption else ""
    return ('<div style="overflow-x:auto; -webkit-overflow-scrolling:touch; margin:0.6rem 0 0.4rem;">\n'
            '  <table style="border-collapse:collapse; margin:0 auto; font-family:%s; font-size:%s; color:var(--ink); background:#fff;">\n'
            '    <thead><tr>%s</tr></thead>\n'
            '    <tbody>\n%s    </tbody>\n'
            '  </table>\n%s</div>\n' % (ff, fs, th, trs, cap))


def truth_table(inputs, rows):
    """真理値表。inputs: ['A','B'] / rows: [([0,0],1), ...]"""
    n = len(inputs)
    head_top = ('<tr><th colspan="%d" style="padding:0.3rem 0.5rem; border:1px solid var(--line-strong); background:var(--action-pale); color:var(--anchor);">入力</th>'
                '<th style="padding:0.3rem 0.5rem; border:1px solid var(--line-strong); background:var(--gold-pale); color:var(--gold-deep);">出力</th></tr>' % n)
    head2 = "<tr>" + "".join('<th style="padding:0.3rem 0.7rem; border:1px solid var(--line-strong); background:#fff; color:var(--anchor);">%s</th>' % i for i in inputs) + \
            '<th style="padding:0.3rem 0.7rem; border:1px solid var(--line-strong); background:#fff; color:var(--gold-deep);">X</th></tr>'
    body = ""
    for ins, out in rows:
        tds = "".join('<td style="padding:0.3rem 0.7rem; border:1px solid var(--line); text-align:center;">%s</td>' % v for v in ins)
        body += '<tr>%s<td style="padding:0.3rem 0.7rem; border:1px solid var(--line); text-align:center; font-weight:700; color:var(--gold-deep);">%s</td></tr>\n' % (tds, out)
    return ('<table style="border-collapse:collapse; margin:0.5rem auto; font-family:var(--f-mono); font-size:0.9rem; color:var(--ink); background:#fff;">\n'
            '<thead>%s%s</thead>\n<tbody>\n%s</tbody>\n</table>\n' % (head_top, head2, body))


def bits16(s, e, m, note=None):
    """16 ビット浮動小数点数の帯(符号部 1 / 指数部 5 / 仮数部 10)"""
    def cell(lbl, val, w, col):
        return ('<div style="flex:%d 1 0; min-width:0; border:2px solid %s; border-radius:8px; padding:0.45rem 0.4rem; text-align:center; background:#fff;">'
                '<div style="font-family:var(--f-mono); font-size:0.66rem; letter-spacing:0.08em; color:%s; font-weight:700;">%s</div>'
                '<div style="font-family:var(--f-mono); font-size:1.05rem; font-weight:700; color:var(--ink); letter-spacing:0.08em; word-break:break-all;">%s</div></div>'
                % (w, col, col, lbl, val))
    out = ('<div style="display:flex; gap:0.4rem; margin:0.6rem 0 0.3rem;">%s%s%s</div>\n'
           % (cell("符号部 1", s, 1, "var(--ng)"), cell("指数部 5", e, 3, "var(--gold-deep)"), cell("仮数部 10", m, 6, "var(--action)")))
    if note:
        out += '<div style="font-size:0.84rem; color:var(--ink-soft); line-height:1.8; margin-top:0.3rem;">%s</div>\n' % note
    return out


def fb_section(title, body):
    return ('    <div class="fb-section">\n'
            '      <div class="fb-section-title">%s</div>\n'
            '      %s\n'
            '    </div>\n' % (title, body))


def explain(html):
    return '<div class="fb-explain">%s</div>' % html


def bestfit(html):
    return '<div class="fb-bestfit">%s</div>' % html


def feedback(banner_text, sections, example=False):
    score = "" if example else '<span class="score-tag"></span>'
    return ('<div class="feedback" data-feedback>\n'
            '  <div class="fb-banner ok"><span class="icon">✓</span><span>%s</span>%s</div>\n'
            '  <div class="fb-body">\n%s  </div>\n'
            '</div>\n' % (banner_text, score, "".join(sections)))


def indent(text, n):
    if not text:
        return ""
    pad = " " * n
    return "".join(pad + line if line.strip() else line for line in text.splitlines(True))


def stage_example(idx, total, num, source, title, prob_id, type_tag, lead, extra, input_html, fb):
    return (
        '  <section class="stage" data-stage-name="例題 %s" data-prob-id="%s">\n'
        '    <div class="problem-meta">\n'
        '      <span class="problem-tag">EXAMPLE %d / %d</span>\n'
        '      %s\n'
        '      <span class="problem-source">%s</span>\n'
        '    </div>\n'
        '    <div class="problem-q-num"><span class="q">Q</span>%s</div>\n'
        '    <h3 class="problem-title">%s</h3>\n'
        '    <div class="problem-card">\n'
        '      <p class="problem-q lead">%s</p>\n'
        '%s'
        '%s'
        '      <div class="actions-inline">\n'
        '        <button class="btn-reveal" data-action="reveal">解答を見る</button>\n'
        '      </div>\n'
        '%s'
        '    </div>\n'
        '  </section>\n' % (num, prob_id, idx, total, type_tag, source, num, title, lead,
                            indent(extra, 6), indent(input_html, 6), indent(fb, 6))
    )


def stage_practice(idx, total, num, source, title, prob_id, type_tag, lead, extra, input_html, fb,
                   grade_label="採点する"):
    return (
        '  <section class="stage" data-stage-name="練習 %s" data-prob-id="%s">\n'
        '    <div class="problem-meta">\n'
        '      <span class="problem-tag practice">PRACTICE %d / %d</span>\n'
        '      %s\n'
        '      <span class="problem-source">%s</span>\n'
        '    </div>\n'
        '    <div class="problem-q-num"><span class="q">Q</span>%s</div>\n'
        '    <h3 class="problem-title">%s</h3>\n'
        '    <div class="problem-card">\n'
        '      <p class="problem-q lead">%s</p>\n'
        '%s'
        '%s'
        '      <div class="actions-inline">\n'
        '        <button class="btn-grade" data-action="grade">%s <span class="arrow">→</span></button>\n'
        '      </div>\n'
        '%s'
        '    </div>\n'
        '  </section>\n' % (num, prob_id, idx, total, type_tag, source, num, title, lead,
                            indent(extra, 6), indent(input_html, 6), grade_label, indent(fb, 6))
    )


def digest_mod(num, en, icon_svg, question, title, lede, body, hero=False):
    cls = "digest-mod hero" if hero else "digest-mod"
    ico = ('<span class="dg-ico" aria-hidden="true" style="display:inline-flex;width:18px;height:18px;'
           'color:var(--action);flex:none;align-items:center;justify-content:center;margin-right:0.15rem;">'
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round" style="width:100%%;height:100%%">%s</svg></span>' % icon_svg)
    return (
        '    <div class="%s">\n'
        '      <button class="digest-prompt" type="button">\n'
        '        <div class="digest-prompt-head">\n'
        '          <span class="digest-num">%s</span>\n'
        '          %s<span class="digest-en">%s</span>\n'
        '          <span class="digest-toggle"><span class="plus">+</span></span>\n'
        '        </div>\n'
        '        <div class="digest-q">%s</div>\n'
        '      </button>\n'
        '      <div class="digest-answer">\n'
        '        <div class="digest-title">%s</div>\n'
        '        <p class="digest-lede">%s</p>\n'
        '%s'
        '      </div>\n'
        '    </div>\n' % (cls, num, ico, en, question, title, lede, indent(body, 8))
    )


SELF_TAG = '<span class="problem-tag self">記述・自己採点</span>'
SINGLE_TAG = '<span class="problem-tag">SINGLE</span>'

WEIGHT_TABLE = tbl(["…", "整数部", "", "", "", "小数点", "小数部", "", "", "", "…"],
                   [["", "8", "4", "2", "1", ".", "0.5", "0.25", "0.125", "0.0625", ""]],
                   caption="2 進数の桁の重み", mono=True)

# ============================================================
# STAGE 0 — WELCOME
# ============================================================
WELCOME = """  <section class="stage active" data-stage-name="START">
    <div class="welcome-kicker">
      <span class="num">03</span>
      <span>3章 第9節</span>
    </div>
    <h1 class="welcome-title-en">Binary Numbers<br>&amp; Logic<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">2進数と論理演算</h2>
    <p class="welcome-lede">
      2進数の加算と減算、補数、浮動小数点数による実数の表現、演算誤差、そして論理回路と真理値表までを扱います。計算は 4 ビットの筆算から 16 ビットの浮動小数点数まで段階を追い、論理回路は図記号と真理値表を往復して確かめます。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">examples</div>
        <div class="welcome-meta-value">7<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">13<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">60<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">3章09</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー この節の基本知識を、Q&amp;A形式の6モジュールで確認します(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>例題ツアー</strong>ー 例題43〜49の解き方を7問たどります(採点なし。計算は模範解答と照らします)</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>演習</strong>ー 類題75〜83・練習84〜87の計13問。回答 → 採点 → 解説</div></div>
        <div class="flow-item"><span class="flow-num">4</span><div><strong>結果</strong>ー 完答数と、間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>
"""

# ============================================================
# STAGE 1 — REVIEW (Q&A 6 modules)
# ============================================================
FAMILY_TREE = """<div class="viz">
  <span class="viz-label">THE BIG MAP — この節で扱う四つの内容</span>
  <div class="viz-caption">整数の計算(加算・減算・補数)、実数の表現(浮動小数点数)、演算誤差、論理回路の順に積み上がります。</div>
  <div class="family-tree-wrap">
    <svg class="family-tree-svg" viewBox="0 0 760 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2進数と論理演算の地図。2進数の計算(加算と減算・補数・補数を使った減算)、実数の表現(符号部・指数部・仮数部・バイアス)、演算誤差(5 種)、論理回路(AND・OR・NOT・真理値表)の四つに分かれる">
      <rect x="4" y="172" width="118" height="52" rx="12" fill="#122E55"/>
      <text x="63" y="194" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">2進数と</text>
      <text x="63" y="212" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">論理演算</text>
      <line x1="122" y1="198" x2="140" y2="198" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="46" x2="140" y2="350" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="46" x2="156" y2="46" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="148" x2="156" y2="148" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="250" x2="156" y2="250" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="350" x2="156" y2="350" stroke="#B8C5D7" stroke-width="1.5"/>

      <rect x="156" y="24" width="128" height="44" rx="10" fill="#4A78C8"/>
      <text x="220" y="52" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">2進数の計算</text>
      <line x1="284" y1="46" x2="304" y2="46" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="10" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="367" y="30" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">加算と減算</text>
      <rect x="440" y="10" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="503" y="30" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">補数(反転して1を加える)</text>
      <rect x="304" y="50" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="435" y="70" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">補数を使った減算 / 補数による負の数の表現</text>
      <text x="580" y="70" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題43・44 / 類題75・76</text>

      <rect x="156" y="126" width="128" height="44" rx="10" fill="#2A4A78"/>
      <text x="220" y="154" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">実数の表現</text>
      <line x1="284" y1="148" x2="304" y2="148" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="112" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="367" y="132" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">2進数の小数</text>
      <rect x="440" y="112" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="503" y="132" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">浮動小数点数</text>
      <rect x="304" y="152" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="435" y="172" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">符号部・指数部(バイアス)・仮数部</text>
      <text x="580" y="172" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題45・46 / 類題77〜79 / 練習84・85</text>

      <rect x="156" y="228" width="128" height="44" rx="10" fill="#B85975"/>
      <text x="220" y="256" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">演算誤差</text>
      <line x1="284" y1="250" x2="304" y2="250" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="235" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#B85975" stroke-width="1.5"/>
      <text x="435" y="255" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">桁あふれ・丸め・打ち切り・桁落ち・情報落ち</text>
      <text x="580" y="255" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題47 / 類題80</text>

      <rect x="156" y="328" width="128" height="44" rx="10" fill="#2E826F"/>
      <text x="220" y="356" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">論理回路</text>
      <line x1="284" y1="350" x2="304" y2="350" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="314" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#2E826F" stroke-width="1.5"/>
      <text x="367" y="334" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">AND・OR・NOT</text>
      <rect x="440" y="314" width="126" height="30" rx="8" fill="#FAFCFF" stroke="#2E826F" stroke-width="1.5"/>
      <text x="503" y="334" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">真理値表</text>
      <rect x="304" y="354" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#2E826F" stroke-width="1.5"/>
      <text x="435" y="374" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">図記号の読み取り / 回路の組合せ</text>
      <text x="580" y="374" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題48・49 / 類題81〜83 / 練習86・87</text>
    </svg>
  </div>
</div>
"""

SIGN_TABLE = (
    tbl(["2進数"] + [format(i, "04b") for i in range(8)],
        [["符号なし"] + [str(i) for i in range(8)], ["符号あり"] + [str(i) for i in range(8)]],
        mono=True, small=True)
    + tbl(["2進数"] + [format(i, "04b") for i in range(8, 16)],
          [["符号なし"] + [str(i) for i in range(8, 16)], ["符号あり"] + ["－%d" % (16 - i) for i in range(8, 16)]],
          caption="補数による負の数の表現(確認事項の表。前半 0000〜0111 と後半 1000〜1111 に分けて示す)", mono=True, small=True))

BIAS_TABLE = (
    tbl(["指数"] + [("－%d" % -i if i < 0 else str(i)) for i in range(-7, 1)],
        [["バイアス加算後"] + [str(i + 7) for i in range(-7, 1)]], mono=True, small=True)
    + tbl(["指数"] + [str(i) for i in range(1, 9)],
          [["バイアス加算後"] + [str(i + 7) for i in range(1, 9)]],
          caption="例: 指数部 4 ビットで 2<sup>－7</sup>〜2<sup>8</sup> を表現するとき(バイアスは 7)。前半 －7〜0 と後半 1〜8 に分けて示す", mono=True, small=True))

REVIEW_MODS = [
    digest_mod(
        "01", "The Big Map",
        '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><line x1="7" y1="11" x2="17" y2="7"/><line x1="7" y1="13" x2="17" y2="17"/>',
        "この節では、何を順に扱いますか?",
        "整数の計算 → 実数の表現 → 誤差 → 論理回路",
        "はじめに 2 進数の加算と減算、そして補数を使った減算を確認します。次に小数を含む実数を浮動小数点数で表し、内部表現に収まらないときの誤差を分類します。最後に、演算や制御を行う論理回路を図記号と真理値表で読みます。",
        FAMILY_TREE, hero=True),

    digest_mod(
        "02", "Add & Subtract",
        '<line x1="5" y1="12" x2="19" y2="12"/><line x1="12" y1="5" x2="12" y2="19"/>',
        "2進数の足し算と引き算は、どう計算しますか?",
        "10進数と同じように桁ごとに計算を行う",
        "確認事項の一文はこれだけです。違いは、繰り上げが 1＋1 で起こること、繰り下げでは上の桁から借りた 1 が 2 になることです。",
        viz("CARRY / BORROW — 桁ごとの計算",
            "確認事項の例と、例題43 の解説にある繰り上げ・繰り下げの手順を並べます。",
            figure("assets/fig01-add-sub-example.png",
                   "例: 1001(2)＋0101(2)＝1110(2)、1101(2)－1010(2)＝0011(2)",
                   "確認事項の例 — 加算と減算", 420, 360)
            + compare2(
                ("繰り上げ(加算)", [
                    ("起こるとき", "その桁の和が 1＋1 になったとき"),
                    ("手順(例題43 解説)", "一つ上の桁に1を書き、その桁で加算(1＋0＋0)をする。"),
                ]),
                ("繰り下げ(減算)", [
                    ("起こるとき", "その桁が 0－1 になったとき"),
                    ("手順(例題43 解説)", "一つ下の桁に1を二つ書き、その桁で減算(1＋1＋0－1)をする。"),
                ])))),

    digest_mod(
        "03", "Complement",
        '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M8 12h8"/><path d="M12 9v6"/>',
        "補数は何で、引き算にどう使いますか?",
        "加えると1桁増える最も小さな数。反転して1を加える",
        "補数は、ある自然数に対し、加えると1桁増える最も小さな数です。2進数では各桁の0と1を反転し、1を加えて求められます。この補数を足すと、引き算が足し算で計算できます。",
        viz("COMPLEMENT — 作り方と使い方",
            "例: 0101<sub>(2)</sub>　反転→1010<sub>(2)</sub>　1を加える→1011<sub>(2)</sub>",
            bd_grid([
                ("① 反転", "0101 → 1010", "各桁の 0 と 1 を反転する。"),
                ("② 1 を加える", "1010 → 1011", "反転した数に 1 を加えたものが補数。"),
                ("③ 足す", "0111＋1100", "引く数の補数を足す。4ビットを超える桁上がりは無視。"),
            ])
            + fig_row([
                figure("assets/fig02-subtraction-direct.png", "減算: 0111(2)－0100(2)＝0011(2)", "＜減算＞", 200, 160),
                figure("assets/fig03-subtraction-by-complement.png", "補数で計算: 0111(2)＋1100(2)＝1 0011(2)。4ビットを超える桁上がりは無視", "＜補数で計算＞ ※0100<sub>(2)</sub> の補数は 1100<sub>(2)</sub>", 220, 170),
            ])
            + note_box("※4ビットを超える桁上がりは無視。<br>※符号なし2進数では、0000<sub>(2)</sub>～1111<sub>(2)</sub> は10進数の0～15を表す。一方、符号あり2進数では、0000<sub>(2)</sub>～0111<sub>(2)</sub> は0～7を表すが、1000<sub>(2)</sub>～1111<sub>(2)</sub> は－8～－1を表す。<br>※例えば、10進数の7は2進数で 0111<sub>(2)</sub> であり、この補数は 1001<sub>(2)</sub> である。よって、1001<sub>(2)</sub> が－7である。")
            + SIGN_TABLE)),

    digest_mod(
        "04", "Floating Point",
        '<path d="M4 18L20 6"/><circle cx="7" cy="8" r="2.5"/><circle cx="17" cy="16" r="2.5"/>',
        "小数を含む実数は、どう表しますか?",
        "浮動小数点数 — 符号部・指数部・仮数部",
        "実数を表す場合には、浮動小数点数を使います。自然科学などの分野で、数値を指数表記で「4.235×10<sup>8</sup>」と表すように、符号部、指数部、仮数部で表されます。",
        viz("THREE PARTS — 10 進数と 2 進数の対応",
            "確認事項の表です。2 進数では、指数部にバイアスを加え、仮数部は先頭の 1 を省略します。",
            compare2(
                ("10進数", [
                    ("符号部", "＋または－"),
                    ("指数部", "10の何乗の形"),
                    ("仮数部", "最上位の桁が一の位となる小数"),
                    ("例", "－423　→　－4.23×10<sup>2</sup><br><span style=\"color:var(--ink-mute)\">符号部　仮数部　指数部</span>"),
                ]),
                ("2進数", [
                    ("符号部", "正は0、負は1"),
                    ("指数部", "指数部がすべて正で表現できるようにバイアスを加える。"),
                    ("仮数部", "常に1となる最上位は省略し、2番目の桁から仮数部とする。"),
                    ("例", "10.101<sub>(2)</sub> → 0 10000 0101000000<sub>(2)</sub><br><span style=\"color:var(--ink-mute)\">符号部　指数部　　仮数部</span>"),
                ]))
            + note_box("※p.50の2進数の例は、符号部1ビット、指数部5ビット、仮数部10ビットの半精度浮動小数点数で考えている。また、見やすいように便宜的に各部の間にスペースを入れてある。<br>※指数は、小さい数から大きい数までを表すため、負から正までで表したいが、「■補数による負の数の表現」にあるように、符号あり2進数では補数を使っているため、大小の比較が難しい。そこで、指数部にバイアスを加え、指数部を0以上で表現することにより、大小比較が簡単になる。")
            + BIAS_TABLE
            + bits16("0", "10000", "0101000000", "10.101<sub>(2)</sub>＝1.0101<sub>(2)</sub>×2<sup>1</sup>。指数 1 にバイアス 15 を加えて 16＝10000<sub>(2)</sub>、仮数部は先頭の 1 を省いた 0101 に 0 を足して 10 ビット。"))),

    digest_mod(
        "05", "Five Errors",
        '<path d="M12 3l9 16H3z"/><line x1="12" y1="10" x2="12" y2="14"/><line x1="12" y1="17" x2="12" y2="17"/>',
        "コンピュータの計算で誤差が出るのは、どんなときですか?",
        "内部表現(ビット列)に収まらないとき — 5 種類",
        "数値をコンピュータで扱う場合、コンピュータの内部表現(ビット列)に変換されて取り扱われるため、その表現に収まらない場合に、誤差が生じます。生じる場面で名前が決まります。",
        viz("ERRORS — 名前と生じる場面",
            "確認事項の 5 つの定義です。「いつ」生じるかで見分けます。",
            bd_grid([
                ("桁あふれ誤差", "ビット数を超える", "計算した結果の桁数が、扱えるビット数を超えてしまうことにより発生する。<br><span style=\"color:var(--ink-mute)\">・オーバーフロー：ビット数の最大値を上回るとき<br>・アンダーフロー：ビット数の最小値を下回るとき</span>"),
                ("丸め誤差", "桁を削る", "限られた桁数の範囲で数値を表現するとき、切り上げや切り捨て、四捨五入などを行って桁を削ったことで発生する。"),
                ("打ち切り誤差", "途中でやめる", "計算を途中で打ち切ってしまうことで発生する。"),
                ("桁落ち", "近い数の引き算", "絶対値のほぼ等しい二つの数の引き算を行ったとき、有効桁数が減少するために発生する。"),
                ("情報落ち", "大小の足し引き", "絶対値の大きな値と絶対値の小さな値の足し算や引き算を行ったとき、小さな値の桁情報が無視されてしまい、計算結果に反映されないことで発生する。"),
            ]))),

    digest_mod(
        "06", "Logic Gates",
        '<path d="M4 6h6a6 6 0 0 1 0 12H4z"/><line x1="16" y1="12" x2="21" y2="12"/>',
        "論理回路の三つの基本と、真理値表とは何ですか?",
        "AND・OR・NOT と、入力と出力の対応表",
        "コンピュータで演算や制御を行う回路を論理回路といいます。基本は三つで、すべての入力の組合せと、対応する出力の関係を示す表が真理値表です。",
        viz("GATES — 図記号と働き",
            "図記号は「ANDはD、ORはR(丸み『)』)がある」と覚えます(例題48 ベストフィット)。",
            fig_row([
                figure("assets/fig04-and-gate.jpeg", "論理積回路(AND回路)の図記号", "論理積回路(AND回路)", 200, 160),
                figure("assets/fig05-or-gate.jpeg", "論理和回路(OR回路)の図記号", "論理和回路(OR回路)", 200, 160),
                figure("assets/fig06-not-gate.jpeg", "否定回路(NOT回路)の図記号", "否定回路(NOT回路)", 200, 160),
            ])
            + bd_grid([
                ("論理積回路(AND回路)", "ともに1", "二つの入力と一つの出力をもつ回路で、二つの入力がともに1のときだけ、出力が1になる回路。"),
                ("論理和回路(OR回路)", "いずれか1", "二つの入力と一つの出力をもつ回路で、入力のいずれか一方が1であれば、出力が1になる回路。"),
                ("否定回路(NOT回路)", "反転", "一つの入力と一つの出力をもつ回路で、入力した信号を反転した値を出力信号とする回路。"),
            ])
            + figure("assets/fig07-truth-tables-and-or-not.png",
                     "真理値表: 論理積回路(AND回路)、論理和回路(OR回路)、否定回路(NOT回路)",
                     "真理値表 — すべての入力の組合せと、対応する出力の関係を示す表", 560, 520))),
]

REVIEW = ('  <section class="stage" data-stage-name="REVIEW">\n'
          '    <div class="section-divider">\n'
          '      <span class="num">01</span>\n'
          '      <div class="text">\n'
          '        <div class="label">Section 1 — Visual Digest</div>\n'
          '        <div class="name">ひと目でわかる おさらい</div>\n'
          '      </div>\n'
          '    </div>\n'
          '    <div class="digest">\n'
          + "".join(REVIEW_MODS) +
          '    </div>\n'
          '  </section>\n')

# ============================================================
# 例題43 — 2進数の加算と減算
# ============================================================
EX43 = stage_example(
    1, 7, "43", "ベストフィット 例題43", "2進数の加算と減算", "ex43", SELF_TAG,
    "次の2進数の計算をせよ。",
    "",
    self_list([
        ("⑴", "%s＋%s" % (b("1001"), b("0011")),
         "<p><strong>%s</strong></p>" % b("1100") + figure("assets/fig08-ex43-1-addition.png", "⑴ 1001(2)＋0011(2) の筆算。繰り上げが二度起こり 1100(2)", "⑴ 筆算(解説の図)", 460, 420)),
        ("⑵", "%s＋%s" % (b("0110"), b("0101")),
         "<p><strong>%s</strong></p>" % b("1011") + figure("assets/fig09-ex43-2-addition.png", "⑵ 0110(2)＋0101(2) の筆算。繰り上げが一度起こり 1011(2)", "⑵ 筆算(解説の図)", 460, 420)),
        ("⑶", "%s－%s" % (b("1011"), b("0110")),
         "<p><strong>%s</strong></p>" % b("0101") + figure("assets/fig10-ex43-3-subtraction.png", "⑶ 1011(2)－0110(2) の筆算。繰り下げが一度起こり 0101(2)", "⑶ 筆算(解説の図)", 460, 420)),
        ("⑷", "%s－%s" % (b("1110"), b("1001")),
         "<p><strong>%s</strong></p>" % b("0101") + figure("assets/fig11-ex43-4-subtraction.png", "⑷ 1110(2)－1001(2) の筆算。繰り下げが一度起こり 0101(2)", "⑷ 筆算(解説の図)", 460, 420)),
    ]),
    feedback("正答: ⑴ %s　⑵ %s　⑶ %s　⑷ %s" % (b("1100"), b("1011"), b("0101"), b("0101")), [
        fb_section("ベストフィット", bestfit("10進数と同じように桁ごとに計算を行う。")),
        fb_section("解説(原本)", explain(
            "<p>各小問の筆算は、模範解答の図のとおり。繰り上げと繰り下げの手順は次の二つ。</p>"
            + fig_row([
                figure("assets/fig12-carry-note.jpg", "繰り上げ: 一つ上の桁に1を書き、その桁で加算(1＋0＋0)をする", "<strong>繰り上げ</strong>　一つ上の桁に1を書き、その桁で加算(1＋0＋0)をする。", 260, 220),
                figure("assets/fig13-borrow-note.png", "繰り下げ: 一つ下の桁に1を二つ書き、その桁で減算(1＋1＋0－1)をする", "<strong>繰り下げ</strong>　一つ下の桁に1を二つ書き、その桁で減算(1＋1＋0－1)をする。", 260, 220),
            ]))),
        fb_section("10進数で検算する(補足)", explain(
            "<p>⑴ 9＋3＝12＝%s、⑵ 6＋5＝11＝%s、⑶ 11－6＝5＝%s、⑷ 14－9＝5＝%s。筆算の結果を 10 進数に直して確かめると、繰り上げ・繰り下げの書き忘れに気づけます。</p>"
            % (b("1100"), b("1011"), b("0101"), b("0101")))),
        viz("CARRY / BORROW — 二つの手順", "加算は 1＋1 で上の桁へ、減算は 0－1 で上の桁から借ります。",
            compare2(
                ("繰り上げ(⑴⑵)", [
                    ("起こる桁", "1＋1 になった桁"),
                    ("書くもの", "一つ上の桁に 1"),
                    ("その桁の計算", "1＋0＋0(上から来た 1 を足す)"),
                ]),
                ("繰り下げ(⑶⑷)", [
                    ("起こる桁", "0－1 になった桁"),
                    ("書くもの", "一つ下の桁に 1 を二つ"),
                    ("その桁の計算", "1＋1＋0－1(借りた 1 は下の桁で 2 になる)"),
                ]))),
    ], example=True))

# ============================================================
# 例題44 — 補数
# ============================================================
def comp_model(x, inv, res):
    return ("<p><strong>%s</strong><br>%s　反転→　%s　1を加える→　%s</p>" % (b(res), b(x), b(inv), b(res)))


EX44 = stage_example(
    2, 7, "44", "ベストフィット 例題44", "補数", "ex44", SELF_TAG,
    "次の2進数の補数を求めよ。",
    "",
    self_list([
        ("⑴", b("1001"), comp_model("1001", "0110", "0111")),
        ("⑵", b("0111"), comp_model("0111", "1000", "1001")),
        ("⑶", b("01101010"), comp_model("01101010", "10010101", "10010110")),
        ("⑷", b("10011100"), comp_model("10011100", "01100011", "01100100")),
    ]),
    feedback("正答: ⑴ %s　⑵ %s　⑶ %s　⑷ %s" % (b("0111"), b("1001"), b("10010110"), b("01100100")), [
        fb_section("ベストフィット", bestfit("2進数の補数は、各桁の0と1を反転し、1を加えて求められる。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　%s　反転→　%s　1を加える→　%s</li>"
            "<li><strong>⑵</strong>　%s　反転→　%s　1を加える→　%s</li>"
            "<li><strong>⑶</strong>　%s　反転→　%s　1を加える→　%s</li>"
            "<li><strong>⑷</strong>　%s　反転→　%s　1を加える→　%s</li></ul>"
            % (b("1001"), b("0110"), b("0111"), b("0111"), b("1000"), b("1001"),
               b("01101010"), b("10010101"), b("10010110"), b("10011100"), b("01100011"), b("01100100")))),
        fb_section("定義に戻って確かめる(補足)", explain(
            "<p>補数は「加えると1桁増える最も小さな数」です。⑴では %s＋%s＝%s と、4 ビットから 5 ビットへ桁が一つ増えます。"
            "⑶⑷の 8 ビットでも同じで、もとの数と補数を足すと %s になります。反転と 1 を加える操作を別々に覚えるより、この足し算で確かめると間違えません。</p>"
            % (b("1001"), b("0111"), b("1 0000"), b("1 0000 0000")))),
        viz("TWO STEPS — 反転してから 1 を加える", "反転しただけでは補数になりません。1 を加えるところまでが一組です。",
            bd_grid([
                ("⑴ 1001", "0111", "反転 0110 → 1を加える 0111"),
                ("⑵ 0111", "1001", "反転 1000 → 1を加える 1001"),
                ("⑶ 01101010", "10010110", "反転 10010101 → 1を加える 10010110"),
                ("⑷ 10011100", "01100100", "反転 01100011 → 1を加える 01100100"),
            ], warn="⑴と⑵、⑶と⑷は互いに補数の関係にあります。片方を求めれば、もう片方の答えの確かめに使えます。")),
    ], example=True))

# ============================================================
# 例題45 — 2進数の小数への変換
# ============================================================
EX45 = stage_example(
    3, 7, "45", "ベストフィット 例題45", "2進数の小数への変換", "ex45", SELF_TAG,
    "次の10進数を、2進数の桁の重み(右の表)に分解し、2進数の小数に変換せよ。",
    WEIGHT_TABLE,
    self_list([
        ("⑴", "1.625", "<p><strong>%s</strong><br>1.625＝1＋0.5＋0.125　と分解されるので、%sと変換できる。</p>" % (b("1.101"), b("1.101"))),
        ("⑵", "5.75", "<p><strong>%s</strong><br>5.75＝4＋1＋0.5＋0.25　と分解されるので、%sと変換できる。</p>" % (b("101.11"), b("101.11"))),
        ("⑶", "6.375", "<p><strong>%s</strong><br>6.375＝4＋2＋0.25＋0.125　と分解されるので、%sと変換できる。</p>" % (b("110.011"), b("110.011"))),
    ]),
    feedback("正答: ⑴ %s　⑵ %s　⑶ %s" % (b("1.101"), b("101.11"), b("110.011")), [
        fb_section("ベストフィット", bestfit("桁の重みがある位には1を、ない位には0を書いて求められる。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　1.625＝1＋0.5＋0.125　と分解されるので、%sと変換できる。</li>"
            "<li><strong>⑵</strong>　5.75＝4＋1＋0.5＋0.25　と分解されるので、%sと変換できる。</li>"
            "<li><strong>⑶</strong>　6.375＝4＋2＋0.25＋0.125　と分解されるので、%sと変換できる。</li></ul>"
            % (b("1.101"), b("101.11"), b("110.011")))),
        fb_section("分解の順序(補足)", explain(
            "<p>整数部と小数部を分けて考えます。整数部は 8・4・2・1 の重みで、小数部は 0.5・0.25・0.125・0.0625 の重みです。"
            "大きい重みから順に「引けるか」を見て、引けた重みの位に 1 を書きます。⑶なら 6.375 から 4 を引いて 2.375、2 を引いて 0.375、0.5 は引けず、0.25 を引いて 0.125、0.125 を引いて 0 になります。</p>")),
        viz("PLACE VALUES — 重みの分解", "重みがある位に 1、ない位に 0。小数点の右は 0.5 から始まります。",
            bd_grid([
                ("⑴ 1.625", "1.101", "1 ＋ 0.5 ＋ 0.125。0.25 の位は 0。"),
                ("⑵ 5.75", "101.11", "4 ＋ 1 ＋ 0.5 ＋ 0.25。2 の位は 0。"),
                ("⑶ 6.375", "110.011", "4 ＋ 2 ＋ 0.25 ＋ 0.125。1 と 0.5 の位は 0。"),
            ])),
    ], example=True))

# ============================================================
# 例題46 — 実数の表現
# ============================================================
EX46_TEXT = quote_box(
    "2進数の桁の重みは以下のようになる。\n" + WEIGHT_TABLE +
    "よって6.75は、6.75＝4＋2＋0.5＋（　①　）のように桁の重みに分解できるので、%s＝%sと2進数へ変換できる。"
    "次に、%s＝＋%s×2<sup>2</sup> となるので、符号部は（　②　）、仮数部は（　③　）となる。指数部は 2＋15＝17 から（　④　）となる。"
    "以上より、求める浮動小数点数は、（　⑤　）である。\n" % (d("6.75"), b("110.11"), b("110.11"), b("1.1011"))
)

NWEIGHT_TABLE = tbl(["…", "整数部", "", "", "", "小数点", "小数部", "", "", "", "…"],
                    [["", pw("n", "3"), pw("n", "2"), pw("n", "1"), pw("n", "0"), ".", pw("n", "－1"), pw("n", "－2"), pw("n", "－3"), pw("n", "－4"), ""]],
                    caption="n 進数の桁の重み(ベストフィット)", mono=True)

EX46 = stage_example(
    4, 7, "46", "ベストフィット 例題46", "実数の表現", "ex46", SELF_TAG,
    "10進数の6.75を、16ビットの2進数の浮動小数点数(符号部1ビット、指数部5ビット、仮数部10ビット)で表すことを考える。次の文章の空欄に適当な数字を入れよ。",
    EX46_TEXT,
    self_list([
        ("①", "6.75＝4＋2＋0.5＋（　①　）", "<p><strong>0.25</strong><br>4＋2＋0.5＋0.25＝6.75。よって %s＝%s。</p>" % (d("6.75"), b("110.11"))),
        ("②", "符号部は（　②　）", "<p><strong>0</strong><br>正の数なので、符号部は0となる。</p>"),
        ("③", "仮数部は（　③　）", "<p><strong>1011000000</strong><br>常に1となる最上位は省略し、2番目の桁から仮数部となり、残った桁は0で満たす。よって、1011000000となる。</p>"),
        ("④", "指数部は 2＋15＝17 から（　④　）", "<p><strong>10001</strong><br>この例題の場合、指数部5ビットなので、バイアスは15(%s)である。17 を 5 ビットの 2 進数で表して 10001。</p>" % b("01111")),
        ("⑤", "求める浮動小数点数は（　⑤　）", "<p><strong>%s</strong><br>符号部 0、指数部 10001、仮数部 1011000000 の順に並べる。</p>" % b("0 10001 1011000000")),
    ]),
    feedback("正答: ① 0.25　② 0　③ 1011000000　④ 10001　⑤ %s" % b("0 10001 1011000000"), [
        fb_section("ベストフィット", bestfit("n進数の桁の重みは、次のように求められる。" + NWEIGHT_TABLE)),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>②</strong>　正の数なので、符号部は0となる。</li>"
            "<li><strong>③</strong>　常に1となる最上位は省略し、2番目の桁から仮数部となり、残った桁は0で満たす。よって、1011000000となる。</li>"
            "<li><strong>④</strong>　この例題の場合、指数部5ビットなので、バイアスは15(%s)である。</li></ul>" % b("01111"))),
        fb_section("手順を四つに分ける(補足)", explain(
            "<p>① 10進数を2進数の小数にする(110.11)。② 先頭が 1 になるよう小数点を動かし、1.1011×2<sup>2</sup> の形にする。"
            "③ 符号部・指数部(指数 2 にバイアス 15 を加えて 17)・仮数部(先頭の 1 を省いた 1011 に 0 を足して 10 ビット)を作る。④ 三つを並べる。"
            "類題79・練習84 も同じ四段です。</p>")),
        viz("16 BITS — 三つの部分を並べる", "符号部 1 ビット、指数部 5 ビット、仮数部 10 ビットで合計 16 ビットです。",
            bits16("0", "10001", "1011000000",
                   "6.75＝110.11<sub>(2)</sub>＝1.1011<sub>(2)</sub>×2<sup>2</sup>。指数 2＋バイアス 15＝17＝10001<sub>(2)</sub>。仮数部は 1011 のあとを 0 で埋めて 10 ビット。")),
    ], example=True))

# ============================================================
# 例題47 — コンピュータによる演算誤差
# ============================================================
EX47 = stage_example(
    5, 7, "47", "ベストフィット 例題47", "コンピュータによる演算誤差", "ex47", SELF_TAG,
    "次の⑴～⑸の記述は、コンピュータによる演算誤差についての説明である。それぞれの誤差の名称を答えよ。",
    "",
    self_list([
        ("⑴", "絶対値のほぼ等しい二つの数の引き算を行ったとき、有効桁数が減少するために発生する。",
         "<p><strong>桁落ち</strong><br>例えば、%sと%sの引き算を行うと、%sとなる。引き算の前では、有効数字は4桁であるが、引き算の後では1桁となってしまい、有効桁数が減ってしまう。</p>" % (b("0.1111"), b("0.1110"), b("0.0001"))),
        ("⑵", "限られた桁数の範囲で数値を表現するとき、切り上げや切り捨て、四捨五入などを行って桁を削ったことで発生する。",
         "<p><strong>丸め誤差</strong><br>例えば、円周率や循環小数などを限られた桁数の範囲で表現すると、差が生じることで理解できる。</p>"),
        ("⑶", "計算を途中で打ち切ってしまうことで発生する。",
         "<p><strong>打ち切り誤差</strong><br>無限に続く計算を有限回で止めたときに生じます(補足)。</p>"),
        ("⑷", "計算した結果の桁数が、扱えるビット数の最大値を超えてしまうことにより発生する。",
         "<p><strong>桁あふれ誤差</strong><br>例えば、「%s×2<sup>10000</sup>」という極めて大きな数を扱おうとした場合、指数部の値「10000」は、浮動小数点数の指数部が取り得る最大値を超えるため扱えない。</p>" % b("1.01")),
        ("⑸", "絶対値の大きな値と絶対値の小さな値の足し算や引き算を行ったとき、小さな値の桁情報が無視されてしまい、計算結果に反映されないことで発生する。",
         "<p><strong>情報落ち</strong><br>例えば、絶対値の大きな数 %s と小さな数 %s を用意すると、二数の足し算の結果は、%s になる。仮数部のビットに収まりきらない小数の下位部分は削除されてしまう。</p>" % (b("1101"), b("0.00001101"), b("1101.00001101"))),
    ]),
    feedback("正答: ⑴ 桁落ち　⑵ 丸め誤差　⑶ 打ち切り誤差　⑷ 桁あふれ誤差　⑸ 情報落ち", [
        fb_section("ベストフィット", bestfit("数値をコンピュータで扱う際、内部表現(ビット列)に収まらない場合に誤差が生じる。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　例えば、%sと%sの引き算を行うと、%sとなる。引き算の前では、有効数字は4桁であるが、引き算の後では1桁となってしまい、有効桁数が減ってしまう。これを浮動小数点数で表現すると、仮数部において、有効桁数以降の桁は0で満たすことになるが、これは仮数部のビット表現のために付与したにすぎず、正しい値である保証はない。</li>"
            "<li><strong>⑵</strong>　例えば、円周率や循環小数などを限られた桁数の範囲で表現すると、差が生じることで理解できる。</li>"
            "<li><strong>⑷</strong>　例えば、「%s×2<sup>10000</sup>」という極めて大きな数を扱おうとした場合、指数部の値「10000」は、浮動小数点数の指数部が取り得る最大値を超えるため扱えない。</li>"
            "<li><strong>⑸</strong>　例えば、絶対値の大きな数 %s と小さな数 %s を用意すると、二数の足し算の結果は、%s になる。これを浮動小数点数で表現するとき、仮数部のビットに収まりきらない小数の下位部分は削除されてしまい、計算結果が反映されなくなることがある。例えば、半精度浮動小数点数では、仮数部が10ビットなので、すべてが収まりきらない。</li></ul>"
            % (b("0.1111"), b("0.1110"), b("0.0001"), b("1.01"), b("1101"), b("0.00001101"), b("1101.00001101")))),
        fb_section("⑶ と、名前の見分け方(補足)", explain(
            "<p>⑶の打ち切り誤差は、原本に例がありません。無限に続く計算(級数や繰り返し)を有限回で止めたときの、止めた先の分のずれです。"
            "五つの名前は「いつ生じるか」で決まります。桁を削れば丸め、ビット数を超えれば桁あふれ、途中でやめれば打ち切り、近い数を引けば桁落ち、大きさの違う数を足し引きすれば情報落ちです。</p>")),
        viz("WHEN — 生じる場面で名前が決まる", "説明文の中の「引き算」「桁を削った」「最大値を超え」「打ち切って」「小さな値の桁情報」が手がかりです。",
            bd_grid([
                ("⑴ 桁落ち", "近い数の引き算", "絶対値のほぼ等しい二つの数の引き算 → 有効桁数が減少"),
                ("⑵ 丸め誤差", "桁を削る", "切り上げ・切り捨て・四捨五入で桁を削った"),
                ("⑶ 打ち切り誤差", "途中でやめる", "計算を途中で打ち切った"),
                ("⑷ 桁あふれ誤差", "ビット数を超える", "結果の桁数が扱えるビット数の最大値を超えた"),
                ("⑸ 情報落ち", "大小の足し引き", "小さな値の桁情報が無視され、結果に反映されない"),
            ])),
    ], example=True))

# ============================================================
# 例題48 — 論理回路
# ============================================================
GATE_OPTS = [
    ("ア", inline_img("assets/fig14-or-symbol.jpeg", "(ア) 図記号: 入力 A・B、出力 X。丸みのある記号", 56)),
    ("イ", inline_img("assets/fig15-nor-symbol.jpeg", "(イ) 図記号: 丸みのある記号の出力に○が付く", 56)),
    ("ウ", inline_img("assets/fig16-xor-symbol.jpeg", "(ウ) 図記号: 丸みのある記号の入力側に線が一本多い", 56)),
    ("エ", inline_img("assets/fig17-nand-symbol.jpeg", "(エ) 図記号: D の形の記号の出力に○が付く", 56)),
    ("オ", inline_img("assets/fig18-not-symbol.jpeg", "(オ) 図記号: 入力 A、出力 X。三角形の出力に○が付く", 56)),
    ("カ", inline_img("assets/fig04-and-gate.jpeg", "(カ) 図記号: 入力 A・B、出力 X。D の形の記号", 56)),
]

EX48 = stage_example(
    6, 7, "48", "ベストフィット 例題48", "論理回路", "ex48",
    '<span class="problem-tag match">MATCH</span>',
    "次の⑴～⑶の論理回路にあたる図記号を、下の(ア)～(カ)から一つずつ選べ。",
    "",
    legend(GATE_OPTS, "図記号")
    + match_list("ア,イ,ウ,エ,オ,カ", "5,0,4",
                 [("⑴", "論理積回路(AND回路)"), ("⑵", "論理和回路(OR回路)"), ("⑶", "否定回路(NOT回路)")]),
    feedback("正答: ⑴ (カ)　⑵ (ア)　⑶ (オ)", [
        fb_section("ベストフィット", bestfit("図記号は「ANDはD、ORはR(丸み『)』)がある」と覚えよ。")),
        fb_section("解説(原本)", explain(
            "<p>(イ)は論理和回路(OR回路)の図記号に「○」(否定)が付いているので否定論理和回路(NOR回路)、(エ)は論理積回路(AND回路)の図記号に「○」(否定)が付いているので否定論理積回路(NAND回路)と呼ばれる。また、(ウ)は排他的論理和回路(XOR回路)と呼ばれ、二つの入力のうち、一方のみ「1」のときだけ出力が「1」となる。</p>")),
        fb_section("○ の見方(補足)", explain(
            "<p>出力側の小さな「○」は否定を表します。(オ)の三角形に○が付いたものが否定回路で、(イ)(エ)は OR・AND の出力を否定したものです。"
            "○のない(ア)(カ)が、そのまま OR と AND です。</p>")),
        viz("SYMBOLS — 六つの図記号と名前", "D の形が AND、丸みのある形が OR。○が付けば否定、入力側の線が増えれば排他的論理和です。",
            fig_row([
                figure("assets/fig04-and-gate.jpeg", "(カ) 論理積回路(AND回路)", "(カ) 論理積回路(AND回路)", 190, 150),
                figure("assets/fig14-or-symbol.jpeg", "(ア) 論理和回路(OR回路)", "(ア) 論理和回路(OR回路)", 190, 150),
                figure("assets/fig18-not-symbol.jpeg", "(オ) 否定回路(NOT回路)", "(オ) 否定回路(NOT回路)", 190, 150),
                figure("assets/fig17-nand-symbol.jpeg", "(エ) 否定論理積回路(NAND回路)", "(エ) 否定論理積回路(NAND回路)", 190, 150),
                figure("assets/fig15-nor-symbol.jpeg", "(イ) 否定論理和回路(NOR回路)", "(イ) 否定論理和回路(NOR回路)", 190, 150),
                figure("assets/fig16-xor-symbol.jpeg", "(ウ) 排他的論理和回路(XOR回路)", "(ウ) 排他的論理和回路(XOR回路)", 190, 150),
            ])),
    ], example=True))

# ============================================================
# 例題49 — 真理値表
# ============================================================
TT_OR = truth_table(["A", "B"], [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)])
TT_AND = truth_table(["A", "B"], [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)])
TT_NOT = truth_table(["A"], [([0], 1), ([1], 0)])

EX49 = stage_example(
    7, 7, "49", "ベストフィット 例題49", "真理値表", "ex49", SELF_TAG,
    "次に示した⑴～⑶の論理回路の図記号について、それぞれ真理値表を作成せよ。",
    "",
    self_list([
        ("⑴", inline_img("assets/fig14-or-symbol.jpeg", "⑴ 図記号(入力 A・B、出力 X)", 60),
         "<p><strong>論理和回路(OR回路)の真理値表</strong></p>" + TT_OR + "<p>入力のいずれか一方が1であれば、出力が1になる。</p>"),
        ("⑵", inline_img("assets/fig04-and-gate.jpeg", "⑵ 図記号(入力 A・B、出力 X)", 60),
         "<p><strong>論理積回路(AND回路)の真理値表</strong></p>" + TT_AND + "<p>二つの入力がともに1のときだけ、出力が1になる。</p>"),
        ("⑶", inline_img("assets/fig18-not-symbol.jpeg", "⑶ 図記号(入力 A、出力 X)", 60),
         "<p><strong>否定回路(NOT回路)の真理値表</strong></p>" + TT_NOT + "<p>入力した信号を反転した値を出力信号とする。</p>"),
    ]),
    feedback("正答: 確認事項(p.51)の「■真理値表」を参照 — ⑴ OR回路　⑵ AND回路　⑶ NOT回路", [
        fb_section("ベストフィット", bestfit("思考のステップ(→p.62)「真理値表」を参照。")),
        fb_section("解説(原本)", explain("<p>⑴は論理和回路(OR回路)、⑵は論理積回路(AND回路)、⑶は否定回路(NOT回路)の図記号である。</p>")),
        fb_section("表の作り方(補足)", explain(
            "<p>入力が二つなら、組合せは 2<sup>2</sup>＝4 通りで、上から 00・01・10・11 の順に並べます。入力が一つなら 0・1 の 2 通りです。"
            "出力の列は、その回路の働き(ともに1 / いずれか1 / 反転)を一行ずつ当てはめて埋めます。</p>")),
        viz("TRUTH TABLES — 三つの基本回路", "確認事項の表です。OR は「0 になるのは 00 だけ」、AND は「1 になるのは 11 だけ」と覚えます。",
            figure("assets/fig07-truth-tables-and-or-not.png", "真理値表: 論理積回路(AND回路)、論理和回路(OR回路)、否定回路(NOT回路)", "確認事項 ■真理値表", 560, 520)),
    ], example=True))

# ============================================================
# 類題75 — 2進数の加算と減算
# ============================================================
def p75_model(res, n, desc):
    return "<p><strong>%s</strong></p>" % b(res) + figure("assets/ans75-%d.png" % n, desc, "解説の図(筆算)", 520, 480)


P75 = stage_practice(
    1, 13, "75", "ベストフィット 類題75", "〈2進数の加算と減算〉", "p1", SELF_TAG,
    "次の2進数の計算をせよ。",
    "",
    self_list([
        ("⑴", "%s＋%s" % (b("1010"), b("0101")), p75_model("1111", 1, "⑴ 1010(2)＋0101(2) の筆算。繰り上げなしで 1111(2)")),
        ("⑵", "%s＋%s" % (b("0100"), b("0111")), p75_model("1011", 2, "⑵ 0100(2)＋0111(2) の筆算。繰り上げが一度起こり 1011(2)")),
        ("⑶", "%s＋%s" % (b("1011"), b("0011")), p75_model("1110", 3, "⑶ 1011(2)＋0011(2) の筆算。繰り上げが二度起こり 1110(2)")),
        ("⑷", "%s－%s" % (b("1001"), b("0110")), p75_model("0011", 4, "⑷ 1001(2)－0110(2) の筆算。繰り下げが二度起こり 0011(2)")),
        ("⑸", "%s－%s" % (b("1010"), b("0101")), p75_model("0101", 5, "⑸ 1010(2)－0101(2) の筆算。繰り下げが二度起こり 0101(2)")),
        ("⑹", "%s－%s" % (b("1101"), b("1010")), p75_model("0011", 6, "⑹ 1101(2)－1010(2) の筆算。繰り下げが一度起こり 0011(2)")),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ %s　⑵ %s　⑶ %s<br>⑷ %s　⑸ %s　⑹ %s</div>'
                   % (b("1111"), b("1011"), b("1110"), b("0011"), b("0101"), b("0011"))),
        fb_section("解説(原本)", explain("<p>各小問の筆算の図は、模範解答に載せてある。繰り上げは一つ上の桁に1を書き、繰り下げは一つ下の桁に1を二つ書いて計算する(例題43 解説)。</p>")),
        fb_section("10進数で検算する(補足)", explain(
            "<p>⑴ 10＋5＝15、⑵ 4＋7＝11、⑶ 11＋3＝14、⑷ 9－6＝3、⑸ 10－5＝5、⑹ 13－10＝3。結果を 10 進数に直すと、それぞれ 1111・1011・1110・0011・0101・0011 と一致します。</p>")),
        viz("DECIMAL CHECK — 10 進数で確かめる", "2 進数の筆算のあと、10 進数の計算と突き合わせます。",
            bd_grid([
                ("⑴", "1111", "10＋5＝15"),
                ("⑵", "1011", "4＋7＝11"),
                ("⑶", "1110", "11＋3＝14"),
                ("⑷", "0011", "9－6＝3"),
                ("⑸", "0101", "10－5＝5"),
                ("⑹", "0011", "13－10＝3"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 類題76 — 補数
# ============================================================
def p76_model(x, inv, res):
    return ("<p><strong>%s</strong><br>%s<br>↓ 各桁の0と1を反転<br>%s<br>↓ 1を加算<br>%s</p>" % (b(res), b(x), b(inv), b(res)))


P76 = stage_practice(
    2, 13, "76", "ベストフィット 類題76", "〈補数〉", "p2", SELF_TAG,
    "次の2進数の補数を求めよ。",
    "",
    self_list([
        ("⑴", b("1100"), p76_model("1100", "0011", "0100")),
        ("⑵", b("1010"), p76_model("1010", "0101", "0110")),
        ("⑶", b("01001000"), p76_model("01001000", "10110111", "10111000")),
        ("⑷", b("10111000"), p76_model("10111000", "01000111", "01001000")),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ %s　⑵ %s　⑶ %s　⑷ %s</div>' % (b("0100"), b("0110"), b("10111000"), b("01001000"))),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　%s ↓各桁の0と1を反転 %s ↓1を加算 %s</li>"
            "<li><strong>⑵</strong>　%s ↓各桁の0と1を反転 %s ↓1を加算 %s</li>"
            "<li><strong>⑶</strong>　%s ↓各桁の0と1を反転 %s ↓1を加算 %s</li>"
            "<li><strong>⑷</strong>　%s ↓各桁の0と1を反転 %s ↓1を加算 %s</li></ul>"
            % (b("1100"), b("0011"), b("0100"), b("1010"), b("0101"), b("0110"),
               b("01001000"), b("10110111"), b("10111000"), b("10111000"), b("01000111"), b("01001000")))),
        fb_section("足して確かめる(補足)", explain(
            "<p>⑴ %s＋%s＝%s、⑶ %s＋%s＝%s。もとの数と補数を足すと、ちょうど桁が一つ増えて残りが 0 になります。"
            "⑶と⑷は互いに補数なので、片方の答えがもう片方の問題になっています。</p>"
            % (b("1100"), b("0100"), b("1 0000"), b("01001000"), b("10111000"), b("1 0000 0000")))),
        viz("INVERT → ADD 1", "反転した数に 1 を加える。末尾が 1 のときは繰り上がりが続きます。",
            bd_grid([
                ("⑴ 1100", "0100", "反転 0011 → 1を加算 0100"),
                ("⑵ 1010", "0110", "反転 0101 → 1を加算 0110"),
                ("⑶ 01001000", "10111000", "反転 10110111 → 1を加算 10111000"),
                ("⑷ 10111000", "01001000", "反転 01000111 → 1を加算 01001000"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 類題77 — 2進数の小数への変換
# ============================================================
P77 = stage_practice(
    3, 13, "77", "ベストフィット 類題77", "〈2進数の小数への変換〉", "p3", SELF_TAG,
    "次の10進数を、2進数の小数に変換せよ。",
    "",
    self_list([
        ("⑴", "3.25", "<p><strong>%s</strong><br>3.25＝2＋1＋0.25と表すことができる。よって、2と1と0.25の桁はあり、0.5の桁はないので、%sとなる。</p>" % (b("11.01"), b("11.01"))),
        ("⑵", "5.5625", "<p><strong>%s</strong><br>5.5625＝4＋1＋0.5＋0.0625と表すことができる。よって、4と1と0.5と0.0625の桁はあり、2と0.25と0.125の桁はないので、%sとなる。</p>" % (b("101.1001"), b("101.1001"))),
        ("⑶", "7.875", "<p><strong>%s</strong><br>7.875＝4＋2＋1＋0.5＋0.25＋0.125と表すことができる。よって、4と2と1と0.5と0.25と0.125の桁があるので、%sとなる。</p>" % (b("111.111"), b("111.111"))),
        ("⑷", "7.625", "<p><strong>%s</strong><br>7.625＝4＋2＋1＋0.5＋0.125と表すことができる。よって、4と2と1と0.5と0.125の桁があり、0.25の桁はないので、%sとなる。</p>" % (b("111.101"), b("111.101"))),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ %s　⑵ %s　⑶ %s　⑷ %s</div>' % (b("11.01"), b("101.1001"), b("111.111"), b("111.101"))),
        fb_section("解説(原本)", explain(
            "<p>2進数の桁の重みは、以下のように表される。</p>" + WEIGHT_TABLE +
            "<ul><li><strong>⑴</strong>　3.25＝2＋1＋0.25と表すことができる。よって、2と1と0.25の桁はあり、0.5の桁はないので、%sとなる。</li>"
            "<li><strong>⑵</strong>　5.5625＝4＋1＋0.5＋0.0625と表すことができる。よって、4と1と0.5と0.0625の桁はあり、2と0.25と0.125の桁はないので、%sとなる。</li>"
            "<li><strong>⑶</strong>　7.875＝4＋2＋1＋0.5＋0.25＋0.125と表すことができる。よって、4と2と1と0.5と0.25と0.125の桁があるので、%sとなる。</li>"
            "<li><strong>⑷</strong>　7.625＝4＋2＋1＋0.5＋0.125と表すことができる。よって、4と2と1と0.5と0.125の桁があり、0.25の桁はないので、%sとなる。</li></ul>"
            % (b("11.01"), b("101.1001"), b("111.111"), b("111.101")))),
        fb_section("桁数の決め方(補足)", explain(
            "<p>小数部の桁数は、使った重みのうち最も小さいものまでです。⑵は 0.0625 を使うので小数部は 4 桁、⑴は 0.25 までなので 2 桁になります。"
            "使わなかった位に 0 を書き忘れると、桁がずれます。</p>")),
        viz("PLACE VALUES — 使った重みと使わなかった重み", "「ある」重みに 1、「ない」重みに 0。0 の書き忘れが最も多い誤りです。",
            bd_grid([
                ("⑴ 3.25", "11.01", "2＋1＋0.25。0.5 は 0"),
                ("⑵ 5.5625", "101.1001", "4＋1＋0.5＋0.0625。2・0.25・0.125 は 0"),
                ("⑶ 7.875", "111.111", "4＋2＋1＋0.5＋0.25＋0.125"),
                ("⑷ 7.625", "111.101", "4＋2＋1＋0.5＋0.125。0.25 は 0"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 類題78 — 2進数の小数からの変換
# ============================================================
P78 = stage_practice(
    4, 13, "78", "ベストフィット 類題78", "〈2進数の小数からの変換〉", "p4", SELF_TAG,
    "次の2進数を、10進数の小数に変換せよ。",
    "",
    self_list([
        ("⑴", b("11.011"), "<p><strong>3.375</strong><br>2と1と0.25と0.125の桁に1があるので、2＋1＋0.25＋0.125＝3.375と表すことができる。</p>"),
        ("⑵", b("1001.11"), "<p><strong>9.75</strong><br>8と1と0.5と0.25の桁に1があるので、8＋1＋0.5＋0.25＝9.75と表すことができる。</p>"),
        ("⑶", b("101.0101"), "<p><strong>5.3125</strong><br>4と1と0.25と0.0625の桁に1があるので、4＋1＋0.25＋0.0625＝5.3125と表すことができる。</p>"),
        ("⑷", b("100.001"), "<p><strong>4.125</strong><br>4と0.125の桁に1があるので、4＋0.125＝4.125と表すことができる。</p>"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ 3.375　⑵ 9.75　⑶ 5.3125　⑷ 4.125</div>'),
        fb_section("解説(原本)", explain(
            "<p>2進数の桁の重みは、以下のように表される。</p>" + WEIGHT_TABLE +
            "<ul><li><strong>⑴</strong>　2と1と0.25と0.125の桁に1があるので、2＋1＋0.25＋0.125＝3.375と表すことができる。</li>"
            "<li><strong>⑵</strong>　8と1と0.5と0.25の桁に1があるので、8＋1＋0.5＋0.25＝9.75と表すことができる。</li>"
            "<li><strong>⑶</strong>　4と1と0.25と0.0625の桁に1があるので、4＋1＋0.25＋0.0625＝5.3125と表すことができる。</li>"
            "<li><strong>⑷</strong>　4と0.125の桁に1があるので、4＋0.125＝4.125と表すことができる。</li></ul>")),
        fb_section("小数点からの距離で重みを読む(補足)", explain(
            "<p>小数点のすぐ右が 0.5、その右が 0.25、0.125、0.0625 です。⑶の 0101 なら、2 桁目の 0.25 と 4 桁目の 0.0625 を足します。"
            "整数部は右端から 1・2・4・8 と読みます。</p>")),
        viz("READ THE WEIGHTS — 1 のある位を足す", "類題77 の逆向きです。1 のある位の重みだけを足します。",
            bd_grid([
                ("⑴ 11.011", "3.375", "2＋1＋0.25＋0.125"),
                ("⑵ 1001.11", "9.75", "8＋1＋0.5＋0.25"),
                ("⑶ 101.0101", "5.3125", "4＋1＋0.25＋0.0625"),
                ("⑷ 100.001", "4.125", "4＋0.125"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 類題79 — 実数の表現
# ============================================================
P79 = stage_practice(
    5, 13, "79", "ベストフィット 類題79", "〈実数の表現〉", "p5", SELF_TAG,
    "次の①～④の手順に従って各問いに答え、10進数の3.125を16ビットの2進数の浮動小数点数で表せ。ただし、浮動小数点数は、符号部1ビット、指数部5ビット、仮数部10ビットとする。",
    "",
    self_list([
        ("①", "3.125を2進数の小数(指数を用いない形)に変換せよ。",
         "<p><strong>%s</strong><br>3.125＝2＋1＋0.125と表すことができるので、2と1と0.125の桁はあり、0.5と0.25の桁はないので、%s となる。</p>" % (b("11.001"), b("11.001"))),
        ("②", "①で求めた小数を、指数を用いた「1.…<sub>(2)</sub>×2<sup>n</sup>」の形で表せ。",
         "<p><strong>%s×2<sup>1</sup></strong><br>%s＝%s×2<sup>1</sup> となる。</p>" % (b("1.1001"), b("11.001"), b("1.1001"))),
        ("③", "浮動小数点数で表現するためのバイアスを求めよ。ただし、10進法で示すこと。",
         "<p><strong>15</strong><br>指数部5ビットなので、バイアスは %s である。よって、10進法では15となる。</p>" % b("01111")),
        ("④", "3.125を16ビットの2進数の浮動小数点数の形で表せ。",
         "<p><strong>%s</strong><br>正の数なので符号部は0である。また、指数部は、②で求めた1にバイアスの15を加算した16なので、%s となる。仮数部は、②で求めた小数の最上位の1を省略した1001に、残りの桁を0で埋めて、%s である。</p>"
         % (b("0  10000  1001000000"), b("10000"), b("1001000000"))),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">① %s　② %s×2<sup>1</sup>　③ 15<br>④ %s</div>' % (b("11.001"), b("1.1001"), b("0  10000  1001000000"))),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>①</strong>　3.125＝2＋1＋0.125と表すことができるので、2と1と0.125の桁はあり、0.5と0.25の桁はないので、%s となる。</li>"
            "<li><strong>②</strong>　%s＝%s×2<sup>1</sup> となる。</li>"
            "<li><strong>③</strong>　指数部5ビットなので、バイアスは %s である。よって、10進法では15となる。</li>"
            "<li><strong>④</strong>　正の数なので符号部は0である。また、指数部は、②で求めた1にバイアスの15を加算した16なので、%s となる。仮数部は、②で求めた小数の最上位の1を省略した1001に、残りの桁を0で埋めて、%s である。よって、%s となる。</li></ul>"
            % (b("11.001"), b("11.001"), b("1.1001"), b("01111"), b("10000"), b("1001000000"), b("0  10000  1001000000")))),
        fb_section("例題46 との違い(補足)", explain(
            "<p>手順は例題46 と同じ四段ですが、②で小数点を動かす桁数が違います。11.001 は小数点を左に 1 つ動かすので指数は 1、例題46 の 110.11 は 2 つ動かすので指数は 2 でした。"
            "動かした桁数がそのまま指数になり、バイアス 15 を足したものが指数部です。</p>")),
        viz("16 BITS — 3.125", "符号部 0、指数部 1＋15＝16、仮数部は 1001 のあとを 0 で埋めます。",
            bits16("0", "10000", "1001000000", "3.125＝11.001<sub>(2)</sub>＝1.1001<sub>(2)</sub>×2<sup>1</sup>。指数 1＋バイアス 15＝16＝10000<sub>(2)</sub>。")),
    ]), grade_label="自己採点する")

# ============================================================
# 類題80 — コンピュータによる演算誤差
# ============================================================
P80 = stage_practice(
    6, 13, "80", "ベストフィット 類題80", "〈コンピュータによる演算誤差〉", "p6", SINGLE_TAG,
    "次の(ア)～(エ)の記述のうち、桁落ちの説明として最も適当なものを一つ選べ。",
    "",
    opts_single("p80", 0, [
        ("ア", "値がほぼ等しい二つの浮動小数点数の引き算を行ったとき、有効桁数が大幅に減ってしまうことで発生する。"),
        ("イ", "計算した結果の桁数が、扱えるビット数の最大値を超えることによって生じる誤差のことである。"),
        ("ウ", "計算した結果、最小の桁より小さい部分の四捨五入、切り上げまたは切り捨てを行うことによって生じる誤差のことである。"),
        ("エ", "絶対値の大きな値と絶対値の小さな値の加算において、小さな値の桁情報が結果に反映されないことである。"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">(ア)</div>'),
        fb_section("解説(原本)", explain(
            "<p>桁落ちは、絶対値のほぼ等しい二つの数の引き算を行ったとき、有効桁数が減少するために発生する。</p>"
            "<ul><li><strong>(イ)</strong>　適当でない。桁あふれ誤差のオーバーフローの説明である。</li>"
            "<li><strong>(ウ)</strong>　適当でない。丸め誤差の説明である。</li>"
            "<li><strong>(エ)</strong>　適当でない。情報落ちの説明である。</li></ul>")),
        fb_section("四つを並べて読む(補足)", explain(
            "<p>五つの誤差のうち、この問題には打ち切り誤差だけが出てきません。残る四つの説明が一つずつ並んでいるので、名前と場面を対にして読めば、桁落ちの(ア)だけでなく、ほかの三つも同時に確かめられます。</p>")),
        viz("FOUR STATEMENTS — それぞれ何の説明か", "(ア)以外の三つも、確認事項の定義そのままです。",
            bd_grid([
                ("(ア)", "桁落ち", "値がほぼ等しい二つの数の引き算 → 有効桁数が大幅に減る"),
                ("(イ)", "桁あふれ誤差", "結果の桁数が扱えるビット数の最大値を超える(オーバーフロー)"),
                ("(ウ)", "丸め誤差", "最小の桁より小さい部分の四捨五入・切り上げ・切り捨て"),
                ("(エ)", "情報落ち", "大きな値と小さな値の加算で、小さな値の桁情報が反映されない"),
            ])),
    ]))

# ============================================================
# 類題81 — 論理回路(ド・モルガンの法則)
# ============================================================
P81_LEAD = (
    "集合について成り立つ「ド・モルガンの法則」がある。それを以下に示す(①、②)。なお、集合をAとB、記号を和集合∪、共通部分(積集合)∩、補集合 %s とする。"
    % ov("A"))
P81_EXTRA = (
    quote_box(
        '<div style="font-family: var(--f-mono); font-size: 1.05rem; line-height: 2.2;">'
        '%s ＝ %s∩%s　　①<br>'
        '%s ＝ %s∪%s　　②</div>' % (ov("A∪B"), ov("A"), ov("B"), ov("A∩B"), ov("A"), ov("B")))
    + '<p class="problem-q">この関係は、集合A、Bを「入力」、共通部分(積集合)を「論理積」、和集合を「論理和」、補集合を「否定」とすると、論理回路にもなり立つ法則である。そこで、次の問いに答えよ。ただし、解答には次の論理回路を用いること。</p>\n'
    + fig_row([
        figure("assets/fig19-and-gate-q81.jpeg", "＜論理積＞ AND回路の図記号", "＜論理積＞", 180, 140),
        figure("assets/fig20-or-gate-q81.jpeg", "＜論理和＞ OR回路の図記号", "＜論理和＞", 180, 140),
        figure("assets/fig21-not-gate-q81.jpeg", "＜否定＞ NOT回路の図記号", "＜否定＞", 180, 140),
    ])
)

P81 = stage_practice(
    7, 13, "81", "ベストフィット 類題81", "〈論理回路〉", "p7", SELF_TAG,
    P81_LEAD,
    P81_EXTRA,
    self_list([
        ("⑴", '<div style="flex:1 1 auto; min-width:0;">次に示した論理回路は、①の右辺を論理回路で示したものである。①の左辺の回路を答えよ。'
         + figure("assets/fig22-q81-1-circuit.jpeg", "①の右辺の論理回路: 入力 A と B をそれぞれ否定回路に通し、二つの出力を論理積回路に入れて X を出す", "①の右辺の論理回路", 420, 380) + '</div>',
         "<p><strong>論理和回路に否定回路を接続する</strong></p>"
         + figure("assets/ans81-1-not-or.jpeg", "解答⑴: 入力 A と B を論理和回路に入れ、その出力を否定回路に通して X を出す", "⑴ の解答(原本の図)", 420, 380)
         + "<p>求める①の左辺「%s」は、入力A、Bの論理和「A∪B」の否定である。よって、論理回路＜論理和＞に論理回路＜否定＞を接続する。</p>" % ov("A∪B")),
        ("⑵", '<div style="flex:1 1 auto; min-width:0;">次に示した論理回路は、②の左辺を論理回路で示したものである。②の右辺の回路を答えよ。'
         + figure("assets/fig23-q81-2-circuit.jpeg", "②の左辺の論理回路: 入力 A と B を論理積回路に入れ、その出力を否定回路に通して X を出す", "②の左辺の論理回路", 420, 380) + '</div>',
         "<p><strong>否定回路に論理和回路を接続する</strong></p>"
         + figure("assets/ans81-2-or-of-nots.jpeg", "解答⑵: 入力 A と B をそれぞれ否定回路に通し、二つの出力を論理和回路に入れて X を出す", "⑵ の解答(原本の図)", 420, 380)
         + "<p>求める②の右辺「%s∪%s」は、各入力A、Bの否定「%s」、「%s」の論理和である。よって、論理回路＜否定＞に論理回路＜論理和＞を接続する。</p>" % (ov("A"), ov("B"), ov("A"), ov("B"))),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ 論理和回路の出力に否定回路を接続した回路(模範解答の図)<br>⑵ 各入力を否定回路に通してから論理和回路に接続した回路(模範解答の図)</div>'),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　求める①の左辺「%s」は、入力A、Bの論理和「A∪B」の否定である。よって、論理回路＜論理和＞に論理回路＜否定＞を接続する。</li>"
            "<li><strong>⑵</strong>　求める②の右辺「%s∪%s」は、各入力A、Bの否定「%s」、「%s」の論理和である。よって、論理回路＜否定＞に論理回路＜論理和＞を接続する。</li></ul>"
            % (ov("A∪B"), ov("A"), ov("B"), ov("A"), ov("B")))),
        fb_section("上線の位置を回路に写す(補足)", explain(
            "<p>上線が式全体にかかっていれば、回路の最後に否定を置きます。上線が A と B に別々にかかっていれば、入力のすぐあとにそれぞれ否定を置きます。"
            "∪は論理和、∩は論理積です。⑴は「和のあとに否定」、⑵は「否定のあとに和」で、否定の位置が入れ替わります。</p>")),
        viz("DE MORGAN — 集合の記号と回路の対応", "上線の位置が、否定回路を置く位置になります。",
            compare2(
                ("① %s ＝ %s∩%s" % (ov("A∪B"), ov("A"), ov("B")), [
                    ("右辺(問題の図)", "A・B を否定してから論理積"),
                    ("左辺(答え)", "A・B の論理和を否定"),
                    ("否定の位置", "回路の最後"),
                ]),
                ("② %s ＝ %s∪%s" % (ov("A∩B"), ov("A"), ov("B")), [
                    ("左辺(問題の図)", "A・B の論理積を否定"),
                    ("右辺(答え)", "A・B を否定してから論理和"),
                    ("否定の位置", "入力のすぐあと"),
                ]))
            + note_box("集合A、Bを「入力」、共通部分(積集合)を「論理積」、和集合を「論理和」、補集合を「否定」とすると、論理回路にもなり立つ法則である(問題文)。")),
    ]), grade_label="自己採点する")

# ============================================================
# 類題82 — 真理値表(2 入力)
# ============================================================
TT82 = truth_table(["A", "B"], [([0, 0], 1), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)])

P82 = stage_practice(
    8, 13, "82", "ベストフィット 類題82", "〈真理値表〉", "p8", SELF_TAG,
    "次の図のように、論理回路を組み合わせた回路を作った。このとき、入力A、Bと出力Xの真理値表を作成せよ。",
    figure("assets/fig24-q82-circuit.jpeg", "図: 入力 A と B を論理積回路に入れ、その出力を否定回路に通して X を出す回路", "図: 論理回路を組み合わせた回路", 460, 420),
    self_list([
        (None, "入力A、Bと出力Xの真理値表を作成せよ。",
         TT82 + "<p>入力A、Bは論理積(AND)回路につながっており、その出力が否定(NOT)回路につながっている。よって、A、Bの論理積を反転した結果が出力Xとなる。</p>"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">上の真理値表(X は 1・1・1・0)</div>'),
        fb_section("解説(原本)", explain(
            "<p>入力の数がAとBの二つなので、入力の枠の行数は、2<sup>2</sup>＝4 である。0と1のすべての組合せを記入後、それぞれの出力を記入する。</p>"
            "<p>入力A、Bは論理積(AND)回路につながっており、その出力が否定(NOT)回路につながっている。よって、A、Bの論理積を反転した結果が出力Xとなる。</p>")),
        fb_section("列を一つ足して考える(補足)", explain(
            "<p>途中の値(論理積の出力)を一列足して書くと、反転の対象がはっきりします。論理積は 11 のときだけ 1 なので、その列は 0・0・0・1。これを反転した 1・1・1・0 が X です。"
            "例題48 の(エ)否定論理積回路(NAND回路)と同じ働きです。</p>")),
        viz("STEP BY STEP — 途中の列を足す", "AND の出力を書いてから、NOT で反転します。",
            tbl(["A", "B", "A AND B", "X ＝ NOT(A AND B)"],
                [["0", "0", "0", "<strong>1</strong>"], ["0", "1", "0", "<strong>1</strong>"], ["1", "0", "0", "<strong>1</strong>"], ["1", "1", "1", "<strong>0</strong>"]],
                caption="途中の列(A AND B)を足した表", mono=True)),
    ]), grade_label="自己採点する")

# ============================================================
# 類題83 — 真理値表(3 入力)
# ============================================================
TT83 = truth_table(["A", "B", "C"], [([0, 0, 0], 1), ([0, 0, 1], 0), ([0, 1, 0], 1), ([0, 1, 1], 0),
                                     ([1, 0, 0], 1), ([1, 0, 1], 0), ([1, 1, 0], 1), ([1, 1, 1], 1)])

P83 = stage_practice(
    9, 13, "83", "ベストフィット 類題83", "〈真理値表〉", "p9", SELF_TAG,
    "次の図のように、論理回路を組み合わせた回路を作った。このとき、入力A、B、Cと出力Xの真理値表を作成せよ。",
    figure("assets/fig25-q83-circuit.jpeg", "図: 入力 A と B を論理積回路に入れ、入力 C を否定回路に通し、二つの出力を論理和回路に入れて X を出す回路", "図: 論理回路を組み合わせた回路", 460, 420),
    self_list([
        (None, "入力A、B、Cと出力Xの真理値表を作成せよ。",
         TT83 + "<p>入力Cは否定(NOT)回路につながっており、さらにその出力は論理和(OR)回路につながっている。よって、入力Cが0のときはすべて、出力Xが1になる。</p>"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">上の真理値表(X は 1・0・1・0・1・0・1・1)</div>'),
        fb_section("解説(原本)", explain(
            "<p>入力の数がA、B、Cの三つなので、入力の枠の行数は、2<sup>3</sup>＝8である。0と1のすべての組合せを記入するには、次の手順で進める。</p>"
            "<ul><li><strong>①</strong>　Aの上半分の4行を0、下半分の4行を1とする。</li>"
            "<li><strong>②</strong>　Aの0の4行の上半分の2行分のBを0、下半分の2行分を1とし、Aの1の4行についても上半分を0、下半分を1とする。</li>"
            "<li><strong>③</strong>　最後にCは、Bの2行の0、2行の1に対して0、1を記入する。</li></ul>"
            "<p>入力Cは否定(NOT)回路につながっており、さらにその出力は論理和(OR)回路につながっている。よって、入力Cが0のときはすべて、出力Xが1になる。</p>")),
        fb_section("C が 1 の行の決め方(補足)", explain(
            "<p>C が 0 の行は、否定の出力が 1 なので論理和も 1 になり、A・B を見なくても X＝1 です。C が 1 の行は否定の出力が 0 なので、X は A と B の論理積で決まります。"
            "A＝B＝1 の最後の行だけが 1、残りの 3 行は 0 です。</p>")),
        viz("EIGHT ROWS — 途中の列を足す", "C の否定と、A AND B の列を足してから論理和を取ります。",
            tbl(["A", "B", "C", "A AND B", "NOT C", "X"],
                [["0", "0", "0", "0", "1", "<strong>1</strong>"], ["0", "0", "1", "0", "0", "<strong>0</strong>"],
                 ["0", "1", "0", "0", "1", "<strong>1</strong>"], ["0", "1", "1", "0", "0", "<strong>0</strong>"],
                 ["1", "0", "0", "0", "1", "<strong>1</strong>"], ["1", "0", "1", "0", "0", "<strong>0</strong>"],
                 ["1", "1", "0", "1", "1", "<strong>1</strong>"], ["1", "1", "1", "1", "0", "<strong>1</strong>"]],
                caption="X ＝ (A AND B) OR (NOT C)", mono=True)
            + checklist([
                ("①", "A", "上半分の4行を0、下半分の4行を1"),
                ("②", "B", "Aの各半分を、さらに上2行 0・下2行 1"),
                ("③", "C", "Bの2行ごとに 0、1"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 練習84 — 実数の表現
# ============================================================
P84 = stage_practice(
    10, 13, "84", "ベストフィット 練習84", "〈実数の表現〉", "p10", SELF_TAG,
    "次の問いに答えよ。",
    "",
    self_list([
        ("⑴", "－5.75を16ビットの2進数の浮動小数点数(符号部1ビット、指数部5ビット、仮数部10ビット)で表せ。",
         "<p><strong>%s</strong></p>"
         "<p>① －5.75＝－(4＋1＋0.5＋0.25) と表すことができるので、4と1と0.5と0.25の桁はあり、2の桁はないので、－%s となる。<br>"
         "② －%s＝－%s×2<sup>2</sup> となる。<br>"
         "③ 指数部5ビットなので、バイアスは %s である。<br>"
         "④ 負の数なので符号部は1である。また、指数部は、②で求めた2にバイアスの15を加算した17なので、%s となる。仮数部は、②で求めた小数の最上位の1を省略した0111に、残りの桁を0で埋めて、%s である。</p>"
         % (b("1  10001  0111000000"), b("101.11"), b("101.11"), b("1.0111"), b("01111"), b("10001"), b("0111000000"))),
        ("⑵", "16ビットの2進数の浮動小数点数(符号部1ビット、指数部5ビット、仮数部10ビット)である%s を10進数で表せ。" % b("0 10010 1010100000"),
         "<p><strong>13.25</strong></p>"
         "<p>・符号部が0なので、正の数である。<br>"
         "・バイアスは %s であり、指数部からバイアスを引いて、%s－%s＝%s よって、2<sup>3</sup> となる。仮数部は、%s なので、省略した最上位の1を追加し、求めた指数と合わせて %s×2<sup>3</sup> と表される。<br>"
         "・%s×2<sup>3</sup>＝1101.0100000<br>"
         "・8と4と1と0.25の桁に1があるので、8＋4＋1＋0.25＝13.25と求められる。</p>"
         % (b("01111"), b("10010"), b("01111"), b("00011"), b("1010100000"), b("1.1010100000"), b("1.1010100000"))),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ %s<br>⑵ 13.25</div>' % b("1  10001  0111000000")),
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong></p>"
            "<ul><li><strong>①</strong>　10進数を2進数の小数(指数を用いない形)に変換<br>－5.75＝－(4＋1＋0.5＋0.25) と表すことができるので、4と1と0.5と0.25の桁はあり、2の桁はないので、－%s となる。</li>"
            "<li><strong>②</strong>　指数を用いた「1.～<sub>(2)</sub>×2<sup>n</sup>」の形で表す。<br>－%s＝－%s×2<sup>2</sup> となる。</li>"
            "<li><strong>③</strong>　浮動小数点数で表現するためのバイアスを求める。<br>指数部5ビットなので、%s である。</li>"
            "<li><strong>④</strong>　16ビットの2進数の浮動小数点数の形で表す。<br>負の数なので符号部は1である。また、指数部は、②で求めた2にバイアスの15を加算した17なので、%s となる。仮数部は、②で求めた小数の最上位の1を省略した0111に、残りの桁を0で埋めて、%s である。よって、%s となる。</li></ul>"
            "<p><strong>⑵</strong></p>"
            "<ul><li>正負を求める。<br>符号部が0なので、正の数である。</li>"
            "<li>指数を用いた「1.～<sub>(2)</sub>×2<sup>n</sup>」の形で表す。<br>バイアスは %s であり、指数部からバイアスを引いて、%s－%s＝%s<br>よって、2<sup>3</sup> となる。<br>仮数部は、%s なので、省略した最上位の1を追加し、求めた指数と合わせて<br>%s×2<sup>3</sup> と表される。</li>"
            "<li>2進数の小数(指数を用いない形)に変換<br>%s×2<sup>3</sup>＝1101.0100000</li>"
            "<li>2進数の小数(指数を用いない形)を10進数に変換<br>8と4と1と0.25の桁に1があるので、8＋4＋1＋0.25＝13.25と求められる。</li></ul>"
            % (b("101.11"), b("101.11"), b("1.0111"), b("01111"), b("10001"), b("0111000000"), b("1  10001  0111000000"),
               b("01111"), b("10010"), b("01111"), b("00011"), b("1010100000"), b("1.1010100000"), b("1.1010100000")))),
        fb_section("行きと帰り(補足)", explain(
            "<p>⑴は 10進数 → 浮動小数点数、⑵は浮動小数点数 → 10進数で、手順を逆にたどります。どちらも真ん中に「1.～×2<sup>n</sup>」の形を置くと迷いません。"
            "⑴の符号は最後に符号部へ、⑵の指数は「指数部からバイアス 15 を引く」で戻します。</p>")),
        viz("16 BITS — 行きと帰り", "⑴ は組み立て、⑵ は分解です。",
            bits16("1", "10001", "0111000000", "⑴ －5.75＝－101.11<sub>(2)</sub>＝－1.0111<sub>(2)</sub>×2<sup>2</sup>。負なので符号部 1、指数 2＋15＝17＝10001<sub>(2)</sub>。")
            + bits16("0", "10010", "1010100000", "⑵ 指数部 10010<sub>(2)</sub>＝18、18－15＝3。1.1010100000<sub>(2)</sub>×2<sup>3</sup>＝1101.01<sub>(2)</sub>＝13.25。")),
    ]), grade_label="自己採点する")

# ============================================================
# 練習85 — 実数の表現(加算)
# ============================================================
P85_TEXT = quote_box(
    "加算する二数を、A＝%s、B＝%s とする。<br>\n"
    "AとBは、指数部の数値が異なるのでそのままでは加算できない。そこで、両者を指数のない2進数の小数へ変換してから計算することにする。<br>\n"
    "・Aについて<br>\n"
    "符号部は0なので、「正の数」である。<br>\n"
    "また、指数部は5ビットなので、バイアスは %s<sub>(2)</sub> である。よって、%s からバイアスを引き算し、%s つまり2となる。<br>\n"
    "仮数部は %s なので、省略している1を考慮して「 %s<sub>(2)</sub> 」となり、<br>\n"
    "よって、Aは %s<sub>(2)</sub>×2<sup>2</sup> つまり、%s と変換することができる。<br>\n"
    "・Bについて<br>\n"
    "Aと同様に、指数のない2進数の小数に変換すると、Bは %s<sub>(2)</sub>となる。<br>\n"
    "以上から、A＋Bは、%s＋ %s<sub>(2)</sub>＝%s である。<br>\n"
    "これを、先ほどと逆の流れで、%s×2<sup>2</sup> とし、符号部は0、指数部は %s<sub>(2)</sub>、仮数部は%s となる。よって加算した結果は、浮動小数点数で表すと %s<sub>(2)</sub>と求めることができる。<br>\n"
    "また、同様に考えて、%s と %s の二つの数を加算すると %s<sub>(2)</sub> と求めることができる。\n"
    % (b("0 10001 0101110000"), b("0 10000 0010110000"),
       blank("ア"), b("10001"), b("00010"),
       b("0101110000"), blank("イ"),
       blank("イ"), b("101.01110000"),
       blank("ウ"),
       b("101.01110000"), blank("ウ"), b("111.11001000"),
       b("1.1111001000"), blank("エ"), b("1111001000"), blank("オ"),
       b("0 10010 1101100000"), b("1 10001 1001010000"), blank("カ"))
)

P85 = stage_practice(
    11, 13, "85", "ベストフィット 練習85", "〈実数の表現〉", "p11", SELF_TAG,
    "16ビットの2進数の浮動小数点数(符号部1ビット、指数部5ビット、仮数部10ビット)どうしの加算について述べた、次の文章の空欄に入る最も適当な2進数を答えよ。",
    P85_TEXT,
    self_list([
        ("ア", "バイアスは %s<sub>(2)</sub> である。" % blank("ア"),
         "<p><strong>01111</strong><br>バイアスは、5ビットの指数部の場合、最上位を0とし、残りの4ビットを1とした %sである。</p>" % b("01111")),
        ("イ", "省略している1を考慮して「 %s<sub>(2)</sub> 」となり" % blank("イ"),
         "<p><strong>1.0101110000</strong><br>省略している1を付け加えて、「1.～」の形にする。よって、%sである。</p>" % b("1.0101110000")),
        ("ウ", "Bは %s<sub>(2)</sub> となる。" % blank("ウ"),
         "<p><strong>10.010110000</strong><br>指数部が %s なので、バイアスの %s を引くと、%s つまり1である。仮数部は、省略している1を付け加えて、「1.～」の形にすると、%s である。よって、Bは、%s×2<sup>1</sup> つまり %s と表すことができる。</p>"
         % (b("10000"), b("01111"), b("00001"), b("1.0010110000"), b("1.0010110000"), b("10.010110000"))),
        ("エ", "指数部は %s<sub>(2)</sub>" % blank("エ"),
         "<p><strong>10001</strong><br>%s×2<sup>2</sup> であることから、指数部は、%s にバイアスの %s を加えた %s となる。</p>" % (b("1.1111001000"), b("00010"), b("01111"), b("10001"))),
        ("オ", "浮動小数点数で表すと %s<sub>(2)</sub>" % blank("オ"),
         "<p><strong>0  10001  1111001000</strong><br>符号部は0、指数部は %s、仮数部は %s なので、%s である。</p>" % (b("10001"), b("1111001000"), b("0  10001  1111001000"))),
        ("カ", "%s と %s を加算すると %s<sub>(2)</sub>" % (b("0 10010 1101100000"), b("1 10001 1001010000"), blank("カ")),
         "<p><strong>0  10010  0000111000</strong><br>%s は %s×2<sup>3</sup> つまり %s、%s は負の数で －%s×2<sup>2</sup> つまり －%s。加算結果は %s＋(－%s)＝%s。これを %s×2<sup>3</sup> とし、符号部 0、指数部 %s＋%s＝%s、仮数部 %s。</p>"
         % (b("0 10010 1101100000"), b("1.1101100000"), b("1110.1100000"), b("1 10001 1001010000"), b("1.1001010000"), b("110.01010000"),
            b("1110.1100000"), b("110.01010000"), b("1000.0111000"), b("1.0000111000"), b("00011"), b("01111"), b("10010"), b("0000111000"))),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">ア：01111　　イ：1.0101110000　　ウ：10.010110000<br>エ：10001　　オ：0  10001  1111001000<br>カ：0  10010  0000111000</div>'),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>ア</strong>　バイアスは、5ビットの指数部の場合、最上位を0とし、残りの4ビットを1とした %sである。</li>"
            "<li><strong>イ</strong>　省略している1を付け加えて、「1.～」の形にする。よって、%sである。</li>"
            "<li><strong>ウ</strong>　指数部が %s なので、バイアスの %s を引くと、%s つまり1である。<br>仮数部は、省略している1を付け加えて、「1.～」の形にすると、%s である。<br>よって、Bは、%s×2<sup>1</sup> つまり %s と表すことができる。</li>"
            "<li><strong>エ</strong>　%s×2<sup>2</sup> であることから、指数部は、%s にバイアスの %s を加えた %s となる。</li>"
            "<li><strong>オ</strong>　符号部は0、指数部は %s、仮数部は %s なので、%s である。</li>"
            "<li><strong>カ</strong>　%s について<br>指数部が %s なので、バイアスの %s を引くと、%s つまり3である。<br>仮数部は、省略している1を付け加えて、「1.～」の形にすると、%sである。<br>よって、%s×2<sup>3</sup> つまり %s と表すことができる。<br>"
            "%s について<br>符号部は、1なので負の数である。<br>指数部が %s なので、バイアスの %s を引くと、%s つまり2である。<br>仮数部は、省略している1を付け加えて、「1.～」の形にすると、－%sである。<br>よって、－%s×2<sup>2</sup> つまり －%s と表すことができる。<br>"
            "以上から、加算結果は、%s＋(－%s)＝%s となる。<br>これを、浮動小数点数で表現する。<br>正の数なので、符号部は0である。<br>%s＝%s×2<sup>3</sup> から、指数部は、%s＋%s＝%s である。<br>仮数部は、先頭の1を省略し、%sである。<br>以上から、%s となる。</li></ul>"
            % (b("01111"), b("1.0101110000"),
               b("10000"), b("01111"), b("00001"), b("1.0010110000"), b("1.0010110000"), b("10.010110000"),
               b("1.1111001000"), b("00010"), b("01111"), b("10001"),
               b("10001"), b("1111001000"), b("0  10001  1111001000"),
               b("0 10010 1101100000"), b("10010"), b("01111"), b("00011"), b("1.1101100000"), b("1.1101100000"), b("1110.1100000"),
               b("1 10001 1001010000"), b("10001"), b("01111"), b("00010"), b("1.1001010000"), b("1.1001010000"), b("110.01010000"),
               b("1110.1100000"), b("110.01010000"), b("1000.0111000"), b("1000.0111000"), b("1.0000111000"), b("00011"), b("01111"), b("10010"),
               b("0000111000"), b("0  10010  0000111000")))),
        fb_section("10進数で検算する(補足)", explain(
            "<p>A＝101.0111<sub>(2)</sub>＝5.4375、B＝10.01011<sub>(2)</sub>＝2.34375 で、A＋B＝7.78125＝111.11001<sub>(2)</sub> です。"
            "カは 1110.11<sub>(2)</sub>＝14.75 と －110.0101<sub>(2)</sub>＝－6.3125 の和で 8.4375＝1000.0111<sub>(2)</sub> です。10進数で足しても同じ値になれば、2進数の筆算が合っています。</p>")),
        viz("SIX BLANKS — 分解して足し、また組み立てる", "指数をそろえるために一度「指数のない小数」に戻し、足してから浮動小数点数へ戻します。",
            bd_grid([
                ("ア", "01111", "5 ビットのバイアス＝15"),
                ("イ", "1.0101110000", "A の仮数部に先頭の 1 を戻す"),
                ("ウ", "10.010110000", "B を指数のない小数に(指数 1)"),
                ("エ", "10001", "指数 2＋バイアス 15＝17"),
                ("オ", "0 10001 1111001000", "A＋B＝111.11001000 を戻す"),
                ("カ", "0 10010 0000111000", "14.75＋(－6.3125)＝8.4375＝1000.0111"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# 練習86 — 真理値表(選択)
# ============================================================
P86 = stage_practice(
    12, 13, "86", "ベストフィット 練習86", "〈真理値表〉", "p12", SINGLE_TAG,
    "次に示す論理回路の真理値表として最も適当なものを、下の(ア)～(エ)から一つ選べ。",
    figure("assets/fig26-q86-circuit.jpeg", "図: 入力 A と B。A と B をそれぞれ否定回路に通して論理和回路に入れ、その出力と A を論理積回路に、その出力と B を論理積回路に入れ、二つの論理積の出力を論理和回路に入れて X を出す回路", "図: 論理回路", 560, 520),
    opts_single("p86", 2, [
        ("ア", inline_img("assets/fig27-q86-table-a.png", "(ア) 真理値表: X は 0・1・0・1", 150)),
        ("イ", inline_img("assets/fig28-q86-table-b.png", "(イ) 真理値表: X は 1・0・0・1", 150)),
        ("ウ", inline_img("assets/fig29-q86-table-c.png", "(ウ) 真理値表: X は 0・1・1・0", 150)),
        ("エ", inline_img("assets/fig30-q86-table-d.png", "(エ) 真理値表: X は 1・1・0・0", 150)),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">(ウ)</div>'),
        fb_section("解説(原本)", explain(
            "<p>入力A、Bのすべての組合せを順番に確かめ、出力Xの違うものを除いていけばよい。</p>"
            "<ul><li><strong>①</strong>　A＝0、B＝0のとき<br>出力Xは0となるので、真理値表で出力Xが1となっている(イ)と(エ)が除かれる。"
            + figure("assets/ans86-1-a0b0.jpeg", "A＝0、B＝0 のとき: 否定の出力はともに 1、論理和は 1、二つの論理積はともに 0、出力 X は 0", "A＝0、B＝0 のとき(原本の図)", 560, 520)
            + "</li><li><strong>②</strong>　A＝0、B＝1のとき<br>残りの候補の(ア)、(ウ)ともに真理値表での出力Xは1となっており同じなので、次の組合せを確かめる。</li>"
            "<li><strong>③</strong>　A＝1、B＝0のとき<br>出力Xは1となるので、残りの候補の(ア)、(ウ)のうち真理値表での出力Xが0となっている(ア)が除かれ、正答の(ウ)が求められる。"
            + figure("assets/ans86-2-a1b0.jpeg", "A＝1、B＝0 のとき: 否定の出力は 0 と 1、論理和は 1、上の論理積は 1、下の論理積は 0、出力 X は 1", "A＝1、B＝0 のとき(原本の図)", 560, 520)
            + "</li></ul>")),
        fb_section("四つの行を全部書くと(補足)", explain(
            "<p>残る A＝1、B＝1 のときは、否定の出力がともに 0 なので論理和は 0、二つの論理積も 0 で X＝0 です。四行そろえると X は 0・1・1・0 で、例題48 の(ウ)排他的論理和回路(XOR回路)と同じ出力になります。"
            "選択問題では原本のように、違いが出る行だけ確かめて候補を減らすのが速い方法です。</p>")),
        viz("ELIMINATION — 違う行で候補を減らす", "全部の行を作らず、答えが割れる組合せから確かめます。",
            checklist([
                ("①", "A＝0、B＝0 → X＝0", "X が 1 の(イ)(エ)を除く"),
                ("②", "A＝0、B＝1 → X＝1", "(ア)(ウ)とも 1 なので決まらない"),
                ("③", "A＝1、B＝0 → X＝1", "X が 0 の(ア)を除く → (ウ)"),
            ], warn="四行すべては 0・1・1・0。二つの入力の一方だけが 1 のとき出力が 1 になる回路です。")),
    ]))

# ============================================================
# 練習87 — 論理回路(同じ出力)
# ============================================================
TT87 = truth_table(["A", "B"], [([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 0)])

P87 = stage_practice(
    13, 13, "87", "ベストフィット 練習87", "〈論理回路〉", "p13", SINGLE_TAG,
    "次に示す論理回路と同じ出力が得られる論理回路を、下の(ア)～(オ)から一つ選べ。",
    figure("assets/fig31-q87-circuit.jpeg", "図: 入力 A を否定回路に通した出力と、A と B の論理和回路の出力を、論理積回路に入れて X を出す回路", "図: 論理回路", 460, 420),
    opts_single("p87", 3, [
        ("ア", inline_img("assets/fig32-q87-option-a.jpeg", "(ア) A と B の論理和を否定回路に通す回路", 70)),
        ("イ", inline_img("assets/fig33-q87-option-b.jpeg", "(イ) A と B の論理和の出力と B を論理積回路に入れる回路", 70)),
        ("ウ", inline_img("assets/fig34-q87-option-c.jpeg", "(ウ) A と、B の否定を論理積回路に入れる回路", 70)),
        ("エ", inline_img("assets/fig35-q87-option-d.jpeg", "(エ) A と、B の否定を論理和回路に入れ、その出力を否定回路に通す回路", 70)),
        ("オ", inline_img("assets/fig36-q87-option-e.jpeg", "(オ) A と B の論理積の出力と、B の否定を論理和回路に入れる回路", 70)),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">(エ)</div>'),
        fb_section("解説(原本)", explain(
            "<p>はじめに、問題に示された論理回路の真理値表を作成する。</p>" + TT87 +
            "<p>次に、(ア)～(オ)の論理回路の真理値表を作成して比較してもよいが、効率的に入力A、Bのすべての組合せを順番に確かめ、出力Xの違うものを除いていく。</p>"
            "<ul><li><strong>①</strong>　A＝0、B＝0のとき<br>問題に示された論理回路の出力Xは0なので、出力Xが1となる論理回路(ア)、(オ)は除かれる。</li>"
            "<li><strong>②</strong>　A＝0、B＝1のとき<br>問題に示された論理回路の出力Xは1なので、残りの論理回路(イ)、(ウ)、(エ)のうち、出力Xが0となる論理回路(ウ)は除かれる。</li>"
            "<li><strong>③</strong>　A＝1、B＝0のとき<br>問題に示された論理回路の出力Xは0であるが、残った論理回路(イ)、(エ)のうち、出力Xが1となるものはないので除かれるものはない。</li>"
            "<li><strong>④</strong>　A＝1、B＝1のとき<br>問題に示された論理回路の出力Xは0なので、出力Xが1となる論理回路(イ)は除かれ、出力Xが0となる論理回路(エ)が正答となる。</li></ul>")),
        fb_section("問題の回路の読み方(補足)", explain(
            "<p>問題の回路は、A の否定と「A または B」の論理積です。A＝1 なら否定が 0 なので X＝0、A＝0 なら「A または B」は B そのものなので X＝B。"
            "つまり A＝0 かつ B＝1 のときだけ 1 になります。(エ)は「A または（B の否定）」の全体を否定した回路です。類題81 のド・モルガンの法則で書き換えると「A の否定 かつ B」になり、問題の回路と同じ働きです。</p>")),
        viz("ELIMINATION — 四つの組合せで絞る", "問題の回路の X は 0・1・0・0。同じ並びになる回路だけが残ります。",
            checklist([
                ("①", "A＝0、B＝0 → 0", "X が 1 になる(ア)(オ)を除く"),
                ("②", "A＝0、B＝1 → 1", "X が 0 になる(ウ)を除く"),
                ("③", "A＝1、B＝0 → 0", "(イ)(エ)とも 0。除かれない"),
                ("④", "A＝1、B＝1 → 0", "X が 1 になる(イ)を除く → (エ)"),
            ])),
    ]))

# ============================================================
# RESULT
# ============================================================
RESULT = """  <section class="stage" data-stage-name="RESULT">
    <div class="section-divider">
      <span class="num">02</span>
      <div class="text">
        <div class="label">Section 2 — Result</div>
        <div class="name">演習結果</div>
      </div>
    </div>
    <div class="summary-hero">
      <div class="summary-grade" id="summary-grade">—<span class="denom">/13</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">13問の練習問題のうち、何問完答できたかを示します。</div>
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
  </section>
"""

STAGES = (WELCOME + REVIEW + EX43 + EX44 + EX45 + EX46 + EX47 + EX48 + EX49
          + P75 + P76 + P77 + P78 + P79 + P80 + P81 + P82 + P83 + P84 + P85 + P86 + P87 + RESULT)

# ============================================================
# JS 差し替え
# ============================================================
TIMELINE = """  const TIMELINE_ENTRIES = [
    { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
    { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2,  group: 'examples', num: '例43', label: '2進数の加算と減算', probId: 'ex43' },
    { idx: 3,  group: 'examples', num: '例44', label: '補数', probId: 'ex44' },
    { idx: 4,  group: 'examples', num: '例45', label: '2進数の小数への変換', probId: 'ex45' },
    { idx: 5,  group: 'examples', num: '例46', label: '実数の表現', probId: 'ex46' },
    { idx: 6,  group: 'examples', num: '例47', label: 'コンピュータによる演算誤差', probId: 'ex47' },
    { idx: 7,  group: 'examples', num: '例48', label: '論理回路', probId: 'ex48' },
    { idx: 8,  group: 'examples', num: '例49', label: '真理値表', probId: 'ex49' },
    { idx: 9,  group: 'practice', num: 'Q75', label: '〈2進数の加算と減算〉', probId: 'p1' },
    { idx: 10, group: 'practice', num: 'Q76', label: '〈補数〉', probId: 'p2' },
    { idx: 11, group: 'practice', num: 'Q77', label: '〈2進数の小数への変換〉', probId: 'p3' },
    { idx: 12, group: 'practice', num: 'Q78', label: '〈2進数の小数からの変換〉', probId: 'p4' },
    { idx: 13, group: 'practice', num: 'Q79', label: '〈実数の表現〉', probId: 'p5' },
    { idx: 14, group: 'practice', num: 'Q80', label: '〈コンピュータによる演算誤差〉', probId: 'p6' },
    { idx: 15, group: 'practice', num: 'Q81', label: '〈論理回路〉', probId: 'p7' },
    { idx: 16, group: 'practice', num: 'Q82', label: '〈真理値表〉', probId: 'p8' },
    { idx: 17, group: 'practice', num: 'Q83', label: '〈真理値表〉', probId: 'p9' },
    { idx: 18, group: 'practice', num: 'Q84', label: '〈実数の表現〉', probId: 'p10' },
    { idx: 19, group: 'practice', num: 'Q85', label: '〈実数の表現〉', probId: 'p11' },
    { idx: 20, group: 'practice', num: 'Q86', label: '〈真理値表〉', probId: 'p12' },
    { idx: 21, group: 'practice', num: 'Q87', label: '〈論理回路〉', probId: 'p13' },
    { idx: 22, group: 'result',   num: '✓',   label: '結果サマリ' }
  ];"""

PROBLEMS = """  const PROBLEMS = [
    { id: 'p1',  label: 'Q75', name: '〈2進数の加算と減算〉', stageIdx: 9 },
    { id: 'p2',  label: 'Q76', name: '〈補数〉', stageIdx: 10 },
    { id: 'p3',  label: 'Q77', name: '〈2進数の小数への変換〉', stageIdx: 11 },
    { id: 'p4',  label: 'Q78', name: '〈2進数の小数からの変換〉', stageIdx: 12 },
    { id: 'p5',  label: 'Q79', name: '〈実数の表現〉', stageIdx: 13 },
    { id: 'p6',  label: 'Q80', name: '〈コンピュータによる演算誤差〉', stageIdx: 14 },
    { id: 'p7',  label: 'Q81', name: '〈論理回路〉', stageIdx: 15 },
    { id: 'p8',  label: 'Q82', name: '〈真理値表〉', stageIdx: 16 },
    { id: 'p9',  label: 'Q83', name: '〈真理値表〉', stageIdx: 17 },
    { id: 'p10', label: 'Q84', name: '〈実数の表現〉', stageIdx: 18 },
    { id: 'p11', label: 'Q85', name: '〈実数の表現〉', stageIdx: 19 },
    { id: 'p12', label: 'Q86', name: '〈真理値表〉', stageIdx: 20 },
    { id: 'p13', label: 'Q87', name: '〈論理回路〉', stageIdx: 21 }
  ];"""


# ============================================================
# 独立検算(原本の解答を計算で確かめる)
# ============================================================
def selfcheck():
    def bi(s):
        return int(s, 2)

    def comp(s):
        return format((1 << len(s)) - bi(s), "0%db" % len(s))

    def tobin(x):
        i = int(x)
        f = x - i
        s = format(i, "b") + "."
        while f:
            f *= 2
            s += str(int(f))
            f -= int(f)
        return s

    def half(x):
        s = "1" if x < 0 else "0"
        x = abs(x)
        e = 0
        while x >= 2:
            x /= 2
            e += 1
        while x < 1:
            x *= 2
            e -= 1
        m = x - 1
        mb = ""
        for _ in range(10):
            m *= 2
            mb += str(int(m))
            m -= int(m)
        return s + " " + format(e + 15, "05b") + " " + mb

    def unhalf(t):
        s, e, m = t.split()
        v = (1 + sum(int(ch) * 2 ** -(k + 1) for k, ch in enumerate(m))) * 2 ** (int(e, 2) - 15)
        return -v if s == "1" else v

    assert [format(bi(a) + bi(c), "04b") for a, c in [("1001", "0011"), ("0110", "0101")]] == ["1100", "1011"]
    assert [format(bi(a) - bi(c), "04b") for a, c in [("1011", "0110"), ("1110", "1001")]] == ["0101", "0101"]
    assert [comp(x) for x in ["1001", "0111", "01101010", "10011100"]] == ["0111", "1001", "10010110", "01100100"]
    assert [tobin(x) for x in [1.625, 5.75, 6.375]] == ["1.101", "101.11", "110.011"]
    assert half(6.75) == "0 10001 1011000000"
    assert [format(bi(a) + bi(c), "04b") for a, c in [("1010", "0101"), ("0100", "0111"), ("1011", "0011")]] == ["1111", "1011", "1110"]
    assert [format(bi(a) - bi(c), "04b") for a, c in [("1001", "0110"), ("1010", "0101"), ("1101", "1010")]] == ["0011", "0101", "0011"]
    assert [comp(x) for x in ["1100", "1010", "01001000", "10111000"]] == ["0100", "0110", "10111000", "01001000"]
    assert [tobin(x) for x in [3.25, 5.5625, 7.875, 7.625]] == ["11.01", "101.1001", "111.111", "111.101"]
    assert half(3.125) == "0 10000 1001000000" and half(-5.75) == "1 10001 0111000000"
    assert unhalf("0 10010 1010100000") == 13.25
    A = unhalf("0 10001 0101110000")
    B = unhalf("0 10000 0010110000")
    assert half(A + B) == "0 10001 1111001000"
    C = unhalf("0 10010 1101100000")
    D = unhalf("1 10001 1001010000")
    assert half(C + D) == "0 10010 0000111000"
    tt = lambda f: [f(a, c) for a in (0, 1) for c in (0, 1)]
    assert tt(lambda a, c: 1 - (a & c)) == [1, 1, 1, 0]
    assert [(a & c) | (1 - e) for a in (0, 1) for c in (0, 1) for e in (0, 1)] == [1, 0, 1, 0, 1, 0, 1, 1]
    P = lambda a, c: (1 - a) | (1 - c)
    assert tt(lambda a, c: (a & P(a, c)) | (P(a, c) & c)) == [0, 1, 1, 0]
    assert tt(lambda a, c: (1 - a) & (a | c)) == [0, 1, 0, 0] and tt(lambda a, c: 1 - (a | (1 - c))) == [0, 1, 0, 0]


def main():
    selfcheck()
    html = SRC.read_text(encoding="utf-8")

    def sub1(pattern, repl, text, flags=0, label=""):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        assert n == 1, "置換に失敗: %s" % (label or pattern)
        return new

    html = sub1(r"<title>.*?</title>",
                "<title>2進数と論理演算 | Practice Lab</title>", html, 0, "title")
    html = sub1(r'<span class="tg">CHAPTER 2\.06</span>',
                '<span class="tg">CHAPTER 3.09</span>', html, 0, "chapter tag")
    html = sub1(r'<span class="sb-score" id="sb-score">—/6</span>',
                '<span class="sb-score" id="sb-score">—/13</span>', html, 0, "sb-score")

    html = sub1(r'(<main id="stages">\n).*?(\n</main>)',
                lambda m: m.group(1) + STAGES.rstrip("\n") + m.group(2),
                html, re.S, "stages")

    html = sub1(r"  const TIMELINE_ENTRIES = \[.*?\n  \];",
                lambda m: TIMELINE, html, re.S, "TIMELINE_ENTRIES")
    html = sub1(r"  const PROBLEMS = \[.*?\n  \];",
                lambda m: PROBLEMS, html, re.S, "PROBLEMS")

    html = sub1(r"sbScore\.textContent = full \+ '/14';",
                "sbScore.textContent = full + '/13';", html, 0, "sb score denom")
    html = sub1(r"animateCounter\(grade, 0, fullCount, 1100, '<span class=\"denom\">/14</span>'\);",
                "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/13</span>');",
                html, 0, "grade denom")
    html = sub1(r"if \(fullCount >= 11\) grade\.classList\.add\('s-high'\);\n"
                r"    else if \(fullCount >= 7\) grade\.classList\.add\('s-mid'\);",
                "if (fullCount >= 11) grade.classList.add('s-high');\n"
                "    else if (fullCount >= 7) grade.classList.add('s-mid');",
                html, 0, "thresholds")

    # 原本の全角カンマは、キット慣例の「、」に(数値の 3 桁区切りは原本に無い)
    assert "，" not in STAGES, "全角カンマが残っている"
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT, len(html), "bytes")


if __name__ == "__main__":
    main()
