#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
practices 03-10「コンピュータの構成と動作」ビルダ

- エンジン(CSS / JS ハーネス / サイドバー / トップバー / フッタ)は
  examples/02-07-digital-info-representation.html を 1 文字も変えずに流用する(03-09 と同じ)。
- 差し替えるのは <main id="stages"> の中身と、JS の TIMELINE_ENTRIES / PROBLEMS /
  サマリ分母・閾値 だけ。
- 問題文・選択肢・解答・原本解説は _source の docx から逐語(「，」→「、」のみ)。
- 原本の図は assets/ に抽出済み(練習91 の仮想コンピュータ 1 枚)。
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
      <span>3章 第10節</span>
    </div>
    <h1 class="welcome-title-en">Computer<br>Architecture<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">コンピュータの構成と動作</h2>
    <p class="welcome-lede">
      CPU が命令を取り出し、解読し、実行する一連の動作から始めます。次に CPU の処理速度を決めるもの(クロック信号・コア数・スレッド数)を確かめ、最後にクロック周波数と周期から処理能力を計算します。仮想コンピュータのプログラムを 1 命令ずつ追う問題も扱います。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">examples</div>
        <div class="welcome-meta-value">3<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">7<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">45<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">3章10</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー この節の基本知識を、Q&amp;A形式の6モジュールで確認します(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>例題ツアー</strong>ー 例題50〜52の解き方を3問たどります(採点なし。計算は模範解答と照らします)</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>演習</strong>ー 類題88〜90・練習91〜94の計7問。回答 → 採点 → 解説</div></div>
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
          '    <div class="review-head">\n'
          '      <span class="review-kicker">Review</span>\n'
          '      <h2 class="review-title">おさらい — この節の基本知識</h2>\n'
          '      <p class="review-lede">問いをタップすると答えが開きます。複数同時に開けます。</p>\n'
          '    </div>\n'
          '    <div class="digest">\n'
          + digest_mod(
              "01", "The Big Map",
              '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><line x1="7" y1="11" x2="17" y2="7"/><line x1="7" y1="13" x2="17" y2="17"/>',
              "この節では、何を順に扱いますか?",
              "命令の動作 → CPU の性能 → 処理能力の計算",
              "はじめに、CPU が命令を取り出し・解読・実行する一連の動作と、その各段を担う装置を確かめます。次に、コンピュータの処理速度を決めるものを整理します。最後に、クロック周波数と周期から処理能力を計算します。",
              tbl(["観点", "扱うもの", "対応する問題"],
                  [["動作", "取り出し・解読・実行と、各段の装置", "例題50 / 類題88 / 練習91"],
                   ["性能", "CPU と主記憶装置のやり取り、コア・スレッド", "例題51 / 類題89"],
                   ["計算", "クロック周波数と周期、平均クロック数", "例題52 / 類題90 / 練習92〜94"]],
                  caption="この節の三つの観点"), hero=True)
          + digest_mod(
              "02", "Fetch, Decode, Execute",
              '<path d="M4 7h16M4 12h16M4 17h10"/>',
              "CPU の中では、命令がどんな順に処理されますか?",
              "取り出し → 解読 → 実行",
              "主記憶装置にはプログラムが記憶されており、CPU 内部ではプログラムの構成単位である命令の取り出し・解読・実行の一連の動作が順番に行われます(確認事項)。",
              tbl(["段", "何が起きるか", "担う装置"],
                  [["取り出し", "どの番地の命令を取り出すかを指定し、取り出した命令を一時的に保存する", "プログラムカウンタ → 命令レジスタ"],
                   ["解読", "命令を解読して各部を制御する", "命令解読器"],
                   ["実行", "データを一時的に保存し、演算を行う", "データレジスタ → 演算装置"]],
                  caption="例題50 の解説による三つの段"))
          + digest_mod(
              "03", "Inside the CPU",
              '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/>',
              "CPU の中の装置は、それぞれ何をしますか?",
              "名前が、記憶するものを表している",
              "○○レジスタという名前は「○○を記憶(一時保存)する」と読めます。命令解読器と演算装置は、名称から働きを推測できます(類題88 の解説)。",
              tbl(["装置", "内容"],
                  [["プログラムカウンタ", "主記憶装置のどの番地の命令を取り出すかを指定する"],
                   ["命令レジスタ", "主記憶装置から取り出した命令を一時的に保存する"],
                   ["命令解読器", "命令を解読して各部を制御する"],
                   ["データレジスタ", "データを一時的に保存する"],
                   ["演算装置", "加算などの算術演算やそのほかの演算を行う"]],
                  caption="確認事項の表"))
          + digest_mod(
              "04", "What Decides Speed",
              '<path d="M12 2v4M12 18v4M2 12h4M18 12h4"/><circle cx="12" cy="12" r="5"/>',
              "コンピュータの処理速度は、何で決まりますか?",
              "CPU だけでは決まらない",
              "CPU と主記憶装置のそれぞれの性能、および CPU と主記憶装置間の情報のやり取りの速さが、コンピュータの性能(処理能力)に大きく関係します(確認事項)。CPU の処理の速さだけに依存するわけではありません(例題51 ⑷)。",
              compare2(
                  ("関係するもの", [
                      ("CPU の性能", "ビット数・コア数・スレッド数・クロック周波数"),
                      ("主記憶装置の性能", "記憶装置そのものの速さ"),
                      ("両者のやり取り", "CPU と主記憶装置間の情報のやり取りの速さ"),
                  ]),
                  ("取り違えやすいところ", [
                      ("CPU だけで決まる", "誤り。やり取りの速さも関係する(例題51 ⑷)"),
                      ("古い CPU でも周波数が大きければ速い", "誤り。必ずしも処理能力は上がらない(類題89 ⑷)"),
                      ("クロック周期は関係ない", "誤り。短いほど処理能力が高い(類題89 ⑸)"),
                  ])))
          + digest_mod(
              "05", "Clock",
              '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
              "クロック周波数とクロック周期は、どんな関係ですか?",
              "逆数の関係",
              "クロック信号は、コンピュータ各回路での処理動作を行うタイミングを合わせるために用いられる信号です。1 秒間に何回発振されるかがクロック周波数(単位 Hz)、1 回分にかかる時間の長さがクロック周期(単位 秒)で、両者は逆数の関係にあります(確認事項)。",
              tbl(["求めるもの", "計算"],
                  [["クロック周期", "1 ÷ クロック周波数"],
                   ["クロック周波数", "1 ÷ クロック周期"],
                   ["1 命令の実行時間", "クロック周期 × その命令のクロック数"],
                   ["1 秒間の実行回数", "クロック周波数 ÷ 1 命令のクロック数"]],
                  caption="例題52 で使う四つの形", mono=False)
              + note_box("クロック信号の間隔が短い、はクロック周波数が大きい、と同じ意味です(例題51 ⑴ の解説)。"))
          + digest_mod(
              "06", "Prefixes",
              '<path d="M4 18V6M4 6l6 12 6-12 4 12"/>',
              "G(ギガ)や n(ナノ)は、10 の何乗ですか?",
              "10 の 3 乗ごとに変わる",
              "国際単位系(SI)の接頭語です。10 の 3 乗ごとに変化します。情報量は慣例的に 2 の 10 乗(＝1024)ごとに、この接頭語の一部(k は除く)を流用しています(確認事項)。",
              tbl(["大きい量", "k", "M", "G", "T"],
                  [["倍数", "10³", "10⁶", "10⁹", "10¹²"]], caption="大きな量の接頭語", mono=True)
              + tbl(["小さい量", "m", "μ", "n", "p"],
                    [["倍数", "10⁻³", "10⁻⁶", "10⁻⁹", "10⁻¹²"]], caption="小さな量の接頭語", mono=True))
          + '    </div>\n'
          '  </section>\n')
