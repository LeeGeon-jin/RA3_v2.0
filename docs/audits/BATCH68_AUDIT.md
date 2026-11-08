# BATCH68 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete; Natasha as a whole is not complete.

## Package
- 287683 B, sha256 5f568a94…dba1d1d match. All entries under `data/`. 114 XML parse.
- Mod: 113 all, unchanged; commands unchanged.
- vs 67: only 2 files differ; the other 112 are byte-identical.
  - **Soviet/Units/SovietCommandoTech1.xml:** only L34 `MaxSimultaneousOfType="1"` deleted. BuildTime 20 (L24), GameDependency SovietTechStructure and all else kept.
  - **GlobalData/SpecialPowerTemplates.xml:** L915 SpecialPower_PilotSnipe ReloadTime 60s→10s, nothing else.

## Checks
- **Schema:** `MaxSimultaneousOfType` is optional (AssetTypeGameObject.xsd L471, SageUnsignedShort, no default) → omission = no cap (same as the Tanya/Yuriko precedent). Engine meaning of omission is a native test.
- **Parent:** parent BaseInfantry has no MaxSimultaneousOfType.
- **Campaign:** CampaignOverrides has no SovietCommandoTech1 / PilotSnipe entry.
- **Cooldown chain:** SpecialPower_PilotSnipe used only by Natasha's ModuleTag_PilotSnipe / WeaponFireSpecialAbilityUpdate and Command_ActivatePilotSnipeSpecialPower. Unchanged in that chain:
  - the weapon SovietCommandoPilotSnipeWeapon (ParalyzeNugget UNMANNED, range 500);
  - unpack `$LOCAL_PILOT_SNIPE_TIMING` 2s.

## Requirement attribution (doc L737, user's full words)
> 娜塔莎：对付载具、舰船改为用狙击枪一枪打爆一辆；对付建筑距离增加，在安全距离外召唤飞机炸敌军防御；特殊能力狙击驾驶冷却时间改为10秒，启动时瞄准时间缩短1秒。训练时间20秒。可造无限个

- The "one-shot vehicles/ships" item concerns the **normal sniper rifle** (狙击枪), not the Pilot Snipe special ability (狙击驾驶). The batch does not touch either beyond the cooldown.
- **Not done:** one-shot vehicles/ships, building range / bombing distance, and the 1 s aim reduction (see NEXT_R69).
