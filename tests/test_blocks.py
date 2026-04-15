from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import kysc_components
from kysc_components.registry import blocks


BLOCKS_DIR = Path(kysc_components.__file__).parent / "blocks"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(BLOCKS_DIR)),
        autoescape=select_autoescape(["html"]),
    )


def test_version_matches_pyproject():
    assert kysc_components.__version__ == "0.1.0"


def test_registry_lists_nav():
    assert "nav" in blocks()


def test_nav_renders_without_error():
    template = _env().get_template("nav.html")
    html = template.render()
    assert "Hello from nav block" in html
    assert "<nav" in html
