# Hospital buildable — minimal plan (research only)
Refs archive: `/workspace/ra3xfer/hospital_sdk_refs.tar.gz` (read-only SDK originals, 21 files, see list at end).

## Values (decided; no guesses)
Three objects Allies/Soviet/Japan; cost 1000; 15 s; no prerequisite; original MaxHealth 3000 (field untouched); no EnergyProduction (original has none); appears directly, no build animation/dust (memory 11-06, doc L1089); map HospitalTechStructure unchanged (new ids; L226). Flags: keep original parent KindOf incl. NOT_AUTOACQUIRABLE, IGNORE_FOR_VICTORY, NOT_SELLABLE, NEUTRAL_TECH — no rule asks to change tech-building flags (the -NOT_AUTOACQUIRABLE rule is landmark-only). Not a decoration conversion: keep PassiveAreaEffect heal, engineer capture, repair, flag draw.

## Inherit vs full copy — choose full copy
- SDK loads HospitalTechStructure only in the **MapSpecific** stream (`MapSpecific.xml` L17 → `Neutral/NeutralMapSpecific.xml` L15), not static/skirmish-global. The mod data is the static stream. SDK inherit precedent (`Allied/Units_Campaign/CAMP_AlliedBomberAircraft_Infantry_2.xml` instance-include + inheritFrom AlliedBomberAircraft) is same-stream; cross-stream inheritance from a map-specific object is unproven.
- All passed civilian buildables (Kremlin, statues, Liberty, Fuji, admin building) are full copies with ART all removed and collapse instance include kept → proven package pattern.
- Plan: file `data/Neutral/Structures/HospitalTechStructureBuildable.xml` (path free; Mod +1):
  1. `AlliedHospitalTechStructureBuildable`: full verbatim copy of the SDK GameObject (all Draws incl. TechBuildingFlagDraw xi, Behaviors, AI, Body, Geometry, audio, UI strings), includes = BaseTechStructure instance, YU_HotelDebris instance, HospitalTechStructure_Collapse instance, GlobalDefines all (ART all removed per rule); changes: id/EditorName, Side Allies, BuildTime 15, BuildPlacementTypeFlag MAIN_STRUCTURE (ProductionQueueType MAIN_STRUCTURE already), BuildCost literal 1000.
  2. `SovietHospitalTechStructureBuildable` inheritFrom the Allied copy (same file; Rushmore Allied/Soviet precedent): Side Soviet, BuildTime 0, `<StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="15s"/>` (merges with BaseTechStructure same id).
  3. `JapanHospitalTechStructureBuildable` inheritFrom the Allied copy: Side Japan, BuildTime 15.
  Needs root `xmlns:xai` for DisplayName Replace (source has inline xmlns:xai — keep verbatim).
- Commands: 3 × CONSTRUCTION_YARD_CONSTRUCT; append Allied CY Base 16→17, Allied Crane 15→16, Soviet CY 21→22, Soviet Crane 19→20, Japan CY 19→20.

## BaseTechStructure parent behaviour check (Soviet/others)
- ModelConditionUpgrade USER_1/2/3 by Upgrade_AlliesFaction/SovietFaction/JapanFaction: owner-faction look (same as captured hospital) — expected.
- StructureUnpackUpdate 0.0s in parent: Allied/Japan keep 0 (BuildTime counts); Soviet override 15s. No unpack animation exists on this model (PARSE_DEFAULT "no anim") → static model during 15 s, no dust (parent has no build FX). TEST visual/function during unpack.
- Death: SlowDeath (6s sink) + BuildingDestructionBehavior + collapse via hospital file; EVA BuildingStolen/EnemyBuildingCaptured/HospitalCaptured — original.
- Capture: GenericEngineerContain → enemy engineer can capture a built one (original). LUAEventList BuildingPowerFunctions: original Lua hook — TEST that it does not misbehave on a player-built copy.
- Do not add landmark FX/BuildingDestruction changes or StructureUnpack on Allied/Japan.

## Risks / open
- ART resolution of NUHospitalTechStructure.w3x / COL and flag w3x (AU/SU/JU_Garrison_Flag, NU_GarFlag via BaseTechStructure all-includes) in a static-stream mod object → native build log (same class as landmarks).
- Self-built NEUTRAL_TECH ownership/score, IGNORE_FOR_VICTORY means it won't count for defeat — original flag, TEST.
- No limit decided → unlimited; heal NonStackable so multiple don't stack.
- Health/flags/power: original by non-change; any change needs user.

## Archive contents (all exist in SDK)
XMLFiles/Neutral/Structures/HospitalTechStructure.xml; XMLFiles/Neutral/Props/HospitalTechStructure_Collapse.xml; XMLFiles/BaseObjects/BaseTechStructure.xml; XMLFiles/BaseObjects/BaseObject.xml; XMLFiles/BaseObjects/BaseCollapsingObject.xml; XMLFiles/Includes/TechBuildingFlagDraw.xml; XMLFiles/Includes/GenericEngineerContain.xml; XMLFiles/Includes/GenericBuildingRepair.xml; XMLFiles/Civilian/Yucatan_YU/Props/YU_HotelDebris.xml; XMLFiles/GlobalData/GlobalDefines.xml; XMLFiles/Neutral/NeutralMapSpecific.xml; XMLFiles/MapSpecific.xml; Schemas/xsd/AssetTypeGameObject.xsd; Schemas/xsd/Modules/{PassiveAreaEffectBehavior,StructureUnpackUpdate,EngineerContain,ModelConditionUpgrade,SlowDeath,BuildingDestructionBehavior,LUAEventList,PhysicsBehavior}.xsd. Package templates (not in archive): Soviet/Structures/SovietGreatKremlinPalace.xml, Civilian/Mount_Rushmore_MR/Buildings/MR_LaserMtRushmore_Lincoln_Ready.xml, GlobalData/LogicCommand(Set).xml from batch51.
