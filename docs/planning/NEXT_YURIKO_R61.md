# Next (R61): Yuriko "press F → fire immediately" — decided values, partial guarantee only
Refs: `yuriko_sdk_refs.tar.gz` (7 files: JapanCommandoTech1, Weapon, SpecialPowerTemplates, LogicCommand, LogicCommandSet, WeaponFireSpecialAbilityUpdate.xsd, AssetTypeWeaponTemplate.xsd).

## Requirement (devdoc)
- **L996 (user):** "百合子按F到出招的间隔时间去掉，按F立马出招". Difficulty 容易, phase 一. No later revision or correction found.
- **L999 (plan):**
  - DelayTimeSeconds 1.0s → 0s and ShockwaveDelaySeconds 1.0s → 0s.
  - FiringDuration 1.0 → 0.1 is "可选" → **not decided, keep 1.0s**.
  - PackTime 2s and reload 30s unchanged.
  - Risk noted: visuals were made for the 1 s wind-up → desync.

## Real call chain (package b95 = SDK except ART includes removed)
1. Command `Command_PsyonicBlastSpecialPower` (LogicCommand L1990-1995, references the weapon for range) → `SpecialPower_PsyonicBlast` (ReloadTime 30s, TargetType NONE, package SpecialPowerTemplates L987).
2. Unit `JapanCommandoTech1.xml` package L552-562:
   - `SpecialPower ModuleTag_PsyonicBlast UpdateModuleStartsAttack="true"`;
   - `WeaponFireSpecialAbilityUpdate SpecialWeapon="JapanCommandoTech1PsyonicBlast" UnpackTime="0s" PackTime="2s" Options="BUSY_DURING_PACK"`.
   - No unpack wait, no PreAttackDelay in the weapon.
3. Weapon (package Weapon.xml L450-484):
   - FiringDuration 1.0s;
   - DamageNugget 500 / r250 **DelayTimeSeconds 1.0s** (L466);
   - MetaImpactNugget shockwave **ShockwaveDelaySeconds 1.0s** (L472).
   - One version only, also used for veteran levels.
4. **Visuals:** `ConditionsYes="PACKING"` AnimationState plays `JUCommandoTech1_SPCA` ONCE, AnimationAbsoluteTime 2s, with `FXEvent FX_JapanCommandoBlast Frame="28"` (L250-260). The blast FX is tied to the pack animation, not to the nuggets.

## Is 1→0 on both delays sufficient?
- **Damage/shockwave:** the only explicit delays in the chain are these two. Schema defaults are 0s (AssetTypeWeaponTemplate.xsd L321, L551), and the SDK has 16 `DelayTimeSeconds="0s/0.0s"` precedents. Setting 0 makes the nuggets apply when the weapon fires.
- **Not provable from XML:** whether the engine fires the special weapon at the start of FiringDuration (vs the end), and when PACKING starts relative to firing. → **Native test:** time from F to damage. If damage still lags ~1 s, the remaining lag is FiringDuration, which is undecided → ask the user. Don't change it now.
- **Visual desync expected:** the FX at frame 28 of the pack animation stays where it is; moving it would be a new design.

## Minimal Batch 61
- Package `data/GlobalData/Weapon.xml` text edit only: L466 `DelayTimeSeconds="1.0s"` → `"0s"` and L472 `ShockwaveDelaySeconds="1.0s"` → `"0s"`.
- Expected diff vs 60: exactly 2 lines. Nothing else; 111 XML.

## Out of scope / pending
Bunker (conflict L31/L215), Hammer Max, Apocalypse AA, paradrop buttons, health values.
