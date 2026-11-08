# BATCH82FIX2 + BATCH83 AUDIT — SOURCE PASS (source candidates)
Static check only: no compile, no in-game test, no PC. Not Phase 1 complete.

## 82FIX2 (real package from cloud handoff)
- `RA3_V2.0_Batch82FIX2_CrushingMechanics.tar.gz` → `batch82fix2.tar.gz`: 336162 B, sha256 8946eb9b…1555b.
- 135 XML, 133 all; no non-XML files; all paths under `data/`.
- `diff -rq` vs 82FIX: the only difference is that the 2 `.backup` files are removed. All 135 XML files are byte-identical to 82FIX (whose content was already PASS).
- **Crush batch: PASS** (source candidate; runtime unproven as in BATCH82FIX_AUDIT).

## 83 (real package)
- `RA3_V2.0_Batch83_EngineerInstantCapture.tar.gz` → `batch83.tar.gz`: 336419 B, sha256 f15fe50f…1e71.
- 136 XML, 134 all; no non-XML files.
- vs 82FIX2:
  - **new** `data/System/UnitAISettings.xml`: byte-identical to the SDK except L12 `CaptureWaitTime="3s"` → `"0s"`. Same 29 lines, same header and no BOM, as the SDK.
  - **Mod.xml:** `diff -w` = +1 line `<Include type="all" source="DATA:System/UnitAISettings.xml" />` right after the AudioSettings include. The rest is indentation-only changes (L6-7 and the UnitAbilityButtonTemplates line).
  - The other 134 XML files are byte-identical.
- **Status:** source candidate. It is a global-stream singleton (SDK global.xml L50) overridden through Mod.xml, the same pattern as B71 / B72. Whether it takes effect, whether the builder accepts the duplicate `Settings_UnitAI`, and whether 0s removes the whole delay are runtime-only; not claimed effective.