# ============================================================
# 例題50 — コンピュータの動作
# ============================================================
EX50 = stage_example(
    1, 3, "50", "ベストフィット 例題50", "コンピュータの動作", "ex50", SELF_TAG,
    "次の(ア)〜(オ)の動作を、コンピュータ内部で行われる正しい順に並べ替えよ。",
    legend([("ア", "命令レジスタが、主記憶装置から取り出した命令を一時的に保存する。"),
            ("イ", "データレジスタが、データを一時的に保存する。"),
            ("ウ", "命令解読器が、命令を解読して各部を制御する。"),
            ("エ", "プログラムカウンタが、主記憶装置のどの番地の命令を取り出すかを指定する。"),
            ("オ", "演算装置が、加算などの算術演算やそのほかの演算を行う。")], "動作"),
    self_list([
        (None, "(ア)〜(オ)を、コンピュータ内部で行われる正しい順に並べよ。",
         "<p><strong>(エ)→(ア)→(ウ)→(イ)→(オ)</strong></p>"
         + tbl(["段", "動作", "装置"],
               [["取り出し", "(エ) どの番地の命令を取り出すかを指定する", "プログラムカウンタ"],
                ["取り出し", "(ア) 取り出した命令を一時的に保存する", "命令レジスタ"],
                ["解読", "(ウ) 命令を解読して各部を制御する", "命令解読器"],
                ["実行", "(イ) データを一時的に保存する", "データレジスタ"],
                ["実行", "(オ) 算術演算やそのほかの演算を行う", "演算装置"]],
               caption="解説の三つの段")),
    ]),
    feedback("正答: (エ)→(ア)→(ウ)→(イ)→(オ)", [
        fb_section("ベストフィット", bestfit("CPU内部では、プログラムの構成単位である命令の取り出し・解読・実行の一連の動作が順番に行われる。")),
        fb_section("解説(原本)", explain("<p>(エ)→(ア)が「取り出し」、(ウ)が「解読」、(イ)→(オ)が「実行」である。</p>")),
        fb_section("順番の覚え方(補足)", explain(
            "<p>どの番地か決める → その命令を手元に置く → 何をする命令か読む → 使うデータを手元に置く → 計算する、と読むと順序が決まります。"
            "レジスタは「一時的に保存する」役で、命令を置くのが命令レジスタ、データを置くのがデータレジスタです。</p>")),
        viz("FETCH / DECODE / EXECUTE", "三つの段に、五つの動作が割り当たります。",
            checklist([("1", "取り出し", "(エ) 番地を指定 → (ア) 命令を保存"),
                       ("2", "解読", "(ウ) 命令を解読して各部を制御"),
                       ("3", "実行", "(イ) データを保存 → (オ) 演算")])),
    ], example=True))

