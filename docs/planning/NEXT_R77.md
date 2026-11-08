# Next (R77): Apocalypse anti-air with Striker-VX missiles (user decided L821) — technical adaptation
Refs: `r77_sdk_refs.tar.gz` (52073 B, sha256 0c0537e25c8604bdea72dad0f8d5e417396daedf1515443b0a5e004ade076153):
- SovietAntiVehicleVehicleTech3, JapanAntiAirVehicleTech1, Weapon;
- JapanAntiAirVehicleTech1MissileProjectile, Japan.xml;
- SovietAntiVehicleVehicleTech1 (TERTIARY bone precedent);
- WeaponSetUpdate.xsd, GlobalGameData.xsd.

## User requirement
- L821: "天启坦克……增加对空能力，对空用打击者vx的导弹".
- Plan L825: reuse `JapanAntiAirVehicleTech1_LandMissileLauncher`.
- Ground cannon / harpoon stay as they are. The remaining points below are technical choices, not user questions.

## Facts
- **VX ground weapon** `JapanAntiAirVehicleTech1_LandMissileLauncher` (package Weapon.xml L7494-7530, = SDK):
  - inheritFrom ScatterableWeapon; AttackRange 300, WeaponSpeed 300, AcceptableAimDelta 20d, ClipSize 3, FiringDuration 0.2, ClipReload 0.5, CanFireWhileMoving true;
  - mask ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY;
  - projectile JapanAntiAirVehicleTech1MissileProjectile / _Veteran (Japan/Props, loaded by Japan.xml L86) + warhead L7537;
  - Japan FX/sound.
  - On the VX it is a **WeaponSlotHardpoint** PRIMARY (JapanAntiAirVehicleTech1.xml L557-565), gated `ForbiddenObjectStatus="TRANSFORMATION_TOGGLE_STATE ADVANCED_MISSILE_PACKS"` (VX-specific statuses).
- **Apocalypse** (package SovietAntiVehicleVehicleTech3.xml, 777 lines, full SDK copy + Batch57 values) WeaponSetUpdate L547-585:
  - Turret ID1: Cannon / Cannon_Veteran, `ForbiddenObjectStatus GENERIC_TOGGLE_STATE` (+WEAPON_UPGRADED_01);
  - Hardpoint ID2: SECONDARY Harpoon, `ObjectStatus GENERIC_TOGGLE_STATE` (harpoon mode only).
- **Draw bones** (default state L124-150):
  - PRIMARY FX_MUZZLEFLASH / B_BARREL (recoil) / FX_MUZZLEFLASH (launch);
  - SECONDARY FX_Harpoon (fire FX + launch).
  - No missile bone. The art files are not on the box, so the full bone list cannot be read. Usable known bones: FX_MUZZLEFLASH, B_BARREL, FX_Harpoon, FX_BONE01, InvisBone01, FXExhaust01/02.

## Minimal technical design (keeps cannon + harpoon unchanged)
1. **New slot:** `<WeaponSlotHardpoint ID="3"><Weapon Ordering="TERTIARY_WEAPON" Template="JapanAntiAirVehicleTech1_LandMissileLauncher"/></WeaponSlotHardpoint>` after ID2.
   - Its own slot, so it fires independently of the turret cannon and the harpoon.
   - Hardpoint = the same aiming as on the VX (hull ±20d).
   - **No ObjectStatus gating** → AA in both normal and harpoon mode. "增加对空能力" is unconditional; the VX toggle statuses do not exist on the Apocalypse.
   - Masks are disjoint (air vs ground/structure), so no weapon competition.
2. **Bones:** add `WeaponFireFXBone` + `WeaponLaunchBone` WeaponSlotType TERTIARY_WEAPON → **FX_Harpoon**, in the default ModelConditionState (L124-150).
   - FX_Harpoon is the hull-mounted hardpoint bone, so it matches hardpoint aiming. The cannon muzzle is on the turret and would mismatch.
   - Precedent for TERTIARY bones: SovietAntiVehicleVehicleTech1 L139-144.
3. **No Weapon.xml change:**
   - the template is reused as-is, no new values;
   - the Japan `_JapanAdvancedMissilePacks` variant is not used;
   - the HEROIC projectile comes from the template's VeterancyProjectiles.
4. **Expected:**
   - 121 XML / Mod 119;
   - one file (SovietAntiVehicleVehicleTech3.xml) +~8 lines;
   - commands unchanged.

## Technical test items (in game)
- Hull aim 20d: AA fires only when the hull faces the target. While moving, this may delay AA. (This is VX-original behaviour.)
- Missile spawn / FX at FX_Harpoon look acceptable; the projectile is visible (Japan props loaded globally).
- No interference with the harpoon in toggle mode; AI uses AA.
- Optionally, a FIRING_C sound/anim is not needed: the VX sound comes via the weapon's FireSound.

## Reminder (decided, pending later batches)
- Cloning center & quick production center: HP 2000 (= battle lab), not implemented.
- Quick production ≤2 s accepted, not implemented.
