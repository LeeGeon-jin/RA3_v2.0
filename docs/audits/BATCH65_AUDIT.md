# BATCH65 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 287176 B, sha256 9de7f1b8…746ce2b34 match. All entries under `data/`. 113 XML parse.
- Mod: 112 all.
- vs 64:
  - Mod +1 line 29 `<Include type="all" source="DATA:Soviet/Props/VacuumBombEffect.xml" />`, right after IronCurtainEffect (same convention);
  - new `Soviet/Props/VacuumBombEffect.xml`;
  - the other 111 files are byte-identical.

## New file vs SDK
- 140 lines each. `diff` = exactly L105 GatherEjectUpdate Lifetime 8s→16s.
- **Byte-identical to SDK:**
  - ART includes FXCrit01/FXLightRays01/FXInvisBone;
  - Draw / particle bones;
  - GatherAcceleration 0.01 / EffectDistance 200 / HeightOffGround 75 / rotation / spacing / filter;
  - FireWeaponUpdate 0.25s → VacuumBombIncrementalWeapon (Weapon.xml not changed → original damage 45 / radius 300);
  - SlowDeath 1s.
- The 4 s warning (VacuumBombSeed) is not in the package → original kept.
- Include closure: same ART includes as SDK; the object is reached through the original OCL_VacuumBomb.
- **Lifetime:** GatherEjectUpdate is the only XML lifetime on the object (no LifetimeUpdate).
  - XML cannot rule out a hidden engine timer, or whether SlowDeath/FireWeaponUpdate behave over the full 16 s.
  - The tick count (~64) is arithmetic, not a schema guarantee → native test.
- **Visual risk:** particle SystemLifetimes are unchanged, so the effects may end before the pull does.
