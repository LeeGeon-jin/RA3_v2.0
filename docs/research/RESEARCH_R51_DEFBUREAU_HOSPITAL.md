# R51 research (read-only): Defense Bureau 1000/15 origin + Hospital batch plan
No source edits, no PC, no compile.

## 1. AlliedTechStructure (Defense Bureau) 1000 / 15
### Package history (real tars, BuildTime / BuildCost of AlliedTechStructure.xml)
| Package | Value |
|---|---|
| structures_base / xmlfix / artfix / artfix2 (box) | file absent |
| structures_phase1_validated (handoff, 2026-11-07 22:18) | file absent |
| **batch2_fix** (earliest box copy containing it; batch2 itself not on box) | **15 / 1000**, GameDependency kept AlliedAirfield + AlliedRefinery |
| batch3 … batch50 (every handoff tar checked) | 15 / 1000 unchanged |
SDK original: BuildTime 30, Amount 1500.
### Origin of the value
- Cloud artifact `artifacts/FINAL_SUMMARY.txt` (2026-11-07 22:10) L81: "AlliedTechStructure (国防局): 1000块/15秒/无前置" under "后续批次需处理".
- `artifacts/PHASE1_REGRESSION_REPORT.txt` L145-147: "[Item #1] AlliedTechStructure (国防局) … 需求: 科技建筑统一1000块/15秒/无前提".
→ The cloud mapped the user rule "科技建筑统一1000块、15秒、无前置" (doc L224, 5.1 #11 "解锁允许建造加成建筑，如精英学院、医院等") onto the Defense Bureau. It even contradicts itself: "无前置" yet Airfield+Refinery were kept.
### Doc evidence
- L224/L226/L30: the rule is about **buildable neutral tech buildings** ("加成建筑，如精英学院、医院"; L226 "新 id 直接写造价，不改全局 $TECH_STRUCTURE_EFFECTIVE_COST，地图上原有、可占领的科技建筑不受影响").
- L459-464 (Defense Bureau item, 5.4 #2): check result "不删、不改其现有前提（机场 + 矿场保留）… 未实作 mod，只更新本开发规范" — no cost/time change.
- L221/L263/L487/L524/L589/L788 mention the Defense Bureau only as a prerequisite; no cost/time decision found anywhere in the doc.
### Memory / transcripts
- Shared memory (333 facts) has Defense Bureau facts (tier licences removed; Tanya, coastal gun, quick-prod prereq) but **no** Defense Bureau cost/time fact.
- Other session transcripts: not readable from this run (no session id given), so user wording outside the doc is **unchecked**. Absence ≠ no decision.
### My earlier audits
BATCH2_BLOCKED / BATCH3–BATCH4 audits list AlliedTechStructure only for ART/regression; none checked its values against a decision. The value passed unnoticed since batch2.
### Status
**Conflict, unresolved:** package 1000/15 vs doc (no change). Likely a misapplied neutral-tech rule. Do not revert yet. Minimal user question: "国防局造价/时间是否改为 1000 / 15 秒？（文档只对中立科技建筑定了 1000 / 15，国防局未定）". If no → revert BuildTime 30 / Amount 1500 (prereqs already original).

## 2. Hospital (buildable neutral tech) — decisions check
| Point | Doc / memory evidence | Status |
|---|---|---|
| Which sides | L224 is in 5.1 (global) and adds "对于帝国…所有科技建筑…直接…建造" → all three sides; L30 same. | decided: 3 sides |
| Cost / time / prereq | L224, L226, L30: 1000 / 15 s / none | decided |
| Power | not mentioned; SDK hospital & BaseTechStructure have no EnergyProduction | keep none (no field) |
| Health | no tech-building health rule; no change requested; SDK MaxHealth 3000.0 | keep original field untouched. (Differs from quick-prod: doc explicitly "待定"; and from clone center: new function on a reskinned civilian model, no rule.) |
| Japan | direct place CONSTRUCTION_YARD_CONSTRUCT, BuildTime 15 (L224/L226); Japan CY accepts MAIN_STRUCTURE since batch 50 | decided |
| Soviet | doc only says "15 秒"; Soviet mechanism (BuildTime vs unpack) **not stated** for tech buildings | technical: use Soviet convention BuildTime 0 + unpack 15 s (Kremlin precedent passed) — record as technical choice, TEST |
| Build animation / dust | memory 2026-11-06: "new buildable tech buildings and Rapid Production Center get no build animation or dust effect; they just appear when placed"; doc L1089 "同已定科技建筑 / 快速生产中心写法 … 无建造动画、无烟尘，直接出现（已定）" | decided. Hospital model has PARSE_DEFAULT "no anim"; BaseTechStructure has no build FX/dust → nothing to add. Do **not** copy landmark/Soviet build-up FX. Soviet unpack 15 s gives only timing on the static model (no animation) — consistent; TEST visual. |
| Attackable | no tech-building rule; parent KindOf has NOT_AUTOACQUIRABLE (landmark "-NOT_AUTOACQUIRABLE" rule is landmarks only) | keep parent flags |
| Limit | not decided | leave unset |
| Map hospitals | L226 "地图上原有、可占领的科技建筑不受影响" | new ids only; HospitalTechStructure untouched |
### Ownership / capture chain (SDK)
- `BaseObjects/BaseTechStructure.xml`: inheritFrom BaseObject; Side Neutral; CommandSet EmptyCommandSet; KindOf `STRUCTURE SELECTABLE IMMOBILE CAN_CAST_REFLECTIONS FS_TECHNOLOGY NOT_AUTOACQUIRABLE IGNORE_FOR_VICTORY NOT_SELLABLE NEUTRAL_TECH ALWAYS_VISIBLE_IN_RADAR CAN_BUILD_ON_WATER CAN_BUILD_ON_DEEP_WATER`; ModelConditionUpgrade USER_1/2/3 by Upgrade_AlliesFaction/SovietFaction/JapanFaction (owner-faction look); SlowDeath; FXList; `StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="0.0s"`; SecondaryDamageTracker; AIUpdate StructureAIStateMachine; ActiveBody DefaultBody; EVA BuildingStolen / EnemyBuildingCaptured. Includes BaseObject.xml, AU/SU/JU_Garrison_Flag.w3x, NU_GarFlag.xml.
- `Neutral/Structures/HospitalTechStructure.xml`: TechBuildingFlagDraw xi (owner flag), Physics, PassiveAreaEffectBehavior (EffectRadius -1, NonStackable, 2%/s, INFANTRY ALLIES + contained), **GenericEngineerContain xi (engineer capture → enemy can still capture a built one)**, GenericBuildingRepair, LUAEventList BuildingPowerFunctions, BuildingDestructionBehavior, AIUpdate AutoAcquire NO, MaxHealth 3000, EVA HospitalCaptured.
- Built by a player → owned by that player (owner-faction flag/look). Re-capture by enemy engineer possible (original behaviour, not changed). TEST.
### Minimal Batch 51 (no undecided values)
One new file e.g. `data/Neutral/Structures/HospitalTechStructureBuildable.xml` with three GameObjects, each `inheritFrom="HospitalTechStructure"`? — **No**: HospitalTechStructure is not loaded in skirmish by the mod unless included; inheriting would also need the SDK file as instance include. Simplest safe: Include `type="instance" source="DATA:Neutral/Structures/HospitalTechStructure.xml"` and inherit, overriding only:
- id/EditorName `AlliedHospitalTechStructureBuildable` / `SovietHospitalTechStructureBuildable` / `JapanHospitalTechStructureBuildable`; Side Allies/Soviet/Japan.
- `ObjectResourceInfo` BuildCost `=$ACCOUNT_ORE` 1000 (literal, macro untouched).
- BuildTime 15 (Allied, Japan); Soviet BuildTime 0 + `StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="15s"` (same id → merge).
- `BuildPlacementTypeFlag="MAIN_STRUCTURE"` (ProductionQueueType MAIN_STRUCTURE already in source).
- No GameDependency, no EnergyProduction, no KindOf change, no Body change, no animation/FX.
(Alternative: three full verbatim copies — larger diff; inheritance keeps every original node by construction. Instance include of a civilian/neutral file is the same mechanism used for Collapse files; build-log check.)
Commands: `Command_ConstructAlliedHospitalTechStructure`, `…Soviet…`, `…Japan…` (CONSTRUCTION_YARD_CONSTRUCT). Append: AlliedConstructionYardCommandSetBase 16→17, AlliedCraneCommandSet 15→16, SovietConstructionYardCommandSet 21→22, SovietCraneCommandSet 19→20, JapanConstructionYardCommandSet 19→20. Mod +1 include → 98 all + 3 ref.
### SDK attachments (XMLFiles/)
Neutral/Structures/HospitalTechStructure.xml; Neutral/Props/HospitalTechStructure_Collapse.xml (→ BaseObjects/BaseCollapsingObject.xml, ART NUHospitalTechStructure_COL.w3x); BaseObjects/BaseTechStructure.xml; BaseObjects/BaseObject.xml; Includes/TechBuildingFlagDraw.xml; Includes/GenericEngineerContain.xml; Includes/GenericBuildingRepair.xml; Civilian/Yucatan_YU/Props/YU_HotelDebris.xml; GlobalData/GlobalDefines.xml. Schemas: Schemas/xsd/Modules/PassiveAreaEffectBehavior.xsd, StructureUnpackUpdate.xsd, EngineerContain.xsd, ModelConditionUpgrade.xsd, SlowDeath.xsd; Schemas/xsd/AssetTypeGameObject.xsd. ART: NUHospitalTechStructure.w3x, ABBarracks_particles.w3x, AU/SU/JU_Garrison_Flag.w3x, NU_GarFlag.xml. Package refs: Soviet/Structures/SovietGreatKremlinPalace.xml (unpack override), GlobalData/LogicCommand.xml, LogicCommandSet.xml.
### Tests
Self-built ownership & flag, heal works when built, engineer recapture, Soviet 15 s timer on static model, Japan placement in 480×465, no dust/animation.

## Unchanged open items
Quick-prod 2 s aura expiry ≠ immediate restore (unresolved); clone / quick-prod / Guard02 health; Rushmore Japan split; Defense Bureau question above.
