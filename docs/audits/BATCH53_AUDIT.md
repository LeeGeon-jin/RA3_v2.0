# BATCH53 AUDIT — FAIL (packaging only; content passes)
Source check only; not full XSD, not compiled, not tested. Phase 1 not complete.

## BLOCKER — archive layout changed
- batch1…52 tars are rooted at `data/` (`data/Mod.xml`, `data/Allied/...`). Batch53 is rooted at `./` (`./Mod.xml`, `./Allied/...`) — **no `data/` directory**. Extracting over the cumulative tree or feeding the existing build layout (`DATA:` paths resolved under `data/`) would put files in the wrong place / drop the mod root. Not a path-safety issue (no absolute/`..`), but the delivery is not drop-in compatible with every previous batch.
- Probably also why the tar is ~5 KB smaller (different entry names/order + compression), not a content loss: content comparison below is complete.
- **Minimal fix:** repack the same 100 files under `data/` (e.g. `tar czf ra3v2_phase1_batch53_fix.tar.gz data/`), no content changes.

## Content (compared b84/data vs batch53 root) — would PASS
- 255146 B, sha256 `dc6677d4d3d9cda1cfa3277210fb2a94cf50dd0e7f47fdcb79ea39f627c03798` match; saved `batch53.tar.gz`.
- New 1 `Neutral/Structures/GarageTechStructureBuildable.xml` (291 lines); changed 3 (Mod +1, LogicCommand +3, LogicCommandSet +5); other 96 byte-identical (hospital/landmarks untouched). 100 XML parse; Mod 99 all + 3 ref.
- Commands: 3 × CONSTRUCTION_YARD_CONSTRUCT → Allied/Soviet/JapanGarageTechStructureBuildable; list ends: Allied CY 18, Allied Crane 17, Soviet CY 23, Soviet Crane 21, Japan CY 21.
- diff -w vs SDK GarageTechStructure.xml, only: +xmlns:xai; ART all removed (AutoPartsStoreTechStructure.w3x, ABBarracks_particles.w3x); instance BaseTechStructure / YU_HotelDebris / GarageTechStructure_Collapse kept; +GlobalDefines; id/EditorName; +Side Allies, BuildTime 15, ProductionQueueType MAIN_STRUCTURE (attribute → no element-order issue), BuildPlacementTypeFlag MAIN_STRUCTURE; cost literal 1000; OCL renamed `NUGarageTechStructureBuildable_Die_OCL` in both CreateObjectDie CreationList and the OCL id — OCL body (creates GarageTechStructure_Collapse) verbatim.
- All else verbatim: KindOf +DONT_UNATTACH_WHEN_HEALING, ArmorSet, flag draw xi, PassiveAreaEffect -1 / 2% VEHICLE HUGE_VEHICLE, engineer/repair xi, LUAEventList, death/collapse, MaxHealth 3000, all geometry shapes, vision 100/200, ProjectedBuildabilityInfo Radius 0.
- Soviet inherit: BuildTime 0 + `ModuleTag_StructureUnpackUpdate` 15s; Japan inherit (15, MAIN). No animation/FX/flags/power/limit changes. Map GarageTechStructure untouched.
- Cross-stream duplicate-id risk: avoided here by the OCL rename; for hospital/landmarks still only an inference, not proven.

Next-item research deferred until the repacked 53_FIX passes.
