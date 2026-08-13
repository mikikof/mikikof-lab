#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
practices 03-08「ハードウェアとソフトウェア」ビルダ

- エンジン(CSS / JS ハーネス / サイドバー / トップバー / フッタ)は
  examples/02-07-digital-info-representation.html を 1 文字も変えずに流用する。
- 差し替えるのは <main id="stages"> の中身と、JS の TIMELINE_ENTRIES / PROBLEMS /
  サマリ分母・閾値 だけ。
- 問題文・選択肢・解答・原本解説は _source の docx から逐語(「，」→「、」のみ)。
"""
import re
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PRACTICES = HERE.parent.parent
SRC = PRACTICES / "skills/interactive-practice/examples/02-07-digital-info-representation.html"
OUT = HERE / "index.html"

# ============================================================
# 共通パーツ
# ============================================================

def figure(src, alt, caption, fw=360, iw=320):
    return (
        '<figure style="margin: 0.85rem auto 0.2rem; padding: 0.8rem 1rem; background: var(--bg-card); '
        'border: 1px solid var(--line); border-radius: 8px; display: block; max-width: %dpx; text-align: center;">\n'
        '  <img src="%s" alt="%s" style="display: block; width: 100%%; height: auto; max-width: %dpx; margin: 0 auto;">\n'
        '  <figcaption style="margin-top: 0.5rem; font-family: var(--f-mono); font-size: 0.74rem; color: var(--ink-mute); line-height: 1.6;">%s</figcaption>\n'
        '</figure>\n' % (fw, src, alt, iw, caption)
    )


def quote_box(inner):
    return (
        '<div style="margin: 0.7rem 0 1.1rem; padding: 0.95rem 1.1rem; background: var(--bg-soft); '
        'border-left: 4px solid var(--action-pale2); border-radius: 0 8px 8px 0; '
        'font-family: var(--f-jp-body); font-size: 0.95rem; line-height: 2.05; color: var(--ink);">\n%s</div>\n' % inner
    )


def legend(items):
    rows = "".join(
        '      <span class="option-legend-item"><span class="let">(%s)</span>%s</span>\n' % (l, t)
        for l, t in items
    )
    return (
        '<div class="option-legend">\n'
        '  <div class="option-legend-title">選択肢</div>\n'
        '  <div class="option-legend-list">\n%s'
        '  </div>\n'
        '</div>\n' % rows
    )


def opts_single(prob_id, correct, items):
    body = "".join(
        '  <label class="opt"><input type="radio" name="%s"><span class="opt-mark"></span>'
        '<span class="opt-text"><span class="opt-letter">(%s)</span>%s</span></label>\n' % (prob_id, l, t)
        for l, t in items
    )
    return '<div class="opts" data-input="single" data-correct="%d">\n%s</div>\n' % (correct, body)


def ox_list(correct, items):
    rows = ""
    for i, (lbl, text) in enumerate(items):
        rows += (
            '  <div class="ox-row" data-sub="%d">\n'
            '    <span class="ox-sub-label">%s</span>\n'
            '    <span class="ox-text">%s</span>\n'
            '    <div class="ox-buttons"><button class="ox-btn maru" data-val="o">○</button>'
            '<button class="ox-btn batsu" data-val="x">×</button></div>\n'
            '  </div>\n' % (i, lbl, text)
        )
    return '<div class="ox-list" data-input="ox" data-correct="%s">\n%s</div>\n' % (correct, rows)


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


def mps_list(options, correct, items):
    rows = ""
    for i, (lbl, text) in enumerate(items):
        rows += (
            '  <div class="mps-row" data-sub="%d">\n'
            '    <span class="match-sub-label">%s</span>\n'
            '    <div class="sub-content">\n'
            '      <span class="mps-text">%s</span>\n'
            '      <div class="match-pills"></div>\n'
            '    </div>\n'
            '  </div>\n' % (i, lbl, text)
        )
    return ('<div class="mps-list" data-input="multi_per_sub" data-options="%s" data-correct="%s">\n%s</div>\n'
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
        '<div class="desc">%s</div></div>\n' % (k, b, d) for k, b, d in cards
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


def indent(text, n):
    if not text:
        return ""
    pad = " " * n
    return "".join(pad + line if line.strip() else line for line in text.splitlines(True))


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


# ============================================================
# STAGE 0 — WELCOME
# ============================================================
WELCOME = """  <section class="stage active" data-stage-name="START">
    <div class="welcome-kicker">
      <span class="num">03</span>
      <span>3章 第8節</span>
    </div>
    <h1 class="welcome-title-en">Hardware<br>&amp; Software<span class="accent">.</span></h1>
    <h2 class="welcome-title-jp">ハードウェアとソフトウェア</h2>
    <p class="welcome-lede">
      コンピュータを構成する五つの装置と、それを動かすソフトウェアの種類を確認します。オペレーティングシステム、アプリケーションソフトウェア、デバイスドライバ、そして機器どうしをつなぐインタフェースまでを扱います。装置の違いをどの層が引き受けているのかを、例題と練習で確かめます。
    </p>
    <div class="welcome-meta">
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">examples</div>
        <div class="welcome-meta-value">4<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">practice</div>
        <div class="welcome-meta-value">7<span class="unit">問</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">est. time</div>
        <div class="welcome-meta-value">35<span class="unit">分</span></div>
      </div>
      <div class="welcome-meta-item">
        <div class="welcome-meta-label">source</div>
        <div class="welcome-meta-value" style="font-size: 0.95rem;">ベストフィット<br><span class="unit" style="margin-left:0;">3章08</span></div>
      </div>
    </div>
    <div class="flow-strip">
      <div class="flow-strip-title">本セットの流れ</div>
      <div class="flow-list">
        <div class="flow-item"><span class="flow-num">1</span><div><strong>おさらい</strong>ー この節の基本知識を、Q&amp;A形式の6モジュールで確認します(タップで展開)</div></div>
        <div class="flow-item"><span class="flow-num">2</span><div><strong>例題ツアー</strong>ー 例題39〜42の解き方を4問たどります(採点なし)</div></div>
        <div class="flow-item"><span class="flow-num">3</span><div><strong>演習</strong>ー 類題68〜71・練習72〜74の計7問。回答 → 採点 → 解説</div></div>
        <div class="flow-item"><span class="flow-num">4</span><div><strong>結果</strong>ー 完答数と、間違えた問題の再確認</div></div>
      </div>
    </div>
  </section>
