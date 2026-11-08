# BATCH77 AUDIT — SOURCE PASS (static only; no full XSD/compile/in-game; not Phase1 complete)

## Package
- 300064 B, sha256 21a0f9c8…6235ce8a match. All entries under data/. 121 XML parse.
- Mod: 3 reference / 119 all.
- vs 76FIX: only Soviet/Units/SovietAntiVehicleVehicleTech3.xml differs; the other 120 XML are byte-identical.

## Changes
The element-tree diff covers namespace, all attributes and text. It shows **4 additions, 0 removals/changes**. The cloud's ~20 reformatted lines are whitespace-only (`diff -w` shows nothing else).
1. Default ModelConditionState: `WeaponFireFXBone` + `WeaponLaunchBone` WeaponSlotID 3, TERTIARY_WEAPON, FX_Harpoon, after the SECONDARY pair.
   - The spelling is correct (TERTIARY), a valid WeaponSlotType.
   - SlotID follows this file's own convention: turret ID1 bones use SlotID 1, harpoon hardpoint ID2 bones use SlotID 2.
   - Schema BoneAttachPoint: WeaponSlotID SageInt default 1; element order Fire…Launch is valid.
2. WeaponSetUpdate: new `WeaponSlotHardpoint ID="3"` with `Weapon Ordering="TERTIARY_WEAPON" Template="JapanAntiAirVehicleTech1_LandMissileLauncher"`, no status gating.

## Weapon chain (unchanged template, package Weapon.xml L7494-7530 = SDK)
- inheritFrom ScatterableWeapon; range 300; WeaponSpeed 300; AcceptableAimDelta 20d; ClipSize 3; FiringDuration 0.2s; ClipReload 0.5s; CanFireWhileMoving true; LOS required.
- Mask ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY (air only).
- Projectiles JapanAntiAirVehicleTech1MissileProjectile / _Veteran (HEROIC): SDK Japan/Props, loaded globally via Japan.xml L86 `type="all"`.
- Warhead JapanAntiAirVehicleTech1_LandMissileLauncherWarhead (Weapon.xml L7537).
- Sound/FX are Japan global assets.

## Old behaviour preserved (static)
- Turret ID1 cannon / veteran: ForbiddenObjectStatus GENERIC_TOGGLE_STATE (+WEAPON_UPGRADED_01).
- Hardpoint ID2 harpoon: ObjectStatus GENERIC_TOGGLE_STATE.
- GrapplingHookUpdate gated by RequiredStatus GENERIC_TOGGLE_STATE, KeepAlive VEHICLE STRUCTURE TIME_BOMB.
- Toggle states (WEAPONSTATE_ONE, harpoon vision modifier, AI hints), bones and laser (WeaponSlotID 1): all unchanged.
- No AnimationState or sound in the file keys on FIRING_*_B/C (grep), so the new slot cannot trigger the harpoon FX states via model conditions. The harpoon draw is tied to GrapplingHook/WEAPONSTATE_ONE, not to slot 3.
- Masks are disjoint (air vs ground/structure), so there is no static competition between slots.

## Not proven / test in game
- AA fires in both modes (no gating);
- hardpoint ±20d needs the hull to face the target; firing while moving;
- auto-acquire of aircraft;
- missile spawn and look at FX_Harpoon;
- whether ToggleStatusSpecialAbility / harpoon "UpdateModuleStartsAttack" interrupts slot 3;
- AI use;
- performance.

The cloud's "auto-choose correct / omnidirectional / bone tested" claims are not accepted.
