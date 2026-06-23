# FULL OFFLINE VALIDATION V4 — YEAR_END 2024 LOCKED DECISIONS

Generated: 2026-06-24

## Why V4 exists

V3 still contained conditional language inside embedded run files. V4 is a closed, no-internet decision file.
Codex must not decide whether a model is current. Codex must only apply the action in the locked decision ledger.

## Absolute Codex rules

- No internet browsing.
- No year inference.
- No use of `2026` as a fake current marker.
- Current rows use `year_end: null`.
- No mass replace of `2024` to `null`.
- The locked ledger below is the source of truth for all 257 `year_end: 2024` suspect profile entries.
- The missing-profile section is the source of truth for Tesla Model 3, Peugeot 3008, Chery FX, and Mazda CX-30.
- Source URLs embedded in this file are evidence anchors already selected outside Codex.
- Add source objects with numeric `source_index` values. No placeholders.
- Every `source_indexes` and `field_sources` value must point to an existing source inside the same profile.
- EV rows use `engine_displacement_l: null`.
- Hybrid, mild-hybrid and plug-in-hybrid rows keep the ICE displacement listed in the target row.
- Every variant must include `version_or_trim`, using `null` for no grounded trim.
- Recompute `available_values_for_website` after every profile change.

## Action code meanings

| Action code | Codex operation |
|---|---|
| `LOCK_SET_PROFILE_CURRENT` | Set profile-level `year_end` to `null`. Set all profile variant rows currently ending in `2024` to `null`. Add note: `V4_LOCK: 2024 was corrected as a cutoff artifact.` |
| `FINAL_CHANGE_TO_CURRENT` | Set the named current row(s) to `year_end:null`, and set profile-level `year_end:null`. |
| `FINAL_SPLIT_CURRENT` | Preserve legacy 2024 rows and add the named current row with `year_end:null`. Set profile-level `year_end:null`. |
| `FINAL_FIX_YEAR_END_TO_2022` | Change the relevant historical row from `year_end:2024` to `year_end:2022`. Do not mark current. |
| `FINAL_RETAIN_2024` | Keep `year_end:2024` at profile/variant level and add note: `V4_LOCK: 2024 retained after offline final validation.` |
| `FINAL_MERGE_DUPLICATE_RETAIN_2024` | Merge duplicate profiles into one canonical profile. Preserve valid variants and sources. Keep `year_end:2024`. |
| `LOCK_RETAIN_2024` | Keep `year_end:2024` and add note: `V4_LOCK: 2024 retained; current Israeli row was not grounded in offline validation.` |

## Counts

| Bucket | Count |
|---|---:|
| Suspect profile entries locked in ledger | 257 |
| Profiles/current entries to open/change | 138 |
| Exact historical-year corrections | 1 |
| Retain 2024 / duplicate-retain decisions | 118 |
| Duplicate merge retain decisions | 0 |
| Missing full model profiles to add | 4 |

---

# LOCKED DECISION LEDGER — ALL 257 SUSPECT PROFILE ENTRIES

