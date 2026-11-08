# BATCH82 AUDIT — FAIL (2 content defects in new full copies)
Static check only: no compile, no in-game test, no PC. Not Phase 1 complete.

## Package
- `batch82.tar.gz` 333065 B, sha256 013e0449…11db (matches).
- All 135 XML files parse.
- Mod.xml: 133 `type="all"` includes.
- vs Batch81: 14 changed + 5 new + Mod.xml = 20 entries differ. The other **115** files are byte-identical (cloud's "116" is wrong; 135 − 20 = 115).
- GlobalData/Weapon.xml is unchanged, so Hammer reload .4 / .667 and every other earlier weapon dependency is kept.
- CampaignOverrides is not in the package and was not touched (SDK has 0 crush fields there).

## PASS parts
- **14 existing files:** each `diff` vs B81 is exactly one line, `CrushDecelerationPercent` → `0%`:
  - AssaultDestroyer (AlliedAntiNavyShipTech1) L505, from 50%;
  - from 80%: AlliedAntiStructureVehicle L627, AlliedAntiVehicleVehicleTech1 L477, AlliedAntiVehicleVehicleTech3 L695, AlliedMCV L667, AlliedMiner L493, JapanMCV L507, JapanMiner L862, JapanEmperorMecha L506, SovietAntiStructureVehicle L397, SovietAntiVehicleVehicleTech3 L789, SovietMCV L593, SovietMiner L570, SovietSurveyor L339.
  - Not touched: crush levels, CrushWeapon, ExtraCrushLevels / water crush, AI, production or tech entries.
  - JapanMechaKing is not in the diff and stays 0%.
- **BaseVehicle.xml** (191/191 lines vs SDK): `diff -w` shows only L41 `CrushKillDelay 1.5s → 0s` and L186 `80% → 0%`.
- **BaseEgg.xml** (68/68 lines): only L52 `80% → 0%`.
- **SovietAntiVehicleVehicleTech2** (Tesla tank): only the 3 ART includes stripped (package convention) and L425 → 0%.
  - Its Buildable / cost 2200 / time 22 / prerequisites stay at SDK values, so it is **not** unlocked by this batch.
- **Mod.xml:** +5 includes, placed after BaseMiner / BaseOreNode (L64-68: BaseVehicle, BaseEgg, JapanAVVT1, SovietAVVT1, SovietAVVT2). Each id is defined once in the package; no duplicate asset ids.
  - Cosmetic: L62-63 lost one indent tab.

## FAIL 1 — JapanAntiVehicleVehicleTech1 (Tsunami tank): data removed beyond the ART convention
SDK 580 lines vs package 220 lines. Besides the ART includes, the copy **deleted**:
- the **entire `<Draws>`** block (SDK L76-384):
  - TruckDraw `ModuleTag_Draw` (model JUAntiVehicleVehicleTech1_SKN, weapon / turret bones, damage states, land / water transform AnimationStates + scripts);
  - the `xi:include DATA:Includes/HeadlightDraw1.xml`;
  - ScriptedModelDraws `ModuleTag_FX` (nano armor FX) and `ModuleTag_ParticlesDraw` (water wakes);
- the **entire `<ClientBehaviors>`** block (SDK L494-520): move loops, shrunken voice, water voice selector, transform AnimationSoundCB;
- a commented AudioEntry at L553-555 (harmless).

No earlier package full copy drops Draws (e.g. SovietAntiVehicleVehicleTech3 and AlliedMiner keep `<Draws>`). Without a Draw module the unit has no model. This is a real regression, not a crush change.

**Fix:** recopy the SDK file. Strip only the 7 ART `<Include>` lines (SDK L7-27). Keep Draws, the HeadlightDraw xi:include, ClientBehaviors and all modules. Change only L563 `80% → 0%`.

## FAIL 2 — SovietAntiVehicleVehicleTech1 (Hammer tank): leech table entries removed
Besides the ART includes (SDK L8-40), the copy deleted 5 `IncludeThing` lines inside the Leech beam ObjectEffectTuples:
- SDK L1213 `AlliedAntiVehicleVehicleTech3`, from the Leech_PrismCannonUpgrade tuple; AlliedFighterAircraft is kept;
- SDK L1226-1228 `SovietAntiInfantryVehicle`, `JapanAntiInfantryVehicle`, `AlliedAntiInfantryVehicle`, from the Leech_AutoCannonUpgrade tuple; JapanMiner is kept;
- SDK L1235 `SovietAntiStructureVehicle`, from the Leech_V4RocketUpgrade tuple; SovietAntiStructureShip is kept.

This changes the Hammer's leech-absorb gameplay: it can no longer absorb those weapons. That is outside the crush scope.

The Hammer is an ordinary buildable SDK unit (its Buildable / cost / build entry are unchanged here). A "not unlocked" narrative must not lead to adding or removing build-chain entries, and none were.

**Fix:** recopy the SDK file. Strip only the ART `<Include>` lines (SDK L8-40). Keep every IncludeThing. Change only L1541 `80% → 0%`.

## Notes (not FAIL)
- **BaseVehicle** keeps the SDK relative include `source="BaseObject.xml"` (L7). In the package that resolves next to `data/BaseObjects/`, where BaseObject.xml is not shipped. It falls back like the already-accepted CoopBasePersonality `BasePersonality.xml`. `DATA:BaseObjects/BaseObject.xml` (the form BaseOreNode uses) is an optional, safer equivalent.
- **BaseEgg / cores:** SDK BaseEgg includes `DATA:BaseObjects/BaseVehicle.xml` as an instance include and defines no SquishCollide of its own. It inherits the BaseVehicle `DefaultSquishCollide` by id.
  - The package's 2 cores inherit BaseEgg.
  - BaseVehicle is now both Mod-included (`all`) and instance-included by BaseEgg / BaseMiner. That is the same pattern as the existing BaseMiner, which is Mod-included and instance-includes BaseVehicle.
  - The asset builder resolves by id, and there are no duplicate definitions. Merge-by-id inheritance means no second SquishCollide is added.
  - Build-time duplicate handling is unproven (runtime / native).
- **Runtime unproven:**
  - whether base-object overrides reach every SDK vehicle inheriting BaseVehicle;
  - whether the crush stop disappears (the engine pathfinding part may remain);
  - how wrecks look at 0s.
  - These are source candidates through static inheritance only.

## Verdict
FAIL. Re-issue only JapanAntiVehicleVehicleTech1.xml and SovietAntiVehicleVehicleTech1.xml as described. Everything else in B82 can stay byte-identical.
NEXT_R83 (UnitAISettings) is deferred until the crush fix passes, per "若通过".
