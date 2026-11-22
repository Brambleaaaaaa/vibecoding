# -*- coding: utf-8 -*-
"""Render the product list in README.md from products.json."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "<!-- PRODUCTS:START -->"
END = "<!-- PRODUCTS:END -->"


def load_products():
    with open(os.path.join(ROOT, "products.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return sorted(data["products"], key=lambda p: p["no"])


def render_table(products):
    lines = [
        "| # | 产品 | 介绍 | 技术栈 | 链接 |",
        "|---|---|---|---|---|",
    ]
    for p in products:
        links = [f"[仓库]({p['repo']})"]
        if p.get("demo"):
            links.append(f"[在线体验]({p['demo']})")
        tags = " · ".join(p.get("tags") or [])
        lines.append(
            f"| {p['no']} | **{p['name']}** | {p.get('desc', '')} | {tags} | {' / '.join(links)} |"
        )
    return "\n".join(lines)


def main():
    products = load_products()
    with open(os.path.join(ROOT, "README.template.md"), "r", encoding="utf-8") as f:
        tpl = f.read()
    table = render_table(products)
    if START not in tpl or END not in tpl:
        raise SystemExit("README.template.md is missing PRODUCTS markers")
    head, rest = tpl.split(START, 1)
    _, tail = rest.split(END, 1)
    out = head + START + "\n" + table + "\n" + END + tail
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"README.md updated: {len(products)} product(s)")


if __name__ == "__main__":
    main()
