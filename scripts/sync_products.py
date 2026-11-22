# -*- coding: utf-8 -*-
"""Discover public repos tagged with the `vibecoding` topic and add them as submodules."""
import json
import os
import subprocess
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "Brambleaaaaaa"
SELF = "vibecoding"
TOPIC = "vibecoding"


def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ.get('GH_TOKEN', '')}",
            "User-Agent": "vibecoding-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def run(cmd):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}")


def norm_url(url):
    return (url or "").rstrip("/").removesuffix(".git").lower()


def main():
    data = json.load(open(os.path.join(ROOT, "products.json"), encoding="utf-8"))
    known = {p["slug"] for p in data["products"]}
    known_urls = {norm_url(p.get("repo")) for p in data["products"]}

    repos = []
    page = 1
    while True:
        batch = api(f"/users/{OWNER}/repos?per_page=100&type=owner&page={page}")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    added = 0
    for repo in repos:
        slug = repo["name"]
        if slug == SELF or slug in known or norm_url(repo["html_url"]) in known_urls:
            continue
        if TOPIC not in (repo.get("topics") or []):
            continue
        no = max([p["no"] for p in data["products"]] or [0]) + 1
        folder = f"products/{no:02d}-{slug}"
        if os.path.exists(os.path.join(ROOT, folder)):
            continue
        run(["git", "submodule", "add", "--depth", "1", repo["clone_url"], folder])
        data["products"].append({
            "no": no,
            "name": slug,
            "slug": slug,
            "repo": repo["html_url"],
            "demo": repo.get("homepage") or "",
            "desc": repo.get("description") or "",
            "tags": [t for t in (repo.get("topics") or []) if t != TOPIC],
        })
        known.add(slug)
        known_urls.add(norm_url(repo["html_url"]))
        added += 1

    data["products"].sort(key=lambda p: p["no"])
    with open(os.path.join(ROOT, "products.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    run(["python", "scripts/render_readme.py"])
    print(f"added {added} product(s)")


if __name__ == "__main__":
    main()
