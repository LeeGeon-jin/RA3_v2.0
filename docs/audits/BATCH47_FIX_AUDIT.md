# BATCH47_FIX AUDIT — SOURCE PASS (native-compile candidate)
Box-only read; not full XSD, not compiled, not tested in game. Phase 1 not complete.

- 247632 B, sha256 `e3907fcd6eac0ee6c8b7d4f05d04fbf52d14b943c9e1e58574e99c69777efbfc` match; saved `batch47_FIX.tar.gz`; safe paths.
- vs 47: only `Japan/Structures/JapanStatueGuard01.xml` differs: ArmorSet + `id="DefaultArmor"` + `xai:joinAction="Replace"`, comment line updated. Other 92 files byte-identical. 93 XML parse; Mod 92 all + 3 ref.
- Effective armor: parent `BaseCivilianStructureNoGarrison` `DefaultArmor` StructureArmor replaced → single set NoArmor (precedent MR_RushmoreFiringBase L24-27). root has xmlns:xai.
- All B47 pass items unchanged (Draw, geometry, FXList Replace, SlowDeath, Body 2000, flags, no xi/UI/bones/BuildingDestruction, command, Mod).
- SlowDeath: the original TH local `ModuleTag_Death` (ALL) and the prop parent's `ModuleTag_SlowDeath` (TOPPLED) have different ids and never override each other. The TOPPLED one disappears only because the parent changed.
- **Correction to BATCH47_AUDIT:** I wrote Japan CY 19→20. Recount (Cmd elements only): b76 = 18, b78 = 19 → **18→19**; earlier count wrongly included a header line. Append at end, old order intact.
- Pending/test: ART include of TH_StatueGuard01.w3x not carried (Guard03 pattern) → native build log; NoArmor fragility; small footprint.
