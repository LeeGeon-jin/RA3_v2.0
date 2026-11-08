# BATCH64 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 286310 B, sha256 787e4fe2…5bd989c84 match. All entries under `data/`. 112 XML parse; Mod 111 all (unchanged).
- vs 63: only GlobalData/Weapon.xml; other 111 files byte-identical (Mod, commands, AlliedBomberAircraft.xml).

## Diff (complete)
- L1661-1662, inside `id="AlliedBomberAircraftBombWeapon"` (L1648): FiringDuration MinSeconds/MaxSeconds .25s → .125s.
- Nothing else in the file changed, so all earlier Weapon.xml edits are kept.
- **Kept:**
  - ClipSize 6, ClipReloadTime 15s, FORCE_EMPTY_ENTIRE_CLIP, RETURN_TO_BASE, projectile/warhead (damage), AttackRange 50.
  - `_AirPower` (L1680): ClipSize 9 / reload 10s; no FiringDuration of its own, so it inherits .125s.
  - The campaign override (SDK CampaignOverrides L1035) only changes reload; not in package, untouched.

## Note
The per-shot interval is halved. The actual time from first to last bomb, audio overlap, engine limits and AI behaviour are **not** derivable from XML → native test.
