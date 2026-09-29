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
        group = re.sub(r"[^a-z0-9-]+", "-", parts[0].lower().replace("_", "-"))
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
            f' · <a href="{esc(c.SITE["contacts"]["paypal"])}">PayPal</a></p><p>{esc(ui["footer_note"])}</p></div>\n'
            f'    <nav aria-label="{esc(ui["other_nav"])}">{links}</nav>')


def contact_rows(site, lang):
    c = site.c
    ct = c.SITE["contacts"]
    ui = c.UI[lang]
    rows = [
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
    same = [ct["github"], ct["x"]] + [u for u in (ct.get("youtube"), ) if u]
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
        im = imgs.get(p["hero"]["src"])
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
    hero = imgs.get(p["hero"]["src"])
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
    gal = [(g, imgs.get(g["src"])) for g in gallery_items]

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

    parts.append(sec(ui["what_h"], '<div class="prose">' + "".join(f"<p>{esc(t)}</p>" for t in p["what"][lang]) + "</div>", "what"))

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


# --------------------------------------------------------------------------- 404, misc
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
    site.write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site.abs(site.prefix + '/sitemap.xml')}\n")
    cname = os.path.join(site.out, "CNAME")
    if site.args.cname:
        site.write("CNAME", site.args.cname.strip() + "\n")
    elif os.path.exists(cname):
        site.keep("CNAME")   # keep a previously configured domain


def build_sitemap(site):
    c = site.c
    pages = [None] + [p["slug"] for p in c.PROJECTS]
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
            if fn.endswith(".html"):
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
    os.makedirs(site.out, exist_ok=True)
    imgs = Images(site)

    build_static(site)
    for lang in LANGS:
        build_hub(site, imgs, lang)
        for i in range(len(content.PROJECTS)):
            build_project(site, imgs, lang, i)
    build_404(site)
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
