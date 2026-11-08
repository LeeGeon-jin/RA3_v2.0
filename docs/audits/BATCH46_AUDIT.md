# BATCH46 AUDIT — SOURCE PASS (replaces batch45_FIX as candidate)
Box-only, field-level; not full XSD, not compiled, not tested in game. Phase 1 not complete.

## Package
- `ra3v2_phase1_batch46.tar.gz` 247120 B, sha256 `21d4a4acb0877b91386114d1003d017de62eadfdf33808f977e2e5cd7885039f`; safe paths; saved as `batch46.tar.gz`.
- vs 45_FIX: new 1 (`Soviet/Structures/SovietGreatKremlinPalace.xml`), changed 3, other 88 identical. 92 XML parse; Mod 91 all + 3 ref; new id unique.
- `Command_ConstructSovietGreatKremlinPalace` = `CONSTRUCTION_YARD_CONSTRUCT` + `<Object>SovietGreatKremlinPalaceBuildable</Object>`; SovietConstructionYardCommandSet 20→21, SovietCraneCommandSet 18→19, pure append, old order kept.

## Node diff vs SDK `Civilian/Kremlin_KR/Buildings/KR_GreatKremlinPalace.xml`
Only:
- Root: xmlns:xi dropped (no xi: left in file), xmlns:xai added. Includes: ART all + commented _GAR removed; parent include → `BaseCivilianStructureNoGarrisonDestructible`; YU_HotelDebris + `KR_GreatKremlinPalace_Collapse` instance kept; GlobalDefines added.
- id/EditorName `SovietGreatKremlinPalaceBuildable`; inheritFrom NoGarrisonDestructible; KindOf `-NOT_AUTOACQUIRABLE +AUTO_ACQUIRABLE_BY_AI`; Side Soviet, BuildTime 0, EnergyProduction 0, MaxSimultaneousOfType 1, OTHER_STRUCTURE ×2; BuildCost 2000; no GameDependency.
- ArmorSet DefaultArmor StructureArmor/GenericStructureDamageFX (overrides parent's same-id set with identical values) + CryoBeamFrozenArmor SECONDARY_DAMAGE (verbatim from BaseCivilianStructure); legal order.
- `GarrisonFlagArmorXLargeDraw` xi:include removed.
- Added `DestroyDie id=ModuleTag_DestroyDie DeathTypes ALL` (verbatim from BaseCivilianStructure) and `StructureUnpackUpdate id=ModuleTag_StructureUnpack 20s`.
- Body `ActiveBody DefaultBody =$CIV_HEALTH_XLARGE` (5000, original from XLarge; single slot).
Verbatim: ScriptedModelDraw `KR_GreatKremlinPalace_A` (+RUBBLE, bones), Physics, BuildingDestruction, FXList Replace `FX_Civ_Explosion_XLarge`, CreateObjectDie → `KR_GreatKremlinPalace_Die_OCL`, Geometry 131.481/36.8328/112.28 offset 0.351135/3.37231/0, audio, OCL.

## Effective inheritance check (merge/Remove)
- Original: XLarge **Removes** `DefaultSquishCollide`, `ModuleTag_Physics`, `id_CrusherInfo` inherited from BaseCivilianStructure; the object then re-adds `ModuleTag_Physics` locally → effective: Physics yes, SquishCollide no, CrusherInfo no.
- New chain (BaseObject / NoGarrison / Destructible) defines none of SquishCollide, CrusherInfo, Physics (grep empty) → effective: Physics (local) yes, SquishCollide no, CrusherInfo no. **Identical.**
- Removed by design (doc L812 garrison rule): ContestableGarrisonContain, garrison aura, stealth-garrison InvisibilityBehavior, KindOf GARRISON/IGNORE_FOR_VICTORY/NOT_SELLABLE (counts for defeat — test item, same as Fuji).
- Death kept (Soviet landmark text does not order removal): CreateObjectDie + restored DestroyDie.

## Risks / pending
- Collapse + `_A`/`_A_COL` W3X resolution via SDK DATA instance include: same mechanism as earlier passed files; confirm in native build log.
- Footprint ~263×74 placement; collapse debris cost (doc).
- UI: SDK object has no DisplayName/portrait/button → UI keys pending; nothing invented; display unverified.
- J08 original untouched (not in mod).

## Guard01 (user confirmed health 2000) — plan for next batch (not implemented)
Source `Civilian/Tokyo_Harbor_TH/Buildings/TH_StatueGuard01.xml` (parent BaseSimulatedProp, PropBody no value).
- Independent copy, inheritFrom `BaseCivilianStructureNoGarrisonDestructible`; KindOf `-NOT_AUTOACQUIRABLE` (do not copy crushable macro).
- Draw: DynamicsDraw → ScriptedModelDraw id ModuleTag_Draw, PARSE_DEFAULT Model `TH_StatueGuard01` (no invented RUBBLE/bones).
- Remove ToppleUpdate (prop parent's EnableDynamicsCollide/CrusherInfo/SlowDeath(TOPPLED) vanish with re-parent). Keep original SlowDeath ALL 1.5s/4/8s (only death module; Japan rule removes CreateObjectDie/DestroyDie, not present here) and FXList onDeath `FX_RockCrush_AudioOnly` with `xai:joinAction="Replace"` id ModuleTag_FXList.
- ArmorSet keep original `NoArmor` explicitly. Body `ActiveBody DefaultBody MaxHealth="2000"` (user value; literal, not a macro — `CIV_HEALTH_SMALL`=2000 also acceptable, state which).
- Geometry verbatim 8.70357/9.7518/49.2804 offset 4.42938/3.6086/0.251526. No BuildingDestruction, no xi, no UI keys.
- Side Japan, BuildTime 10, EnergyProduction 0, Max 1, OTHER_STRUCTURE ×2, BuildCost 1000; command CONSTRUCTION_YARD_CONSTRUCT; JapanConstructionYardCommandSet append 18→19; Mod +1.
- Risks: small footprint; NoArmor makes it fragile; SlowDeath sink untested; model may lack structure bones (visual).
- Attach: `Civilian/Tokyo_Harbor_TH/Buildings/TH_StatueGuard01.xml`, `BaseObjects/BaseSimulatedProp.xml`, `BaseObjects/BaseCivilianStructureNoGarrisonDestructible.xml`, `BaseObjects/BaseCivilianStructureNoGarrison.xml`, `BaseObjects/BaseObject.xml`, `GlobalData/GlobalDefines.xml`, package `Japan/Structures/JapanStatueGuard03.xml` (template).
- Guard02 health still undecided — not to be implemented.
