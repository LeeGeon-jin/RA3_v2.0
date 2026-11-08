# BATCH93_AUDIT — RA3_V2.0_Batch93_KirovBoost（静态独审，运行时一律未证）
包：cloudstore handoff/RA3_V2.0_Batch93_KirovBoost.tar.gz，352300 B，sha256 0d8dca1af8adddd84f6093c67bd13753df4a27775a1de770048e63a84d8ecdd1，与指令一致。已存为 ra3xfer/batch93.tar.gz，解包到 /workspace/b93/data。未使用 host 旧片段。

## 结论
- **核心改动：静态合法（候选）。**
- **整体：待定（PENDING），不是 PASS。** 有 1 项未经用户批准的音效损失（D1），另有 3 项技术风险（D2–D4）需列明。
- 飞机上用 MovementSpecialPower 在 SDK 中无先例，加速效果在运行时未证，不标效果 PASS。

## 1. 包结构
- 143 个 XML；Mod.xml 含 138 条 type="all" + 3 条 reference。
- 与 92FIX2 做 diff -rq，只有 4 个文件变化：SovietBomberAircraft、LogicCommand、SpecialPowerTemplates、Weapon。其余 139 个逐字节相同。
- 4 个改动文件均能被 python ElementTree 正常解析。

## 2. 加速（SovietBomberAircraft.xml）
- **删除：** SpecialPower 模块 ModuleTag_SpecialPower_ToggleAfterburners、ToggleStatusSpecialAbilityUpdate（含 on/off 两个 ToggleState）、LoseHealthUpdate（200/s）。删除范围 = 92FIX2 的 L217–267。
- **新增：** `MovementSpecialPower id=ModuleTag_AfterburnersBoost SpecialPowerTemplate=SpecialPower_ToggleAfterburners MovementType=NONE Duration=10s LocomotorSet=NORMAL_UPGRADED ModelCondition=LOCOMOTOR_NORMAL_UPGRADED ObjectStatus=SHROUD_REVEAL_TO_ALL`。
- **Schema 核对：**
  - Modules/MovementSpecialPower.xsd 继承自 SpecialPowerModuleData，即它本身就是 SpecialPower 模块。
  - MovementType 枚举含 NONE；Duration、ModelCondition、ObjectStatus、LocomotorSet 都是合法属性。
  - 取值：NORMAL_UPGRADED 在 GlobalGameData.xsd L54；LOCOMOTOR_NORMAL_UPGRADED 在 ModelState.xsd；SHROUD_REVEAL_TO_ALL 在 ObjectStatus.xsd L206。
  - 元素名 MovementSpecialPower 在 AssetTypeGameObject.xsd L266 的 Behaviors choice 中。
- **无需另挂 SpecialPower 模块：** SDK 冲刺先例 JapanEngineer L924（SpecialPower_JapanEngineerSprint，MovementType NONE，Duration 10s）、JapanAntiVehicleVehicleTech3 L659、JapanAntiStructureShip L424 都只有一个 MovementSpecialPower，没有额外的 SpecialPower 模块。绑定无遗漏。
- **速度：** NORMAL 30 / NORMAL_UPGRADED 55 / TAXIING 10 均保留（L42–56）。LOCOMOTOR_NORMAL_UPGRADED 的 Draw 状态（L92/L119）保留。
- **其余部分与 92FIX2 逐元素一致：** Draw、武器、CreateObjectDie、AutoHeal、音频等。

## 3. 模板与命令
- SpecialPower_ToggleAfterburners（SpecialPowerTemplates L753）：只新增 ReloadTime="30s" 和 InitiateSound="SOV_Kirov_CastroBurnersOn"。TargetType NONE 与 Flags CAN_NOT_BE_SCRAMBLED 保留。
- LogicCommand 新增 Command_ToggleAfterburners，Type 为 SPECIAL_POWER，AISpecialPowerInfo Heuristic="SPEED_BOOST"（AssetTypeAISpecialPower.xsd L21 枚举中存在），Manager 为 MICRO_MANAGER。
  - 它和 SDK 的 LC L1482 是同 id 覆盖。包内已有同模式先例 Command_RammingSpeed（92FIX2 已过）。
  - 同 id 覆盖的实际生效顺序属运行时项，未证。