| Run | Profile entry | Locked action | Exact target | Evidence / rationale |
|---:|---|---|---|---|
| 1 | Abarth \| 500 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Aiways \| U6 | `FINAL_RETAIN_2024` | retain profile/model year_end=2024; keep variant year_end=2024 | No current official/importer evidence found in the final offline pass. Do not open to current. |
| 1 | Alfa Romeo \| Stelvio | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| A4 | `FINAL_RETAIN_2024` | retain 2024 | Replaced by new Audi A5/S5 family; do not open A4 as current. |
| 1 | Audi \| A5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| A6 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| A8 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| e-tron GT | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| Q5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| Q7 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| R8 | `FINAL_RETAIN_2024` | retain 2024 | R8 is discontinued; no current Israeli new-car page. |
| 1 | Audi \| RS4 | `FINAL_RETAIN_2024` | retain 2024 | No current RS4 Israeli new-car page in final offline pass. |
| 1 | Audi \| RS5 | `FINAL_SPLIT_CURRENT` | keep legacy RS5 rows ending 2024; add/split current Audi RS 5 Sedan e-hybrid row with year_start=2026, year_end=null | Audi Israel currently exposes the all-new RS 5 Sedan e-hybrid. Old coupe/sportback RS5 rows must not be blindly opened; add current sedan/e-hybrid row only. |
| 1 | Audi \| RS7 | `FINAL_RETAIN_2024` | retain 2024 | No current RS7 Israeli new-car page in final offline pass; do not infer from RS family. |
| 1 | Audi \| S3 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Audi \| SQ5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Bentley \| Continental GT | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Bentley \| Flying Spur | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| 118i | `FINAL_RETAIN_2024` | retain 2024 | Current BMW Israel 1 Series price list exposes 116/120/M135, not 118i. |
| 1 | BMW \| 120i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| 128ti | `FINAL_RETAIN_2024` | retain 2024 | Current BMW Israel 1 Series price list does not expose 128ti. |
| 1 | BMW \| 218i Gran Coupe | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| 225xe (Active Tourer PHEV) | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 1 | BMW \| 318i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| 320e | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| 640i GT | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW \| 850i | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW \| i4 eDrive35 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| iX xDrive40 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| M135i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| M2 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| M8 | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW \| M850i | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 1 | BMW \| X2 M35i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| X3 2.0i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| X3 M | `FINAL_RETAIN_2024` | retain 2024 | Current X3 exists, but X3 M is not grounded as current in final offline pass. |
| 1 | BMW \| X3 M40i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| X3 xDrive30e | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BMW \| X6 M | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence for X6 M row; do not open. |
| 1 | BMW \| Z4 sDrive20i | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BYD \| Atto 3 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BYD \| Dolphin | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BYD \| Han | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | BYD \| Tang | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Cadillac \| XT5 | `FINAL_RETAIN_2024` | retain 2024 | Cadillac Israel current lineup found XT6/Optiq/Escalade IQ context, not XT5. |
| 1 | Chery \| Tiggo 7 Pro | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Chery \| Tiggo 8 Pro | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 1 | Chevrolet \| Camaro | `FINAL_RETAIN_2024` | retain 2024 | Camaro generation ended after MY2024; no current Chevrolet Israel listing. |
| 1 | Chevrolet \| Equinox | `FINAL_RETAIN_2024` | retain 2024 | Chevrolet Israel current lineup does not support Equinox as new current. |
| 1 | Citroen \| Berlingo | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| C3 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| C3 Aircross | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| C4 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| C5 X | `FINAL_RETAIN_2024` | retain 2024 | Citroen Israel current range does not show C5 X; do not open. |
| 2 | Citroen \| Jumper | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| Jumpy | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Citroen \| SpaceTourer | `FINAL_RETAIN_2024` | retain 2024 | Citroen Israel current range does not show SpaceTourer; Jumpy/Berlingo are separate. |
| 2 | Cupra \| Ateca | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli Cupra Ateca support in final offline pass. |
| 2 | Cupra \| Born | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli Cupra Born support in final offline pass. |
| 2 | Cupra \| Formentor | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Cupra \| Leon | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Dacia \| Jogger | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Dodge \| Durango | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | DS Automobiles \| DS 4 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | DS Automobiles \| DS 7 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | DS Automobiles \| DS 9 | `FINAL_RETAIN_2024` | retain 2024 | DS Israel current visible model support centered on DS 7/DS 4 context, not DS 9. |
| 2 | Ferrari \| 812 Superfast | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; model is not a current 2026 row. |
| 2 | Ferrari \| Portofino | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 2 | Fiat \| 500e | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Ford \| Bronco | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Ford \| Explorer | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Ford \| F-150 | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current passenger/commercial evidence did not ground F-150 as current new-car row. |
| 2 | Ford \| Kuga | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Kuga as current. |
| 2 | Ford \| Mustang Mach-E | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Mach-E as current. |
| 2 | Ford \| Puma | `FINAL_RETAIN_2024` | retain 2024 | Ford Israel current lineup did not ground Puma as current. |
| 2 | Ford \| Transit | `FINAL_RETAIN_2024` | retain 2024 | No current local Transit row sufficiently grounded in final offline pass; do not infer from global Ford. |
| 2 | Geely \| Geometry C | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Genesis \| G70 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Genesis \| GV70 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hongqi \| E-HS9 | `FINAL_CHANGE_TO_CURRENT` | set profile year_end=null; preserve old 2024 rows that are legacy body/powertrain rows; add the current row named in the rationale with year_end=null | Hongqi Israel still exposes HONGQI 9/EHS9 official current pages. |
| 2 | Hyundai \| Bayon | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Creta | `FINAL_RETAIN_2024` | retain 2024 | No current Hyundai Israel evidence in final offline pass; do not open. |
| 2 | Hyundai \| i10 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| i20 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| i30 N | `FINAL_RETAIN_2024` | retain 2024 | No current Hyundai Israel evidence in final offline pass; do not open. |
| 2 | Hyundai \| Ioniq 5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Ioniq 6 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Palisade | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Santa Fe | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Sonata | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Hyundai \| Staria | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Infiniti \| QX60 | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jaguar \| F-Pace | `FINAL_RETAIN_2024` | retain 2024 | Jaguar new-car activity/current status not grounded enough; do not open. |
| 2 | Jaguar \| F-Type | `FINAL_RETAIN_2024` | retain 2024 | F-Type discontinued globally and not current locally; retain 2024. |
| 2 | Jaguar \| XE | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jaguar \| XF | `FINAL_RETAIN_2024` | retain 2024 | No current official Israeli evidence; do not open. |
| 2 | Jeep \| Avenger | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 2 | Jeep \| Compass | `FINAL_RETAIN_2024` | retain 2024 | Jeep Israel current focus did not ground Compass as active current in final pass. |
| 2 | Jeep \| Renegade | `FINAL_RETAIN_2024` | retain 2024 | Jeep Israel current focus did not ground Renegade as active current in final pass. |
| 2 | Jeep \| Wrangler | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Kia \| Carnival | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Kia \| Ceed SW | `FINAL_RETAIN_2024` | retain 2024 | Kia Israel current model range does not show Ceed SW. |
| 3 | Kia \| Sorento | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Kia \| Stonic | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lamborghini \| Huracan | `FINAL_RETAIN_2024` | retain 2024 | Huracan is not a current new-car profile; retain 2024. |
| 3 | Lamborghini \| Huracan | `FINAL_RETAIN_2024` | retain 2024 | Huracan is not a current new-car profile; retain 2024. |
| 3 | Land Rover \| Defender | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Discovery | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Discovery Sport | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Range Rover | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Range Rover Evoque | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Range Rover Sport | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Range Rover Velar | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Land Rover \| Range Rover Velar | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Leapmotor \| T03 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lexus \| ES | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lexus \| ES | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lexus \| LBX | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lexus \| LC | `FINAL_RETAIN_2024` | retain 2024 | Lexus Israel current new-cars pass did not ground LC as current; do not open. |
| 3 | Lexus \| LS | `FINAL_CHANGE_TO_CURRENT` | set profile year_end=null; preserve old 2024 rows that are legacy body/powertrain rows; add the current row named in the rationale with year_end=null | Lexus Israel exposes LS 500h as current new-car page with price and hybrid powertrain. |
| 3 | Lexus \| UX | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Lynk & Co \| 01 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Maserati \| Ghibli | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 3 | Maserati \| GranCabrio | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Maserati \| Grecale | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Maserati \| Quattroporte | `FINAL_RETAIN_2024` | retain 2024 | No current Israeli new-car evidence; do not open. |
| 3 | Maxus \| Euniq 5 | `FINAL_RETAIN_2024` | retain 2024 | Maxus Israel current contact/model set moved to MIFA 7/9, not Euniq. |
| 3 | Maxus \| Euniq 6 | `FINAL_RETAIN_2024` | retain 2024 | Maxus Israel current contact/model set moved to MIFA 7/9, not Euniq. |
| 3 | Mazda \| CX-3 | `FINAL_RETAIN_2024` | retain 2024 | Mazda CX-3 is not on Mazda Israel 2026 current price list; Israeli source marks marketing stopped. |
| 3 | Mazda \| CX-3 | `FINAL_RETAIN_2024` | retain 2024 | Mazda CX-3 is not on Mazda Israel 2026 current price list; Israeli source marks marketing stopped. |
| 3 | Mazda \| CX-5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mazda \| Mazda2 | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024; merge duplicate Mazda2 profiles into one canonical profile | Mazda Israel official current models/price-list pass did not ground Mazda2 as active; secondary listings are not enough. |
| 3 | Mazda \| Mazda2 | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024; merge duplicate Mazda2 profiles into one canonical profile | Mazda Israel official current models/price-list pass did not ground Mazda2 as active; secondary listings are not enough. |
| 3 | Mazda \| MX-5 | `FINAL_RETAIN_2024` | retain 2024 | Mazda Israel 2026 current price list does not ground MX-5 as active new-car row. |
| 3 | McLaren \| Artura | `FINAL_RETAIN_2024` | retain 2024 | No robust local current evidence; do not open. |
| 3 | Mercedes-Benz \| A-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| B-Class | `FINAL_RETAIN_2024` | retain 2024 | Mercedes Israel current model pass does not show B-Class. |
| 3 | Mercedes-Benz \| C-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| Citan | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| CLE | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| E-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| EQS | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| EQS SUV | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| EQV | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| G-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| GLA | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| GLB | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| GLS | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 3 | Mercedes-Benz \| Maybach GLS | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set Maybach GLS 600 current row year_end=null | Mercedes-Benz Israel current Maybach GLS page exposes Maybach GLS 600 4Matic Ultimate FL as active. |
| 3 | Mercedes-Benz \| S-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mercedes-Benz \| SL | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mercedes-Benz \| V-Class | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mercedes-Benz \| Vito | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | MG \| HS | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | MG \| Marvel R | `FINAL_RETAIN_2024` | retain 2024 | MG Israel current model/shop list does not show Marvel R. |
| 4 | MG \| MG4 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | MG \| ZS EV | `FINAL_RETAIN_2024` | retain 2024 | MG Israel current model/shop list shows ZS Hybrid and newer EVs, not ZS EV as current new row. |
| 4 | Mini \| Aceman | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mini \| Cabrio | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mini \| Clubman | `FINAL_RETAIN_2024` | retain 2024 | MINI Clubman is not current in final pass; do not open. |
| 4 | Mini \| Cooper S | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mini \| Cooper SE | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mini \| Countryman | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mitsubishi \| ASX | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Mitsubishi \| L200 | `FINAL_FIX_YEAR_END_TO_2022` | change L200/Triton historical row year_end from 2024 to 2022 where the row maps to the official Israel Triton/L200 generation; do NOT set null | Mitsubishi Israel official past-model page grounds Triton 2015-2022. |
| 4 | NIO \| EL6 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | NIO \| ET5 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Nissan \| Altima | `FINAL_RETAIN_2024` | retain 2024 | Nissan Israel current range does not show Altima. |
| 4 | Nissan \| Ariya | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Nissan \| Juke | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Nissan \| Leaf | `FINAL_RETAIN_2024` | retain 2024 | Nissan Israel treats Leaf as legacy; current range does not show it. |
| 4 | Nissan \| Qashqai | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Nissan \| X-Trail | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Omoda \| C5 | `FINAL_RETAIN_2024` | retain 2024 | Omoda Israel current official range shows OMODA 7/9, not C5/5 as active current row. |
| 4 | Opel \| Astra | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Combo | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Corsa | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Crossland | `FINAL_CHANGE_TO_CURRENT` | set profile year_end=null; preserve old 2024 rows that are legacy body/powertrain rows; add the current row named in the rationale with year_end=null | Opel Israel current price list exposes Crossland Edition/Elegance 1.2L 130hp. |
| 4 | Opel \| Grandland | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Grandland | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Mokka | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Opel \| Vivaro | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Ora \| Funky Cat | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Peugeot \| 208 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Peugeot \| 408 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Peugeot \| Expert | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Peugeot \| Rifter | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Polestar \| 2 | `FINAL_RETAIN_2024` | retain 2024 | Polestar Israel says no cars available for purchase; do not open current. |
| 4 | Porsche \| 718 Boxster | `FINAL_SPLIT_CURRENT` | set profile year_end=null; preserve old 2024 rows that are legacy body/powertrain rows; add the current row named in the rationale with year_end=null | Porsche Israel official 718 page/configurator exposes current 718 range. |
| 4 | Porsche \| 911 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | RAM \| 1500 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | RAM \| 2500 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Arkana | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Austral | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Captur | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Clio | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Koleos | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show Koleos. |
| 4 | Renault \| Master | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 4 | Renault \| Megane | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show legacy Megane as new car. |
| 4 | Renault \| Megane E-Tech | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range did not ground Megane E-Tech as current new-car row; Renault 5 E-Tech is separate. |
| 5 | Renault \| Trafic | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Renault \| Zoe | `FINAL_RETAIN_2024` | retain 2024 | Renault Israel current range does not show Zoe; Renault 5 E-Tech is separate. |
| 5 | Seat \| Arona | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Seat \| Ateca | `FINAL_RETAIN_2024` | retain 2024 | Seat Israel current homepage shows Arona/Ibiza only, not Ateca. |
| 5 | Seat \| Ibiza | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Seat \| Tarraco | `FINAL_RETAIN_2024` | retain 2024 | Seat Israel current homepage shows Arona/Ibiza only, not Tarraco. |
| 5 | Skoda \| Karoq | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Skoda \| Kodiaq | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Skoda \| Octavia | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Skoda \| Scala | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Skywell \| ET5 | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | SsangYong \| Torres | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Subaru \| Ascent | `FINAL_RETAIN_2024` | retain 2024 | Subaru Israel current range shows Outback/Crosstrek/Forester/BRZ, not Ascent. |
| 5 | Subaru \| Outback | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Subaru \| WRX | `FINAL_RETAIN_2024` | retain 2024 | Subaru Israel current range does not show WRX. |
| 5 | Suzuki \| Jimny | `FINAL_RETAIN_2024` | retain 2024 | No current official new-car evidence; do not open. |
| 5 | Tesla \| Model X | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Aygo X | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| bZ4X | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Corolla | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Corolla Cross | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| GR86 | `FINAL_RETAIN_2024` | retain 2024 | Toyota Israel current new-car list did not ground GR86 as active. |
| 5 | Toyota \| Highlander | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Hilux | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Land Cruiser | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Land Cruiser Prado | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Proace City | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Proace City | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Sienna | `FINAL_RETAIN_2024` | retain 2024 | No official Toyota Israel new-car evidence; do not open. |
| 5 | Toyota \| Supra | `FINAL_RETAIN_2024` | retain 2024 | Toyota Israel current new-car list did not ground Supra as active. |
| 5 | Toyota \| Yaris | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Toyota \| Yaris Cross | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Arteon | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range does not ground Arteon as active; retain. |
| 5 | Volkswagen \| Arteon | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range does not ground Arteon as active; retain. |
| 5 | Volkswagen \| Caddy | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Crafter | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| golf | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Golf GTI | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| ID.3 | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range/search did not ground ID.3 as active; do not open. |
| 5 | Volkswagen \| ID.3 | `FINAL_RETAIN_2024` | retain 2024 | VW Israel current range/search did not ground ID.3 as active; do not open. |
| 5 | Volkswagen \| ID.4 | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| ID.5 | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Multivan | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| polo | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| T-Cross | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Taigo | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Tiguan | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volkswagen \| Touareg | `FINAL_RETAIN_2024` | retain 2024 | Touareg not grounded as current; retain 2024. |
| 5 | Volkswagen \| Transporter | `LOCK_RETAIN_2024` | retain profile/variant year_end=2024 | V4 offline decision did not ground a current Israeli new-car row. Codex keeps 2024 and adds a retained-note. |
| 5 | Volvo \| C40 | `LOCK_RETAIN_2024` | retain 2024; do not create EC40 merge here | Volvo current range uses EC40 context; old C40 name is not opened in this pass. |
| 6 | Volvo \| S90 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground S90 as active. |
| 6 | Volvo \| V60 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground V60 as active. |
| 6 | Volvo \| V90 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground V90 as active. |
| 6 | Volvo \| V90 | `FINAL_RETAIN_2024` | retain 2024 | Volvo Israel current pricing/model pass does not ground V90 as active. |
| 6 | Volvo \| XC40 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 6 | Volvo \| XC60 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |
| 6 | Volvo \| XC90 | `LOCK_SET_PROFILE_CURRENT` | set profile year_end=null; set every profile row with year_end=2024 to year_end=null, then add one note that 2024 was a source-cutoff artifact in V4 | Main run offline validation marked this Israeli model line as active/current or requiring a current split. V4 closes the decision as current, with no Codex web check. |

