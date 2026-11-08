# BATCH86 AUDIT — PASS (static; no compile or in-game test)

## Package
- Package: batch86.tar.gz, copied from the cloud store RA3_V2.0_Batch86_BarracksRestore.tar.gz.
- 342960 B, sha256 d804910490ca937f7e753e3d593385bec124b848ffd2e9cd6a064775136711b2.
- 138 XML, no non-XML files.
- vs Batch85: only Allied/Structures/AlliedBarracks.xml differs. The other 137 XML are byte-identical.

## AlliedBarracks vs SDK (element-by-element: path, all attributes, text, order)
The only differences are:
1. **9 `ART:` includes removed** (GBDugOut, ABBarracks, _particles, _GAG, _DOOR, _UPGRADE, _BLD_SKN, _BLD_BLD, _LightsA). This is the package convention: ART is not included as type=all, the same as every other file.
2. **GameObject BuildTime 10 → 8.** All other GameObject attributes are equal.
3. **UpgradeTranslate added** as the 4th entry: Upgrade_SovietCloning → Upgrade_CloneMe. The original 3 veterancy translates are unchanged.

Element counts: SDK 138 = package 130 + 9 removed ART includes − 1 added translate.

## R1 restored, and more
- All 6 Draw modules are back: Draw, Door, UPGRADE, GAG, LIGHTS, particles, with every state and animation. The main draw has its BUILD_PLACEMENT_CURSOR and STRUCTURE_UNPACKING states.
- Death and destruction modules are back: BuildingDestruction, FXList, DieSound, CreateObjectDie (ABBarracks_Die_OCL), DestroyDie, LUAEventList (AlliedBarracksFunctions).
- **9 xi:includes are back.** Batch85 had **0** of them, so R1 was larger than I first reported:
  - GenericBuildingRepair, GenericEngineerContain;
  - GenericAlliedBuildingDestruction, GenericAlliedBuildingSuicide;
  - InfiltratorContainInfantry;
  - AlliedTechUpgradeReceiverLevel2/3;
  - AlliedSubObjectsUpgradeTech2/3.

## Dependencies
- ABBarracks_Die_OCL exists in SDK ObjectCreationLists.xml.
- AlliedBarracksFunctions is also used by the SDK naval yard and outpost.
- The include hrefs are SDK Includes files, and the xi namespace is declared.
- Every Batch85 element is still present in Batch86, so no approved change was lost.

## Runtime (unproven)
Compile and in-game checks still needed: barracks destruction/rubble, repair, engineer capture, spy, the Tech2/3 visuals, clone + veteran production.
