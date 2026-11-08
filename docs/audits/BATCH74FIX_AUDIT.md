# BATCH74FIX AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Phase 1 not complete. Not claimed that Guard02 works fully in game.
The cloning center and quick production center are still not implemented.

## Package
- 295875 B, sha256 faa33281…4177a20655 match. All entries under `data/`. 119 XML parse.
- Mod: 3 reference / 117 all.

## vs 74 (3 files; the other 116 byte-identical)
- **JapanStatueGuard02.xml:** only L18 `MaxSimultaneousOfType="1"` deleted.
- **LogicCommand.xml:** a new block after Guard01 (L121-125) `Command_ConstructJapanStatueGuard02` Type CONSTRUCTION_YARD_CONSTRUCT `<Object>JapanStatueGuard02Buildable</Object>`. The id is unique (1 occurrence).
- **LogicCommandSet.xml:** +1 `<Cmd>Command_ConstructJapanStatueGuard02</Cmd>` at L113, in the Japan construction-yard set between Guard03 (L112) and the Fuji tower; Guard01 is now at L115.
- **Namespace:** all elements of both command files are in the asset namespace (0 non-namespace elements). Total Cmd count 136 (+1).

## Chain
Mod L110 → object id → command `<Object>` → Japan CY CommandSet. All references hit.

## Cumulative vs 73FIX
- new Guard02 file + Mod +1 + 2 command files only;
- other 116 files are identical to 73FIX, so no earlier parameter was touched.

## Guard02 values kept
- MaxHealth 2000, cost 1000, BuildTime 10, EnergyProduction 0, no GameDependency (no prerequisite), now no build limit.
- Geometry / Draw / FX / SlowDeath as in 74.

## Runtime risks (unchanged, not tested)
- No ART include for TH_StatueGuard02.w3x → possible invisible model.
- No ButtonImage / DisplayName → blank build button.
- Buildability, attackability and death behaviour are not tested in game.