"""

# ============================================================
# STAGE 1 — REVIEW (Q&A 6 modules)
# ============================================================

FAMILY_TREE = """<div class="viz">
  <span class="viz-label">THE BIG MAP — コンピュータの中身</span>
  <div class="viz-caption">コンピュータは、物理的な装置(ハードウェア)と、それを動かすプログラム(ソフトウェア)でできています。</div>
  <div class="family-tree-wrap">
    <svg class="family-tree-svg" viewBox="0 0 740 372" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="コンピュータがハードウェア(入力装置・出力装置・記憶装置・演算装置・制御装置)とソフトウェア(オペレーティングシステム・アプリケーションソフトウェア・デバイスドライバ)に分かれる地図">
      <rect x="4" y="158" width="104" height="48" rx="12" fill="#122E55"/>
      <text x="56" y="188" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">コンピュータ</text>
      <line x1="108" y1="182" x2="124" y2="182" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="124" y1="90" x2="124" y2="272" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="124" y1="90" x2="140" y2="90" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="124" y1="272" x2="140" y2="272" stroke="#B8C5D7" stroke-width="1.5"/>

      <rect x="140" y="68" width="120" height="44" rx="10" fill="#4A78C8"/>
      <text x="200" y="96" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">ハードウェア</text>
      <line x1="260" y1="90" x2="280" y2="90" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="51" x2="280" y2="129" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="51" x2="300" y2="51" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="129" x2="292" y2="129" stroke="#B8C5D7" stroke-width="1.5"/>

      <rect x="300" y="32" width="104" height="38" rx="9" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="352" y="56" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">入力装置</text>
      <rect x="414" y="32" width="104" height="38" rx="9" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="466" y="56" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">出力装置</text>
      <rect x="528" y="32" width="104" height="38" rx="9" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="580" y="56" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">記憶装置</text>

      <rect x="292" y="100" width="240" height="58" rx="12" fill="none" stroke="#B85975" stroke-width="1.5" stroke-dasharray="5 4"/>
      <rect x="304" y="110" width="104" height="38" rx="9" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="356" y="134" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">演算装置</text>
      <rect x="416" y="110" width="104" height="38" rx="9" fill="#FAFCFF" stroke="#4A78C8" stroke-width="1.5"/>
      <text x="468" y="134" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">制御装置</text>
      <text x="542" y="134" font-family="'Zen Kaku Gothic New',sans-serif" font-size="13" font-weight="700" fill="#B85975">＝ CPU(中央処理装置)</text>

      <rect x="140" y="250" width="120" height="44" rx="10" fill="#2A4A78"/>
      <text x="200" y="278" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">ソフトウェア</text>
      <line x1="260" y1="272" x2="280" y2="272" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="209" x2="280" y2="333" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="209" x2="300" y2="209" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="271" x2="300" y2="271" stroke="#B8C5D7" stroke-width="1.5"/>
      <line x1="280" y1="333" x2="300" y2="333" stroke="#B8C5D7" stroke-width="1.5"/>

      <rect x="300" y="190" width="232" height="38" rx="9" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="416" y="214" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">オペレーティングシステム</text>
      <text x="544" y="215" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" fill="#75839B">基本ソフトウェア</text>

      <rect x="300" y="252" width="252" height="38" rx="9" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="426" y="276" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">アプリケーションソフトウェア</text>
      <text x="564" y="277" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" fill="#75839B">応用ソフトウェア</text>

      <rect x="300" y="314" width="176" height="38" rx="9" fill="#FAFCFF" stroke="#2A4A78" stroke-width="1.5"/>
      <text x="388" y="338" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="500" fill="#1A2B47">デバイスドライバ</text>
      <text x="488" y="339" font-family="'Zen Kaku Gothic New',sans-serif" font-size="12" fill="#75839B">周辺機器を OS が制御するための</text>
    </svg>
  </div>
</div>
"""

REVIEW_MODS = [
    digest_mod(
        "01", "The Big Map",
        '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><line x1="7" y1="11" x2="17" y2="7"/><line x1="7" y1="13" x2="17" y2="17"/>',
        "コンピュータは、何と何でできていますか?",
        "ハードウェアとソフトウェア",
        "ハードウェアは、コンピュータを構成する装置の機能を実現する物理的な装置や部品です。ソフトウェアは、コンピュータを動作させるためのプログラムなどのことです。この節では、この二つに加えて、情報機器を相互に接続する規格であるインタフェースまでを扱います。",
        FAMILY_TREE, hero=True),

    digest_mod(
        "02", "Five Units",
        '<rect x="3" y="4" width="18" height="12" rx="2"/><line x1="8" y1="20" x2="16" y2="20"/><line x1="12" y1="16" x2="12" y2="20"/>',
        "五つの装置は、それぞれ何をしていますか?",
        "入力・出力・記憶・演算・制御",
        "ハードウェアの働きは五つに分けられます。このうち演算装置と制御装置を合わせて CPU といいます。",
        viz("FIVE UNITS — 装置の働きと例",
            "働きで五つに分け、CPU にあたる二つを押さえます。",
            bd_grid([
                ("入力装置", "入力", "データなどを入力する。<br><span style=\"color:var(--ink-mute)\">例　キーボード、マウス</span>"),
                ("出力装置", "出力", "処理結果などを表示する。<br><span style=\"color:var(--ink-mute)\">例　ディスプレイ、プリンタ</span>"),
                ("記憶装置", "記憶", "データや処理結果を記憶する。<br><span style=\"color:var(--ink-mute)\">例　メモリ、ハードディスク、SSD</span>"),
                ("演算装置", "CPU", "データを処理する。"),
                ("制御装置", "CPU", "各装置を制御する。"),
            ], warn="演算装置と制御装置を合わせ、CPU(中央処理装置)といいます。また記憶装置は、主記憶装置(メインメモリ)と補助記憶装置に分かれます。"))),

    digest_mod(
        "03", "Two Softwares",
        '<rect x="3" y="3" width="18" height="8" rx="2"/><rect x="3" y="13" width="18" height="8" rx="2"/>',
        "ソフトウェアは、どう分けられますか?",
        "オペレーティングシステムとアプリケーションソフトウェア",
        "土台になるのがオペレーティングシステム、その上で特定の作業を行うのがアプリケーションソフトウェアです。どちらも別名を持っているので、名前の対応まで覚えておきます。",
        viz("SOFTWARE — 二つの種類",
            "定義と別名を対にして押さえます。",
            compare2(
                ("オペレーティングシステム", [
                    ("定義", "コンピュータの基本的な管理・制御を行うソフトウェア"),
                    ("別名", "基本ソフトウェア"),
                    ("略称", "OS"),
                ]),
                ("アプリケーションソフトウェア", [
                    ("定義", "特定の作業を行うために使用されるソフトウェア"),
                    ("別名", "応用ソフトウェア"),
                    ("例", "表計算ソフトウェア、プレゼンテーションソフトウェア"),
                ])))),

    digest_mod(
        "04", "Device Driver",
        '<rect x="4" y="4" width="16" height="16" rx="2"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/>',
        "デバイスドライバは、何と何の間に立っていますか?",
        "オペレーティングシステムと周辺機器の間",
        "コンピュータの周辺機器をオペレーティングシステムが制御するためのソフトウェアが、デバイスドライバです。周辺機器そのものではなく、周辺機器を制御するためのソフトウェアである点に注意します。",
        viz("DEVICE DRIVER — 制御する側と、される側",
            "デバイスドライバは、OS が周辺機器を制御するために使うソフトウェアです。",
            """  <div class="lk-grid">
    <div class="lk-card locked">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>
        </svg>
      </div>
      <h5>オペレーティングシステム</h5>
      <span class="stamp">制御する側</span>
      <ul class="lk-list">
        <li><span>コンピュータの基本的な管理・制御を行う</span></li>
        <li><span>基本ソフトウェアともいう</span></li>
      </ul>
      <p class="lk-rules">周辺機器を制御するときは、<strong>デバイスドライバ</strong>を通します。</p>
    </div>
    <div class="lk-card transferable">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="4" y="9" width="16" height="9" rx="2"/><path d="M7 9V4h10v5"/><line x1="8" y1="14" x2="16" y2="14"/>
        </svg>
      </div>
      <h5>周辺機器</h5>
      <span class="stamp">制御される側</span>
      <ul class="lk-list">
        <li><span>プリンタ</span></li>
        <li><span>キーボード</span></li>
        <li><span>ハードディスク</span></li>
      </ul>
      <p class="lk-rules">コンピュータの核となる部分に接続し、データの記憶や入出力を行います。</p>
    </div>
  </div>
