from importlib.resources import files


def blocks() -> list[str]:
    return ["nav"]


def block_path(slug: str) -> str:
    if slug not in blocks():
        raise KeyError(f"unknown block: {slug}")
    return str(files("kysc_components.blocks").joinpath(f"{slug}.html"))
