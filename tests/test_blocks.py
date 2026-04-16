from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

import kysc_components
from kysc_components.registry import block_path, block_schema, blocks


BLOCKS_DIR = Path(kysc_components.__file__).parent / "blocks"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(BLOCKS_DIR)),
        autoescape=select_autoescape(["html"]),
    )


def _render(block: str, **kwargs) -> str:
    src = "{% import '" + block + ".html' as b %}{{ b." + block + "(**kwargs) }}"
    return _env().from_string(src).render(kwargs=kwargs)


# --- version + registry ---


def test_version_matches_pyproject():
    assert kysc_components.__version__ == "1.0.0"


def test_registry_lists_all_blocks():
    expected = [
        "nav", "hero", "footer",
        "about", "services", "gallery", "contact_block",
        "pricing_table", "faq_accordion", "testimonials", "booking_embed",
    ]
    assert blocks() == expected


def test_registry_has_11_blocks():
    assert len(blocks()) == 11


def test_block_path_rejects_unknown():
    with pytest.raises(KeyError):
        block_path("nope")


def test_schema_rejects_unknown():
    with pytest.raises(KeyError):
        block_schema("nope")


def test_tailwind_preset_is_packaged():
    preset = Path(kysc_components.__file__).parent / "tailwind" / "preset.js"
    assert preset.exists()
    body = preset.read_text(encoding="utf-8")
    assert "module.exports" in body
    assert "brand" in body
    assert "accent2" in body
    assert "kysc-card" in body


# --- nav (preserved from v0.2.0) ---


def test_nav_renders():
    html = _render(
        "nav",
        brand={"label": "KYSC", "href": "/"},
        items=[{"label": "About", "href": "/about"}, {"label": "Contact", "href": "/contact"}],
    )
    assert "<nav" in html
    assert "KYSC" in html
    assert "/about" in html
    assert "/contact" in html


def test_nav_schema():
    assert block_schema("nav") == {"required": ["items", "brand"], "optional": []}


# --- hero (preserved from v0.2.0) ---


def test_hero_renders_without_bg():
    html = _render(
        "hero",
        headline="Ship it",
        subhead="Nightly builds, shipped calmly.",
        cta_text="Start",
        cta_href="/start",
    )
    assert "Ship it" in html
    assert "/start" in html
    assert "background-image" not in html


def test_hero_renders_with_bg():
    html = _render(
        "hero",
        headline="H",
        subhead="S",
        cta_text="C",
        cta_href="/c",
        bg_image="/img/x.jpg",
    )
    assert "/img/x.jpg" in html
    assert "background-image" in html


def test_hero_schema():
    assert block_schema("hero") == {
        "required": ["headline", "subhead", "cta_text", "cta_href"],
        "optional": ["bg_image"],
    }


# --- footer (preserved from v0.2.0) ---


def test_footer_renders():
    html = _render(
        "footer",
        copyright="(c) 2026 Kevin Sykes",
        links=[
            {"heading": "Work", "items": [{"label": "Projects", "href": "/projects"}]},
            {"heading": "More", "items": [{"label": "Blog", "href": "/blog"}]},
        ],
    )
    assert "<footer" in html
    assert "2026 Kevin Sykes" in html
    assert "/projects" in html
    assert "/blog" in html


def test_footer_schema():
    assert block_schema("footer") == {"required": ["copyright", "links"], "optional": []}


# --- about (NEW) ---


def test_about_renders_without_image():
    html = _render("about", heading="About Me", body="<p>Hello world</p>")
    assert "kysc-about" in html
    assert "About Me" in html
    assert "Hello world" in html
    assert "<img" not in html


def test_about_renders_with_image():
    html = _render(
        "about",
        heading="About",
        body="<p>Bio</p>",
        image="/img/portrait.jpg",
        image_alt="Portrait",
    )
    assert "/img/portrait.jpg" in html
    assert 'alt="Portrait"' in html