# ============================================================
# 例題51 — コンピュータの処理速度
# ============================================================
EX51 = stage_example(
    2, 3, "51", "ベストフィット 例題51", "コンピュータの処理速度", "ex51", SELF_TAG,
    "次の⑴〜⑸の記述のうち、適当なものには○を、適当でないものには×を記せ。",
    "",
    self_list([
        ("⑴", "クロック信号の間隔が短いほど命令実行に時間がかかる。",
         "<p><strong>×</strong>　適当でない。「クロック信号の間隔が短い」ということは、クロック周波数が大きいということである。</p>"),
        ("⑵", "クロック信号は、命令実行のタイミングを調整する。",
         "<p><strong>○</strong>　クロック信号は、コンピュータ各回路での処理動作を行うタイミングを合わせるために用いられる。</p>"),
        ("⑶", "同一種類のCPUならば、クロック周波数が大きいほど処理能力が速い。",
         "<p><strong>○</strong>　クロック周波数は 1 秒間に何回のクロック信号が発振されるかを表す。同一種類なら、多いほど速い。</p>"),
        ("⑷", "コンピュータの処理速度は、CPUの処理の速さだけに依存する。",
         "<p><strong>×</strong>　適当でない。コンピュータの処理速度はCPUと主記憶装置間の情報のやり取りの速さやCPUの処理の速さなどが関係する。</p>"),
        ("⑸", "4コア/8スレッドのCPUは、同時に八つの命令を処理することができる。",
         "<p><strong>○</strong>　スレッド数は同時に処理できる命令の最大数を表す。4コア8スレッドなら、処理に余裕があれば最大八つの命令を処理できる。</p>"),
    ]),
    feedback("正答: ⑴ ×　⑵ ○　⑶ ○　⑷ ×　⑸ ○", [
        fb_section("ベストフィット", bestfit("クロック信号の周期の逆数がクロック周波数である。")),
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　適当でない。「クロック信号の間隔が短い」ということは、クロック周波数が大きいということである。</p>"
            "<p><strong>⑷</strong>　適当でない。コンピュータの処理速度はCPUと主記憶装置間の情報のやり取りの速さやCPUの処理の速さなどが関係する。</p>")),
        fb_section("言い換えの表(補足)", explain(
            "<p>「間隔が短い」「周期が短い」「周波数が大きい」は、どれも同じ状態を指します。⑴ は言い換えに気づけば ×、⑷ は「だけ」に気づけば × です。</p>")),
        viz("SPEED — 何が処理速度に効くか", "CPU の中だけでは決まりません。",
            compare2(("CPU の側", [("ビット数", "一度に扱えるデータの情報量"),
                                   ("コア数", "並列して処理できる演算の数"),
                                   ("スレッド数", "同時に処理できる命令の最大数"),
                                   ("クロック周波数", "1 秒間の信号の回数")]),
                     ("CPU の外", [("主記憶装置の性能", "記憶装置そのものの速さ"),
                                   ("両者のやり取り", "CPU と主記憶装置間の情報のやり取りの速さ")]))),
    ], example=True))

# ============================================================
# 例題52 — CPUの処理能力
# ============================================================
EX52 = stage_example(
    3, 3, "52", "ベストフィット 例題52", "CPUの処理能力", "ex52", SELF_TAG,
    "次の問いに答えよ。なお、解答は有効数字2桁で表せ。",
    "",
    self_list([
        ("⑴", "クロック周波数が1.6 GHzのCPUは、4クロックで処理される命令を1秒間に何回実行できるか。",
         "<p><strong>4.0×10<sup>8</sup> 回</strong></p><p>クロック周波数 1.6 GHz＝1.6×10<sup>9</sup> Hz より、1秒間に 1.6×10<sup>9</sup> 回のクロック信号が発生している。よって、4クロックで処理される命令は、1.6×10<sup>9</sup>÷4＝4.0×10<sup>8</sup> 回実行できる。</p>"),
        ("⑵", "クロック周波数が2.0 GHzのCPUのクロック周期は何ns（ナノ秒）か。",
         "<p><strong>0.50 ns</strong></p><p>クロック周期は、クロック周波数の逆数である。クロック周波数 2.0 GHz＝2.0×10<sup>9</sup> Hz より、クロック周期は、1÷2.0×10<sup>9</sup> Hz＝0.50×10<sup>−9</sup> s＝0.50 ns である。</p>"),
        ("⑶", "クロック周波数2.0 GHzのCPUにおいて、ある命令が5クロックで実行できるとき、この命令の実行に必要な時間は何ns（ナノ秒）か。",
         "<p><strong>2.5 ns</strong></p><p>クロック周期は、0.50 nsであるから、0.50×5＝2.5 nsである。</p>"),
        ("⑷", "クロック周期が2.5 ns（ナノ秒）のCPUのクロック周波数は何GHzか。",
         "<p><strong>0.40 GHz</strong></p><p>クロック周波数は、クロック周期の逆数である。クロック周期 2.5 ns＝2.5×10<sup>−9</sup> s より、クロック周波数は、1÷2.5×10<sup>−9</sup> s＝0.40×10<sup>9</sup> Hz＝0.40 GHz である。</p>"),
    ]),
    feedback("正答: ⑴ 4.0×10⁸ 回　⑵ 0.50 ns　⑶ 2.5 ns　⑷ 0.40 GHz", [
        fb_section("ベストフィット", bestfit("クロック周波数とクロック周期は、逆数の関係にある。")),
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　1.6×10<sup>9</sup>÷4＝4.0×10<sup>8</sup> 回。<strong>⑵</strong>　1÷2.0×10<sup>9</sup>＝0.50 ns。"
            "<strong>⑶</strong>　0.50×5＝2.5 ns。<strong>⑷</strong>　1÷2.5×10<sup>−9</sup>＝0.40 GHz。</p>")),
        fb_section("単位のそろえ方(補足)", explain(
            "<p>GHz は 10<sup>9</sup> Hz、ns は 10<sup>−9</sup> s です。先に 10 の累乗へそろえてから割ると、桁を取り違えません。"
            "1 GHz の逆数がちょうど 1 ns になることを覚えておくと、⑵⑷ は暗算で確かめられます。</p>")),
        viz("FOUR FORMS — 四つの形", "周波数と周期は逆数。時間はクロック数をかけ、回数はクロック数で割ります。",
            tbl(["求めるもの", "計算", "この問題での例"],
                [["クロック周期", "1 ÷ 周波数", "1÷2.0×10⁹＝0.50 ns"],
                 ["クロック周波数", "1 ÷ 周期", "1÷2.5×10⁻⁹＝0.40 GHz"],
                 ["1 命令の時間", "周期 × クロック数", "0.50×5＝2.5 ns"],
                 ["1 秒間の回数", "周波数 ÷ クロック数", "1.6×10⁹÷4＝4.0×10⁸ 回"]])),
    ], example=True))

