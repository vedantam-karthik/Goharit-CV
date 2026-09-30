"""Setup check: passes when a developer's local environment matches the team standard."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AGREED_FOLDERS = [
    "src/roof/preprocessing",
    "src/roof/extraction",
    "src/roof/postprocessing",
    "src/roof/evaluation",
    "src/obstacles/annotation",
    "src/obstacles/segmentation",
    "src/obstacles/evaluation",
    "src/roof_analysis/classification",
    "src/roof_analysis/imagery_quality",
    "src/roof_analysis/evaluation",
    "src/geospatial",
    "src/confidence",
    "src/geojson",
    "src/hitl",
    "src/active_learning",
    "src/pipeline",
    "configs",
    "scripts",
    "tests",
    "docs",
    "docker",
    "notebooks",
    "requirements",
]


def test_python_is_3_12():
    assert sys.version_info[:2] == (3, 12), f"Team standard is Python 3.12.x, found {sys.version.split()[0]}"


def test_running_inside_a_virtual_environment():
    assert sys.prefix != sys.base_prefix, "Activate the project's .venv before running the tests"


def test_agreed_folder_structure_exists():
    missing = [f for f in AGREED_FOLDERS if not (ROOT / f).is_dir()]
    assert not missing, f"Missing agreed folders: {missing}"
