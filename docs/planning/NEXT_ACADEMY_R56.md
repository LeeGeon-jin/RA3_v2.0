# Next: buildable Veteran (Elite) Academy — decided, not implemented
Refs: `academy_sdk_refs.tar.gz` (16 SDK files, read-only).

## Decision (latest, unambiguous)
"算啦算啦，精兵学院不调整了" means: **keep the effect, still make it buildable.** Quotes:
- devdoc L28 (11-06 revision): "效果完全沿用原版老兵训练营…只改为可建造，造价 1500、建造 15 秒…保留自建时是否生效的实测项"
- L224: "精英学院1500、15秒" (no prerequisite, same as the other tech buildings)
- L227: 1 / 2 / 3 academies → barracks, war factory, naval yard and airfield units are Veteran / Elite / Heroic. The map originals are unaffected; Japan places it directly (no core).
- L1608: whether it works when self-built is a batch-2 test; the fallback is GrantUpgradeCreate.
- **Not in the current package:** no Veterancy/Academy object in b89.

## SDK (`Neutral/Structures/VeterancyTechStructure.xml`, 217 lines)
- **Includes:** ART VeterancyGranterTechStructure.w3x and ABBarracks_particles.w3x (remove); BaseTechStructure once; YU_HotelDebris; VeterancyTechStructure_Collapse (→ _COL.w3x, BaseCollapsingObject). Loaded via NeutralMapSpecific L18 only → full copy.
- **Object:** KindOf +GRANTS_VETERANCY; cost `$TECH_STRUCTURE_EFFECTIVE_COST` → literal 1500; no own StructureUnpackUpdate (the Soviet child overrides parent `ModuleTag_StructureUnpackUpdate` 0.0s → 15s); Body 3000/3000; 3 BOX shapes; OCL `NUVeterancyTechStructure_Die_OCL` → rename to `…Buildable_Die_OCL`.
- **Effect:** `CaptureAndGiveUpgradeBehavior` UnificationType ALLIED_PLAYERS, mapping 1/2/3 → Upgrade_ProductionVeterancy_VETERAN/ELITE/HEROIC (PLAYER, DO_NOT_TRANSFER). The factories translate these through GiveUpgradeToProduced/UpgradeTranslate → Upgrade_CreationVeterancy_*.
  - The SDK factories carry this: Allied barracks/war factory/naval yard/airfield, Soviet ×4, Japan barracks/war factory/naval yard.
  - The package overrides only AlliedNavalYard and AlliedWarFactory, and both still have the 3 translates.
- **Keep verbatim, including the module id:** with the same ALLIED_PLAYERS unification, built and captured academies should count together. That is inferred, not proven → test.

## Minimal Batch 56
- New `data/Neutral/Structures/VeterancyTechStructureBuildable.xml`, garage/airport pattern:
  - Allied full copy: Side Allies, BuildTime 15, MAIN_STRUCTURE queue and placement, cost 1000→**1500**, OCL rename.
  - Soviet child: BuildTime 0 + Unpack 15s.
  - Japan child: inherits.
- No GrantUpgradeCreate now; that is the fallback only after the batch-2 test.
- 3 commands `Command_Construct{Allied,Soviet,Japan}VeterancyTechStructure`; append to the 5 lists → 21/20/26/24/24. Edit as text; no XML re-serialisation.
- Mod +1 include (102 all).

## Open / test
- Whether a self-built academy grants the upgrade (L1608).
- Captured + built count stacking; AI behaviour; ART resolution.
- Health is the original 3000, not a new decision.
