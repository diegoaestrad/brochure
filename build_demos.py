#!/usr/bin/env python3
"""Build distinct demo sites + customer showcase gallery."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "businesses.json").read_text())
CATALOG = json.loads((ROOT / "catalog.json").read_text())
SCRIPT = (ROOT / "bakery" / "script.js").read_text()

THEME_BY_SLUG = {d["slug"]: d["theme"].lower() for d in CATALOG["demos"]}

DEMO_BAR = """
    <div class="demo-bar" role="note" aria-label="Demo website notice">
      <p><strong>Demo preview</strong> — sample client website</p>
      <a href="../index.html">← Services & portfolio</a>
    </div>"""

DEMO_BAR_CSS = """
.demo-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 3000;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.65rem 1.25rem;
  padding: 0.55rem 1rem;
  background: #0f172a;
  color: #e2e8f0;
  font-size: 0.82rem;
  border-top: 1px solid rgba(148, 163, 184, 0.35);
}
.demo-bar p { margin: 0; }
.demo-bar a {
  color: #38bdf8;
  font-weight: 700;
  text-decoration: underline;
}
body { padding-bottom: 3.1rem; }
"""


def img(photo_id: str, w: int = 900) -> str:
    if photo_id.startswith("http"):
        return photo_id
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=80"


def hero_url(b: dict) -> str:
    h = b["hero_image"]
    return img(h, 1920) if h.startswith("photo-") else h


def rgba_hex(h: str, a: float) -> str:
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {a})"


def cards_html(b: dict) -> str:
    out = []
    for title, desc, photo, alt in b["products"]:
        out.append(
            f"""            <article class="product-card">
              <img src="{img(photo)}" alt="{alt}" loading="lazy" decoding="async" width="900" height="600" />
              <div class="product-copy"><h3>{title}</h3><p>{desc}</p></div>
            </article>"""
        )
    return "\n".join(out)


def services_html(b: dict) -> str:
    out = []
    for title, items in b["services"]:
        lis = "\n".join(f"                <li>{i}</li>" for i in items)
        out.append(f"""            <article class="service-card"><h3>{title}</h3><ul>
{lis}
              </ul></article>""")
    return "\n".join(out)


def shared_main(b: dict, email: str, phone_display: str, phone_href: str, map_q: str) -> str:
    about = "\n".join(f"            <p>{p}</p>" for p in b["about"])
    social = "\n".join(
        f'            <li><a href="#">{n}</a></li>' for n in b.get("social", ["Instagram", "Facebook"])
    )
    return f"""
    <main id="main-content">
      <section class="section" id="products">
        <div class="container">
          <div class="section-head"><h2>{b["products_heading"]}</h2><p>{b["products_sub"]}</p></div>
          <div class="product-grid">{cards_html(b)}</div>
        </div>
      </section>
      <section class="section section-alt" id="about">
        <div class="container about-grid">
          <div class="about-image-wrap">
            <img src="{img(b['about_photo'], 1100)}" alt="{b['about_alt']}" loading="lazy" decoding="async" width="1100" height="750" />
          </div>
          <div class="about-copy">
            <div class="section-head left-align"><h2>About Us</h2></div>
{about}
          </div>
        </div>
      </section>
      <section class="section" id="services">
        <div class="container">
          <div class="section-head"><h2>{b["services_heading"]}</h2><p>{b["services_sub"]}</p></div>
          <div class="services-grid">{services_html(b)}</div>
        </div>
      </section>
      <section class="section section-alt" id="contact">
        <div class="container contact-grid">
          <div>
            <div class="section-head left-align"><h2>Contact Us</h2><p>{b["contact_sub"]}</p></div>
            <ul class="contact-list">
              <li><strong>Address:</strong> {b["location"]}</li>
              <li><strong>Phone:</strong> <a href="tel:{phone_href}">{phone_display}</a></li>
              <li><strong>Email:</strong> <a href="mailto:{email}">{email}</a></li>
              <li><strong>Hours:</strong> {b["hours"]}</li>
            </ul>
            <div class="map-wrap">
              <iframe title="Map" src="https://www.google.com/maps?q={map_q}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
          </div>
          <aside class="contact-card">
            <h3>{b.get("form_title", "Send a Message")}</h3>
            <form id="contact-form" novalidate>
              <div class="form-group"><label for="name">Full Name</label><input id="name" name="name" type="text" required maxlength="60" /></div>
              <div class="form-group"><label for="email">Email</label><input id="email" name="email" type="email" required /></div>
              <div class="form-group"><label for="phone">Phone (optional)</label><input id="phone" name="phone" type="tel" placeholder="{phone_display}" pattern="^\\+?[0-9\\s\\-()]{7,20}$" /></div>
              <div class="form-group"><label for="message">Message</label><textarea id="message" name="message" rows="5" required minlength="10" maxlength="500"></textarea></div>
              <button class="btn btn-primary" type="submit">Send Inquiry</button>
              <p class="form-feedback" id="form-feedback" role="status" aria-live="polite"></p>
            </form>
          </aside>
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <div class="container footer-content">
        <div><a class="logo footer-logo" href="#home">{b["name"]}</a><p>{b["footer_tag"]}</p></div>
        <div><h4>Follow</h4><ul class="social-links">{social}</ul></div>
      </div>
      <p class="copyright">© <span id="year"></span> {b["name"]}. Demo website.</p>
    </footer>"""


def nav_html(b: dict) -> str:
    return f"""          <ul class="nav-links" id="nav-menu">
            <li><a href="#home">Home</a></li>
            <li><a href="#products">{b.get("products_nav", "Services")}</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">{b.get("services_nav", "More")}</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>"""