- CommandSet 仍用 SDK SovietBomberAircraftCommandSet（LCS L606），id 未变，引用链完整。

## 4. 坠毁武器（Weapon.xml）
- 与 SDK 逐元素对比，SovietBomberAircraftDeathWeapon 只改了 Damage 500→2000、Radius 50→112（用户 22:30 已定）。
- 保留不变：DamageTaperOff 200、50% ALLIES DamageScalar、MetaImpact ShockWave 50/50/1.0、RadiusDamageAffects 与 Flags。
- **引用链（全查）：** 基洛夫 CreateObjectDie → SUBomberAircraft_Dying_OCL（SDK ObjectCreationLists）→ SDK Soviet/Props/SovietBomberAircraft_Dying.xml L91 的 DeathWeapon。全 SDK 和包内仅此一处引用，包内没有覆盖这两个文件。
- 普通炸弹 SovietBomberAircraftBombWarhead 保持 Damage 400 / Radius 50。

## 5. 两个报告红旗
- **“Mirage 75 unchanged”是 cloud 报告写错：** 包内 AlliedAntiVehicleVehicleTech3 的 NORMAL Speed 为 80.0（L47），与 SDK 一致，文件未改动。
- 复制中心 MaxSimultaneousOfType="1" 保留。
- 91 与 92 的内容在 93 中没有任何文件变化，没有回退（相关文件与已过的 92FIX2 逐字节相同）。

## 6. 差异 / 风险（待处理，不自修）
- **D1 熄火音效丢失（未经用户批准）：**
  - 原来 off 状态的 EnterStateSound SOV_Kirov_CastroBurnersOff 已删除。
  - MovementSpecialPower 和 SpecialPowerTemplate 的 schema 里只有 InitiateSound，没有结束音效属性。
  - 现有模块中找不到“定时结束时播放声音”的干净做法。唯一线索是 Draw 中的 ModelConditionSound（需 RequiredFlags 配合 ExcludedFlags LOCOMOTOR_NORMAL_UPGRADED），但可能在起飞、生成等状态下误触发，未测，不推荐默认采用。
  - **更正：** 我自己的 NEXT_R93 规格当初写了 “off 音效丢失（cosmetic）”，这只是技术说明，不是授权；cloud 称其 “acceptable” 也不能当作授权。需用户决定是否接受。
- **D2 按钮模板类型不匹配（我的规格也漏了）：**
  - SDK 的 ButtonToggleAfterburners（UI/Mouse/UnitAbilityButtonTemplates L733）仍是 `<ToggleSpecialPower>` 双态（Afterburners / AfterburnersOff）。
  - SDK 一次性冲刺的先例是 `<SpecialPower StateData=…>`（ButtonJapanEngineerSprint L975）。
  - 包内的 UnitAbilityButtonTemplates 是只有 3 个 id 的部分覆盖文件，没有覆盖这个按钮。
  - 不匹配的按钮能否触发、能否显示冷却，运行时未证。建议候选：在包内 UnitAbilityButtonTemplates 用同 id 覆盖，改成 `<SpecialPower StateData="ButtonStateToggleAfterburners"/>`（待批）。
- **D3 SwitchLocomotorUpdate ModuleTag_Afterburners 保留但已无触发者：**
  - 它的 schema 没有 StartsActive 一类属性，SDK 中也只有基洛夫这一处使用（原先靠 toggle 的 Module 触发）。
  - 是否完全惰性无法静态证明。如果它默认运行，可能让基洛夫常驻 55。属于运行时必测项；删掉它同样合法。
- **D4 行为差异：** 原 SwitchLocomotorUpdate 的 MinimumHealth 10%，以及 AI 的 NeverUseWhenHealthIsBelow 2000 等提示，在新方案里不再生效。属于设计差异，是否接受请记录。

## 7. 运行时必测（未证）
1. 点击后 10 秒内速度为 55，到期回到 30，冷却 30 秒。
2. 期间全图可见。
3. 开启音效正常播放。
4. AI 会使用（SPEED_BOOST）。
5. 按钮表现（D2）。
6. 非加速状态下不常驻 55（D3）。
7. 坠毁伤害 2000、半径 112。
