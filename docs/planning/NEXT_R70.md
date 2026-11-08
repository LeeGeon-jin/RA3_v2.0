# Next (R70): Natasha Pilot Snipe startup aim −1 s
Refs: `r70_sdk_refs.tar.gz` (50084 B, sha256 425d9c54…2d1ee4e7):
- SovietCommandoTech1, Weapon, SpecialPowerTemplates;
- AudioSettings, UIComponentOptionsSettingsGeneral, UIConfigs.

## Requirement
- **devdoc L737 (user):** "特殊能力狙击驾驶冷却时间改为10秒，启动时瞄准时间缩短1秒". The cooldown was done in b103.
- No later doc entry changes this.
- **Separate item, not in this batch:** the normal sniper rifle (SovietCommandoSniperRifle, slot L953) one-shotting vehicles/ships. Different weapon; values undecided.

## Package b104 (SovietCommandoTech1.xml, SDK lines in brackets)
- **L14 [212]:** `<Define name="LOCAL_PILOT_SNIPE_TIMING" value="2s" />`.
- **It has exactly 3 uses, all in this file** (no other file in package or SDK references it):
  1. L539 [738]: AnimationState `USER_1 OVER_WATER` (STATE_OverWater), SUCommando_WATKA ONCE_BACKWARDS, `AnimationAbsoluteTime`, + splash particle.
  2. L649 [848]: AnimationState `USER_1`, SUCommando_ATKA ONCE_BACKWARDS, `AnimationAbsoluteTime`.
  3. L1089 [1288]: WeaponFireSpecialAbilityUpdate ModuleTag_PilotSnipeUpdate `UnpackTime`; PackTime 0s, BusyForDuration 0.2s, ActiveModelCondition USER_1 (which drives the two animation states), StartAbilityRange 500.
- **Weapon:** SovietCommandoPilotSnipeWeapon (package Weapon.xml, byte-same as SDK) has no PreAttackDelay/FiringDuration/ClipReload. The only aim timer is the Define.
- No AttributeModifier or veterancy entry changes this timing.

## Minimal Batch 70
- SovietCommandoTech1.xml L14: `value="2s"` → `value="1s"`. One line.
- **Expected:**
  - 115 XML; Mod 114 all;
  - 1 file / 1 line diff; other 114 files byte-identical; commands unchanged.
- **Native test:**
  - real startup time (frame rounding);
  - the backwards aim animation now plays in 1 s (it is compressed, not cut);
  - snipe still fires and the paralyze applies, including over water.

---
# Later candidates (read-only, not for now; no user profile touched)
- **L272 music default 0%:**
  - field `Sounds/AudioSettings.xml` L48 `DefaultMusicVolume="50%"` → `0%`;
  - include chain: global.xml L19 → Sounds/MasterAudioEvents.xml L19 → AudioSettings.xml (global.xml is a package reference);
  - a profile's Options.ini overrides it.
- **L278 classic mouse:**
  - field `UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml` L15 `<DefaultAlternateMouse>false` → `true`;
  - the file is xi:included at GlobalData/UIConfigs.xml L106/L142, so the override path must cover UIConfigs;
  - a profile's Options.ini overrides it.