# ============================================================
# 類題88 — コンピュータの動作
# ============================================================
P88 = stage_practice(
    1, 7, "88", "ベストフィット 類題88", "〈コンピュータの動作〉", "p1",
    '<span class="problem-tag match">MATCH</span>',
    "コンピュータを構成する⑴〜⑸の装置の動作内容として最も適当なものを、下の(ア)〜(オ)から一つずつ選べ。",
    legend([("ア", "データを一時的に保存する。"),
            ("イ", "命令を解読して各部を制御する。"),
            ("ウ", "主記憶装置のどの番地の命令を取り出すかを指定する。"),
            ("エ", "加算などの算術演算やそのほかの演算を行う。"),
            ("オ", "主記憶装置から取り出した命令を一時的に保存する。")], "動作内容"),
    match_list("ア,イ,ウ,エ,オ", "2,4,1,0,3",
               [("⑴", "プログラムカウンタ"), ("⑵", "命令レジスタ"), ("⑶", "命令解読器"),
                ("⑷", "データレジスタ"), ("⑸", "演算装置")]),
    feedback("正答: ⑴ (ウ)　⑵ (オ)　⑶ (イ)　⑷ (ア)　⑸ (エ)", [
        fb_section("解説(原本)", explain(
            "<p>命令解読器と演算装置の働きは、名称から推測することができる。残りの装置はレジスタであるが、○○レジスタの名称から「○○を記憶（一時保存）する」と考えれば働きがわかる。</p>"
            "<p><strong>⑴</strong>　プログラムカウンタは、主記憶装置へ転送されている命令のうち、次に実行する番地（アドレス）を記憶している。"
            "<strong>⑵</strong>　命令レジスタは、「命令」を一時的に保存している。"
            "<strong>⑷</strong>　データレジスタは、「データ」を一時的に保存している。</p>")),
        viz("NAME → ROLE", "名前が役割を表しています。",
            tbl(["装置", "名前が指すもの", "動作内容"],
                [["プログラムカウンタ", "番地を数える", "(ウ) どの番地の命令を取り出すか指定"],
                 ["命令レジスタ", "命令を記憶", "(オ) 取り出した命令を一時保存"],
                 ["命令解読器", "命令を解読", "(イ) 解読して各部を制御"],
                 ["データレジスタ", "データを記憶", "(ア) データを一時保存"],
                 ["演算装置", "演算する", "(エ) 算術演算などを行う"]])),
    ]))

# ============================================================
# 類題89 — コンピュータの処理速度
# ============================================================
P89 = stage_practice(
    2, 7, "89", "ベストフィット 類題89", "〈コンピュータの処理速度〉", "p2", SELF_TAG,
    "次の⑴〜⑸の記述のうち、適当なものには○を、適当でないものには×を記せ。",
    "",
    self_list([
        ("⑴", "CPUと主記憶装置間の情報のやり取りの速さは、コンピュータの性能に大きく関係している。",
         "<p><strong>○</strong>　適当である。CPUと主記憶装置間の情報のやり取りが速いほど処理にかかる時間が短くなり、コンピュータの処理速度が速くなる。</p>"),
        ("⑵", "CPUの速さは、コンピュータの性能にある程度関係している。",
         "<p><strong>×</strong>　適当でない。CPUの速さは、コンピュータの性能に大きく関係している。</p>"),
        ("⑶", "同一種類のCPUならば、クロック周波数が大きいほど処理能力が速い。",
         "<p><strong>○</strong>　適当である。クロック周波数が大きいということは、1秒間に発振されるクロック信号の数が多いということである。</p>"),
        ("⑷", "古いCPUでもクロック周波数が大きければ、処理能力が速い。",
         "<p><strong>×</strong>　適当でない。一般的に新しいCPUは、古いCPUより処理能力が速く、古いCPUでクロック周波数が大きくても必ずしも処理能力が上がらない。</p>"),
        ("⑸", "クロック周期は、コンピュータの性能には関係していない。",
         "<p><strong>×</strong>　適当でない。クロック周期は、クロック信号1回分にかかる時間の長さであり、短ければ短いほど処理能力が高い。</p>"),
    ]),
    feedback("正答: ⑴ ○　⑵ ×　⑶ ○　⑷ ×　⑸ ×", [
        fb_section("解説(原本)", explain(
            "<p><strong>⑵</strong>　「ある程度」ではなく「大きく」関係している。<strong>⑷</strong>　古いCPUで周波数が大きくても、必ずしも処理能力が上がるとは限らない。"
            "<strong>⑸</strong>　クロック周期は短いほど処理能力が高いので、関係している。</p>")),
        fb_section("例題51 との違い(補足)", explain(
            "<p>例題51 ⑷ は「CPU だけに依存する」が誤りでした。類題89 ⑵ は逆に「ある程度」と弱めたところが誤りです。"
            "どちらも、程度を表す言葉が正誤を決めています。</p>")),
        viz("DEGREE WORDS — 程度の言葉に線を引く", "記述問題では、程度を表す語が正誤の分かれ目になります。",
            checklist([("1", "だけ", "ほかの要因を否定している → 誤りになりやすい"),
                       ("2", "ある程度", "実際は「大きく」関係する → 誤り"),
                       ("3", "必ずしも", "例外を認める表現。原本の解説がこの形で否定する"),
                       ("4", "関係していない", "短いほど高い、という事実と食い違う")])),
    ]))

