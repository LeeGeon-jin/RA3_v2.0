# BATCH72 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 294175 B, sha256 ad64707e…14984a98e match. All entries under `data/`. 118 XML parse.
- Mod: 116 all.
- vs 71:
  - new `GlobalData/UIConfigs.xml`;
  - new `UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml`;
  - Mod +1 at L13 `<Include type="all" source="DATA:GlobalData/UIConfigs.xml" />` — the wrapping asset, not the fragment (the fragment is not in Mod);
  - the other 115 files are byte-identical.

## Diffs vs SDK
- **UIConfigs.xml:** `cmp` identical, bytes/BOM/namespace (default asset ns + xi), 8 ART includes, UIConfigList `DynamicUIConfigList`.
- **UIComponentOptionsSettingsGeneral.xml:** only L15 `<DefaultAlternateMouse>false` → `true`. All other bytes identical (same root element/namespace, Priority 100, the other 7 elements).
- **Include count:**
  - 107 xi:include total, 70 unique DATA targets (all exist in SDK; one differs only in case);
  - the modified fragment is referenced **2×** (L106 MouseTactical INGAME, L142 MouseShell SHELL);
  - so there are 105 other references, not "106".

## Not runtime evidence
- Whether DATA: resolves to the package copy first, whether the same-id UIConfigList overrides the static one, and whether this field drives the "Alternate Mouse Setup" checkbox default are all unproven from XML.
- Public sources (NEXT_R72) only support Alternate = classic.
- Existing profiles keep their setting; Options.ini not touched.
