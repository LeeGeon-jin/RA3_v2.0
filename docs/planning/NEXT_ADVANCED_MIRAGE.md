# NEXT — Advanced Mirage Tank (AlliedAdvancedMirageTank) + three re-checked items + Kirov crash value
2026-11-08 22:19 UTC+10. Read-only. Base package: 88FIX. The object does **not exist** in the package; it is a new file. The veteran Mirage is not the advanced Mirage.

## 1. Advanced Mirage — user-settled values (devdoc L10–L14, L586/L589 ③④⑥⑦; user 22:14 "移动速度和幻影坦克相同")
New file `Allied/Units/AlliedAdvancedMirageTank.xml`, a copy of SDK `Allied/Units_Campaign/CAMP_A08_SpecialMirageTank.xml` (inheritFrom AlliedAntiVehicleVehicleTech3).

### Changes from CAMP_A08
| Field | CAMP_A08 | New |
|---|---|---|
| id | A08_SpecialMirageTank | AlliedAdvancedMirageTank |
| EditorName | A08_SpecialMirageTank | AlliedAdvancedMirageTank |
| EditorSorting | (as in file) | UNIT |
| Side | — | Allies |
| LocomotorSet | AlliedAntiVehicleVehicleTech3Locomotor, Speed 20.0 | **same locomotor, Speed 80.0**. This is the normal Mirage value (SDK L54–58: same locomotor id + Speed 80); it is not set on the locomotor itself. |
| BuildCost | — | 1500 (same as the package Mirage) |
| BuildTime | — | 15 |
| GameDependency | — | RequiredObject AlliedTechStructure |
| KindOf | — | add T3_UNIT; keep MOVE_FOR_NOONE and everything else |
| ButtonImage | Button_AlliedMeerageTank | Button_AlliedAntiVehicleVehicleTech3_on |
| SelectPortrait | Portrait_AlliedMeerageTank | Portrait_AlliedAntiVehicleVehicleTech3 |
| Invisibility UpdatePeriod | 0.01s (L229) | 0.2s (L12) |
| DisplayName | — | Name:AlliedAdvancedMirageTank |
| Description / TypeDescription | — | Desc:AlliedAdvancedMirageTank / Type:AlliedAdvancedMirageTank. The text is fixed in devdoc L589 ⑥. |

### Kept as in CAMP_A08
- MaxHealth 2000; vision 200/200; BroadcastRange 225; A08 invisibility template.
- A08 field sounds (L12 "不需要换").
- NON_AUTOACQUIRABLE toggle status; crusher 30/20.
- UnitAIStateMachine; FAKE model draw; cloaking-field draw.

### Build button
- New LogicCommand `Command_ConstructAlliedAdvancedMirageTank`, copied from SDK LogicCommand L449 Command_ConstructAlliedAntiVehicleVehicleTech3.
- Add it to AlliedWarFactoryCommandSet right after the Mirage.

### Move-fire
Inherited from the R89 weapons. No unit-side change.

### Model loading (static evidence)
- CAMP_A08 is loaded only through `MapSpecific.xml` L14 → `Allied/AlliedMapSpecific.xml` L20, so skirmish never sees it.
- Its art includes are:
  - `ART:AUAntiVehicleVehicleTech3_FAKE.w3x` (instance)
  - `ART:AUAntiVehicleVehicleTech3_IDLZ.w3x` (instance)
  - `ART:EX_Headlights.w3x` (instance)
  - `ART:EXCloakingField.w3x` (all)
- **Removing ART includes is not a hard rule.** It only applies to assets the global/static streams already provide. The package already loads campaign-only models with ART includes:
  - `<Include type="all" source="ART:AM_AlliedFutureTechHQ.W3X"/>` in the three QuickProductionCenter files;
  - `ART:GE_SovietVIPBunkerSubStructure.W3X` in SovietCloningCenter.
- **Required, do not strip:**
  - `<Include type="all" source="ART:AUAntiVehicleVehicleTech3_FAKE.w3x"/>`
  - `<Include type="all" source="ART:AUAntiVehicleVehicleTech3_IDLZ.w3x"/>`
  - Using `all` rather than `instance` follows the quick-production-center precedent: the asset has to be emitted into the mod stream because no skirmish stream contains it.
- **Can be omitted:**
  - EX_Headlights: already used by global Allied units (e.g. AlliedAntiAirVehicleTech1 includes it).
  - EXCloakingField: already included `all` by the normal Mirage (SDK unit L16).
  - The normal Mirage's own ART is global.
- **Keep the inheritance include:** `<Include type="instance" source="DATA:Allied/Units/AlliedAntiVehicleVehicleTech3.xml"/>`.
- **Mod.xml:** add one `type="all"` include for the new file, giving 140 XML. Do not add MapSpecific.
- **Non-ART dependencies (all global):**
  - InvisibilityTemplates.xml (A08 template), loaded from Static.xml;
  - A08 sounds in Sounds/SoundEffects.xml, via MasterAudioEvents;
  - SpecialPower_ToggleMirageField (normal Mirage);
  - Mirage portrait/button.
