#!/usr/bin/env python3
# 使い方: python3 _ops/docx2txt2.py <出力先フォルダ> <原本の docx> [<docx> …]（docx ごとに <名前>.txt を書く。学習ノート・ベストフィットの裏取り用。出力は公開リポに置かない）
# docx → text。w:t と m:t(数式)を拾い、下付き(vertAlign subscript)は「(…)」、上付きは「^…」で印す。画像の位置は [IMG:rIdN→media/file] で残す。
import sys, zipfile, re
import xml.etree.ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M='{http://schemas.openxmlformats.org/officeDocument/2006/math}'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
V='{urn:schemas-microsoft-com:vml}'
def rels(z):
    root=ET.fromstring(z.read('word/_rels/document.xml.rels'))
    return {r.get('Id'):r.get('Target') for r in root}
def run_text(r, rel):
    # r は w:r か m:r
    out=[]
    rpr=r.find(W+'rPr'); va=None
    if rpr is not None:
        v=rpr.find(W+'vertAlign')
        if v is not None: va=v.get(W+'val')
    for el in r.iter():
        if el.tag in (W+'t', M+'t'): out.append(el.text or '')
        elif el.tag==W+'tab': out.append('\t')
        elif el.tag==W+'br': out.append('\n')
        elif el.tag==W+'sym': out.append('[SYM:%s]'%el.get(W+'char'))
        elif el.tag==A+'blip':
            rid=el.get(R+'embed'); out.append('[IMG:%s→%s]'%(rid, rel.get(rid)))
        elif el.tag==V+'imagedata':
            rid=el.get(R+'id'); out.append('[IMG:%s→%s]'%(rid, rel.get(rid)))
    t=''.join(out)
    if va=='subscript' and t.strip(): t='('+t.strip()+')'
    elif va=='superscript' and t.strip(): t='^'+t.strip()
    return t
def ptext(p, rel):
    out=[]
    for ch in p:
        if ch.tag==W+'r': out.append(run_text(ch, rel))
        elif ch.tag in (M+'oMath', M+'oMathPara'):
            # 数式: 下付き sSub は base(sub) と印す
            out.append(mtext(ch, rel))
        elif ch.tag==W+'hyperlink' or ch.tag==W+'smartTag' or ch.tag==W+'ins':
            out.append(ptext(ch, rel))
        elif ch.tag==W+'sdt':
            c=ch.find(W+'sdtContent')
            if c is not None: out.append(ptext(c, rel))
    return ''.join(out)
def mtext(node, rel):
    out=[]
    for ch in node:
        if ch.tag==M+'r': out.append(run_text(ch, rel))
        elif ch.tag==M+'sSub':
            e=ch.find(M+'e'); s=ch.find(M+'sub')
            out.append(mtext(e, rel)+'('+mtext(s, rel)+')')
        elif ch.tag==M+'sSup':
            e=ch.find(M+'e'); s=ch.find(M+'sup')
            out.append(mtext(e, rel)+'^'+mtext(s, rel))
        elif ch.tag==M+'sSubSup':
            e=ch.find(M+'e'); s=ch.find(M+'sub'); u=ch.find(M+'sup')
            out.append(mtext(e, rel)+'('+mtext(s, rel)+')^'+mtext(u, rel))
        elif ch.tag==M+'f':
            n=ch.find(M+'num'); d=ch.find(M+'den'); out.append('('+mtext(n, rel)+')/('+mtext(d, rel)+')')
        elif ch.tag in (M+'oMath', M+'d', M+'e', M+'num', M+'den', M+'sub', M+'sup', M+'bar', M+'rad', M+'deg', M+'nary', M+'box', M+'eqArr'):
            out.append(mtext(ch, rel))
        elif ch.tag in (M+'sSubPr', M+'sSupPr', M+'fPr', M+'dPr', M+'oMathParaPr', M+'rPr', M+'ctrlPr', M+'barPr', M+'radPr', M+'naryPr', M+'boxPr', M+'eqArrPr'):
            pass
        else:
            out.append(mtext(ch, rel))
    return ''.join(out)
def walk(body, rel):
    lines=[]
    for ch in body:
        if ch.tag==W+'p':
            t=ptext(ch, rel).strip()
            if t: lines.append(t)
        elif ch.tag==W+'tbl':
            for tr in ch.iter(W+'tr'):
                cells=[]
                for tc in tr.findall(W+'tc'):
                    cells.append(' / '.join(ptext(p, rel).strip() for p in tc.iter(W+'p') if ptext(p, rel).strip()))
                lines.append('| '+' | '.join(cells)+' |')
            lines.append('')
        elif ch.tag==W+'sdt':
            c=ch.find(W+'sdtContent')
            if c is not None: lines+=walk(c, rel)
    return lines
for f in sys.argv[2:]:
    z=zipfile.ZipFile(f); rel=rels(z); root=ET.fromstring(z.read('word/document.xml'))
    body=root.find(W+'body')
    out=re.sub(r'（Python）|-問題|-解答|\.docx','',f.split('/')[-1])+'.txt'
    lines=walk(body, rel)
    open(sys.argv[1]+'/'+out,'w').write('\n'.join(lines))
    print(f"{out}: {len(lines)} lines, {sum(len(l) for l in lines)} chars")
