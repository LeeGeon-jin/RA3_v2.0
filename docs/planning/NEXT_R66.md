# Next (R66): Spy in IFV / Multigunner Turret attack interval ≤1 s
Refs: `spy_r66_sdk_refs.tar.gz` (51392 B, sha256 883ba36d…8ba6cd8): SDK Weapon.xml, AlliedBaseDefense, AlliedAntiAirVehicleTech1, AlliedInfiltrationInfantry, AlliedCommandoTech1.

## Requirement
- **devdoc L652 (user, phase 一):** "间谍进多功能车或多功能炮台后的攻击间隔若超过1秒改为1秒".
- **Plan L655:**
  - IFV: AAAVT1_PistolWeapon gets FiringDuration 0.5/0.5 + ClipReloadTime 0.5/0.5.
  - Turret: a new ABD_SpyPistolWeapon inheriting ABD_PistolWeapon, same times, replaces the spy slot.
  - Base weapon, damage and range unchanged.

## Current package (b100)
- **AAGA_PistolWeapon** (Weapon.xml L5449-5480, unchanged from SDK):
  - ClipSize 1, FiringDuration 1.0–1.2s, ClipReloadTime 1.0–1.2s;
  - Damage 30 SNIPER ×1000000% vs infantry, range 200, CanFireWhileMoving;
  - mask ANTI_WATER ANTI_GROUND.
- **AAAVT1_PistolWeapon** (L5824-5828): inherit + FireFX only, no timing.
  - Its only reference in SDK and package is AlliedAntiAirVehicleTech1.xml (package L605, spy slot).
  - So it is spy-only, and overriding it directly is isolated.
- **ABD_PistolWeapon** (L5984-5987): inherit + AttackRange 300. Package AlliedBaseDefense uses it twice:
  - L373 spy (Uprade_IFV_GoldenGun);
  - L398 Tanya (Uprade_IFV_Pistol).
  - Changing it would also change Tanya → a new child weapon is needed.
- **Interval:** ClipSize 1, so one shot = FiringDuration + ClipReload ≈ 2.0–2.4 s (theory) > 1 s.
- **Already in the package (byte-preserve):** earlier batches edited AlliedBaseDefense (ART includes removed). Only change the one slot line.
- **Override precedent:** 26 SDK weapon templates with inheritFrom override both FiringDuration and ClipReloadTime child elements (e.g. AlliedBaseDefenseRockets ← ScatterableWeapon). Child element override is native precedent.

## Minimal Batch 66
- **Weapon.xml:**
  1. Inside AAAVT1_PistolWeapon (before `</WeaponTemplate>`, L5828):
     `<FiringDuration MinSeconds="0.5s" MaxSeconds="0.5s" />` and `<ClipReloadTime MinSeconds="0.5s" MaxSeconds="0.5s" />`.
  2. After ABD_PistolWeapon (L5987), add a new template, text insert (no XML re-serialize):
     `<WeaponTemplate id="ABD_SpyPistolWeapon" inheritFrom="ABD_PistolWeapon">` + the same two elements.
     It inherits range 300, damage, sound, FX and mask.
- **AlliedBaseDefense.xml:** L373 only, `ABD_PistolWeapon` → `ABD_SpyPistolWeapon`. Upgrade/Ordering and Tanya's slot L398 are unchanged.
- **Mod/commands:** unchanged.
- **Expected:**
  - 113 XML; Mod 112 all;
  - diff: Weapon.xml +~10 lines, AlliedBaseDefense 1 line, other 111 files identical.

## Note / native test
- **Why 0.5 + 0.5:** this split is an implementation choice that gives a theoretical 1.0 s per shot. The engine's real cadence (frame rounding, turret/aim time, LOS) is unverified → measure in game.
- **Tanya:** still uses the original ABD_PistolWeapon. Check she is unaffected.
- **Also verify:**
  - the spy upgrade switches to the new weapon;
  - the IFV spy cadence;
  - the fire sound repeating faster.
