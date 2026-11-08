# BATCH66 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 287212 B, sha256 247daf45…5083f9ee match. All entries under `data/`. 113 XML parse.
- Mod: 112 all, unchanged.
- vs 65: only GlobalData/Weapon.xml and Allied/Structures/AlliedBaseDefense.xml differ; the other 111 files are byte-identical (Mod, commands).

## Diff
- **Weapon.xml +18 lines, no deletions:**
  - **AAAVT1_PistolWeapon:** after its FireFX/inheritFrom attributes, adds `FiringDuration` 0.5/0.5s and `ClipReloadTime` 0.5/0.5s.
  - **New `ABD_SpyPistolWeapon`** (L5996-6004) inheritFrom ABD_PistolWeapon, with the same two elements.
    - Inserted between ABD_PistolWeapon and the existing Tanya `ABD_CommandoPistolWeapon` block.
    - Default asset namespace, no prefix. Not a re-serialized file: there are no other diffs.
- **AlliedBaseDefense.xml:** 1 line, L373 (spy slot, Uprade_IFV_GoldenGun) ABD_PistolWeapon → ABD_SpyPistolWeapon. Tanya's slot L398 is still ABD_PistolWeapon.
- **Element order:** FiringDuration then ClipReloadTime, matching the SDK base AAGA_PistolWeapon order; the children have no Nuggets.
- **Inheritance precedent:** 26 SDK child templates with inheritFrom override both elements. This is evidence of the pattern, not a runtime guarantee.

## Cloud's ABD_CommandoPistolWeapon
It is **real**: SDK Weapon.xml L6019, inheritFrom AAGA_CommandoPistolWeapon. It is in the package since b10 and is unchanged.

## Isolation
- **AAAVT1_PistolWeapon:** referenced only by AlliedAntiAirVehicleTech1 L605 (spy slot). Tanya's IFV slot uses AAAVT1_CommandoPistolWeapon (L623) → untouched.
- **ABD_PistolWeapon:** now referenced only by the Tanya turret slot. AAGA_PistolWeapon is unchanged.
- **Damage, range, sound, mask:** inherited, unchanged.

## Native test
- 0.5 + 0.5 gives a theoretical ~1 s. It is not a schema/exact guarantee: frame rounding, aiming and slot switching are untested.
- Also verify: Tanya unaffected, and the turret spy actually uses the new weapon.
