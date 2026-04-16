from importlib.resources import files


_BLOCKS = [
    "nav",
    "hero",
    "footer",
    "about",
    "services",
    "gallery",
    "contact_block",
    "pricing_table",
    "faq_accordion",
    "testimonials",
    "booking_embed",
]

_SCHEMAS: dict[str, dict[str, list[str]]] = {
    "nav": {
        "required": ["items", "brand"],
        "optional": [],
    },
    "hero": {
        "required": ["headline", "subhead", "cta_text", "cta_href"],
        "optional": ["bg_image"],
    },
    "footer": {
        "required": ["copyright", "links"],
        "optional": [],
    },
    "about": {
        "required": ["heading", "body"],
        "optional": ["image", "image_alt", "reverse"],
    },
    "services": {
        "required": ["heading", "items"],
        "optional": ["columns"],
    },
    "gallery": {
        "required": ["heading", "items"],
        "optional": ["columns"],
    },
    "contact_block": {
        "required": ["heading", "fields", "action"],
        "optional": ["method", "submit_text"],
    },
    "pricing_table": {
        "required": ["heading", "tiers"],
        "optional": ["footnote"],
    },
    "faq_accordion": {
        "required": ["heading", "items"],
        "optional": [],
    },
    "testimonials": {
        "required": ["heading", "items"],
        "optional": ["columns"],
    },
    "booking_embed": {
        "required": ["heading", "url"],
        "optional": ["fallback_href", "fallback_text"],
    },
}


def blocks() -> list[str]:
    return list(_BLOCKS)


def block_path(slug: str) -> str:
    if slug not in _BLOCKS:
        raise KeyError(f"unknown block: {slug}")
    return str(files("kysc_components.blocks").joinpath(f"{slug}.html"))


def block_schema(slug: str) -> dict[str, list[str]]:
    if slug not in _SCHEMAS:
        raise KeyError(f"unknown block: {slug}")
    return {k: list(v) for k, v in _SCHEMAS[slug].items()}
