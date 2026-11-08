# Next (R76): Natasha bombing range ×1.5 for STRUCTURES only (vehicles stay 300)
Refs: `r76_sdk_refs.tar.gz` (67115 B, sha256 6a823be248e5543da5a69a08a8eb89db52a98e362375b909cb97593d5091915e):
- SovietCommandoTech1, Weapon, SpecialPowerTemplates, ObjectCreationLists;
- JapanNavyScoutShip, SovietAntiNavyShipTech2 (precedents);
- WeaponSetUpdate.xsd, AssetTypeWeaponTemplate.xsd.

Sniper rifle and Pilot Snipe unchanged.

## Current chain
- **Natasha WeaponSetUpdate** (package SovietCommandoTech1.xml L946-958): one WeaponSlotHardpoint ID 1, AllowInterleavedFiring false, defaults `WeaponChoiceCriteria=PREFER_MOST_DAMAGE`, `AutoChooseWeapon=true` (WeaponSetUpdate.xsd L47-50):
  - PRIMARY `SovietCommandoSniperRifle` (range 300, infantry-only LineDamage filter);
  - SECONDARY `SovietCommandoCallBombingRun`.
- **SovietCommandoCallBombingRun** (Weapon.xml L802-852):
  - AttackRange 300, MinimumAttackRange 50, `RequiredAntiMask="ANTI_WATER ANTI_GROUND ANTI_STRUCTURE"`;
  - nuggets: laser designator + SpecialPowerNugget SpecialPowerBombingRun (filter VEHICLE STRUCTURE VALID_TARGET_FOR_C4) + tint + inform.
  - One weapon for vehicles and buildings → a shared 450 would widen vehicles. Rejected.

## Minimal split (SDK precedent: "…ForBridges" structure-only clones)
- **Precedent:** `JapanNavalScoutShipMiniTorpedoLauncherForBridges` (Weapon.xml ~L3889) `inheritFrom` the base weapon with `RequiredAntiMask="ANTI_STRUCTURE"`, placed as an extra Ordering in the unit's slot. Same for SovietAntiNavyShipTech2TorpedoForBridges (SECONDARY in SovietAntiNavyShipTech2.xml L274-279).
- **Weapon.xml:** new template after L852:
  ```
  <WeaponTemplate id="SovietCommandoCallBombingRunStructure"
      inheritFrom="SovietCommandoCallBombingRun"
      AttackRange="450.0"
      RequiredAntiMask="ANTI_STRUCTURE" />
  ```
  It inherits all nuggets, delays, MinimumAttackRange 50 and the AI hint.
- **Weapon.xml:** the original `SovietCommandoCallBombingRun` mask `"ANTI_WATER ANTI_GROUND ANTI_STRUCTURE"` → `"ANTI_WATER ANTI_GROUND"`, so buildings are served only by the 450 weapon. Range 300 unchanged.
- **SovietCommandoTech1.xml** WeaponSlotHardpoint ID 1: add `<Weapon Ordering="TERTIARY_WEAPON" Template="SovietCommandoCallBombingRunStructure" />` after the SECONDARY entry.
  - TERTIARY is a valid WeaponSlotType (GlobalGameData.xsd L11), used e.g. by AlliedCommandoTech1 L911.
- **Expected:**
  - 121 XML / Mod 119;
  - Weapon.xml +1 template and 1 attribute; SovietCommandoTech1 +1 Weapon line;
  - other files identical.

## Technical uncertainties → native tests (not user questions)
1. Whether ANTI_GROUND alone also matches structures in RA3. If yes, the 300 weapon could still pick structures inside 300; that is harmless (same effect), but the 300–450 band must use TERTIARY.
2. Whether AutoChooseWeapon / PREFER_MOST_DAMAGE selects the TERTIARY weapon against structures at 300–450, for both player-forced and auto targeting. It is equal damage via the same special power.
3. The CommandSet / UI secondary-attack button (if Natasha's bombing is a weapon-mode command) still works with two templates.
4. Vision 325 vs 450 range (ATTACK_NEEDS_LINE_OF_SIGHT; ShroudClearingRange 500).
5. The original structure-attack behaviour of vehicles is unchanged.
