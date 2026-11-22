# -*- coding: utf-8 -*-
"""Add a product repo as a submodule, update products.json, regenerate README and push."""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="display name")
    ap.add_argument("--slug", required=True, help="folder slug, lowercase letters/digits/dash")
    ap.add_argument("--repo", required=True, help="git clone URL")
    ap.add_argument("--desc", default="", help="one-line description")
    ap.add_argument("--tags", default="", help="comma separated tech tags")
    ap.add_argument("--demo", default="", help="live demo URL")
    ap.add_argument("--no-push", action="store_true", help="commit locally without pushing")
    args = ap.parse_args()

    slug = args.slug.strip().lower()
    if not slug or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slug):
        raise SystemExit("slug must be lowercase letters, digits or dash")

    path = os.path.join(ROOT, "products.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if any(p["slug"] == slug for p in data["products"]):
        raise SystemExit(f"slug already exists: {slug}")

    no = max([p["no"] for p in data["products"]] or [0]) + 1
    folder = f"products/{no:02d}-{slug}"
    if os.path.exists(os.path.join(ROOT, folder)):
        raise SystemExit(f"folder already exists: {folder}")

    run(["git", "submodule", "add", args.repo, folder])

    data["products"].append({
        "no": no,
        "name": args.name,
        "slug": slug,
        "repo": args.repo,
        "demo": args.demo,
        "desc": args.desc,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
    })
    data["products"] = sorted(data["products"], key=lambda p: p["no"])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    run([sys.executable, "scripts/render_readme.py"])
    run(["git", "add", "-A"])
    run(["git", "commit", "-m", f"add product: {no:02d} {args.name}"])
    if not args.no_push:
        run(["git", "push"])
    print(f"done: {folder}")


if __name__ == "__main__":
    main()
