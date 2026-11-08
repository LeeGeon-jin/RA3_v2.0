# BATCH92 AUDIT — STATIC FAIL (1 blocking defect), 2026-11-08 22:48 UTC+10
## Package
- batch92.tar.gz = store handoff/RA3_V2.0_Batch92_SovietSpy.tar.gz. 351636 B, sha256 c15bae9b6055c61da7a67b781d69cbe5359ae645782eb093c74b7edb1070b8bd. Matches; the host asset is identical.
- Root is data/. 142 XML. Mod.xml: 139 type="all" + 3 reference.
- vs 91: 3 new files plus 4 modified files (LogicCommand, LogicCommandSet, SpecialPowerTemplates, Mod). The other 135 files are byte-identical. All 142 files parse as well-formed XML.

## BLOCKING (FAIL)
1. **Mod.xml L145: `<Include type="all" source="DATA:Includes/InfantryFighting/IF_SecondaryObjectListener.xml" />` is wrong.**
   - The file's root is `<SecondaryObjectListenerModule>`, a module fragment meant for `xi:include`. It is not an `<AssetDeclaration>`.
   - In the SDK all 774 `<Include>` targets have an AssetDeclaration root, and this file is never `<Include>`d anywhere. It is only consumed through xi:include (package AlliedAntiAirVehicleTech1 L726, AlliedBaseDefense L573).
   - Fix: delete that one Mod.xml line and keep the file at data/Includes/InfantryFighting/. Whether the package copy takes precedence over the SDK copy for xi:include stays a compile-time check.

## Should fix (compile risk, not proven)
2. ExperienceLevels_SovietSpy.xml has no `<Includes>`.
   - Its 4 templates use inheritFrom ExperienceLevel_SovietRank1–4. Those exist (SDK ExperienceLevels L93–L102) but live in the Static stream.
   - SDK and package inheritFrom convention: the parent's file is pulled in by an instance include (e.g. units do `Include type="instance" BaseInfantry`).
   - Recommended: add `<Includes><Include type="instance" source="DATA:GlobalData/ExperienceLevels.xml"/></Includes>`. Otherwise the parents may not resolve at compile.
   - Values and chain are otherwise correct: Required 1/3000/6000/9000, Award 1000–4000, Prerequisite chain _1→_4, Target SovietInfiltrationInfantry. The Allied templates are untouched.
3. Hotkey "select spies" group: SDK UIInGame/UIComponentObjectSelector.xml L61–64 ShortcutObjects lists JapanInfiltrationInfantry and AlliedInfiltrationInfantry. **The package has no copy, so the Soviet spy is not in the group.** This is a parity gap. Cloud did not mention it.

## Verified OK
- **SovietInfiltrationInfantry.xml vs b91 AlliedInfiltrationInfantry.xml, the complete diff:**
  - id;
  - Side Allies→Soviet;
  - EditorName / Description / TypeDescription / DisplayName;
  - RequiredObject AlliedWarFactory→SovietWarFactory;
  - L844 ThingToSpawn → SovietInfiltrationInfantry.
  - Nothing else differs: 1000 / 8, KindOf, armor, weapons, Draws including ParachuteDrawAllied xi:include, all modules and includes are kept.
  - One definition only. The Allied spy file is unchanged.
- **Cloning:**
  - SovietBarracks ProductionUpdate GiveUpgradeToProduced translates Upgrade_SovietCloning → Upgrade_CloneMe with no object filter, so it applies to every produced unit, the new spy included.
  - The cloning center provides Upgrade_SovietCloning by ownership.
  - The spy's ObjectCreationUpgrade (TriggeredBy Upgrade_CloneMe) now spawns a Soviet spy.
  - Cloning center MaxSimultaneousOfType=1 kept.
- LogicCommand: +Command_ConstructSovietInfiltrationInfantry (UNIT_BUILD, Object exists). Single definition.
- LogicCommandSet: +SovietBarracksCommandSet = SDK L375–382 identical + the new command at the end. Single definition.
- SpecialPowerTemplates: +ExcludeThing SovietInfiltrationInfantry in the bribe filter (additive only).
- IF_SecondaryObjectListener.xml = SDK copy + one IncludeThing in the Allied-spy golden-gun tuple. Everything else is identical.
- Earlier batches kept: R89 / R90 Weapon.xml and R91 Tesla are byte-identical to 91, normal mirage Speed 80, advanced mirage not created.

## Runtime unproven
Production, disguise and bribe on the Soviet side, cloning, rank display, IFV golden gun, voices, AI. Compile.

**Verdict: static FAIL. Fix #1 is required. #2 and #3 are recommended in the same fix batch.**