def build_html(b: dict, theme: str) -> str:
    slug = b["slug"]
    email = b.get("email", f"hello@{slug.replace('-', '')}.com")
    phone_display = b.get("phone_display", b["phone"])
    phone_href = re.sub(r"[^\d+]", "", b["phone"])
    map_q = b["location"].replace(" ", "+").replace(",", "%2C")
    hero = hero_url(b)
    c = b["colors"]

    if theme == "corporate":
        hero_block = f"""
      <section class="hero hero-split" id="home">
        <div class="container hero-split-grid">
          <div class="hero-copy">
            <p class="eyebrow">{b["eyebrow"]}</p>
            <h1>{b["headline"]}</h1>
            <p>{b["hero_text"]}</p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="#products">{b["cta_primary"]}</a>
              <a class="btn btn-secondary" href="#contact">{b["cta_secondary"]}</a>
            </div>
          </div>
          <div class="hero-media">
            <img src="{hero}" alt="" width="1200" height="800" />
          </div>
        </div>
      </section>"""
    elif theme == "editorial":
        hero_block = f"""
      <section class="hero hero-editorial" id="home" style="background-image:url('{hero}')">
        <div class="container hero-editorial-inner">
          <p class="eyebrow">{b["eyebrow"]}</p>
          <h1>{b["headline"]}</h1>
          <p>{b["hero_text"]}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#products">{b["cta_primary"]}</a>
            <a class="btn btn-secondary" href="#contact">{b["cta_secondary"]}</a>
          </div>
        </div>
      </section>"""
    elif theme == "bold":
        hero_block = f"""
      <section class="hero hero-bold" id="home">
        <div class="hero-bold-bg" style="background-image:url('{hero}')"></div>
        <div class="container hero-bold-inner">
          <p class="eyebrow">{b["eyebrow"]}</p>
          <h1>{b["headline"]}</h1>
          <p>{b["hero_text"]}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#contact">{b["cta_secondary"]}</a>
            <a class="btn btn-secondary" href="#products">{b["cta_primary"]}</a>
          </div>
        </div>
      </section>"""
    elif theme == "calm":
        hero_block = f"""
      <section class="hero hero-calm" id="home" style="background-image:linear-gradient({rgba_hex(c['dark'], 0.45)}, {rgba_hex(c['dark'], 0.62)}), url('{hero}')">
        <div class="container hero-calm-inner">
          <p class="eyebrow">{b["eyebrow"]}</p>
          <h1>{b["headline"]}</h1>
          <p>{b["hero_text"]}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#products">{b["cta_primary"]}</a>
            <a class="btn btn-secondary" href="#contact">{b["cta_secondary"]}</a>
          </div>
        </div>
      </section>"""
    else:  # warm + lifestyle
        hero_block = f"""
      <section class="hero" id="home" style="background-image:linear-gradient({rgba_hex(c['dark'], 0.5)}, {rgba_hex(c['dark'], 0.7)}), url('{hero}')">
        <div class="container hero-content">
          <p class="eyebrow">{b["eyebrow"]}</p>
          <h1>{b["headline"]}</h1>
          <p>{b["hero_text"]}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#products">{b["cta_primary"]}</a>
            <a class="btn btn-secondary" href="#contact">{b["cta_secondary"]}</a>
          </div>
        </div>
      </section>"""

    fonts = {
        "warm": "https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital@0;1&family=DM+Sans:wght@400;600;700&display=swap",
        "lifestyle": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Lato:wght@400;700&display=swap",
        "corporate": "https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap",
        "calm": "https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap",
        "bold": "https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Open+Sans:wght@400;600;700&display=swap",
        "editorial": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@400;600&display=swap",
    }
    font = fonts.get(theme, fonts["warm"])

    return f"""<!DOCTYPE html>
<html lang="en" class="theme-{theme}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{b["meta"]}" />
    <title>{b["name"]} | {b["tagline"]}</title>
    <link rel="preconnect" href="https://images.unsplash.com" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="stylesheet" href="{font}" />
    <link rel="stylesheet" href="styles.css" />
    <script src="script.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <nav class="navbar" aria-label="Main">
        <div class="container nav-content">
          <a class="logo" href="#home"><span class="logo-mark">{b["emoji"]}</span><span>{b["name"]}</span></a>
          <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Menu"><span></span><span></span><span></span></button>
{nav_html(b)}
        </div>
      </nav>
{hero_block}
    </header>
{shared_main(b, email, phone_display, phone_href, map_q)}
{DEMO_BAR}
  </body>
</html>"""


