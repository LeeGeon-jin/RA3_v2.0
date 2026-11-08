# NEXT R94: Soviet war factory / naval yard repair (skill + 3 drones). Base: b89. Read-only spec
## User-fixed (devdoc L29/L218/L221 ③/L222/L1560/L1609)
- Only the repair function: SpecialPower_TargetedRepairVehicle + 3 repair drones.
- No crane / salvage yard ("那就不做这个").
- devdoc method: "照抄 SovietCrane". The button already exists (Command_RepairVehicle in SovietWarFactoryCommandSet L483 and SovietNavalYardCommandSet L431).
- Test item: can naval-yard drones repair ships.

## SDK source (SovietCrane.xml L464–479), copy verbatim
```
<AssignSlavesTargetObjectSpecialPower id="ModuleTag_SpecialPowerRepairVehicle" SpecialPowerTemplate="SpecialPower_TargetedRepairVehicle" />
<SpawnBehavior id="ModuleTag_SpawnRepairDrones" SpawnNumberData="3" InitialBurst="3" SpawnReplaceDelayData="10s" SpawnedRequireSpawner="true" KillSpawnsOnCaptured="true" SpawnInsideBuilding="true" KillSpawnsOnDisabled="true" SpawnOnUnpack="true">
  <Die DeathTypes="ALL" />
  <SpawnTemplate>SovietRepairDrone</SpawnTemplate>
</SpawnBehavior>
```
- SovietRepairDrone: SDK Soviet/Units/SovietRepairDrone.xml, globally included by Soviet.xml L14. No package file needed.
- Allied naval-yard precedent (AlliedNavalYard L353–368): the same modules with the same AlliedWarFactoryRepairDrone as the war factory. There is no special naval drone, so the Soviet naval yard also uses SovietRepairDrone.
- SpawnOnUnpack="true" stays: Soviet buildings unpack, the same as the crane.
- Command_RepairVehicle (SDK LC L55) → SpecialPower_TargetedRepairVehicle: ReloadTime 1s, MaxCastRange 200, filter VEHICLE HUGE_VEHICLE, excluding AIRCRAFT / AIRBORNE_TARGET. Whether ships carry VEHICLE is a runtime test (L1609). Not changed.

## Changes
1. Package Soviet/Structures/SovietWarFactory.xml: insert the 2 modules inside `<Behaviors>` (opens L519, before the GenericBuildingRepair xi:include at L606).
2. Package Soviet/Structures/SovietNavalYard.xml: same, inside `<Behaviors>` (L483, before L562).
   - Check: neither file already has ModuleTag_SpecialPowerRepairVehicle / ModuleTag_SpawnRepairDrones (static grep: none). No id clash.
3. CommandSets:
   - The war factory command set is fully defined in the package by R91 (SDK copy, Command_RepairVehicle kept).
   - The naval yard set is global (SDK L423), so no change.
   - **Note:** if R91 is not merged first, R94 needs nothing in LogicCommandSet. If it is, make sure Command_RepairVehicle is kept.
4. Mod.xml: no change. Both files are already included.

## Unproven
Drones launching from the unpacked factory, ship repair (L1609), the ~6 extra drones per base for performance (low per devdoc).
