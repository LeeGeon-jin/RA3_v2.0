# BATCH52 AUDIT — SOURCE PASS (native-compile candidate)
Source check only; not full XSD, not compiled, not tested in game. Phase 1 not complete.

## Package
- 260701 B, sha256 `47ba0e135fbc0cc1ae234882db6c2e17b1c3605dcfb49eb295e6bdc40e65aee6` match; saved `batch52.tar.gz`; safe paths.
- vs 51 (real diff, not cloud totals): new 1 `Neutral/Structures/HospitalTechStructureBuildable.xml` (201 lines); changed 3 (Mod +1 include, LogicCommand +3, LogicCommandSet +5 Cmd); **other 95 files byte-identical** (diff -rq). 99 XML parse; Mod 98 all + 3 ref. The cloud's +523517→+500507 total change is not reflected in any retained file.

## Commands
3 × `CONSTRUCTION_YARD_CONSTRUCT`, Objects Allied/Soviet/JapanHospitalTechStructureBuildable. Appended at list ends: AlliedConstructionYardCommandSetBase 17, AlliedCraneCommandSet 16 (Allied cmd), SovietConstructionYardCommandSet 22, SovietCraneCommandSet 20 (Soviet cmd), JapanConstructionYardCommandSet 20 (Japan cmd). Old order intact.

## Diff vs SDK HospitalTechStructure.xml (diff -w), only:
- root +xmlns:xai; ART all removed (NUHospitalTechStructure.w3x, ABBarracks_particles.w3x, per rule); instance includes BaseTechStructure / YU_HotelDebris / HospitalTechStructure_Collapse kept; +GlobalDefines.
- Allied object: id/EditorName new; +Side Allies, BuildTime 15, BuildPlacementTypeFlag MAIN_STRUCTURE (ProductionQueueType MAIN_STRUCTURE original); BuildCost literal 1000 (macro unchanged globally).
- Everything else verbatim: DisplayName Replace, UI/portrait/button, ArmorSet AlliedBarracksArmor, Draw + TechBuildingFlagDraw xi, Physics, PassiveAreaEffect (-1, NonStackable, 2%, INFANTRY ALLIES, contained), GenericEngineerContain + GenericBuildingRepair xi, LUAEventList BuildingPowerFunctions, BuildingDestruction, AI AutoAcquire NO, MaxHealth 3000, Geometry, audio/EVA, ProjectedBuildabilityInfo, OCL NUHospitalTechStructure_Die_OCL.
- Soviet: inheritFrom Allied copy; Side Soviet; BuildTime 0; Behaviors only `StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="15s"` (= BaseTechStructure module id → merge/override). No animation/FX added.
- Japan: inheritFrom Allied copy; Side Japan; BuildTime 15 inherited; MAIN_STRUCTURE inherited (Japan CY accepts since B50).
- No GameDependency, EnergyProduction, MaxSimultaneousOfType, KindOf or Body change; parent flags (NOT_AUTOACQUIRABLE, IGNORE_FOR_VICTORY, NOT_SELLABLE, NEUTRAL_TECH) kept. Child objects without Body: legal (3245 SDK inherited GameObjects omit Body).
- Map HospitalTechStructure untouched (new ids).

## Risks / native tests (not claimed working)
- **Duplicate OCL id** `NUHospitalTechStructure_Die_OCL` now in static mod data and in the SDK map-specific stream; many skirmish maps contain hospitals → if duplicate ids across streams error, it surfaces here first. Same pattern as passed Kremlin/Liberty OCLs. Build log + map with a hospital. Fallback (only if it errors): rename OCL id and CreateObjectDie reference.
- Model/COL/flag ART resolution from static stream; Lua BuildingPowerFunctions on self-built copy; heal function; Soviet 15 s unpack on static model; ownership/engineer recapture; IGNORE_FOR_VICTORY.
