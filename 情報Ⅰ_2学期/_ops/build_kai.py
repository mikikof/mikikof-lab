#!/usr/bin/env python3
"""情報Ⅰ 2学期 — 回フォルダを正本から組む。

回フォルダは派生物。ここで組み直せる形を保つ（手でコピーして育てない）。
台帳は _ops/manifest.toml だけ。読み込みは stdlib の tomllib（外部依存を足さない）。

    python3 _ops/build_kai.py 1        1回ぶんを組む
    python3 _ops/build_kai.py --all    全回を組み直す
    python3 _ops/build_kai.py --index  ハブの index.html だけ作り直す

公開安全: 02_プリント/ と _teacher/ は .gitignore で外してある（解答・原本由来）。
組んだあとは必ず `python3 _ops/check_public.py` を通す。
"""

from __future__ import annotations

import html
import shutil
import sys
import tomllib
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent          # 情報Ⅰ_2学期/
MANIFEST = HUB / "_ops" / "manifest.toml"
KAI_SRC = HUB / "_ops" / "kai"


# --------------------------------------------------------------------------- 読み込み

def die(msg: str) -> None:
    print(f"[中断] {msg}", file=sys.stderr)
    sys.exit(1)


def load() -> dict:
    if not MANIFEST.exists():
        die(f"台帳が無い: {MANIFEST}")
    with MANIFEST.open("rb") as fh:
        try:
            return tomllib.load(fh)
        except tomllib.TOMLDecodeError as e:
            die(f"manifest.toml の書式が壊れている: {e}")


def company_root(m: dict) -> Path:
    """my-company/.company を返す。単独 clone では解決できないので明示的に止まる。"""
    root = (HUB / m["paths"]["company_root"]).resolve()
    if not (root / "media").is_dir():
        die(
            f"正本の置き場が見つからない: {root}\n"
            "       mikikof-lab を単独で clone した環境では回フォルダを組めない。\n"
            "       my-company の submodule として配置した状態で実行する。"
        )
    return root


def kai_dirname(k: dict) -> str:
    return f"第{k['no']:02d}回_{k['slug']}"


# --------------------------------------------------------------------------- 部品

def copy_one(src: Path, dst_dir: Path, label: str, warn: list[str]) -> Path | None:
    if not src.exists():
        warn.append(f"{label}: 正本が無い → {src}")
        return None
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return dst


def pick(*cands: Path) -> Path | None:
    for c in cands:
        if c.exists():
            return c
    return None


def anchor_title(m: dict, kind: str, ident) -> str:
    for ch in m.get("anchor_map", {}).values():
        for p in ch.get("points", []):
            if kind == "lec" and p["lec"] == ident:
                return p["title"]
            if kind == "practice" and p["practices"] == str(ident):
                return p["practices_title"]
    return ""


# --------------------------------------------------------------------------- HTML

CSS = """
:root{--navy:#0F2847;--blue:#2f6da8;--pale:#e4ecf5;--ink:#16202c;--sub:#4c5a6b;--bg:#f7f9fc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic Medium",sans-serif;
 font-weight:500;line-height:1.75;-webkit-text-size-adjust:100%}
.wrap{max-width:760px;margin:0 auto;padding:32px 20px 80px}
header{border-bottom:2px solid var(--navy);padding-bottom:14px;margin-bottom:26px}
.term{font-size:13px;letter-spacing:.14em;color:var(--blue);font-weight:700}
h1{font-size:26px;margin:6px 0 4px;color:var(--navy);line-height:1.4}
.lead{font-size:15px;color:var(--sub);margin:0}
h2{font-size:17px;color:var(--navy);margin:32px 0 12px;
 border-left:4px solid var(--blue);padding-left:10px}
.card{display:block;background:#fff;border:1px solid var(--pale);border-radius:10px;
 padding:16px 18px;margin-bottom:12px;text-decoration:none;color:inherit;
 transition:border-color .15s,transform .15s}
a.card:hover{border-color:var(--blue);transform:translateY(-1px)}
.card .no{font-size:12px;letter-spacing:.1em;color:var(--blue);font-weight:700}
.card .ttl{font-size:17px;color:var(--navy);font-weight:700;margin:2px 0 4px}
.card .meta{font-size:13px;color:var(--sub)}
.blk{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 0}
.blk div{flex:1 1 150px;background:#fff;border:1px solid var(--pale);border-radius:8px;padding:12px 14px}
.blk .m{font-size:12px;color:var(--blue);font-weight:700;letter-spacing:.08em}
.blk .n{font-size:15px;color:var(--navy);font-weight:700}
.empty{background:#fff;border:1px dashed var(--pale);border-radius:10px;padding:22px;
 color:var(--sub);font-size:14px}
footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--pale);
 font-size:13px;color:var(--sub)}
@media(max-width:720px){.wrap{padding:22px 16px 64px}h1{font-size:22px}}
"""


