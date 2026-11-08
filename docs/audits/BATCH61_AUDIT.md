# BATCH61 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 285530 B, sha256 4287ad85…15dca7d6e match. All entries under `data/`. 111 XML parse.
- vs 60: only GlobalData/Weapon.xml differs; other 110 files byte-identical (Mod, commands, JapanCommandoTech1.xml unchanged).

## Diff
- Inside `id="JapanCommandoTech1PsyonicBlast"` (L450): DamageNugget `DelayTimeSeconds` 1.0s → 0s (L466); MetaImpactNugget `ShockwaveDelaySeconds` 1.0s → 0s (L472).
- `diff -w` = exactly those 2 lines. Raw diff also shows one tab less on L463-465/467/471/473 (whitespace only).
- **Unchanged:**
  - FiringDuration 1.0s; Damage 500; Radius 250; shockwave 89/250;
  - PackTime 2s; FX frame 28 (unit file byte-same); ReloadTime 30s (SpecialPowerTemplates byte-same).
  - All earlier Weapon.xml changes are intact.

## Notes
- **Attribution:** L996 "百合子按F到出招的间隔时间去掉，按F立马出招" is the user's request. The 1.0→0 values are the doc plan (L999), not the user's words; the cloud report's attribution is wrong.
- **XML can't prove the whole thing is instant.** Native timing test needed. Possible remaining lag sources, none proven: engine firing point within FiringDuration, special-ability state handling, animation/PACKING timing.
- Visual FX (pack anim frame 28) is expected to be out of sync.
