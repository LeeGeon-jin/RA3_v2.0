# Next (R79): Infantry Cloning Center — decided facts, SDK mechanism, impact
Refs: `r79_sdk_refs.tar.gz` (28820 B, sha256 4cbca9dd77d122f09f0bb16647ceb4ec94af1121358909124c668a7ceeffc131):
- VIP bunker + collapse + Geneva.xml;
- VeterancyTechStructure, upgrade.xml;
- Soviet / Allied / Japan Barracks;
- Hammer (ObjectCreationUpgrade precedent), AlliedConstructionYard (GrantUpgradeCreate);
- SovietTechStructure, BaseSovietStructure, LogicCommandSet;
- 5 module xsds.

## Decided (devdoc L803 user, L806 plan, L34 decisions, your brief)
| Item | Value | Source |
|---|---|---|
| Side | **Soviet building only** ("增加苏联建筑步兵复制中心"). Not three sides; correct the brief's "三军". | L803 |
| Cost / time / power | 2500 / 30s (Soviet unpack 30s, BuildTime 0) / -100 | L803, L806 |
| Prereq | Battle Lab SovietTechStructure | L803 |
| Model | GE_SovietVIPBunkerSubStructure (ART W3X, collapse, YU_HotelDebris; only WorldBuilder / map loaded → the mod must include them). The model has a LOOP idle animation (keep; it is not a build animation). Original HP 7500. | L806; SDK file L6-8, L35-36, L83 |
| HP | 2000 (= battle lab, your later decision) | brief |
| Limit | one per player, no stacking ("6.只能造一个，不能叠加") | L34, L806 |
| Effect | "效果和ra2复制中心效果一样" → each infantry produced gets one free copy | L803, L806 |
| Scope | **"7.能复制，只要是兵就能复制"** — all infantry, no exceptions | L34 |

### Scope consequences (no technical exceptions invented)
- Soviet barracks infantry per SDK SovietBarracksCommandSet: SovietScoutInfantry (war bear), AntiInfantry (conscript), AntiVehicle (flak), Engineer, HeavyAntiVehicle (tesla), CommandoTech1 (Natasha).
  - (The doc L806 mention of a "苏军间谍" is wrong; there is none in the Soviet set.)
- "只要是兵" also covers infantry the owner produces from **captured Allied/Japan barracks**, and infantry of a player who **captures the center**:
  - Allied: Scout (dog), AntiInfantry, AntiVehicle, Engineer, Infiltration (spy), CommandoTech1 (Tanya);
  - Japan: Scout, AntiInfantry, AntiVehicle, Engineer, Infiltration, AntiVehicleInfantryTech3 (rocket angel), CommandoTech1 (Yuriko).
  - Full coverage = 19 infantry + 3 barracks.
- **Heroes:**
  - Natasha has no limit in the package (Batch68 removed MaxSimultaneousOfType);
  - Tanya / Yuriko keep SDK MaxSimultaneousOfType 1 → whether an OCU spawn bypasses or is refused is runtime. Do not add or remove limits.

## Mechanism (SDK chain; decided pattern L806, verified pieces)
1. **Center:** `CaptureAndGiveUpgradeBehavior` (schema: UpgradeMap OwnershipAmount / ProvidedUpgrade).
   - It extends UnifiedControlBehavior, `UnificationType` default **SAME_PLAYER**, so it is per player, unlike the academy's ALLIED_PLAYERS.
   - The count-based map implies ownership recomputation (academy precedent VeterancyTechStructure L52-58), so the upgrade should follow ownership on destroy / sell / capture. **Runtime test**, including whether it fires for a self-built (not captured) building.
   - Map `OwnershipAmount 1 → Upgrade_SovietCloning` and **also `OwnershipAmount 2 → the same upgrade`**, so a captured second center keeps exactly one effect (no stacking) instead of possibly losing it when the count is 2.
   - New PLAYER upgrade, options like Upgrade_ProductionVeterancy (upgrade.xml L46-49: Type PLAYER, DO_NOT_TRANSFER).
2. **Barracks** ProductionUpdate `GiveUpgradeToProduced`: add `UpgradeTranslate RequiredUpgrade=Upgrade_SovietCloning ProvidedUpgrade=Upgrade_CloneMe` (OBJECT type, like Upgrade_CreationVeterancy, upgrade.xml L61).
   - Precedent SovietBarracks L427-447. Keep the 3 veterancy translates.
   - Applies at production exit, so an item already queued gets cloned if the player has the upgrade when it pops out. Same for Allied/Japan barracks (full scope).
3. **Each infantry:** `ObjectCreationUpgrade ThingToSpawn=<own template>` TriggeredBy Upgrade_CloneMe (Hammer L1411-1415 precedent; schema also has Angle / Delay / RemoveUpgrade).
   - **Recursion:** the clone is spawned, not produced, so it never receives CloneMe → no loop.
   - The clone spawns at the unit's position (not from the center), with no rally point and no veterancy.
   - The owner is the producing player (runtime confirm).
   - Collision / placement and transforming infantry (rocket angel) are runtime.
- **Rejected:** GrantUpgradeCreate (AlliedConstructionYard L501) is a permanent grant with no SDK removal → would leave residue after loss.

## Impact (large; report before editing)
New:
- center object (BaseSovietStructure + repair / engineer includes as in 78FIX2, ACTIVATE_AFTER_UNPACK);
- 2 upgrades (upgrade.xml full copy or new GlobalData file);
- LogicCommand + Soviet CY / crane sets.

Modified:
- 3 barracks (Allied / Soviet already in the package; Japan new full copy);
- 19 infantry (Allied ×5, Japan ×7 and Soviet ×4 already in the package; 3 new full copies needed: SovietScoutInfantry, SovietAntiInfantryInfantry, AlliedScoutInfantry).

Campaign: global rule; hero script interplay is runtime.

## Runtime tests
- self-built CaptureAndGiveUpgrade grant;
- revocation on destroy / sell / capture;
- 2-center behaviour;
- clone owner and placement;
- hero limits for Tanya / Yuriko;
- queued items at the moment of loss;
- spy / engineer doubling;
- performance.