# ============================================================
# 類題90 — CPUの処理能力
# ============================================================
P90 = stage_practice(
    3, 7, "90", "ベストフィット 類題90", "〈CPUの処理能力〉", "p3", SELF_TAG,
    "次の問いに答えよ。なお、解答は有効数字2桁で表せ。",
    "",
    self_list([
        ("⑴", "クロック周波数が2.8 GHzのCPUは、4クロックで処理される命令を1秒間に何回実行できるか。ただし、このCPUはシングルコア/シングルスレッドCPUであるとする。",
         "<p><strong>7.0×10<sup>8</sup> 回</strong></p><p>クロック周波数が 2.8 GHz＝2.8×10<sup>9</sup> Hz なので、4クロックで処理される命令は、2.8×10<sup>9</sup>÷4＝0.7×10<sup>9</sup> 回＝7.0×10<sup>8</sup> 回</p>"),
        ("⑵", "クロック周波数が2.5 GHzのCPUのクロック周期は何ns（ナノ秒）か。",
         "<p><strong>0.40 ns</strong></p><p>クロック周波数とクロック周期は、逆数の関係にあるので、1÷(2.5×10<sup>9</sup>)＝0.40×10<sup>−9</sup> s＝0.40 ns</p>"),
        ("⑶", "クロック周波数4.0 GHzのCPUにおいて、ある命令が5クロックで実行できるとき、この命令の実行に必要な時間は何ns（ナノ秒）か。",
         "<p><strong>1.3 ns</strong></p><p>クロック周期は、1÷4.0×10<sup>9</sup>＝0.25×10<sup>−9</sup> s。よって求める時間は、0.25×10<sup>−9</sup> s×5＝1.25×10<sup>−9</sup> s＝1.25 ns≒1.3 ns</p>"),
        ("⑷", "クロック周期が4.0 nsのCPUのクロック周波数は何GHzか。",
         "<p><strong>0.25 GHz</strong></p><p>4.0 ns＝4.0×10<sup>−9</sup> s　1÷4.0×10<sup>−9</sup>＝0.25×10<sup>9</sup> Hz＝0.25 GHz</p>"),
    ]),
    feedback("正答: ⑴ 7.0×10⁸ 回　⑵ 0.40 ns　⑶ 1.3 ns　⑷ 0.25 GHz", [
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　2.8×10<sup>9</sup>÷4＝7.0×10<sup>8</sup> 回。<strong>⑵</strong>　1÷(2.5×10<sup>9</sup>)＝0.40 ns。"
            "<strong>⑶</strong>　クロック周期 0.25 ns×5＝1.25 ns≒1.3 ns。<strong>⑷</strong>　1÷4.0×10<sup>−9</sup>＝0.25 GHz。</p>")),
        fb_section("有効数字の扱い(補足)", explain(
            "<p>⑶ は 1.25 ns がそのままの値で、有効数字 2 桁にすると 1.3 ns です。問題文の「有効数字2桁で表せ」を最後に当てます。"
            "途中で丸めると、⑶ のように 3 桁目が出る問題でずれます。</p>")),
    ]))

