# BATCH60 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 285530 B, sha256 3955d1c4…e698ef match. All entries under `data/`. 111 XML parse; Mod 110 all + 3 ref.
- vs 59: LogicCommandSet, JapanBaseDefenseAdvanced, Mod changed; +JapanAntiStructureVehicle.xml; other 107 files byte-identical.
- **Mod:** +1 line (L106).

## Diffs (real lines)
- **Tower vs 59:** `diff -w` = only L936-939 deleted (PrematureDischargeSpecialPower `ModuleTag_FireKiCannonSpecialPower` + blank line). The next `<StructureUnpackUpdate` line lost one tab (whitespace).
- **Tank vs SDK:** 602 lines vs SDK 605. `diff -w` = only SDK L479-481 deleted (same module, SpecialPower_JASV_FireKiCannon). The adjacent `</WeaponSetUpdate>` / `<Physics` lines lost a tab (whitespace). Same id; every include (14 Include lines, same as SDK), Draw, weapons/charge, geometry, other modules kept.
- **LogicCommandSet vs 59:** +10 text lines appended:
  - `JapanBaseDefenseAdvancedCommandSet` (empty);
  - `JapanAntiStructureVehicleCommandSet` = Command_AttackMove, Command_MoveToPositionAndCollect (SDK order minus FireKi).
- **Parsed:**
  - 135 `{uri:ea.com:eala:asset}Cmd`, 0 bare.
  - 13 sets, no duplicate id in the package.
  - CY lists unchanged: Allied 21, Crane 20, Japan 24, Soviet 26, Crane 24.
- **References hit:** tank CommandSet="JapanAntiStructureVehicleCommandSet" (L55); tower CommandSet="JapanBaseDefenseAdvancedCommandSet" (L21).
- No `Premature` anywhere in the package.
- LogicCommand, SpecialPowerTemplates and UI are unchanged; the orphaned commands are harmless.

## Native test
- Override of SDK sets by same id; empty set precedent: SDK JapanNavalYardRepairBayCommandSet.
- Normal charge-and-fire on tower and tank; no F button; AI without errors.
