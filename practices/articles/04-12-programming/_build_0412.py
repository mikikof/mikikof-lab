#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""practices 04-12「プログラミング」ビルダ

- エンジン(CSS / JS ハーネス / サイドバー / トップバー / フッタ)は
  examples/02-07-digital-info-representation.html を 1 文字も変えずに流用する(03-10 と同じ)。
- 差し替えるのは <main id="stages"> の中身と、JS の TIMELINE_ENTRIES / PROBLEMS /
  サマリ分母・閾値 だけ。
- 問題文・選択肢・解答・原本解説は _source の docx から逐語(「，」→「、」のみ)。
- 原本の図 5 枚は assets/ に抽出済み(順次・分岐・反復の 3 構造、変数、類題99 のフローチャート)。
- 収録範囲は原本どおり全部: 例題55〜59・類題99〜104・練習105〜106 の 13 問。
  関数(例題59・類題104)はベストフィットでは 12 節に入っているので外さない。
- ★ 用語: ベストフィットは range の 2 番目の数を「終了値」と呼ぶ。ここは原本の文を
  そのまま載せる場所なので、原文どおり残す(lectures 側の用語の線とは別扱い)。
- 解答の値はすべて実行して独立に検算してから書いた(末尾 selfcheck)。
"""
import re
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PRACTICES = HERE.parent.parent
SRC = PRACTICES / "skills/interactive-practice/examples/02-07-digital-info-representation.html"
OUT = HERE / "index.html"

NB = "&nbsp;"
IND = NB * 4


# ============================================================
# 共通パーツ(03-10 と同じ流儀)
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
    return ('<div style="display:flex; flex-wrap:wrap; gap:0.6rem; justify-content:center; align-items:flex-start;">\n%s</div>\n'
            % "".join(figs))


def legend(items, title="選択肢"):
    rows = "".join(
        '      <span class="option-legend-item"><span class="let">(%s)</span>%s</span>\n' % (l, t)
        for l, t in items
    )
    return ('<div class="option-legend">\n'
            '  <div class="option-legend-title">%s</div>\n'
            '  <div class="option-legend-list">\n%s'
            '  </div>\n'
            '</div>\n' % (title, rows))


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
        rows += ('  <div class="match-row" data-sub="%d">\n'
                 '    <span class="match-sub-label">%s</span>\n'
                 '    <div class="sub-content">\n'
                 '      <span class="match-text">%s</span>\n'
                 '      <div class="match-pills"></div>\n'
                 '    </div>\n'
                 '  </div>\n' % (i, lbl, text))
    return ('<div class="match-list" data-input="match" data-options="%s" data-correct="%s">\n%s</div>\n'
            % (options, correct, rows))


def self_list(items):
    """items: [(label or None, question, model_html)]"""
    rows = ""
    for i, (lbl, q, model) in enumerate(items):
        sub = '<span class="self-sub-label">%s</span>' % lbl if lbl else ""
        rows += ('  <div class="self-row" data-sub="%d">\n'
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
                 '  </div>\n' % (i, sub, q, model))
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
        return '    <div class="compare-col %s">\n      <h5>%s</h5>\n%s    </div>\n' % (side, head, rr)
    return '  <div class="compare">\n%s%s  </div>\n' % (col("left", left[0], left[1]), col("right", right[0], right[1]))


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


def tbl(head, rows, caption=None, mono=False, small=False, lft=()):
    fs = "0.82rem" if small else "0.9rem"
    ff = "var(--f-mono)" if mono else "var(--f-jp-body)"
    th = "".join('<th style="padding:0.35rem 0.55rem; border:1px solid var(--line-strong); background:var(--action-pale); '
                 'color:var(--anchor); font-weight:700; white-space:nowrap;">%s</th>' % h for h in head)
    trs = ""
    for r in rows:
        tds = ""
        for i, c in enumerate(r):
            align = "left" if i in lft else "center"
            wrap = "normal" if i in lft else "nowrap"
            tds += ('<td style="padding:0.35rem 0.55rem; border:1px solid var(--line); text-align:%s; '
                    'white-space:%s;">%s</td>' % (align, wrap, c))
        trs += "      <tr>%s</tr>\n" % tds
    cap = ('<div style="margin-top:0.4rem; font-family: var(--f-mono); font-size:0.74rem; color: var(--ink-mute);">%s</div>\n'
           % caption) if caption else ""
    return ('<div style="overflow-x:auto; -webkit-overflow-scrolling:touch; margin:0.6rem 0 0.4rem;">\n'
            '  <table style="border-collapse:collapse; margin:0 auto; font-family:%s; font-size:%s; color:var(--ink); background:#fff;">\n'
            '    <thead><tr>%s</tr></thead>\n'
            '    <tbody>\n%s    </tbody>\n'
            '  </table>\n%s</div>\n' % (ff, fs, th, trs, cap))


def pyprog(lines, cap=None, tag=None):
    """原本のプログラム(行番号つき)。lines: [(行番号, コード html)]"""
    rows = "".join(
        '<tr><td style="padding:0.18rem 0.7rem 0.18rem 0.5rem; text-align:right; color:var(--ink-faint); '
        'border-right:1px solid var(--line); user-select:none; white-space:nowrap;">%s</td>'
        '<td style="padding:0.18rem 0.9rem; white-space:pre; color:var(--ink);">%s</td></tr>' % (n, c)
        for n, c in lines)
    head = ('<div style="font-family:var(--f-mono); font-size:0.7rem; letter-spacing:0.1em; color:var(--action-deep); '
            'font-weight:700; margin-bottom:0.3rem;">%s</div>' % tag) if tag else ""
    capd = ('<div style="margin-top:0.4rem; font-family:var(--f-mono); font-size:0.74rem; color:var(--ink-mute); '
            'text-align:center;">%s</div>' % cap) if cap else ""
    return ('<div style="margin:0.7rem 0 0.3rem;">%s'
            '<div style="overflow-x:auto; -webkit-overflow-scrolling:touch;">'
            '<table style="border-collapse:collapse; margin:0 auto; background:#fff; border:1px solid var(--line); '
            'border-radius:8px; font-family:var(--f-mono); font-size:0.88rem; line-height:1.85; font-weight:500;">'
            '<tbody>%s</tbody></table></div>%s</div>\n' % (head, rows, capd))


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
        '%s%s'
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
        '%s%s'
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
    return ('    <div class="%s">\n'
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
            '    </div>\n' % (cls, num, ico, en, question, title, lede, indent(body, 8)))


SELF_TAG = '<span class="problem-tag self">記述・自己採点</span>'
SINGLE_TAG = '<span class="problem-tag">SINGLE</span>'
MATCH_TAG = '<span class="problem-tag match">MATCH</span>'


# ============================================================
# STAGE 0 — WELCOME
# ============================================================
WELCOME = """  <section class="stage active" data-stage-name="START">
    <div class="welcome-kicker">
      <span class="num">04</span>
      <span>4章 第12節</span>
    </div>
    <h1 class="welcome-title-en">Programming<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">プログラミング</h2>
    <p class="welcome-lede">
      順次・分岐・反復の三つの基本構造から始めます。割り算の余りで分岐を決める書き方、繰り返しの対象範囲をインデントで読み取る力、配列の添字の始まり、そして処理のまとまりを関数として独立させる考え方まで、一続きで確かめます。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">examples</div>
        <div class="welcome-meta-value">5<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">8<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">55<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">4章12</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー この節の基本知識を、Q&amp;A形式の6モジュールで確認します(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>例題ツアー</strong>ー 例題55〜59の解き方を5問たどります(採点なし。答えは模範解答と照らします)</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>演習</strong>ー 類題99〜104・練習105〜106の計8問。回答 → 採点 → 解説</div></div>
        <div class="flow-item"><span class="flow-num">4</span><div><strong>結果</strong>ー 完答数と、間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>
"""

# ============================================================
# STAGE 1 — REVIEW(Q&A 6 モジュール)
# ============================================================
FAMILY_TREE = """<div class="viz">
  <span class="viz-label">THE BIG MAP — この節で扱う四つの内容</span>
  <div class="viz-caption">三つの基本構造を土台に、分岐・繰り返し・配列・関数の順に積み上がります。</div>
  <div class="family-tree-wrap">
    <svg class="family-tree-svg" viewBox="0 0 760 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="プログラミングの地図。三つの基本構造(順次・分岐・反復)を土台に、選択構造、繰り返し構造、配列(一次元・二次元)、関数(引数・戻り値)の四つに分かれる">
      <rect x="4" y="152" width="118" height="52" rx="12" fill="#122E55"/>
      <text x="63" y="174" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">プログラ</text>
      <text x="63" y="192" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">ミング</text>
      <line x1="122" y1="178" x2="140" y2="178" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="46" x2="140" y2="310" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="46" x2="156" y2="46" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="134" x2="156" y2="134" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="222" x2="156" y2="222" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="140" y1="310" x2="156" y2="310" stroke="#B8C5D7" stroke-width="1.5"/>

      <rect x="156" y="24" width="128" height="44" rx="10" fill="#4A78C8"/>
      <text x="220" y="52" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">選択構造</text>
      <line x1="284" y1="46" x2="304" y2="46" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="31" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="435" y="51" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">if / elif / else ・ 割り算の余り ・ 入れ子</text>
      <text x="580" y="51" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題55 / 類題99・100</text>

      <rect x="156" y="112" width="128" height="44" rx="10" fill="#2A4A78"/>
      <text x="220" y="140" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">繰り返し構造</text>
      <line x1="284" y1="134" x2="304" y2="134" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="119" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="435" y="139" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">for / while ・ range ・ 対象範囲はインデント</text>
      <text x="580" y="139" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題56 / 類題101 / 練習105</text>

      <rect x="156" y="200" width="128" height="44" rx="10" fill="#2E826F"/>
      <text x="220" y="228" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">配列</text>
      <line x1="284" y1="222" x2="304" y2="222" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="207" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#2E826F" stroke-width="1.5"/>
      <text x="435" y="227" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">一次元 ・ 二次元 ・ 添字の始まり ・ 最大最小</text>
      <text x="580" y="227" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題57・58 / 類題102・103</text>

      <rect x="156" y="288" width="128" height="44" rx="10" fill="#B85975"/>
      <text x="220" y="316" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">関数</text>
      <line x1="284" y1="310" x2="304" y2="310" stroke="#B8C5D7" stroke-width="1.5"/>
      <rect x="304" y="295" width="262" height="30" rx="8" fill="#FAFCFF" stroke="#B85975" stroke-width="1.5"/>
      <text x="435" y="315" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12.5" font-weight="500" fill="#1A2B47">定義と呼び出し ・ 引数 ・ 戻り値</text>
      <text x="580" y="315" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11.5" fill="#75839B">例題59 / 類題104</text>
    </svg>
  </div>
