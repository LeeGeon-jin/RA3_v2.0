# BATCH47 AUDIT — FAIL (1 blocker, one-line fix)
Box-only read; not full XSD, not compiled, not tested in game. Phase 1 not complete.

## Package
- 247625 B, sha256 `49a9d2bb840338517a8f3683fda44e56ae10935df2dc91da1bfeec0a20894a59` match; saved `batch47.tar.gz`; safe paths.
- vs 46: new 1 (`Japan/Structures/JapanStatueGuard01.xml`), changed 3 (LogicCommand, LogicCommandSet, Mod), 89 identical. 93 XML parse; Mod 92 all + 3 ref; id unique (1 definition); Guard02 not referenced.
- Command `Command_ConstructJapanStatueGuard01` CONSTRUCTION_YARD_CONSTRUCT → `JapanStatueGuard01Buildable` OK. JapanConstructionYardCommandSet append at end, old order kept; real count **19→20** (Fuji in B44 already made 19; brief's "18→19" is stale). Mod +1.

## BLOCKER — ArmorSet merge
Package: `<ArmorSet Armor="NoArmor" />` (no id).
Parent `BaseCivilianStructureNoGarrison` defines `<ArmorSet id="DefaultArmor" Armor="StructureArmor" .../>`. xai merges list children by id; an id-less child is appended, not overriding. Effective = two unconditioned ArmorSets (StructureArmor + NoArmor) → ambiguous, not the intended "NoArmor replaces parent".
SDK precedent: `Civilian/Mount_Rushmore_MR/Buildings/MR_RushmoreFiringBase.xml` L24-27 `<ArmorSet id="DefaultArmor" xai:joinAction="Replace" Armor="A06_FiringBaseArmor"`.
**Fix:** `<ArmorSet id="DefaultArmor" xai:joinAction="Replace" Armor="NoArmor" />` (xmlns:xai already on root). Nothing else.
Note: B43 Guard03 has the same id-less pattern, but with StructureArmor (same value as parent) → harmless duplicate; optionally align later.

## Verified OK
- Source real TH_StatueGuard01. Parent NoGarrisonDestructible; KindOf crush macro removed, `-NOT_AUTOACQUIRABLE`; Japan, 10, 0 power, no prereq, Max 1, OTHER_STRUCTURE ×2, cost 1000 ORE.
- Draw: ScriptedModelDraw id ModuleTag_Draw, PARSE_DEFAULT Model `TH_StatueGuard01` (= original). All Dynamics-only fields removed: Collision, Explodiness, InitiallyActive, 13 BoneVolumes, Lifetime. Empty PARSE_DEFAULT AnimationState = Guard03 precedent. `OkToChangeModelColor="true"` is an addition (also in Guard03; color tint only, not data invention of bones/UI). No RUBBLE/bones.
- No ART include: TH object's `ART:TH_StatueGuard01.w3x` not carried; same pattern as Guard03 (model resolved by name in build) → build-log check.
- ToppleUpdate removed. FXList `ModuleTag_FXList` Replace, DieMux ALL, onDeath FX_RockCrush_AudioOnly = original local (replaces parent FX_MediumBuildingDieExplosion).
- SlowDeath: package `ModuleTag_Death` 1.5s/4/8s DeathTypes ALL = **original TH local** verbatim. Prop parent's separate `ModuleTag_SlowDeath` (TOPPLED) disappears with re-parent; not merged, not altered. Pass.
- Body ActiveBody DefaultBody MaxHealth 2000 (merges with parent id). PropBody gone.
- Geometry IsSmall false, BOX 8.70357/9.7518/49.2804, ContactPointGeneration STRUCTURE, offset 4.42938/3.6086/0.251526 — exact.
- Effective chain: no EnableDynamics, no id_CrusherInfo, no prop SlowDeath (all BaseSimulatedProp-only). Inherited: AttributeModifierPool, SecondaryDamageTracker etc. from NoGarrison; KindOf from Destructible (SELECTABLE STRUCTURE … minus NOT_AUTOACQUIRABLE). No BuildingDestruction/xi/UI added.

## Next
Fix the single ArmorSet line → resubmit as 47_FIX. Statue of Liberty research deferred until pass (per instruction). Guard02 untouched.
