# Next item research: buildable neutral tech buildings (5.1 #11, doc L223-L228; 5.2 L367-L426)
## Latest decisions (doc)
- L224 user: "解锁允许建造加成建筑，如精英学院、医院等（本人补充：科技建筑统一1000块、15秒、无前置。精英学院1500、15秒。）…（本人最终决定：算啦算啦，精兵学院不调整了。）（本人补充：对于帝国，…所有科技建筑…直接像盟军一样部署好了直接在基地周围建造。）"
- L226: buildable versions 1000 / 15 s / no prereq; academy 1500 / 15 s with original effect; **new id, write cost directly, do not change global $TECH_STRUCTURE_EFFECTIVE_COST**; map tech buildings unaffected; Japan direct place (CONSTRUCTION_YARD_CONSTRUCT); ownership / re-capture = test.
- L30 (11-06 revision): "科技建筑 1000 / 15 秒、无前提，精英学院 1500 / 15 秒".
- Health: not mentioned → keep original (no change, no guess). Hospital MaxHealth 3000.
## Scope ambiguity (record, do not guess)
- Which buildings: user list 5.2 = oil derrick, hospital, garage, dry dock, airport, academy, observation post (+ shops/bank = map-specific, not tech). SDK Neutral/Structures also has DefensiveStructureTechStructure, NeutralPowerPlant (not in user list → exclude).
- Academy: "精兵学院不调整了" read by doc L226 as "effect unchanged, still buildable 1500/15" — ambiguous (could mean drop it). Keep out of first batch.
- Airport paradrop (L398-402) = separate larger item.
## Minimal Batch 51 = Hospital only (explicitly named in L224)
Source `Neutral/Structures/HospitalTechStructure.xml` (189 lines): parent BaseTechStructure (Side Neutral, CommandSet EmptyCommandSet, KindOf includes NOT_AUTOACQUIRABLE IGNORE_FOR_VICTORY NOT_SELLABLE NEUTRAL_TECH; faction ModelConditionUpgrade USER_1/2/3; StructureUnpackUpdate id `ModuleTag_StructureUnpackUpdate` 0.0s; SlowDeath; DefaultBody).
Per-side new ids (package precedent: per-side Rushmore heads/statues):
- `AlliedHospitalTechStructureBuildable`: Side Allies, BuildTime 15.
- `SovietHospitalTechStructureBuildable`: Side Soviet, BuildTime 0 + override `StructureUnpackUpdate id="ModuleTag_StructureUnpackUpdate" UnpackTime="15s"` (same id as parent → merge; Kremlin precedent of BuildTime 0 + unpack).
- `JapanHospitalTechStructureBuildable`: Side Japan, BuildTime 15, direct place.
Each: full copy of the hospital node set; cost `Amount="1000"` literal (replaces macro); no GameDependency; keep ProductionQueueType MAIN_STRUCTURE (original) and add BuildPlacementTypeFlag MAIN_STRUCTURE (Japan CY now accepts MAIN, batch 50); keep PassiveAreaEffect (-1, 2%), Armor, Body 3000, Geometry, UI, collapse/YU includes. No limit (MaxSimultaneousOfType not decided → leave unset). KindOf left as parent (no new flag request; IGNORE_FOR_VICTORY/NOT_SELLABLE retained — note test).
Commands: 3 × `CONSTRUCTION_YARD_CONSTRUCT` Command_Construct<Side>HospitalTechStructure; append to AlliedConstructionYardCommandSetBase (16→17) + AlliedCraneCommandSet (15→16), SovietConstructionYardCommandSet (21→22) + SovietCraneCommandSet (19→20), JapanConstructionYardCommandSet (19→20). Mod +3 (or one file with 3 objects +1).
Attach (SDK XMLFiles/): Neutral/Structures/HospitalTechStructure.xml; Neutral/Props/HospitalTechStructure_Collapse.xml; BaseObjects/BaseTechStructure.xml; BaseObjects/BaseObject.xml; Civilian/Yucatan_YU/Props/YU_HotelDebris.xml; GlobalData/GlobalDefines.xml; package Soviet/Structures/SovietGreatKremlinPalace.xml (unpack template) + GlobalData/LogicCommand(Set).xml.
Tests: self-built neutral-tech flagged building ownership/capture, heal works when built, Soviet unpack 15 s, Japan placement.
Then same template → garage, dry dock, airport heal, oil derrick, observation post (values identical, no new decisions).

## Side finding to verify (prior batch, not Batch50)
Package `Allied/Structures/AlliedTechStructure.xml` (Defense Bureau) is 1000 / 15 s (SDK 1500 / 30). The "科技建筑 1000/15" rule refers to neutral tech buildings; I found no decision changing the Defense Bureau. Check whether an earlier passed batch justified it; if not, revert to SDK.

## Still unresolved
Quick-production 2 s aura expiry ≠ "立即恢复"; clone / quick / Guard02 health; Rushmore Japan split.
