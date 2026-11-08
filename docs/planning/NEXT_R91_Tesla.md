# NEXT R91: 磁能坦克 (Tesla Tank) = SovietAntiVehicleVehicleTech2. Base: batch89. Read-only spec, 2026-11-08 22:2x UTC+10
User-fixed values (devdoc L881/L885, no re-confirmation needed): cost 1500, build time 15s, prerequisite super reactor SovietPowerPlantAdvanced, skirmish speed 70. Buildable in skirmish and all campaign missions.

## Current state in b89 (static)
- The unit file is complete: SDK copy with only the B82 crush change (CrushDecelerationPercent 80%→0%) and 3 ART includes removed.
- Removing those ART includes is legal. SDK Soviet/Soviet.xml L22 already includes this unit in the global stream, so its ART is loaded there.
- EditorSorting UNIT, Side Soviet, no Buildable/forbidden flag. ProductionQueueType VEHICLE.
- ButtonImage Button_SovietTeslaTank_small, SelectPortrait Portrait_SovietTeslaTank_big. Keep both.
- No GameDependency at all.
- The only thing blocking production is that no command set offers it. SDK global LogicCommand L2287 already defines Command_ConstructSovietAntiVehicleVehicleTech2, but only S08_SovietWarFactoryCommandSet (SDK LogicCommandSet L1075) uses it.
- Locomotor SovietAntiVehicleVehicleTech2Locomotor is referenced only by this unit (devdoc L885), so changing Speed affects nothing else. Speed sits on the unit's LocomotorSet.

## Exact changes (2 files)
1. Soviet/Units/SovietAntiVehicleVehicleTech2.xml
   - BuildTime 22→15 (L20).
   - BuildCost Amount 2200→1500 (L35).
   - LocomotorSet Speed 62.5→70 (L44).
   - Insert `<GameDependency><RequiredObject>SovietPowerPlantAdvanced</RequiredObject></GameDependency>` before ObjectResourceInfo. Position follows the SovietAntiVehicleVehicleTech3 L76 pattern.
   - Keep everything else, including crush, Draws, ClientBehaviors, modules and includes.
2. GlobalData/LogicCommandSet.xml (package)
   - The package has no SovietWarFactoryCommandSet. Add the full set copied from SDK L473–487, then insert `<Cmd>Command_ConstructSovietAntiVehicleVehicleTech2</Cmd>` after Command_ConstructSovietAntiVehicleVehicleTech1.
   - Placement after Hammer is an inferred position.
   - Keep every other SDK cmd, including the commented salvage line.

## Not needed
- New LogicCommand (the global one exists).
- Mod.xml change (the unit is already included at L71).
- Locomotor change.
- Campaign: the S08 override Speed 100 stays untouched (devdoc).

## Notes
- The S08 commandset is untouched.
- Other campaigns use SovietWarFactoryCommandSet unless they have their own override; not re-scanned.
- Unproven: runtime, preview/ghost, AI use.

Refs: r91_r92_sdk_refs.tar.gz (shared with R92).
