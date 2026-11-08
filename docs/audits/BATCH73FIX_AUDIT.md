# BATCH73FIX AUDIT — SOURCE PARAMETERS VERIFIED (in-game fire rate not tested)
No full XSD, compile or in-game test. Phase 1 not complete.
- The old Batch73 (0.333/0.6) was experimental only and is **superseded** by this fix.
- Basis: the user (17:07/17:08) confirmed reload 0.6–1.0 ×2/3 with firing 0.2 unchanged.

## Package
- 294180 B, sha256 b686f7c0…493c8f04f9 match.
- All entries under `data/`, no `../`. 118 XML parse.
- Mod: 3 reference / 116 all.

## Diff
- **vs 72:** only GlobalData/Weapon.xml L6317-6318, `SovietAntiVehicleVehicleTech1CannonWeapon` ClipReloadTime Min 0.6s→0.4s, Max 1.0s→0.667s (2 attributes). The other 117 XML are byte-identical, including Mod, LogicCommand/LogicCommandSet and namespaces.
- **vs old 73:** 0.333/0.6 → 0.4/0.667 at the same two lines only.

## Unchanged
- FiringDuration 0.2/0.2s, ClipSize 1, AutoReloadsClip AUTO, AttackRange 150, inheritFrom ScatterableWeapon, warhead/damage.
- `Leech_SovietTankCannon` (L7093) still inherits with no timing override.
- Campaign Tutorial_SovietTech1Tank uses the same weapon.

## Status
- **Source parameters:** match the user-confirmed values.
- **Actual in-game fire rate:** not measured.