- **Not statically provable:**
  - The SDK on this box has no official w3x art (Art/ holds only 5 sample folders). Whether the build machine's ART path has AUAntiVehicleVehicleTech3_FAKE/IDLZ, and their texture dependencies, only shows up at native compile. The same is true of the existing AM_AlliedFutureTechHQ.
  - New string keys: the package has no string file, so all new Name:/Desc: keys share the same unresolved display issue. Not specific to this unit.
  - Runtime (L1597): FAKE model stacking with the inherited Mirage draw, the tree-disguise look.

Refs: advanced_mirage_sdk_refs.tar.gz (17142 B, sha256 f1122039…c7f6).
- SDK: CAMP_A08, AlliedMapSpecific, MapSpecific, normal Mirage, InvisibilityTemplates, Kirov, Kirov_Dying.
- Package: Mirage unit, QuickProductionCenter (ART precedent), LogicCommand, LogicCommandSet, Mod.xml.

## 2. Re-checked "decisions" — none needs the user
- **Japanese Rushmore head:** **not direct placement.**
  - devdoc L788: JapanRushmoreLaserHead + core JapanRushmoreLaserHeadEgg, "核心时间 + 展开时间合计 30 秒". The ch.7 test L1605 also says "帝国核心 + 展开合计 30 秒", prerequisite JapanTechStructure, confirmed.
  - Direct placement was decided only for the quick production center, tech buildings and decor (L263/L30/L6), not Rushmore.
  - The split is technical. Use the devdoc example 5 + 25: the core uses the original defence-egg precedent (JapanBaseDefenseAdvancedEgg BuildTime 5), and the total stays 30 as decided.
- **Tech-airport paradrop button:**
  - The user specified "像超级武器一样点击" plus a 9-minute countdown (L398), but no button location. L1601 says to decide after testing.
  - Minimal choice within scope: option B (L401), the button on the airport's own command set with a superweapon-style countdown. The protocol panel is fixed-slot, which is a risk. Revisit only if testing fails.
- **RA2-style Allied build range:**
  - devdoc L466–L470: add ProjectedBuildabilityInfo to the Allied buildings, "苏军普通建筑原版就有这个节点…正是原理". So use the Soviet equivalents.
  - Radii:

| Building | Radius |
|---|---|
| PowerPlant | 180 |
| Barracks | 195 |
| Refinery | 180 / 195 |
| WarFactory | 240 |
| NavalYard | 240 / 255 |
| Airfield | 270 |
| TechStructure | 210 |
| SuperWeapon(s) | 180 / 165 |

  - All with BuildPlacementTypes "MAIN_STRUCTURE OTHER_STRUCTURE". Defences/walls are 0 in the Soviet data, so they get none.
  - Allied CY 600 and Outpost 390 are unchanged.
  - Not a design change. The performance note is in L1565.

## 3. Kirov boost + crash (L845/L849; both required, boost alone is not enough)
### Crash
- SDK chain: SovietBomberAircraft L290 SlowDeath OCL SUBomberAircraft_Dying_OCL → SovietBomberAircraft_Dying.xml L89–95 FireWeaponWhenDead `SovietBomberAircraftDeathWeapon`.
- Current values: Damage 500, Radius 50, DamageTaperOff 200, EXPLOSIVE, allies ×50%; MetaImpact 50/50.
- One bomb = `SovietBomberAircraftBombWarhead`: Damage 400, Radius 50, TaperOff 0, EXPLOSIVE. The Kirov drops 1 per clip (SovietBomberAircraftBombWeapon ClipSize 1).
- **Five bombs = Damage 2000** (5×400). This is exact.
- Radius: devdoc L845 explicitly says "威力**和范围**相当于五颗炸弹", and the L848 risk note says "坠毁爆炸范围较大，留意…性能". So the document asks for a larger range too, but gives **no number**. 112/250 are my calculations, **not user-approved**.
- Minimal implementation without widening the agreed scope (inferred): Damage 500→2000; Radius 50 / TaperOff 200 / MetaImpact unchanged. This leaves the "范围" part open; it needs a user number before it can count as done.

### Boost
- Original:
  - SpecialPower_ToggleAfterburners: toggle, no ReloadTime.
  - The ON state triggers ModuleTag_Afterburners + ModuleTag_LoseHealthUpdate (DamagePerSecond 200).
- Target: 10s timed, 30s cooldown, no health drain.
  - Remove the LoseHealthUpdate module trigger from the toggle state.
  - Add the timed and cooldown behaviour with ReloadTime 30s, using the precedent pattern SpecialPower_JapanEngineerSprint (ReloadTime). The exact module for auto-off after 10s needs its own short research before R94.
