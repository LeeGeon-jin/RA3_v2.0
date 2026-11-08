# Next (R69): Remove side/rear damage bonus (devdoc L266)
Refs: `armor_r69_sdk_refs.tar.gz` (27458 B, sha256 2ddd1745…4f697ac9f313a):
- Armor.xml, Static.xml, AssetTypeArmorTemplate.xsd;
- AlliedAntiInfantryInfantry, AlliedAntiNavyShipTech1;
- CampaignOverrides, SovietCommandoTech1.

## User requirement (L266, phase 一, easy)
> 把ra3的按D原地后退的正面和背面受到伤害不同的机制去掉。太复杂了。像RA2一样单位无论哪面遭到攻击受到伤害都一样。

- **Plan L269-270:** set Side/RearDamageScalar of the non-100 templates to 100. Reverse-move (KEY_D, CanReverseMove) is kept.
- **Plan note:** this also removes the Peacekeeper shield's rear ×5 weakness.

## Real SDK facts (GlobalData/Armor.xml, 2430 lines, 154 ArmorTemplates)
- **Schema:** SideDamageScalar / RearDamageScalar exist only as ArmorTemplate attributes (AssetTypeArmorTemplate.xsd L50/L58, Percentage, default 100).
- **Where they appear:** in the whole SDK, only in Armor.xml: 15 templates, 30 attributes. Campaign/Tokyo armor templates have none.
- **Values:**

| Line | Template | Side | Rear | Direct child templates (inheritFrom) |
|---|---|---|---|---|
| 582 | BaseHarassmentVehicleArmor | 105 | 110 | 4 |
| 624 | BaseVehicleArmor | 105 | 110 | 4 |
| 710 | BaseTankArmor | 105 | 110 | 5 |
| 756 | BaseAdvancedTankArmor | 105 | 110 | 2 |
| 801 | BaseAntiAirVehicleArmor | 105 | 110 | 0 |
| 847 | BaseArtilleryArmor | 105 | 110 | 3 |
| 893 | BaseSupportVehicleArmor | 105 | 110 | 6 |
| 938 | BaseMinerArmor | 105 | 110 | 3 |
| 1437 | AlliedAntiNavyShipTech1Armor | 105 | 110 | 0 (unit L61) |
| 1880 | AlliedAntiInfantryInfantryRiotArmor | 100 | **500** | 0 (Peacekeeper L147) |

- **Already 100/100, untouched:** BaseEggArmor 667, BaseSubmarine 1087, BaseSurfaceShip 1132, BaseAdvancedSurfaceShip 1177, BaseCapitalShip 1223.
- **Count:** 10 non-100 templates, **19 values to change** (9×2 + Riot rear only).
- **Inheritance:** child templates do not redefine the scalars (they appear nowhere else), so they inherit from these bases. Changing the 10 bases covers all children. Merge semantics are a native test.

## Minimal Batch 69 (keeps all other armor)
- **New `data/GlobalData/Armor.xml`:** a full SDK copy (same as the Weapon.xml precedent; both are in Static.xml).
  - **Option A (remove the attributes):** delete the 19 attribute values / set them to `100`. Deletion uses the schema default of 100, but **setting the explicit value `"100"` is the safer minimal text edit**.
  - No `<Armor Damage=… Percent=…>` line is touched, so front damage reductions and immunities (e.g. Riot SNIPER 5%) stay.
- **Mod +1** `<Include type="all" source="DATA:GlobalData/Armor.xml" />` next to the other GlobalData includes.
- **Expected:**
  - 115 XML; Mod 114 all;
  - Armor.xml diff vs SDK = 19 value changes on 10 lines-blocks;
  - other 114 files byte-identical; commands unchanged.

## Decision point (only one)
- **Peacekeeper riot shield rear 500 → 100.** This is literal from "无论哪面…都一样" and is in the plan.
  - However, it changes the riot-shield mechanic (which the user separately tuned, L496 speed 35).
  - I read it as covered by the user's universal wording; the parent may confirm.
  - If excluded: 9 templates / 18 values.

## Native test
- Side/rear hits equal front hits.
- Per-map overrides (S15 not on box) are not re-checked here.

---
# Side research: Natasha "启动时瞄准时间缩短1秒" — field located
- **SovietCommandoTech1.xml:** `<Define name="LOCAL_PILOT_SNIPE_TIMING" value="2s"/>` (SDK L212 / package L14). Used in:
  - WeaponFireSpecialAbilityUpdate `UnpackTime` (package L1089) — the aim-up before the snipe;
  - two AnimationAbsoluteTime (package L539, L649, USER_1 / USER_1 OVER_WATER) — the aim animation, kept in sync.
- **Weapon:** SovietCommandoPilotSnipeWeapon has no PreAttackDelay/FiringDuration, so the Define is the only aim timer.
- **Candidate:** 2s → 1s. One Define line, same file, BuildTime 20 / no Max kept.
  - Animation playback at a shorter absolute time is visual; native test.
  - This is a located parameter, not a user decision.
