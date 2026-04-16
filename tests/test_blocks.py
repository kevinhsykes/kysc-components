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


def test_version_matches_pyproject():
    assert kysc_components.__version__ == "0.2.0"


def test_registry_lists_all_blocks():
    assert blocks() == ["nav", "hero", "footer"]


def test_block_path_rejects_unknown():
    with pytest.raises(KeyError):
        block_path("nope")


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


def test_schema_matches_macro_signatures():
    assert block_schema("nav") == {"required": ["items", "brand"], "optional": []}
    assert block_schema("hero") == {
        "required": ["headline", "subhead", "cta_text", "cta_href"],
        "optional": ["bg_image"],
    }
    assert block_schema("footer") == {"required": ["copyright", "links"], "optional": []}


def test_schema_rejects_unknown():
    with pytest.raises(KeyError):
        block_schema("nope")


def test_tailwind_preset_is_packaged():
    preset = Path(kysc_components.__file__).parent / "tailwind" / "preset.js"
    assert preset.exists()
    body = preset.read_text(encoding="utf-8")
    assert "module.exports" in body
    assert "brand" in body
