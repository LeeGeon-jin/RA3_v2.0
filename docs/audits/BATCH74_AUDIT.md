# BATCH74 AUDIT — FAIL (not buildable): object correct, command chain missing
No full XSD, compile or in-game test. Phase 1 not complete.
The cloning center and quick production center are **not implemented** (no files). Not counted as done.

## Package
- 295875 B, sha256 6e68223a…0d7cbf8 match. All entries under `data/`. 119 XML parse.
- Mod: 3 reference / 117 all.
- vs 73FIX:
  - new `Japan/Structures/JapanStatueGuard02.xml`;
  - Mod +1 (L110, between Guard03 L109 and Guard01 L112);
  - the other 117 files are byte-identical, **including LogicCommand.xml and LogicCommandSet.xml**.

## Defect (blocking): Guard02 cannot be built
- `JapanStatueGuard02Buildable` is referenced **nowhere** except its own file and Mod (`rg` over all 119 XML).
- No LogicCommand constructs it, and no LogicCommandSet lists it.
- The siblings are wired in:
  - LogicCommand.xml L116-120 `Command_ConstructJapanStatueGuard01` (Type CONSTRUCTION_YARD_CONSTRUCT, `<Object>JapanStatueGuard01Buildable</Object>`), and likewise Guard03 (L97-99);
  - the Japan construction-yard CommandSet lists them at LogicCommandSet.xml L112 (Guard03) and L114 (Guard01). That is the only set containing them.
- **Minimal fix** (plain text insert, no XML re-serialization, default asset namespace):
  1. LogicCommand.xml, after the Guard01 block (L120):
     ```
     <LogicCommand
         id="Command_ConstructJapanStatueGuard02"
         Type="CONSTRUCTION_YARD_CONSTRUCT">
         <Object>JapanStatueGuard02Buildable</Object>
     </LogicCommand>
     ```
  2. LogicCommandSet.xml: in the same set, add `<Cmd>Command_ConstructJapanStatueGuard02</Cmd>` next to L114 (Guard01). That set's Cmd count +1; no other set.
  3. Expected: 119 XML / Mod 117; 2 command files change; the other 117 files are identical to 74.
- **No prerequisite:** the object has no GameDependency (same as Guard01/03) → buildable without prerequisites once the command exists. This matches the user's "无前置条件" (devdoc L6 / L1086).

## Object review (vs SDK TH_StatueGuard02 and the Guard01 precedent)
- **The file is the Guard01 conversion with only:**
  - the id / EditorName;
  - Model `TH_StatueGuard02`;
  - Geometry → the real SDK Guard02 shape (BOX 9.0 / 9.0 / 44.0, offset -0.143921 / -0.225959 / 0.0, ContactPointGeneration STRUCTURE). Values identical to the SDK TH_StatueGuard02 Geometry.
  - Plus an encoding / indent / comment difference.
- **Matches the user (L6 / L1086):** cost 1000, BuildTime 10, EnergyProduction 0, Side Japan, ProductionQueueType / BuildPlacementTypeFlag OTHER_STRUCTURE like Guard01, no aura, no prerequisite.
- **HP:** ActiveBody MaxHealth 2000 (user decision 02=2000).
  - The SDK original is a PropBody without HP (HP_SOURCE_AUDIT_R74), so the conversion to ActiveBody is required. The doc L1089 says Guard01/02 copies "须改成建筑体（带 ActiveBody…）".
- **Draw:** `ScriptedModelDraw / ModelConditionState(PARSE_DEFAULT) / Model Name` is the correct schema nesting (Model is a child of ModelConditionState, as in SDK ScriptedModelDraw objects, e.g. AlliedTankShell_Large).
  - The empty `AnimationState PARSE_DEFAULT` is allowed (ScriptedModelDraw.xsd L68 minOccurs 0; same as Guard01).
- **Removed DynamicsDraw (11 BoneVolumes) + ToppleUpdate:** these are prop-physics debris pieces and topple-on-crush. They are not usable on a structure body and are consistent with the doc's "改成建筑体". Not a fidelity loss of the building model.
- **Kept:** FXListBehavior onDeath FX_RockCrush_AudioOnly and SlowDeath (1.5 s / 4 / 8 s) from the SDK prop. ArmorSet NoArmor (prop parent value) replaces the structure parent's armor via `xai:joinAction="Replace"` with id DefaultArmor (same as Guard01).
- **Parent:** BaseCivilianStructureNoGarrisonDestructible (instance include); `KindOf="-NOT_AUTOACQUIRABLE"` (attackable / auto-acquirable, same as Guard01).

## Notes (pre-existing, shared with Guard01/03 and the other decorative buildables — not new in 74)
- **`MaxSimultaneousOfType="1"`:** the user's Japanese-decor wording (L6, L1086) gives cost/time/power/prerequisite only, with no "只能造一个".
  - That phrase is from the 11-06 answer for the Liberty/Kremlin/Heroes/clone/quick-production group (L34).
  - The limit was set on all Japan decor in earlier batches. Guard02 is consistent with them, but the source for Japan decor is a precedent, not a user statement → flag to the user/parent. Not changed here.
- **No ART include** for `TH_StatueGuard02.w3x`, which is the package convention for all decor buildables. The doc (L1569 / L1571) warns civilian models are only loaded via WorldBuilder → **in-game check for an invisible model**.
- **No ButtonImage / DisplayName** (same as Guard01/03) → the build button may show no icon or name. UI check.

## Cloning / quick production center facts (for the parent; nothing implemented)
- **User's latest choice:** HP = battle lab.
- **SDK:** SovietTechStructure ActiveBody `MaxHealth="2000.0"` (Soviet/Structures/SovietTechStructure.xml L445); AlliedTechStructure `MaxHealth="2000.0"` (L435); JapanTechStructure 2000.0 (L804). The package's AlliedTechStructure is also 2000.
- The cloud's "2000" is correct. The two centers still have no object files → open work, not done.
