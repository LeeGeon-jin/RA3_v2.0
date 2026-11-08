# BATCH92FIX AUDIT — STATIC FAIL (same class of defect, moved to another file), 2026-11-08 22:55 UTC+10
## Package
- batch92fix.tar.gz = store handoff/RA3_V2.0_Batch92FIX_SovietSpy.tar.gz. 352452 B, sha256 5a28c528a1d4372193b16de0c6d140eea42f8e41b6b476187cdc3e40360cee75. Matches; the host asset is identical.
- Root is data/. 143 XML (includes 2 fragment files). Mod.xml: 139 all + 3 reference.
- vs 92: only ExperienceLevels_SovietSpy.xml and Mod.xml changed, plus the new UIInGame/UIComponentObjectSelector.xml.
- vs 91: 4 new + 4 changed. The other 135 files are byte-identical.

## BLOCKING
1. **Mod.xml L145 `<Include type="all" source="DATA:UIInGame/UIComponentObjectSelector.xml" />` is the same error as in 92.**
   - The file root is `<UIComponentObjectSelector>`, a fragment, not an AssetDeclaration.
   - In the SDK it is only consumed by `xi:include` in GlobalData/UIConfigs.xml L34. All 774 SDK `<Include>` targets are AssetDeclaration roots.
   - The package already has GlobalData/UIConfigs.xml (Mod.xml L15 type all), which xi:includes `DATA:UIInGame/UIComponentObjectSelector.xml` at L34. So the consumer already exists and the Mod.xml line is wrong and unnecessary.
   - **Fix: delete Mod.xml L145 only.** Mod.xml then has 138 all + 3 reference.

## Fixed / verified
- The IF_SecondaryObjectListener type all line was removed. ✔
- **Fragment reachability (static):**
  - IF_SecondaryObjectListener.xml is xi:included by package AlliedAntiAirVehicleTech1 L726 and AlliedBaseDefense L573.
  - UIComponentObjectSelector.xml is xi:included by package UIConfigs L34.
  - Both use `DATA:` hrefs whose target path exists in the package, so they are reachable. Whether the package copy wins over the SDK copy is not statically proven.
  - BinaryAssetBuilder.exe.config has defaultDataPaths=".;.\Mods;.\SAGEXML". The search order for the mod data dir is not statically provable.
  - There is a precedent of the same shadowing mechanism in the package: B72 UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml, via UIConfigs, without a Mod.xml line. Also unproven.
  - → Acceptable static candidate, **pending compile**. Not functionally proven.
- **UIComponentObjectSelector.xml:** a full SDK copy + `<IncludeThing>SovietInfiltrationInfantry</IncludeThing>` in the spy shortcut group (with Japan and Allied spies). Only other difference: a trailing blank line.
- **ExperienceLevels_SovietSpy.xml:**
  - Now has `<Includes><Include type="instance" source="DATA:GlobalData/ExperienceLevels.xml"/></Includes>`.
  - Parents ExperienceLevel_SovietRank1–4 exist there (L93–L102).
  - SDK ExperienceLevels.xml has its own includes (only 3 ART decal files: decal_G_level1 / decal_GDI_S_CO / decal_Good_CO), none of which points back to the new file, so there is no cycle.
  - The 4 templates are unchanged and correct.
- **Unchanged since 92 and already verified:**
  - Spy object diff: only id, Side, names, prerequisite, clone ThingToSpawn.
  - Cloning chain unfiltered.
  - Bribe exclusion; IFV golden-gun IncludeThing.
  - LC / LCS single definitions.
- Earlier batches kept: cloning center limit 1, normal mirage 80, 89–91 bytes unchanged. Advanced mirage not created.

## Runtime / compile unproven
Fragment shadow precedence, instance include of a Static-stream file from the mod stream, and all spy behaviours (production, disguise, bribe, cloning, ranks, IFV gun, hotkey).

**Verdict: static FAIL on #1. After deleting that one line, expected static PASS (candidate). Functional equivalence is not final.**
