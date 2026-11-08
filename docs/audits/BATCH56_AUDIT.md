# BATCH56 AUDIT — FAIL (VeterancyTechStructureBuildable.xml only)
Source check only. No full XSD, compile or in-game test. A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## OK
- **Package:** 263414 B, sha256 eeebfdc9…81a265c match. All entries under `data/`. 103 XML parse; Mod 102 all + 3 ref.
- **vs 55_FIX:** new file + 3 changed; other 99 byte-identical.
- **Mod.xml:** +1 include.
- **LogicCommand:** +3 CONSTRUCTION_YARD_CONSTRUCT → Allied/Soviet/JapanVeterancyTechStructureBuildable.
- **LogicCommandSet vs 55_FIX:** exactly +5 text lines, appended. 133 `{uri:ea.com:eala:asset}Cmd`, 0 bare. Lists 21/20/26/24/24, old order kept.
- **Allied object:** id; Side Allies; BuildTime 15; MAIN_STRUCTURE queue + placement; literal 1500.
- **Includes:** both ART all includes removed; GlobalDefines added.
- **OCL:** renamed in both places; body unchanged.
- **Kept:** CaptureAndGiveUpgradeBehavior ALLIED_PLAYERS 1/2/3; Draw; flag/engineer/repair xi; Lua; death; Body 3000; 3 boxes; audio; ProjectedBuildabilityInfo.
- **Children:** Soviet BuildTime 0 + ModuleTag_StructureUnpackUpdate 15s; Japan inherits.
- **Unchanged:** factories and the map academy. No build animation or dust.
- The KindOf attribute was moved; attribute order doesn't matter.

## Blockers — invented simplification and additions (188 vs SDK 217 lines)
1. **All 8 `<ContactPoint>` entries in Geometry (SDK L141-188) were deleted.** These set the points units use to approach and attack the building, so this is a behaviour loss, not cosmetic. Restore them verbatim, all 8, in the original order after the third Shape.
2. **A second `BaseTechStructure` include was invented.** The academy SDK file has it once; only the airport had a duplicate. Keep one.
3. **`EditorSorting="STRUCTURE"` was added.** It's not in the academy SDK; it was copied from the airport. Remove it (unrequested).

**Minimal fix:** in this one file only, apply 1–3. Expected `diff -w` vs SDK then = includes (ART removed, +GlobalDefines), id/Side/BuildTime/queue/placement/EditorName, 1500, OCL rename ×2, the two children; nothing else. No other file changes.

## To verify natively (after fix)
- Self-built grant (L1608): if it doesn't work, use the GrantUpgradeCreate fallback.
- Stacking of built + captured academies; ART; Soviet unpack.
