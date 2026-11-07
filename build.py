#!/usr/bin/env python3
"""Build the static project showcase into docs/ (published by GitHub Pages from /docs).

    python3 build.py --base https://vitamindb.github.io
    python3 build.py --base https://example.dev --cname example.dev
    python3 build.py --google-verify TOKEN --yandex-verify TOKEN

Sources live in src/: content.py (all texts, EN + RU), templates/base.html, style.css,
fonts/. Screenshots are read from the project repositories on every build (REPOS_ROOT in
content.py, or --repos), converted to WebP and cached in docs/img by modification time.
After writing, the build checks every internal link, image and anchor and a few SEO rules;
it exits non-zero if something is wrong.

Only the Python standard library and Pillow are used (ffmpeg for the video poster).
"""

import argparse
import datetime as dt
import glob
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from string import Template
from urllib.parse import urlparse, urljoin

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
LANGS = ("en", "ru")
FULL_W, THUMB_W = 1600, 800
WEBP_Q = 82

esc = lambda s: html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- setup
def load_content():
    spec = importlib.util.spec_from_file_location("content", os.path.join(SRC, "content.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Site:
    def __init__(self, args, content):
        self.args = args
        self.c = content
        base = args.base.rstrip("/")
        u = urlparse(base)
        if u.scheme not in ("http", "https") or not u.netloc:
            sys.exit(f"--base must be an absolute URL, got {args.base!r}")
        self.origin = f"{u.scheme}://{u.netloc}"
        self.prefix = u.path.rstrip("/")          # "" for a user site or custom domain
        self.out = os.path.abspath(args.out)
        self.repos = os.path.expanduser(args.repos or content.REPOS_ROOT)
        self.written = set()                       # every file the build produced
        self.lastmod = args.lastmod or dt.date.today().isoformat()
        self.template = Template(open(os.path.join(SRC, "templates", "base.html"), encoding="utf-8").read())

    # URL helpers ---------------------------------------------------------
    def path(self, lang, slug=None):
        p = self.prefix + ("/ru" if lang == "ru" else "") + (f"/{slug}" if slug else "") + "/"
        return p

    def abs(self, path):
        return self.origin + path

    def asset(self, rel):
        return f"{self.prefix}/{rel}"

    # file helpers --------------------------------------------------------
    def write(self, rel, data, binary=False):
        dst = os.path.join(self.out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        mode = "wb" if binary else "w"
        with open(dst, mode, **({} if binary else {"encoding": "utf-8", "newline": "\n"})) as f:
            f.write(data)
        self.written.add(os.path.normpath(rel))

    def keep(self, rel):
        self.written.add(os.path.normpath(rel))

    def fresh(self, rel, *sources):
        dst = os.path.join(self.out, rel)
        if not os.path.exists(dst):
            return False
        m = os.path.getmtime(dst)
        return all(os.path.getmtime(s) <= m for s in sources)


# --------------------------------------------------------------------------- images
def src_for(item, lang):
    """Image path for a language: a Russian-interface screenshot on /ru/ pages when there is one."""
    return item.get("src_ru", item["src"]) if lang == "ru" else item["src"]


class Images:
    """Converts repository screenshots to WebP (full ≤1600 px, thumb ≤800 px)."""

    def __init__(self, site):
        self.s = site
        self.cache = {}

    def src_path(self, rel):
        return os.path.join(self.s.repos, rel)

    def get(self, rel):
        if rel in self.cache:
            return self.cache[rel]
        src = self.src_path(rel)
        if not os.path.exists(src):
            raise FileNotFoundError(f"image not found: {src}")
        parts = rel.split("/")
        g = "-".join(parts[1:3]) if parts[0] == "alexeyev.dev" and len(parts) > 3 and parts[1] == "blog" else parts[0]
        group = re.sub(r"[^a-z0-9-]+", "-", g.lower().replace("_", "-"))
        stem = os.path.splitext(parts[-1])[0]
        stem = re.sub(r"[^A-Za-z0-9-]+", "-", stem).strip("-").lower() or hashlib.sha1(rel.encode()).hexdigest()[:8]
        out = {}
        img = None
        for key, width in (("full", FULL_W), ("thumb", THUMB_W)):
            name = f"img/{group}/{stem}.webp" if key == "full" else f"img/{group}/{stem}-{width}.webp"
            if not self.s.fresh(name, src):
                if img is None:
                    img = Image.open(src)
                    img.load()
                    if img.mode not in ("RGB", "RGBA"):
                        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
                im = img
                if im.width > width:
                    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
                dst = os.path.join(self.s.out, name)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                im.save(dst, "WEBP", quality=WEBP_Q, method=6)
            self.s.keep(name)
            with Image.open(os.path.join(self.s.out, name)) as done:
                out[key] = {"url": self.s.asset(name), "rel": name, "w": done.width, "h": done.height}
        out["src"] = src
        self.cache[rel] = out
        return out


def img_tag(im, alt, *, eager=False, variant="thumb", sizes=None, cls=None):
    v = im[variant]
    attrs = [f'src="{esc(v["url"])}"', f'width="{v["w"]}"', f'height="{v["h"]}"', f'alt="{esc(alt)}"']
    if sizes:
        attrs.append(f'srcset="{esc(im["thumb"]["url"])} {im["thumb"]["w"]}w, {esc(im["full"]["url"])} {im["full"]["w"]}w"')
        attrs.append(f'sizes="{esc(sizes)}"')
    if eager:
        attrs.append('fetchpriority="high"')
    else:
        attrs.append('loading="lazy"')
        attrs.append('decoding="async"')
    if cls:
        attrs.append(f'class="{cls}"')
    return "<img " + " ".join(attrs) + ">"


# --------------------------------------------------------------------------- OG images
FONT_DISPLAY = os.path.join(SRC, "fonts", "unbounded-700.ttf")
TEXT_FONTS = [
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
]
MONO_FONTS = [
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
]


def _font(cands, size):
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype(FONT_DISPLAY, size)


def _wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def make_og(site, rel, title, line, kicker, shots):
    """1200×630: dark engineering-paper background, title, one line, screenshot(s) on the right."""
    srcs = [s["src"] for s in shots]
    if site.fresh(rel, *srcs, os.path.join(SRC, "content.py"), __file__):
        site.keep(rel)
        return
    W, H = 1200, 630
    bg, ink, ink2, accent, line_c = (18, 19, 22), (236, 232, 223), (176, 171, 160), (236, 135, 99), (40, 41, 47)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 30):
        d.line([(x, 0), (x, H)], fill=(24, 25, 29))
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(24, 25, 29))
    # screenshots: bleed off the right and bottom edges
    x0, y0 = 600, 150
    for i, path in enumerate(srcs[:3][::-1]):
        k = len(srcs[:3]) - 1 - i
        shot = Image.open(path).convert("RGB")
        sw = 740
        shot = shot.resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
        ox, oy = x0 + k * 48, y0 - k * 48
        shadow = Image.new("RGBA", (shot.width + 60, shot.height + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle([30, 30, shot.width + 30, shot.height + 30], fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        im.paste(shadow, (ox - 30 + 8, oy - 30 + 14), shadow)
        d.rectangle([ox - 7, oy - 7, ox + shot.width + 6, oy + shot.height + 6], fill=(30, 31, 36), outline=line_c)
        im.paste(shot, (ox, oy))
    # left panel so text stays readable
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    for x in range(0, 620):
        a = 255 if x < 520 else int(255 * (620 - x) / 100)
        pd.line([(x, 0), (x, H)], fill=bg + (a,))
    im.paste(panel, (0, 0), panel)
    d = ImageDraw.Draw(im)
    pad = 64
    # kicker
    mono = _font(MONO_FONTS, 20)
    d.rectangle([pad, 70, pad + 38, 108], fill=accent)
    fk = ImageFont.truetype(FONT_DISPLAY, 15)
    d.text((pad + 19, 89), "VA", font=fk, fill=bg, anchor="mm")
    d.text((pad + 56, 89), kicker, font=mono, fill=ink2, anchor="lm")
    # title, shrink to fit
    size = 76
    while size > 36:
        ft = ImageFont.truetype(FONT_DISPLAY, size)
        tl = _wrap(d, title, ft, 470)
        if len(tl) <= 2 and all(d.textlength(t, font=ft) <= 470 for t in tl):
            break
        size -= 4
    y = 170
    for t in tl:
        d.text((pad, y), t, font=ft, fill=ink)
        y += int(size * 1.12)
    y += 22
    fb = _font(TEXT_FONTS, 25)
    for t in _wrap(d, line, fb, 450)[:5]:
        d.text((pad, y), t, font=fb, fill=ink2)
        y += 36
    d.rectangle([0, H - 10, W, H], fill=accent)
    d.text((pad, H - 50), "github.com/VitaminDB", font=mono, fill=ink2, anchor="ls")
    dst = os.path.join(site.out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    site.keep(rel)


# --------------------------------------------------------------------------- pieces
ICON_GH = ('<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>')
ICON_ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

SPDX = {"MIT": "https://spdx.org/licenses/MIT.html", "Apache-2.0": "https://spdx.org/licenses/Apache-2.0.html"}


def licences(expr):
    return [SPDX[x] for x in re.findall(r"[A-Za-z0-9.\-]+", expr) if x in SPDX]


def code_html(code):
    out = []
    for ln in code.split("\n"):
        m = re.match(r"^(.*?)(\s+#.*)$", ln)
        if m:
            out.append(esc(m.group(1)) + '<span class="c">' + esc(m.group(2)) + "</span>")
        else:
            out.append(esc(ln))
    return "\n".join(out)


def stat_items(stats, lang, cls):
    items = []
    for st in stats:
        unit = f'<small>{esc(st["unit"])}</small>' if st.get("unit") else ""
        items.append(f'<div><dt>{esc(st["label"][lang])}</dt><dd>{esc(st["value"])}{unit}</dd></div>')
    return f'<dl class="{cls}">' + "".join(items) + "</dl>"


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


# --------------------------------------------------------------------------- page shell
def render(site, *, lang, rel, title, description, main, canonical=None, alternates=None,
           og_image, og_type="website", ld=None, body_class="", verify=False, noindex=False,
           lang_url=None, og_title=None):
    c = site.c
    ui = c.UI[lang]
    other = "ru" if lang == "en" else "en"
    alt_html = ""
    if alternates:
        for code, href in alternates:
            alt_html += f'<link rel="alternate" hreflang="{code}" href="{esc(href)}">\n'
    ver = ""
    if verify:
        if site.args.google_verify:
            ver += f'<meta name="google-site-verification" content="{esc(site.args.google_verify)}">\n'
        if site.args.yandex_verify:
            ver += f'<meta name="yandex-verification" content="{esc(site.args.yandex_verify)}">\n'
    footer = footer_html(site, lang)
    page = site.template.substitute(
        lang=lang,
        title=esc(title),
        description=esc(description),
        author=esc(c.SITE["name"][lang]),
        robots='<meta name="robots" content="noindex">\n' if noindex else "",
        verify=ver,
        canonical=esc(canonical or site.abs(site.path(lang))),
        alternates=alt_html,
        prefix=site.prefix,
        css_ver=site.css_ver,
        og_type=og_type,
        site_name=esc(c.SITE["name"][lang]),
        og_title=esc(og_title or title),
        og_locale="en_US" if lang == "en" else "ru_RU",
        og_locale_alt="ru_RU" if lang == "en" else "en_US",
        og_image=esc(og_image),
        jsonld="\n".join(jsonld(x) for x in (ld or [])),
        body_class=body_class,
        skip=esc(ui["skip"]),
        home_url=site.path(lang),
        home_label=esc(ui["home"]),
        nav_label="Main" if lang == "en" else "Основная навигация",
        nav_projects=esc(ui["nav_projects"]),
        nav_blog=esc(site.blog.UI[lang]["nav"]),
        blog_url=site.path(lang, "blog"),
        nav_vibe=esc(ui["nav_vibe"]),
        nav_contact=esc(ui["nav_contact"]),
        lang_url=esc(lang_url or site.path(other)),
        lang_other_code=other,
        lang_other=esc(ui["lang_other"]),
        lang_other_short=esc(ui["lang_other_short"]),
        main=main,
        footer=footer,
    )
    site.write(rel, page)


def footer_html(site, lang):
    c = site.c
    ui = c.UI[lang]
    links = "".join(f'<a href="{site.path(lang, p["slug"])}">{esc(p["name"])}</a>' for p in c.PROJECTS)
    year = site.lastmod[:4]
    return (f'    <div><p>© {year} {esc(c.SITE["name"][lang])} · <a href="{esc(c.SITE["contacts"]["github"])}" rel="me">GitHub</a>'
            f' · <a href="{esc(c.SITE["contacts"]["linkedin"])}" rel="me">LinkedIn</a>'
            f' · <a href="{esc(c.SITE["contacts"]["paypal"])}">PayPal</a></p><p>{esc(ui["footer_note"])}</p></div>\n'
            f'    <nav aria-label="{esc(ui["other_nav"])}">{links}</nav>')


def contact_rows(site, lang):
    c = site.c
    ct = c.SITE["contacts"]
    ui = c.UI[lang]
    rows = [
        ("LinkedIn", ct.get("linkedin"), "in/vitaly-alexeyev", "me"),
        ("GitHub", ct["github"], "github.com/VitaminDB", "me"),
        ("X", ct["x"], "@alexeyev_vitaly", "me"),
        (ui["email"], "mailto:" + ct["email"], ct["email"], None),
        ("YouTube", ct.get("youtube"), (ct.get("youtube") or "").split("//")[-1], "me"),
        ("Discord", ct.get("discord"), (ct.get("discord") or "").split("//")[-1], None),
        ("PayPal", ct["paypal"], "paypal.me/vitamindbnfkz", None),
    ]
    out = []
    for k, href, label, rel in rows:
        if not href:
            continue
        r = f' rel="{rel}"' if rel else ""
        out.append(f'<li><a href="{esc(href)}"{r}><span class="k">{esc(k)}</span><span class="v">{esc(label)}</span><span class="arr" aria-hidden="true">→</span></a></li>')
    return '<ul class="contacts">' + "".join(out) + "</ul>"


def person_ld(site):
    c = site.c
    ct = c.SITE["contacts"]
    same = [ct["github"], ct["x"]] + [u for u in (ct.get("linkedin"), ct.get("youtube")) if u]
    return {
        "@type": "Person",
        "@id": site.abs(site.path("en")) + "#person",
        "name": c.SITE["name"]["en"],
        "alternateName": [c.SITE["name"]["ru"], c.SITE["handle"]],
        "jobTitle": "Systems engineer",
        "description": c.SITE["role"]["en"],
        "url": site.abs(site.path("en")),
        "email": "mailto:" + ct["email"],
        "address": {"@type": "PostalAddress", "addressLocality": "Kostanay", "addressCountry": "KZ"},
        "knowsAbout": ["Rust", "CUDA", "GPU programming", "Machine learning inference", "Quantization",
                       "Wayland", "Linux desktop software", "Embedded systems"],
        "sameAs": same,
    }


# --------------------------------------------------------------------------- hub
def build_hub(site, imgs, lang):
    c = site.c
    S, ui = c.SITE, c.UI[lang]
    hub = S["hub"]
    name = S["name"][lang]
    first, _, last = name.partition(" ")
    ct = S["contacts"]

    # vibe: first sentence as heading, the rest as body — together the text is verbatim
    vibe = S["vibe"][lang]
    head, rest = vibe.split(". ", 1)
    head += "."

    cards = []
    for i, p in enumerate(c.PROJECTS, 1):
        im = imgs.get(src_for(p["hero"], lang))
        chips = "".join(f"<li class=\"chip\">{esc(t)}</li>" for t in p["stack"][:3])
        if p["aur"]:
            chips += '<li class="chip">AUR</li>'
        cards.append(
            f'<li class="card">'
            f'<div class="card-media">{img_tag(im, p["hero"]["alt"][lang])}</div>'
            f'<div class="card-body"><div class="card-top"><span class="card-num">{i:02d}</span></div>'
            f'<h3><a href="{site.path(lang, p["slug"])}">{esc(p["name"])}</a></h3>'
            f'<p>{esc(p["card"][lang])}</p><ul class="chips" aria-label="{esc(ui["stack"])}">{chips}</ul></div></li>')

    bg = "".join(f'<p class="lead-p">{esc(t)}</p>' for t in hub["background"][lang])
    skills = "".join(f'<li class="chip">{esc(s)}</li>' for s in hub["skills"])

    main = f"""
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow rise">@{esc(S["handle"])} · {esc(S["location"][lang])}</p>
      <h1 id="hero-h" class="rise d1">{esc(first)} <span class="accent">{esc(last)}</span></h1>
      <p class="role rise d2">{esc(S["role"][lang])}</p>
      <p class="intro rise d3">{esc(hub["intro"][lang])}</p>
      <div class="meta-row rise d4"><span class="avail">{esc(S["availability"][lang])}</span></div>
      <div class="actions rise d5">
        <a class="btn" href="{esc(ct["github"])}" rel="me">{ICON_GH}<span>github.com/VitaminDB</span></a>
        <a class="btn ghost" href="{esc(ct["linkedin"])}" rel="me">LinkedIn</a>
        <a class="btn ghost" href="mailto:{esc(ct["email"])}">{esc(ct["email"])}</a>
      </div>
    </div>
    <div class="rise d3">
      {stat_items(hub["stats"], lang, "specs")}
      <p class="spec-note">{esc(S["hardware"][lang])}</p>
    </div>
  </div>
</section>
<section class="vibe" id="vibe" aria-labelledby="vibe-h">
  <div class="wrap">
    <p class="eyebrow">{esc(ui["vibe_label"])}</p>
    <h2 id="vibe-h">{esc(head)}</h2>
    <p class="vibe-text">{esc(rest)}</p>
    <p class="vibe-more">{esc(ui["vibe_more"])}</p>
  </div>
</section>
<section class="section" id="projects" aria-labelledby="projects-h">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">01</span><h2 id="projects-h">{esc(ui["projects_h"])}</h2><p>{esc(ui["projects_sub"])}</p></div>
    <ul class="cards">{"".join(cards)}</ul>
  </div>
</section>
<section class="section" aria-label="{esc(ui["background_h"])} / {esc(ui["contact_h"])}">
  <div class="wrap two-col">
    <div id="background">
      <div class="sec-head"><span class="sec-num">02</span><h2>{esc(ui["background_h"])}</h2></div>
      {bg}
      <ul class="chips" aria-label="Skills">{skills}</ul>
    </div>
    <div id="contact">
      <div class="sec-head"><span class="sec-num">03</span><h2>{esc(ui["contact_h"])}</h2><p>{esc(ui["contact_sub"])}</p></div>
      {contact_rows(site, lang)}
    </div>
  </div>
</section>
"""
    url_en, url_ru = site.abs(site.path("en")), site.abs(site.path("ru"))
    canonical = url_en if lang == "en" else url_ru
    person = person_ld(site)
    website = {
        "@type": "WebSite", "@id": url_en + "#website", "url": url_en,
        "name": S["name"]["en"] + " — projects", "inLanguage": ["en", "ru"],
        "author": {"@id": person["@id"]}, "publisher": {"@id": person["@id"]},
    }
    profile = {
        "@type": "ProfilePage", "@id": canonical + "#page", "url": canonical,
        "name": hub["title"][lang], "inLanguage": lang,
        "isPartOf": {"@id": website["@id"]}, "mainEntity": {"@id": person["@id"]},
        "hasPart": [{"@type": "SoftwareApplication", "name": p["name"], "url": site.abs(site.path(lang, p["slug"]))} for p in c.PROJECTS],
    }
    ld = [{"@context": "https://schema.org", "@graph": [person, website, profile]}]
    og_rel = f"og/home-{lang}.jpg"
    make_og(site, og_rel, S["name"][lang], S["role"][lang], "@VitaminDB · " + S["location"][lang],
            [imgs.get(c.PROJECTS[i]["hero"]["src"]) for i in (0, 2, 4)])
    render(site, lang=lang, rel=("ru/" if lang == "ru" else "") + "index.html",
           title=hub["title"][lang], description=hub["description"][lang], main=main,
           canonical=canonical,
           alternates=[("en", url_en), ("ru", url_ru), ("x-default", url_en)],
           og_image=site.abs(site.asset(og_rel)), ld=ld, body_class="hub", verify=True,
           og_title=hub["title"][lang])


# --------------------------------------------------------------------------- project page
def build_project(site, imgs, lang, idx):
    c = site.c
    S, ui = c.SITE, c.UI[lang]
    p = c.PROJECTS[idx]
    slug = p["slug"]
    hero = imgs.get(src_for(p["hero"], lang))
    url_en, url_ru = site.abs(site.path("en", slug)), site.abs(site.path("ru", slug))
    canonical = url_en if lang == "en" else url_ru
    home = site.path(lang)

    gallery_items = list(p.get("gallery", []))
    if p.get("gallery_glob"):
        found = sorted(f for f in glob.glob(os.path.join(site.repos, p["gallery_glob"]))
                       if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
        for f in found:
            rel = os.path.relpath(f, site.repos)
            words = re.sub(r"[-_]+", " ", os.path.splitext(os.path.basename(f))[0]).strip()
            alt = {l: f'{p["glob_alt"][l]}: {words}' for l in LANGS}
            gallery_items.append({"src": rel, "alt": alt, "caption": alt})
        if found and p["hero"]["src"] not in [os.path.relpath(f, site.repos) for f in found]:
            pass  # the themes collage stays the hero; new screenshots fill the gallery
    gal = [(g, imgs.get(src_for(g, lang))) for g in gallery_items]

    n = 0
    def sec(title, body, sid, extra_cls=""):
        nonlocal n
        n += 1
        return (f'<section class="section {extra_cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">'
                f'<div class="sec-head"><span class="sec-num">{n:02d}</span><h2 id="{sid}-h">{esc(title)}</h2></div>'
                f'{body}</div></section>')

    facts = [(ui["licence"], p["licence"]), (ui["platform"], p["platform"][lang]),
             (ui["packages"], ", ".join(p["aur"]) + " (AUR)" if p["aur"] else ("Cargo" if lang == "en" else "Cargo, из исходников")),
             (ui["status"], p["status"][lang])]
    facts_html = '<dl class="facts">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts) + "</dl>"
    buttons = f'<a class="btn" href="{esc(p["repo"])}">{ICON_GH}<span>{esc(ui["on_github"])}</span></a>'
    for pkg in p["aur"]:
        buttons += f'<a class="btn ghost" href="https://aur.archlinux.org/packages/{esc(pkg)}">{esc(ui["on_aur"])}: {esc(pkg)}</a>'

    parts = []
    parts.append(f"""
<nav class="crumbs wrap" aria-label="{esc(ui["breadcrumb"])}"><ol><li><a href="{home}">{esc(S["name"][lang])}</a></li><li><a href="{home}#projects">{esc(ui["projects_h"])}</a></li><li aria-current="page">{esc(p["name"])}</li></ol></nav>
<section class="p-hero" aria-labelledby="p-h">
  <div class="wrap">
    <p class="eyebrow rise">{idx + 1:02d} / {len(c.PROJECTS):02d} · {esc(" · ".join(p["stack"]))}</p>
    <h1 id="p-h" class="rise d1">{esc(p["name"])}</h1>
    <p class="p-lead rise d2">{esc(p["tagline"][lang])}</p>
    <div class="rise d3">{facts_html}</div>
    <div class="actions rise d4">{buttons}</div>
    <figure class="shot-hero rise d4"><div class="frame">{img_tag(hero, p["hero"]["alt"][lang], eager=True, variant="full", sizes="(max-width: 1240px) 100vw, 1180px")}</div>
    <figcaption>{esc(p["hero"]["caption"][lang])}</figcaption></figure>
    <div style="margin-top:clamp(32px,5vw,56px)">{stat_items(p["stats"], lang, "statbar")}</div>
  </div>
</section>""")

    what_body = '<div class="prose">' + "".join(f"<p>{esc(t)}</p>" for t in p["what"][lang]) + "</div>"
    for a in p.get("animations", []):
        url, src = project_media(site, a["src"], slug)
        with Image.open(src) as g:
            w, h = g.size
        what_body += (f'<figure class="post-gif"><div class="frame"><img src="{esc(url)}" width="{w}" height="{h}" '
                      f'alt="{esc(a["alt"][lang])}" loading="lazy" decoding="async"></div>'
                      f'<figcaption>{esc(a["caption"][lang])}</figcaption></figure>')
    parts.append(sec(ui["what_h"], what_body, "what"))

    video_ld = None
    v = p.get("video")
    if v:
        vsrc = os.path.expanduser(v["file"])
        vrel = "media/" + os.path.basename(vsrc)
        dst = os.path.join(site.out, vrel)
        if not (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(vsrc) and os.path.getmtime(dst) >= os.path.getmtime(vsrc)):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(vsrc, dst)
        site.keep(vrel)
        poster_rel = f"img/{slug}/video-poster.webp"
        if not site.fresh(poster_rel, vsrc) and shutil.which("ffmpeg"):
            tmp = os.path.join(site.out, f"img/{slug}/.poster.png")
            os.makedirs(os.path.dirname(tmp), exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(v.get("poster_at", 1)), "-i", vsrc,
                            "-frames:v", "1", tmp], check=True)
            pi = Image.open(tmp).convert("RGB")
            pi = pi.resize((FULL_W, round(pi.height * FULL_W / pi.width)), Image.LANCZOS)
            pi.save(os.path.join(site.out, poster_rel), "WEBP", quality=WEBP_Q, method=6)
            os.remove(tmp)
        site.keep(poster_rel)
        with Image.open(os.path.join(site.out, poster_rel)) as pim:
            pw, ph = pim.size
        links = f'<a class="btn ghost" href="{site.asset(vrel)}" download>{esc(ui["video_file"])} · {os.path.getsize(vsrc) / 1e6:.1f} MB</a>'
        if v.get("youtube_id"):
            links = f'<a class="btn" href="https://www.youtube.com/watch?v={esc(v["youtube_id"])}">{esc(ui["video_youtube"])}</a>' + links
        body = (f'<figure class="video" style="margin:0"><div class="frame">'
                f'<video controls preload="none" playsinline width="{pw}" height="{ph}" poster="{site.asset(poster_rel)}" aria-label="{esc(v["title"][lang])}">'
                f'<source src="{site.asset(vrel)}" type="video/mp4"></video></div>'
                f'<figcaption>{esc(v["caption"][lang])}</figcaption></figure><div class="video-links">{links}</div>')
        parts.append(sec(ui["video_h"], body, "video"))
        video_ld = {
            "@type": "VideoObject", "name": v["title"][lang], "description": v["caption"][lang],
            "thumbnailUrl": site.abs(site.asset(poster_rel)), "contentUrl": site.abs(site.asset(vrel)),
            "uploadDate": dt.date.fromtimestamp(os.path.getmtime(vsrc)).isoformat(),
            "duration": v.get("duration", ""), "inLanguage": "en",
        }
        if v.get("youtube_id"):
            video_ld["embedUrl"] = f"https://www.youtube.com/embed/{v['youtube_id']}"

    feats = "".join(f"<li>{esc(f)}</li>" for f in p["features"][lang])
    parts.append(sec(ui["features_h"], f'<ul class="features">{feats}</ul>', "features"))
    if p.get("apps"):
        t_apps = "Applications" if lang == "en" else "Приложения"
        parts.append(sec(t_apps, apps_section_html(site, imgs, p, lang), "apps"))


    if p.get("perf"):
        heads = [ui["col_model"], ui["col_prefill"], ui["col_decode"], ui["col_notes"]]
        rows = "".join("<tr>" + f"<td>{esc(r[0])}</td>" + "".join(f'<td class="num">{esc(x)}</td>' for x in r[1:3]) + f"<td>{esc(r[3])}</td></tr>" for r in p["perf"]["rows"])
        body = (f'<div class="table-wrap"><table><thead><tr>{"".join(f"<th scope=col>{esc(h)}</th>" for h in heads)}</tr></thead>'
                f'<tbody>{rows}</tbody></table></div><p class="perf-note">{esc(p["perf"]["note"][lang])}</p>'
                f'<p class="hw-note">{esc(S["hardware"][lang])}</p>')
        parts.append(sec(ui["perf_h"], body, "performance"))

    inst = p["install"]
    body = (f'<div class="install"><pre><code>{code_html(inst["code"])}</code></pre><p>{esc(inst["note"][lang])}</p>'
            f'<p><a href="{esc(p["readme"])}">{esc(ui["install_readme"])} →</a></p></div>')
    parts.append(sec(ui["install_h"], body, "install"))

    lim = "".join(f"<li>{esc(t)}</li>" for t in p["requirements"][lang])
    parts.append(sec(ui["req_h"], f'<ul class="limits">{lim}</ul>', "requirements"))

    if gal:
        items = []
        for g, im in gal:
            items.append(f'<li><figure><a href="{esc(im["full"]["url"])}"><div class="frame">{img_tag(im, g["alt"][lang])}</div>'
                         f'<span class="visually-hidden"> ({esc(ui["gallery_open"])})</span></a>'
                         f'<figcaption>{esc(g["caption"][lang])}</figcaption></figure></li>')
        parts.append(sec(ui["gallery_h"], f'<ul class="gallery">{"".join(items)}</ul>', "screenshots"))

    parts.append(f"""
<section class="vibe compact" id="how-built" aria-labelledby="how-built-h">
  <div class="wrap">
    <p class="eyebrow">{esc(ui["vibe_label"])}</p>
    <h2 id="how-built-h">{esc(ui["built_h"])}</h2>
    <p class="vibe-text">{esc(p["built"][lang])}</p>
    <p class="vibe-more"><a href="{home}#vibe">{esc(S["vibe"][lang].split(". ")[0])}.</a> <a href="{esc(p["repo"])}">{esc(p["repo"].replace("https://", ""))}</a></p>
  </div>
</section>""")

    others = []
    for q in c.PROJECTS:
        if q is p:
            continue
        others.append(f'<li><a href="{site.path(lang, q["slug"])}"><b>{esc(q["name"])}</b><span>{esc(q["card"][lang].split(". ")[0].split(": ")[0])}</span></a></li>')
    n += 1
    parts.append(f'<nav class="section" aria-labelledby="others-h"><div class="wrap"><div class="sec-head"><span class="sec-num">{n:02d}</span>'
                 f'<h2 id="others-h">{esc(ui["others_h"])}</h2></div><ul class="others">{"".join(others)}</ul></div></nav>')

    person = person_ld(site)
    app = {
        "@type": ["SoftwareApplication", "SoftwareSourceCode"],
        "@id": canonical + "#software",
        "name": p["name"],
        "description": p["description"][lang],
        "abstract": p["tagline"][lang],
        "url": canonical,
        "mainEntityOfPage": canonical,
        "codeRepository": p["repo"],
        "sameAs": [p["repo"]] + [f"https://aur.archlinux.org/packages/{x}" for x in p["aur"]],
        "applicationCategory": p["category"],
        "operatingSystem": "Linux",
        "programmingLanguage": "Rust",
        "license": licences(p["licence"]),
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "@id": person["@id"], "name": S["name"]["en"], "url": site.abs(site.path("en"))},
        "image": site.abs(site.asset(f"og/{slug}-{lang}.jpg")),
        "screenshot": [site.abs(hero["full"]["url"])] + [site.abs(im["full"]["url"]) for _, im in gal],
        "inLanguage": lang,
        "featureList": p["features"][lang],
    }
    if p["aur"]:
        app["downloadUrl"] = f"https://aur.archlinux.org/packages/{p['aur'][0]}"
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": S["name"][lang], "item": site.abs(home)},
        {"@type": "ListItem", "position": 2, "name": p["name"], "item": canonical}]}
    graph = [app, crumbs] + ([video_ld] if video_ld else [])
    ld = [{"@context": "https://schema.org", "@graph": graph}]

    og_rel = f"og/{slug}-{lang}.jpg"
    make_og(site, og_rel, p["name"], p["card"][lang].split(". ")[0].rstrip(".") + ".",
            "  ·  ".join(p["stack"]), [hero] + [im for _, im in gal[:1]])
    render(site, lang=lang, rel=("ru/" if lang == "ru" else "") + f"{slug}/index.html",
           title=p["title"][lang], description=p["description"][lang], main="\n".join(parts),
           canonical=canonical, alternates=[("en", url_en), ("ru", url_ru), ("x-default", url_en)],
           og_image=site.abs(site.asset(og_rel)), ld=ld, body_class="project",
           lang_url=site.path("ru" if lang == "en" else "en", slug), og_title=p["title"][lang])


# --------------------------------------------------------------------------- blog
def load_blog():
    spec = importlib.util.spec_from_file_location("blog", os.path.join(SRC, "blog.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def project_media(site, rel, slug):
    """Copy a project's GIF as is (animated) into docs/media/<slug>/ and return (url, abs source)."""
    src = os.path.join(site.repos, rel)
    if not os.path.exists(src):
        raise FileNotFoundError(f"media not found: {src}")
    out_rel = f"media/{slug}/{os.path.basename(rel)}"
    dst = os.path.join(site.out, out_rel)
    if not (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    site.keep(out_rel)
    return site.asset(out_rel), src


def blog_media(site, rel):
    """Copy a GIF/MP4 into docs/media/blog/<folder>/ and return (url, abs source)."""
    src = os.path.join(site.repos, rel)
    if not os.path.exists(src):
        raise FileNotFoundError(f"media not found: {src}")
    parts = rel.split("/")
    folder = parts[2] if len(parts) > 3 and parts[1] == "blog" else "misc"
    out_rel = f"media/blog/{folder}/{parts[-1]}"
    dst = os.path.join(site.out, out_rel)
    if not (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    site.keep(out_rel)
    return site.asset(out_rel), src


def blog_poster(site, src, folder):
    stem = os.path.splitext(os.path.basename(src))[0]
    rel = f"img/blog-{folder}/{stem}-poster.webp"
    if not site.fresh(rel, src) and shutil.which("ffmpeg"):
        tmp = os.path.join(site.out, f"img/blog-{folder}/.poster.png")
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", src, "-frames:v", "1", tmp], check=True)
        im = Image.open(tmp).convert("RGB")
        if im.width > FULL_W:
            im = im.resize((FULL_W, round(im.height * FULL_W / im.width)), Image.LANCZOS)
        im.save(os.path.join(site.out, rel), "WEBP", quality=WEBP_Q, method=6)
        os.remove(tmp)
    site.keep(rel)
    with Image.open(os.path.join(site.out, rel)) as p:
        return site.asset(rel), p.width, p.height


def blog_tr(v, lang):
    return v[lang] if isinstance(v, dict) else v


def blog_block(site, imgs, lang, block):
    kind = block[0]
    if kind == "p":
        return f'<p>{esc(block[1][lang])}</p>'
    if kind == "h":
        hid = block[2] if len(block) > 2 else "s-" + re.sub(r"[^a-z0-9]+", "-", block[1]["en"].lower()).strip("-")
        return f'<h2 id="{esc(hid)}">{esc(block[1][lang])}</h2>'
    if kind == "list":
        return '<ul class="limits">' + "".join(f"<li>{esc(t)}</li>" for t in block[1][lang]) + "</ul>"
    if kind == "shots":
        items = []
        for path, cap in block[1]:
            im = imgs.get(path)
            items.append(f'<li><figure><a href="{esc(im["full"]["url"])}"><div class="frame">{img_tag(im, cap[lang], sizes="(max-width: 700px) 50vw, 300px")}</div>'
                         f'<span class="visually-hidden"> ({esc(site.blog.UI[lang]["open_full"])})</span></a><figcaption>{esc(cap[lang])}</figcaption></figure></li>')
        return f'<ul class="phone-shots">{"".join(items)}</ul>'
    if kind == "wide":
        im = imgs.get(blog_tr(block[1], lang))
        cap = block[2][lang]
        return (f'<figure class="post-wide"><a href="{esc(im["full"]["url"])}"><div class="frame">{img_tag(im, cap, variant="full", sizes="(max-width: 900px) 100vw, 860px")}</div></a>'
                f'<figcaption>{esc(cap)}</figcaption></figure>')
    if kind == "gif":
        url, src = blog_media(site, block[1])
        with Image.open(src) as g:
            w, h = g.size
        cap = block[2][lang]
        cls = "post-gif tall" if h > w else "post-gif"
        return (f'<figure class="{cls}"><div class="frame"><img src="{esc(url)}" width="{w}" height="{h}" alt="{esc(cap)}" loading="lazy" decoding="async"></div>'
                f'<figcaption>{esc(cap)}</figcaption></figure>')
    if kind == "video":
        url, src = blog_media(site, block[1])
        folder = block[1].split("/")[2]
        purl, pw, ph = blog_poster(site, src, folder)
        cap = block[2][lang]
        cls = "post-video tall" if ph > pw else "post-video"
        size = os.path.getsize(src) / 1e6
        return (f'<figure class="{cls}"><div class="frame"><video controls preload="none" playsinline width="{pw}" height="{ph}" poster="{esc(purl)}" aria-label="{esc(cap)}">'
                f'<source src="{esc(url)}" type="video/mp4"></video></div>'
                f'<figcaption>{esc(cap)} · <a href="{esc(url)}" download>{esc(site.blog.UI[lang]["video_file"])}, {size:.1f} MB</a></figcaption></figure>')
    raise ValueError(f"unknown blog block {kind}")


def blog_date(d, lang):
    y, m, day = d.split("-")
    if lang == "ru":
        months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        return f"{int(day)} {months[int(m) - 1]} {y}"
    return dt.date(int(y), int(m), int(day)).strftime("%B %-d, %Y")


def post_tags(site, post):
    return list(dict.fromkeys([post["section"]] + list(post.get("tags", []))))


def h_id(block):
    return block[2] if len(block) > 2 else "s-" + re.sub(r"[^a-z0-9]+", "-", block[1]["en"].lower()).strip("-")


BLOG_JS = r"""<script>
(function(){
  var q=document.getElementById('bq'), chips=document.querySelectorAll('[data-filter]'),
      cards=document.querySelectorAll('.post-card'), secs=document.querySelectorAll('.blog-sec'),
      out=document.getElementById('site-results'), idx=null, tag='';
  var m=location.search.match(/[?&]tag=([^&]+)/); if(m){tag=decodeURIComponent(m[1]);}
  function load(cb){ if(idx) return cb(); fetch(out.dataset.index).then(function(r){return r.json()}).then(function(j){idx=j;cb()}).catch(function(){idx=[];cb()}); }
  function apply(){
    var t=(q.value||'').trim().toLowerCase(), words=t.split(/\s+/).filter(Boolean);
    chips.forEach(function(c){c.setAttribute('aria-pressed', c.dataset.filter===tag?'true':'false')});
    cards.forEach(function(c){
      var okT=!tag||(' '+c.dataset.tags+' ').indexOf(' '+tag+' ')>=0;
      var okQ=words.every(function(w){return c.dataset.text.indexOf(w)>=0});
      c.hidden=!(okT&&okQ);
    });
    secs.forEach(function(s){ s.hidden=!s.querySelector('.post-card:not([hidden])'); });
    if(!words.length){ out.hidden=true; out.innerHTML=''; return; }
    load(function(){
      var res=idx.filter(function(e){var h=(e.t+' '+e.d+' '+(e.g||'')).toLowerCase(); return words.every(function(w){return h.indexOf(w)>=0})}).slice(0,24);
      out.hidden=false;
      out.innerHTML='<h2>'+out.dataset.title+' ('+res.length+')</h2>'+(res.length?'<ul class="others">'+res.map(function(e){
        return '<li><a href="'+e.u+'"><b>'+e.t.replace(/</g,'&lt;')+'</b><span>'+e.k+' · '+e.d.replace(/</g,'&lt;')+'</span></a></li>'}).join('')+'</ul>':'<p>'+out.dataset.empty+'</p>');
    });
  }
  chips.forEach(function(c){c.addEventListener('click',function(){tag=(tag===c.dataset.filter?'':c.dataset.filter);
    history.replaceState(null,'',tag?'?tag='+encodeURIComponent(tag):location.pathname); apply();})});
  q.addEventListener('input',apply); apply();
})();
</script>"""


def build_search_index(site):
    """search-<lang>.json: projects, app pages and blog posts for the blog search box."""
    c, B = site.c, site.blog
    for lang in LANGS:
        kinds = {"en": ("project", "app", "post"), "ru": ("проект", "программа", "запись")}[lang]
        items = []
        for p in c.PROJECTS:
            items.append({"t": p["name"], "d": p["card"][lang], "u": site.path(lang, p["slug"]), "k": kinds[0]})
            for group, apps in site.app_lists.get(p["slug"], {}).get(lang, []):
                for a in apps:
                    items.append({"t": a["title"], "d": a["desc"], "u": site.path(lang, p["slug"] + "/" + a["crate"]),
                                  "k": f'{kinds[1]} {p["name"]}', "g": f'{a["name"]} {group}'})
        for post in B.POSTS:
            items.append({"t": post["title"][lang], "d": post["summary"][lang], "u": site.path(lang, "blog/" + post["slug"]),
                          "k": kinds[2], "g": " ".join(post_tags(site, post))})
        site.write(("ru/" if lang == "ru" else "") + "search.json", json.dumps(items, ensure_ascii=False))


def blog_card(site, imgs, lang, post):
    im = imgs.get(post["cover"])
    ui = site.blog.UI[lang]
    tags = post_tags(site, post)
    text = " ".join([post["title"][lang], post["summary"][lang]] + tags).lower()
    return (f'<li class="card post-card" data-tags="{esc(" ".join(tags))}" data-text="{esc(text)}"><div class="card-media">{img_tag(im, post["title"][lang])}</div>'
            f'<div class="card-body"><div class="card-top"><time class="card-num" datetime="{post["date"]}">{esc(blog_date(post["date"], lang))}</time></div>'
            f'<h3><a href="{site.path(lang, "blog/" + post["slug"])}">{esc(post["title"][lang])}</a></h3>'
            f'<p>{esc(post["summary"][lang])}</p><span class="read">{esc(ui["read"])} →</span></div></li>')


def build_blog(site, imgs):
    B = site.blog
    S = site.c.SITE
    person = person_ld(site)
    for lang in LANGS:
        ui = B.UI[lang]
        home = site.path(lang)
        secs = []
        n = 0
        for sec in B.SECTIONS:
            posts = [p for p in B.POSTS if p["section"] == sec["slug"]]
            if not posts:
                continue
            n += 1
            cards = "".join(blog_card(site, imgs, lang, p) for p in posts)
            secs.append(f'<section class="section blog-sec" id="{sec["slug"]}" aria-labelledby="{sec["slug"]}-h"><div class="wrap">'
                        f'<div class="sec-head"><span class="sec-num">{n:02d}</span><h2 id="{sec["slug"]}-h">{esc(sec["name"])}</h2>'
                        f'<p>{esc(sec["about"][lang])} · {len(posts)} {esc(ui["posts"])}</p></div>'
                        f'<ul class="cards">{cards}</ul></div></section>')
        all_tags = list(dict.fromkeys(t for p in B.POSTS for t in post_tags(site, p)))
        t_all = "All" if lang == "en" else "Все"
        toc = (f'<button type="button" class="chip" data-filter="">{esc(t_all)}</button>'
               + "".join(f'<button type="button" class="chip" data-filter="{esc(t)}">{esc(t)}</button>' for t in all_tags))
        t_search = "Search posts, projects and apps" if lang == "en" else "Поиск по записям, проектам и программам"
        t_found = "Found on the site" if lang == "en" else "Найдено на сайте"
        t_empty = "Nothing found." if lang == "en" else "Ничего не найдено."
        search_html = (f'<div class="blog-search rise d3"><label class="visually-hidden" for="bq">{esc(t_search)}</label>'
                       f'<input id="bq" type="search" placeholder="{esc(t_search)}" autocomplete="off"></div>')
        results_html = (f'<section class="section" aria-live="polite"><div class="wrap" id="site-results" hidden '
                        f'data-index="{site.prefix}{"/ru" if lang == "ru" else ""}/search.json" data-title="{esc(t_found)}" data-empty="{esc(t_empty)}"></div></section>')
        main = (f'<nav class="crumbs wrap" aria-label="{esc(site.c.UI[lang]["breadcrumb"])}"><ol><li><a href="{home}">{esc(S["name"][lang])}</a></li><li aria-current="page">{esc(ui["h1"])}</li></ol></nav>'
                f'<section class="p-hero" aria-labelledby="blog-h"><div class="wrap"><p class="eyebrow rise">@{esc(S["handle"])}</p>'
                f'<h1 id="blog-h" class="rise d1">{esc(ui["h1"])}</h1><p class="p-lead rise d2">{esc(ui["lead"])}</p>'
                f'{search_html}<div class="chips rise d3" role="group">{toc}</div></div></section>' + results_html + "".join(secs) + BLOG_JS)
        url_en, url_ru = site.abs(site.path("en", "blog")), site.abs(site.path("ru", "blog"))
        canonical = url_en if lang == "en" else url_ru
        ld = [{"@context": "https://schema.org", "@graph": [{
            "@type": "Blog", "@id": canonical + "#blog", "url": canonical, "name": ui["title"], "inLanguage": lang,
            "author": {"@id": person["@id"]},
            "blogPost": [{"@type": "BlogPosting", "headline": p["title"][lang], "url": site.abs(site.path(lang, "blog/" + p["slug"])), "datePublished": p["date"]} for p in B.POSTS],
        }]}]
        og_rel = f"og/blog-{lang}.jpg"
        make_og(site, og_rel, ui["h1"], ui["lead"], "@VitaminDB · blog", [imgs.get(p["cover"]) for p in B.POSTS[:3]])
        render(site, lang=lang, rel=("ru/" if lang == "ru" else "") + "blog/index.html", title=ui["title"], description=ui["description"],
               main=main, canonical=canonical, alternates=[("en", url_en), ("ru", url_ru), ("x-default", url_en)],
               og_image=site.abs(site.asset(og_rel)), ld=ld, body_class="blog", lang_url=site.path("ru" if lang == "en" else "en", "blog"))

        for post in B.POSTS:
            sec = next(s for s in B.SECTIONS if s["slug"] == post["section"])
            slug = "blog/" + post["slug"]
            blog_url = site.path(lang, "blog")
            body = "\n".join(blog_block(site, imgs, lang, b) for b in post["body"])
            heads = [b for b in post["body"] if b[0] == "h"]
            toc_html = ""
            if len(heads) >= 3:
                t_toc = "Contents" if lang == "en" else "Содержание"
                toc_html = (f'<nav class="post-toc" aria-label="{esc(t_toc)}"><b>{esc(t_toc)}</b><ol>'
                            + "".join(f'<li><a href="#{esc(h_id(h))}">{esc(h[1][lang])}</a></li>' for h in heads) + "</ol></nav>")
            ordered = sorted(B.POSTS, key=lambda q: (q["date"], B.POSTS.index(q)))
            k = ordered.index(post)
            pn = ""
            if k > 0:
                q = ordered[k - 1]
                pn += f'<a class="pn prev" href="{site.path(lang, "blog/" + q["slug"])}"><span>←</span> {esc(q["title"][lang])}</a>'
            if k + 1 < len(ordered):
                q = ordered[k + 1]
                pn += f'<a class="pn next" href="{site.path(lang, "blog/" + q["slug"])}">{esc(q["title"][lang])} <span>→</span></a>'
            proj_link = ""
            if sec.get("project"):
                t_proj = "Project page" if lang == "en" else "Страница проекта"
                proj_link = f' · <a href="{site.path(lang, sec["project"])}">{esc(t_proj)}: {esc(sec["project"])}</a>'
            tag_html = "".join(f'<a class="chip" href="{site.path(lang, "blog")}?tag={esc(t)}">#{esc(t)}</a>' for t in post_tags(site, post))
            discuss = ""
            if B.FOURPDA_URL:
                discuss = f'<p class="discuss"><a class="btn" href="{esc(B.FOURPDA_URL)}">{esc(ui["discuss"])} →</a></p>'
            others = [p for p in B.POSTS if p["section"] == post["section"] and p is not post]
            more = ""
            if others:
                more = (f'<nav class="section" aria-labelledby="more-h"><div class="wrap"><div class="sec-head"><span class="sec-num">→</span>'
                        f'<h2 id="more-h">{esc(ui["more_in"])}: {esc(sec["name"])}</h2></div><ul class="others">'
                        + "".join(f'<li><a href="{site.path(lang, "blog/" + p["slug"])}"><b>{esc(p["title"][lang])}</b><span>{esc(p["summary"][lang])}</span></a></li>' for p in others)
                        + "</ul></div></nav>")
            main = (f'<nav class="crumbs wrap" aria-label="{esc(site.c.UI[lang]["breadcrumb"])}"><ol><li><a href="{home}">{esc(S["name"][lang])}</a></li>'
                    f'<li><a href="{blog_url}">{esc(ui["h1"])}</a></li><li><a href="{blog_url}#{sec["slug"]}">{esc(sec["name"])}</a></li></ol></nav>'
                    f'<article class="post" aria-labelledby="post-h"><header class="p-hero"><div class="wrap">'
                    f'<p class="eyebrow rise"><time datetime="{post["date"]}">{esc(blog_date(post["date"], lang))}</time> · {esc(sec["name"])}</p>'
                    f'<h1 id="post-h" class="rise d1">{esc(post["title"][lang])}</h1><p class="p-lead rise d2">{esc(post["summary"][lang])}</p></div></header>'
                    f'<div class="wrap"><div class="chips post-tags">{tag_html}</div>{toc_html}</div>'
                    f'<div class="wrap post-body">{body}{discuss}<div class="pn-row">{pn}</div><p class="post-back"><a href="{blog_url}">← {esc(ui["back"])}</a>{proj_link}</p></div></article>{more}')
            url_en, url_ru = site.abs(site.path("en", slug)), site.abs(site.path("ru", slug))
            canonical = url_en if lang == "en" else url_ru
            cover = imgs.get(post["cover"])
            og_rel = f"og/blog-{post['slug']}-{lang}.jpg"
            shots = [cover] + [imgs.get(b[1][0][0]) for b in post["body"] if b[0] == "shots"][:1]
            make_og(site, og_rel, post["title"][lang], post["summary"][lang], sec["name"] + " · blog", shots)
            ld = [{"@context": "https://schema.org", "@graph": [{
                "@type": "BlogPosting", "@id": canonical + "#post", "headline": post["title"][lang], "description": post["summary"][lang],
                "datePublished": post["date"], "dateModified": post["date"], "inLanguage": lang, "url": canonical, "mainEntityOfPage": canonical,
                "image": [site.abs(site.asset(og_rel)), site.abs(cover["full"]["url"])],
                "author": {"@type": "Person", "@id": person["@id"], "name": S["name"]["en"], "url": site.abs(site.path("en"))},
                "isPartOf": {"@id": site.abs(blog_url) + "#blog"},
            }, {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": S["name"][lang], "item": site.abs(home)},
                {"@type": "ListItem", "position": 2, "name": ui["h1"], "item": site.abs(blog_url)},
                {"@type": "ListItem", "position": 3, "name": post["title"][lang], "item": canonical}]}]}]
            render(site, lang=lang, rel=("ru/" if lang == "ru" else "") + slug + "/index.html", title=post["title"][lang],
                   description=post["summary"][lang], main=main, canonical=canonical,
                   alternates=[("en", url_en), ("ru", url_ru), ("x-default", url_en)], og_image=site.abs(site.asset(og_rel)),
                   og_type="article", ld=ld, body_class="blog-post", lang_url=site.path("ru" if lang == "en" else "en", slug),
                   og_title=post["title"][lang])


# --------------------------------------------------------------------------- 404, misc
# --------------------------------------------------------------------------- app pages (synshell programs)
# Every application listed in the "Applications" section of a project README gets its own page
# at /<project>/<crate>/, rendered from crates/<crate>/README.md / README.ru.md with its screenshots.
import markdown as _md

GH_BLOB = "https://github.com/VitaminDB/{repo}/blob/master/{path}"


def parse_app_list(site, p):
    """[(group, [{crate, name, title, desc}])] per language from the project README tables."""
    cfg = p["apps"]
    out = {}
    for lang in LANGS:
        fn = cfg["readme"][lang]
        text = open(os.path.join(site.repos, cfg["dir"], fn), encoding="utf-8").read()
        sec = text.split(cfg["section"][lang], 1)[1]
        sec = re.split(r"\n## ", sec, maxsplit=1)[0]
        groups, cur = [], None
        for line in sec.splitlines():
            g = re.match(r"^\*\*([^*]+)\*\*\s*$", line.strip())
            if g:
                cur = (g.group(1).strip(), [])
                groups.append(cur)
                continue
            m = re.match(r"^\|\s*\[([^\]]+)\]\(crates/([^/]+)/README(?:\.ru)?\.md\)\s*\|\s*\*\*(.+?)\*\*\s*(.*?)\s*\|\s*$", line)
            if m and cur is not None:
                title = m.group(3).strip().rstrip(".")
                cur[1].append({"crate": m.group(2), "name": m.group(1), "title": title,
                               "desc": re.sub(r"`([^`]+)`", r"\1", m.group(4).strip())})
        out[lang] = [g for g in groups if g[1]]
    return out


def _app_readme(site, p, crate, lang):
    base = os.path.join(site.repos, p["apps"]["dir"], "crates", crate)
    fn = "README.ru.md" if lang == "ru" and os.path.exists(os.path.join(base, "README.ru.md")) else "README.md"
    return open(os.path.join(base, fn), encoding="utf-8").read(), fn


def split_header(text):
    """Header block <div align="center"> … </div>: tagline, AUR packages, hero image; body without it."""
    head, body = "", text
    m = re.match(r"\s*<div align=\"center\">(.*?)</div>\s*", text, re.S)
    if m:
        head, body = m.group(1), text[m.end():]
    else:  # plain README: "# name" then text
        body = re.sub(r"^\s*# .*\n", "", text, 1)
    tagline = ""
    t = re.search(r"^\*\*(.+?)\*\*\s*$", head, re.M)
    if t:
        tagline = re.sub(r"`([^`]+)`", r"\1", t.group(1)).strip()
    aur = re.findall(r"aur\.archlinux\.org/packages/([A-Za-z0-9@._+-]+)", head)
    hero = re.search(r"!\[([^\]]*)\]\(([^)\s]+)\)", head)
    hero = (hero.group(1), hero.group(2)) if hero else None
    return tagline, list(dict.fromkeys(aur)), hero, body


def build_apps(site, imgs):
    """Pages for every app of projects that declare "apps"; returns sitemap slugs."""
    c = site.c
    slugs = []
    for p in c.PROJECTS:
        if not p.get("apps"):
            continue
        apps = parse_app_list(site, p)
        site.app_lists[p["slug"]] = apps
        order = [a["crate"] for _, items in apps["en"] for a in items]
        for lang in LANGS:
            flat = [(g, a) for g, items in apps[lang] for a in items]
            for i, (group, a) in enumerate(flat):
                build_app_page(site, imgs, p, lang, group, a, flat, i, set(order))
        slugs += [f'{p["slug"]}/{cr}' for cr in order]
    return slugs


def app_hero(site, imgs, p, crate, lang):
    text, _ = _app_readme(site, p, crate, lang)
    _, _, hero, _ = split_header(text)
    if not hero:
        return None, ""
    rel = os.path.normpath(os.path.join(p["apps"]["dir"], "crates", crate, hero[1]))
    if not os.path.exists(os.path.join(site.repos, rel)):
        return None, ""
    return imgs.get(rel), hero[0]


def build_app_page(site, imgs, p, lang, group, a, flat, idx, known):
    c = site.c
    S, ui = c.SITE, c.UI[lang]
    crate, proj = a["crate"], p["slug"]
    slug = f"{proj}/{crate}"
    text, fn = _app_readme(site, p, crate, lang)
    tagline, aur, hero, body = split_header(text)
    crate_dir = os.path.join(p["apps"]["dir"], "crates", crate)
    repo_name = p["repo"].rstrip("/").split("/")[-1]

    html_body = _md.markdown(body, extensions=["tables", "fenced_code", "sane_lists"], output_format="html")

    def fix_img(m):
        attrs = m.group(1)
        src = re.search(r'src="([^"]+)"', attrs).group(1)
        alt = html.unescape(re.search(r'alt="([^"]*)"', attrs).group(1)) if 'alt="' in attrs else ""
        if re.match(r"^[a-z]+://", src):
            return m.group(0)
        rel = os.path.normpath(os.path.join(crate_dir, src))
        if not os.path.exists(os.path.join(site.repos, rel)) or not rel.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            return f'<img src="{esc(GH_BLOB.format(repo=repo_name, path=os.path.relpath(rel, p["apps"]["dir"])))}?raw=true" alt="{esc(alt or a["title"])}" loading="lazy" width="800" height="500">'
        im = imgs.get(rel)
        return (f'<a class="md-shot" href="{esc(im["full"]["url"])}">'
                + img_tag(im, alt or a["title"]) + "</a>")
    html_body = re.sub(r"<img ([^>]*?)/?>", fix_img, html_body)

    def fix_link(m):
        href = html.unescape(m.group(1))
        if re.match(r"^([a-z]+:|#|/)", href):
            return m.group(0)
        path, _, frag = href.partition("#")
        target = os.path.normpath(os.path.join(crate_dir, path))
        mm = re.match(re.escape(os.path.join(p["apps"]["dir"], "crates")) + r"/([^/]+)/README(\.ru)?\.md$", target)
        if mm and mm.group(1) in known:
            return f'href="{site.path(lang, proj + "/" + mm.group(1))}"'
        if target in (os.path.join(p["apps"]["dir"], "README.md"), os.path.join(p["apps"]["dir"], "README.ru.md")):
            return f'href="{site.path(lang, proj)}"'
        if target.endswith(("README.md", "README.ru.md")) and os.path.dirname(target) == crate_dir:
            return f'href="{site.path("ru" if lang == "en" else "en", slug)}"'
        url = GH_BLOB.format(repo=repo_name, path=os.path.relpath(target, p["apps"]["dir"]))
        return f'href="{esc(url + ("#" + frag if frag else ""))}"'
    html_body = re.sub(r'href="([^"]+)"', fix_link, html_body)
    # one h1 per page: README headings start at h2; demote stray h1
    html_body = re.sub(r"<(/?)h1>", r"<\1h2>", html_body)

    him, halt = (None, "")
    if hero:
        rel = os.path.normpath(os.path.join(crate_dir, hero[1]))
        if os.path.exists(os.path.join(site.repos, rel)):
            him, halt = imgs.get(rel), hero[0]

    url_en, url_ru = site.abs(site.path("en", slug)), site.abs(site.path("ru", slug))
    canonical = url_en if lang == "en" else url_ru
    home = site.path(lang)
    proj_url = site.path(lang, proj)
    gh_readme = GH_BLOB.format(repo=repo_name, path=f"crates/{crate}/{fn}")
    buttons = f'<a class="btn" href="{esc(gh_readme)}">{ICON_GH}<span>README</span></a>'
    for pkg in aur:
        buttons += f'<a class="btn ghost" href="https://aur.archlinux.org/packages/{esc(pkg)}">{esc(ui["on_aur"])}: {esc(pkg)}</a>'
    hero_html = ""
    if him:
        hero_html = (f'<figure class="shot-hero rise"><a href="{esc(him["full"]["url"])}"><div class="frame">'
                     f'{img_tag(him, halt or a["title"], eager=True, variant="full")}</div></a></figure>')
    prev_a = flat[idx - 1][1] if idx > 0 else None
    next_a = flat[idx + 1][1] if idx + 1 < len(flat) else None
    pn = ""
    if prev_a:
        pn += f'<a class="pn prev" href="{site.path(lang, proj + "/" + prev_a["crate"])}"><span>←</span> {esc(prev_a["title"])}</a>'
    if next_a:
        pn += f'<a class="pn next" href="{site.path(lang, proj + "/" + next_a["crate"])}">{esc(next_a["title"])} <span>→</span></a>'
    others = "".join(
        f'<li><a href="{site.path(lang, proj + "/" + b["crate"])}"><b>{esc(b["title"])}</b><span>{esc(b["name"])}</span></a></li>'
        for _, b in flat if b["crate"] != crate)
    t_apps = "Applications" if lang == "en" else "Приложения"
    t_back = f"← {p['name']}: all applications" if lang == "en" else f"← {p['name']}: все приложения"
    desc = tagline or a["desc"]
    main = f"""
<nav class="crumbs wrap" aria-label="{esc(ui["breadcrumb"])}"><ol><li><a href="{home}">{esc(S["name"][lang])}</a></li><li><a href="{proj_url}">{esc(p["name"])}</a></li><li><a href="{proj_url}#apps">{esc(t_apps)}</a></li><li aria-current="page">{esc(a["title"])}</li></ol></nav>
<section class="p-hero app-hero" aria-labelledby="p-h">
  <div class="wrap">
    <p class="eyebrow rise">{esc(p["name"])} · {esc(group)} · {esc(a["name"])}</p>
    <h1 id="p-h" class="rise">{esc(a["title"])}</h1>
    <p class="tagline rise">{esc(desc)}</p>
    <div class="btns rise">{buttons}</div>
    {hero_html}
  </div>
</section>
<article class="section md-body"><div class="wrap"><div class="md">{html_body}</div></div></article>
<nav class="section" aria-labelledby="apps-h"><div class="wrap">
  <div class="pn-row">{pn}</div>
  <p><a href="{proj_url}#apps">{esc(t_back)}</a></p>
  <h2 id="apps-h">{esc(t_apps)} {esc(p["name"])}</h2>
  <ul class="others">{others}</ul>
</div></nav>"""
    title = f'{a["title"]} — {p["name"]}'
    if len(title) > 60:
        title = title[:59] + "…"
    d = desc if len(desc) <= 160 else desc[:157].rsplit(" ", 1)[0] + "…"
    og_rel = f"og/{proj}-{crate}-{lang}.jpg"
    make_og(site, og_rel, a["title"], (desc.split(" — ")[0] if len(desc) > 90 else desc)[:110],
            f'{p["name"]}  ·  {group}', [him] if him else [imgs.get(p["hero"]["src"])])
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": S["name"][lang], "item": site.abs(home)},
        {"@type": "ListItem", "position": 2, "name": p["name"], "item": site.abs(proj_url)},
        {"@type": "ListItem", "position": 3, "name": a["title"], "item": canonical}]}
    app_ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": a["title"],
              "alternateName": a["name"], "description": d, "url": canonical, "operatingSystem": "Linux",
              "applicationCategory": "DesktopEnhancementApplication", "isPartOf": site.abs(proj_url),
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    if him:
        app_ld["screenshot"] = site.abs(him["full"]["url"])
    render(site, lang=lang, rel=("ru/" if lang == "ru" else "") + f"{slug}/index.html",
           title=title, description=d, main=main, canonical=canonical,
           alternates=[("en", url_en), ("ru", url_ru), ("x-default", url_en)],
           og_image=site.abs(site.asset(og_rel)), ld=[crumbs_ld, app_ld], body_class="project app",
           lang_url=site.path("ru" if lang == "en" else "en", slug), og_title=title)


def apps_section_html(site, imgs, p, lang):
    """Grid of app cards for the project overview page."""
    apps = site.app_lists.get(p["slug"])
    if not apps:
        return ""
    out = []
    for group, items in apps[lang]:
        cards = []
        for a in items:
            im, alt = app_hero(site, imgs, p, a["crate"], lang)
            media = f'<div class="card-media">{img_tag(im, alt or a["title"])}</div>' if im else ""
            cards.append(f'<li class="app-card"><a href="{site.path(lang, p["slug"] + "/" + a["crate"])}">{media}'
                         f'<b>{esc(a["title"])}</b><span>{esc(a["desc"])}</span></a></li>')
        out.append(f'<h3 class="app-group">{esc(group)}</h3><ul class="app-grid">{"".join(cards)}</ul>')
    return "".join(out)


def build_redirects(site):
    """Old project URLs (renamed projects): a small page with meta refresh and canonical to the new one."""
    for old, new in getattr(site.c, "REDIRECTS", {}).items():
        for lang in LANGS:
            target = site.abs(site.path(lang, new))
            rel = ("ru/" if lang == "ru" else "") + f"{old}/index.html"
            site.write(rel, f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<title>{esc(new)}</title>
<link rel="canonical" href="{esc(target)}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={esc(target)}">
</head><body><p><a href="{esc(target)}">{esc(target)}</a></p></body></html>
''')


def build_404(site):
    c = site.c
    blocks = []
    for lang in LANGS:
        ui = c.UI[lang]
        links = "".join(f'<li><a href="{site.path(lang, p["slug"])}"><b>{esc(p["name"])}</b><span>{esc(p["card"][lang].split(". ")[0].split(": ")[0])}</span></a></li>' for p in c.PROJECTS)
        blocks.append(f'<div lang="{lang}"><h2>{esc(ui["nf_title"])}</h2><p>{esc(ui["nf_text"])}</p>'
                      f'<p><a class="btn" href="{site.path(lang)}">{esc(ui["nf_back"])}</a></p>'
                      f'<ul class="others" style="margin-top:24px">{links}</ul></div>')
    main = f'<section class="nf"><div class="wrap"><h1>404</h1><div class="pair">{"".join(blocks)}</div></div></section>'
    render(site, lang="en", rel="404.html", title="404 — Page not found · Страница не найдена",
           description="This page does not exist. Эта страница не существует.", main=main,
           canonical=site.abs(site.prefix + "/404.html"), og_image=site.abs(site.asset("og/home-en.jpg")),
           noindex=True, body_class="nf-page")


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>rect{fill:#b3452a}text{fill:#fbf6ee}@media (prefers-color-scheme:dark){rect{fill:#ec8763}text{fill:#15110e}}</style><rect width="32" height="32" rx="6"/><text x="16" y="21.5" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="14">VA</text></svg>
"""


def build_static(site):
    css = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
    site.css_ver = hashlib.sha1(css.encode()).hexdigest()[:10]
    site.write("assets/style.css", css)
    for f in glob.glob(os.path.join(SRC, "fonts", "*.woff2")) + [os.path.join(SRC, "fonts", "OFL.txt")]:
        rel = "assets/fonts/" + os.path.basename(f)
        site.write(rel, open(f, "rb").read(), binary=True)
    site.write("favicon.svg", FAVICON)
    site.write(".nojekyll", "")
    # Files served verbatim from the site root: search-engine verification files and the like.
    for f in sorted(glob.glob(os.path.join(SRC, "root", "*"))):
        site.write(os.path.basename(f), open(f, "rb").read(), binary=True)
    site.write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site.abs(site.prefix + '/sitemap.xml')}\n")
    cname = os.path.join(site.out, "CNAME")
    if site.args.cname:
        site.write("CNAME", site.args.cname.strip() + "\n")
    elif os.path.exists(cname):
        site.keep("CNAME")   # keep a previously configured domain


def build_sitemap(site):
    c = site.c
    pages = [None] + [p["slug"] for p in c.PROJECTS] + list(getattr(site, "app_slugs", [])) + ["blog"] + [f"blog/{p['slug']}" for p in site.blog.POSTS]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug in pages:
        en, ru = site.abs(site.path("en", slug)), site.abs(site.path("ru", slug))
        alts = (f'    <xhtml:link rel="alternate" hreflang="en" href="{esc(en)}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="ru" href="{esc(ru)}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(en)}"/>')
        for loc in (en, ru):
            out.append(f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{site.lastmod}</lastmod>\n{alts}\n  </url>")
    out.append("</urlset>\n")
    site.write("sitemap.xml", "\n".join(out))


def prune(site):
    """Delete files in docs/ that this build did not produce (renamed images and the like)."""
    removed = 0
    for dirpath, dirnames, filenames in os.walk(site.out):
        for fn in filenames:
            rel = os.path.normpath(os.path.relpath(os.path.join(dirpath, fn), site.out))
            if rel not in site.written:
                os.remove(os.path.join(dirpath, fn))
                removed += 1
    for dirpath, dirnames, filenames in sorted(os.walk(site.out), key=lambda t: -len(t[0])):
        if dirpath != site.out and not os.listdir(dirpath):
            os.rmdir(dirpath)
    return removed


# --------------------------------------------------------------------------- checks
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.headings, self.imgs = [], set(), [], []
        self.title, self._in_title = "", False
        self.meta, self.canon, self.hreflang, self.html_lang = {}, None, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canon = a.get("href")
            if a.get("rel") == "alternate" and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a["href"]))
        if tag == "img":
            self.imgs.append(a)
        for attr in ("href", "src", "poster"):
            if a.get(attr) and not (tag == "link" and a.get("rel") in ("canonical", "alternate")):
                self.links.append(a[attr])
        if a.get("srcset"):
            self.links += [part.strip().split()[0] for part in a["srcset"].split(",") if part.strip()]

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def check(site):
    errors, warnings = [], []
    parsed = {}
    for dirpath, _, files in os.walk(site.out):
        for fn in files:
            if fn.endswith(".html") and not (dirpath == site.out and os.path.exists(os.path.join(SRC, "root", fn))):
                path = os.path.join(dirpath, fn)
                pp = PageParser()
                pp.feed(open(path, encoding="utf-8").read())
                parsed[os.path.relpath(path, site.out)] = pp

    def resolve(url, page_rel):
        """Map an internal URL to (file path in docs, fragment) or None if external."""
        if url.startswith(("mailto:", "tel:", "data:", "javascript:")):
            return None
        if url.startswith(site.origin + "/") or url == site.origin:
            url = url[len(site.origin):] or "/"
        elif re.match(r"^[a-z]+://", url) or url.startswith("//"):
            return None
        base = "/" + os.path.dirname(page_rel).replace(os.sep, "/")
        if base != "/":
            base += "/"
        full = urljoin(site.prefix + base, url)
        path, _, frag = full.partition("#")
        path = path.split("?")[0]
        if site.prefix and not path.startswith(site.prefix + "/"):
            return ("<outside prefix>" + path, frag)
        rel = path[len(site.prefix):].lstrip("/")
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        return (rel, frag)

    for rel, pp in parsed.items():
        for url in pp.links:
            r = resolve(url, rel)
            if r is None:
                continue
            target, frag = r
            fp = os.path.join(site.out, target)
            if not os.path.isfile(fp):
                errors.append(f"{rel}: broken link {url}")
                continue
            if frag and target.endswith(".html"):
                tp = parsed.get(os.path.normpath(target))
                if tp is not None and frag not in tp.ids:
                    errors.append(f"{rel}: missing anchor #{frag} in {target}")
        if rel == "404.html":
            continue
        redirect_pages = {os.path.normpath(("ru/" if l == "ru" else "") + f"{o}/index.html")
                          for o in getattr(site.c, "REDIRECTS", {}) for l in LANGS}
        if os.path.normpath(rel) in redirect_pages:
            continue  # meta-refresh stubs for renamed projects
        if pp.headings.count(1) != 1:
            errors.append(f"{rel}: {pp.headings.count(1)} h1 elements")
        prev = 1
        for h in pp.headings[1:]:
            if h > prev + 1:
                errors.append(f"{rel}: heading jumps h{prev} → h{h}")
            prev = h
        t, d = pp.title.strip(), pp.meta.get("description", "")
        if not t or len(t) > 60:
            errors.append(f"{rel}: title length {len(t)} (≤60): {t}")
        if not d or len(d) > 160:
            errors.append(f"{rel}: description length {len(d)} (≤160): {d}")
        if not pp.canon:
            errors.append(f"{rel}: no canonical")
        langs = {h for h, _ in pp.hreflang}
        if langs != {"en", "ru", "x-default"}:
            errors.append(f"{rel}: hreflang set {sorted(langs)}")
        if pp.canon not in [h for _, h in pp.hreflang]:
            errors.append(f"{rel}: canonical is not among hreflang alternates")
        if not pp.meta.get("og:image", "").startswith("http"):
            errors.append(f"{rel}: og:image is not absolute")
        for a in pp.imgs:
            if not a.get("alt"):
                errors.append(f"{rel}: img without alt: {a.get('src')}")
            if not (a.get("width") and a.get("height")):
                errors.append(f"{rel}: img without width/height: {a.get('src')}")
    # sitemap
    sm = os.path.join(site.out, "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    tree = ET.parse(sm)
    locs = [u.find("s:loc", ns).text for u in tree.getroot().findall("s:url", ns)]
    for loc in locs:
        r = resolve(loc, "index.html")
        if r is None or not os.path.isfile(os.path.join(site.out, r[0])):
            errors.append(f"sitemap: {loc} has no page")
    for rel, pp in parsed.items():
        if rel != "404.html" and pp.canon not in locs:
            errors.append(f"sitemap: canonical {pp.canon} of {rel} is missing")
    # JSON-LD must parse
    for rel in parsed:
        txt = open(os.path.join(site.out, rel), encoding="utf-8").read()
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S):
            try:
                json.loads(m.group(1))
            except ValueError as e:
                errors.append(f"{rel}: bad JSON-LD: {e}")
    return errors, warnings, len(parsed), len(locs)


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="https://vitamindb.github.io", help="absolute base URL of the site")
    ap.add_argument("--cname", help="custom domain; writes docs/CNAME")
    ap.add_argument("--google-verify", help="token for <meta name=google-site-verification> on the home pages")
    ap.add_argument("--yandex-verify", help="token for <meta name=yandex-verification> on the home pages")
    ap.add_argument("--repos", help="folder that holds the project repositories (default: REPOS_ROOT in content.py)")
    ap.add_argument("--out", default=os.path.join(ROOT, "docs"), help="output folder (default: docs/)")
    ap.add_argument("--lastmod", help="sitemap lastmod date, YYYY-MM-DD (default: today)")
    ap.add_argument("--no-check", action="store_true", help="skip the link and SEO checks")
    args = ap.parse_args()

    content = load_content()
    site = Site(args, content)
    site.blog = load_blog()
    os.makedirs(site.out, exist_ok=True)
    imgs = Images(site)

    build_static(site)
    site.app_lists = {}
    site.app_slugs = build_apps(site, imgs)
    for lang in LANGS:
        build_hub(site, imgs, lang)
        for i in range(len(content.PROJECTS)):
            build_project(site, imgs, lang, i)
    build_blog(site, imgs)
    build_search_index(site)
    build_404(site)
    build_redirects(site)
    build_sitemap(site)
    removed = prune(site)

    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(site.out) for f in fs)
    print(f"built {len(site.written)} files into {site.out} ({total / 1e6:.1f} MB), pruned {removed}")
    if args.no_check:
        return
    errors, warnings, npages, nlocs = check(site)
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    print(f"checked {npages} pages, {nlocs} sitemap URLs: {len(errors)} errors")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
