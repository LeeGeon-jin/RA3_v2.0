# Research R58: Apocalypse anti-air (Striker-VX missile) — decided goal, open design details
Refs: `apoc_aa_sdk_refs.tar.gz` (8 SDK files).

## Decided (doc)
- L821 (user): "增加对空能力，对空用打击者vx的导弹".
- L825 (plan): reuse `JapanAntiAirVehicleTech1_LandMissileLauncher`.
- **No new range or damage values are needed:** the template is reused as-is.

## SDK facts
- **Weapon** (Weapon.xml L7498):
  - AttackRange 300, ClipSize 3, reload 0.5 s, AcceptableAimDelta 20d, CanFireWhileMoving true;
  - RequiredAntiMask ANTI_AIRBORNE_VEHICLE/INFANTRY;
  - projectile `JapanAntiAirVehicleTech1MissileProjectile` (+_Veteran for HEROIC), Japan/Props, loaded globally;
  - Japan sounds/FX.
  - Also present in the package's own Weapon.xml (1 hit).
- **Apocalypse WeaponSetUpdate** (L547-585):
  - Turret ID1: cannon / veteran cannon, gated by `ForbiddenObjectStatus GENERIC_TOGGLE_STATE`;
  - Hardpoint ID2: harpoon, active only in toggle mode (`ObjectStatus GENERIC_TOGGLE_STATE`).
  - Bones available: FX_MUZZLEFLASH, B_BARREL, FX_Harpoon, FX_BONE01, InvisBone01, exhaust. **There is no missile bone.**
- **Schema:** `WeaponSlotType` enum includes TERTIARY_WEAPON (GlobalGameData.xsd L11). Precedent for a 3rd ordering with its own fire/launch bones: SovietAntiVehicleVehicleTech1 L137-144.

## Minimal candidate (not yet implementable without choices)
- Apocalypse file only, add a new slot:
  `<WeaponSlotHardpoint ID="3"><Weapon Ordering="TERTIARY_WEAPON" Template="JapanAntiAirVehicleTech1_LandMissileLauncher"/></WeaponSlotHardpoint>`
- Add `WeaponFireFXBone` / `WeaponLaunchBone` for TERTIARY_WEAPON in the default Draw state.
- No Weapon.xml change.

## Open points (design, needs user or test — do not guess)
1. **Aim:**
   - A hardpoint with AcceptableAimDelta 20d means the hull must face the aircraft. That conflicts with "move and attack" at full value.
   - The alternative is putting the missile in turret ID1, but then cannon and AA compete for the turret.
   - A third option is a copy of the weapon with a larger AcceptableAimDelta, but that is a new value.
2. **Launch bone:** none matches the model (FX_MUZZLEFLASH/FX_BONE01/InvisBone01 are candidates). This is visual, but a wrong bone can spawn missiles oddly.
3. **Toggle mode:** should AA work in harpoon mode too? Without status gating it fires in both.
4. **Veterancy / upgrades:** reuse the Japan veteran projectile only. Exclude the `_JapanAdvancedMissilePacks` Japan upgrade.

**Recommendation:** ask the user for 1 (and optionally 3). Until then, pick another decided simple item; don't implement AA by assumption.