""")),

    digest_mod(
        "05", "Interfaces",
        '<path d="M9 2v6"/><path d="M15 2v6"/><rect x="6" y="8" width="12" height="7" rx="2"/><path d="M12 15v7"/>',
        "どの規格が、どの機器をつなぎますか?",
        "インタフェース 早見",
        "インタフェースは、コンピュータなどの情報機器を相互に接続する規格です。名前と接続先の組合せで覚えます。",
        viz("INTERFACE — 規格と接続する機器",
            "規格名から接続先を、接続先から規格名を、どちらの向きでも出せるようにします。",
            bd_grid([
                ("USB", "周辺機器", "プリンタ、キーボード、ハードディスクなどの周辺機器"),
                ("HDMI", "映像・音声", "デジタルテレビ、オーディオ機器など"),
                ("イーサネット", "有線", "ハブ、ルータなどの有線接続の通信機器"),
                ("Bluetooth", "無線", "スピーカやマウス、キーボードなどの機器を無線接続する。"),
                ("IEEE 802.11", "無線", "スマートフォンやスマート家電など、無線通信する機器"),
            ]))),

    digest_mod(
        "06", "Who Absorbs It",
        '<circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/>',
        "装置の違いを意識せずに使えるのは、どの層の仕事ですか?",
        "仕様を合わせるのがハードウェアインタフェース、操作の内容を抽象化するのが OS",
        "どちらも「違いを吸収している」と読めるので、混同しやすいところです。ハードウェアインタフェースは機器どうしの仕様をそろえる話、オペレーティングシステムの基本機能の提供は操作の内容を抽象化する話です。並べて確認します。",
        viz("LAYERS — 学習ノート POINT 14",
            "同じ「違いを吸収する」でも、仕事の中身が違います。",
            compare2(
                ("ハードウェアインタフェース", [
                    ("すること", "機器どうしを接続するコネクタの形状や電気信号の形式などの仕様を合わせる"),
                    ("何の話か", "ハードウェアのインタフェースの標準化"),
                    ("OS の目的か", "目的ではない"),
                ]),
                ("オペレーティングシステム", [
                    ("すること", "装置の違いを意識せず利用できるよう操作の内容を抽象化する"),
                    ("何の話か", "基本機能の提供"),
                    ("OS の目的か", "目的の一つ"),
                ]))
            + checklist([
                ("①", "操作支援", "操作の一部を肩代わりしユーザの作業を支援する"),
                ("②", "基本機能の提供", "装置の違いを意識せず利用できるよう操作の内容を抽象化する"),
                ("③", "資源の有効利用", "限られたコンピュータ資源を有効に活用し適切に管理する"),
            ], warn="学習ノート 実習2 より — <strong>基本ソフトウェアに周辺機器を動作させるためのデバイスドライバというプログラムを追加することで、応用ソフトウェアは周辺機器の違いをほとんど意識することなく作業ができる。</strong>"))),
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
# STAGE 2 — 例題39
# ============================================================
EX39_TREE = """  <div class="right-tree">
    <div class="rt-row heading"><span class="rt-bracket">┃</span><span class="rt-name">五つの装置</span><span class="rt-note">図の①〜⑤との対応</span></div>
    <div class="rt-row indent"><span class="rt-bracket">├</span><span class="rt-name">CPU <span class="pill dim">②③</span></span><span class="rt-note">制御装置と演算装置を合わせたもの。中央処理装置ともいう</span></div>
    <div class="rt-row indent2"><span class="rt-bracket">├</span><span class="rt-name small">制御装置 <span class="pill">②</span></span><span class="rt-note">ほかの四つの装置へ命令を送り、制御する</span></div>
    <div class="rt-row indent2"><span class="rt-bracket">└</span><span class="rt-name small">演算装置 <span class="pill">③</span></span><span class="rt-note">演算命令に従ってデータを処理する</span></div>
    <div class="rt-row indent"><span class="rt-bracket">├</span><span class="rt-name">記憶装置 <span class="pill">④</span></span><span class="rt-note">データはすべてここを経由して流れる</span></div>
    <div class="rt-row indent"><span class="rt-bracket">├</span><span class="rt-name">入力装置 <span class="pill">①</span></span><span class="rt-note">入力命令を受け、データを記憶装置へ送る</span></div>
    <div class="rt-row indent"><span class="rt-bracket">└</span><span class="rt-name">出力装置 <span class="pill">⑤</span></span><span class="rt-note">出力命令を受け、記憶装置からデータを受け取る</span></div>
  </div>
"""

EX39 = stage_example(
    1, 4, "39", "ベストフィット 例題39", "コンピュータの構成", "ex39",
    '<span class="problem-tag match">MATCH</span>',
    "コンピュータの構成は右の図のようになる。図の①～⑤に適当な装置名を(ア)～(オ)からそれぞれ選べ。",
    figure("assets/fig1-computer-structure.jpeg",
           "図: コンピュータの構成。CPU の中に②と③があり、①・④・⑤との間を入力命令・演算命令・転送命令・出力命令とデータの流れが結んでいる",
           "図: コンピュータの構成", 560, 520),
    legend([("ア", "演算装置"), ("イ", "出力装置"), ("ウ", "記憶装置"), ("エ", "入力装置"), ("オ", "制御装置")])
    + match_list("ア,イ,ウ,エ,オ", "3,4,0,2,1",
                 [("①", "図の①"), ("②", "図の②"), ("③", "図の③"), ("④", "図の④"), ("⑤", "図の⑤")]),
    feedback("正答: ① (エ)　② (オ)　③ (ア)　④ (ウ)　⑤ (イ)", [
        fb_section("ベストフィット", bestfit("制御装置と演算装置を合わせ、CPU(中央処理装置)という。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>②</strong>　ほかの四つの装置へ命令を送り、制御するのが制御装置である。</li>"
            "<li><strong>④</strong>　データはすべて記憶装置を経由して流れている。</li></ul>")),
        fb_section("残りの三つの決め手(補足)", explain(
            "<p>①は入力命令を受け取り、④へデータを送る側にあります。データがコンピュータへ入ってくる側なので入力装置です。"
            "⑤は④からデータを受け取り、出力命令を受けています。処理の結果が出ていく側なので出力装置です。"
            "③は②から演算命令を受け、④との間でデータをやり取りしています。データを処理する装置なので演算装置です。</p>")),
        '    ' + figure("assets/fig2-data-and-control-flow.jpeg",
                        "図　データと制御の流れ。CPU の中に制御装置と演算装置があり、入力装置・記憶装置・出力装置との間をデータの流れと制御の流れが結んでいる",
                        "図　データと制御の流れ(装置名を入れたもの)", 560, 520),
        viz("STRUCTURE — 五つの装置と ①〜⑤", "装置名を入れると、図の四つの命令がそのまま働きの説明になります。", EX39_TREE),
    ], example=True))

# ============================================================
# STAGE 3 — 例題40
# ============================================================
EX40 = stage_example(
    2, 4, "40", "ベストフィット 例題40", "ソフトウェア", "ex40",
    '<span class="problem-tag multi">MULTI × 2</span>',
    "次の(ア)～(オ)の記述のうち、⑴オペレーティングシステム、⑵アプリケーションソフトウェアのそれぞれに関する説明に該当するものをすべて選べ。",
    "",
    legend([("ア", "特定の作業を行うために使用されるソフトウェアである。"),
            ("イ", "コンピュータを構成する装置の機能を実現する装置である。"),
            ("ウ", "コンピュータの基本的な管理・制御を行うソフトウェアである。"),
            ("エ", "表計算ソフトウェアやプレゼンテーションソフトウェアなどが含まれる。"),
            ("オ", "基本ソフトウェアともいう。")])
    + '<div class="multi-hint">各小問とも、該当するものをすべて選びます</div>\n'
    + mps_list("ア,イ,ウ,エ,オ", "2,4|0,3",
               [("⑴", "オペレーティングシステム"), ("⑵", "アプリケーションソフトウェア")]),
    feedback("正答: ⑴ (ウ)、(オ)　⑵ (ア)、(エ)", [
        fb_section("ベストフィット", bestfit(
            "オペレーティングシステム(OS)は、コンピュータの基本的な管理・制御(オペレーション)を行っている。"
            "アプリケーションソフトウェアは、OSが提供する機能を利用して動作する。")),
        fb_section("解説(原本)", explain("<p>(イ)は、ハードウェアの説明である。</p>")),
        fb_section("選択肢の見分け方(補足)", explain(
            "<p>(ウ)は確認事項のオペレーティングシステムの定義そのもの、(オ)はその別名です。"
            "(ア)は確認事項のアプリケーションソフトウェアの定義そのもの、(エ)はその具体例にあたります。"
            "(イ)だけが「装置」で終わっており、ソフトウェアの説明になっていません。</p>")),
        viz("SOFTWARE — 記述の振り分け", "定義・別名・例のどれにあたるかで振り分けます。",
            compare2(
                ("⑴ オペレーティングシステム", [
                    ("(ウ)", "コンピュータの基本的な管理・制御を行うソフトウェアである。 — 定義"),
                    ("(オ)", "基本ソフトウェアともいう。 — 別名"),
                ]),
                ("⑵ アプリケーションソフトウェア", [
                    ("(ア)", "特定の作業を行うために使用されるソフトウェアである。 — 定義"),
                    ("(エ)", "表計算ソフトウェアやプレゼンテーションソフトウェアなどが含まれる。 — 例"),
                ]))
            + '  <div class="bd-warn"><strong>(イ)</strong> コンピュータを構成する装置の機能を実現する装置である。 — これはハードウェアの説明で、どちらにも入りません。</div>\n'),
    ], example=True))

# ============================================================
# STAGE 4 — 例題41
# ============================================================
EX41_CARDS = """  <div class="ip-rich-grid">
    <div class="ip-rich patent">
      <div class="ip-rich-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M4 19h16"/></svg>
      </div>
      <div class="ip-rich-name">インストーラ</div>
      <div class="ip-rich-period">(ア)</div>
      <div class="ip-rich-desc">アプリケーションソフトウェアをコンピュータにインストールするソフトウェアである。</div>
    </div>
    <div class="ip-rich trademark">
      <div class="ip-rich-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 2 20h20L12 3z"/><line x1="12" y1="10" x2="12" y2="14"/><line x1="12" y1="17" x2="12" y2="17"/></svg>
      </div>
      <div class="ip-rich-name">マルウェア</div>
      <div class="ip-rich-period">(イ)</div>
      <div class="ip-rich-desc">コンピュータに入り込んで不利益をもたらすソフトウェアである。</div>
    </div>
    <div class="ip-rich design">
      <div class="ip-rich-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 4v4"/><circle cx="9" cy="14" r="1"/><circle cx="15" cy="14" r="1"/></svg>
      </div>
      <div class="ip-rich-name">RPA・マクロ</div>
      <div class="ip-rich-period">(エ)</div>
      <div class="ip-rich-desc">キーボードなどの操作手順を登録し、操作を自動化するソフトウェアである。</div>
    </div>
    <div class="ip-rich utility">
      <div class="ip-rich-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="12" rx="2"/><path d="M3 13h18"/><path d="M12 9v12"/><path d="M12 9a3 3 0 1 0-3-3"/><path d="M12 9a3 3 0 1 1 3-3"/></svg>
      </div>
      <div class="ip-rich-name">フリーソフト</div>
      <div class="ip-rich-period">(オ)</div>
      <div class="ip-rich-desc">無償で配布され、利用者が自由に利用できるソフトウェアである。</div>
    </div>
  </div>