def page(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"ja\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n<div class=\"wrap\">\n{body}\n</div>\n</body>\n</html>\n"
    )


def kai_index_html(m: dict, k: dict, links: dict) -> str:
    e = html.escape
    blocks = "".join(
        f'<div><div class="m">{b["min"]}分</div><div class="n">{e(b["label"])}</div></div>'
        for b in m["lesson"]["blocks"]
    )
    rows = []
    for label, url, note in links["public"]:
        if url:
            rows.append(
                f'<a class="card" href="{e(url)}"><div class="ttl">{e(label)}</div>'
                f'<div class="meta">{e(note)}</div></a>'
            )
        else:
            rows.append(
                f'<div class="card"><div class="ttl">{e(label)}</div>'
                f'<div class="meta">{e(note)}</div></div>'
            )
    body = (
        "<header>"
        f'<div class="term">{e(m["term"])} · {e(m["subject"])}</div>'
        f'<h1>第{k["no"]}回　{e(k["theme"])}</h1>'
        f'<p class="lead">{m["lesson"]["total_min"]}分</p>'
        "</header>"
        f'<div class="blk">{blocks}</div>'
        "<h2>授業で使うもの</h2>" + "".join(rows[:2]) +
        "<h2>自分で進めるもの</h2>" + "".join(rows[2:]) +
        '<footer><a href="../">回の一覧へ</a></footer>'
    )
    return page(f"第{k['no']}回 {k['theme']}", body)


def hub_index_html(m: dict) -> str:
    e = html.escape
    kais = sorted(m.get("kai", []), key=lambda x: x["no"])
    if not kais:
        cards = '<div class="empty">回はまだ登録されていない。<br>'\
                '<code>_ops/manifest.toml</code> の <code>[[kai]]</code> に足して '\
                '<code>build_kai.py</code> を走らせる。</div>'
    else:
        cards = "".join(
            f'<a class="card" href="{e(kai_dirname(k))}/">'
            f'<div class="no">第{k["no"]:02d}回</div>'
            f'<div class="ttl">{e(k["theme"])}</div>'
            f'<div class="meta">{e(k.get("date",""))}'
            f'{"　·　準備中" if k.get("status") != "done" else ""}</div></a>'
            for k in kais
        )
    body = (
        "<header>"
        f'<div class="term">{e(m["term"])}</div>'
        f'<h1>{e(m["subject"])}</h1>'
        '<p class="lead">授業で使うものと、自分で進めるものをまとめてある。</p>'
        "</header>"
        f"<h2>回の一覧</h2>{cards}"
        "<h2>いつでも使えるもの</h2>"
        f'<a class="card" href="{e(m["hubs"]["lectures"]["public_url"])}">'
        '<div class="ttl">学習ノート</div><div class="meta">単元ごとの解説スライド</div></a>'
        f'<a class="card" href="{e(m["hubs"]["practices"]["public_url"])}">'
        '<div class="ttl">問題集</div><div class="meta">採点つきの演習</div></a>'
        f'<a class="card" href="{e(m["hubs"]["explainer"]["public_url"])}">'
        '<div class="ttl">解説ツール</div><div class="meta">動かして確かめる</div></a>'
        f'<a class="card" href="{e(m["hubs"]["quiz"]["public_url"])}">'
        '<div class="ttl">スピードテスト</div><div class="meta">速さと正答率で復習する</div></a>'
        '<footer><a href="../">mikikof-lab トップへ</a></footer>'
    )
    return page(f'{m["subject"]} {m["term"]}', body)


# --------------------------------------------------------------------------- 本体

