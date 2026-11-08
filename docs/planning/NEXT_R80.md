# Next (R80): remaining decided Phase-1 source items
Refs: `r80_sdk_refs.tar.gz` (48819 B, sha256 9961f3581990923b0bc3f16f4e12a17a2e874a784a05ccbbf80eb8fe8ed5f98d): 6 SDK Japan decor originals, Weapon.xml, Armor.xml, Weapon / Damage xsd.

## A (recommended next batch, no design needed): remove the invented limit-1 from Japan decor
- **Doc row 25** (user): "让帝国也直接造装饰建筑…雕像1000 其他的2000。雕像10秒 其他的20秒（不耗电；无前置条件）（雕像…都可以造）". Plan L1089: "五种均 1000 / 10 秒、不耗电、无前置、纯装饰".
  - **There is no one-per-player rule for Japan decor.** The "6.只能造一个，不能叠加" decision (L34 / L694 / L809) belongs to the Liberty / Kremlin / Heroes-statue landmarks question set, and those 3 correctly keep limit 1.
- **SDK originals:** TH_EmperorFlagpoleStatue, TH_EmperorSonFlagpoleStatue, VL_ImperialMilitaryAdminBuilding_01, MJ_MtFujiViewingTower, TH_StatueGuard01/03 all have **no** MaxSimultaneousOfType. The limit was invented by the cloud.
- **Precedent:** 74FIX removed the same attribute from Guard02 for this reason.
- **Minimal change:** delete the `MaxSimultaneousOfType="1"` attribute line only, in:
  - JapanEmperorFlagpoleStatue L19;
  - JapanEmperorSonFlagpoleStatue L23;
  - JapanImperialAdminBuilding L24;
  - JapanMtFujiViewingTower L23;
  - JapanStatueGuard01 L18;
  - JapanStatueGuard03 L19.
- Expected: 6 files changed, the other 124 byte-identical, Mod/commands unchanged.
- Note: the doc's phase column for row 25 reads "二", the same as the already-implemented clone / quick production rows. This is the parent's scheduling call; the fix itself is a correction to already-shipped Phase-1 objects.

## B (decided, NOT implemented): Natasha's rifle one-shots vehicles / ships (not bombing, not PilotSnipe)
- **User L737:** "娜塔莎：对付载具、舰船改为用狙击枪一枪打爆一辆".
- Plan L741: "SovietCommandoSniperRifle 伤害 1000（掩码 ANTI_GROUND ANTI_WATER），需让其对载具/舰船生效并给足伤害".
- **Package now** (Weapon.xml L713-762): the only active nugget is a LineDamageNugget 1000 SNIPER with filter `Include="INFANTRY"`. The mask has no structure. The rifle does nothing to vehicles or ships → **missing**.
- **SDK precedent for a guaranteed kill:** AlliedCommandoDetonationWeapon (Tanya C4, SDK Weapon.xml ~L1180-1210): `DamageNugget Damage="999999.0" DamageType="GRENADE" DeathType="DETONATED"` with filter `Include="STRUCTURE VEHICLE VALID_TARGET_FOR_C4"` (minus walls).
- **Minimal technical candidate:** add a second nugget to SovietCommandoSniperRifle: `DamageNugget Damage="999999.0" DamageType=<one whose armor % is non-zero for all vehicles>` with SpecialObjectFilter `Rule="NONE" Include="VEHICLE"` (ships are VEHICLE). Keep the infantry LineDamage, mask, range and timing.
  - "一枪打爆" means a kill, so the huge damage is implementation, not a user number.
- **Must check before implementing:**
  - vehicle ArmorTemplates. GRENADE is listed only on 19 infantry / structure armors (≥50%); vehicle armors fall back to their defaults, so confirm none give 0%;
  - that ships / amphibious units carry VEHICLE;
  - that AI auto-targets vehicles with the PRIMARY rifle (now valid) vs the bombing secondary (vehicles 300) — selection is runtime;
  - DeathType choice (visual).
- Runtime: kills every vehicle tier including epic units, per "一辆" with no exception stated.

## Already done / excluded
Natasha unlimited / 10s PilotSnipe / aim −1s / structure-bombing 450: done. Tanya / Yuriko limits cancelled: done. Phase-2 items are not included.