---

# MISSING FULL PROFILES — ADD FROM ZERO

## 1. Tesla Model 3

**Profile keys**

```json
{
  "market": "IL",
  "make": "Tesla",
  "model": "Model 3",
  "canonical_model": "Model 3",
  "year_start": 2021,
  "year_end": null,
  "profile_confidence": "high"
}
```

**Target technical variants**

| version_or_trim | body_type | fuel_type | engine | engine_displacement_l | horsepower_hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Standard Range Plus | Sedan | electric | electric | null | 283 | single_speed | RWD | 2021 | 2021 | direct |
| RWD | Sedan | electric | electric | null | 283 | single_speed | RWD | 2022 | 2023 | direct |
| Long Range AWD | Sedan | electric | electric | null | 441 | single_speed | AWD | 2021 | 2023 | direct |
| Performance | Sedan | electric | electric | null | 460 | single_speed | AWD | 2021 | 2023 | direct |
| RWD / Highland | Sedan | electric | electric | null | 283 | single_speed | RWD | 2024 | null | direct |
| Long Range RWD | Sedan | electric | electric | null | 320 | single_speed | RWD | 2025 | null | direct |
| Long Range AWD / Highland | Sedan | electric | electric | null | 498 | single_speed | AWD | 2024 | null | direct |
| Performance / Highland | Sedan | electric | electric | null | 460 | single_speed | AWD | 2024 | null | direct |
| Standard | Sedan | electric | electric | null | 283 | single_speed | RWD | 2026 | null | direct |

