from collections import defaultdict
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
HEADINGS = ["重點摘要", "概念說明", "例子或應用", "來源"]


def read_note(path):
    title, category, body = path.read_text(encoding="utf-8-sig").split("\n", 2)
    if not title.startswith("# ") or not category.startswith("分類："):
        raise ValueError(f"{path.name} 缺少標題或分類")
    title, category = title[2:].strip(), category[3:].strip()
    if not title or not category or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.stem):
        raise ValueError(f"{path.name} 的標題、分類或檔名不符格式")
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    sections = dict(zip(parts[1::2], (part.strip() for part in parts[2::2])))
    if parts[0].strip() or parts[1::2] != HEADINGS or not all(sections.values()):
        raise ValueError(f"{path.name} 必須依序包含四段，每段須有內容")
    return title, category, sections


def render_text(text):
    blocks = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.splitlines()
        if all(line.startswith("- ") for line in lines):
            blocks.append("<ul>" + "".join(f"<li>{escape(line[2:])}</li>" for line in lines) + "</ul>")
        else:
            blocks.append(f"<p>{escape(' '.join(lines))}</p>")
    return "\n".join(blocks)


def page(title, content, prefix="", script=False):
    script_tag = '<script src="app.js" defer></script>' if script else ""
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · 資訊安全管理課程筆記</title>
<link rel="stylesheet" href="{prefix}style.css">
{script_tag}
</head>
<body>
<a class="skip" href="#main">跳至主要內容</a>
<header class="masthead"><a href="{prefix}index.html">資訊安全管理<span>課程筆記</span></a></header>
<main id="main">
{content}
</main>
<footer>資訊安全管理課程筆記</footer>
</body>
</html>
"""


def build():
    groups = defaultdict(list)
    outputs = {}
    seen = set()
    for path in sorted((ROOT / "notes").glob("*.md")):
        title, category, sections = read_note(path)
        if (category, title) in seen:
            raise ValueError(f"分類內有重複的筆記標題：{title}")
        seen.add((category, title))
        body = "\n".join(f"<section><h2>{heading}</h2>{render_text(content)}</section>" for heading, content in sections.items())
        article = f'<article><a class="back" href="../index.html">← 返回目錄</a><p class="category">{escape(category)}</p><h1>{escape(title)}</h1>{body}</article>'
        outputs[path.with_suffix(".html")] = page(title, article, "../")
        summary = sections[HEADINGS[0]].removeprefix("- ").replace("\n", " ")
        searchable = escape(" ".join([category, title, *sections.values()]), quote=True)
        groups[category].append(f'<li data-note data-search="{searchable}"><a href="notes/{path.stem}.html">{escape(title)}</a><p>{escape(summary)}</p></li>')
    groups_html = "\n".join(f'<section class="group"><h2>{escape(category)}</h2><ul>{"".join(items)}</ul></section>' for category, items in groups.items())
    home = f"""<div class="intro">
<h1>資訊安全管理</h1>
<p>從資安基本概念到風險管理，按主題複習課堂重點。</p>
</div>
<div class="catalog">
<label for="search">搜尋筆記</label>
<input id="search" type="search" placeholder="例如：風險、CIA、數位簽章">
<p id="results" aria-live="polite">{len(outputs)} 篇筆記</p>
{groups_html}
</div>"""
    outputs[ROOT / "index.html"] = page("首頁", home, script=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"Built {len(outputs)} pages")


if __name__ == "__main__":
    build()
