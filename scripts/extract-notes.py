#!/usr/bin/env python3
"""Extract 13 Notes markdown files from site/notes-NN-slug.html.

One-off operational tool, not part of the build. Run from repo root:
  python3 scripts/extract-notes.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT_DIR = ROOT / "src" / "content" / "notes"

NOTE_FILES = [
    "01-intent",
    "02-brand-guide",
    "03-sketch",
    "04-prd",
    "05-design",
    "06-architecture",
    "07-build-plan",
    "08-automation-setup",
    "09-phase-build",
    "10-integration-test",
    "11-documentation",
    "12-deploy",
    "13-retro",
]

GROUP_OF = {}
for s in ("01-intent", "02-brand-guide", "03-sketch", "04-prd"):
    GROUP_OF[s] = "discover-plan"
for s in ("05-design", "06-architecture", "07-build-plan", "08-automation-setup"):
    GROUP_OF[s] = "design-architect"
for s in ("09-phase-build", "10-integration-test", "11-documentation", "12-deploy", "13-retro"):
    GROUP_OF[s] = "build-ship"


def unescape(s: str) -> str:
    return (
        s.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )


def strip_tags(s: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", s)).strip()


def yaml_str(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def parse_meta(html: str) -> dict:
    meta: dict = {}
    title_m = re.search(r"<title>([^<]+)</title>", html)
    title_text = unescape(title_m.group(1)) if title_m else ""
    # "01 Intent · 의도 — Bsides Notes"
    tm = re.match(r"^(\d{2})\s+(.+?)\s+·\s+(.+?)\s+—", title_text)
    if not tm:
        raise RuntimeError(f"cannot parse title: {title_text!r}")
    meta["num"] = tm.group(1)
    meta["en"] = tm.group(2).strip()
    meta["ko"] = tm.group(3).strip()

    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    description = unescape(desc_m.group(1)) if desc_m else ""

    # Body lead: the <p class="t-body" ...max-width: 580px;">...</p> right after h1 in head section
    lead_m = re.search(
        r'<p class="t-body"[^>]*max-width: 580px[^>]*>([^<]+)</p>',
        html,
    )
    meta["lead"] = unescape(lead_m.group(1).strip()) if lead_m else description

    # h1_lead: text after </span> in <h1 ...><span ...>{en}</span>{h1_lead}</h1>
    h1_m = re.search(r"<h1[^>]*>\s*<span[^>]*>[^<]+</span>([^<]+)</h1>", html)
    meta["h1_lead"] = unescape(h1_m.group(1).strip()) if h1_m else ""

    # read_time: span after the spooni image, "학습 노트 · 약 8분 읽기"
    rt_m = re.search(r"학습 노트 · ([^<]+?)</span>", html)
    meta["read_time"] = unescape(rt_m.group(1).strip()) if rt_m else "약 8분 읽기"

    # italic intro: first <p style="...font-style: italic;">...</p>
    it_m = re.search(
        r'<p style="[^"]*font-style: italic;[^"]*">([^<]+)</p>',
        html,
    )
    meta["italic"] = unescape(it_m.group(1).strip()) if it_m else ""

    # workshop_text: <div class="t-caption" style="line-height: 1.55;">...</div>
    ws_m = re.search(
        r'<div class="t-caption" style="line-height: 1\.55;">([^<]+)</div>',
        html,
    )
    meta["workshop_text"] = unescape(ws_m.group(1).strip()) if ws_m else ""
    return meta


def extract_article_inner(html: str) -> str:
    # Get the <div class="t-body" style="...display: grid; gap: 20px;"> block inside <article>
    art = re.search(
        r'<article class="b-container"[^>]*>(.*?)</article>',
        html,
        re.DOTALL,
    )
    if not art:
        raise RuntimeError("article block not found")
    inner = art.group(1)
    body = re.search(
        r'<div class="t-body"[^>]*display: grid; gap: 20px;[^"]*">(.*?)</div>\s*<div style="margin-top: 56px;',
        inner,
        re.DOTALL,
    )
    if not body:
        # try without trailing marker
        body = re.search(
            r'<div class="t-body"[^>]*display: grid; gap: 20px;[^"]*">(.*)$',
            inner,
            re.DOTALL,
        )
    if not body:
        raise RuntimeError("body grid not found")
    return body.group(1)


def html_to_markdown(inner: str) -> list[str]:
    """Convert the body content sequence into markdown lines.

    Recognized blocks (in order they appear):
      - <p style="...font-style: italic;">...</p>  -> SKIP (italic frontmatter)
      - <p style="margin: 0px;">...</p>            -> paragraph (inline tags converted)
      - <h3 class="t-title-2" ...>...</h3>         -> "### ..."
      - <div style="...background: var(--b-note-mint)...">...</div> -> sticky note HTML kept inline
      - <blockquote ...>...</blockquote>           -> "> ..."
    """
    out: list[str] = []
    # Tokenize: iterate over top-level blocks. We'll walk by repeatedly
    # matching the next top-level tag.
    pos = 0
    # Pattern: matches the next <p>, <h3>, or sticky note <div> at current pos.
    block_re = re.compile(
        r"<p(\s[^>]*)?>(.*?)</p>|"
        r"<h3(\s[^>]*)?>(.*?)</h3>|"
        r'<div style="margin: 12px 0px; padding: 20px 22px; background: var\(--b-note-mint\)[^"]*">(.*?)</div>\s*</div>',
        re.DOTALL,
    )
    # The sticky note has a nested </div> structure. Simpler: detect sticky-note div by full re including its known shape.
    sticky_re = re.compile(
        r'<div style="margin: 12px 0px; padding: 20px 22px; background: var\(--b-note-mint\)[^"]*">'
        r'<div style="font-family: var\(--b-font-hand\)[^"]*">([^<]+)</div>'
        r'<div style="font-family: var\(--b-font-sans\)[^"]*">([^<]+)</div>'
        r"</div>",
        re.DOTALL,
    )

    # Greedy approach: walk forward by trying to match (in priority): sticky note, p, h3.
    italic_seen = False
    while pos < len(inner):
        # skip whitespace
        m_ws = re.match(r"\s+", inner[pos:])
        if m_ws:
            pos += m_ws.end()
            continue
        # try sticky
        m = sticky_re.match(inner, pos)
        if m:
            title = unescape(m.group(1).strip())
            body = unescape(m.group(2).strip())
            out.append(sticky_note_html(title, body))
            pos = m.end()
            continue
        # try <p ...>
        m = re.match(r"<p(\s[^>]*)?>(.*?)</p>", inner[pos:], re.DOTALL)
        if m:
            attrs = m.group(1) or ""
            content = m.group(2)
            pos += m.end()
            if not italic_seen and "font-style: italic" in attrs:
                italic_seen = True
                continue
            out.append(inline_to_md(content))
            continue
        # try <h3 ...>
        m = re.match(r"<h3(\s[^>]*)?>(.*?)</h3>", inner[pos:], re.DOTALL)
        if m:
            content = m.group(2)
            pos += m.end()
            out.append(f"### {inline_to_md(content)}")
            continue
        # try <blockquote ...>
        m = re.match(r"<blockquote(\s[^>]*)?>(.*?)</blockquote>", inner[pos:], re.DOTALL)
        if m:
            content = inline_to_md(m.group(2))
            pos += m.end()
            quoted = "\n".join("> " + line for line in content.splitlines())
            out.append(quoted)
            continue
        # unknown char — advance one to avoid infinite loop
        pos += 1
    return out


def inline_to_md(s: str) -> str:
    s = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", s, flags=re.DOTALL)
    s = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", s, flags=re.DOTALL)
    s = re.sub(r"<br\s*/?>", "  \n", s)
    # Strip any remaining tags
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(s).strip()


def sticky_note_html(title: str, body: str) -> str:
    return (
        '<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); '
        "border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);\">"
        '<div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">'
        f"{title}</div>"
        '<div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">'
        f"{body}</div></div>"
    )


def build_markdown(slug: str, meta: dict, body_blocks: list[str]) -> str:
    fm_lines = [
        "---",
        f'num: "{meta["num"]}"',
        f"en: {yaml_str(meta['en'])}",
        f"ko: {yaml_str(meta['ko'])}",
        f"group: {GROUP_OF[slug]}",
        f"read_time: {yaml_str(meta['read_time'])}",
        f"h1_lead: {yaml_str(meta['h1_lead'])}",
        f"lead: {yaml_str(meta['lead'])}",
        f"italic: {yaml_str(meta['italic'])}",
        f"workshop_text: {yaml_str(meta['workshop_text'])}",
        "---",
        "",
    ]
    body = "\n\n".join(body_blocks)
    return "\n".join(fm_lines) + body + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug in NOTE_FILES:
        src = SITE / f"notes-{slug}.html"
        if not src.exists():
            print(f"skip (missing): {src}")
            continue
        html = src.read_text(encoding="utf-8")
        meta = parse_meta(html)
        inner = extract_article_inner(html)
        blocks = html_to_markdown(inner)
        md = build_markdown(slug, meta, blocks)
        out = OUT_DIR / f"{slug}.md"
        out.write_text(md, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}  (num={meta['num']}, body blocks={len(blocks)})")


if __name__ == "__main__":
    main()