**Source anchors to add**

- Tesla Israel Model 3 current page: `https://www.tesla.com/he_il/model3`
- Israeli 2026 Model 3 launch/current article source already selected in prior validation package.
- Israeli used/current catalog source for 2021-2024 Model 3 rows already selected in prior validation package.

**Notes to add**

- `V4_LOCK: Tesla Model 3 was missing from the clean catalog and must be added as a full profile covering Israeli sale history from 2021 through current.`
- `V4_LOCK: Israeli Performance horsepower is locked to 460 hp for this pass; do not use the earlier ungrounded 627 hp value.`
- `V4_LOCK: EV schema uses engine_displacement_l=null and transmission=single_speed.`

## 2. Peugeot 3008

**Profile keys**

```json
{
  "market": "IL",
  "make": "Peugeot",
  "model": "3008",
  "canonical_model": "3008",
  "year_start": 2010,
  "year_end": null,
  "profile_confidence": "high"
}
```

Do not merge this profile into existing `Peugeot e-3008`.

**Target technical variants**

| version_or_trim | body_type | fuel_type | engine | engine_displacement_l | horsepower_hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Active / Comfort-era | SUV | petrol | 1.6L turbo | 1.6 | 156 | automatic | FWD | 2010 | 2014 | direct |
| Facelift-era | SUV | petrol | 1.6L turbo | 1.6 | 165 | automatic | FWD | 2015 | 2016 | direct |
| Active / Premium-era | SUV | diesel | 1.6L diesel | 1.6 | 120 | automatic | FWD | 2017 | 2018 | direct |
| Active / Premium-era | SUV | diesel | 1.5L diesel | 1.5 | 130 | automatic | FWD | 2018 | 2024 | direct |
| Active / Premium-era | SUV | petrol | 1.2L turbo | 1.2 | 130 | automatic | FWD | 2018 | 2024 | direct |
| GT / GT Pack-era | SUV | petrol | 1.6L turbo | 1.6 | 180 | automatic | FWD | 2018 | 2024 | direct |
| PHEV | SUV | plug-in hybrid | 1.6L turbo plug-in hybrid | 1.6 | 225 | automatic | FWD | 2020 | 2024 | direct |
| PHEV 4x4 | SUV | plug-in hybrid | 1.6L turbo plug-in hybrid | 1.6 | 300 | automatic | AWD | 2020 | 2024 | direct |
| GT MHEV | SUV | mild_hybrid | 1.2L turbo mild-hybrid | 1.2 | 145 | 6-speed automatic / e-DCS6 | FWD | 2025 | null | direct |

