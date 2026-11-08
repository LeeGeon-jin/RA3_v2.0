# NEXT R93: Kirov (SovietBomberAircraft) boost, 10s auto-end / 30s cooldown / no health drain. Base: b89. Read-only spec, 2026-11-08 UTC+10
## User-fixed (devdoc L845/L849)
- "加速持续10秒，技能冷却30秒，不掉血，反复使用".
- The crash ("五弹") is a **separate pending item**, not part of R93. Damage 2000 is certain; the range has no user number (the 112 candidate is with the user and not decided).

## SDK chain today (b89 = SDK + cost 2000 / 20s + ART includes stripped)
| Piece | Where (b89 Kirov file unless noted) | What it does |
|---|---|---|
| CommandSet | SovietBomberAircraftCommandSet (SDK LCS L604) | Command_AttackMove + Command_ToggleAfterburners |
| LogicCommand | Command_ToggleAfterburners (SDK LC L1481) | Type SPECIAL_POWER, AISpecialPowerInfo Heuristic="TOGGLE" Manager MICRO_MANAGER. Not in the package (global). |
| Template | SpecialPower_ToggleAfterburners (package SpecialPowerTemplates L753) | TargetType NONE, Flags CAN_NOT_BE_SCRAMBLED, **no ReloadTime** |
| SpecialPower module | `<SpecialPower id=ModuleTag_SpecialPower_ToggleAfterburners>` (L218) | Ability entry point |
| Toggle module | `<ToggleStatusSpecialAbilityUpdate id=ModuleTag_ToggleAfterburnersUpdate>` (L221) | ON state: ObjectStatus GENERIC_TOGGLE_STATE SHROUD_REVEAL_TO_ALL, ModelConditions LOCOMOTOR_NORMAL_UPGRADED (drives the afterburner FX draws at L92/L119), triggers ModuleTag_Afterburners + ModuleTag_LoseHealthUpdate. Has SkirmishAiInfo. |
| Speed switch | `<SwitchLocomotorUpdate id=ModuleTag_Afterburners LocomotorSet=NORMAL_UPGRADED MinimumHealth=10%>` | Uses LocomotorSet NORMAL_UPGRADED Speed 55 (NORMAL is 30) |
| Health drain | `<LoseHealthUpdate id=ModuleTag_LoseHealthUpdate DamagePerSecond=200>` | RequiredStatus GENERIC_TOGGLE_STATE |

The schema has **no duration on ToggleStatusSpecialAbilityUpdate** (Modules/ToggleStatusSpecialAbilityUpdate.xsd: ToggleState has only status, MC, modules, etc.). A toggle can't auto-end, so the module has to change.

## Precedent: MovementSpecialPower
Schema: Duration, ModelCondition, ObjectStatus, LocomotorSet, BusyDurationOnExit.
- JapanEngineer L924: Sprint, Duration 10s, MovementType NONE, self AttributeModifier. Its template has ReloadTime.
- JapanAntiVehicleVehicleTech3 L660 and JapanEmperorMecha L407: LocomotorSet="NORMAL_UPGRADED" + ModelCondition + Duration. This is exactly the locomotor-switch pattern.

## Spec (minimal)
1. Kirov unit:
   - Replace the 2 modules L218 (SpecialPower) and L221–256 (ToggleStatusSpecialAbilityUpdate) with one module:
     `<MovementSpecialPower id="ModuleTag_AfterburnersBoost" SpecialPowerTemplate="SpecialPower_ToggleAfterburners" MovementType="NONE" Duration="10s" LocomotorSet="NORMAL_UPGRADED" ModelCondition="LOCOMOTOR_NORMAL_UPGRADED" ObjectStatus="SHROUD_REVEAL_TO_ALL"/>`
     - The ON-state sound SOV_Kirov_CastroBurnersOn can go on the template as InitiateSound. The off sound is lost (cosmetic).
     - GENERIC_TOGGLE_STATE is dropped on purpose: its only consumer was the drain.
   - Delete `<LoseHealthUpdate id="ModuleTag_LoseHealthUpdate">` (user-mandated).
   - Leave SwitchLocomotorUpdate ModuleTag_Afterburners as is. Nothing triggers it any more, so it is inert. Deleting it is also legal; keeping it is the smaller diff.
   - Draws, ClientBehaviors, LocomotorSets 30/55 and the other modules stay unchanged.
2. Package SpecialPowerTemplates L753 SpecialPower_ToggleAfterburners: add `ReloadTime="30s"`. Keep the id so the command, button and string still match.
3. Package LogicCommand (new override of Command_ToggleAfterburners):
   - Same id, Type SPECIAL_POWER.
   - AISpecialPowerInfo Heuristic TOGGLE→SPEED_BOOST, Manager MICRO_MANAGER (engineer-sprint pattern, SDK LC L1622).
   - The command already goes through the global CommandSet, so no CommandSet change.
4. Mod.xml: no change.

## Inferred / unproven
- MovementSpecialPower on an **aircraft** has no SDK precedent (all precedents are ground units). Runtime unproven.
- Countdown display. AI will use it.
- Fallback if it fails at runtime: keep the toggle and add a timed auto-off via ActivateModule. Needs separate research.
