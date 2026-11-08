# BATCH62 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Ground attack is **not** claimed to work in game. Phase 1 not complete.

## Package
- 285547 B, sha256 508bab63…bd789f8b match. All entries under `data/`. 111 XML parse.
- vs 61: only GlobalData/Weapon.xml; other 110 files byte-identical.

## Diff (complete)
- **L3988** `SovietAntiAirShipFlakCannon`: RequiredAntiMask → `ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY ANTI_PARACHUTE ANTI_GROUND ANTI_WATER ANTI_STRUCTURE`.
- **Children** get the original air-only list `ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY ANTI_PARACHUTE` as their own attribute:
  - `AAAVT1_SovietAntiVehicleFlakLauncher` (L5874-5876);
  - `ABD_SovietAntiVehicleFlakLauncher` (L6018-6020);
  - `Leech_FlakCannon` (L7126-7128).
  - Opening tags only; nothing else changed.
- Damage nugget 15 / r15 FLAK, FiringDuration, clip, flags unchanged. Armor multipliers untouched.

## Evidence
- **Enums:** all six values are in `WpnAntiT` (AssetTypeWeaponTemplate.xsd L114-126). The attribute type is the list `WeaponAntiBitFlags` (L132-134, L999). Schema validity only — not proof of runtime inheritance.
- **Attribute override on an inheritFrom child, shipped SDK precedent:** `AlliedBaseDefenseRockets_Aircraft` inheritFrom AlliedBaseDefenseRockets with its own RequiredAntiMask (SDK Weapon.xml L1277-1280). Runtime effect still needs a native test.
- **Inheritance closure:**
  - SDK and package have exactly 3 direct children of the parent, and no grandchildren (no inheritFrom on the 3 children).
  - Users: Bullfrog turret (SovietAntiAirShip L244 SDK), AlliedBaseDefense L367, AlliedAntiAirVehicleTech1 L519, Hammer leech (SDK SovietAntiVehicleVehicleTech1 L868).
  - No other user.
- **Bullfrog turret:** MinimumPitch 15d unchanged. Ground fire is unproven → native test.
- **Attribution:** "牛蛙…对地伤害延续对空的设定" (L761) is the user's line. The mask values are plan text (L764), not the user's words.
