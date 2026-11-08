# BATCH75 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Phase 1 not complete. SDK precedent is not runtime evidence.

## Package
- 299787 B, sha256 eac7dec0…c1ff6be4a4 match. All entries under `data/`. 121 XML parse.
- Mod: 3 reference / 119 all.
- vs 74FIX (119 files):
  - 2 new files;
  - Mod.xml changed (+2 includes at L27-28);
  - the other **118** old files are byte-identical. The cloud's "119 old unchanged" miscounts, because Mod changed.

## SovietBaseDefenseGround.xml (SDK 605 → 607 lines)
- **diff = exactly 2 hunks:**
  - L52 Define `SOVIET_BASE_DEFENSE_GROUND_LOCAL_UNPACK_TIME` 20s→10s;
  - +2 lines L543-544 `<xi:include href="DATA:Includes/GenericSovietBuildingDestruction.xml" />`, between GenericBuildingRepair and GenericSovietBuildingSuicide (Barracks order).
  - The `xmlns:xi` declaration is present.
- **Define use:** only StructureUnpackUpdate L540 (BuildTime 0.0 kept).
- **Module ids:** the included `ModuleTag_CreateOccupiedDie` does not collide with the file's `ModuleTag_CreateObjectDie` (L526) or the Suicide include's `ModuleTag_CreateOccupiedSuicide`. The parent BaseSovietStructure has no CreateOccupiedDie.
- **Spawn conditions** (SDK Includes/GenericSovietBuildingDestruction.xml → OCL_GenericSovietBuildingDestruction, ObjectCreationLists L1219-1227):
  - 1 × SovietAntiInfantryInfantry, MinHealth 0.3 / MaxHealth 0.75;
  - Options `IGNORE_ALL_OBJECTS REQUIRES_LIVE_PLAYER DO_NOT_COPY_SHADERS`, Disposition ON_GROUND_ALIGNED;
  - DieMux `DeathTypes="ALL"`, `DeathTypesForbidden="DETONATED SUICIDED SHATTERED"`, `ExemptStatus="OVER_WATER UNPACKING SOLD"`;
  - `UpgradeForbidden Upgrade_NoSpawnUponDestruction`.
  - **Owner:** the conscript's owner is assumed to be the dying object's player (OCL convention, REQUIRES_LIVE_PLAYER). Not explicit in XML → native test.
- **Kept:**
  - the original collapse CreateObjectDie (SBDefenseGround_Die_OCL), DestroyDie, FX;
  - the original **Suicide include** (OCL_GenericSovietBuildingSuicide, DeathTypes SUICIDED, Exempt OVER_WATER UNPACKING), i.e. the original sell/suicide crew behaviour is unchanged;
  - the destruction include is exempt from SOLD/SUICIDED, so the two do not double up — native check.
- Weapons / AI / armor / health unchanged.

## SovietBaseDefenseAir.xml (492 = 492 lines)
- **diff = only** L38 Define `SOVIET_BASE_DEFENSE_AIR_LOCAL_UNPACK_TIME` 20s→10s, used only at L423 StructureUnpackUpdate.
- Weapons (including the Batch62 flak ground-attack change, which lives in Weapon.xml, unchanged) and all other attributes identical to the SDK.

## Native test
- 10 s unpack for both.
- One conscript on destruction; none when sold beyond the original crew; none while unpacking or over water.