**Source anchors to add**

- Peugeot Israel current 3008 / online model page: `https://online.peugeot.co.il/`
- Israeli 3008 launch/history sources already selected in prior validation package.
- Existing `Peugeot e-3008` source objects remain separate.

**Notes to add**

- `V4_LOCK: Peugeot 3008 non-electric profile was missing; e-3008 remains separate.`
- `V4_LOCK: current 3008 row is MHEV and uses year_end=null.`

## 3. Chery FX

**Profile keys**

```json
{
  "market": "IL",
  "make": "Chery",
  "model": "FX",
  "canonical_model": "FX",
  "year_start": 2022,
  "year_end": null,
  "profile_confidence": "high"
}
```

**Target technical variants**

| version_or_trim | body_type | fuel_type | engine | engine_displacement_l | horsepower_hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Comfort | Crossover | petrol | 1.6L turbo | 1.6 | 186 | 7-speed dual-clutch | FWD | 2022 | 2025 | direct |
| Luxury | Crossover | petrol | 1.6L turbo | 1.6 | 186 | 7-speed dual-clutch | FWD | 2022 | 2025 | direct |
| Noble | Crossover | petrol | 1.6L turbo | 1.6 | 147 | 7-speed dual-clutch | FWD | 2026 | null | direct |
| EV Noble | Crossover | electric | electric | null | 204 | single_speed | FWD | 2024 | null | direct |
| HEV Noble | Crossover | hybrid | 1.5L turbo hybrid | 1.5 | 246 | hybrid automatic | FWD | 2025 | null | direct |