"""

EX41 = stage_example(
    3, 4, "41", "ベストフィット 例題41", "デバイスドライバ", "ex41",
    '<span class="problem-tag">SINGLE</span>',
    "次の(ア)～(オ)の記述のうち、デバイスドライバの説明に該当するものを一つ選べ。",
    "",
    opts_single("ex41", 2, [
        ("ア", "アプリケーションソフトウェアをコンピュータにインストールするソフトウェアである。"),
        ("イ", "コンピュータに入り込んで不利益をもたらすソフトウェアである。"),
        ("ウ", "コンピュータに接続された周辺機器を制御するソフトウェアである。"),
        ("エ", "キーボードなどの操作手順を登録し、操作を自動化するソフトウェアである。"),
        ("オ", "無償で配布され、利用者が自由に利用できるソフトウェアである。"),
    ]),
    feedback("正答: (ウ)", [
        fb_section("ベストフィット", bestfit(
            "コンピュータの周辺機器をOSが制御するためのソフトウェアを、デバイスドライバという。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>(ア)</strong>　インストーラの説明である。</li>"
            "<li><strong>(イ)</strong>　マルウェアの説明である。</li>"
            "<li><strong>(エ)</strong>　RPA(Robotic Process Automationの略)やマクロなどの説明である。</li>"
            "<li><strong>(オ)</strong>　フリーソフトの説明である。</li></ul>")),
        fb_section("(ウ)を選ぶ手がかり(補足)", explain(
            "<p>五つとも「〜ソフトウェアである」で終わるので、語尾では区別がつきません。"
            "何を相手にしているかを見ます。(ウ)だけが<strong>コンピュータに接続された周辺機器</strong>を相手にしています。"
            "残りの四つは、ソフトウェアの導入・不利益・操作手順・配布のしかたの話です。</p>")),
        viz("DISTRACTORS — 残り四つは何の説明か", "(ウ)以外の四つは、それぞれ別のソフトウェアの説明です。", EX41_CARDS),
    ], example=True))

# ============================================================
# STAGE 5 — 例題42
# ============================================================
EX42 = stage_example(
    4, 4, "42", "ベストフィット 例題42", "インタフェース", "ex42",
    '<span class="problem-tag ox">○ × 判定</span>',
    "次の⑴～⑸の記述のうち、適当なものには○を、適当でないものには×を記せ。",
    "",
    ox_list("o,x,o,o,x", [
        ("⑴", "コンピュータなどの情報機器を相互に接続する規格をインタフェースという。"),
        ("⑵", "プリンタ、キーボードなどを接続するインタフェースは、HDMIである。"),
        ("⑶", "無線接続のできる通信機器を接続するインタフェースは、IEEE 802.11である。"),
        ("⑷", "USBインタフェースは、キーボードやハードディスクなど多くの機器を接続できる。"),
        ("⑸", "ハブ、ルータなどの有線接続の通信機器を接続する規格は、USBインタフェースである。"),
    ]),
    feedback("正答: ⑴ ○　⑵ ×　⑶ ○　⑷ ○　⑸ ×", [
        fb_section("ベストフィット", bestfit(
            "IEEE 802.11に準拠する通信機器について、その相互接続性を業界団体「Wi-Fi Alliance」が保証するブランドを「Wi-Fi」(ワイファイ)という。")),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑵</strong>　適当でない。HDMIは、デジタルテレビなどを接続し、映像や音声を1本のケーブルで送る通信規格である。</li>"
            "<li><strong>⑸</strong>　適当でない。ハブ、ルータなどの有線接続の通信機器を接続する規格は、イーサネットである。</li></ul>")),
        fb_section("○ になる三つ(補足)", explain(
            "<p>⑴は確認事項のインタフェースの定義そのままです。"
            "⑶は IEEE 802.11 の接続先(無線通信する機器)と一致します。"
            "⑷は USB の接続先(プリンタ、キーボード、ハードディスクなどの周辺機器)と一致します。"
            "×になる二つは、どちらも規格の取り違えです。</p>")),
        viz("CHECK — ⑴〜⑸ の判定", "誤りは「規格名と接続先の組合せ」が入れ替わっているところに出ます。",
            checklist([
                ("⑴", "○", "インタフェースの定義。確認事項どおり。"),
                ("⑵", "×", "プリンタ、キーボードを接続するのは USB。HDMI はデジタルテレビ、オーディオ機器など。"),
                ("⑶", "○", "IEEE 802.11 はスマートフォンやスマート家電など、無線通信する機器の規格。"),
                ("⑷", "○", "USB はプリンタ、キーボード、ハードディスクなどの周辺機器を接続する。"),
                ("⑸", "×", "ハブ、ルータなどの有線接続の通信機器を接続する規格はイーサネット。"),
            ])),
    ], example=True))

# ============================================================
# STAGE 6 — 練習1 / 類題68
# ============================================================
P68 = stage_practice(
    1, 7, "68", "ベストフィット 類題68", "〈コンピュータの構成〉", "p1",
    '<span class="problem-tag">SINGLE</span>',
    "コンピュータの構成を表す左下の図の①～③に入れるべき適当な語句の組合せを、右下の表の(ア)～(エ)から一つずつ選べ。",
    figure("assets/fig3-structure-with-aux-storage.jpeg",
           "図: コンピュータの構成。①から補助記憶装置・②・③・出力装置へ制御の流れが伸び、入力装置・③・出力装置・補助記憶装置の間をデータの流れが結んでいる",
           "図: コンピュータの構成", 520, 480),
    opts_single("p68", 2, [
        ("ア", "①&nbsp;制御装置　②&nbsp;主記憶装置　③&nbsp;演算装置"),
        ("イ", "①&nbsp;主記憶装置　②&nbsp;演算装置　③&nbsp;制御装置"),
        ("ウ", "①&nbsp;制御装置　②&nbsp;演算装置　③&nbsp;主記憶装置"),
        ("エ", "①&nbsp;演算装置　②&nbsp;制御装置　③&nbsp;主記憶装置"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">(ウ)</div>'),
        fb_section("解説(原本)", explain(
            "<p>まず、制御装置を特定する。制御命令は制御装置からのみ送られており、制御の流れの源である①が制御装置であると特定できる。"
            "また、補助記憶装置とデータのやり取りをするのは主記憶装置のみである。そこで③が主記憶装置であると特定できる。</p>")),
        fb_section("②が決まる順序(補足)", explain(
            "<p>①と③が決まると、残る②は演算装置に決まります。図から二つを確定させ、最後の一つは消去法で置く、という順序です。"
            "選択肢は四つとも三つの装置名の並べ替えなので、一つでも確実に決められれば候補は大きく減ります。</p>")),
        viz("READING THE FIGURE — 二つの決め手", "図の中の「流れ」を二種類に分けて読みます。",
            compare2(
                ("①の決め手 — 制御の流れ", [
                    ("見るもの", "制御の流れ(実線の矢印)がどこから出ているか"),
                    ("読み方", "制御命令は制御装置からのみ送られる"),
                    ("結論", "制御の流れの源である①が制御装置"),
                ]),
                ("③の決め手 — データの流れ", [
                    ("見るもの", "補助記憶装置とデータをやり取りしているのはどれか"),
                    ("読み方", "補助記憶装置とデータのやり取りをするのは主記憶装置のみ"),
                    ("結論", "③が主記憶装置"),
                ]))),
    ]))

# ============================================================
# STAGE 7 — 練習2 / 類題69
# ============================================================
P69_LK = """  <div class="lk-grid">
    <div class="lk-card locked">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 14V9a5 5 0 0 1 10 0v5"/></svg>
      </div>
      <h5>オペレーティングシステム</h5>
      <span class="stamp">⑴ ⑶ ⑷</span>
      <ul class="lk-list">
        <li><span>コンピュータの基本的な管理・制御を行うソフトウェアである。</span></li>
        <li><span>基本ソフトウェアとも呼ばれる。</span></li>
        <li><span>オペレーティングシステムとも呼ばれる。</span></li>
      </ul>
      <p class="lk-rules">この三つは<strong>アプリケーションソフトウェアの説明ではない</strong>ので、×になります。</p>
    </div>
    <div class="lk-card transferable">
      <div class="lk-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
      </div>
      <h5>アプリケーションソフトウェア</h5>
      <span class="stamp">⑵ ⑸</span>
      <ul class="lk-list">
        <li><span>特定の作業を行うために使用されるソフトウェアである。</span></li>
        <li><span>表計算やプレゼンテーションソフトウェアなどが含まれる。</span></li>
      </ul>
      <p class="lk-rules">定義と具体例。この二つが<strong>○</strong>です。</p>
    </div>
  </div>
