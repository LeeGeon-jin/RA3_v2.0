# Next (R81): Natasha's rifle one-shots vehicles / ships
Refs: `r81_sdk_refs.tar.gz`: Weapon, Armor, SovietCommandoTech1, representative ships / aircraft / tank, BaseVehicle, Weapon / Armor / Damage / ObjectFilter / WeaponSetUpdate xsds.

## User wording (doc L737, the only source; no later override found)
"娜塔莎：对付载具、舰船改为用狙击枪一枪打爆一辆；对付建筑距离增加，在安全距离外召唤飞机炸敌军防御；特殊能力狙击驾驶冷却时间改为10秒，启动时瞄准时间缩短1秒。训练时间20秒。可造无限个"
- Plan L741: "SovietCommandoSniperRifle 伤害 1000（掩码 ANTI_GROUND ANTI_WATER），需让其对载具/舰船生效并给足伤害".

### Real ambiguity (report; do not decide)
- "对付载具、舰船**改为**用狙击枪" literally says vehicles / ships are handled by the rifle **instead of** the bombing run.
- Batch76 (per the 17:46 brief "车辆仍原300") keeps the bombing run against ground/water at 300.
- **Question:** keep both (rifle + bombing vs vehicles), or make the 300 bombing structure-only? This is a user-intent question, not a technical one. The minimal-change default is to keep Batch76 as-is and only add the rifle kill.

## Current package (Weapon.xml L713-762)
- SovietCommandoSniperRifle: range 300, PreAttack 0.25, Firing 1.5, Reload 0.25, clip 1, LOS, mask `ANTI_GROUND ANTI_WATER`.
- The only active nugget is `LineDamageNugget 1000 SNIPER` with filter `Rule="NONE" Include="INFANTRY"`.
- Armor: BaseTankArmor / BaseAdvancedTankArmor list `SNIPER 0%` → zero vehicle damage today.
- Slot: Natasha WeaponSetUpdate hardpoint ID1 `AllowInterleavedFiring="false"`, PRIMARY rifle / SECONDARY bombing 300 (ground/water) / TERTIARY bombing 450 (structure). WeaponChoiceCriteria default PREFER_MOST_DAMAGE, AutoChooseWeapon true (WeaponSetUpdate.xsd L49-50).
- Draw bones / commands unaffected by adding a nugget.

## Minimal candidate (implementation choices only)
Add **one** nugget to SovietCommandoSniperRifle, leaving the existing infantry LineDamage, mask, range, timing, sound and FX unchanged:
```
<DamageNugget Damage="999999.0" Radius="0.0" DamageType="GRENADE" DamageFXType="SOVIET_SNIPERRIFLE" DeathType="DETONATED">
  <SpecialObjectFilter Rule="NONE" Include="VEHICLE" />
</DamageNugget>
```
- **Kill precedent:** Tanya C4 AlliedCommandoDetonationWeapon (SDK Weapon.xml ~L1180-1210): 999999 GRENADE DETONATED, filter STRUCTURE VEHICLE.
- "一枪打爆" means a kill, so 999999 is an implementation value, not a design number.
- **DamageType GRENADE:**
  - in all of Armor.xml, GRENADE is never 0% (19 listings, all ≥50%);
  - vehicle armors don't list it → ArmorTemplate `Default` = 100 (AssetTypeArmorTemplate.xsd L48);
  - only special armors have Default=0: ProjectileArmor and InvulnerableArmor (e.g. Iron Curtain / invulnerable states — correct to block);
  - CryoBeamFrozenArmor Default 90000 and ShrinkRay 200 only increase.
  - So no static zero-damage on vehicles. Do NOT use SNIPER (0% on tanks).
- **Targets:**
  - ships are VEHICLE (AlliedAntiAirShip VEHICLE SHIP; Soviet ships AMPHIBIOUS VEHICLE; JapanNavyScoutShip VEHICLE SUBMARINE);
  - the mask lacks ANTI_SUBMERGED / ANTI_AIRBORNE_* → submerged subs and flying aircraft remain untargetable. No AA is added.
- **No structures, no infantry:** the filter is VEHICLE only. The infantry kill stays on the LineDamage (Include INFANTRY).
- **Edge (fact, not an invented exclusion):** aircraft carry KindOf VEHICLE (AlliedFighterAircraft AIRCRAFT VEHICLE). When **landed / parked** (not AIRBORNE_TARGET), they are ground-targetable and would be one-shot. Whether parked aircraft count as "载具" is not stated; flag only.
- **Not added:** relationship / force-fire changes. RadiusDamageAffects ENEMIES and force-fire on allies stay as the weapon already is.
- **Passengers / transports:** DETONATED death follows each unit's own death modules (garrison / passenger handling as when killed by C4). Epic units die too ("一辆", no exception stated).

## Runtime only
- PREFER_MOST_DAMAGE choosing the rifle (999999) over the bombing secondary vs vehicles at ≤300; the bombing nugget has no direct damage, so the rifle is likely preferred but this is not statically guaranteed;
- AI usage;
- LineDamage + DamageNugget both applying on one shot;
- DETONATED visuals.

## Scope
Weapon.xml one insertion only (+5 lines). 130 XML, Mod unchanged. Not Phase 2.
