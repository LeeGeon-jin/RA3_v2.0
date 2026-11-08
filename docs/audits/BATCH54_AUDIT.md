# BATCH54 AUDIT — SOURCE PASS (native-compile candidate)
Source check only. **No full XSD, no compile, no in-game test.** A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## Package
- 255654 B, sha256 `9b97ad088ffdee1a65dcb7dfaf1a6d2fee4de7b6f7dbb2155841ae2d9cb80cee` match; saved `batch54.tar.gz`; all entries under `data/`, safe paths.
- vs 53_FIX: new 1 `Neutral/Structures/ShipYardTechStructureBuildable.xml` (207 lines); changed 3 (Mod +1, LogicCommand +3, LogicCommandSet +5); other 97 byte-identical. 101 XML parse; Mod 100 all + 3 ref.
- Commands: 3 × CONSTRUCTION_YARD_CONSTRUCT → Allied/Soviet/JapanShipYardTechStructureBuildable; appended at list ends, old order kept: Allied CY 19, Allied Crane 18, Soviet CY 24, Soviet Crane 22, Japan CY 22.

## diff -w vs SDK ShipYardTechStructure.xml — only:
- root +xmlns:xai; ART all removed (ShipHangarTechStructure.w3x, _Anim.w3x, _Still.w3x, ABBarracks_particles.w3x); instance BaseTechStructure / YU_HotelDebris / ShipYardTechStructure_Collapse kept; +GlobalDefines.
- Allied: id/EditorName; +Side Allies, BuildTime 15, ProductionQueueType MAIN_STRUCTURE, BuildPlacementTypeFlag MAIN_STRUCTURE (attributes); cost literal 1000.
- OCL id + CreateObjectDie CreationList → `NUShipYardTechStructureBuildable_Die_OCL`; OCL body (creates ShipHangarTechStructure_Collapse) verbatim.
- Soviet: inherit, Side Soviet, BuildTime 0, `ModuleTag_StructureUnpackUpdate` 15s (same id as the dry dock's own local 0.0s module and the parent's → override). Japan: inherit, Side Japan (BuildTime 15, MAIN inherited).
- Verbatim: KindOf +DONT_UNATTACH_WHEN_HEALING (parent CAN_BUILD_ON_WATER/DEEP_WATER kept), StructureArmor, UI/portrait/HealthBox 45, DisplayName Replace, Draw with all ExtraPublicBone (flag/contact 01-20/garrison 01-12), RUBBLE state, **idle Still ONCE + USER_1 Anim LOOP (owner-state, not build)**, flag draw xi, PassiveAreaEffect -1 NonStackable 2% SHIP VEHICLE HUGE_VEHICLE ALLIES WATER_LOCOMOTOR_ACTIVE, engineer/repair xi, LUAEventList, BuildingDestruction, FXList Replace, DestroyDie, Body MaxHealth+InitialHealth 3000, 2 BOX shapes, vision, ProjectedBuildabilityInfo Radius 0.
- No GameDependency/power/limit/flag/animation/dust additions. CY ranges untouched (no CY file changed). Map ShipYardTechStructure untouched.

## Native tests
ART/animation resolution (idle anims may fail to load; impact not guaranteed cosmetic), water placement within CY rings, amphibious-in-water heal, Soviet 15 s, Lua hook, engineer recapture.
