#!/usr/bin/env python3
"""公開安全ゲート — mikikof-lab は PUBLIC リポジトリ。

追跡した物は GitHub 上で誰でも読める（Pages が配信するかどうかとは別）。
push の前にこれを通す。**exit 0 でなければ push しない。**

    python3 _ops/check_public.py

  §1 情報Ⅰ_2学期 配下 … 解答・原本由来・配布物が追跡されていないか（1件でも FAIL）
  §2 リポジトリ全体   … 版元著作物が追跡されていないか（報告。既知の残件を可視化する）
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent          # 情報Ⅰ_2学期/
REPO = HUB.parent                                     # mikikof-lab/
HUB_REL = HUB.name

# §1 このハブで追跡してはいけないもの（.gitignore と同じ線引き。CLAUDE.md §4 が正本）
DENY_DIRS = ("_teacher/", "02_プリント/", "_orig/", "_work/")
DENY_EXT = (".pdf", ".docx", ".pptx", ".xlsx", ".zip")

# §2 版元著作物とみなす手がかり（リポジトリ全体）
COPYRIGHT_HINTS = ("_source/", "学習ノート", "ベストフィット", "本文PDF", "winstep")
COPYRIGHT_EXT = (".pdf", ".docx", ".pptx", ".xlsx")


# §3 回の台帳の「中身」（2026-09-13 追加）
# パスと拡張子では止まらない漏れが実際に出た。_ops/kai/*.md に解答 PDF の文が
# 鉤括弧で引用され、出典表の値の欄に空欄の答えが式で書かれていた。
#
# **合格線は在庫を測ってから引いてある。** 01〜07 の 7 本を実測し、
# 「正解は原本で裏取りする」「`while i > 1`（取り違えの型の説明）」「00・01・10・11
# （真理値表の行の順）」のような正当な記述を FAIL にすると、ゲートが鳴りっぱなしになって
# 読まれなくなる。だから **実際に起きた 2 つの形だけを FAIL** にし、残りは警告に留める。
FAIL_RULES = (
    # 鉤括弧の中が「文」のときだけ鳴らす。用語の言い換え（「下限」「上限」）や
    # ページ参照（「p.94〜99」）は答えではないので、長さと中身で外す。
    (re.compile(r"解答 ?PDF[^\n]*「(?![^」]*p\.)[^」]{8,}?(?:[＝=＋+−<>]|を足す|を引く|に変化|とする|になる)[^」]*」"),
     "解答 PDF の文（式・操作）を鉤括弧で引用している"),
    (re.compile(r"^\|[^|]*\|[^|]*[A-Za-z][^|]*[＝=][^|]*\|[^|]*(実習|類題|章末)[^|]*\|"),
     "出典表の値の欄に、空欄の答えが式で書かれている"),
)
WARN_RULES = (
    (re.compile(r"「[^」]*[＝=][^」]*」"), "鉤括弧の中に等式（答えかもしれない）"),
    (re.compile(r"正答は|答えは|正解は(?!原本)"), "答えを名指ししている"),
)


def scan_kai() -> tuple[list[str], list[str]]:
    bad: list[str] = []
    warn: list[str] = []
    for f in sorted((HUB / "_ops" / "kai").glob("*.md")) + sorted((HUB / "_ops" / "kai").glob("*.toml")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for rx, why in FAIL_RULES:
                if rx.search(line):
                    bad.append(f"{f.name}:{i}  {why}\n       {line.strip()[:96]}")
            for rx, why in WARN_RULES:
                if rx.search(line):
                    warn.append(f"{f.name}:{i}  {why}")
    return bad, warn


def tracked() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "-z"],
            capture_output=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[中断] git ls-files が失敗した: {e}", file=sys.stderr)
        sys.exit(2)
    return [p for p in out.decode("utf-8").split("\0") if p]


def main() -> None:
    files = tracked()
    fail: list[str] = []

    # ---------------------------------------------------------------- §1
    hub_files = [f for f in files if f.startswith(HUB_REL + "/")]
    for f in hub_files:
        rest = f[len(HUB_REL) + 1:]
        if any(f"/{d}" in f"/{rest}" for d in DENY_DIRS):
            fail.append(f"{f}  ← 非公開ディレクトリが追跡されている")
        elif f.lower().endswith(DENY_EXT):
            fail.append(f"{f}  ← 配布物・版元著作物の拡張子")

    print(f"§1 {HUB_REL}/ 配下の追跡ファイル: {len(hub_files)} 件")
    if fail:
        print(f"   FAIL {len(fail)} 件")
        for f in fail:
            print(f"     - {f}")
        print("\n   直し方: git rm --cached <path> して .gitignore を確認する。")
        print("   実体は my-company(private)側の各キットにあるので、消しても失われない。")
    else:
        print("   OK  解答・原本由来・配布物の混入なし")

    # ---------------------------------------------------------------- §2
    leaks = [
        f for f in files
        if any(h in f for h in COPYRIGHT_HINTS) or f.lower().endswith(COPYRIGHT_EXT)
    ]
    print(f"\n§2 リポジトリ全体の版元著作物らしき追跡ファイル: {len(leaks)} 件")
    if leaks:
        by_dir: dict[str, int] = {}
        for f in leaks:
            by_dir[str(Path(f).parent)] = by_dir.get(str(Path(f).parent), 0) + 1
        for d, n in sorted(by_dir.items()):
            print(f"     {n:3d}  {d}/")
        print("\n   このリポジトリは public。.gitignore は**既に追跡されているファイルには効かない**。")
        print("   外すには履歴からの除去が要る（オーナー判断・作業前に必ず確認する）。")

    # ---------------------------------------------------------------- §3
    kai_bad, kai_warn = scan_kai()
    print(f"\n§3 回の台帳の中身（_ops/kai/）: FAIL {len(kai_bad)} 件 / 警告 {len(kai_warn)} 件")
    if kai_bad:
        for b in kai_bad:
            print(f"     - {b}")
        print("\n   台帳に解答・原本の逐語を書かない（CLAUDE.md §4）。中身は spec 側（非公開）へ。")
        fail.extend(kai_bad)
    else:
        print("   OK  解答 PDF の逐語引用・出典表への式の書き込みは無い")
    if kai_warn:
        print(f"   警告（人が見る。自動では落とさない）:")
        for w in kai_warn[:12]:
            print(f"     · {w}")

    if fail:
        print("\n[FAIL] push しない。")
        sys.exit(1)
    print("\n[OK] §1 は通った。")
    sys.exit(0)


if __name__ == "__main__":
    main()