**Source anchors to add**

- Chery Israel homepage/current lineup: `https://cheryisrael.co.il/`
- Chery FX EV page: `https://cheryisrael.co.il/models/fx-ev/`
- Chery FX / FX HEV pages selected in prior validation package.
- Israeli launch/spec sources for 2022 petrol FX selected in prior validation package.

**Notes to add**

- `V4_LOCK: Chery FX was missing and must be added as a full profile.`
- `V4_LOCK: petrol 186 hp and petrol 147 hp are separate periods and must not be collapsed.`
- `V4_LOCK: FX EV and FX HEV are current rows with year_end=null.`

## 4. Mazda CX-30

**Profile keys**

```json
{
  "market": "IL",
  "make": "Mazda",
  "model": "CX-30",
  "canonical_model": "CX-30",
  "year_start": 2020,
  "year_end": 2024,
  "profile_confidence": "high"
}
```

**Target technical variants**

| version_or_trim | body_type | fuel_type | engine | engine_displacement_l | horsepower_hp | transmission | drivetrain | year_start | year_end | support_level |
|---|---|---|---|---:|---:|---|---|---:|---:|---|
| Comfort | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Executive | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Executive | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2020 | 2024 | direct |
| Premium Plus | Crossover | petrol | 2.0L | 2.0 | 165 | 6-speed automatic | FWD | 2022 | 2024 | direct |
| Premium Plus | Crossover | petrol | 2.5L | 2.5 | 195 | 6-speed automatic | FWD | 2022 | 2024 | direct |

