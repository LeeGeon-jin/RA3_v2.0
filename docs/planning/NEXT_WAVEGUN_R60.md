# Next (R60): cancel Wave-Force premature fire (tower + Wave-Force tank) — decided, not implemented
Refs: `wavegun_yuriko_sdk_refs.tar.gz` (8 SDK files).

## Requirement
- **L1044 (user):** "波能炮取消提前发射。" Difficulty 容易, phase 一.
- **L1047:** "已确认：取消波能炮和波能坦克的特殊技能（按F提前发射），原因是AI会用它精准点杀玩家".
- **L1048 (plan):** remove the PrematureDischargeSpecialPower modules and the buttons.

## Current state (b94)
| Object | Module | Button |
|---|---|---|
| Wave tower `JapanBaseDefenseAdvanced.xml` (already in package) | still has `PrematureDischargeSpecialPower id="ModuleTag_FireKiCannonSpecialPower"` (L936-938) | SDK `JapanBaseDefenseAdvancedCommandSet` (SDK LogicCommandSet L693-696) = only `Command_JapanBaseDefenseAdvanced_FireKiCannon` |
| Wave-Force tank `JapanAntiStructureVehicle.xml` (**not in package**; SDK 605 lines) | module at SDK L479-481 | `JapanAntiStructureVehicleCommandSet` (SDK L899-904) = AttackMove, `Command_JASV_FireKiCannon`, MoveToPositionAndCollect |

- Neither command set is overridden in the package yet.
- No other XML references the modules. The ids appear only in LogicCommand, SpecialPowerTemplates and the UI button/state templates; no SkirmishAI hits.

## Minimal Batch 60
1. **Package `Japan/Structures/JapanBaseDefenseAdvanced.xml`:** delete only L936-938 (the module) plus its following blank line.
2. **New `data/Japan/Units/JapanAntiStructureVehicle.xml`:** a full SDK copy with only SDK L479-481 deleted. Mod +1 `type="all"`.
3. **Package `GlobalData/LogicCommandSet.xml`:** append two sets as text (default namespace, tab style).
   - `JapanBaseDefenseAdvancedCommandSet` with no Cmd. Empty-set precedent: SDK `JapanNavalYardRepairBayCommandSet`, L698-700.
   - `JapanAntiStructureVehicleCommandSet` = `Command_AttackMove`, `Command_MoveToPositionAndCollect`, with the original order kept minus the one Cmd.
- **Keep unchanged:** LogicCommand, SpecialPowerTemplates and the UI templates. The orphaned templates and commands are harmless and keep the diff minimal.
- **Expected:** 111 XML; Mod 110 all.
  - tower diff vs b94 = −3 (+blank) lines;
  - tank `diff -w` vs SDK = −3 lines;
  - CommandSet +2 sets; the five CY list tails are unchanged (21/20/26/24/24).
- **Native test:**
  - Normal charge-and-fire still works on both (ChargeWeaponUpdate is untouched).
  - No F button; AI does not error.

## Second ready candidate (decided values, smaller)
- **Yuriko instant psionic blast**, L990-996: "百合子按F到出招的间隔时间去掉，按F立马出招".
- **Plan:** package Weapon.xml `JapanCommandoTech1PsyonicBlast` DelayTimeSeconds 1.0s → 0s (L466) and ShockwaveDelaySeconds 1.0s → 0s (L472). Both are still 1.0s in b94.
- FiringDuration "可缩到0.1s" is only optional → leave 1.0s.

## Researched and excluded (not guessed)
- **Bunker "修碉堡速度减半"** (L725/L728): located at `SovietEngineer.xml` (package L844) `AssembleStructureSpecialAbilityUpdate NewObjectAssemblyTime="10s"` → 5s.
  - **Conflicts with** L31/L215 (11-06): "围墙、碉堡不减半…苏军碉堡（展开 10 秒）".
  - That decision was about the defence-halving rule, but it names the same 10 s → ask the user. Not implementable yet.
- **Hammer "开炮间隔减三分之一"** (L767): the plan's "约0.33s" covers only Min; SDK Max 1.0s has no decision → ask.
