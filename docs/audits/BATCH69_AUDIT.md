# BATCH69 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.

## Package
- 290907 B, sha256 6c1cbc59…c077d3e match. All entries under `data/`. 115 XML parse.
- Mod: 114 all.
- vs 68:
  - new `GlobalData/Armor.xml`;
  - Mod +1 (L46 `<Include type="all" source="DATA:GlobalData/Armor.xml" />`, within the GlobalData group);
  - the other 113 files are byte-identical (commands too).

## Armor.xml vs SDK
- 2430 lines each, same BOM; 154 ArmorTemplate.
- **diff = exactly 19 values:**
  - Side105/Rear110 → 100/100 at: BaseHarassmentVehicle 584-585, BaseVehicle 626-627, BaseTank 712-713, BaseAdvancedTank 758-759, BaseAntiAirVehicle 803-804, BaseArtillery 849-850, BaseSupportVehicle 895-896, BaseMiner 940-941, AlliedAntiNavyShipTech1 1439-1440 (18 values);
  - RiotArmor Rear 500 → 100 at L1883 (Side was already 100).
- No `<Armor Damage/Percent>`, default, id, inheritFrom or comment line changed.
- **Children:** 27 direct child templates inherit from the 8 vehicle bases (4+4+5+2+0+3+6+3). None redefines the scalars, so they inherit the new 100 at XML level. Runtime merge is a native test.

## Other armor definitions
- The package has no other ArmorTemplate.
- In the SDK, ArmorTemplates outside Armor.xml (CampaignOverrides JapanScoutInfantryArmor, TH_JapanHiveGenerator, TH_ShinzoHouse) carry no scalars.
- Armor.xml is also loaded by reference Static.xml L28 (the same pattern as the Weapon.xml override). That the `type="all"` copy wins is unproven by XML.
- Per-map overrides were not checked (not on the box).

## Kept
- Reverse-move (KEY_D / CanReverseMove) not touched.
- The riot shield's front reductions (e.g. SNIPER 5%) are kept. The rear ×5 weakness is removed, per the user's "无论哪面" wording.