"""

P69 = stage_practice(
    2, 7, "69", "ベストフィット 類題69", "〈ソフトウェア〉", "p2",
    '<span class="problem-tag ox">○ × 判定</span>',
    "次の⑴～⑸の記述のうち、アプリケーションソフトウェアの説明として適当なものには○を、適当でないものには×を記せ。",
    "",
    ox_list("x,o,x,x,o", [
        ("⑴", "コンピュータの基本的な管理・制御を行うソフトウェアである。"),
        ("⑵", "特定の作業を行うために使用されるソフトウェアである。"),
        ("⑶", "基本ソフトウェアとも呼ばれる。"),
        ("⑷", "オペレーティングシステムとも呼ばれる。"),
        ("⑸", "表計算やプレゼンテーションソフトウェアなどが含まれる。"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ ×　⑵ ○　⑶ ×　⑷ ×　⑸ ○</div>'),
        fb_section("解説(原本)", explain(
            "<p>コンピュータの基本的な管理・制御は、基本ソフトウェア(OS)が担う。</p>")),
        fb_section("⑶⑷ が × になる理由(補足)", explain(
            "<p>⑶の基本ソフトウェアはオペレーティングシステムの別名です。⑷はその名前そのものです。"
            "アプリケーションソフトウェアの別名は応用ソフトウェアなので、⑶⑷はどちらも別のソフトウェアを指しています。"
            "○になるのは、定義にあたる⑵と、具体例にあたる⑸の二つです。</p>")),
        viz("SORTING — どちらの説明か", "五つの記述を、二種類のソフトウェアに振り分けます。", P69_LK),
    ]))

# ============================================================
# STAGE 8 — 練習3 / 類題70
# ============================================================
P70 = stage_practice(
    3, 7, "70", "ベストフィット 類題70", "〈デバイスドライバ〉", "p3",
    '<span class="problem-tag ox">○ × 判定</span>',
    "次の⑴～⑷の記述のうち、デバイスドライバの説明として適当なものには○を、適当でないものには×を記せ。",
    "",
    ox_list("o,x,x,o", [
        ("⑴", "OSと周辺機器の仲立ちをし、メーカや機種の違いによる機器の制御方法の差を吸収する。"),
        ("⑵", "キーボードやマウスなどの入力用のデバイスでは、デバイスドライバは不要である。"),
        ("⑶", "プリンタなどの出力用のデバイスでは、メーカでの違いがない共通のデバイスドライバを用いる。"),
        ("⑷", "OSには多くの一般的なデバイスドライバが用意されているので、デバイスをコンピュータに接続するだけで、自動的に適切なものがインストールされる。"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ ○　⑵ ×　⑶ ×　⑷ ○</div>'),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑵</strong>　適当でない。すべてのデバイスごとにデバイスドライバが必要である。</li>"
            "<li><strong>⑶</strong>　適当でない。プリンタなどの同じ種類のデバイスでも、機種ごとにデバイスドライバが必要である。</li></ul>")),
        fb_section("⑴⑷ が ○ になる理由(補足)", explain(
            "<p>⑴は確認事項の「コンピュータの周辺機器をオペレーティングシステムが制御するためのソフトウェア」を、"
            "仲立ちという言い方で述べたものです。⑷は⑵⑶と合わせて読みます。"
            "デバイスごとに必要であることと、OS があらかじめ多くを用意していることは両立します。</p>")),
        viz("FOUR STATEMENTS — ○ と × の分かれ目", "「一つで足りるか、機器ごとに要るか」で二つが×になります。",
            bd_grid([
                ("⑴", "○", "OSと周辺機器の仲立ちをし、機器の制御方法の差を吸収する。確認事項の定義どおり。"),
                ("⑵", "×", "すべてのデバイスごとにデバイスドライバが必要である。"),
                ("⑶", "×", "同じ種類のデバイスでも、機種ごとにデバイスドライバが必要である。"),
                ("⑷", "○", "OSには多くの一般的なデバイスドライバが用意されている。"),
            ])),
    ]))

# ============================================================
# STAGE 9 — 練習4 / 類題71
# ============================================================
P71 = stage_practice(
    4, 7, "71", "ベストフィット 類題71", "〈インタフェース〉", "p4",
    '<span class="problem-tag self">記述・自己採点</span>',
    "次の⑴～⑸が説明するインタフェースは何か答えよ。",
    "",
    self_list([
        ("⑴", "IEEEで最初に規格統一された無線LAN規格である。",
         "<p><strong>IEEE 802.11</strong><br>スマートフォンやスマート家電など、無線通信する機器を接続する規格です。</p>"),
        ("⑵", "映像や音声などを1本のケーブルにまとめてデジタル信号で送ることができる規格であり、多くの映像機器で使われる。",
         "<p><strong>HDMI</strong><br>デジタルテレビ、オーディオ機器などを接続する規格です。</p>"),
        ("⑶", "パソコンの周辺機器で、最も普及した汎用インタフェース規格である。",
         "<p><strong>USB</strong><br>プリンタ、キーボード、ハードディスクなどの周辺機器を接続する規格です。</p>"),
        ("⑷", "家庭や企業などで使われる有線ネットワークの主流な規格である。",
         "<p><strong>イーサネット</strong><br>ハブ、ルータなどの有線接続の通信機器を接続する規格です。</p>"),
        ("⑸", "デジタル機器間の近距離データ通信に使う無線通信規格の一つで、マウスやワイヤレスイヤホンなど、多くのデジタル機器で使われる。",
         "<p><strong>Bluetooth</strong><br>スピーカやマウス、キーボードなどの機器を無線接続する規格です。</p>"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ IEEE 802.11　⑵ HDMI　⑶ USB　⑷ イーサネット　⑸ Bluetooth</div>'),
        fb_section("解説(原本)", explain(
            "<p>IEEEはInstitute of Electrical and Electronics Engineers(米国電気電子学会)の略称、"
            "HDMIはHigh-Definition Multimedia Interface(高精細度マルチメディアインタフェース)の略称、"
            "USBはUniversal Serial Bus(ユニバーサルシリアルバス)の略称である。</p>")),
        fb_section("略称から意味を引く(補足)", explain(
            "<p>略称の元になった語がわかると、説明文と結びつけやすくなります。"
            "Multimedia は映像や音声、Universal Serial Bus の Universal は汎用、"
            "Institute of Electrical and Electronics Engineers は規格を定める学会です。</p>")),
        viz("INTERFACE — ⑴〜⑸ の対応", "説明文のどの語が決め手になったかを確かめます。",
            bd_grid([
                ("IEEE 802.11", "⑴", "スマートフォンやスマート家電など、無線通信する機器"),
                ("HDMI", "⑵", "デジタルテレビ、オーディオ機器など"),
                ("USB", "⑶", "プリンタ、キーボード、ハードディスクなどの周辺機器"),
                ("イーサネット", "⑷", "ハブ、ルータなどの有線接続の通信機器"),
                ("Bluetooth", "⑸", "スピーカやマウス、キーボードなどの機器を無線接続する。"),
            ])),
    ]), grade_label="自己採点する")

# ============================================================
# STAGE 10 — 練習5 / 練習72
# ============================================================
P72_TEXT = quote_box(
    "⑴　データおよび処理命令が主記憶装置に記憶されている。<br>\n"
    "⑵　（　①　）の指示で、主記憶装置に記憶されたデータおよび処理命令は、（　②　）に転送される。<br>\n"
    "⑶　（　③　）では、処理命令に従ってデータを処理し、（　④　）の指示でその演算結果を転送させて（　⑤　）に記憶させる。<br>\n"
    "⑷　（　⑥　）に記憶された演算結果は、（　⑦　）の指示で（　⑧　）に転送されて出力される。\n"
)

P72_SVG = """  <div class="viz-svg-wrap">
    <svg class="viz-svg wide" viewBox="0 0 620 246" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="制御装置の指示で、主記憶装置から演算装置へ、演算装置から主記憶装置へ、主記憶装置から出力装置へと演算結果が流れる図">
      <defs>
        <marker id="ar-solid" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#1A2B47"/>
        </marker>
        <marker id="ar-dash" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#4A78C8"/>
        </marker>
      </defs>

      <rect x="230" y="10" width="160" height="52" rx="10" fill="#4A78C8"/>
      <text x="310" y="34" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">制御装置</text>
      <text x="310" y="52" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" fill="#DAE6F5">① ④ ⑦</text>

      <line x1="290" y1="62" x2="160" y2="122" stroke="#4A78C8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ar-dash)"/>
      <line x1="320" y1="62" x2="330" y2="122" stroke="#4A78C8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ar-dash)"/>
      <line x1="360" y1="62" x2="480" y2="122" stroke="#4A78C8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ar-dash)"/>

      <rect x="6" y="130" width="130" height="52" rx="10" fill="#FAFCFF" stroke="#122E55" stroke-width="1.5"/>
      <text x="71" y="153" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="700" fill="#1A2B47">主記憶装置</text>
      <text x="71" y="171" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#75839B">⑴ データと処理命令</text>

      <rect x="166" y="130" width="130" height="52" rx="10" fill="#FAFCFF" stroke="#122E55" stroke-width="1.5"/>
      <text x="231" y="153" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="700" fill="#1A2B47">演算装置</text>
      <text x="231" y="171" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" fill="#2E5894">② ③</text>

      <rect x="326" y="130" width="130" height="52" rx="10" fill="#FAFCFF" stroke="#122E55" stroke-width="1.5"/>
      <text x="391" y="153" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="700" fill="#1A2B47">主記憶装置</text>
      <text x="391" y="171" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" fill="#2E5894">⑤ ⑥</text>

      <rect x="486" y="130" width="128" height="52" rx="10" fill="#FAFCFF" stroke="#122E55" stroke-width="1.5"/>
      <text x="550" y="153" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="14" font-weight="700" fill="#1A2B47">出力装置</text>
      <text x="550" y="171" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" fill="#2E5894">⑧</text>

      <line x1="136" y1="156" x2="166" y2="156" stroke="#1A2B47" stroke-width="1.8" marker-end="url(#ar-solid)"/>
      <line x1="296" y1="156" x2="326" y2="156" stroke="#1A2B47" stroke-width="1.8" marker-end="url(#ar-solid)"/>
      <line x1="456" y1="156" x2="486" y2="156" stroke="#1A2B47" stroke-width="1.8" marker-end="url(#ar-solid)"/>

      <text x="151" y="204" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#475673">データ・処理命令</text>
      <text x="311" y="204" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#475673">演算結果</text>
      <text x="471" y="204" text-anchor="middle" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#475673">演算結果</text>

      <line x1="20" y1="228" x2="52" y2="228" stroke="#1A2B47" stroke-width="1.8"/>
      <text x="58" y="232" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#475673">データの流れ</text>
      <line x1="160" y1="228" x2="192" y2="228" stroke="#4A78C8" stroke-width="1.6" stroke-dasharray="5 4"/>
      <text x="198" y="232" font-family="'Zen Kaku Gothic New',sans-serif" font-size="11" fill="#475673">制御の流れ(指示)</text>
    </svg>
  </div>