**Source anchors to add**

- Mazda Israel current models page: `https://www.mazda.co.il/models`
- Mazda Israel price list page: `https://www.mazda.co.il/car-list`
- Israeli Mazda CX-30 history/spec sources selected in prior validation package.

**Notes to add**

- `V4_LOCK: Mazda CX-30 was missing and must be added as a full historical profile.`
- `V4_LOCK: Mazda CX-30 is not opened as current; locked range is 2020-2024.`

---

# IMPLEMENTATION CHECKLIST

1. Load `model_technical_catalog_il.json`.
2. Apply the locked decision ledger exactly.
3. Add the four missing model profiles.
4. Keep every retained 2024 entry with an explanatory V4 note.
5. Recompute `available_values_for_website` for every changed or added profile.
6. Ensure every variant has `version_or_trim`.
7. Ensure all source references and field sources are valid.
8. Set `ready_for_website_upload=true` only after validation passes.

```bash
python -m json.tool model_technical_catalog_il.json > /tmp/catalog_check.json
python -m compileall scripts
python -m scripts.catalog_validation
python -m scripts.catalog_quality_scan
python -m pytest -q
git diff --check
```

# REQUIRED CODEX FINAL REPORT

```text
V4 locked ledger entries applied:
Profiles opened/currentized:
Profiles retained at 2024:
Duplicate profiles merged:
Exact historical year corrections:
Missing profiles added:
Remaining year_end=2024 count:
Remaining year_end=2024 entries with V4 retained note:
Remaining unjustified year_end=2024 entries:
ready_for_website_upload:
```