def test_about_reverse():
    html = _render(
        "about",
        heading="A",
        body="B",
        image="/img/x.jpg",
        reverse=True,
    )
    assert "md:order-2" in html
    assert "md:order-1" in html


def test_about_schema():
    assert block_schema("about") == {
        "required": ["heading", "body"],
        "optional": ["image", "image_alt", "reverse"],
    }


# --- services (NEW) ---


def test_services_renders():
    html = _render(
        "services",
        heading="What I Do",
        items=[
            {"title": "AI Consulting", "description": "Ship AI.", "icon": None},
            {"title": "Web Dev", "description": "Ship sites.", "icon": "🌐"},
        ],
    )
    assert "kysc-services" in html
    assert "What I Do" in html
    assert "AI Consulting" in html
    assert "Web Dev" in html


def test_services_with_icon():
    html = _render(
        "services",
        heading="S",
        items=[{"title": "T", "description": "D", "icon": "⚡"}],
    )
    assert "⚡" in html


def test_services_schema():
    assert block_schema("services") == {
        "required": ["heading", "items"],
        "optional": ["columns"],
    }


# --- gallery (NEW) ---


def test_gallery_renders():
    html = _render(
        "gallery",
        heading="Work",
        items=[
            {"src": "/img/a.jpg", "alt": "Project A", "caption": "First project", "href": None},
            {"src": "/img/b.jpg", "alt": "Project B", "caption": None, "href": "/projects/b"},
        ],
    )
    assert "kysc-gallery" in html
    assert "/img/a.jpg" in html
    assert "First project" in html
    assert "/projects/b" in html


def test_gallery_no_caption():
    html = _render(
        "gallery",
        heading="G",
        items=[{"src": "/x.jpg", "alt": "X", "caption": None, "href": None}],
    )
    assert "<figcaption" not in html


def test_gallery_schema():
    assert block_schema("gallery") == {
        "required": ["heading", "items"],
        "optional": ["columns"],
    }


# --- contact_block (NEW) ---


def test_contact_block_renders():
    html = _render(
        "contact_block",
        heading="Get in Touch",
        fields=[
            {"name": "name", "label": "Name", "type": "text", "required": True, "placeholder": "Your name"},
            {"name": "email", "label": "Email", "type": "email", "required": True, "placeholder": None},
            {"name": "message", "label": "Message", "type": "textarea", "required": False, "placeholder": None},
        ],
        action="/api/contact",
    )
    assert "kysc-contact-block" in html
    assert "<form" in html
    assert "/api/contact" in html
    assert "<textarea" in html
    assert 'type="email"' in html


def test_contact_block_select():
    html = _render(
        "contact_block",
        heading="H",
        fields=[
            {
                "name": "topic",
                "label": "Topic",
                "type": "select",
                "required": False,
                "placeholder": None,
                "options": [{"value": "ai", "label": "AI"}, {"value": "web", "label": "Web"}],
            },
        ],
        action="/submit",
    )
    assert "<select" in html
    assert "AI" in html


def test_contact_block_custom_submit():
    html = _render(
        "contact_block",
        heading="H",
        fields=[{"name": "x", "label": "X", "type": "text", "required": False, "placeholder": None}],
        action="/a",
        submit_text="Submit Now",
    )
    assert "Submit Now" in html


def test_contact_block_schema():
    assert block_schema("contact_block") == {
        "required": ["heading", "fields", "action"],
        "optional": ["method", "submit_text"],
    }


# --- pricing_table (NEW) ---