"""

P72 = stage_practice(
    5, 7, "72", "ベストフィット 練習72", "〈コンピュータの構成〉", "p5",
    '<span class="problem-tag match">MATCH × 8</span>',
    "次の⑴～⑷の記述は、コンピュータの構成とそれらによってコンピュータの基本機能が実現される過程を、順に説明したものである。空欄に入る適当な語句を、下の(ア)～(カ)から一つずつ選べ。ただし、用語は複数回選択することがある。",
    P72_TEXT,
    legend([("ア", "演算装置"), ("イ", "制御装置"), ("ウ", "主記憶装置"),
            ("エ", "入力装置"), ("オ", "補助記憶装置"), ("カ", "出力装置")])
    + match_list("ア,イ,ウ,エ,オ,カ", "1,0,0,1,2,2,1,5", [
        ("①", "⑵　（　①　）の指示で"),
        ("②", "⑵　…データおよび処理命令は、（　②　）に転送される"),
        ("③", "⑶　（　③　）では、処理命令に従ってデータを処理し"),
        ("④", "⑶　…（　④　）の指示でその演算結果を転送させて"),
        ("⑤", "⑶　…（　⑤　）に記憶させる"),
        ("⑥", "⑷　（　⑥　）に記憶された演算結果は"),
        ("⑦", "⑷　…（　⑦　）の指示で"),
        ("⑧", "⑷　…（　⑧　）に転送されて出力される"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">① (イ)　② (ア)　③ (ア)　④ (イ)　⑤ (ウ)　⑥ (ウ)　⑦ (イ)　⑧ (カ)</div>'),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑵</strong>　制御装置の指示で、データおよび処理命令は主記憶装置から演算装置へ転送される。</li>"
            "<li><strong>⑶</strong>　演算装置は、処理命令に従ってデータ処理をし、転送命令に従って演算結果を主記憶装置へ転送する。</li>"
            "<li><strong>⑷</strong>　制御装置からの転送命令に従い、主記憶装置から出力装置へ演算結果が転送され、出力装置によって演算結果が出力される。</li></ul>")),
        fb_section("「指示」と書いてあるところ(補足)", explain(
            "<p>①④⑦は、いずれも直後が「の指示で」です。指示を出すのは制御装置なので、この三つは同じ答えになります。"
            "残りは、データがどこにあるかを順に追います。②③は演算装置、⑤⑥は主記憶装置、⑧は出力装置です。"
            "入力装置と補助記憶装置は、この過程には出てきません。</p>")),
        viz("FLOW — 演算結果が出力されるまで", "実線がデータの流れ、破線が制御装置からの指示です。", P72_SVG),
    ]))

# ============================================================
# STAGE 11 — 練習6 / 練習73
# ============================================================
P73_THREE = """  <div class="origin-compare three-col">
    <div class="origin-side industrial">
      <h5>デバイスドライバ</h5>
      <div class="tag-en">⑴</div>
      <div class="origin-flow">
        <span class="origin-step">周辺機器</span>
        <span class="origin-arrow">→</span>
        <span class="origin-step fill">制御・操作</span>
      </div>
      <span class="origin-key">ハードウェアに最も近い</span>
      <p class="note">コンピュータに接続された周辺機器を制御・操作します。デバイスドライバがインストールされることで、オペレーティングシステムが周辺機器を動作させることができます。</p>
    </div>
    <div class="origin-side industrial">
      <h5>オペレーティングシステム</h5>
      <div class="tag-en">⑵</div>
      <div class="origin-flow">
        <span class="origin-step">基本的な管理</span>
        <span class="origin-arrow">→</span>
        <span class="origin-step fill">共通の機能</span>
      </div>
      <span class="origin-key">基本ソフトウェア</span>
      <p class="note">コンピュータの基本的な管理などの機能や、多くのソフトウェアが共通して利用する基本的な機能などをもちます。</p>
    </div>
    <div class="origin-side copyright">
      <h5>アプリケーションソフトウェア</h5>
      <div class="tag-en">⑶</div>
      <div class="origin-flow">
        <span class="origin-step">基本ソフトウェアの上</span>
        <span class="origin-arrow">→</span>
        <span class="origin-step fill">用途向けの機能</span>
      </div>
      <span class="origin-key">ハードウェアから最も遠い</span>
      <p class="note">基本ソフトウェアの上で、さまざまな用途向けの機能を提供します。応用ソフトウェアともいいます。</p>
    </div>
  </div>
