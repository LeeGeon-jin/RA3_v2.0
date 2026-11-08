# BATCH49 AUDIT — SOURCE PASS (native-compile candidate)
Source check on box only. **Not** full XSD, **not** compiled, **not** tested in game. Phase 1 not complete.

## Package
- `ra3v2_phase1_batch49.tar.gz` 256944 B, sha256 `d848d83bf348f299bf8cee6c5b12c1443b8b2c1ab0bd3eb5a0b4f0c0010e3584` match; saved `batch49.tar.gz`; no absolute/`..` paths.
- vs 48_FIX: new 3 (`Allied/Units/AlliedMCV.xml`, `Soviet/Units/SovietMCV.xml`, `Japan/Units/JapanMCV.xml`), changed 1 (Mod.xml +3 includes), other 93 byte-identical. 97 XML parse; Mod 96 all + 3 ref. ids = original SDK ids (override, no new id).

## Node diff vs real SDK (diff -w) — only these lines differ
| File | BuildTime | BuildCost | Land Speed | Water Speed |
|---|---|---|---|---|
| AlliedMCV | 60→30 | 5000→3000 | DefaultLandLocomotor 50→60 | DefaultWaterLocomotor 50→60 |
| SovietMCV | 60→30 | 5000→3000 | SovietMCVLocomotor 50→60 | SovietMCVWaterLocomotor 50→60 |
| JapanMCV | 60→30 | 5000→3000 | 40 unchanged | 40 unchanged |
- Both LocomotorSets are Condition NORMAL land/water (verified), so both changed per decision.
- Root namespaces, GlobalDefines include, ART includes, instance includes (EX_Headlights, Extnktrack, BaseVehicle), xi:includes (HeadlightDraw, GenericUnpackPower, Terror drone / crush player powers, Japan kamikaze) all identical to SDK (ART not removed — allowed, not required).
- Unpack params unchanged (macros / Japan 2.0s). No weapon, WeaponSet or fire bone added (MG = batch 2).
- Doc basis: L257-258 (3000/30, unpack excluded, no campaign override), L601-602 (speed 50→60 batch 1), L830 Soviet "同盟军基地车", Japan #15 MG only.

## Risks / test
Campaign has no MCV override (doc) → applies to all missions; unpack visual unchanged; speed 60 pathing; build-log check.