def test_pricing_table_renders():
    html = _render(
        "pricing_table",
        heading="Pricing",
        tiers=[
            {
                "name": "Starter",
                "price": "$499",
                "period": "/month",
                "features": ["5 pages", "Basic SEO"],
                "cta_text": "Get Started",
                "cta_href": "/contact",
                "highlighted": False,
            },
            {
                "name": "Pro",
                "price": "$999",
                "period": "/month",
                "features": ["10 pages", "Advanced SEO", "Analytics"],
                "cta_text": "Go Pro",
                "cta_href": "/contact",
                "highlighted": True,
            },
        ],
    )
    assert "kysc-pricing-table" in html
    assert "Starter" in html
    assert "Pro" in html
    assert "$999" in html
    assert "Popular" in html
    assert "&#10003;" in html


def test_pricing_table_footnote():
    html = _render(
        "pricing_table",
        heading="P",
        tiers=[
            {"name": "T", "price": "$1", "period": None, "features": [], "cta_text": "C", "cta_href": "/", "highlighted": False},
        ],
        footnote="All prices in USD",
    )
    assert "All prices in USD" in html


def test_pricing_table_schema():
    assert block_schema("pricing_table") == {
        "required": ["heading", "tiers"],
        "optional": ["footnote"],
    }


# --- faq_accordion (NEW) ---


def test_faq_accordion_renders():
    html = _render(
        "faq_accordion",
        heading="FAQ",
        items=[
            {"question": "How long?", "answer": "About 2 weeks."},
            {"question": "How much?", "answer": "Depends on scope."},
        ],
    )
    assert "kysc-faq-accordion" in html
    assert "<details" in html
    assert "<summary" in html
    assert "How long?" in html
    assert "About 2 weeks." in html


def test_faq_accordion_schema():
    assert block_schema("faq_accordion") == {
        "required": ["heading", "items"],
        "optional": [],
    }


# --- testimonials (NEW) ---


def test_testimonials_renders():
    html = _render(
        "testimonials",
        heading="What Clients Say",
        items=[
            {"quote": "Amazing work!", "name": "Alice", "title": "CEO, Acme", "avatar": "/img/alice.jpg"},
            {"quote": "Highly recommend.", "name": "Bob", "title": None, "avatar": None},
        ],
    )
    assert "kysc-testimonials" in html
    assert "Amazing work!" in html
    assert "Alice" in html
    assert "CEO, Acme" in html
    assert "/img/alice.jpg" in html
    assert "Highly recommend." in html


def test_testimonials_no_avatar():
    html = _render(
        "testimonials",
        heading="T",
        items=[{"quote": "Q", "name": "N", "title": None, "avatar": None}],
    )
    assert "<img" not in html


def test_testimonials_schema():
    assert block_schema("testimonials") == {
        "required": ["heading", "items"],
        "optional": ["columns"],
    }


# --- booking_embed (NEW) ---


def test_booking_embed_renders():
    html = _render(
        "booking_embed",
        heading="Book a Call",
        url="https://calendly.com/kevin",
    )
    assert "kysc-booking-embed" in html
    assert "<iframe" in html
    assert "https://calendly.com/kevin" in html
    assert 'loading="lazy"' in html
    assert "/contact" in html  # default fallback


def test_booking_embed_custom_fallback():
    html = _render(
        "booking_embed",
        heading="Schedule",
        url="https://calendly.com/test",
        fallback_href="/schedule",
        fallback_text="Email instead",
    )
    assert "/schedule" in html
    assert "Email instead" in html


def test_booking_embed_schema():
    assert block_schema("booking_embed") == {
        "required": ["heading", "url"],
        "optional": ["fallback_href", "fallback_text"],
    }


# --- cross-cutting: every block file exists ---


def test_all_block_files_exist():
    for slug in blocks():
        path = BLOCKS_DIR / f"{slug}.html"
        assert path.exists(), f"Missing block file: {slug}.html"


def test_all_blocks_have_schemas():
    for slug in blocks():
        schema = block_schema(slug)
        assert "required" in schema
        assert "optional" in schema


def test_all_blocks_have_paths():
    for slug in blocks():
        path = block_path(slug)
        assert path.endswith(f"{slug}.html")
