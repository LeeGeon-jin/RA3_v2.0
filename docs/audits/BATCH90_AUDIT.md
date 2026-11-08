# BATCH90 AUDIT — PASS (static, read-only), 2026-11-08 22:31 UTC+10
## Package
- batch90.tar.gz = store handoff/RA3_V2.0_Batch90_SovietFlakGround.tar.gz.
- 346498 B (corrected size), sha256 f15cac90726271ee2bf9c345264d3f1bc58fde9f378f89ade534c090f3e88a7a. Matches the claim. The host asset is byte-identical (same sha).
- Layout note: the tar root is `RA3_V2.0_Batch90/data/`. Batch89 used `data/`. Content is unaffected; only the packaging prefix differs.
- 139 XML. Mod.xml: 136 type="all", 3 reference.
- vs b89: only GlobalData/Weapon.xml and Soviet/Structures/SovietBaseDefenseAir.xml differ. The other 137 files are byte-identical.

## Weapon.xml (one insertion, nothing else changed)
- Insertion after SovietBaseDefenseAirFlakCannon (new L5175–5179):
  `<WeaponTemplate id="SovietBaseDefenseAirFlakCannonGround" inheritFrom="SovietBaseDefenseAirFlakCannon" RequiredAntiMask="ANTI_GROUND ANTI_WATER ANTI_STRUCTURE" />`
- **inheritFrom with an attribute override** is a legal SDK pattern (e.g. SDK Weapon L312–316, JapanAntiVehicleInfantryTech3MisslePods_JapanAdvancedMissilePacks).
- The mask values are legal enum values; the SDK uses the identical set (SDK Weapon L36, and the Kirov death weapon).
- Sits at top level between two WeaponTemplates. The file parses as well-formed XML. Template count 339→340.
- **Inherited behaviour:**
  - AttackRange 300, ClipSize 5, 0.2s / 0.25s, CanFireWhileMoving.
  - RadiusDamageAffects ENEMIES.
  - No ProjectileTemplate: WeaponSpeed 1000, the nugget is applied at the target.
  - DamageNugget 25 / r20 / FLAK / SOVIET_FLAK / EXPLODED, with no air-only filter.
  - Nothing in the chain restricts it to aircraft other than the RequiredAntiMask, which is now overridden. So it **can statically hit ground/water/structures.**
  - Actual damage depends on each target's armor FLAK coefficient. Gameplay effect unproven.
- The base flak weapon is unchanged (ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY).
- 89's three Prism attributes and all 81/87 content are unchanged.

## SovietBaseDefenseAir.xml
- Still a full SDK copy. Only differences from SDK: the earlier UNPACK_TIME 20s→10s plus this batch.
- Not a shortened file. Includes, xi:includes (GenericBuildingRepair / SovietSuicide / RepairAlliesEngineerContain), all 4 ScriptedModelDraws, ClientBehaviors and modules are kept element-for-element vs 89.
- **Draw, main PARSE_DEFAULT state:** added SECONDARY_WEAPON WeaponFireFXBone + WeaponLaunchBone "FX_Weapon_", the same bone as primary.
  - No secondary recoil bone. Cosmetic only.
  - The other states are PARSE_NORMAL damage/FX states without weapon bones, the same as for primary.
- **WeaponSlotTurret ID1:**
  - PRIMARY SovietBaseDefenseAirFlakCannon kept.
  - Added SECONDARY Ground, on the same turret. Selection is by anti-mask: primary covers air, secondary covers ground. Primary stays the default for air.
  - MinimumPitch 45d→-10d is shared with primary, as intended.
  - TurnRate 720, PitchRate 360, PitchHeight, idle scan and TurretAITargetChooserData are unchanged.
  - AA capability is not removed; only the lower pitch limit is widened (expected).

## Preserved
- Cloning center MaxSimultaneousOfType="1".
- Normal mirage Speed 80.
- The 3 R89 Prism attributes.
- Advanced mirage not created (0 references). Not counted as complete.

## Unproven
Runtime: ground acquisition, pitch visuals, FLAK damage vs ground armor, AI. Compile.
