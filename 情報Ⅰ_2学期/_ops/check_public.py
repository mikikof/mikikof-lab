#!/usr/bin/env python3
"""公開安全ゲート — mikikof-lab は PUBLIC リポジトリ。

追跡した物は GitHub 上で誰でも読める（Pages が配信するかどうかとは別）。
push の前にこれを通す。**exit 0 でなければ push しない。**

    python3 _ops/check_public.py

  §1 情報Ⅰ_2学期 配下 … 解答・原本由来・配布物が追跡されていないか（1件でも FAIL）
  §2 リポジトリ全体   … 版元著作物が追跡されていないか（報告。既知の残件を可視化する）
"""

from __future__ import annotations

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

    if fail:
        print("\n[FAIL] push しない。")
        sys.exit(1)
    print("\n[OK] §1 は通った。")
    sys.exit(0)


if __name__ == "__main__":
    main()