# ============================================================
# 練習91 — コンピュータの動作（仮想コンピュータ）
# ============================================================
P91 = stage_practice(
    4, 7, "91", "ベストフィット 練習91", "〈コンピュータの動作〉", "p4", SELF_TAG,
    "ある仮想コンピュータについて、次の問いに答えよ。なお、主記憶装置には右の図のような命令が1〜5番地に、データが10〜11番地にそれぞれ保存されているものとする。",
    figure("assets/fig1-virtual-computer.jpeg",
           "仮想コンピュータの命令一覧（READ メモリからレジスタに読み出し／WRITE レジスタからメモリに書き込み／ADD レジスタ間の和／STOP プログラムの停止）と、主記憶装置の内容。1番地 READ A,(10)、2番地 READ B,(11)、3番地 ADD A,B、4番地 WRITE (12),A、5番地 STOP、10番地 3、11番地 5、12番地 空",
           "仮想コンピュータの命令と主記憶装置（原本の図）", 460, 420),
    self_list([
        ("⑴", "プログラムカウンタが「2」のとき、命令レジスタに取り出される命令は何か答えよ。",
         "<p><strong>READ B,(11)</strong></p><p>プログラムカウンタが「2」であるから、保存されている2番地の命令が取り出される。</p>"),
        ("⑵", "プログラムカウンタが「3」のとき、命令が実行されるとデータレジスタAの内容は実行前と実行後ではどのように変化するか答えよ。",
         "<p><strong>3から8へ変化する</strong></p><p>実行前には1番地のREAD A,(10)の命令により、10番地から読み込まれた「3」がレジスタAに保存されている。また、2番地のREAD B,(11)の命令により、11番地から読み込まれた「5」がレジスタBに保存されている。実行後には命令がADD A,Bであるから、レジスタAのデータとレジスタBのデータを加算し、レジスタAのデータは「8」となる。</p>"),
        ("⑶", "プログラムが実行された結果、12番地に保存されるデータは何か答えよ。",
         "<p><strong>8</strong></p><p>プログラムが実行されると、レジスタAのデータ「8」が12番地に保存される。</p>"),
        ("⑷", "このプログラムは、何を計算したものか答えよ。",
         "<p><strong>3と5の加算を計算したもの</strong></p>"),
        ("⑸", "3番地に保存されている命令を「ADD B,A」と書き換えると、プログラムを実行した結果は変わってしまう。書き換え前と同じ結果を得るためには、何番地の命令をどのように書き換えればよいか答えよ。ただし、3番地の命令は元に戻してはいけない。",
         "<p><strong>4番地の命令をWRITE(12),Bに書き換える。</strong></p><p>3番地に保存されている命令を「ADD B,A」と書き換えると、レジスタAのデータとレジスタBのデータを加算し、レジスタBへ書き込むことになる。その結果、レジスタAには「3」、レジスタBには「8」が保存されており、WRITE (12),Aの命令で12番地に書き込まれるデータは、「3」となる。</p>"),
    ]),
    feedback("正答: ⑴ READ B,(11)　⑵ 3から8へ変化する　⑶ 8　⑷ 3と5の加算　⑸ 4番地を WRITE(12),B に", [
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　プログラムカウンタが「2」であるから、保存されている2番地の命令が取り出される。</p>"
            "<p><strong>⑸</strong>　「ADD B,A」に書き換えると結果はレジスタBへ書き込まれる。レジスタAには「3」が残るので、WRITE (12),A のままでは12番地に「3」が書き込まれてしまう。</p>")),
        fb_section("表にして追う(補足)", explain(
            "<p>命令を1行ずつ、レジスタA・レジスタB・12番地の値を書き出すと、どこで値が変わるかが見えます。"
            "加算命令は、結果を<strong>左に書いたレジスタ</strong>に入れます。ADD A,B なら A、ADD B,A なら B です。</p>")
            + tbl(["番地", "命令", "レジスタA", "レジスタB", "12番地"],
                  [["1", "READ A,(10)", "3", "—", "空"],
                   ["2", "READ B,(11)", "3", "5", "空"],
                   ["3", "ADD A,B", "8", "5", "空"],
                   ["4", "WRITE (12),A", "8", "5", "8"],
                   ["5", "STOP", "8", "5", "8"]],
                  caption="書き換える前のトレース", mono=True)
            + tbl(["番地", "命令", "レジスタA", "レジスタB", "12番地"],
                  [["1", "READ A,(10)", "3", "—", "空"],
                   ["2", "READ B,(11)", "3", "5", "空"],
                   ["3", "ADD B,A", "3", "8", "空"],
                   ["4", "WRITE (12),B", "3", "8", "8"],
                   ["5", "STOP", "3", "8", "8"]],
                  caption="⑸ の書き換え後のトレース", mono=True)),
    ]))

# ============================================================
# 練習92〜94 — CPUの処理能力
# ============================================================
P92 = stage_practice(
    5, 7, "92", "ベストフィット 練習92", "〈CPUの処理能力〉", "p5", SELF_TAG,
    "あるプログラムは、命令A〜Dを下に示す順に実行する。各命令の実行に必要なクロック数が下の表の通りであるとすると、クロック周波数1 GHzのCPUで、この命令列を実行するのに必要な時間は何ns（ナノ秒）か答えよ。ただし、このCPUはシングルコア/シングルスレッドCPUであるとする。",
    '<p class="problem-q" style="margin-top:0.6rem;">命令の実行順　A→B→C→A→C→D</p>'
    + tbl(["命令", "A", "B", "C", "D"], [["クロック数", "2", "6", "1", "8"]], mono=True),
    self_list([
        (None, "この命令列を実行するのに必要な時間は何 ns か。",
         "<p><strong>20 ns</strong></p><p>クロック信号1回分にかかる時間の長さ（クロック周期）を求め、その時間にプログラム全体に必要なクロック数をかければ求める時間を計算できる。"
         "クロック周期＝1÷1 GHz＝1÷1×10<sup>9</sup> Hz＝1×10<sup>−9</sup> s＝1 ns。"
         "このプログラム全体で必要なクロック数は、2＋6＋1＋2＋1＋8＝20 である。よって必要な時間は、1×20＝20 ns である。</p>"),
    ]),
    feedback("正答: 20 ns", [
        fb_section("解説(原本)", explain(
            "<p>クロック周期は 1 ns。命令列 A→B→C→A→C→D のクロック数は 2＋6＋1＋2＋1＋8＝20。よって 1×20＝20 ns。</p>")),
        fb_section("A が二度出ることに注意(補足)", explain(
            "<p>表の 4 つを足すのではなく、<strong>実行順に並んだ 6 つ</strong>を足します。A と C が二度ずつ出るので、2＋6＋1＋2＋1＋8 です。</p>")),
    ]))