def build_css(b: dict, theme: str) -> str:
    c = b["colors"]
    dark, mid, light = c["dark"], c["mid"], c["light"]
    cream, soft = c["cream"], c["cream_soft"]
    gold, gsoft = c["gold"], c["gold_soft"]
    text, danger = c["text"], c["danger"]

    radius = "1rem" if theme in ("warm", "calm", "lifestyle") else "0.35rem" if theme == "bold" else "0.65rem"
    font_body = {
        "warm": '"DM Sans", sans-serif',
        "lifestyle": "Lato, sans-serif",
        "corporate": '"Source Sans 3", sans-serif',
        "calm": "Nunito, sans-serif",
        "bold": '"Open Sans", sans-serif',
        "editorial": "Montserrat, sans-serif",
    }[theme]
    font_head = {
        "warm": '"Libre Baskerville", serif',
        "lifestyle": '"Playfair Display", serif',
        "corporate": '"Source Sans 3", sans-serif',
        "calm": "Nunito, sans-serif",
        "bold": "Oswald, sans-serif",
        "editorial": '"Cormorant Garamond", serif',
    }[theme]

    nav_bg = f"rgba({int(dark[1:3],16)}, {int(dark[3:5],16)}, {int(dark[5:7],16)}, 0.92)" if theme != "corporate" else "#ffffff"
    nav_color = cream if theme != "corporate" else dark
    nav_border = "none" if theme == "corporate" else f"1px solid rgba(255,255,255,0.15)"

    extra = ""
    if theme == "corporate":
        extra = """
.hero-split { padding: 5.5rem 0 3rem; background: var(--cream); color: var(--text); }
.hero-split .eyebrow { color: var(--mid); }
.hero-split h1, .hero-split p { color: var(--dark); }
.hero-split .btn-secondary { border-color: var(--mid); color: var(--dark); }
.hero-split-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center; }
.hero-media img { border-radius: 1rem; box-shadow: var(--shadow); min-height: 320px; object-fit: cover; width: 100%; }
.navbar { background: #fff; box-shadow: 0 1px 0 rgba(0,0,0,0.08); }
.navbar .logo, .nav-links a { color: var(--dark); }
.nav-links a::after { background: var(--gold); }
.menu-toggle span { background: var(--dark); }
@media (max-width: 900px) { .hero-split-grid { grid-template-columns: 1fr; } .hero-media { order: -1; } }
"""
    elif theme == "editorial":
        extra = """
.hero-editorial { min-height: 88vh; background-size: cover; background-position: center; display: grid; align-items: end; padding: 6rem 0 4rem; color: #fff; }
.hero-editorial-inner { max-width: 720px; }
.hero-editorial h1 { font-size: clamp(2.8rem, 7vw, 5rem); font-weight: 600; }
.navbar { background: transparent; position: absolute; }
.navbar.scrolled { background: rgba(15,15,15,0.85); }
"""
    elif theme == "bold":
        extra = """
.hero-bold { position: relative; min-height: 85vh; display: grid; align-items: center; color: #fff; overflow: hidden; }
.hero-bold-bg { position: absolute; inset: 0; background-size: cover; background-position: center; }
.hero-bold-bg::after { content: ""; position: absolute; inset: 0; background: linear-gradient(105deg, rgba(0,0,0,0.75) 40%, rgba(0,0,0,0.35)); }
.hero-bold-inner { position: relative; z-index: 1; max-width: 640px; }
.hero-bold h1 { text-transform: uppercase; letter-spacing: 0.02em; font-family: Oswald, sans-serif; font-size: clamp(2.2rem, 6vw, 3.8rem); }
.btn { border-radius: 4px; text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.88rem; }
.product-card { border-radius: 4px; }
"""
    elif theme == "calm":
        extra = """
.hero-calm { min-height: 82vh; display: grid; align-items: center; text-align: center; background-size: cover; background-position: center; color: #fff; padding: 6rem 0; }
.hero-calm-inner { max-width: 680px; margin: 0 auto; }
.hero-calm h1 { font-weight: 800; }
.product-card, .service-card, .contact-card { border-radius: 1.25rem; }
.btn { border-radius: 999px; }
"""
    elif theme == "lifestyle":
        extra = """
.hero { text-align: left; }
.hero h1 { font-family: "Playfair Display", serif; font-weight: 700; }
.section-head h2 { font-family: "Playfair Display", serif; }
.product-card img { height: 240px; }
"""

    return f"""
:root {{
  --cream: {cream}; --cream-soft: {soft}; --dark: {dark}; --mid: {mid}; --light: {light};
  --gold: {gold}; --gold-soft: {gsoft}; --text: {text}; --danger: {danger};
  --white: #fff; --shadow: 0 12px 32px {rgba_hex(dark, 0.14)};
  --radius: {radius};
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; font-family: {font_body}; color: var(--text); background: var(--cream); line-height: 1.6; }}
h1, h2, h3, .logo {{ font-family: {font_head}; }}
img {{ max-width: 100%; display: block; }}
a {{ color: inherit; text-decoration: none; }}
section[id] {{ scroll-margin-top: 90px; }}
.container {{ width: min(1120px, 92%); margin: 0 auto; }}
.skip-link {{ position: absolute; left: -999px; top: 0; z-index: 2000; background: var(--dark); color: var(--white); padding: 0.65rem 1rem; }}
.skip-link:focus {{ left: 1rem; }}
.navbar {{ position: fixed; inset: 0 0 auto 0; z-index: 1000; background: {nav_bg}; border-bottom: {nav_border}; backdrop-filter: blur(6px); transition: 0.3s; }}
.navbar.scrolled {{ box-shadow: var(--shadow); }}
.nav-content {{ min-height: 4.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; position: relative; }}
.logo {{ display: inline-flex; align-items: center; gap: 0.45rem; color: {nav_color}; font-weight: 700; font-size: 1.05rem; }}
.logo-mark {{ font-size: 1.25rem; }}
.nav-links {{ list-style: none; margin: 0; padding: 0; display: flex; gap: 1.2rem; }}
.nav-links a {{ color: {nav_color}; font-weight: 600; }}
.nav-links a:hover {{ color: var(--gold-soft); }}
.menu-toggle {{ display: none; border: 1px solid rgba(128,128,128,0.35); background: transparent; padding: 0.4rem; border-radius: 6px; cursor: pointer; }}
.menu-toggle span {{ display: block; width: 1.2rem; height: 2px; background: {nav_color}; margin: 0.2rem 0; }}
.hero {{ min-height: 90vh; display: grid; align-items: center; padding: 6.5rem 0 4rem; color: var(--white); background-size: cover; background-position: center; }}
.hero-content {{ max-width: 640px; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.8rem; font-weight: 700; color: var(--gold-soft); margin-bottom: 0.75rem; }}
.hero h1 {{ font-size: clamp(2rem, 5.5vw, 3.6rem); line-height: 1.12; margin: 0; }}
.hero p {{ font-size: 1.05rem; margin: 1rem 0 1.5rem; max-width: 52ch; }}
.hero-actions {{ display: flex; flex-wrap: wrap; gap: 0.75rem; }}
.btn {{ display: inline-flex; padding: 0.72rem 1.25rem; font-weight: 700; border-radius: var(--radius); border: 1px solid transparent; cursor: pointer; transition: 0.2s; }}
.btn-primary {{ background: var(--gold); color: var(--dark); }}
.btn-secondary {{ background: transparent; border-color: rgba(255,255,255,0.75); color: #fff; }}
.section {{ padding: 4.5rem 0; }}
.section-alt {{ background: var(--cream-soft); }}
.section-head {{ text-align: center; margin-bottom: 2rem; }}
.section-head h2 {{ margin: 0; color: var(--dark); font-size: clamp(1.6rem, 3vw, 2.2rem); }}
.left-align {{ text-align: left; }}
.product-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; }}
.product-card {{ background: var(--white); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); transition: 0.25s; }}
.product-card:hover {{ transform: translateY(-5px); }}
.product-card img {{ height: 200px; object-fit: cover; width: 100%; }}
.product-copy {{ padding: 1rem; }}
.product-copy h3 {{ margin: 0; color: var(--dark); font-size: 1.05rem; }}
.services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
.service-card {{ background: var(--white); padding: 1rem; border-radius: var(--radius); box-shadow: var(--shadow); }}
.about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center; }}
.about-image-wrap img {{ border-radius: var(--radius); min-height: 300px; object-fit: cover; box-shadow: var(--shadow); }}
.contact-grid {{ display: grid; grid-template-columns: 1.2fr 0.85fr; gap: 1.5rem; }}
.contact-list {{ list-style: none; padding: 0; margin: 0; }}
.contact-list li {{ margin-bottom: 0.5rem; color: var(--mid); }}
.map-wrap {{ margin-top: 1rem; border-radius: var(--radius); overflow: hidden; aspect-ratio: 16/10; box-shadow: var(--shadow); }}
.map-wrap iframe {{ width: 100%; height: 100%; border: 0; }}
.contact-card {{ background: var(--white); padding: 1.2rem; border-radius: var(--radius); box-shadow: var(--shadow); }}
.form-group {{ display: grid; gap: 0.35rem; margin-bottom: 0.85rem; }}
input, textarea {{ width: 100%; padding: 0.65rem; border: 1px solid rgba(0,0,0,0.2); border-radius: calc(var(--radius) * 0.7); font: inherit; }}
input.invalid, textarea.invalid {{ border-color: var(--danger); }}
.form-feedback {{ min-height: 1.2rem; font-weight: 600; margin-top: 0.5rem; }}
.form-feedback.error {{ color: var(--danger); }}
.site-footer {{ background: var(--dark); color: var(--cream); padding: 2rem 0 1rem; }}
.footer-content {{ display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap; }}
.social-links {{ list-style: none; padding: 0; display: flex; gap: 0.75rem; flex-wrap: wrap; }}
.copyright {{ text-align: center; margin: 1rem 0 0; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.15); font-size: 0.9rem; }}
{DEMO_BAR_CSS}
{extra}
@media (max-width: 760px) {{
  .menu-toggle {{ display: inline-block; }}
  .nav-links {{ display: none; position: absolute; top: 100%; right: 0; background: var(--dark); flex-direction: column; padding: 1rem; border-radius: 0.5rem; min-width: 200px; }}
  .nav-links.open {{ display: flex; }}
  .about-grid, .contact-grid {{ grid-template-columns: 1fr; }}
}}
"""


