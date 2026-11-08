# BATCH85 AUDIT — SOURCE PASS (source candidate; effect unproven)
Static check only: no compile, no in-game test, no PC. 第一批 still needs a full native compile and game test; not complete.

## Package (real)
- `batch85.tar.gz` (host asset) **341281 B, sha256 c89b0068b3b2ba69e1d2865bc34e9a3659d8c4df8e31ffb5f6cd51f72e343f4d**. The SHA matches the cloud's; the cloud's size "342016" is wrong.
- All entries under `data/`; no non-XML / backup / fragment files.
- 138 XML. Mod.xml: 135 `type="all"` + 3 `type="reference"` (static / global / audio, unchanged).
- vs B84:
  - new `data/System/GameLOD.xml`, new `data/System/GraphicsHardware.xml`;
  - Mod.xml `diff -w` = +1 line `<Include type="all" source="DATA:System/GameLOD.xml" />` after the UnitAISettings include;
  - the other **135** XML files are byte-identical (cloud's "136" is wrong).
- No global.xml copy and no MapMetaData; GraphicsHardware is not separately Mod-included.

## Element-by-element vs SDK
Method: ElementTree, recursive tag / attribute / text / child-order compare. Comments are not compared; line counts are identical (289/289, 344/344).

| File | Changes | Everything else |
|---|---|---|
| GameLOD.xml | 4× `GameLODPreset SystemMemory` → `999999` (Low / Medium / High 500, UltraHigh 1000) | identical: Processor MinMHz, Xres / YRes, all StaticGameLOD (VeryLow … Custom), DynamicGameLOD, both Includes |
| GraphicsHardware.xml | **293** of **340** `<Device>` Level → `VERY_LOW` (HIGH 38, LOW 162, MEDIUM 63, ULTRA_HIGH 30); the 47 already VERY_LOW are unchanged | identical: VendorId / DeviceId / Name; all 31 `MacLevel` attributes unchanged |

(The cloud's 340 / 371 figures: 340 is the correct device count. My earlier "47/170/77/47/30" counts in R83 / the research note included MacLevel values; corrected here.)

## Schema
- GameLOD.xsd: `SystemMemory` is SageInt (default 500), so 999999 is valid.
- `Device Level` is GameLODType (required); VERY_LOW is a valid enum. MacLevel is optional and untouched.

## Include chain
- GameLOD.xml L6 `<Include type="all" source="GraphicsHardware.xml"/>` is relative, so it resolves to the package's `data/System/GraphicsHardware.xml` [static inference about path resolution].
- L10 `instance DATA:Includes/PlatformSpecificAudioDefines.xml` is not in the package, so it resolves to the SDK (same as B71).
- **No duplicate assets:** GraphicsHardware enters only through GameLOD; the ids `GraphicsHardware` and the presets are each defined once in the package.
- The mod also references `DATA:global.xml`, which contains the SDK GameLOD. This is the same override-by-`all` pattern as B71 / B72 / B83. Static conflict handling by the builder is unproven.

## Scope vs user agreement
- The four presets are unreachable and every GPU is VERY_LOW, so first-run auto-detect should pick VeryLow. That only affects **new profiles** (doc L39 / L197).
- Existing Options.ini values and manual raising are untouched: no Static / Dynamic preset values changed ("不封顶" kept).
- **Unproven (runtime):**
  - whether the global-stream override is used;
  - whether detection runs after `-modconfig` data loads;
  - whether detection reads GraphicsHardware and / or the presets (doc: "两者如何合并未见资料").
- Not claimed effective.

## Verdict
PASS as a source candidate. The user's existing profile can only change via the Options.ini route (PHASE1_LOWEST_QUALITY_RESEARCH §4, PC needed, not executed).