def build_kai(m: dict, k: dict) -> list[str]:
    warn: list[str] = []
    root = company_root(m)
    p = m["paths"]
    d = HUB / kai_dirname(k)
    art = k.get("artifacts", {})

    for sub in ("01_解説", "02_プリント", "03_速テスト", "04_個人学習", "_teacher"):
        (d / sub).mkdir(parents=True, exist_ok=True)

    public: list[tuple[str, str, str]] = []

    # ① 解説ツール（自作・公開ハブでも配信済み → 追跡してよい）
    exp_url = ""
    name = art.get("explainer")
    if name:
        src = pick(root / p["explainer_dist"] / name,
                   root / "media/webツール/情報" / name)
        if src is None:
            warn.append(f"解説ツール: 正本が無い → {p['explainer_dist']}/{name}")
        else:
            copy_one(src, d / "01_解説", "解説ツール", warn)
            exp_url = m["hubs"]["explainer"]["public_url"] + name
    public.append(("解説ツール", exp_url, "授業の前半で動かす" if exp_url else "未作成"))

    # ③ スピードテスト（リンクのみ。配布リンクは _teacher へ）
    quiz = art.get("quiz") or {}
    quiz_url = ""
    if quiz.get("set_index") is not None:
        quiz_url = f'{m["hubs"]["quiz"]["public_url"]}?s={quiz["set_index"]}'
    public.append(("スピードテスト", quiz_url, "授業の最後に実施する" if quiz_url else "未作成"))

    # ④ 個人学習（相対だと階層を間違えるので公開 URL で持つ）
    lec = art.get("lecture")
    lec_url = ""
    if lec is not None:
        hits = sorted((HUB / p["lectures_articles"]).glob(f"{int(lec):02d}-*"))
        if hits:
            lec_url = f'{m["hubs"]["lectures"]["public_url"]}articles/{hits[0].name}/'
        else:
            warn.append(f"lectures: lec{lec} が未作成（この回のフローで作る）")
    public.append(("学習ノート", lec_url,
                   f"POINT {lec}　{anchor_title(m,'lec',lec)}" if lec else "対応なし"))

    pra = art.get("practice")
    pra_url = ""
    if pra:
        hits = sorted((HUB / p["practices_articles"]).glob(f"{pra}-*"))
        if hits:
            pra_url = f'{m["hubs"]["practices"]["public_url"]}articles/{hits[0].name}/'
        else:
            warn.append(f"practices: {pra} が未作成（この回のフローで作る）")
    public.append(("問題集", pra_url,
                   f"{pra}　{anchor_title(m,'practice',pra)}" if pra else "対応なし"))

    # ② 印刷プリント（解答を含む → 非追跡ディレクトリへ）
    if unit := art.get("print"):
        for suffix in ("問題", "解答"):
            fn = f"{unit}_{suffix}.html"
            src = pick(root / p["print_dist"] / fn, root / p["print_examples"] / fn)
            if src:
                copy_one(src, d / "02_プリント", f"プリント({suffix})", warn)
            else:
                warn.append(f"プリント({suffix}): 正本が無い → {p['print_dist']}/{fn}")

    # 進行台本（設計の正本は _ops/kai/。ここへは複製を置く）
    src_md = KAI_SRC / f"{k['no']:02d}-{k['slug']}.md"
    if src_md.exists():
        shutil.copy2(src_md, d / "_teacher" / "進行台本.md")
    else:
        warn.append(f"進行台本が無い → _ops/kai/{k['no']:02d}-{k['slug']}.md"
                    "（_templates/kai.template.md から起こす）")

    # 配布リンク（クラス別・非追跡）
    if quiz_url:
        lines = [f"# 第{k['no']}回 配布リンク（クラス内限定）", ""]
        for cls in m["hubs"]["quiz"].get("classes", []):
            lines.append(f"- {cls}: {quiz_url}&g={cls}")
        lines += ["", f"- 先生用コンソール: {m['hubs']['quiz']['teacher_url']}",
                  "", "> このファイルは .gitignore で外してある（公開しない）。"]
        (d / "_teacher" / "配布リンク.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 案内文（追跡してよい）
    (d / "03_速テスト" / "README.md").write_text(
        f"# 第{k['no']}回 スピードテスト\n\n"
        f"- 公開 URL: {quiz_url or '（未作成）'}\n"
        f"- クラス別の配布リンクは `_teacher/配布リンク.md`（非公開）\n",
        encoding="utf-8")
    (d / "04_個人学習" / "README.md").write_text(
        f"# 第{k['no']}回 個人学習\n\n"
        f"- 学習ノート: {lec_url or '（未作成）'}\n"
        f"- 問題集: {pra_url or '（未作成）'}\n\n"
        "授業内では使わない。復習と自習に使う。\n",
        encoding="utf-8")

    (d / "index.html").write_text(kai_index_html(m, k, {"public": public}), encoding="utf-8")
    return warn


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    m = load()
    kais = {k["no"]: k for k in m.get("kai", [])}

    if args[0] == "--index":
        targets = []
    elif args[0] == "--all":
        targets = sorted(kais)
    else:
        try:
            n = int(args[0])
        except ValueError:
            die(f"回番号か --all / --index を渡す（受け取った値: {args[0]}）")
        if n not in kais:
            die(f"第{n}回が台帳に無い。manifest.toml の [[kai]] に足す")
        targets = [n]

    all_warn: list[str] = []
    for n in targets:
        w = build_kai(m, kais[n])
        print(f"[組んだ] {kai_dirname(kais[n])}")
        all_warn += [f"  第{n}回 {x}" for x in w]

    (HUB / "index.html").write_text(hub_index_html(m), encoding="utf-8")
    print("[組んだ] index.html（回の一覧）")

    if all_warn:
        print("\n[未完]")
        for w in all_warn:
            print(w)
    print(f"\n次: python3 {Path(__file__).parent.name}/check_public.py")


if __name__ == "__main__":
    main()