"""

P73 = stage_practice(
    6, 7, "73", "ベストフィット 練習73", "〈ソフトウェア〉", "p6",
    '<span class="problem-tag self">記述・自己採点</span>',
    "コンピュータでは、さまざまなソフトウェアが使用されている。次の⑴～⑶が説明するソフトウェアの名称を答えよ。また、ハードウェアから近い位置にあるものから順番に⑴～⑶を並べよ。",
    "",
    self_list([
        ("⑴", "コンピュータに接続された周辺機器を制御・操作する。",
         "<p><strong>デバイスドライバ</strong><br>デバイスドライバがインストールされることで、オペレーティングシステムが周辺機器を動作させることができる。</p>"),
        ("⑵", "コンピュータの基本的な管理などの機能や、多くのソフトウェアが共通して利用する基本的な機能などをもつ。",
         "<p><strong>オペレーティングシステム(基本ソフトウェア)</strong><br>オペレーティング(operating)は、「運用、操作」などの意味がある。コンピュータの基本的な管理・制御を行うソフトウェアである。</p>"),
        ("⑶", "基本ソフトウェアの上で、さまざまな用途向けの機能を提供する。",
         "<p><strong>アプリケーションソフトウェア(応用ソフトウェア)</strong><br>オペレーティングシステムの上で、特定の作業を行うために使用されるソフトウェアである。</p>"),
        ("〈位置〉", "近い　（　　　）＜（　　　）＜（　　　）　遠い",
         "<p><strong>近い　⑴　＜　⑵　＜　⑶　遠い</strong><br>周辺機器を制御・操作するために OS が用いる⑴がハードウェアに最も近く、その上に⑵、さらにその上に⑶が乗ります。</p>"),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">⑴ デバイスドライバ　⑵ オペレーティングシステム(基本ソフトウェア)　⑶ アプリケーションソフトウェア(応用ソフトウェア)<br>〈位置〉 近い　⑴　＜　⑵　＜　⑶　遠い</div>'),
        fb_section("解説(原本)", explain(
            "<ul><li><strong>⑴</strong>　デバイスドライバがインストールされることで、オペレーティングシステムが周辺機器を動作させることができる。</li>"
            "<li><strong>⑵</strong>　オペレーティング(operating)は、「運用、操作」などの意味がある。コンピュータの基本的な管理・制御を行うソフトウェアである。</li>"
            "<li><strong>⑶</strong>　オペレーティングシステムの上で、特定の作業を行うために使用されるソフトウェアである。</li></ul>")),
        fb_section("並べる向きの決め方(補足)", explain(
            "<p>説明文の中に、上下の関係がそのまま書かれています。⑶には「基本ソフトウェアの上で」とあり、"
            "⑵より遠いことがわかります。⑴は周辺機器そのものを制御・操作するので、ハードウェアに最も近い位置です。"
            "名前を答えるだけでなく、どの層の仕事かまで押さえておきます。</p>")),
        viz("LAYERS — 近い順に並べる", "ハードウェアに近いほうから、⑴ → ⑵ → ⑶ の順に重なります。", P73_THREE),
    ]), grade_label="自己採点する")

# ============================================================
# STAGE 12 — 練習7 / 練習74
# ============================================================
P74_MODEL = (
    "<p><strong>16台</strong><br>"
    "コンピュータには、USBポートが一つしか残っていないので、そのポートに1台目のハブを接続することになる。"
    "さらに、2台目のハブは、この1台目に接続する。"
    "次に、3台目のハブは、1台目の空きポートまたは2台目のポートへ接続することが考えられる。"
    "ここで、ハブを接続するということはどういうことなのか考えてみると、どのハブに接続しようとも、"
    "接続することにより接続されたハブのポートが一つ減り、新たに接続したハブのポートでポートが四つ増える。"
    "つまり、新しいハブの接続により、ポートが三つ増えていくということがわかる。"
    "よって、1台目接続時に4ポート、2台目以降接続時に3ポートずつ増えるので、4＋3＋3＋3＋3＝16ポート　と求められる。</p>"
)

P74 = stage_practice(
    7, 7, "74", "ベストフィット 練習74", "〈インタフェース〉", "p7",
    '<span class="problem-tag self">記述・自己採点</span>',
    "USBインタフェースでは、USBハブを用いることにより、コンピュータに接続する周辺機器の台数を増やすことができる。右の図のような、ポートが四つあるUSBハブを5台使用したとき、理論上最大何台の周辺機器を接続することができるか。ただし、コンピュータには、使用できるUSBのポートは一つしか残っていないものとする。",
    figure("assets/fig4-usb-hub.jpeg",
           "図: ポートが四つある USB ハブ",
           "図: ポートが四つある USB ハブ", 260, 200),
    self_list([
        (None, "理論上最大何台の周辺機器を接続することができるか。", P74_MODEL),
    ]),
    feedback("解説", [
        fb_section("正答", '<div class="fb-correct-line">16台</div>'),
        fb_section("解説(原本)", explain(
            "<p>コンピュータには、USBポートが一つしか残っていないので、そのポートに1台目のハブを接続することになる。"
            "さらに、2台目のハブは、この1台目に接続する。</p>"
            "<p>次に、3台目のハブは、1台目の空きポートまたは2台目のポートへ接続することが考えられる。</p>"
            "<p>ここで、ハブを接続するということはどういうことなのか考えてみると、どのハブに接続しようとも、"
            "接続することにより接続されたハブのポートが一つ減り、新たに接続したハブのポートでポートが四つ増える。"
            "つまり、新しいハブの接続により、ポートが三つ増えていくということがわかる。</p>"
            "<p>よって、1台目接続時に4ポート、2台目以降接続時に3ポートずつ増えるので、4＋3＋3＋3＋3＝16ポート　と求められる。</p>")),
        fb_section("数え違いが起きるところ(補足)", explain(
            "<p>ハブ1台で4ポート増えると考えて 4×5＝20 としてしまうのが、よくある数え違いです。"
            "ハブをつなぐには、つなぐ先の空きポートを一つ使います。増えるのは 4－1＝3 ポートです。"
            "1台目だけは、もともと空いていたコンピュータ側のポートを使うので、4ポートがそのまま残ります。</p>")),
        viz("COUNTING — ハブを増やしたときのポート数", "2台目からは、増えるのが三つずつになります。",
            bd_grid([
                ("1台目", "4", "コンピュータの空きポート1つに接続。1－1＋4＝4"),
                ("2台目", "7", "空きポート1つを使って接続。4－1＋4＝7"),
                ("3台目", "10", "7－1＋4＝10"),
                ("4台目", "13", "10－1＋4＝13"),
                ("5台目", "16", "13－1＋4＝16。ここに周辺機器を16台つなげます。"),
            ], warn="増えるのは1台につき三つ。4＋3＋3＋3＋3＝16ポート です。")),
    ]), grade_label="自己採点する")

# ============================================================
# STAGE 13 — RESULT
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

STAGES = WELCOME + REVIEW + EX39 + EX40 + EX41 + EX42 + P68 + P69 + P70 + P71 + P72 + P73 + P74 + RESULT

# ============================================================
# JS 差し替え
# ============================================================
TIMELINE = """  const TIMELINE_ENTRIES = [
    { idx: 0,  group: 'overview', num: '00', label: 'スタート' },
    { idx: 1,  group: 'overview', num: '01', label: 'おさらい' },
    { idx: 2,  group: 'examples', num: '例39', label: 'コンピュータの構成', probId: 'ex39' },
    { idx: 3,  group: 'examples', num: '例40', label: 'ソフトウェア', probId: 'ex40' },
    { idx: 4,  group: 'examples', num: '例41', label: 'デバイスドライバ', probId: 'ex41' },
    { idx: 5,  group: 'examples', num: '例42', label: 'インタフェース', probId: 'ex42' },
    { idx: 6,  group: 'practice', num: 'Q68', label: '〈コンピュータの構成〉', probId: 'p1' },
    { idx: 7,  group: 'practice', num: 'Q69', label: '〈ソフトウェア〉', probId: 'p2' },
    { idx: 8,  group: 'practice', num: 'Q70', label: '〈デバイスドライバ〉', probId: 'p3' },
    { idx: 9,  group: 'practice', num: 'Q71', label: '〈インタフェース〉', probId: 'p4' },
    { idx: 10, group: 'practice', num: 'Q72', label: '〈コンピュータの構成〉', probId: 'p5' },
    { idx: 11, group: 'practice', num: 'Q73', label: '〈ソフトウェア〉', probId: 'p6' },
    { idx: 12, group: 'practice', num: 'Q74', label: '〈インタフェース〉', probId: 'p7' },
    { idx: 13, group: 'result',   num: '✓',   label: '結果サマリ' }
  ];"""

PROBLEMS = """  const PROBLEMS = [
    { id: 'p1', label: 'Q68', name: '〈コンピュータの構成〉', stageIdx: 6 },
    { id: 'p2', label: 'Q69', name: '〈ソフトウェア〉', stageIdx: 7 },
    { id: 'p3', label: 'Q70', name: '〈デバイスドライバ〉', stageIdx: 8 },
    { id: 'p4', label: 'Q71', name: '〈インタフェース〉', stageIdx: 9 },
    { id: 'p5', label: 'Q72', name: '〈コンピュータの構成〉', stageIdx: 10 },
    { id: 'p6', label: 'Q73', name: '〈ソフトウェア〉', stageIdx: 11 },
    { id: 'p7', label: 'Q74', name: '〈インタフェース〉', stageIdx: 12 }
  ];"""


def main():
    html = SRC.read_text(encoding="utf-8")

    def sub1(pattern, repl, text, flags=0, label=""):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        assert n == 1, "置換に失敗: %s" % (label or pattern)
        return new

    html = sub1(r"<title>.*?</title>",
                "<title>ハードウェアとソフトウェア | Practice Lab</title>", html, 0, "title")
    html = sub1(r'<span class="tg">CHAPTER 2\.06</span>',
                '<span class="tg">CHAPTER 3.08</span>', html, 0, "chapter tag")
    html = sub1(r'<span class="sb-score" id="sb-score">—/6</span>',
                '<span class="sb-score" id="sb-score">—/7</span>', html, 0, "sb-score")

    # stages
    html = sub1(r'(<main id="stages">\n).*?(\n</main>)',
                lambda m: m.group(1) + STAGES.rstrip("\n") + m.group(2),
                html, re.S, "stages")

    # timeline
    html = sub1(r"  const TIMELINE_ENTRIES = \[.*?\n  \];",
                lambda m: TIMELINE, html, re.S, "TIMELINE_ENTRIES")
    html = sub1(r"  const PROBLEMS = \[.*?\n  \];",
                lambda m: PROBLEMS, html, re.S, "PROBLEMS")

    # summary denominators / thresholds
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

    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT, len(html), "bytes")


if __name__ == "__main__":
    main()
