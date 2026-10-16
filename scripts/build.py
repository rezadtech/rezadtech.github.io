# Build themed pages from Markdown. Run from any directory.
from pathlib import Path
from datetime import date, datetime
from html import escape
from urllib.parse import quote
import argparse
import re
import shutil
import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"cybersecurity": "Cybersecurity", "photonics": "Photonic technologies"}

def parse_post(path):
    text = path.read_text(encoding="utf-8-sig")
    meta = {}
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) != 3:
            raise ValueError(f"{path}: unclosed YAML front matter")
        meta = yaml.safe_load(parts[1]) or {}
        if not isinstance(meta, dict):
            raise ValueError(f"{path}: front matter must be a mapping")
        text = parts[2]
    title_match = re.search(r"^# +(.+)$", text, re.MULTILINE)
    title = str(meta.get("title") or (title_match.group(1) if title_match else path.stem.replace("-", " ").replace("_", " ")))
    if title_match and title_match.group(1).strip() == title.strip():
        text = text[:title_match.start()] + text[title_match.end():]
    published = str(meta.get("date") or "")
    if published:
        date.fromisoformat(published)
    summary = str(meta.get("summary") or "")
    draft = meta.get("draft", False)
    if not isinstance(draft, bool):
        raise ValueError(f"{path}: draft must be true or false")
    return {"title": title, "date": published, "summary": summary, "draft": draft, "body": text}

def build(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output == source or output in source.parents:
        raise ValueError("Output must not overwrite the source directory or its parents")
    output.mkdir(parents=True, exist_ok=True)
    # Clear only generated content, so deleted Markdown posts disappear on rebuild.
    generated_posts = output / "posts"
    if generated_posts.exists():
        shutil.rmtree(generated_posts)
    for path in source.glob("*.html"):
        shutil.copy2(path, output / path.name)
    shutil.copytree(source / "assets", output / "assets", dirs_exist_ok=True)
    (output / ".nojekyll").touch()
    total = 0
    for category, label in CATEGORIES.items():
        page = (source / f"{category}.html").read_text()
        header = re.search(r"<header>.*?</header>", page, re.S).group()
        footer = re.search(r"<footer>.*?</footer>", page, re.S).group()
        # Article pages live two levels below the homepage.
        header = header.replace('href="index.html"', 'href="../../index.html"').replace('href="cybersecurity.html"', 'href="../../cybersecurity.html"').replace('href="photonics.html"', 'href="../../photonics.html"')
        records = []
        folder = source / "posts" / category
        for path in sorted(folder.glob("*.md")):
            post = parse_post(path)
            if post["draft"]:
                continue
            relative = Path("posts") / category / (path.stem + ".html")
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            body = markdown.markdown(post["body"], extensions=["fenced_code", "tables", "footnotes", "attr_list", "toc"])
            # Link sibling Markdown posts without asking the author to use HTML paths.
            body = re.sub(r'href="([^"?#]+)\.md([#?][^"]*)?"', lambda m: 'href="' + m[1] + '.html' + (m[2] or '') + '"', body)
            theme = "photonics" if category == "photonics" else ""
            timestamp = f'<time datetime="{escape(post["date"])}">{escape(post["date"])}</time>' if post["date"] else ""
            article = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(post["title"])} | RDTECH</title><meta name="description" content="{escape(post["summary"], quote=True)}"><meta name="color-scheme" content="{'light' if theme else 'dark'}"><link rel="icon" href="../../assets/favicon.svg"><link rel="stylesheet" href="../../assets/style.css"></head><body class="{theme} article-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main"><article><section class="intro"><a class="eyebrow" href="../../{category}.html#journal">← {label} journal</a><h1>{escape(post["title"])}</h1><p class="meta">Reza Dayhool {timestamp}</p><p class="lead">{escape(post["summary"])}</p></section><div class="prose">{body}</div></article></main>{footer}</body></html>'''
            target.write_text(article)
            records.append((post, quote(relative.as_posix())))
            total += 1
        records.sort(key=lambda item: (item[0]["date"], item[0]["title"]), reverse=True)
        cards = []
        for post, url in records:
            cards.append(f'<article class="entry"><p class="meta">{escape(post["date"])}</p><h3><a href="{url}">{escape(post["title"])}</a></h3><p class="muted">{escape(post["summary"])}</p><a href="{url}">Read article ↗</a></article>')
        listing = "".join(cards) or '<p class="note">No articles published yet.</p>'
        page = page.replace('<!-- POSTS -->', listing)
        (output / f"{category}.html").write_text(page)
        if folder.exists():
            # Images and PDFs can accompany Markdown, preserving relative links.
            for asset in folder.rglob("*"):
                if asset.is_file() and asset.suffix.lower() != ".md" and not any(p.startswith('.') for p in asset.relative_to(folder).parts):
                    dest = output / "posts" / category / asset.relative_to(folder)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(asset, dest)
    print(f"Built {total} articles in {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    build(args.source, args.output)
