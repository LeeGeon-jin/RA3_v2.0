# NEXT R89 — Mirage tank fires while moving (authorized for 第二批; base = 88FIX)

## Approved values (devdoc L10, 2026-11-06 「好，就这样改」; L592/L595/L596)
1. Weapon.xml L2474 `AlliedAntiVehicleVehicleTech3PrismCannon`: AcceptableAimDelta `10d` → `180d` (L2480). CanFireWhileMoving already `true` (L2476).
2. L2550 `AlliedAntiVehicleVehicleTech3PrismCannon_Veteran`: AcceptableAimDelta `10d` → `180d` (L2556), and CanFireWhileMoving `false` → `true` (L2552).

Nothing else changes: range 125/150, damage, laser, FiringDuration 1.5s, and ForbiddenObjectStatus GENERIC_TOGGLE_STATE (no firing with the field on) are all kept.

## Scope
- References: only Allied/Units/AlliedAntiVehicleVehicleTech3.xml (hardpoint ID1) uses these weapons, in both the SDK and the package.
- CAMP_A08_SpecialMirageTank inherits them, so the campaign Havana tank is also affected. That matches "同时生效".
- AlliedAdvancedMirageTank does **not exist yet** (not in the package). Once created by inheriting CAMP_A08, it gets move-fire automatically.
- Unit file and Mod.xml unchanged; 139 XML stays 139.

## Evidence
- Schema: AssetTypeWeaponTemplate.xsd L902 AcceptableAimDelta Angle (default 0d); L920 CanFireWhileMoving SageBool (default false).
- 34 SDK weapons already use 180d.

## Runtime only (L1596)
- The beam look at 180d; the fallback is 90d, which is the user's own alternative.
- Veteran firing while moving.

## Refs
r89_sdk_refs.tar.gz (92548 B, sha256 51bbc29e…3562d):
- package (88FIX) Weapon.xml and unit file;
- SDK Weapon.xml, unit file, CAMP_A08, Locomotor.xml;
- AssetTypeWeaponTemplate.xsd, WeaponSetUpdate.xsd.

## Second small batch candidate R90 — Soviet flak cannon hits ground (devdoc L779/L782/L783, approved "首选")
- Weapon.xml: new `SovietBaseDefenseAirFlakCannonGround` inheritFrom `SovietBaseDefenseAirFlakCannon`, RequiredAntiMask="ANTI_GROUND ANTI_STRUCTURE ANTI_WATER". Everything else is inherited: FLAK 25 / r20, range 300.
- SovietBaseDefenseAir.xml WeaponSlotTurret ID1 (L357–372): add `<Weapon Ordering="SECONDARY_WEAPON" Template="SovietBaseDefenseAirFlakCannonGround"/>`. The schema allows multiple Weapon elements per slot, sorted by Ordering; precedent AlliedBaseDefense.
- TurretSettings MinimumPitch 45d → -10d (TurretAI.xsd MinimumPitch Angle).
- Draw: add SECONDARY WeaponFireFXBone / WeaponLaunchBone using the same FX_Weapon_ bones as PRIMARY (Apocalypse B77 precedent). Package L93–99 has the PRIMARY ones.
- Open: DamageType for infantry is "待本人定". Default: keep FLAK, so infantry takes 10%. Do not change without the user.
- Runtime: ground firing, unchanged AA, aim animation.
- Refs: r90_sdk_refs.tar.gz (57671 B, sha256 90b5452e…e0a41c):
  - package SovietBaseDefenseAir / Weapon / Armor;
  - SDK SovietBaseDefenseAir, AlliedBaseDefense, Apocalypse unit;
  - WeaponSetUpdate.xsd, TurretAI.xsd, WeaponTemplate.xsd.
