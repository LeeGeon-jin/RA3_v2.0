# BATCH48 AUDIT — FAIL (2 blockers, minimal fixes)
Box-only read; not full XSD, not compiled, not tested in game. Phase 1 not complete.

## Package
- 249071 B, sha256 `38856a1d8d3bfc6c1f6b25ffd376c89cd1021fc3f611f8f1d962ab77d95338a2` match; saved `batch48.tar.gz`; safe paths.
- vs 47_FIX: new 1 `Allied/Structures/AlliedStatueOfLiberty.xml`, changed 3, 90 identical. 94 XML parse; Mod 93 all + 3 ref (+1 include); id unique.
- Command `Command_ConstructAlliedStatueOfLiberty` CONSTRUCTION_YARD_CONSTRUCT → AlliedStatueOfLibertyBuildable. AlliedConstructionYardCommandSetBase 15→16, AlliedCraneCommandSet 14→15, appended after RushmoreLaserHead, old order kept. New_York.xml not included; S09 original untouched.

## Diff vs SDK NY_Liberty.xml (whitespace-insensitive)
Only: root +xmlns:xai; ART includes NY_Liberty.W3X / NY_LibertyBase.W3X and commented YU line removed; +GlobalDefines; id/EditorName; Side Allies; +BuildTime 20, EnergyProduction 0, Max 1, OTHER_STRUCTURE ×2; +ObjectResourceInfo 2000 ORE. Everything else verbatim (DisplayName Replace, UI fields incl. HealthBoxHeightOffset -400, Draw + 20 bones, Physics, BuildingDestruction/AlliedBarracks_Debris, FXList Replace, CreateObjectDie OCL + DestroyDie, xi engineer/repair, AI idle NO, Body ModuleTag_Body MEDIUM, 7 BOX + offsets, audio, OCL/collapse include). No unpack.

## BLOCKER 1 — KindOf: NOT_AUTOACQUIRABLE not removed (real omission)
Package `KindOf="+AUTO_ACQUIRABLE_BY_AI"` (= original). Parent BaseCivilianStructureNoGarrisonDestructible L12 KindOf contains `NOT_AUTOACQUIRABLE`. Doc L697: "新对象须去掉 NOT_AUTOACQUIRABLE 并加 AUTO_ACQUIRABLE_BY_AI".
Fix: `KindOf="-NOT_AUTOACQUIRABLE +AUTO_ACQUIRABLE_BY_AI"` (package Kremlin L14 precedent).

## BLOCKER 2 — element order
`<ObjectResourceInfo>` is placed before `<DisplayName>`. AssetTypeGameObject.xsd L385-389 is an xs:sequence: DisplayName, DisplayNameTransformed, GameDependency, …, ObjectResourceInfo.
Fix: move the ObjectResourceInfo block to directly after `</DisplayName>` (before `<Draws>`).

## Body — retraction of my B47_FIX research claim
AssetTypeGameObject.xsd L301-303: `BodyModule` = `xs:choice minOccurs=1 maxOccurs=1`; L403 Body maxOccurs 1. Body is a single slot, so the child's ActiveBody replaces the parent's whatever the id. Keeping `ModuleTag_Body` + `=$CIV_HEALTH_MEDIUM` (3000) is correct. My "two Body" claim was wrong.

## Risks/tests (unchanged)
ART W3X resolved by name in build (ART includes removed by permission) + collapse COL via instance include → native build log; footprint ~270×278; perf; UI assets; counts for defeat.

Next-item research (clone center / quick production) deferred until 48_FIX passes, per instruction. Guard02 untouched.