def sync_portfolio_data() -> None:
    """Embed catalog into portfolio-data.js for file:// and static hosting."""
    catalog = json.loads((ROOT / "catalog.json").read_text())
    js = (
        "// Generated from catalog.json — loaded by index.html\n"
        "window.PORTFOLIO_DEMOS = "
        + json.dumps(catalog["demos"], indent=2)
        + ";\n"
    )
    (ROOT / "portfolio-data.js").write_text(js)


def build_showcase() -> None:
    """Portfolio hub is root index.html — sync embedded data only."""
    sync_portfolio_data()


def _build_showcase_legacy() -> None:
    cards = []
    for d in CATALOG["demos"]:
        thumb = img(d["hero"], 640)
        cat = d["category"]
        cards.append(
            f"""        <article class="demo-card" data-category="{cat}">
          <div class="demo-thumb">
            <span class="demo-theme">{d["theme"]}</span>
            <img src="{thumb}" alt="{d["name"]} website preview" loading="lazy" width="640" height="400" />
          </div>
          <div class="demo-body">
            <div class="demo-meta"><span class="demo-emoji">{d["emoji"]}</span><span>{cat}</span></div>
            <h2>{d["name"]}</h2>
            <p>{d["tagline"]} — click to open the live demo page.</p>
            <div class="demo-actions">
              <a class="btn btn-primary" href="{d["slug"]}/index.html" target="_blank" rel="noopener">View live demo</a>
            </div>
          </div>
        </article>"""
        )

    filters = ['<button type="button" class="filter-btn active" data-filter="all" aria-pressed="true">All</button>']
    for cat in CATALOG["categories"][1:]:
        f = cat.lower().replace(" & ", "-").replace(" ", "-")
        filters.append(
            f'<button type="button" class="filter-btn" data-filter="{cat}" aria-pressed="false">{cat}</button>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Browse 30 industry demo websites — preview sample sites for local businesses." />
    <title>Website Demos for Local Businesses</title>
    <link rel="preconnect" href="https://images.unsplash.com" />
    <link rel="stylesheet" href="showcase.css" />
    <script src="showcase.js" defer></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container brand">
        <div>
          <p class="brand-badge">30 live demo pages</p>
          <h1>Website demos by industry</h1>
          <p>Each link opens a full sample website your customer can explore — bakery, dentist, plumber, gym, and more.</p>
        </div>
      </div>
      <div class="container filters" role="group" aria-label="Filter demos">
        {chr(10).join(filters)}
      </div>
    </header>
    <main class="container">
      <div class="demo-grid" id="demo-grid">
{chr(10).join(cards)}
      </div>
      <p class="empty-state" id="empty-state">No demos in this category.</p>
    </main>
    <footer class="site-footer">
      <div class="container"><p>Sample websites for portfolio review. Each demo is a standalone preview.</p></div>
    </footer>
  </body>
</html>"""
    (ROOT / "index.html").write_text(html)


def patch_bakery_demo_bar() -> None:
    path = ROOT / "bakery" / "index.html"
    html = path.read_text()
    if "demo-bar" in html:
        return
    css_path = ROOT / "bakery" / "styles.css"
    css = css_path.read_text()
    if ".demo-bar" not in css:
        css_path.write_text(css.rstrip() + "\n" + DEMO_BAR_CSS)
    html = html.replace("</body>", DEMO_BAR + "\n  </body>")
    path.write_text(html)


def main() -> None:
    build_showcase()
    patch_bakery_demo_bar()

    for b in DATA:
        slug = b["slug"]
        theme = THEME_BY_SLUG.get(slug, "warm")
        out = ROOT / slug
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(build_html(b, theme))
        (out / "styles.css").write_text(build_css(b, theme))
        (out / "script.js").write_text(SCRIPT)
        print(f"✓ {slug} ({theme})")

    sync_portfolio_data()
    print("\nPortfolio data: portfolio-data.js")
    print("Tip: run python3 fix_images.py if any Unsplash thumbnails break.")


if __name__ == "__main__":
    main()
