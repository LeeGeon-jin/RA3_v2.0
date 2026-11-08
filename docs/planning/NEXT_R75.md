# Next (R75): Natasha bombing range ×1.5; sentry gun drops 1 conscript (+ found gap: sentry/flak build halving)
Refs: `r75_sdk_refs.tar.gz` (60925 B, sha256 0f67d7fffe682f6c39f52f7183bfad1fddd703b85fdc72354e2bab6f2efea88e):
- SovietCommandoTech1, Weapon, SpecialPowerTemplates, ObjectCreationLists;
- SovietBaseDefenseGround / Air, SovietBarracks;
- Includes GenericSovietBuildingDestruction / Suicide / GenericBuildingRepair / RepairAlliesEngineerContain.

## 1. Natasha call-in bombing vs buildings — distance ×1.5 (user 17:46; devdoc L737 "对付建筑距离增加")
- **The only range parameter in the chain:** package Weapon.xml L802-803 `SovietCommandoCallBombingRun AttackRange="300.0"`, MinimumAttackRange 50. Identical to SDK (SDK L807).
  - The weapon sits in Natasha's slot as SECONDARY (SovietCommandoTech1.xml L956).
  - Its SpecialPowerNugget fires SpecialPowerBombingRun, which has **no range** (SpecialPowerTemplates L707-709: TargetType OBJECT only).
  - OCLSpecialPower ModuleTag_BombingRun (L971-981) spawns OCL_SovietBombingRun at the nearest own SovietConstructionYard — no range.
  - OCLMonitorUpdate has no range.
  - **There is no StartAbilityRange for the bombing run.** StartAbilityRange 500 at L1091 belongs to Pilot Snipe → do not touch.
- **Not related:** TracerModelDraw MinLength/MaxLength 300 (L916-917) is the sniper-rifle tracer visual (rifle AttackRange 300) → do not touch. The sniper rifle and Pilot Snipe stay unchanged.
- **Minimal:** Weapon.xml L803 `AttackRange="300.0"` → `"450.0"`. One value; MinimumAttackRange 50 unchanged. → 119 XML; 1 file.
- **Side effects / native test:**
  - The weapon's filter targets VEHICLE **and** STRUCTURE (`Include="VEHICLE STRUCTURE VALID_TARGET_FOR_C4"`), so the 450 range also applies when the bombing is used on vehicles.
    - A structure-only range would need a split weapon. Not proposed: the user asked for distance only, and the existing weapon serves both.
  - Natasha's VisionRange is 325 (ShroudClearingRange 500) and the weapon has ATTACK_NEEDS_LINE_OF_SIGHT. Targets at 325-450 are within shroud clearing, but auto-acquire may still be limited by vision. In-game check; not changed (not requested).

## 2. Sentry gun destroyed → 1 conscript (user 17:46: 1)
- **Current:** SovietBaseDefenseGround is **not in the package** (SDK only: Soviet/Structures/SovietBaseDefenseGround.xml, 605 lines).
  - Death today:
    - CreateObjectDie `SBDefenseGround_Die_OCL` → collapse debris only (OCL L1775-1786);
    - DestroyDie;
    - xi:includes GenericBuildingRepair, **GenericSovietBuildingSuicide** (sell/suicide OCL), RepairAlliesEngineerContain (L541-546).
- **SDK precedent:** Soviet structures (e.g. SovietBarracks L466-467, Airfield, Refinery, Outpost, SuperWeapon) use:
  - `<xi:include href="DATA:Includes/GenericSovietBuildingDestruction.xml" />` → CreateObjectDie `ModuleTag_CreateOccupiedDie` CreationList `OCL_GenericSovietBuildingDestruction`;
  - that OCL creates 1 SovietAntiInfantryInfantry, health 0.3–0.75, options `REQUIRES_LIVE_PLAYER`, so the conscript belongs to the sentry's owner;
  - DieMux `ExemptStatus="OVER_WATER UNPACKING SOLD"` (no conscript when sold, unpacking or over water), DeathTypesForbidden DETONATED SUICIDED SHATTERED;
  - `UpgradeForbidden Upgrade_NoSpawnUponDestruction`.
- **Minimal:**
  - add the sentry gun as a full SDK copy (same id; package conventions);
  - add one xi:include of GenericSovietBuildingDestruction.xml next to the existing Suicide include, the same pair order as Barracks;
  - nothing else; the module id `ModuleTag_CreateOccupiedDie` does not collide with `ModuleTag_CreateObjectDie`;
  - Mod +1.
  - **Exactly 1 conscript** = the existing OCL, no new OCL.
- **Native test:** a conscript appears only on destruction, not on sale.

## 3. Gap found — defence build-time halving not fully implemented (decided, devdoc L212-215, 11-06 L31)
- **Decided:** "苏军哨兵炮 20 → 10 秒、防空炮 20 → 10 秒".
- **Package:** Allied BaseDefense 10 / Prism 15 / Tesla 15 / Japan tower are done. **SovietBaseDefenseGround and SovietBaseDefenseAir files are absent**, so both stay at the SDK `*_LOCAL_UNPACK_TIME` 20s:
  - Ground: SDK L52 `SOVIET_BASE_DEFENSE_GROUND_LOCAL_UNPACK_TIME 20s`;
  - Air: SDK L38 `SOVIET_BASE_DEFENSE_AIR_LOCAL_UNPACK_TIME 20s`; BuildTime 0.0 for both.
- **Minimal:**
  - in the same sentry full copy, Define 20s→10s (same as the Tesla coil precedent);
  - SovietBaseDefenseAir full copy with Define 20s→10s;
  - Mod +1.
- **Combined batch (2 + 3):** 2 new files, Mod +2 → 121 XML, Mod 119. Batch 1 (Natasha) can go separately or in the same batch (Weapon.xml 1 value).

## Not in scope (decided by user, but not implemented here)
- Apocalypse VX AA and quick production 2 s are now decided and remain to be implemented separately.
- Cloning and quick production centers (HP 2000 = battle lab) are not implemented.
