#!/usr/bin/env python3
"""Generate demo sites from bakery template (excludes bakery/)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
BAKERY_CSS = (ROOT / "bakery" / "styles.css").read_text()
SCRIPT = (ROOT / "bakery" / "script.js").read_text()
DATA_FILE = ROOT / "businesses.json"


def img(photo_id: str, w: int = 900) -> str:
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=80"


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def build_css(b: dict) -> str:
    dark, mid, light = b["colors"]["dark"], b["colors"]["mid"], b["colors"]["light"]
    cream, cream_soft = b["colors"]["cream"], b["colors"]["cream_soft"]
    gold, gold_soft = b["colors"]["gold"], b["colors"]["gold_soft"]
    text, danger = b["colors"]["text"], b["colors"]["danger"]
    dr, dg, db = hex_rgb(dark)
    hero_overlay = b.get("hero_overlay", f"rgba({dr}, {dg}, {db}, 0.55), rgba({dr}, {dg}, {db}, 0.72)")
    lr, lg, lb = hex_rgb(light)

    css = BAKERY_CSS
    css = css.replace("#fff8ed", cream).replace("#f5e9d7", cream_soft)
    css = css.replace("#3a2417", dark).replace("#5a3b2b", mid).replace("#8b5f3d", light)
    css = css.replace("#d9aa5a", gold).replace("#e8c98c", gold_soft)
    css = css.replace("#3f291a", text).replace("#a14a31", danger)
    css = css.replace("rgba(58, 36, 23,", f"rgba({dr}, {dg}, {db},")
    css = css.replace("rgba(40, 22, 12, 0.5), rgba(40, 22, 12, 0.68)", hero_overlay)
    css = css.replace("rgba(139, 95, 61, 0.12)", f"rgba({lr}, {lg}, {lb}, 0.12)")
    css = css.replace("rgba(139, 95, 61, 0.2)", f"rgba({lr}, {lg}, {lb}, 0.2)")
    css = css.replace("rgba(90, 59, 43, 0.35)", f"rgba({hex_rgb(mid)[0]}, {hex_rgb(mid)[1]}, {hex_rgb(mid)[2]}, 0.35)")
    css = css.replace("rgba(217, 170, 90, 0.25)", f"rgba({hex_rgb(gold)[0]}, {hex_rgb(gold)[1]}, {hex_rgb(gold)[2]}, 0.25)")
    css = css.replace("rgba(217, 170, 90, 0.55)", f"rgba({hex_rgb(gold)[0]}, {hex_rgb(gold)[1]}, {hex_rgb(gold)[2]}, 0.55)")
    css = re.sub(
        r'url\("https://images\.unsplash\.com/[^"]+"\)',
        f'url("{b["hero_image"]}")',
        css,
        count=1,
    )
    return css


def product_cards(b: dict) -> str:
    blocks = []
    for title, desc, photo, alt in b["products"]:
        blocks.append(
            f"""            <article class="product-card">
              <img
                src="{img(photo)}"
                alt="{alt}"
                loading="lazy"
                decoding="async"
                width="900"
                height="600"
              />
              <div class="product-copy">
                <h3>{title}</h3>
                <p>{desc}</p>
              </div>
            </article>"""
        )
    return "\n\n".join(blocks)


def service_cards(b: dict) -> str:
    blocks = []
    for title, items in b["services"]:
        lis = "\n".join(f"                <li>{item}</li>" for item in items)
        blocks.append(
            f"""            <article class="service-card">
              <h3>{title}</h3>
              <ul>
{lis}
              </ul>
            </article>"""
        )
    return "\n\n".join(blocks)


def about_paragraphs(b: dict) -> str:
    return "\n".join(f"            <p>{p}</p>" for p in b["about"])


def social_links(b: dict) -> str:
    return "\n".join(
        f'            <li><a href="#" aria-label="Follow {b["name"]} on {net}">{net}</a></li>'
        for net in b.get("social", ["Instagram", "Facebook", "Google"])
    )


def build_html(b: dict) -> str:
    slug = b["slug"]
    email = b.get("email", f"hello@{slug.replace('-', '')}.com")
    phone_display = b.get("phone_display", b["phone"])
    phone_href = re.sub(r"[^\d+]", "", b["phone"])
    map_q = b["location"].replace(" ", "+").replace(",", "%2C")
    products_nav = b.get("products_nav", "Products")
    services_nav = b.get("services_nav", "Services")

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{b["meta"]}" />
    <title>{b["name"]} | {b["tagline"]}</title>
    <link rel="preconnect" href="https://images.unsplash.com" />
    <link rel="stylesheet" href="styles.css" />
    <script src="script.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>

    <header class="site-header" id="home">
      <nav class="navbar" aria-label="Main navigation">
        <div class="container nav-content">
          <a class="logo" href="#home" aria-label="{b["name"]} Home">
            <span class="logo-mark" aria-hidden="true">{b["emoji"]}</span>
            <span>{b["name"]}</span>
          </a>

          <button
            class="menu-toggle"
            type="button"
            aria-expanded="false"
            aria-controls="nav-menu"
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          <ul class="nav-links" id="nav-menu">
            <li><a href="#home">Home</a></li>
            <li><a href="#products">{products_nav}</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">{services_nav}</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div>
      </nav>

      <section class="hero" aria-label="{b["name"]} hero banner">
        <div class="container hero-content">
          <p class="eyebrow">{b["eyebrow"]}</p>
          <h1>{b["headline"]}</h1>
          <p>{b["hero_text"]}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#products">{b["cta_primary"]}</a>
            <a class="btn btn-secondary" href="#contact">{b["cta_secondary"]}</a>
          </div>
        </div>
      </section>
    </header>

    <main id="main-content">
      <section class="section" id="products">
        <div class="container">
          <div class="section-head">
            <h2>{b["products_heading"]}</h2>
            <p>{b["products_sub"]}</p>
          </div>

          <div class="product-grid">
{product_cards(b)}
          </div>
        </div>
      </section>

      <section class="section section-alt" id="about">
        <div class="container about-grid">
          <div class="about-image-wrap">
            <img
              src="{img(b["about_photo"], 1100)}"
              alt="{b["about_alt"]}"
              loading="lazy"
              decoding="async"
              width="1100"
              height="750"
            />
          </div>

          <div class="about-copy">
            <div class="section-head left-align">
              <h2>About Us</h2>
            </div>
{about_paragraphs(b)}
          </div>
        </div>
      </section>

      <section class="section" id="services">
        <div class="container">
          <div class="section-head">
            <h2>{b["services_heading"]}</h2>
            <p>{b["services_sub"]}</p>
          </div>

          <div class="services-grid">
{service_cards(b)}
          </div>
        </div>
      </section>

      <section class="section section-alt" id="contact">
        <div class="container contact-grid">
          <div>
            <div class="section-head left-align">
              <h2>Contact Us</h2>
              <p>{b["contact_sub"]}</p>
            </div>

            <ul class="contact-list">
              <li><strong>Address:</strong> {b["location"]}</li>
              <li><strong>Phone:</strong> <a href="tel:{phone_href}">{phone_display}</a></li>
              <li><strong>Email:</strong> <a href="mailto:{email}">{email}</a></li>
              <li><strong>Hours:</strong> {b["hours"]}</li>
            </ul>

            <div class="map-wrap" aria-label="{b["name"]} location map">
              <iframe
                title="{b["name"]} Location"
                src="https://www.google.com/maps?q={map_q}&output=embed"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>

          <aside class="contact-card" aria-label="Customer inquiry form">
            <h3>{b.get("form_title", "Customer Inquiry")}</h3>
            <form id="contact-form" novalidate>
              <div class="form-group">
                <label for="name">Full Name</label>
                <input id="name" name="name" type="text" required maxlength="60" />
              </div>

              <div class="form-group">
                <label for="email">Email Address</label>
                <input id="email" name="email" type="email" required />
              </div>

              <div class="form-group">
                <label for="phone">Phone Number (optional)</label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  placeholder="{phone_display}"
                  pattern="^\\+?[0-9\\s\\-()]{7,20}$"
                />
              </div>

              <div class="form-group">
                <label for="message">Message</label>
                <textarea
                  id="message"
                  name="message"
                  rows="5"
                  required
                  minlength="10"
                  maxlength="500"
                ></textarea>
              </div>

              <button class="btn btn-primary" type="submit">Send Inquiry</button>
              <p class="form-feedback" id="form-feedback" role="status" aria-live="polite"></p>
            </form>
          </aside>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="container footer-content">
        <div>
          <a class="logo footer-logo" href="#home">{b["name"]}</a>
          <p>{b["footer_tag"]}</p>
        </div>

        <div>
          <h4>Follow Us</h4>
          <ul class="social-links">
{social_links(b)}
          </ul>
        </div>
      </div>

      <p class="copyright">
        © <span id="year"></span> {b["name"]}. All rights reserved.
      </p>
    </footer>
  </body>
</html>
"""


def main() -> None:
    businesses = json.loads(DATA_FILE.read_text())
    for b in businesses:
        if b["slug"] == "bakery":
            continue
        out = ROOT / b["slug"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(build_html(b))
        (out / "styles.css").write_text(build_css(b))
        (out / "script.js").write_text(SCRIPT)
        print(f"✓ {b['slug']}")


if __name__ == "__main__":
    main()
