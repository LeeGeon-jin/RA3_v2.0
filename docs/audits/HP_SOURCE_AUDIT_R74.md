# HP_SOURCE_AUDIT_R74 — original model-building health (SDK, read-only)
User decision (17:28): Guard02, cloning center and quick production center keep the original HP of each model's building.
Sources: real SDK `XMLFiles/`; package = Batch73FIX (b109). No PC, no compile, no source edit.
Refs: `hp_r74_sdk_refs.tar.gz` (10680 B, sha256 25898bb66bf23ce72d21a0c7483720dc1bb7600092ef0fcc0b231600fbad674f, 15 files; paths are relative to the SDK root, e.g. `XMLFiles/Civilian/...`, `Schemas/xsd/Modules/...`).

## 1. Cloning center model — GE_SovietVIPBunkerSubStructure
- **File:** `XMLFiles/Civilian/Geneva_GE/Buildings/GE_SovietVIPBunkerSubStructure.xml`, GameObject id L12.
- **Parent:** `inheritFrom="BaseCivilianStructureNoGarrisonDestructible"` (L13) → BaseCivilianStructureNoGarrison.
  - The parents' Body is `<ActiveBody id="DefaultBody"/>` with no MaxHealth.
- **HP:** `<ActiveBody id="ModuleTag_Body" MaxHealth="7500.0"/>` (L80-84). A literal, not a Define.
  - No InitialHealth → schema default -1.0 (ActiveBody.xsd: `InitialHealth default="-1.0"`, i.e. starts at MaxHealth by convention; native behaviour not tested).
- **Original HP = 7500.**

## 2. Quick production center model — AM_AlliedFutureTechHQ
- **File:** `XMLFiles/Civilian/Amsterdam_AM/Buildings/AM_AlliedFutureTechHQ.xml`, GameObject id L12.
- **Parent:** `inheritFrom="BaseCivilianStructureNoGarrisonDestructible"` (L13).
- **HP:** `<ActiveBody id="ModuleTag_Body" MaxHealth="=50000"/>` (L74-78).
  - A literal expression `=50000`, no `$` Define.
  - ArmorSet AlliedConYardArmor (L80-82). No InitialHealth.
- **Original HP = 50000.**

## 3. Guard02 — TH_StatueGuard02
- **File:** `XMLFiles/Civilian/Tokyo_Harbor_TH/Buildings/TH_StatueGuard02.xml`, id L13.
  - It is an `OPTIMIZED_PROPS` object, `inheritFrom="BaseSimulatedProp"` (L14).
  - KindOf `$BASE_CRUSHABLE_OBSTACLE_CLEAR_BY_BUILD_KINDOF`.
  - DynamicsDraw, ToppleUpdate KillWhenToppled, SlowDeath.
  - **No Body in the file.**
- **Parent:** `XMLFiles/BaseObjects/BaseSimulatedProp.xml` (id L10).
  - Body = `<PropBody id="DefaultBody"/>` (L41-44), ArmorSet NoArmor.
  - Schema `Schemas/xsd/Modules/PropBody.xsd`: PropBodyModuleData extends BodyModuleData with **no MaxHealth attribute** (MaxHealth exists only on ActiveBody, ActiveBody.xsd).
- **Fact: TH_StatueGuard02 has no original HP value in the SDK.** It is a prop body destroyed by toppling/crushing, not a health-based building.
- **Siblings, for context only — not assumed equal:**
  - TH_StatueGuard01 is also BaseSimulatedProp / no HP.
  - TH_StatueGuard03 is a real structure (BaseCivilianStructureNoGarrisonDestructible, ActiveBody `MaxHealth="=$CIV_HEALTH_SMALL"`, GlobalDefines L13 `CIV_HEALTH_SMALL = 2000.0`).
- **Package precedent:** b109 `Japan/Structures/JapanStatueGuard01.xml` L70-74 converts Guard01's PropBody to ActiveBody `MaxHealth="2000"` (comment in file). That was an earlier batch decision, not an SDK original HP.
- **Gap:** "keep the original HP" cannot be satisfied literally for Guard02, because no value exists. Any HP for Guard02 (e.g. following the Guard01 2000 precedent) is a choice, not an original value.

## 4. Current package (b109 / Batch73FIX)
- I searched all 118 package XML for `GE_SovietVIPBunker`, `AM_AlliedFutureTech`, `TH_StatueGuard02`, and for clone / quick-production / Guard02 ids and aliases. **No match for any of the three.**
- **Present:** JapanStatueGuard01Buildable / JapanStatueGuard03Buildable (Guard01/03), AlliedSuperWeapon's `ModuleTag_CloneStoredObjectsSpecialPower` (the chronosphere — unrelated to the cloning center).
- **Gap:** the cloning center, quick production center and Guard02 objects are **not implemented** in the package. The HP values above are ready for when they are built.

## Summary
| Object (model) | SDK original HP | Source | In package |
|---|---|---|---|
| Cloning center (GE_SovietVIPBunkerSubStructure) | 7500.0 | GE_SovietVIPBunkerSubStructure.xml L83 | not present |
| Quick production center (AM_AlliedFutureTechHQ) | =50000 | AM_AlliedFutureTechHQ.xml L77 | not present |
| Guard02 (TH_StatueGuard02) | none (PropBody, no MaxHealth) | TH_StatueGuard02.xml + BaseSimulatedProp.xml L41-44 + PropBody.xsd | not present |
