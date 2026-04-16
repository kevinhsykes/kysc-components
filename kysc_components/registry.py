from importlib.resources import files


_BLOCKS = ["nav", "hero", "footer"]

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
