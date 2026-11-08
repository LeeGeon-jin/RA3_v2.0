# Next: buildable Garage (Tech Garage, vehicle repair) — same reliable pattern as hospital
Refs: `/workspace/ra3xfer/garage_sdk_refs.tar.gz` (14 read-only SDK files).
## Rules (same as hospital, doc L224/L226/L30; 5.2 L380-384)
Three sides, 1000 / 15 s, no prereq; original health 3000, no power, no limit, flags kept; direct appear, no anim/dust; map GarageTechStructure untouched. 5.2 L381-384: original already global 2% (EffectRadius -1) → no effect change.
## SDK facts (`Neutral/Structures/GarageTechStructure.xml`, 272 lines)
- Includes: ART AutoPartsStoreTechStructure.w3x (remove per rule), instance BaseTechStructure, YU_HotelDebris, GarageTechStructure_Collapse (→ ART AutoPartsStoreTechStructure_COL.w3x, BaseCollapsingObject), ART ABBarracks_particles.w3x (remove).
- inheritFrom BaseTechStructure, `KindOf="+DONT_UNATTACH_WHEN_HEALING"` (keep), TechBuildingFlagDraw xi, PassiveAreaEffect -1 / 2% Include "VEHICLE HUGE_VEHICLE", GenericEngineerContain/Repair xi, LUAEventList BuildingPowerFunctions, MaxHealth 3000.0, VisionInfo 100/200, ProjectedBuildabilityInfo Radius 0.0, OCL `GarageTechStructure_Die_OCL`.
- Loaded only via Neutral/NeutralMapSpecific.xml L14 → full copy (not cross-stream inherit).
## Minimal batch 53
`data/Neutral/Structures/GarageTechStructureBuildable.xml`: Allied full copy (id AlliedGarageTechStructureBuildable, Side Allies, BuildTime 15, BuildPlacementTypeFlag MAIN_STRUCTURE — check ProductionQueueType present in source; if absent add MAIN_STRUCTURE like hospital source, cost literal 1000, +GlobalDefines, +xmlns:xai only if DisplayName Replace uses inline ns — keep verbatim); Soviet inherit + BuildTime 0 + same-id unpack 15s; Japan inherit. 3 commands; lists → Allied CY 18, Crane 17, Soviet CY 23, Crane 21, Japan CY 21; Mod +1 (99 all).
## Not now
- Dry dock (ShipYardTechStructure): 3 ART incl. _Anim/_Still (animated model) + ship heal → next, same pattern; verify water/land placement (BaseTechStructure CAN_BUILD_ON_WATER).
- Airport: heal part same pattern, but 5.2 #6 paradrop is a separate larger decided item → do airport with paradrop together later or heal-only first (needs user? doc says paradrop "建造后" depends on buildable airport — heal-only first is compatible).
- Academy (ambiguous "不调整了"), observation post (map reveal needs Lua), oil derrick: later.
## Same OCL duplicate-id risk as hospital (GarageTechStructure_Die_OCL).
