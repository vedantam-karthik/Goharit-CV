# Goharit Computer Vision Module

## Project purpose

Goharit lets a customer select a roof on a map and decide on solar without waiting for a site visit. This module is the first AI step: from satellite or aerial imagery of the selected roof, it produces a clean, georeferenced map of the usable roof area and every obstacle on it, each with a confidence score.

## Architecture

```
Satellite / Aerial Image
        ↓
Roof Extraction & Image Preprocessing          (src/roof)
        ↓
Roof Mask / Crop
        ↓                     ↓
Obstacle & Vegetation         Roof Type &
Segmentation                  Imagery Quality
(src/obstacles)               (src/roof_analysis)
        ↓                     ↓
Geospatial Processing, Confidence, HITL & Integration
(src/geospatial, src/confidence, src/geojson, src/hitl,
 src/active_learning, src/pipeline)
        ↓
Final GeoJSON → Usable Roof Area
```

## Repository structure

```
Goharit-CV/
├── src/
│   ├── roof/                 preprocessing/ extraction/ postprocessing/ evaluation/
│   ├── obstacles/            annotation/ segmentation/ evaluation/
│   ├── roof_analysis/        classification/ imagery_quality/ evaluation/
│   ├── geospatial/
│   ├── confidence/
│   ├── geojson/
│   ├── hitl/
│   ├── active_learning/
│   └── pipeline/
├── configs/
├── scripts/
├── tests/
├── docs/
├── docker/
├── notebooks/
├── requirements/
├── .gitignore
└── README.md
```

Do not create new top-level folders without agreement from the team.

## Development rule

We will use individual local development environments. Git is the source of truth for code. The shared server will be used later for common datasets, GPU training, experiments and integration—not as a shared coding folder.

## Development setup

**Python version: 3.11.x.** Everyone uses this version. Do not install project packages globally.

1. Clone the repository and check it:

   ```
   git clone https://github.com/vedantam-karthik/Goharit-CV.git
   cd Goharit-CV
   git remote -v
   git branch
   ```

2. Check your Python and pip versions (both should report Python 3.11.x):

   ```
   python --version
   pip --version
   ```

   On Windows, if `python` points to another version, install 3.11 with `py install 3.11` and use `py -V:3.11` in place of `python` below.

3. Create your own virtual environment inside the repository. It is ignored by git.

   ```
   python -m venv .venv
   ```

4. Activate it:

   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`

## Development branches

```
main      → stable production code
develop   → integration branch
feature/* → individual development
```

- **main**: stable, accepted code. Never develop here directly.
- **develop**: team integration branch. Features are merged here after review.
- **feature/\***: individual development branches.

`main` and `develop` are protected. Changes reach them only through reviewed pull requests.

## Team ownership

| Member | Stories | Area | Feature branch |
|---|---|---|---|
| Keerthana | 1–10 | Roof Extraction & Image Preprocessing | `feature/keerthana-roof-extraction` |
| Sameeksha | 11–20 | Obstacle & Vegetation Segmentation | `feature/sameeksha-obstacle-segmentation` |
| Omkar | 21–30 | Roof Type & Imagery Quality | `feature/omkar-roof-quality` |
| Karthik | 31–48 | Geospatial, Confidence, HITL & Integration | `feature/karthik-geospatial` |
| Cross-Team | 49–56 | Integration & Validation | — |

## Running locally

Nothing to run yet. Entry points will be documented here as they are added under `src/pipeline/` and `scripts/`.

## Testing

Tests live in `tests/`. Run all tests locally before every push and pull request. The exact test command will be documented here once the test tooling is added.

## Contribution workflow

```
Individual Desktop → Feature Branch → Local Development → Local Testing
→ Git Commit → Push → Pull Request → Code Review → develop
→ Integration Testing → main
```

1. Start from an up-to-date `develop`:

   ```
   git checkout develop
   git pull origin develop
   git checkout -b feature/<name>-<area>
   ```

2. Develop and test locally. Commit in small, focused steps.

3. Before opening a pull request, bring in the latest team changes:

   ```
   git pull origin develop
   ```

4. Push your branch and open a pull request into `develop`:

   ```
   git push -u origin feature/<name>-<area>
   ```

5. After review and approval, the pull request is merged into `develop`.

6. After integration testing, `develop` is merged into `main` through a release pull request.

**Never commit:** datasets, imagery, model weights or checkpoints, logs, `.env` files or API keys. The `.gitignore` covers these; check `git status` before every commit.
