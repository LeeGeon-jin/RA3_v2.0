# Next (R65): Vacuum Imploder duration ×2 — decided (phase 一), not implemented
Refs: `vacuum_spy_sdk_refs.tar.gz` (9 SDK files: VacuumBombEffect, VacuumBombSeed, Soviet.xml, ObjectCreationLists, Weapon, AlliedBaseDefense, AlliedAntiAirVehicleTech1, GatherEjectUpdate.xsd, FireWeaponUpdate.xsd).

## Requirement
- **5.1 #15, L248 (user):** "苏联的真空内爆弹持续时间加一倍". Difficulty 容易, phase 一.
- **L251-252 (plan):**
  - Pull/damage phase 8 s → 16 s via `GatherEjectUpdate Lifetime`.
  - The 4 s warning is unchanged.
  - Total damage roughly doubles (accepted as the consequence of "duration ×2").
  - Particle SystemLifetime doubling is **"按需" / optional (display only) → not decided, not in batch.**

## Package state b99
- `Soviet/Props/VacuumBombEffect.xml` is **not in package**: only IronCurtainEffect.xml exists in Soviet/Props.
- No Weapon/OCL change related to the vacuum bomb.

## SDK (VacuumBombEffect.xml, 140 lines)
- **Includes:** ART:FXCrit01.xml, FXLightRays01.xml, FXInvisBone.w3x.
- **Draw:** particle bones only; no AnimationAbsoluteTime / duration fields.
- **Behaviors:**
  - SlowDeath DestructionDelay 1s;
  - FireWeaponUpdate FireInterval 0.25s → VacuumBombIncrementalWeapon (runs while the object lives);
  - **GatherEjectUpdate Lifetime="8s" (L105)**: the only lifetime in the object (no LifetimeUpdate); EffectDistance 200, filter excludes Iron Curtain / nanohive.
- **Chain:** SovietSuperWeaponAdvanced SpecialWeapon SovietVacuumBomb → VacuumBombSeed (4.0s) → OCL_VacuumBomb (ObjectCreationLists L316) → VacuumBombEffect.
- Loaded via Soviet.xml L92. No campaign value override (doc L252).

## Minimal Batch 65
- New `data/Soviet/Props/VacuumBombEffect.xml`: full SDK copy, same id, **only L105 `8s` → `16s`**, ART includes kept (IronCurtainEffect convention).
- Mod +1 `type="all"`.
- **Expected:** 113 XML; Mod 112 all; `diff -w` vs SDK = 1 line.
- **Native test:**
  - The object actually lives 16 s and damage keeps ticking (≈64 ticks).
  - Lifted units drop/die normally.
  - Particles end early (visual).

## Second ready candidate: spy in IFV / multigunner turret attack interval ≤1 s
- **Requirement:** L652 (user) "间谍进多功能车或多功能炮台后的攻击间隔若超过1秒改为1秒". Phase 一.
- **Plan L655:**
  - AAGA_PistolWeapon FiringDuration 1.0–1.2 + ClipReload 1.0–1.2 ≈ 2.0–2.4 s.
  - IFV: `AAAVT1_PistolWeapon` (spy-only) gets its own FiringDuration 0.5/0.5 + ClipReloadTime 0.5/0.5 → 1.0 s.
  - Turret: new `ABD_SpyPistolWeapon` inheritFrom ABD_PistolWeapon with the same times. The spy slot (Uprade_IFV_GoldenGun) is pointed to it, because ABD_PistolWeapon is shared with Tanya.
  - The base weapon is unchanged; damage/range unchanged.
- **Package b99:**
  - `AAAVT1_PistolWeapon` (Weapon.xml L5824-5828) has no timing override.
  - No ABD_SpyPistolWeapon exists.
  - AlliedBaseDefense (in package) spy slot Template="ABD_PistolWeapon" (L373).
- **Minimal:** Weapon.xml +override in AAAVT1_PistolWeapon + new ABD_SpyPistolWeapon template; AlliedBaseDefense 1 line.
- **The 0.5/0.5 split is a technical choice:** it yields exactly 1.0 s, as requested.

## Checked this round — not candidates
- **Superweapon build ≤30 s:** all original = 30 s, no change (L233).
- **Proton ×2 shots:** needs 5 new OCL entries with computed 36° positions. Plan-specified, but it is an OCL/new-position design → leave for a later, larger batch.
- **Instant capture / crush no-stop:** test-first items (L185 / L209).
- **Already in package:** bribe 5 s (doc correction L517), riot shield, Vindicator, Century.
