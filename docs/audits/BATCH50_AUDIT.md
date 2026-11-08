# BATCH50 AUDIT — SOURCE PASS (native-compile candidate)
Source check on the real tar only. Not full XSD, not compiled, not tested in game. Phase 1 not complete.

## Package (real tar, not the notice attachments)
- 259704 B, sha256 `f52285244621175409eb5ace33c7db1d67e45b9e861f87ec079e7c4f5dbd4bbd` match; saved `batch50.tar.gz`; safe paths.
- vs 49: new 1 `Japan/Structures/JapanConstructionYard.xml` (**671 lines, 20316 B — full file, not a 943 B patch**), Mod.xml +1 include (`DATA:Japan/Structures/JapanConstructionYard.xml`; real Mod differs from 49, so the 10871 B attachment was not the packaged file). Other 96 files byte-identical. 98 XML parse; Mod 97 all + 3 ref. id `JapanConstructionYard` (original), defined once.

## Node diff vs SDK (diff -w): only
1. L657 existing ProjectedBuildabilityInfo 480/465: `OTHER_STRUCTURE` → `MAIN_STRUCTURE OTHER_STRUCTURE`.
2. Appended second ProjectedBuildabilityInfo = Soviet L574-585 verbatim (600/585, MAIN_STRUCTURE OTHER_STRUCTURE, AllowedBuildabilityHeightVariation -1.0, AllowedObjectFilter Rule NONE + AlliedNavalYard/SovietNavalYard/JapanNavalYard).
Everything else identical (ART includes kept, all instance/xi includes, Draws, Behaviors, AI, Body, Geometry, VisionInfo 100/1000, CommandSet).

## Schema / merge
- AssetTypeGameObject.xsd L422: ProjectedBuildabilityInfo `maxOccurs="unbounded"`, last in sequence → two nodes legal, same position as Soviet CY.
- File is a full override of the same id (not inheritance) → no list-merge issue; both rings are local.
- `CommandSet="JapanConstructionYardCommandSet"` unchanged → still uses the package's modified set (19 cmds incl. decorations/Guard01). Consistent.

## Test only (not verified)
Placement of MAIN_STRUCTURE buildings in 480×465; naval ring effect for Japan; campaign building copies untouched by decision.
