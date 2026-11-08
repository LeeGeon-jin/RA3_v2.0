# BATCH59 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 282399 B, sha256 625f5d7b…6747dc7f match. All entries under `data/`. 110 XML parse.
- vs 58: only GlobalData/Weapon.xml differs; other 109 files byte-identical (Mod/commands unchanged).

## Exact diff (4 lines)
- L4122-4123, inside `id="SovietBaseDefenseAdvancedTeslaGun"` (L4107) PreAttackDelay: Min/Max 2.5s → 1.25s.
- L5199-5200, inside `id="SovietEngineerPistol"` (L5184) PreAttackDelay: Min/Max 0.5s → 0.0s.
- Correct ids, no other weapon touched. All earlier Weapon.xml changes are untouched (rest of the file byte-identical).

## Notes
- **Children:** EI_EasterIslandHeadDefenseTeslaGun keeps its own PreAttackDelay 3.0s (L9047-9049). SovietBaseDefenseAdvancedTeslaGun **Link**Gun (overcharge) is unchanged.
- **0.0s precedent:** SDK Weapon.xml L5748-5750 and L8451-8453 (0.0s/0.0s).
- **References:** SovietBaseDefenseAdvanced.xml L365 (package), campaign SovietTeslaWallHub (SDK), SovietEngineer.xml L828.
- **Native test:** the SDK marks PreAttackDelay as "needed for NotifyWhenAttackingBehavior (hackish)", so check Tesla coil assist/charge behaviour; also pistol behaviour.
