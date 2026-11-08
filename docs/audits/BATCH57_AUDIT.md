# BATCH57 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
**Not natively verified:** no full XSD, compile or in-game test. A missing resource is not guaranteed to be cosmetic only. Phase 1 not complete. **The Apocalypse row (L821) is NOT complete:** anti-air and multi-harpoon are still open.

## Package
- 269723 B, sha256 25da927d…64515b6 match; all entries under `data/`; 105 XML parse; Mod 104 all + 3 ref.
- vs 56_FIX: +2 files `Soviet/Units/SovietAntiStructureVehicle.xml` and `SovietAntiVehicleVehicleTech3.xml`; Mod +2 `type="all"` lines (L107-108); other 102 files byte-identical (commands/command sets unchanged).

## Real-file diff vs SDK (whole tar files, not the notification attachments)
- **V4:** 398 lines, same as SDK (cloud's "399" is wrong / off by one). Only L67-70 differ:
  - LocomotorSet NORMAL Speed 50.0 → 70.0;
  - those 4 lines lost one leading tab (whitespace only).
  - BuildTime 15 and cost 1200 kept. No other byte differs; trailing bytes identical.
- **Apocalypse:** 777 lines. Only L79-81 and L85-88 differ:
  - cost 2000 → 1750;
  - Speed 50.0 → 75.0;
  - same one-tab indentation change (whitespace only).
  - BuildTime 20 kept.
- **Everything else is byte-identical to SDK:** all ART `type="all"` includes kept (allowed); BaseVehicle/GlobalDefines includes, Draw/bones/turret/laser draws, WeaponSetUpdate (cannon, veteran cannon, harpoon), geometry, KindOf, armor/body, audio, AI, xi includes.
- **CanFireWhileMoving:**
  - Weapon.xml is unchanged vs 56_FIX. `SovietAntiVehicleVehicleTech3Cannon` keeps `CanFireWhileMoving="true"`.
  - The harpoon template also has that attribute in XML. That does **not** prove the grappling attack needs no stop; behaviour is untested.
  - Main gun, AA and harpoon untouched.
- **Campaign:** the Heidelberg map overrides (BuildTime 60) are not in this XML package → still a separate item.
