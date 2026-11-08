# BATCH55_FIX AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
**Natively unverified:** no full XSD, compile or in-game test. A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## Source checks (passed)
- **Package:** copied from asset 01M6W8R65D4F555SYFV27PMM06.gz. 256212 B, sha256 f0aaaf37…12dd7908 match. All entries under `data/`. 102 XML parse; Mod 101 all + 3 ref.
- **vs 55:** only `GlobalData/LogicCommandSet.xml` differs; other 101 byte-identical, so the Batch55 airport, Mod and LogicCommand source checks carry over unchanged.
- **vs 54:** exactly +5 lines (L47, 70, 116, 145, 172), each `\t\t<Cmd>…</Cmd>`, placed last in its list. Declaration, default namespace, indentation, line endings and trailing byte are identical.
- **Parsed:** root `{uri:ea.com:eala:asset}AssetDeclaration`; 128 `{uri:ea.com:eala:asset}Cmd`, 0 bare `Cmd`. The file has 174 *lines*, not 174 Cmds: the cloud's figure is a line count.
- **List lengths:** Allied CY 20, Allied Crane 19, Japan CY 23, Soviet CY 25, Soviet Crane 23. Old order kept.
- **Command → object:** each of the 3 commands is CONSTRUCTION_YARD_CONSTRUCT → Allied/Soviet/JapanAirportTechStructureBuildable. All three objects exist in AirportTechStructureBuildable.xml.

## To verify natively
- The duplicate BaseTechStructure include, kept from the SDK original.
- Placement of the large 4-box footprint, Soviet 15 s unpack, airborne repair, Lua hook, engineer recapture, ART resolution.

Paradrop is not done and still pending as a whole; it was not cancelled by the user. Oil derrick: not explicitly decided, not done.
