# BATCH67 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 287705 B, sha256 4c550efa…fbd3a77ad match. All entries under `data/`. 114 XML parse.
- Mod: 113 all.
- vs 66:
  - new `GlobalData/ObjectCreationLists_ProtonX2.xml`;
  - Mod +1 (L49, right after Weapon.xml, `type="all"`, DATA: path matches);
  - Weapon.xml 1 line (L1328 ParticleCannonWeapon first WeaponOCLNugget → `OCL_ParticleCannonProjectiles_x2`; OCLParticleCannon, AiHint, ReportWeaponFiredStat unchanged);
  - the other 111 files are byte-identical.

## New file (210 lines)
- **Format:** us-ascii, AssetDeclaration in the default asset namespace (same header as the SDK AlliedTankShell_Large), no prefixes.
- **Content:** Tags/Includes empty, one ObjectCreationList; parses.
- **id `OCL_ParticleCannonProjectiles_x2`:**
  - unique in package and SDK;
  - referenced only by Weapon.xml L1328;
  - the original OCL_ParticleCannonProjectiles is still in the referenced global.xml, now unused.
- **Parsed comparison with SDK** (all attributes of each FlingObject and of its 4 children Offset/DistanceFromTarget/AngleAroundTarget/DistanceAtTarget):
  - all 10 blocks equal the SDK block except InitialDelay (0.0s…9.0s) and AngleAroundTarget Low=High (0,36,…,324);
  - CreateObject is an attribute of FlingObject (as in SDK), not a missing child;
  - Count 1, Speed 100, Height 0, UsePrimaryObjectForOffsets, z500, 75/75, 50/50 kept;
  - the angle unit is plain degrees like SDK (72/144…), no `d` suffix;
  - delays use the SDK string form `N.0s`.
- **Not changed:**
  - ParticleCannonProjectile (AlliedSuperWeaponAdvancedEffect.xml) → ParticleAcceleratorFinalWeapon 400 / taper 200 / r250;
  - SpecialPower reload 360 s, 5 s beacon, OCLParticleCannon.
- **Dependency closure:** the new OCL references the GameObject ParticleCannonProjectile, which is loaded from Allied.xml in the referenced game data. Resolving it from a mod-side OCL file is not proven by XML → native test.

## Risks (record only, not fixed)
- **Shroud revealer:** OCLParticleCannon creates `AlliedSuperWeaponAdvancedEffectShroudRevealer` (AlliedSuperWeaponAdvancedEffect.xml L69-70) with LifetimeUpdate 8 s (L102-105).
  - Shots at 8 s and 9 s may fall after the reveal ends. This is an **information/visibility change for the player**, not purely cosmetic.
  - Whether projectiles spawned after 8 s still spawn, hit and damage normally is unproven. The SDK's last shot at 4 s < 8 s proves nothing about >8 s.
  - The cloud's "system guarantees all 0–9 s fire / 8 s won't truncate" is not test evidence.
- **Beacon/audio:** 5 s, mismatched with the 10 s barrage.
- **Damage/FX:** roughly double total damage and FX load.
