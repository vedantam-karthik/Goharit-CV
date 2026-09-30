# Input/Output Contract — DRAFT for team session

**Status:** draft, for discussion. Nothing here is final until the decision table (section 4) is filled in and merged via a PR.

**Session:** 30–60 min. Attendees: Keerthana (M1), Sameeksha (M2), Omkar (M3), Karthik (M4).

**Goal:** agree the data each member hands to the next *before* model work starts. Downstream members can then build against ground truth or a baseline without waiting for upstream models.

**Sources:**
- **Brief:** *Goharit – Computer Vision Brief*.
- **Plan:** *4-Member Implementation & Collaboration Plan*.
- **Proposed:** not in either document; needs agreement in the session.

---

## 1. Final output — fixed by the Brief (§2)

GeoJSON FeatureCollection, **one feature per object**.

| Field | Values |
|---|---|
| `class` | `roof`, `tank`, `mumty`, `ac_unit`, `dish`, `solar_existing`, `parapet`, `tree`, `other` |
| `geometry` | Polygon in map coordinates |
| `confidence` | 0 to 1, **calibrated** |
| `source` | `model`, `user_edited`, `user_added` |
| roof-level fields | `roof_type`, `imagery_quality_score` |

## 2. Rule every prediction must follow (Plan, "Final team rule")

Every prediction keeps: **image ID, roof ID, model version, raw confidence, and the original coordinate/reference information.**

## 3. Draft hand-offs

### Input to M1 (image + metadata) — *Proposed*
- `image_id`, `image` (rows × cols × bands, RGB).
- `crs` and a **full affine geotransform**. The Brief only mentions "coordinate system and pixel size", which isn't enough to place a crop on the map.
- `pixel_size_m`, `capture_date` (if available), `capture_angle` (if available; Google APIs don't provide it).
- `city`, `imagery_source`.
- Optional prompt: user tap point, rough polygon or building footprint.

### M1 → M2, M3, M4: roof — *Plan + Proposed*
`extract_roof(image, metadata, prompt)` returns:
- `image_id`, `roof_id`;
- `roof_mask` (boolean, image pixel grid);
- `pixel_offset` (row, col) if the mask covers only a crop (*Proposed*);
- `roof_confidence_raw` (0–1);
- `model_name`, `model_version`.

### M2 → M4: obstacles — *Plan + Proposed*
`detect_obstacles(image, roof, metadata)` returns a list, one entry per object instance:
- `image_id`, `roof_id`, `instance_id`;
- `label` (M2's class, mapped to a Brief §2 `class`);
- `mask`, `pixel_offset`, `confidence_raw`, `model_version`.

### M3 → M4: roof type and imagery quality — *Plan + Proposed*
- `classify_roof_type(image, roof, metadata)` returns `image_id`, `roof_id`, `roof_type`, `roof_type_confidence_raw`, `model_version`.
- `assess_image_quality(image, metadata)` returns `image_id`, individual indicators (`cloud`, `blur`, `shadow`, `off_nadir`, `resolution`; "old imagery" comes from `capture_date`), `overall_quality` 0–1, `model_version`.

### M4 → M1, M2, M3: corrections and difficult examples — *Plan*
Every stored correction keeps the original prediction. The Brief lists three correction types: delete a false detection, add a missed obstacle, redraw the roof outline.

---

## 4. Decisions to make in the session (agenda)

| # | Topic | Question | Options / starting point | Decision | Owner |
|---|---|---|---|---|---|
| 1 | Pipeline order (5 min) | The Plan shows three different orders. Which is official? | Quality → roof → (type ‖ obstacles) | | |
| 2 | IDs (5 min) | Who creates `roof_id` and `instance_id`, and in what format? | M1 creates roof_id; M2 creates instance_id; UUID strings | | |
| 3 | Georeference (5 min) | Is the full affine transform plus CRS mandatory in the metadata? | Yes: read from the GeoTIFF; computed for Static Maps | | |
| 4 | Masks (5 min) | Mask format in memory and on disk? Full image grid or crop plus offset? | numpy bool in memory; COCO RLE on disk; offset allowed | | |
| 5 | Classes (10 min) | Map M2 labels to Brief classes. Where do Phase-2 classes go (chimney/vent, skylight, drying structure, shed)? Is the parapet an obstacle or the roof boundary? | Phase-2 → `other` until data exists? | | |
| 6 | Roof type names (2 min) | Exact spellings | `flat_rcc`, `sloped_tile`, `metal_sheet`, `other` | | |
| 7 | Quality score (5 min) | Scale and meaning of `overall_quality`; which threshold triggers "review / better imagery"? | 0–1, higher = better; threshold after baseline | | |
| 8 | Confidence (5 min) | What single number does each model output as `confidence_raw`? (SAM 2 gives predicted IoU, not a probability) | Per-instance score, 0–1 | | |
| 9 | Output CRS (3 min) | GeoJSON in WGS84 (the RFC 7946 standard) with areas computed in metres (UTM)? | Yes | | |
| 10 | Versioning (3 min) | `model_version` format | `<model>-<semver>` or git SHA | | |
| 11 | Imagery licence (5 min, info) | The Google Maps Platform terms appear to prohibit using Google content for model training/validation. The exact clause wasn't confirmed, and legal review is pending. Which imagery do we train on? | Pending legal answer; don't build training sets from Google imagery until then | | Karthik |

**Parked, needs the product team:**
- usable-area exclusion rules (setbacks, buffers, which classes are excluded);
- usable-area tolerance;
- first city;
- GPU budget.

---

## 5. After the session
1. Fill in the Decision and Owner columns.
2. Change the status to **Agreed** and merge via a PR into `develop`.
3. Any later contract change needs a PR reviewed by every member it affects.