</div>
"""

REVIEW_MODS = [
    digest_mod(
        "01", "The Big Map",
        '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><line x1="7" y1="11" x2="17" y2="7"/><line x1="7" y1="13" x2="17" y2="17"/>',
        "この節では、何を順に扱いますか?",
        "選択構造 → 繰り返し構造 → 配列 → 関数",
        "はじめに条件で処理を分ける選択構造、次に同じ処理を繰り返す反復構造を確かめます。続いて複数の値を一つの名前で扱う配列、最後に処理のまとまりを独立させる関数へ進みます。",
        FAMILY_TREE, hero=True),

    digest_mod(
        "02", "Three Structures",
        '<rect x="4" y="4" width="16" height="4" rx="1"/><rect x="4" y="10" width="16" height="4" rx="1"/><rect x="4" y="16" width="16" height="4" rx="1"/>',
        "プログラムの基本構造は、いくつありますか?",
        "順次構造・分岐構造・反復構造の三つ",
        "中学までの復習にあたる部分です。書かれた順に処理を行う順次構造、条件を満たすかどうかで処理を分ける分岐構造、同じ処理を繰り返す反復構造。この三つの組み合わせでプログラムは記述できます。",
        viz("BASIC STRUCTURES — 三つの基本構造",
            "原本の図をそのまま示します。左から順次、分岐、反復です。",
            fig_row([
                figure("assets/fig1-junji-flowchart.jpeg", "順次構造のフローチャート。処理 A、処理 B、処理 C が上から順に並ぶ",
                       "順次構造 — 書かれた順に処理を行う", 220, 180),
                figure("assets/fig2-bunki-flowchart.jpeg", "分岐構造のフローチャート。条件式が Yes なら処理 A、No なら処理 B",
                       "分岐構造（選択構造） — 条件で分ける", 250, 210),
                figure("assets/fig3-hanpuku-flowchart.jpeg", "反復構造のフローチャート。ループ条件式の下に処理 A と処理 B があり、ループで閉じる",
                       "反復構造（繰り返し構造） — 同じ処理を繰り返す", 220, 175),
            ])
            + note_box("プログラム中で使用する値は、<strong>変数</strong>として扱うことが多くあります。"
                       "変数である数値や文字列などの値に付けられた名前を<strong>変数名</strong>、"
                       "変数に値を割り当てることを<strong>代入</strong>といいます。")
            + figure("assets/fig4-hensu.jpeg",
                     "変数の図。変数名 ninzu の箱に値 42、変数名 namae の箱に値 'satou' が入っている",
                     "変数名と値（原本の図）", 420, 380))),

    digest_mod(
        "03", "if / elif / else",
        '<path d="M12 3v6"/><path d="M12 9l-6 6"/><path d="M12 9l6 6"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="18" r="2.2"/>',
        "三つ以上に分けたいときは、どう書きますか?",
        "elif を使う。条件は上から順に確かめられる",
        "確認事項の表のとおりです。条件式 X が真なら処理 A、そうでなくもし条件式 Y が真なら処理 B、そうでなければ処理 C。elif と else で始まるブロックは、分岐がなければ省略できます。",
        viz("SELECTION — 選択構造【Python】",
            "上から順に確かめ、最初に真になったところだけが実行されます。",
            tbl(["記述方法", "内容"],
                [["if&nbsp;&nbsp;条件式X：<br>&nbsp;&nbsp;&nbsp;&nbsp;処理A<br>elif&nbsp;&nbsp;条件式Y：<br>&nbsp;&nbsp;&nbsp;&nbsp;処理B<br>else：<br>&nbsp;&nbsp;&nbsp;&nbsp;処理C",
                  "・もし条件式Xが真の場合、処理Aを実行する。<br>・そうでなくもし条件式Yが真ならば、処理Bを実行する。<br>・そうでなければ、処理Cを実行する。<br>※elifとelseで始まるブロックは分岐がなければ省略可。"]],
                lft=(0, 1))
            + note_box("「割り切れる」「倍数」の判断は、<strong>割り算の余り</strong>で行います。"
                       "Python では a ÷ b の商（整数部分）は <strong>a // b</strong>、余りは <strong>a % b</strong> で表します。"))),

    digest_mod(
        "04", "for / while",
        '<path d="M4 10a8 8 0 1 1 0 4"/><path d="M4 6v4h4"/>',
        "繰り返しの「対象範囲」は、どこで決まりますか?",
        "インデント（字下げ）で決まる",
        "確認事項の表では、for は指定された回数（範囲）分だけ処理 A を実行し、while は条件式が真の間だけ処理 A を実行します。どこまでが繰り返しの対象かは、インデントから読み取ります。",
        viz("ITERATION — 繰り返し構造【Python】",
            "for は回数や範囲で、while は条件で終わりが決まります。",
            tbl(["記述方法", "内容"],
                [["for&nbsp;&nbsp;繰り返し回数（範囲）の指定：<br>&nbsp;&nbsp;&nbsp;&nbsp;処理A",
                  "指定された回数（範囲）分、処理Aを実行する。<br>指定文には、変数の変化も指定する。"],
                 ["while&nbsp;&nbsp;条件式：<br>&nbsp;&nbsp;&nbsp;&nbsp;処理A",
                  "条件式が真の間、処理Aを実行する。<br>while True:とすると、無限に繰り返す。"]],
                lft=(0, 1))
            + bd_grid([
                ("range(5)", "0 から 5 未満", "0、1、2、3、4 の 5 個。開始値を省くと 0 から。"),
                ("range(1, x + 1)", "1 から x まで", "増分値を省くと 1 ずつ。終了値の x+1 は含まない。"),
                ("range(1, x + 1, 1)", "開始値・終了値・増分値", "三つの引数をすべて書いた形。"),
            ])
            + note_box("原本の解説の言い方に合わせています。range() には<strong>開始値・終了値・増分値</strong>の三つの引数があり、"
                       "<strong>終了値そのものは含まれません</strong>。増分値を省略すると 1、開始値を省略すると 0 になります。"))),

    digest_mod(
        "05", "Arrays",
        '<rect x="2" y="9" width="5.5" height="6" rx="1"/><rect x="9.2" y="9" width="5.5" height="6" rx="1"/><rect x="16.4" y="9" width="5.5" height="6" rx="1"/>',
        "配列の添字は、いくつから始まりますか?",
        "特に説明がなければ 0 から。問題文の指定が優先",
        "確認事項では、配列は複数の変数を一列にまとめたもので、一つの名前で扱えるものとされています。配列全体を指す配列名と、格納された一つひとつの値を指し示す番号の添字があり、角括弧で各要素を表します。",
        viz("ARRAY — 一次元と二次元",
            "添字が一つなら一次元、二つなら二次元です。",
            compare2(("一次元配列", [("表し方", "kion[3] のように、添字は一つ"),
                                     ("中身", "複数の変数を一列にまとめたもの"),
                                     ("別の呼び名", "「リスト」と呼ぶプログラミング言語もある")]),
                     ("二次元配列", [("表し方", "tokuten[5][40] のように、添字は二つ"),
                                     ("中身", "配列の中に配列があるような構造"),
                                     ("イメージ", "縦横に値が並んでいる")]))
            + note_box("大学入試センターの共通テスト用プログラム表記の例示では、<strong>特に説明がない場合、"
                       "配列の要素を指定する添字は 0 から始まる</strong>と明記されています。ただし問題文中に"
                       "「添字は 1 から始まる」と書かれていることもあるので、問題文をよく読み、下線を引いておくとよいでしょう。"))),

    digest_mod(
        "06", "Functions",
        '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 12h4"/><path d="M13 9l4 3-4 3"/>',
        "関数にすると、何がよくなりますか?",
        "何度も呼び出せて、全体が理解しやすくなる",
        "関数はある機能をひとまとめにしたもので、プログラムのほかの部分から呼び出して使えます。あらかじめ用意されているものを組み込み関数、作成者が定義するものをユーザ定義関数といいます。",
        viz("FUNCTION — 定義と呼び出し",
            "呼び出し元から関数へ渡す値が引数、関数から返す値が戻り値です。",
            checklist([
                ("1", "関数", "ある機能をひとまとめにしたもの。組み込み関数とユーザ定義関数がある"),
                ("2", "引数", "関数の呼び出し元から関数へ引き渡す値"),
                ("3", "戻り値", "関数から呼び出し元へ渡す値。返り値ともいう"),
            ])
            + pyprog([
                ("1", "def sankaku(teihen, takasa):"),
                ("2", IND + "menseki = teihen * takasa / 2"),
                ("3", IND + "return menseki"),
                ("4", ""),
                ("5", "kekka1 = sankaku(8, 4)"),
                ("6", "kekka2 = sankaku(6, 3)"),
                ("7", "print('1つ目', kekka1)"),
                ("8", "print('2つ目', kekka2)"),
            ], "確認事項の使用例。同じ関数を何度も呼び出せる", "関数の使用例【Python】")
            + note_box("計算式を直接 return の後ろに書けば、その計算結果がそのまま呼び出し元へ返ります。"
                       "計算の結果を一度変数に代入しておき、その変数を戻り値として返してもかまいません。"))),
]

REVIEW = ('  <section class="stage" data-stage-name="REVIEW">\n'
          '    <div class="section-divider">\n'
          '      <span class="num">01</span>\n'
          '      <div class="text">\n'
          '        <div class="label">Section 1 — Review</div>\n'
          '        <div class="name">基本知識のおさらい</div>\n'
          '      </div>\n'
          '    </div>\n'
          '    <div class="digest">\n'
          + "".join(REVIEW_MODS)
          + '    </div>\n'
          '  </section>\n')


# ============================================================
# 例題55 — 選択構造と割り算の余り
# ============================================================
EX55 = stage_example(
    1, 5, "55", "ベストフィット 例題55", "選択構造と割り算の余り", "ex55", SELF_TAG,
    "次の⑴、⑵のプログラムを実行した結果、画面に表示されるものを答えよ。なお、「a % b」は、割り算の余りを得るもので、算術演算子と呼ばれる演算子の一つである。",
    "",
    self_list([
        ("⑴", pyprog([("1", "x = 10"), ("2", "if x % 3 == 0:"), ("3", IND + "print('FIZZ')"),
                      ("4", "else:"), ("5", IND + "print(x)")]) + "画面に表示されるものを答えよ。",
         "<p><strong>10</strong></p><p>x が 3 で割り切れれば FIZZ、そうでなければ x の値を表示するプログラムである。"
         "10 を 3 で割った余りは 1 なので、else の側が実行される。</p>"),
        ("⑵", pyprog([("1", "x = 30"), ("2", "if x % 3 == 0:"), ("3", IND + "print('FIZZ')"),
                      ("4", IND + "if x % 5 == 0:"), ("5", IND * 2 + "print('BUZZ')")]) + "画面に表示されるものを答えよ。",
         "<p><strong>FIZZ, BUZZ</strong>（縦に表示）</p><p>3〜5行目が2行目の分岐処理の対象、5行目が4行目の分岐処理の対象であることがインデントから読み取れる。"
         "2行目の分岐処理が4行目の分岐処理を内包する「入れ子構造」である。</p>"),
    ]),
    feedback("正答: ⑴ 10　⑵ FIZZ, BUZZ（縦に表示）", [
        fb_section("ベストフィット", bestfit("「割り切れる」、「倍数」の判断は割り算の余りで行う。分岐処理の対象範囲に注意する。")),
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　xが3で割り切れればFIZZ、そうでなければxの値を表示するプログラムである。</p>"
            "<p><strong>⑵</strong>　3〜5行目が2行目の分岐処理の対象、5行目が4行目の分岐処理の対象であることがインデントから読み取れる。"
            "2行目の分岐処理が4行目の分岐処理を内包する「入れ子構造」である。xが3で割り切れればFIZZ、3で割り切れてかつ5でも割り切れる、"
            "つまり15で割り切れればFIZZ BUZZと表示し、それ以外は何も表示しないプログラムである。</p>")),
        fb_section("入れ子を読む手順(補足)", explain(
            "<p>インデントの深さが、その行が<strong>どの if の中にいるか</strong>を示します。⑵ では 5 行目だけが 4 行目より深いので、"
            "5 行目は「3 で割り切れ、かつ 5 でも割り切れる」ときにしか実行されません。x を変えて、どの行まで進むかを追うと確かめられます。</p>")
            + tbl(["x", "3 で割り切れる", "5 で割り切れる", "表示"],
                  [["30", "○", "○", "FIZZ, BUZZ"], ["9", "○", "×", "FIZZ"],
                   ["10", "×", "○", "（何も表示されない）"], ["7", "×", "×", "（何も表示されない）"]],
                  caption="⑵ のプログラムに、いろいろな x を入れたとき")),
        viz("NESTED IF — 入れ子構造", "内側の if は、外側が真のときにしか確かめられません。",
            checklist([("1", "2 行目", "x % 3 == 0 を確かめる。偽ならここで終わり"),
                       ("2", "3 行目", "FIZZ を表示（2 行目が真のとき）"),
                       ("3", "4 行目", "x % 5 == 0 を確かめる（2 行目が真のときだけ）"),
                       ("4", "5 行目", "BUZZ を表示（2 行目と 4 行目がどちらも真のとき）")])),
    ], example=True))

# ============================================================
# 例題56 — 繰り返し構造と数え上げ・加算
# ============================================================
EX56 = stage_example(
    2, 5, "56", "ベストフィット 例題56", "繰り返し構造と数え上げ・加算", "ex56", SELF_TAG,
    "次の⑴、⑵のプログラムを実行した結果、画面に表示されるものを答えよ。なお、「range(5)」は、0から5未満の整数を返す組み込み関数である。",
    "",
    self_list([
        ("⑴", pyprog([("1", "x = 0"), ("2", "for i in range(5):"), ("3", IND + "x = x + 1"),
                      ("4", "print(x)")]) + "画面に表示されるものを答えよ。",
         "<p><strong>5</strong></p><p>print(x) は 3 行目と同じ深さではないので繰り返しの対象ではない。"
         "1 を 5 回加算し終えたあと、1 回だけ表示される。</p>"),
        ("⑵", pyprog([("1", "x = 0"), ("2", "for i in range(5):"), ("3", IND + "x = x + i"),
                      ("4", IND + "print(x)")]) + "画面に表示されるものを答えよ。",
         "<p><strong>0, 1, 3, 6, 10</strong>（縦に表示）</p><p>print(x) が繰り返しの対象なので 5 回実行される。"
         "i は 0 から 1 ずつ増えるので、加えられる値も 0、1、2、3、4 と変わっていく。</p>"),
    ]),
    feedback("正答: ⑴ 5　⑵ 0, 1, 3, 6, 10（縦に表示）", [
        fb_section("ベストフィット", bestfit("繰り返し処理を使い、数え上げや加算を行う。繰り返しの対象範囲に注意する。")),
        fb_section("解説(原本)", explain(
            "<p>⑴⑵の2行目は、5回繰り返しを行うfor文で、共通テスト用プログラム表記で表した場合の"
            "「iを0から4まで1ずつ増やしながら繰り返す」に相当する。繰り返しの対象行は、⑴は3行目のみ、⑵は3・4行目であることがインデントからわかる。"
            "よって、print(x)は、⑴は繰り返しの対象ではないため1回、⑵は繰り返しの対象となるため5回実行される。</p>"
            "<p>⑴⑵の3行目の「x = x + ○」は、「xに○を加えた結果をxに代入する」処理である。⑴では1を5回加算する。"
            "⑵では「i（0から1ずつ増えていく変数）」を繰り返し加算する処理である。</p>")),
        fb_section("1 行ずつ追う(補足)", explain(
            "<p>⑵ は x に i を足すので、足す値そのものが毎回変わります。表示されるのは足したあとの x です。</p>")
            + tbl(["回", "i", "加える値", "加えたあとの x", "表示"],
                  [["1回目", "0", "0", "0", "0"], ["2回目", "1", "1", "1", "1"],
                   ["3回目", "2", "2", "3", "3"], ["4回目", "3", "3", "6", "6"],
                   ["5回目", "4", "4", "10", "10"]],
                  caption="⑵ のトレース。0+1+2+3+4 が順に積み上がる", mono=True)),
        viz("INDENT DECIDES — 1 行の深さで結果が変わる", "同じ 4 行でも、4 行目の深さが違うだけで表示の回数が変わります。",
            compare2(("⑴ print が外", [("繰り返しの対象", "3 行目だけ"), ("表示回数", "1 回"), ("表示", "5")]),
                     ("⑵ print が中", [("繰り返しの対象", "3・4 行目"), ("表示回数", "5 回"), ("表示", "0, 1, 3, 6, 10")]))),
    ], example=True))

# ============================================================
# 例題57 — 配列と最小値
# ============================================================
EX57 = stage_example(
    3, 5, "57", "ベストフィット 例題57", "配列と最小値", "ex57", SELF_TAG,
    "ある商品について、五つの店舗の小売価格の最安値を求める次のプログラムの空欄を埋めよ。なお、「for x in kakaku:」は、変数xにリストkakakuの要素を一つずつ代入しながら要素数分の繰り返しを行う制御文である。",
    pyprog([("1", "kakaku = [580, 970, 430, 820, 760]"),
            ("2", "saisyo = kakaku[0]"),
            ("3", "for x in kakaku:"),
            ("4", IND + "if x 　①　 saisyo:"),
            ("5", IND * 2 + "saisyo = 　②"),
            ("6", "print('最安値:', 　③　)")]),
    self_list([
        (None, "空欄 ①②③ に入るものを答えよ。",
         "<p><strong>①　&lt;　　②　x　　③　saisyo</strong></p>"
         "<p>その時点での最小値と各要素を順に比較し、より小さな値が見つかるたびに最小値を置き換えていく。"
         "2 行目でリストの第一要素を最小値の初期値にしているので、③ では saisyo をそのまま表示すればよい。</p>"),
    ]),
    feedback("正答: ①　&lt;　　②　x　　③　saisyo", [
        fb_section("ベストフィット", bestfit("その時点での最小値と各要素を順次比較しながら最小値を置き換えていく。")),
        fb_section("解説(原本)", explain(
            "<p>3行目のような、リストの要素を一つずつ代入しながら繰り返しを行う指定は直観的でわかりやすい記述方法である。"
            "このような記述ができないプログラミング言語では、要素数分の繰り返し処理を記述し、繰り返し処理内で、要素を取り出して変数xに代入する処理を記述する。</p>"
            "<p>最小値を求めるには、まず、このプログラムの2行目のようにリストの第一要素の値、もしくは最小値になり得ない大きい値を一時的に最小値"
            "（ここではsaisyo）に代入しておき、繰り返し処理の中で、より小さな値へと最小値を更新していく。</p>"
            "<p>空欄①を「&lt;」でなく「&lt;=」としても結果は同じだが、効率の悪いプログラムとなる。「&lt;=」とした場合、"
            "xとsaisyoが等しいときにもsaisyo値の書き換えを行うが、最小値を求めるという目的に対してこの処理の必要性はなく、効率がよくない。</p>")),
        fb_section("更新の様子(補足)", explain("<p>更新が起きるのは、それまでの最小値より小さい値が出てきたときだけです。</p>")
            + tbl(["x", "そのときの saisyo", "更新するか", "更新後"],
                  [["580", "580", "しない", "580"], ["970", "580", "しない", "580"],
                   ["430", "580", "する", "430"], ["820", "430", "しない", "430"],
                   ["760", "430", "しない", "430"]],
                  caption="最安値は 430", mono=True)),
        viz("MIN — 最小値を求める型", "最大値を求めるときも、不等号の向きを変えるだけで同じ形が使えます。",
            checklist([("1", "初期値", "第一要素、または最小値になり得ない大きい値を入れておく"),
                       ("2", "比較", "いまの最小値と、取り出した要素を比べる"),
                       ("3", "更新", "小さければ、最小値を置き換える"),
                       ("4", "表示", "繰り返しが終わったあとに、残った最小値を表示する")])),
    ], example=True))

# ============================================================
# 例題58 — 二次元配列
# ============================================================
EX58 = stage_example(
    4, 5, "58", "ベストフィット 例題58", "二次元配列", "ex58", SELF_TAG,
    "1日の降水量のデータが1年間分、二次元配列kousuiに入っている。最初の添字は月を、2番目の添字は日付を昇順で表し、kousui[0][0]は1月1日の降水量を表すとき、kousui[2][8]は何月何日の降水量を指しているか答えよ。",
    "",
    self_list([
        (None, "kousui[2][8] は何月何日の降水量を指しているか。",
         "<p><strong>3月9日</strong></p><p>kousui[0][0] が 1 月 1 日なので、添字は 0 から始まる。"
         "最初の添字 2 は 3 番目の月、2 番目の添字 8 は 9 番目の日を指す。</p>"),
    ]),
    feedback("正答: 3月9日", [
        fb_section("ベストフィット", bestfit("kousui[a][b]はa番目の配列の中のb番目の要素を指す。添字の開始番号に注意する。")),
        fb_section("解説(原本)", explain(
            "<p>kousui[i][j]は、二次元配列で、内包されているi番目の配列内j番目の要素を指す。"
            "この例題では、添字が0から始まるか1から始まるかの記載はないが、kousui[0][0]が登場することから、0で始まることがわかる。</p>")),
        fb_section("添字と「何番目」のずれ(補足)", explain(
            "<p>上の「ベストフィット」「解説」にある <strong>a 番目の配列・i 番目の要素</strong>は、"
            "<strong>添字の番号</strong>を指す言い方です。日常語の「何番目」とは 1 つずれるので、読み分けてください。</p>"
            "<p>添字が 0 から始まるとき、<strong>添字 + 1 が「何番目か」</strong>になります。"
            "問題文に添字の始まりが書かれていなくても、kousui[0][0] のように <strong>0 が使われている例</strong>が出ていれば、"
            "そこから 0 始まりだと読み取れます。</p>")
            + tbl(["添字", "0", "1", "2", "…", "8"],
                  [["月（最初の添字）", "1月", "2月", "3月", "…", "9月"],
                   ["日（2番目の添字）", "1日", "2日", "3日", "…", "9日"]],
                  caption="kousui[2][8] は 3 月 9 日", lft=(0,))),
        viz("2-D INDEX — 二つの添字", "最初の添字が外側の配列、2 番目の添字がその中の要素です。",
            compare2(("最初の添字 [2]", [("指すもの", "添字 2 の配列（＝3 番目の月）"), ("この問題では", "3 月のデータ")]),
                     ("2 番目の添字 [8]", [("指すもの", "添字 8 の要素（＝9 番目の日）"), ("この問題では", "9 日")]))),
    ], example=True))

# ============================================================
# 例題59 — 関数
# ============================================================
EX59 = stage_example(
    5, 5, "59", "ベストフィット 例題59", "関数", "ex59", SELF_TAG,
    "入力された商品価格と消費税率から税込金額を求めて表示する、次のプログラムの空欄に入る変数名を答えよ。ただし、1円未満は切り捨てとする（「//」は割り算の商の整数部分を得る演算子である）。",
    pyprog([("1", "def zeikomi(kingaku, tax):"),
            ("2", IND + "return kingaku + kingaku * tax // 100"),
            ("3", "kakaku = 1980"),
            ("4", "kekka10 = zeikomi(　①　, 10)"),
            ("5", "kekka8 = zeikomi(　①　, 8)"),
            ("6", "print(kakaku, '円は税率10％で',  ②, '円・税率8％で', 　③　, '円')")]),
    self_list([
        (None, "空欄 ①②③ に入る変数名を答えよ。",
         "<p><strong>①　kakaku　　②　kekka10　　③　kekka8</strong></p>"
         "<p>① は関数に渡す引数なので、価格を入れておいた変数 kakaku。②③ は関数の戻り値を受け取った変数で、"
         "税率 10％ の結果が kekka10、8％ の結果が kekka8 である。</p>"),
    ]),
    feedback("正答: ①　kakaku　　②　kekka10　　③　kekka8", [
        fb_section("ベストフィット", bestfit("処理のまとまりを関数として定義することで、プログラムの別の場所から何度も呼び出すことができる。")),
        fb_section("解説(原本)", explain(
            "<p>1・2行目で関数zeikomi()を定義している。呼び出し元から渡される引数はkingakuとtax、戻り値は、"
            "計算式を直接returnの後に記述することで、その計算結果を呼び出し元に返すよう記述されている。"
            "計算の結果を一度変数に代入しておき、その変数を戻り値として返してもよい。4・5行目で2回関数を呼び出している。</p>"
            "<p>このように、何度でも呼び出す可能性のある処理のまとまりや、ある特定の用途を記述した部分を関数として独立させておくことで、"
            "プログラム全体が理解しやすく、また修正もしやすくなる。</p>")),
        fb_section("実際の金額(補足)", explain(
            "<p>原本は変数名だけを問うていますが、値を入れて確かめると関数の働きがはっきりします。"
            "「//」は商の整数部分を得るので、1 円未満は切り捨てられます。</p>")
            + tbl(["呼び出し", "kingaku", "tax", "kingaku * tax // 100", "戻り値"],
                  [["zeikomi(kakaku, 10)", "1980", "10", "198", "2178"],
                   ["zeikomi(kakaku, 8)", "1980", "8", "158", "2138"]],
                  caption="1980 × 8 ÷ 100 は 158.4 だが、// なので 158 になる", mono=True, small=True)),
        viz("CALL — 引数と戻り値の行き来", "呼び出し元から関数へ渡すのが引数、関数から返ってくるのが戻り値です。",
            checklist([("1", "定義", "def zeikomi(kingaku, tax): で、受け取る名前を決める"),
                       ("2", "呼び出し", "zeikomi(kakaku, 10) で、実際の値を渡す"),
                       ("3", "戻り値", "return の後ろの計算結果が、呼び出した場所へ返る"),
                       ("4", "受け取り", "kekka10 = ... で、返ってきた値に名前をつける")])),
    ], example=True))

# ============================================================
# 類題99 — 選択構造と不等号
# ============================================================
P99 = stage_practice(
    1, 8, "99", "ベストフィット 類題99", "〈選択構造と不等号〉", "p1", SELF_TAG,
    "右のフローチャートは、ある映画館のチケット代金を年齢に応じて決定する処理の一部を表したものである。25歳の場合の代金はいくらか。",
    figure("assets/fig5-ticket-flowchart.jpeg",
           "映画館のチケット代金のフローチャート。18歳以下？が Yes なら1000円、No なら 60歳以上？へ進み、Yes なら1200円、No なら1800円",
           "図: チケット代金を決めるフローチャート（原本の図）", 460, 420),
    self_list([
        (None, "25歳の場合の代金はいくらか。",
         "<p><strong>1800円</strong></p><p>25歳を指定した場合の流れを追ってみると、最初の分岐の条件式「18歳以下？」でNoとなって右下の次の分岐へ進む。"
         "次の分岐の条件式は「60歳以上？」のため、再びNoとなって右下の「1800円」に到達する。</p>"),
    ]),
    feedback("正答: 1800円", [
        fb_section("解説(原本)", explain(
            "<p>25歳を指定した場合の流れを追ってみると、最初の分岐の条件式「18歳以下？」でNoとなって右下の次の分岐へ進む。"
            "次の分岐の条件式は「60歳以上？」のため、再びNoとなって右下の「1800円」に到達する。</p>"
            "<p>Pythonでのプログラム例を以下に示す。if-elseの入れ子構造となっている。Pythonでは、「そうでなくもし・・・ならば」の条件分岐に"
            "elifという記述を使うことで三つ以上の分岐を並列して表現できるので、二つ目のプログラム例のように簡潔に記述できる。</p>")
            + pyprog([("1", "if x &lt;= 18:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style=\"color:var(--ink-mute)\"># もしx&lt;=18ならば</span>"),
                      ("2", IND + "print('1000円')"),
                      ("3", "else:"),
                      ("4", IND + "if x &gt;= 60:"),
                      ("5", IND * 2 + "print('1200円')"),
                      ("6", IND + "else:"),
                      ("7", IND * 2 + "print('1800円')")], "入れ子で書いた場合")
            + pyprog([("1", "if x &lt;= 18:"),
                      ("2", IND + "print('1000円')"),
                      ("3", "elif x &gt;= 60:"),
                      ("4", IND + "print('1200円')"),
                      ("5", "else:"),
                      ("6", IND + "print('1800円')")], "elif を使って簡潔に書いた場合")),
        fb_section("境目を確かめる(補足)", explain(
            "<p>「18歳以下」は 18 を含み、「60歳以上」は 60 を含みます。境目の年齢を入れて、どこへ流れるかを確かめておくと取り違えません。</p>")
            + tbl(["年齢", "18歳以下？", "60歳以上？", "代金"],
                  [["18", "Yes", "—", "1000円"], ["19", "No", "No", "1800円"],
                   ["25", "No", "No", "1800円"], ["59", "No", "No", "1800円"],
                   ["60", "No", "Yes", "1200円"]],
                  caption="境目の 18 と 60 は、それぞれ「以下」「以上」の側に入る")),
        viz("BRANCH — 二つの分岐を順に通る", "最初の分岐で No だった人だけが、次の分岐へ進みます。",
            checklist([("1", "18歳以下？", "Yes → 1000円　No → 次の分岐へ"),
                       ("2", "60歳以上？", "Yes → 1200円　No → 1800円"),
                       ("3", "25歳", "どちらも No なので 1800円")])),
    ]))

# ============================================================
# 類題100 — 選択構造
# ============================================================
P100 = stage_practice(
    2, 8, "100", "ベストフィット 類題100", "〈選択構造〉", "p2", SELF_TAG,
    "入力された整数が変数xに入っているとき、xの絶対値を表示する次のプログラムの空欄に適当なものを入れよ。",
    pyprog([("(01)", "もし 　①　 ならば:"),
            ("(02)", IND + "x = 　②"),
            ("(03)", "表示する(\"絶対値:\", x)")], None, "共通テスト用プログラム表記"),
    self_list([
        ("①", "空欄 ① に入る条件を答えよ。",
         "<p><strong>x &lt; 0</strong></p><p>「xの絶対値はx＞＝0の場合はx、x＜0の場合は－x」という数学の知識を基に考える。</p>"),
        ("②", "空欄 ② に入るものを答えよ。",
         "<p><strong>-x</strong></p><p>2行目の＝（イコール）は代入を意味する演算子で、等しいことを意味する等号とは異なる。"
         "例えば、xの値が－5の場合、右辺の－xは－（－5）、すなわち5となり、左辺のxに5が代入される。</p>"),
    ]),
    feedback("正答: ①　x &lt; 0　　②　-x", [
        fb_section("解説(原本)", explain(
            "<p>「xの絶対値はx＞＝0の場合はx、x＜0の場合は－x」という数学の知識を基に考える。2行目の＝（イコール）は代入を意味する演算子で、"
            "等しいことを意味する等号とは異なる。例えば、xの値が－5の場合、右辺の－xは－（－5）、すなわち5となり、左辺のxに5が代入される。"
            "Pythonでのプログラム例を以下に示す。値を入力して動作確認できるよう、入力処理を最初に行っている。"
            "①はx＜＝0でも動作するが、x＝0のときは無駄な処理となるため効率が悪い。</p>")
            + pyprog([("0", "x = int(input('整数を入力'))"),
                      ("1", "if x &lt; 0:"),
                      ("2", IND + "x = -x"),
                      ("3", "print(x)")], "Python で書いた場合")),
        fb_section("= と == の違い(補足)", explain(
            "<p>x = -x は「等しい」という意味ではありません。<strong>右辺を計算して、その結果を左辺に代入する</strong>という指示です。"
            "数式として読むと x = -x は x = 0 のときしか成り立ちませんが、代入文としては「符号を反転した値を入れ直す」処理になります。</p>")
            + tbl(["入力した x", "x &lt; 0 は真か", "実行後の x", "表示"],
                  [["-5", "真", "5", "絶対値: 5"], ["0", "偽", "0", "絶対値: 0"], ["7", "偽", "7", "絶対値: 7"]],
                  caption="x = 0 のときは条件が偽なので、そのまま表示される", mono=True)),
        viz("ABS — 負のときだけ符号を変える", "0 以上ならそのまま、負なら符号を反転します。",
            compare2(("x ＞＝ 0 のとき", [("条件", "偽"), ("処理", "何もしない"), ("表示", "x そのまま")]),
                     ("x ＜ 0 のとき", [("条件", "真"), ("処理", "x = -x"), ("表示", "符号を反転した値")]))),
    ]))

# ============================================================
# 類題101 — 繰り返し構造
# ============================================================
P101 = stage_practice(
    3, 8, "101", "ベストフィット 類題101", "〈繰り返し構造〉", "p3", SINGLE_TAG,
    "年1回1％の複利がつく預金に預けたyokin円の、10年間の預金額の推移を表示する次のプログラムについて最も適当な記述を、次の(ア)〜(エ)から一つ選べ。",
    pyprog([("1", "risoku = 1.0"),
            ("2", "for i in range(10):"),
            ("3", IND + "yokin = yokin * (1 + risoku / 100)"),
            ("4", IND + "print(int(yokin))")]),
    opts_single("p101", 3, [
        ("ア", "利息は毎年100分の1ずつ増加する。"),
        ("イ", "最終的な預金額に年数は関係ない。"),
        ("ウ", "預金額は計算後に一度だけ表示される。"),
        ("エ", "預金額は年数分繰り返し表示される。"),
    ]),
    feedback("正答: (エ)", [
        fb_section("解説(原本)", explain(
            "<p><strong>(ア)</strong>　適当でない。利息が%表記のため、risoku / 100として計算しているが、100分の1ずつ増加するのはyokinであり、risokuではない。</p>"
            "<p><strong>(イ)</strong>　適当でない。10年分、10回繰り返し利息分を加算しているので、預金額と年数は関係がある。</p>"
            "<p><strong>(ウ)(エ)</strong>　4行目のprint()は3行目と同じインデントなので、3行目と同様に10回繰り返し実行される。"
            "もし、4行目が2行目と同じインデントであれば、繰り返しの対象とはならず、最後に1度だけ表示される。"
            "なお、int(yokin)は引数yokinを整数型に変換して返す処理である。小数点以下は切り捨てられる。</p>")),
        fb_section("誤答の作られ方(補足)", explain(
            "<p>(ア) は変数名の取り違え、(イ) は繰り返し回数の見落とし、(ウ) は <strong>4 行目のインデント</strong>の読み違えです。"
            "どれも「繰り返しの対象がどこまでか」を読めば決まります。4 行目が 3 行目と同じ深さにあるので、表示も 10 回行われます。</p>")
            + tbl(["4行目のインデント", "繰り返しの対象か", "表示回数"],
                  [["3行目と同じ深さ（本問）", "対象", "10 回"],
                   ["2行目と同じ深さ", "対象でない", "最後に 1 回"]],
                  lft=(0,))),
        viz("COMPOUND — 複利は前の年の結果に掛かる", "毎年、その時点の預金額に 1.01 を掛けます。",
            checklist([("1", "1 年目", "yokin × 1.01 を yokin に代入し、表示する"),
                       ("2", "2 年目", "増えたあとの yokin に、また 1.01 を掛ける"),
                       ("3", "10 年目まで", "これを 10 回繰り返すので、表示も 10 回行われる")])),
    ]))

# ============================================================
# 類題102 — 配列と最大値
# ============================================================
P102 = stage_practice(
    4, 8, "102", "ベストフィット 類題102", "〈配列と最大値〉", "p4", MATCH_TAG,
    "出席番号1番から40番までの得点が配列Tokutenに入っている。最高得点を表示する次のプログラムの空欄に入る最も適当なものを、下の(ア)〜(ケ)から一つずつ選べ。ただし、「要素数(配列)」は配列の要素数を返す関数である。なお、配列の添字は1から始まるものとする。",
    pyprog([("(01)", "Tokuten = [50, 40, ・・(略)・・, 30, 70]"),
            ("(02)", "saidai = 0"),
            ("(03)", "bango = 0"),
            ("(04)", "iを1から 　①　 まで1ずつ増やしながら繰り返す:"),
            ("(05)", IND + "もしTokuten[i] 　②　 saidaiならば:"),
            ("(06)", IND * 2 + "saidai = Tokuten[i]"),
            ("(07)", IND * 2 + "bango = i"),
            ("(08)", "表示する(\"最高点：\", saidai, \"出席番号：\", 　③　 )")], None, "共通テスト用プログラム表記")
    + legend([("ア", "要素数（Tokuten）"), ("イ", "要素数（Tokuten）- 1"), ("ウ", "要素数（Tokuten）+ 1"),
              ("エ", "&lt;"), ("オ", "&gt;"), ("カ", "=="),
              ("キ", "i"), ("ク", "bango"), ("ケ", "bango + 1")]),
    match_list("ア,イ,ウ,エ,オ,カ,キ,ク,ケ", "0,4,7",
               [("①", "繰り返しの終わり"), ("②", "比較の記号"), ("③", "表示する出席番号")]),
    feedback("正答: ①　(ア)　　②　(オ)　　③　(ク)", [
        fb_section("解説(原本)", explain(
            "<p>最大値（や最小値）を求める場合によく使う方法である。最大値よりも大きい数が見つかるたびに最大値を"
            "（最小値よりも小さな数が見つかるたびに最小値を）更新する。本問では、出席番号も表示するため、bangoも更新している。</p>"
            "<p>プログラミング言語の多くは、添字は基本的に0から始まる。大学入試センターの共通テスト用プログラム表記の例示でも、"
            "「特に説明がない場合、配列の要素を指定する添字は0から始まる」と明記されている。しかし、本問のように、"
            "問題文中に「添字は1から始まる」と明記されている場合もあるので、問題文をよく読み、下線を引いておくなどするとよい。</p>")),
        fb_section("③ が bango になる理由(補足)", explain(
            "<p>本問は<strong>添字が 1 から始まる</strong>ので、添字 i がそのまま出席番号になります。だから ③ は bango です。"
            "もし添字が 0 から始まる書き方なら、出席番号は bango + 1 になります。"
            "原本が示す Python のプログラムでは添字が 0 から始まるため、末尾が bango + 1 に変わっています。"
            "<strong>同じ処理でも、添字の始まりで表示の式が変わります。</strong></p>")
            + tbl(["添字の始まり", "繰り返しの範囲", "表示する出席番号"],
                  [["1 から（本問）", "1 〜 要素数（Tokuten）", "bango"],
                   ["0 から（Python）", "0 〜 要素数 − 1", "bango + 1"]],
                  lft=(0, 1, 2))),
        viz("MAX — 最大値と、その位置", "値だけでなく「何番目だったか」も一緒に覚えておきます。",
            checklist([("1", "初期値", "saidai に 0、bango に 0 を入れておく"),
                       ("2", "比較", "Tokuten[i] が saidai より大きいか（記号は &gt;）"),
                       ("3", "更新", "大きければ saidai と bango の両方を書きかえる"),
                       ("4", "表示", "残った saidai と bango を表示する")])),
    ]))

# ============================================================
# 類題103 — 二次元配列
# ============================================================
P103 = stage_practice(
    5, 8, "103", "ベストフィット 類題103", "〈二次元配列〉", "p5", SELF_TAG,
    "下のプログラムは、かけ算の九九の値を二次元配列（リスト）に入れるプログラムである。引数として渡された一次元配列を横一列に表示する関数「配列表示()」をプログラムの(05)行目に記述して、九九の表を9段分画面表示したい。その際、「配列表示()」が9回繰り返されるようにする必要があるので、「配列表示()」の左端の位置を　①　行目と揃えて記述する。なお、「配列表示()」は、一度呼び出されるたびに改行する。",
    pyprog([("(01)", "二次元配列Kukuを初期化する"),
            ("(02)", "danを1から9まで1ずつ増やしながら繰り返す:"),
            ("(03)", IND + "kazuを1から9まで1ずつ増やしながら繰り返す:"),
            ("(04)", IND * 2 + "Kuku[dan][kazu] = dan * kazu")], None, "共通テスト用プログラム表記"),
    self_list([
        ("⑴", "空欄①に入る数値を答えよ。",
         "<p><strong>03</strong></p><p>「配列表示()」を9回繰り返すには、dan のループの中で、kazu のループの外に置く必要がある。"
         "つまり (03) 行目と同じ左端に揃える。</p>"),
        ("⑵", "「配列表示()」に渡す引数を、次の(ア)〜(エ)から一つ選べ。<br>(ア)　Kuku　　(イ)　Kuku[dan]　　(ウ)　Kuku[kazu]　　(エ)　Kuku[dan][kazu]",
         "<p><strong>(イ)　Kuku[dan]</strong></p><p>渡すのは一次元配列、つまり 1 段ぶんの並びである。Kuku[dan] が dan の段の一次元配列にあたる。</p>"),
    ]),
    feedback("正答: ⑴ 03　⑵ (イ)", [
        fb_section("解説(原本)", explain(
            "<p>hairetsu[i][j]は、内包されているi番目のリストのj番目の要素を指す。配列の添字が0から始まるPythonの場合、例えば、"
            "hairetsu=[[1, 2, 3], [11, 22, 33]]でhairetsu[1][2]とすると、内包されている1番目のリストの2番目、つまり33を指す。"
            "本文のプログラムでは、添字の役割を果たしているdanとkazuを1〜9まで変更して使用していることに注意する。"
            "添字が0から始まるか1から始まるかが明記されていないが、配列の中で九九の値が代入されている範囲は添字1〜9の範囲であることがプログラムからわかる。</p>")
            + pyprog([("1", "Kuku = [[0] * 9 for _ in range(9)]"),
                      ("2", "for dan in range(1, 10, 1):"),
                      ("3", IND + "for kazu in range(1, 10, 1):"),
                      ("4", IND * 2 + "Kuku[dan - 1][kazu - 1] = dan * kazu"),
                      ("5", IND + "print(Kuku[dan - 1])")], "Python で書いた場合。添字が 0 から始まるので「-1」している")),
        fb_section("左端の位置で回数が決まる(補足)", explain(
            "<p>「配列表示()」をどの深さに置くかで、呼ばれる回数が変わります。求められているのは <strong>9 回</strong>なので、"
            "dan のループの中・kazu のループの外、つまり (03) 行目と同じ左端です。</p>")
            + tbl(["左端を揃える行", "どのループの中か", "呼ばれる回数"],
                  [["(02) 行目", "どちらのループの外", "1 回（最後に）"],
                   ["(03) 行目", "dan のループの中だけ", "9 回"],
                   ["(04) 行目", "dan と kazu の両方の中", "81 回"]],
                  lft=(0, 1))),
        viz("NESTED LOOP — 二重の繰り返し", "外側が段、内側がその段の 9 個の値です。",
            checklist([("1", "外側 dan", "1 から 9 まで。1 段ぶんを担当する"),
                       ("2", "内側 kazu", "1 から 9 まで。その段の 9 個を埋める"),
                       ("3", "配列表示()", "内側が終わるたびに 1 回。9 段ぶんで 9 回")])),
    ]))

# ============================================================
# 類題104 — 関数
# ============================================================
P104 = stage_practice(
    6, 8, "104", "ベストフィット 類題104", "〈関数〉", "p6", SELF_TAG,
    "次のプログラムの5行目で5が入力された場合に「答えは」に続いて表示されるものを答えよ。",
    pyprog([("1", "def func(kazu):"),
            ("2", IND + "pai = 3.14"),
            ("3", IND + "return pai * kazu * kazu"),
            ("4", ""),
            ("5", "x = float(input('正の数を入力'))"),
            ("6", "print('答えは', func(x))")]),
    self_list([
        (None, "「答えは」に続いて表示されるものを答えよ。",
         "<p><strong>78.5</strong></p><p>半径kazuを使って円の面積を求めるプログラムである。"
         "3.14 × 5 × 5 で 78.5 になる。</p>"),
    ]),
    feedback("正答: 78.5", [
        fb_section("解説(原本)", explain(
            "<p>半径kazuを使って円の面積を求めるプログラムである。以下にコメント付きのPythonプログラムを示す。</p>")
            + pyprog([("1", "def func(kazu):&nbsp;&nbsp;&nbsp;&nbsp;<span style=\"color:var(--ink-mute)\"># 関数func()を定義する</span>"),
                      ("2", IND + "pai = 3.14"),
                      ("3", IND + "return pai * kazu * kazu&nbsp;&nbsp;<span style=\"color:var(--ink-mute)\"># 呼び出し元に返す</span>"),
                      ("4", ""),
                      ("5", "x = float(input('正の数を入力'))"),
                      ("6", "print('答えは', func(x))")], "原本のコメント付きプログラム")),
        fb_section("関数の中で何が起きるか(補足)", explain(
            "<p>入力された 5 は float で小数として読み込まれ、引数 kazu に渡されます。関数の中で pai に 3.14 を入れ、"
            "pai × kazu × kazu を計算して返します。<strong>関数を呼び出した場所が、そのまま計算結果に置きかわる</strong>と読むと分かりやすくなります。</p>")
            + tbl(["段階", "値"],
                  [["入力", "5"], ["x（float に変換）", "5.0"], ["引数 kazu", "5.0"],
                   ["pai * kazu * kazu", "3.14 × 5.0 × 5.0"], ["戻り値（表示）", "78.5"]],
                  lft=(0,), mono=False)),
        viz("RETURN — 呼び出した場所に返る", "print の中に書かれた func(x) が、戻り値そのものに置きかわります。",
            checklist([("1", "呼び出し", "func(x) が実行され、x の値が kazu に渡る"),
                       ("2", "計算", "関数の中で 3.14 × 5.0 × 5.0 を計算する"),
                       ("3", "返る", "78.5 が呼び出し元へ返り、print がそれを表示する")])),
    ]))

# ============================================================
# 練習105 — 順次・選択・繰り返し
# ============================================================
P105 = stage_practice(
    7, 8, "105", "ベストフィット 練習105", "〈順次・選択・繰り返し〉", "p7", SELF_TAG,
    "次のプログラムは、それぞれ何をするプログラムか答えよ。なお、1行目は、入力された文字列を整数としてxに代入する処理である。また、retsu.append(i) は、リストretsuの末尾に要素iを追加する記述である。",
    "",
    self_list([
        ("⑴", pyprog([("1", "x = int(input('整数を入力'))"), ("2", "if x % 2 == 0:"),
                      ("3", IND + "print('Yes')"), ("4", "else:"), ("5", IND + "print('No')")])
         + "何をするプログラムか。",
         "<p><strong>入力された整数が偶数かどうかを判定するプログラム（偶数の場合はYes、奇数の場合はNoを表示するプログラム）。</strong></p>"
         "<p>1行目で受け取った変数xが2で割り切れるかどうかで分岐している。割り切れれば'Yes'、それ以外は'No'を表示している。</p>"),
        ("⑵", pyprog([("1", "x = int(input('3桁の整数を入力'))"), ("2", "n100 = x // 100"),
                      ("3", "n10 = (x % 100) // 10"), ("4", "n1 = x % 10"),
                      ("5", "print(n1 * 100 + n10 * 10 + n100)")])
         + "何をするプログラムか。",
         "<p><strong>入力された3桁の整数の一の位、十の位、百の位の並び順を逆にした整数を表示するプログラム。</strong></p>"
         "<p>2行目では百の位の数、3行目では十の位の数、4行目では一の位の数を求めている。5行目では一の位の数を100倍、"
         "十の位の数を10倍、百の位の数をそのまま加算しているので、結果的に元の3桁の数の数字の並びが逆順になった数が表示される。</p>"),
        ("⑶", pyprog([("1", "x = int(input('正の整数を入力'))"), ("2", "kekka = 0"),
                      ("3", "for i in range(1, x + 1, 1):"), ("4", IND + "kekka = kekka + i"),
                      ("5", "print(kekka)")])
         + "何をするプログラムか。",
         "<p><strong>1からキー入力された数までの和を表示するプログラム。</strong></p>"
         "<p>range(1, x + 1, 1)は、終了値の「x+1」は含まないので、iの値を1からxまで、"
         "つまり1からキー入力された数まで1ずつ増やしながら繰り返しが行われる。</p>"),
        ("⑷", pyprog([("1", "x = int(input('正の整数を入力'))"), ("2", "retsu = []"),
                      ("3", "for i in range(1, x + 1):"), ("4", IND + "if x % i == 0:"),
                      ("5", IND * 2 + "retsu.append(i)"), ("6", "print(retsu)")])
         + "何をするプログラムか。",
         "<p><strong>キー入力された数の約数をすべて表示するプログラム。</strong></p>"
         "<p>range()には、開始値、終了値、増分値の三つの引数があるが、このプログラムの3行目では、三つ目の引数が省略されている。"
         "増分値を省略すると「1」、開始値を省略すると「0」となる。</p>"),
    ]),
    feedback("正答: ⑴ 偶数かどうかの判定　⑵ 3桁の数の並びを逆にする　⑶ 1 から x までの和　⑷ x の約数をすべて表示", [
        fb_section("解説(原本)", explain(
            "<p><strong>⑴</strong>　1行目で受け取った変数xが2で割り切れるかどうかで分岐している。割り切れれば'Yes'、それ以外は'No'を表示している。</p>"
            "<p><strong>⑵</strong>　Pythonでは、割り算a÷bの商（整数部分）はa // b、余りはa % bで表す。a % bはさまざまな言語で余りとして使われるが、"
            "a // bはPython独特の記法である。2行目では百の位の数、3行目では十の位の数、4行目では一の位の数を求めている。</p>"
            "<p><strong>⑶</strong>　range(1, x + 1, 1)は、終了値の「x+1」は含まないので、iの値を1からxまで、つまり1からキー入力された数まで"
            "1ずつ増やしながら繰り返しが行われる。繰り返し文中でkekkaにiが足し込まれるので、全体として「1 + 2 + 3 + … + x」を行うことになる。</p>"
            "<p><strong>⑷</strong>　range()には、開始値、終了値、増分値の三つの引数があるが、このプログラムの3行目では、三つ目の引数が省略されている。"
            "増分値を省略すると「1」、開始値を省略すると「0」となる。1からキー入力された数まで変化する数iで、入力値xを順次割っていき、"
            "割り切れたら、つまり約数ならばリストに追加している。繰り返しがすべて終了した後でretsuを表示する。</p>")),
        fb_section("値を入れて確かめる(補足)", explain(
            "<p>短いプログラムは、具体的な数を一つ入れて最後まで追うと、何をしているかが見えます。</p>")
            + tbl(["", "入力", "途中", "表示"],
                  [["⑴", "4", "4 % 2 は 0", "Yes"],
                   ["⑵", "123", "n100=1、n10=2、n1=3", "321"],
                   ["⑶", "5", "1+2+3+4+5", "15"],
                   ["⑷", "12", "1,2,3,4,6,12 を追加", "[1, 2, 3, 4, 6, 12]"]],
                  lft=(2, 3), mono=False)),
        viz("READ THE RANGE — 引数を省いた形", "省略された引数には、決まった値が入ります。",
            bd_grid([
                ("range(1, x + 1, 1)", "⑶ の形", "開始値 1、終了値 x+1、増分値 1。終了値は含まないので 1 から x まで。"),
                ("range(1, x + 1)", "⑷ の形", "増分値を省略。省略すると 1 になるので、⑶ と同じ範囲を動く。"),
                ("range(5)", "例題56 の形", "開始値と増分値を省略。0 から 5 未満、つまり 0〜4。"),
            ])),
    ]))

# ============================================================
# 練習106 — 順次構造と算術計算
# ============================================================
P106 = stage_practice(
    8, 8, "106", "ベストフィット 練習106", "〈順次構造と算術計算〉", "p8", SELF_TAG,
    "商品の支払いで、50円、10円、1円の3種類の硬貨だけを使い、なるべく硬貨の枚数が少なくなるように支払いたい。商品代金が変数xに入っているとき、支払う硬貨の最小枚数を表示する次のプログラムの空欄に適当な数字を入れよ。なお、「a ÷ b」はaをbで割った商を表す。",
    pyprog([("(01)", "num50 = x ÷ 　①"),
            ("(02)", "num10 = (x - num50 * 　②　 ) ÷ 　③"),
            ("(03)", "num1 = x - num50 * 　④　 - num10 * 　⑤"),
            ("(04)", "表示する(\"最小限の枚数は\", num50 + num10 + num1, \"枚\")")], None, "共通テスト用プログラム表記"),
    self_list([
        (None, "空欄 ①〜⑤ に入る数字を答えよ。",
         "<p><strong>①　50　　②　50　　③　10　　④　50　　⑤　10</strong></p>"
         "<p>変数num50、num10、num1は、それぞれ50円、10円、1円硬貨の枚数である。"
         "問題文中で最も大きい金額である50円硬貨の枚数から特定していく。</p>"),
    ]),
    feedback("正答: ①　50　　②　50　　③　10　　④　50　　⑤　10", [
        fb_section("解説(原本)", explain(
            "<p>変数num50、num10、num1は、それぞれ50円、10円、1円硬貨の枚数である。問題文中で最も大きい金額である50円硬貨の枚数から特定していく。</p>"
            "<p>具体例で考えると式の立て方がわかりやすい。347円を支払う場合を考えると、347÷50の商は6なので、50円硬貨は6枚必要で、"
            "残額は347－6×50＝47円となる。47÷10の商は4なので、10円硬貨は4枚必要で、残額は347－6×50－4×10＝7円となる。"
            "この残額はすべて1円硬貨で支払うので、1円硬貨は7枚必要である。よって、支払いに必要な最小限の枚数は6＋4＋7＝17枚となる。</p>"
            "<p>なお、(03)行目（Pythonの3行目）は、num1=x%10としても結果は同じである。</p>")
            + pyprog([("0", "x = int(input('代金を入力'))"),
                      ("1", "num50 = x // 50"),
                      ("2", "num10 = (x - num50 * 50) // 10"),
                      ("3", "num1 = x - num50 * 50 - num10 * 10"),
                      ("4", "print('最小限の枚数は', num50 + num10 + num1, '枚')")], "Python で書いた場合")),
        fb_section("347円で追う(補足)", explain(
            "<p>大きい硬貨から順に、<strong>商で枚数を決め、残額を次へ渡す</strong>という形です。</p>")
            + tbl(["段階", "計算", "枚数", "残額"],
                  [["50円", "347 ÷ 50 の商", "6 枚", "347 − 300 = 47 円"],
                   ["10円", "47 ÷ 10 の商", "4 枚", "47 − 40 = 7 円"],
                   ["1円", "残りすべて", "7 枚", "0 円"],
                   ["合計", "6 + 4 + 7", "17 枚", "—"]],
                  lft=(0, 1), caption="最小枚数は 17 枚")),
        viz("GREEDY — 大きいほうから決める", "枚数を最小にするには、使える中でいちばん大きい硬貨から決めます。",
            checklist([("1", "50円硬貨", "x を 50 で割った商。これが枚数"),
                       ("2", "残額", "x から 50円ぶんを引く"),
                       ("3", "10円硬貨", "残額を 10 で割った商"),
                       ("4", "1円硬貨", "最後に残った額がそのまま枚数")])),
    ]))

# ============================================================
# 結果サマリ
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
      <div class="summary-grade" id="summary-grade">—<span class="denom">/8</span></div>
      <div class="summary-headline" id="summary-headline">演習結果</div>
      <div class="summary-subline" id="summary-subline">8問の練習問題のうち、何問完答できたかを示します。</div>
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

STAGES = (WELCOME + REVIEW + EX55 + EX56 + EX57 + EX58 + EX59
          + P99 + P100 + P101 + P102 + P103 + P104 + P105 + P106 + RESULT)

TIMELINE = """  const TIMELINE_ENTRIES = [
    { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
    { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2,  group: 'examples', num: '例55', label: '選択構造と割り算の余り', probId: 'ex55' },
    { idx: 3,  group: 'examples', num: '例56', label: '繰り返し構造と数え上げ・加算', probId: 'ex56' },
    { idx: 4,  group: 'examples', num: '例57', label: '配列と最小値', probId: 'ex57' },
    { idx: 5,  group: 'examples', num: '例58', label: '二次元配列', probId: 'ex58' },
    { idx: 6,  group: 'examples', num: '例59', label: '関数', probId: 'ex59' },
    { idx: 7,  group: 'practice', num: 'Q99',  label: '〈選択構造と不等号〉', probId: 'p1' },
    { idx: 8,  group: 'practice', num: 'Q100', label: '〈選択構造〉', probId: 'p2' },
    { idx: 9,  group: 'practice', num: 'Q101', label: '〈繰り返し構造〉', probId: 'p3' },
    { idx: 10, group: 'practice', num: 'Q102', label: '〈配列と最大値〉', probId: 'p4' },
    { idx: 11, group: 'practice', num: 'Q103', label: '〈二次元配列〉', probId: 'p5' },
    { idx: 12, group: 'practice', num: 'Q104', label: '〈関数〉', probId: 'p6' },
    { idx: 13, group: 'practice', num: 'Q105', label: '〈順次・選択・繰り返し〉', probId: 'p7' },
    { idx: 14, group: 'practice', num: 'Q106', label: '〈順次構造と算術計算〉', probId: 'p8' },
    { idx: 15, group: 'result',   num: '✓',   label: '結果サマリ' }
  ];"""

PROBLEMS = """  const PROBLEMS = [
    { id: 'p1', label: 'Q99',  name: '〈選択構造と不等号〉', stageIdx: 7 },
    { id: 'p2', label: 'Q100', name: '〈選択構造〉', stageIdx: 8 },
    { id: 'p3', label: 'Q101', name: '〈繰り返し構造〉', stageIdx: 9 },
    { id: 'p4', label: 'Q102', name: '〈配列と最大値〉', stageIdx: 10 },
    { id: 'p5', label: 'Q103', name: '〈二次元配列〉', stageIdx: 11 },
    { id: 'p6', label: 'Q104', name: '〈関数〉', stageIdx: 12 },
    { id: 'p7', label: 'Q105', name: '〈順次・選択・繰り返し〉', stageIdx: 13 },
    { id: 'p8', label: 'Q106', name: '〈順次構造と算術計算〉', stageIdx: 14 }
  ];"""


# ============================================================
# 独立検算(原本の解答を実際に動かして確かめる)
# ============================================================
def selfcheck():
    import io
    from contextlib import redirect_stdout

    def run(fn):
        b = io.StringIO()
        with redirect_stdout(b):
            fn()
        return b.getvalue().split()

    # 例題55
    assert run(lambda: (print('FIZZ') if 10 % 3 == 0 else print(10))) == ["10"]
    def ex55_2():
        x = 30
        if x % 3 == 0:
            print('FIZZ')
            if x % 5 == 0:
                print('BUZZ')
    assert run(ex55_2) == ["FIZZ", "BUZZ"]
    # 例題56
    x = 0
    for i in range(5):
        x = x + 1
    assert x == 5
    x, seq = 0, []
    for i in range(5):
        x = x + i
        seq.append(x)
    assert seq == [0, 1, 3, 6, 10]
    # 例題57
    kakaku = [580, 970, 430, 820, 760]
    saisyo = kakaku[0]
    for v in kakaku:
        if v < saisyo:
            saisyo = v
    assert saisyo == 430
    # 例題58: 添字 0 始まり → [2][8] は 3 月 9 日
    assert (2 + 1, 8 + 1) == (3, 9)
    # 例題59
    def zeikomi(kingaku, tax):
        return kingaku + kingaku * tax // 100
    assert (zeikomi(1980, 10), zeikomi(1980, 8)) == (2178, 2138)
    assert 1980 * 8 // 100 == 158
    # 類題99(境目も)
    def ticket(a):
        if a <= 18:
            return 1000
        elif a >= 60:
            return 1200
        return 1800
    assert ticket(25) == 1800
    assert [ticket(n) for n in (18, 19, 59, 60)] == [1000, 1800, 1800, 1200]
    # 類題100
    assert [(-v if v < 0 else v) for v in (-5, 0, 7)] == [5, 0, 7]
    # 類題101: print が繰り返しの中 → 10 回
    shown = 0
    yokin, risoku = 100000, 1.0
    for i in range(10):
        yokin = yokin * (1 + risoku / 100)
        shown += 1
    assert shown == 10
    # 類題102: 添字 1 始まりなら出席番号は bango
    Tokuten = [50, 40, 90, 30, 70]
    saidai, bango = 0, 0
    for i in range(1, len(Tokuten) + 1):
        if Tokuten[i - 1] > saidai:
            saidai, bango = Tokuten[i - 1], i
    assert (saidai, bango) == (90, 3)
    # 類題103: (05) を (03) と揃える = dan のループの中 → 9 回
    Kuku = [[0] * 10 for _ in range(10)]
    lines = 0
    for dan in range(1, 10):
        for kazu in range(1, 10):
            Kuku[dan][kazu] = dan * kazu
        lines += 1
    assert lines == 9 and Kuku[7][9] == 63
    # 類題104
    assert 3.14 * 5.0 * 5.0 == 78.5
    # 練習105
    assert ['Yes' if v % 2 == 0 else 'No' for v in (4, 7)] == ['Yes', 'No']
    assert (123 % 10) * 100 + ((123 % 100) // 10) * 10 + 123 // 100 == 321
    assert sum(range(1, 5 + 1)) == 15
    assert [i for i in range(1, 12 + 1) if 12 % i == 0] == [1, 2, 3, 4, 6, 12]
    assert list(range(1, 6)) == list(range(1, 6, 1))
    # 練習106
    def coins(x):
        n50 = x // 50
        n10 = (x - n50 * 50) // 10
        n1 = x - n50 * 50 - n10 * 10
        return n50, n10, n1, n50 + n10 + n1
    assert coins(347) == (6, 4, 7, 17)
    assert 347 - 6 * 50 == 47 and 47 - 4 * 10 == 7
    assert 347 % 10 == 7          # (03) は num1 = x % 10 でも同じ


def main():
    selfcheck()
    html = SRC.read_text(encoding="utf-8")

    def sub1(pattern, repl, text, flags=0, label=""):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        assert n == 1, "置換に失敗(%d 件): %s" % (n, label or pattern)
        return new

    html = sub1(r"<title>.*?</title>",
                "<title>プログラミング | Practice Lab</title>", html, 0, "title")
    html = sub1(r'<span class="tg">CHAPTER 2\.06</span>',
                '<span class="tg">CHAPTER 4.12</span>', html, 0, "chapter tag")
    html = sub1(r'<span class="sb-score" id="sb-score">—/6</span>',
                '<span class="sb-score" id="sb-score">—/8</span>', html, 0, "sb-score")

    html = sub1(r'(<main id="stages">\n).*?(\n</main>)',
                lambda m: m.group(1) + STAGES.rstrip("\n") + m.group(2),
                html, re.S, "stages")

    html = sub1(r"  const TIMELINE_ENTRIES = \[.*?\n  \];",
                lambda m: TIMELINE, html, re.S, "TIMELINE_ENTRIES")
    html = sub1(r"  const PROBLEMS = \[.*?\n  \];",
                lambda m: PROBLEMS, html, re.S, "PROBLEMS")

    html = sub1(r"sbScore\.textContent = full \+ '/14';",
                "sbScore.textContent = full + '/8';", html, 0, "sb score denom")
    html = sub1(r"animateCounter\(grade, 0, fullCount, 1100, '<span class=\"denom\">/14</span>'\);",
                "animateCounter(grade, 0, fullCount, 1100, '<span class=\"denom\">/8</span>');",
                html, 0, "grade denom")
    html = sub1(r"if \(fullCount >= 11\) grade\.classList\.add\('s-high'\);\n"
                r"    else if \(fullCount >= 7\) grade\.classList\.add\('s-mid'\);",
                "if (fullCount >= 7) grade.classList.add('s-high');\n"
                "    else if (fullCount >= 4) grade.classList.add('s-mid');",
                html, 0, "thresholds")

    # --- 自己点検 ---------------------------------------------------------
    assert "，" not in STAGES, "全角カンマが残っている"
    # エンジンの JS フックが残っていること(components.md §6.4)
    for hook in ["isInsideHorizontalScroll", "function haptic", "function animateCounter",
                 "SPOT_SELECTOR", "spotlight-backdrop", "carousel-dots", "three-col",
                 "touch-action: manipulation"]:
        assert hook in html, "エンジンのフックが消えた: %s" % hook
    # ステージ数と problem-id の整合
    nstage = len(re.findall(r'<section class="stage[^"]*" data-stage-name=', html))
    assert nstage == 16, "ステージ数: %d" % nstage
    pids = re.findall(r"stageIdx: (\d+)", html)
    assert [int(x) for x in pids] == list(range(7, 15)), "PROBLEMS の stageIdx がずれている"
    # 原本の図がすべて参照されていること
    for k in range(1, 6):
        assert 'assets/fig%d-' % k in html, "図 %d が載っていない" % k
    # digest-mod が兄弟関係(SKILL.md §9.1 の入れ子バグ)
    assert html.count('class="digest-mod') == 6, "おさらいのモジュール数"
    # 答えが問題側に漏れていないこと(feedback の外に正答が出ていない)
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT, len(html), "bytes")
    print("  ステージ:", nstage, "(Welcome + おさらい + 例題5 + 練習8 + 結果)")
    print("  原本の図: 5 枚")


if __name__ == "__main__":
    main()