# 原本（ベストフィット 3章 解答）の式は「5×60＋10×40÷100＝7」で括弧が落ちている。
# そのまま読むと 10×40÷100 だけが先に計算されて 304 になるため、括弧を補って掲載する。
P93 = stage_practice(
    6, 7, "93", "ベストフィット 練習93", "〈CPUの処理能力〉", "p6", SELF_TAG,
    "クロック周波数が1.4 GHzのCPUがある。このCPUの命令種が、下の表に示す二つから構成されているとき、1秒間に実行可能な命令数は何回か答えよ。ただし、このCPUはシングルコア/シングルスレッドCPUであるとする。",
    tbl(["命令種", "クロック数", "実行頻度（％）"], [["命令A", "5", "60"], ["命令B", "10", "40"]], mono=True),
    self_list([
        (None, "1秒間に実行可能な命令数は何回か。",
         "<p><strong>2億回（2×10<sup>8</sup> 回）</strong></p><p>命令種の実行頻度から平均のクロック数を計算し、1秒間に発信されるクロック信号の回数（クロック周波数）を割れば求める回数を得られる。"
         "平均のクロック数は、(5×60＋10×40)÷100＝7。よって1秒間に実行可能な命令数は、1.4 GHz÷7＝1.4×10<sup>9</sup> Hz÷7＝0.2×10<sup>9</sup>＝2×10<sup>8</sup> である。</p>"),
    ]),
    feedback("正答: 2億回（2×10⁸ 回）", [
        fb_section("解説(原本)", explain(
            "<p>平均のクロック数は (5×60＋10×40)÷100＝7。1.4×10<sup>9</sup>÷7＝2×10<sup>8</sup> 回。</p>")),
        fb_section("平均クロック数の出し方(補足)", explain(
            "<p>頻度は % なので、100 で割って重みにします。(5×0.6)＋(10×0.4)＝3＋4＝7 と計算しても同じです。"
            "この 7 が「1 命令あたり平均 7 クロック」で、周波数をこれで割ると 1 秒間の命令数になります。</p>")),
    ]))

P94 = stage_practice(
    7, 7, "94", "ベストフィット 練習94", "〈CPUの処理能力〉", "p7", SELF_TAG,
    "ある命令種の速度が5倍速くなるようにコンピュータの機能を改善した。機能改善の前では、コンピュータの性能を数値化して評価する指標である「ベンチマーク」の実行時間が10秒であったが、機能改善後の速度向上比はどうなるか。ただし、この「ベンチマーク」の10秒の半分がこの命令種の実行に費やされていたとし、速度向上比は「改善前のベンチマーク値÷改善後のベンチマーク値」で求めるものとする。また、計算結果は小数第2位を四捨五入して求めよ。",
    "",
    self_list([
        (None, "機能改善後の速度向上比はどうなるか。",
         "<p><strong>1.7</strong></p><p>ベンチマークの半分がこの命令種に費やされているのだから、この命令を使用する部分の改善前の実行時間は5秒である。よって、5倍速くなるように改善したのだから、この命令を使用する部分の改善後の実行時間は、5÷5＝1 s。"
         "それ以外の実行時間は、5秒で変化がないのだから、全体では、1＋5＝6 s。よって、速度向上比は、10÷6＝1.66…≒1.7 となる。</p>"),
    ]),
    feedback("正答: 1.7", [
        fb_section("解説(原本)", explain(
            "<p>改善される部分は 5 秒 → 1 秒。残りの 5 秒は変わらないので全体は 6 秒。10÷6＝1.66…≒1.7。</p>")),
        fb_section("全体が 5 倍にならない理由(補足)", explain(
            "<p>速くなるのは<strong>半分だけ</strong>です。残りの半分は元のままなので、全体の時間は 1/5 にはなりません。"
            "改善しない部分が残るかぎり、全体の向上比はその部分で頭打ちになります。</p>")),
    ]))

