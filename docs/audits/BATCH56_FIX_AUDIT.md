# BATCH56_FIX AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
**Natively unverified:** no full XSD, compile or in-game test. A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## Source checks
- **Package:** 263502 B, sha256 57c49ba9…4b42b4e match. All entries under `data/`. 103 XML parse; Mod 102 all + 3 ref.
- **vs 56:** only VeterancyTechStructureBuildable.xml changed; other 102 byte-identical, so the Mod, LogicCommand and LogicCommandSet checks carry over. 133 asset-namespace Cmds; lists 21/20/26/24/24; 3 commands → objects.
- **diff -w vs SDK VeterancyTechStructure.xml** (238 lines, SDK 217 + the two children), limited to:
  - both ART all includes removed;
  - id, EditorName, Side Allies, BuildTime 15, MAIN_STRUCTURE queue + placement;
  - literal 1500;
  - OCL rename ×2;
  - Soviet child: BuildTime 0 + ModuleTag_StructureUnpackUpdate 15s; Japan child inherits.
- **Restored / removed vs 56:**
  - All 8 ContactPoints are back verbatim, in the original order after the third Shape (no diff).
  - A single BaseTechStructure include.
  - EditorSorting removed.
  - KindOf +GRANTS_VETERANCY is back in its original position.
- **Verbatim:**
  - CaptureAndGiveUpgradeBehavior ALLIED_PLAYERS, 1/2/3 → VETERAN/ELITE/HEROIC;
  - Draw, the flag xi, engineer/repair xi, Lua, BuildingDestruction, FXList, death, collapse OCL body;
  - Body 3000/3000; 3 BOX shapes; audio; UI; ProjectedBuildabilityInfo.

## GlobalDefines removal — accepted (dependency closed)
- The only macro left in the file is `=$ACCOUNT_ORE`, now that the cost is a literal. It is defined in GlobalData/GlobalDefines.xml L69.
- The instance include `BaseTechStructure.xml` itself has `<Include type="all" source="DATA:GlobalData/GlobalDefines.xml"/>` (L5).
- This is the same chain the SDK original uses. All four SDK neutral originals (Hospital, Garage, Veterancy, ShipYard) have no direct GlobalDefines include, and they resolve `$ACCOUNT_ORE` and `$TECH_STRUCTURE_EFFECTIVE_COST` this way.
- Basis: shipped SDK precedent. This package's own build is still pending native verification. The other buildable files keep a direct include; both forms are harmless.

## To verify natively
- Self-built grant (L1608); if it fails, the GrantUpgradeCreate fallback.
- Stacking of built + captured academies; ART; Soviet unpack.

Paradrop is still pending as a whole; the oil derrick is undecided. Neither is part of this batch.
