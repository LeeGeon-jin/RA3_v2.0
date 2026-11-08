# Next: Tech Airport — repair now, paradrop later (research only)
Refs: `/workspace/ra3xfer/airport_sdk_refs.tar.gz` (14 read-only SDK files for the repair building).

## Requirement mapping (doc)
| Part | Doc | Status |
|---|---|---|
| Buildable airport, 3 sides, 1000/15, no prereq, no anim/dust | L224/L226/L30 | decided → Batch 55 |
| Repair 2%/s map-wide own aircraft | 5.2 #5 L392-396 "原版即…" | original, keep |
| Paradrop power | 5.2 #6 L398-402 | decided values, **one open point** |
| ↳ 9 min reload (540 s), click target like SW | L398 user | decided |
| ↳ Badger bomber (SovietSupportBomber model), map edge default | L398/L401 | decided (map edge = doc default; user offered either) |
| ↳ payload: Allies 3 peacekeeper + 2 javelin; Soviet 3 conscript + 2 flak; Japan 3 imperial warrior + 2 tank buster | L398 | decided |
| ↳ after capture OR build | L398 | decided (needs original + buildable ids as prerequisites) |
| ↳ button placement: protocol bar (A) vs airport's own bar (B) | L401 ①, **L1601 "第二批实测后定"** | **open — needs test, then user** |
| ↳ non-stacking, shot-down infantry die, AI won't use | L401 ③④⑥ | test items |
Paradrop therefore is a separate, larger batch, not part of 55, and must not be marked complete when the repair building is done.

## SDK facts (`Neutral/Structures/AirportTechStructure.xml`, 207 lines)
- Includes: ART NUAirportTechStructure.w3x, ABBarracks_particles.w3x (remove per rule); instance BaseTechStructure **listed twice** (keep verbatim or dedupe — harmless either way; recommend verbatim), YU_HotelDebris, AirportTechStructure_Collapse (→ NUAirportTechStructure_COL.w3x, BaseCollapsingObject). Loaded only via NeutralMapSpecific.xml L12 → full copy.
- KindOf +DONT_UNATTACH_WHEN_HEALING; StructureArmor; no ProductionQueueType (add MAIN_STRUCTURE, garage/dry-dock precedent); Draw default + RUBBLE, "no anim"; flag xi; DestroyDie; PassiveAreaEffect -1 NonStackable 2% `AIRCRAFT VEHICLE HUGE_VEHICLE` ALLIES `AIRBORNE_TARGET`; engineer/repair xi; LUAEventList; Body ModuleTag_Body 3000/3000; **4 BOX shapes, ~343 × 229 footprint** (largest tech building → placement test); vision 100; ProjectedBuildabilityInfo; OCL `NUAirportTechStructure_Die_OCL` → rename `NUAirportTechStructureBuildable_Die_OCL`.
- No own StructureUnpackUpdate → Soviet child adds `ModuleTag_StructureUnpackUpdate` 15s (parent id) as hospital.

## Minimal Batch 55 (repair building only)
`data/Neutral/Structures/AirportTechStructureBuildable.xml`: Allied full copy + Soviet/Japan inherit (dry-dock pattern); 3 commands; lists → Allied CY 20, Crane 19, Soviet CY 25, Crane 23, Japan CY 23; Mod +1 (101 all).

## Paradrop later — SDK paths (exist; not in archive, CampaignOverrides is large)
Includes/CampaignOverrides/CampaignOverrides.xml (OCL_ParaDropLvl1 L88, SpecialPowerParadropLvl1 L142); System/PlayerSpellBook.xml (OCLSpecialPower, CREATE_AT_EDGE_NEAR_SOURCE); Allied/Units_Campaign/CAMP_AlliedBomberAircraft_Infantry_2.xml; Allied/Units_Campaign/CAMP_PowerStore_AlliedBomberDrop.xml; Soviet/Units/SovietSupportBomber.xml; infantry: Allied/Units/AlliedAntiInfantryInfantry.xml, AlliedAntiVehicleInfantry.xml, Soviet/Units/SovietAntiInfantryInfantry.xml, SovietAntiVehicleInfantry.xml, Japan/Units/JapanAntiInfantryInfantry.xml, JapanAntiVehicleInfantry.xml.

## Oil derrick — not recommended now
5.2 #1 only confirms original income (L368-372 "无需改动"); whether it is in the buildable set is not explicit (L224 names "加成建筑，如精英学院、医院"), and a built derrick would interact with InitialCaptureBonus 500. Treat as ambiguous → ask before doing.
