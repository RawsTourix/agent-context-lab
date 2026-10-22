"""Small command line entry point for deterministic experiments and local inspection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .experiment import run_demo
from .storage import load_bundle, verify_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agent Context Lab research harness")
    parser.add_argument("--runs-dir", type=Path, default=Path("runs"))
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="Run deterministic scripted agent benchmark")
    demo.add_argument("--budget", type=int, default=2048)
    listing = sub.add_parser("list", help="List local run attempts")
    show = sub.add_parser("show", help="Inspect a run bundle")
    show.add_argument("path", type=Path)
    verify = sub.add_parser("verify", help="Verify immutable run evidence and hashes")
    verify.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.command == "demo":
        target = run_demo(args.runs_dir, budget_tokens=args.budget)
        print(target)
        return 0
    if args.command == "list":
        for manifest in sorted(args.runs_dir.glob("*/*/*/manifest.json")):
            target = manifest.parent
            result = target / "result.json"
            status = json.loads(result.read_text(encoding="utf-8")).get("status") if result.exists() else "incomplete"
            print(f"{target}: {status}")
        return 0
    if args.command == "verify":
        print(json.dumps(verify_bundle(args.path), ensure_ascii=False, indent=2))
        return 0
    if args.command == "show":
        run = load_bundle(args.path)
        print(json.dumps(run, ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
