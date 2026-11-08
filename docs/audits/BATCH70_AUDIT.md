# BATCH70 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete; Natasha overall not complete.

## Package
- 290909 B, sha256 7b49f1fc…5b9e3fb5 match. All entries under `data/`. 115 XML parse.
- Mod: 114 all, unchanged; commands unchanged.
- vs 69: only Soviet/Units/SovietCommandoTech1.xml differs, 1 line (L14 Define LOCAL_PILOT_SNIPE_TIMING 2s→1s, same element/namespace). The other 114 files are byte-identical.

## Kept
- The Define has 4 occurrences (definition + 3 uses: animation L539 OVER_WATER, L649, UnpackTime L1089).
- PackTime 0s, BusyForDuration 0.2s, BuildTime 20, no MaxSimultaneousOfType, SpecialPower_PilotSnipe 10s (SpecialPowerTemplates unchanged).
- The weapon is unchanged.

## Timing caveat
- SovietCommandoPilotSnipeWeapon omits PreAttackDelay/FiringDuration. Both are optional elements in AssetTypeWeaponTemplate.xsd L835/L840, and the engine's default for an omitted element is unknown here.
- So "fires instantly" or any computed total (e.g. 1.2 s) is **not** guaranteed.
- **Native test:**
  - actual press-to-shot time;
  - the animation compressed to 1 s;
  - over-water state;
  - the paralyze still applies.
