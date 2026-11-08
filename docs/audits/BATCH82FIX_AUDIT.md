# BATCH82FIX AUDIT — content PASS; packaging defect: 2 stray `.backup` files to remove
Static check only: no compile, no in-game test, no PC. Not Phase 1 complete.

## Package
- `batch82fix.tar.gz` 345361 B, sha256 91f15bb2…304def (matches). All entries under `data/`.
- 135 XML files; Mod.xml has 133 "all" includes.

### vs Batch82 (`diff -rq`)
- Changed: `Japan/Units/JapanAntiVehicleVehicleTech1.xml` and `Soviet/Units/SovietAntiVehicleVehicleTech1.xml`.
- **Extra, non-XML:** `JapanAntiVehicleVehicleTech1.xml.backup` (20473 B) and `SovietAntiVehicleVehicleTech1.xml.backup` (48901 B).
  - Neither is byte-identical to the B82 file (they differ from byte 39).
  - They are not Mod-included, so the builder should ignore them, but they are stray files in the shipped `data/`.
  - **Fix:** delete both and repack. Nothing else changes.
- The other 133 XML files are byte-identical to B82. That covers the 14 single-value overrides, BaseVehicle, BaseEgg, Tesla tank, Mod.xml and everything accumulated through 81 (Weapon.xml unchanged).

## Element-by-element check vs the full SDK
Method: ElementTree parse, ART: `<Include>` removed from the SDK side, then the full tree compared recursively — tag, every attribute and text, child count and order.

| File | Differences |
|---|---|
| JapanAntiVehicleVehicleTech1 (Tsunami) | **1**: `GameObject/CrusherInfo` CrushDecelerationPercent 80% → 0% |
| SovietAntiVehicleVehicleTech1 (Hammer) | **1**: `GameObject/CrusherInfo` CrushDecelerationPercent 80% → 0% |

- **Scope of the comparison:** XML comments are not compared (ElementTree drops them). `xi:include` elements are compared as elements.
- **Tsunami:** `<Draws>` and `<ClientBehaviors>` are both present again, including TruckDraw, the HeadlightDraw1 xi:include, the FX / particles draws and all sound behaviors.
- **Hammer:** 24 IncludeThing = SDK 24. All 5 removed leech targets are back:
  - Mirage → Leech_PrismCannonUpgrade;
  - 3 IFV-type vehicles → Leech_AutoCannonUpgrade;
  - V4 → Leech_V4RocketUpgrade.
- **Hammer unchanged at SDK values:** modules, BuildTime 10, cost 1000, RequiredObject SovietPowerPlantAdvanced. The Hammer's Weapon.xml reload .4 / .667 is still in the unchanged package Weapon.xml.
- **No new build entries, nothing unlocked.**

## Runtime still unproven
- the crush stop disappearing;
- wrecks at 0s;
- the base-object override reaching every SDK vehicle;
- how the builder treats BaseVehicle being both Mod-included and instance-included.

## Verdict
The crush batch is a source candidate once the 2 `.backup` files are removed. No content changes are needed.
