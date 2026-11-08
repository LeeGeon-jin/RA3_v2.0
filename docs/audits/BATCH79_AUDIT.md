# BATCH79 AUDIT — FAIL (partial delivery 16/19 + static defects). Not approvable as the full requirement.
No full XSD / compile / in-game test. Not Phase1 complete.

## Package
- 309682 B, sha256 d26c45a6…9d60bc045 match. data/ root, cumulative. 129 XML parse. Mod: 3 reference / 127 all (+5 vs 78FIX2).
- vs 78FIX2: 5 new files (SovietCloningCenter, JapanBarracks, Civilian/Geneva.xml, Geneva_GE bunker + collapse) and 23 modified (Allied / Soviet Barracks, 16 infantry, upgrade.xml, LogicCommand, LogicCommandSet, Mod). All other files byte-identical.
- 78FIX2 quick production / earlier changes are untouched.

## Correct parts
- **upgrade.xml (already a full copy, already in Mod L12):** +Upgrade_SovietCloning (PLAYER, DO_NOT_TRANSFER, like ProductionVeterancy) and Upgrade_CloneMe (OBJECT). The old upgrades are intact (pure append).
- **LogicCommand** Command_ConstructSovietCloningCenter (CONSTRUCTION_YARD_CONSTRUCT) + Cmd appended to SovietConstructionYardCommandSet and SovietCraneCommandSet; old order kept.
- **Center:**
  - BaseSovietStructure (+ACTIVATE_AFTER_UNPACK), KindOf additive, BuildTime 0 + unpack 30s, ObjectResourceInfo 2500, -100, limit 1, prereq SovietTechStructure;
  - HP 2000/2000; repair / engineer includes; LOOP idle animation kept;
  - no module id collisions with the base;
  - CaptureAndGiveUpgradeBehavior (UnificationType default SAME_PLAYER per UnifiedControlBehavior.xsd).
- **Barracks translates:**
  - Soviet: +1 translate after the 3 veterancy translates;
  - Japan: new full SDK copy + 1 translate (only diff);
  - Allied: the package's 151-line copy had **lost** the 3 SDK veterancy translates in an earlier batch. This batch restores them (= SDK L414-424) and adds the clone translate. This is an SDK-restoring change; it should be stated in the delivery notes.
- **16 infantry:** each has exactly one appended `ObjectCreationUpgrade id="ModuleTag_Clone" ThingToSpawn=<own id>` + `<TriggeredBy>Upgrade_CloneMe</TriggeredBy>` inside Behaviors, and nothing else changed.
  - The syntax matches the Hammer precedent and ObjectCreationUpgrade.xsd. Angle / Delay / RemoveUpgrade are optional and unused.
  - JapanAntiVehicleInfantry: added to the base object; the _Ambush child inherits it (harmless, never produced with CloneMe).

## Static defects (FIX)
1. **Missing 3 of 19 infantry:** AlliedScoutInfantry, SovietScoutInfantry (war bear), SovietAntiInfantryInfantry (conscript) — the most-produced Soviet infantry.
   - Full SDK files + deps are provided: `r79fix_sdk_refs.tar.gz`.
   - Package convention: the existing infantry copies have the ART includes stripped (e.g. SovietAntiVehicleInfantry 0 vs SDK 119); follow the same convention.
   - Add the same 5-line OCU, + Mod 3 includes.
2. **Duplicate asset id:** `GE_SovietVIPBunkerSubStructure_Die_OCL` is defined in SovietCloningCenter.xml L140 **and** in the bunker file, which Mod includes directly (+ again via Geneva.xml).
   - Two definitions of one id in the mod stream.
   - Fix: rename the center's OCL (e.g. `SovietCloningCenter_Die_OCL`) and its CreateObjectDie reference, and/or drop the bunker include (see 3).
3. **Unneeded global loads:**
   - `DATA:Civilian/Geneva.xml` (full SDK copy) pulls ~40 Geneva civilian objects/props globally via relative includes. Only 2 of those files exist in the package, so the rest depend on fallback resolution. This also double-includes the bunker.
   - `GE_SovietVIPBunkerSubStructure.xml` (the original civilian object) is not needed: the center is a full copy.
   - Precedent: 78FIX2 did not include Amsterdam.xml or the AM HQ.
   - Fix: remove the Geneva.xml and bunker Mod includes (and the files).
   - The collapse object is used via the center's instance include. Keeping its Mod include is optional; the quick production center did not.
4. **Unrequested deviations from the SDK bunker (restore):**
   - debris `CreationObject` changed AlliedBarracks_Debris → YU_HotelDebris (the original uses AlliedBarracks_Debris);
   - damage sounds filled in where the original has empty strings (cosmetic; restore or declare).
5. **CaptureAndGiveUpgrade map coverage:**
   - Schema: UpgradeMap OwnershipAmount is a SageInt. The academy maps 1/2/3 to three different upgrades, so it is unclear whether the value is an exact count or a threshold.
   - With only 1 and 2 mapped, a player owning 3+ centers (one built + captured others; up to the player count) may get no entry under exact matching.
   - Static fix: map OwnershipAmount 1…6 (max players) all to Upgrade_SovietCloning (no stacking).

## Scope note (fact, not an exception)
JapanScoutInfantry is the **Burst Drone**: SDK KindOf VEHICLE (not INFANTRY), produced by the Japan barracks. The cloud included it among the 16. Whether a barracks-produced drone counts as "兵" is an interpretation of the user's words. Flagged only; the 19-list was barracks products.

## Runtime only (no claims accepted)
- CaptureAndGiveUpgrade on a self-built building;
- revocation on destroy / sell / capture (the SDK only shows the count-map design; no explicit removal statement);
- grant during the 30s unpack despite ACTIVATE_AFTER_UNPACK;
- the clone not inheriting CloneMe / no recursion (static: the spawn is not produced, so no translate);
- whether OCU fires once;
- clone owner and placement collision;
- Tanya / Yuriko limit 1 vs spawn;
- queued units at the moment of loss.

The ≤2s figure is the user's quick production allowance and is **not** applied to cloning.
