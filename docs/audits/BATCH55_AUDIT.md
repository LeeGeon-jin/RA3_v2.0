# BATCH55 AUDIT — FAIL (LogicCommandSet.xml only)
Source check only. No full XSD, compile or in-game test. A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## Package — OK
256262 B, sha256 4c773fd6…4935c match; all entries under data/, safe paths; 102 XML parse; Mod 101 all + 3 ref.
vs 54: new AirportTechStructureBuildable.xml (222 lines) + Mod/LogicCommand/LogicCommandSet changed; other 98 byte-identical.

## Blocker — LogicCommandSet.xml re-serialized
- The whole file was rewritten by an ElementTree-style serializer: root `<ns0:AssetDeclaration xmlns:ns0="uri:ea.com:eala:asset">`, every element `ns0:`-prefixed, quotes in the XML declaration changed, no final newline.
- The 5 new entries are bare `<Cmd>…</Cmd>` with **no namespace** (parsed tag `Cmd`, not `{uri:ea.com:eala:asset}Cmd`), each glued to the closing tag. Schema-wise these are foreign elements → expected to be rejected or ignored.
- Even the prefixed form is unproven with EA tools; every SDK/package file uses the default namespace.
- Counts would have been right (20/19/25/23/23, appended, old order kept), but the content is not acceptable.

**Minimal fix:** start from the Batch54 LogicCommandSet.xml byte-for-byte and insert just one line before each of the five closing tags, same tab style as the existing Cmd lines:
- AlliedConstructionYardCommandSetBase: `Command_ConstructAlliedAirportTechStructure`
- AlliedCraneCommandSet: `Command_ConstructAlliedAirportTechStructure`
- JapanConstructionYardCommandSet: `Command_ConstructJapanAirportTechStructure`
- SovietConstructionYardCommandSet: `Command_ConstructSovietAirportTechStructure`
- SovietCraneCommandSet: `Command_ConstructSovietAirportTechStructure`
Expected diff vs 54: +5 lines, nothing else. Do not use an XML library to re-serialize.

## Other changes — source OK (recheck after the fix)
- Mod: +1 include (all). LogicCommand: +3 CONSTRUCTION_YARD_CONSTRUCT → Allied/Soviet/JapanAirportTechStructureBuildable, default namespace, fine.
- Airport diff -w vs SDK, limited to:
  - +xai; the two ART all includes removed; BaseTechStructure include kept twice as in the SDK; YU_HotelDebris / Collapse kept; +GlobalDefines.
  - Allied: id/EditorName, Side Allies, BuildTime 15, MAIN_STRUCTURE queue + placement, cost literal 1000.
  - OCL renamed in both places; body verbatim (NUAirportTechStructure_Collapse).
  - Soviet: BuildTime 0 + ModuleTag_StructureUnpackUpdate 15s. Correct: the real parent BaseTechStructure has a StructureUnpackUpdate with this id and UnpackTime 0 (see the grep below), so this overrides it; "no such module" is wrong. Japan inherits BuildTime 15.
  - Verbatim: KindOf +DONT_UNATTACH_WHEN_HEALING, StructureArmor, UI, model + RUBBLE, all bones, "no anim", flag xi, 2% -1 NonStackable AIRCRAFT VEHICLE HUGE_VEHICLE ALLIES AIRBORNE_TARGET, engineer/repair xi, Lua, DestroyDie, Body 3000/3000, 4 BOX, vision, ProjectedBuildabilityInfo.
- **Duplicate BaseTechStructure include:** the SDK original has it, but I know of no natively verified build of a package object with a duplicate include → *to verify in native build*. Not a blocker.
- No build animation or dust added; map AirportTechStructure untouched.
- **Paradrop:** not in this batch. It is still pending as a whole, not cancelled by the user. Calling the main assistant's split instruction "user explicitly won't do it" misstates it.
