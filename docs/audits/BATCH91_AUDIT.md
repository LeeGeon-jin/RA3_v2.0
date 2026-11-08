# BATCH91 AUDIT — PASS (static, read-only), 2026-11-08 22:37 UTC+10
## Package
- batch91.tar.gz = store handoff/RA3_V2.0_Batch91_TeslaTank.tar.gz. 347261 B, sha256 4e5915b67a2fcfba2bfacb3dc17c4d478148a447c36dd49f566cc4ed12d25e92. Matches the claim; the host asset is identical.
- Root is `data/` again. 90 was compared after normalising its `RA3_V2.0_Batch90/data`.
- 139 XML. Mod.xml: 136 all + 3 reference.
- vs 90: only Soviet/Units/SovietAntiVehicleVehicleTech2.xml and GlobalData/LogicCommandSet.xml differ. The other 137 files are byte-identical.

## SovietAntiVehicleVehicleTech2 (磁能坦克), 4 hunks, nothing else changed
- BuildTime 22→15.
- BuildCost 2200→1500.
- LocomotorSet NORMAL Speed 62.5→70.
- Added `<GameDependency><RequiredObject>SovietPowerPlantAdvanced</RequiredObject></GameDependency>` between DisplayName and ObjectResourceInfo. This matches the xsd GameObject sequence order (L386 DisplayName, L388 GameDependency, L389 ObjectResourceInfo; maxOccurs 1). The object had none before.
- B82 CrushDecelerationPercent 0% kept (L419). Draws, modules and includes are unchanged. Well-formed.
- Locomotor SovietAntiVehicleVehicleTech2Locomotor is referenced only by this unit (SDK-wide grep), so the speed change affects no other unit.
- The S08 campaign override (Speed 100) lives in campaign data and is not touched.

## LogicCommandSet.xml, one addition
- New SovietWarFactoryCommandSet. It is the only definition in the package file and sits between two LogicCommandSets.
- Identical to SDK L473–487 except for one added line: `Command_ConstructSovietAntiVehicleVehicleTech2` after `...Tech1` (Hammer).
- Command_RepairVehicle, all original commands and the commented salvage line are kept. Well-formed.
- Production chain:
  - Command_ConstructSovietAntiVehicleVehicleTech2 is already defined in the SDK global LogicCommand (L2287, Object = this unit).
  - The unit is loaded globally (SDK Soviet.xml L22) and is in the package Mod.xml.
  - SovietWarFactory L93 uses CommandSet SovietWarFactoryCommandSet. The button and portrait come from the unit (Tesla UI assets).
- The campaign S08 uses its own S08_SovietWarFactory + S08_SovietWarFactoryCommandSet, so it is independent.

## Preserved
- R90 Ground flak weapon.
- R89 Prism attributes (Weapon.xml unchanged from 90).
- Normal mirage Speed 80.
- Cloning center MaxSimultaneousOfType=1.
- Advanced mirage not created.

## Not proven (runtime)
- Production / unlock behaviour.
- What happens to the queue if the super reactor is destroyed: cloud's claim is not verified.
- Speed feel vs other tanks: no comparison was made from the cloud report.
- AI use. Compile.
