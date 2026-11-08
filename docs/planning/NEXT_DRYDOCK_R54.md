# Next: buildable Dry Dock (ShipYardTechStructure) — research, not implemented
Refs: `/workspace/ra3xfer/drydock_sdk_refs.tar.gz` (16 read-only SDK files).
## Rules (doc L224/L226/L30; 5.2 #4 L386-390)
All three sides; 1000 / 15 s; no prereq; appears directly, no build animation/dust; new ids, map ShipYardTechStructure untouched. 5.2 L387-390: original already global 2% ship repair → no effect change. Health/power/flags/limit: no rule → original fields untouched (MaxHealth 3000 + InitialHealth 3000; no EnergyProduction; no limit).
## SDK facts (`Neutral/Structures/ShipYardTechStructure.xml`, 193 lines)
- Includes: ART ShipHangarTechStructure.w3x, _Anim.w3x, _Still.w3x, ABBarracks_particles.w3x (ART all → removed per package rule); instance BaseTechStructure, YU_HotelDebris, ShipYardTechStructure_Collapse (→ ART ShiphangarTechStructure_COL.w3x, BaseCollapsingObject). Loaded only via Neutral/NeutralMapSpecific.xml L17 → full copy (hospital/garage pattern).
- KindOf `+DONT_UNATTACH_WHEN_HEALING`; ArmorSet StructureArmor; no ProductionQueueType (add MAIN_STRUCTURE as garage).
- **Animations are idle/owner-state, not build animations — keep verbatim:** PARSE_DEFAULT `ShipHangarTechStructure_Still` ONCE; `USER_1` → `ShipHangarTechStructure_Anim` LOOP. USER_1 comes from BaseTechStructure `ModelConditionUpgrade ModuleTag_AlliesFaction` (Upgrade_AlliesFaction, upgrade.xml L78) → loop plays when an Allied player owns it. Nothing to delete for the no-build-animation rule (there is no build-up state).
- Draw: ExtraPublicBone flag/contact/garrison bones; RUBBLE state; TechBuildingFlagDraw xi.
- PassiveAreaEffect -1, NonStackable, 2%, `SHIP VEHICLE HUGE_VEHICLE` ALLIES with `StatusBitFlags="WATER_LOCOMOTOR_ACTIVE"` (amphibious only while in water).
- **Own local `StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="0.0s"`** (same id as parent) → Soviet child override 15s merges the same id.
- Engineer/repair xi, LUAEventList BuildingPowerFunctions, BuildingDestruction (SovietRefineryHit, AlliedBarracks_Debris), FXList Replace, CreateObjectDie `ShipHangarTechStructure_Die_OCL` + DestroyDie, Body `ModuleTag_Body` (single slot → fine), 2 BOX shapes ~90×191, VisionInfo 100, ProjectedBuildabilityInfo Radius 0.
## Placement / water
- Water flags are not dry-dock-specific: BaseTechStructure KindOf has `CAN_BUILD_ON_WATER CAN_BUILD_ON_DEEP_WATER` for every tech building (hospital/garage already inherit it). Keep.
- Construction-yard rings: Soviet + (since B50) Japan 600/585 outer ring has AllowedObjectFilter Rule NONE + only Allied/Soviet/JapanNavalYard → **does not apply** to the dry dock; it uses the normal 480/465 MAIN_STRUCTURE ring (Allied CY uses its own). No change needed. Whether water tiles inside the 480 ring accept it = TEST.
## Minimal batch 54 (garage pattern)
`data/Neutral/Structures/ShipYardTechStructureBuildable.xml`: Allied full copy (id AlliedShipYardTechStructureBuildable, Side Allies, BuildTime 15, ProductionQueueType + BuildPlacementTypeFlag MAIN_STRUCTURE, cost literal 1000, +GlobalDefines, +root xmlns:xai, ART all removed, instance includes kept), OCL renamed `NUShipYardTechStructureBuildable_Die_OCL` (id + CreationList; body still creates ShipHangarTechStructure_Collapse); Soviet inherit (BuildTime 0, same-id unpack 15s); Japan inherit. 3 CONSTRUCTION_YARD_CONSTRUCT commands; lists → Allied CY 19, Crane 18, Soviet CY 24, Crane 22, Japan CY 22; Mod +1 (100 all).
## Risks / tests
- **Animation ART:** removing `_Anim`/`_Still` ART includes follows the rule but the idle animations may then not resolve → build log; if missing, the model just doesn't animate (cosmetic). Flag clearly.
- Water placement, amphibious heal, Soviet 15 s on animated model (Soviet owner → USER_2, so Still only), Lua hook, ART resolution, engineer recapture.
## Airport alternative
Heal-only airport is the same pattern and simpler (single ART model). Paradrop (5.2 #6) stays separate — not included.