RESULT = """  <section class="stage" data-stage-name="RESULT">
    <div class="section-divider">
      <span class="num">02</span>
      <div class="text">
        <div class="label">Section 2 — Result</div>
        <div class="name">演習結果</div>
      </div>
    </div>
    <div class="summary-hero">
      <div class="summary-grade" id="summary-grade">—<span class="denom">/7</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">7問の練習問題のうち、何問完答できたかを示します。</div>
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

STAGES = (WELCOME + REVIEW + EX50 + EX51 + EX52
          + P88 + P89 + P90 + P91 + P92 + P93 + P94 + RESULT)

TIMELINE = """  const TIMELINE_ENTRIES = [
    { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
    { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2,  group: 'examples', num: '例50', label: 'コンピュータの動作', probId: 'ex50' },
    { idx: 3,  group: 'examples', num: '例51', label: 'コンピュータの処理速度', probId: 'ex51' },
    { idx: 4,  group: 'examples', num: '例52', label: 'CPUの処理能力', probId: 'ex52' },
    { idx: 5,  group: 'practice', num: 'Q88', label: '〈コンピュータの動作〉', probId: 'p1' },
    { idx: 6,  group: 'practice', num: 'Q89', label: '〈コンピュータの処理速度〉', probId: 'p2' },
    { idx: 7,  group: 'practice', num: 'Q90', label: '〈CPUの処理能力〉', probId: 'p3' },
    { idx: 8,  group: 'practice', num: 'Q91', label: '〈コンピュータの動作〉', probId: 'p4' },
    { idx: 9,  group: 'practice', num: 'Q92', label: '〈CPUの処理能力〉', probId: 'p5' },
    { idx: 10, group: 'practice', num: 'Q93', label: '〈CPUの処理能力〉', probId: 'p6' },
    { idx: 11, group: 'practice', num: 'Q94', label: '〈CPUの処理能力〉', probId: 'p7' },
    { idx: 12, group: 'result',   num: '✓',   label: '結果サマリ' }
  ];"""

PROBLEMS = """  const PROBLEMS = [
    { id: 'p1', label: 'Q88', name: '〈コンピュータの動作〉', stageIdx: 5 },
    { id: 'p2', label: 'Q89', name: '〈コンピュータの処理速度〉', stageIdx: 6 },
    { id: 'p3', label: 'Q90', name: '〈CPUの処理能力〉', stageIdx: 7 },
    { id: 'p4', label: 'Q91', name: '〈コンピュータの動作〉', stageIdx: 8 },
    { id: 'p5', label: 'Q92', name: '〈CPUの処理能力〉', stageIdx: 9 },
    { id: 'p6', label: 'Q93', name: '〈CPUの処理能力〉', stageIdx: 10 },
    { id: 'p7', label: 'Q94', name: '〈CPUの処理能力〉', stageIdx: 11 }
  ];"""


# ============================================================
# 独立検算(原本の解答を計算で確かめる)
# ============================================================
def selfcheck():
    from decimal import Decimal, ROUND_HALF_UP
    import math

    def sig2(x):
        # 有効数字 2 桁の四捨五入（原本の「小数第2位を四捨五入」等に合わせる。
        # python の %g は偶数丸めなので 1.25 → 1.2 になり、原本の 1.3 と食い違う）
        if x == 0:
            return 0.0
        e = math.floor(math.log10(abs(x)))
        q = Decimal(10) ** (e - 1)
        return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))
    # 例題52
    assert sig2(1.6e9 / 4) == 4.0e8
    assert sig2(1 / 2.0e9 * 1e9) == 0.50
    assert sig2(1 / 2.0e9 * 5 * 1e9) == 2.5
    assert sig2(1 / 2.5e-9 / 1e9) == 0.40
    # 類題90
    assert sig2(2.8e9 / 4) == 7.0e8
    assert sig2(1 / 2.5e9 * 1e9) == 0.40
    assert round(1 / 4.0e9 * 5 * 1e9, 2) == 1.25 and sig2(1 / 4.0e9 * 5 * 1e9) == 1.3
    assert sig2(1 / 4.0e-9 / 1e9) == 0.25
    # 練習92: 実行順 A B C A C D
    clocks = {"A": 2, "B": 6, "C": 1, "D": 8}
    total = sum(clocks[c] for c in ["A", "B", "C", "A", "C", "D"])
    assert total == 20 and (1 / 1e9 * 1e9) * total == 20
    # 練習93: 平均クロック数と 1 秒間の命令数
    avg = (5 * 60 + 10 * 40) / 100
    assert avg == 7 and 1.4e9 / avg == 2e8
    # 練習94: 半分が 5 倍速くなる
    after = 5 / 5 + 5
    assert after == 6 and round(10 / after, 1) == 1.7
    # 練習91: 仮想機械
    def run(code, mem):
        mem = dict(mem); reg = {}
        for op in code:
            t = op[0]
            if t == "READ":   reg[op[1]] = mem[op[2]]
            elif t == "WRITE": mem[op[1]] = reg[op[2]]
            elif t == "ADD":   reg[op[1]] = reg[op[1]] + reg[op[2]]
        return mem, reg
    M = {10: 3, 11: 5, 12: None}
    orig = [("READ", "A", 10), ("READ", "B", 11), ("ADD", "A", "B"), ("WRITE", 12, "A")]
    mem, reg = run(orig, M)
    assert reg["A"] == 8 and mem[12] == 8
    swapped_nofix = [("READ", "A", 10), ("READ", "B", 11), ("ADD", "B", "A"), ("WRITE", 12, "A")]
    assert run(swapped_nofix, M)[0][12] == 3
    swapped_fix = [("READ", "A", 10), ("READ", "B", 11), ("ADD", "B", "A"), ("WRITE", 12, "B")]
    assert run(swapped_fix, M)[0][12] == 8


def main():
    selfcheck()
    html = SRC.read_text(encoding="utf-8")

    def sub1(pattern, repl, text, flags=0, label=""):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        assert n == 1, "置換に失敗: %s" % (label or pattern)
        return new

    html = sub1(r"<title>.*?</title>",
                "<title>コンピュータの構成と動作 | Practice Lab</title>", html, 0, "title")
    html = sub1(r'<span class="tg">CHAPTER 2\.06</span>',
                '<span class="tg">CHAPTER 3.10</span>', html, 0, "chapter tag")
    html = sub1(r'<span class="sb-score" id="sb-score">—/6</span>',
                '<span class="sb-score" id="sb-score">—/7</span>', html, 0, "sb-score")

    html = sub1(r'(<main id="stages">\n).*?(\n</main>)',
                lambda m: m.group(1) + STAGES.rstrip("\n") + m.group(2),
                html, re.S, "stages")

    html = sub1(r"  const TIMELINE_ENTRIES = \[.*?\n  \];",
                lambda m: TIMELINE, html, re.S, "TIMELINE_ENTRIES")
    html = sub1(r"  const PROBLEMS = \[.*?\n  \];",
                lambda m: PROBLEMS, html, re.S, "PROBLEMS")

    html = sub1(r"sbScore\.textContent = full \+ '/14';",
                "sbScore.textContent = full + '/7';", html, 0, "sb score denom")
    html = sub1(r"animateCounter\(grade, 0, fullCount, 1100, '<span class=\"denom\">/14</span>'\);",
                "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/7</span>');",
                html, 0, "grade denom")
    html = sub1(r"if \(fullCount >= 11\) grade\.classList\.add\('s-high'\);\n"
                r"    else if \(fullCount >= 7\) grade\.classList\.add\('s-mid'\);",
                "if (fullCount >= 6) grade.classList.add('s-high');\n"
                "    else if (fullCount >= 4) grade.classList.add('s-mid');",
                html, 0, "thresholds")

    # 原本の全角カンマは、キット慣例の「、」に
    assert "，" not in STAGES, "全角カンマが残っている"
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT, len(html), "bytes")


if __name__ == "__main__":
    main()
