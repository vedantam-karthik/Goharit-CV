"""Setup check: every pinned dependency is importable and installed at exactly the pinned version."""

import importlib
import re
from importlib.metadata import version
from pathlib import Path

import pytest

REQUIREMENTS = Path(__file__).resolve().parents[1] / "requirements"

# Distribution name -> module to import.
IMPORT_NAMES = {
    "PyYAML": "yaml",
    "pydantic": "pydantic",
    "pydantic-settings": "pydantic_settings",
    "rasterio": "rasterio",
    "shapely": "shapely",
    "pyproj": "pyproj",
    "scikit-learn": "sklearn",
    "numpy": "numpy",
    "opencv-python-headless": "cv2",
    "pillow": "PIL",
    "pytest": "pytest",
    "ruff": None,  # command-line tool, no Python module to import
}


def _pins() -> dict[str, str]:
    pins = {}
    for name in ("base.txt", "dev.txt"):
        for line in (REQUIREMENTS / name).read_text(encoding="utf-8").splitlines():
            m = re.fullmatch(r"\s*([A-Za-z0-9_.\-]+)==([^\s#]+)\s*(#.*)?", line)
            if m:
                pins[m.group(1)] = m.group(2)
    return pins


PINS = _pins()


def test_every_pin_is_checked():
    assert set(PINS) == set(IMPORT_NAMES), "Update IMPORT_NAMES when requirements change"


@pytest.mark.parametrize("dist", sorted(PINS))
def test_pinned_version_installed(dist):
    assert version(dist) == PINS[dist], f"{dist}: installed {version(dist)}, pinned {PINS[dist]}"
    if IMPORT_NAMES[dist]:
        importlib.import_module(IMPORT_NAMES[dist])
