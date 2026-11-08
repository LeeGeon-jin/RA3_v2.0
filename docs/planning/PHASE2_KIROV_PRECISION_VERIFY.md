# 精准轰炸机 / 基洛夫 第二阶段核实（2026-11-09 08:52 UTC+10，只读，未编译未实测）
依据：真实 SDK、100C 实包、b92f2 / b93f2 实包，以及 cloud 的两份评估。cloud 提供的 JapanEngineer 305 B 附件未使用；工程师冲刺直接以 SDK 原文为准。
执行条件只来自用户 08:43 的指示，cloud 的建议不视为新的授权。

## cloud 评估的错误
1. 仍把“4 级军衔、UI、93 审批”列为待批。用户已定：军衔保持原版一级，UI 属技术项，两者都不需要再批。
2. 称“100C 内 toggle 模块未变、L257–261 为 200”。**不实。**
   - 100C 的 SovietBomberAircraft L216–225 已被 93 的 MovementSpecialPower（10 秒）取代。
   - 原版的 SpecialPower、ToggleStatusSpecialAbilityUpdate、SwitchLocomotorUpdate、LoseHealthUpdate 四个模块都不在包内。
   - 另外 4 个文件也带有 93 的改动。所以回退方案不是“1 个字段、1 个文件”。
3. 称“200 DPS → 100 DPS”。SDK 的真实字段是 **LoseHealthUpdate 的 DamagePerSecond="200.0"**（SDK SovietBomberAircraft L267–273，HealthTrigger="0%"，要求状态 GENERIC_TOGGLE_STATE）。
   - 它不是 Weapon 或 DOT，没有单独的周期字段。xsd 的注释是“每秒受到的伤害”，默认值 100。
   - 实际按帧扣血还是按秒扣血，未证。

## 基洛夫
- **判断：** 目标方案 F（10 秒、不掉血、自动恢复速度、冷却 25 秒、AI 同工程师）属于“难”。
  - SDK 里没有任何 AIRCRAFT 使用 MovementSpecialPower。唯一的先例是步兵 JapanEngineer（SDK L924 起：AttributeModifier 加速、Duration 10s、BusyDurationOnExit 5s；LogicCommand L1624 的 Heuristic 为 SPEED_BOOST）。
  - 93 候选的写法是给 MovementSpecialPower 加 LocomotorSet 来换飞机运动器，没有先例，也没测过。
  - 按用户条件，F 移到第三阶段；第二阶段保留原版双模式，掉血减半。
- **第二阶段：要从 100C 恢复的内容**（都以 b92f2 和 SDK 为准）：

| 文件 | 100C 现状（93 改动） | 恢复做法 |
|---|---|---|
| Soviet/Units/SovietBomberAircraft.xml | L217–223 是 MovementSpecialPower ModuleTag_AfterburnersBoost | 删除这一块，换回 b92f2 的 L217–268（与 SDK L224–275 一致）：SpecialPower、ToggleStatusSpecialAbilityUpdate（两种状态、开关音效、SkirmishAiInfo 原值 TOGGLE_ALWAYS / NeverUseWhenHealthIsBelow 2000）、SwitchLocomotorUpdate（MinimumHealth 10%）、LoseHealthUpdate |
| 同上，减半 | — | LoseHealthUpdate 的 **DamagePerSecond="200.0" 改为 "100.0"**（b92f2 L263）。只改这一个值，HealthTrigger 0% 不变 |
| GlobalData/SpecialPowerTemplates.xml | L754–755 加了 ReloadTime="30s"、InitiateSound | 删掉这两行，回到 SDK（没有冷却） |
| GlobalData/LogicCommand.xml | L34–41 是 Command_ToggleAfterburners（Heuristic SPEED_BOOST） | 删除这一块。b92f2 没有它，由 static 引用里的 SDK 原版提供（Heuristic TOGGLE） |
| UI/Mouse/UnitAbilityButtonTemplates.xml | L30–37 是 ButtonToggleAfterburners（单状态 SpecialPower） | 删除这一块，回到 SDK 的 ToggleSpecialPower 两种状态（Toggle 加 Off）。100C 机场按钮紧跟其后，删除不影响机场按钮 |
| UI/ButtonStateDataCommon.xml | L11–17 是 ButtonStateToggleAfterburners（与 SDK 相同） | 删除，回到 b92f2 |
| SkirmishAI | 没有改动 | 不需要处理。AI 由 SDK 的 ToggleState SkirmishAiInfo 和 TOGGLE 恢复 |

- **必须保留：**
  - Weapon.xml 坠毁 Damage 2000.0 / Radius 112.0（b93f2 L4515–4516）；
  - 基洛夫 2000 / 20 秒；
  - 包内剥离 ART 的惯例；
  - 其它所有已定改动。
- 恢复后，93 的 D1（关闭音效）和 D4（低血量限制）自然消失，不再需要用户决定。93 的 AI 时机也回到原版。
- **核对方法：** 恢复后，用 diff 比较 SovietBomberAircraft 与 b92f2，应当只差 DamagePerSecond 一处；SpecialPowerTemplates、LogicCommand、两个 UI 文件除 100C 机场新增内容外，应与 b92f2 一致。

## 精准轰炸机
- **判断：不难，留在第二阶段。** 但它不是“改几个字段”，而是整对象迁移。理由：
  - SDK 的 AlliedSupersonicBomber 是召唤机：226 行，AIUpdate 加 ParabolicCurveUpdate，CommandSet 为 EmptyCommandSet，KindOf 含 SUMMONED，没有 JetAIUpdate、TAXIING 或返航。所以它本身不能直接用。
  - SDK 有完整的机场机范式：AlliedAntiGroundAircraft（维和轰炸机），包括 JetAIUpdate、两套 LocomotorSet（含 taxi）、ReturnToProducerSpecialPower、自己的命令集。
  - 包内也有同样的先例：96FIX 的 SovietSupportBomber_Buildable 是 272 行的完整对象，以 BaseVehicle 为基类，从世纪轰炸机迁移了 JetAIUpdate、TAXI、武器和回机场语音。
  - SDK 武器 AlliedPrecisionBomb 是 ClipSize 1、AutoReloadsClip NONE，正适合回机场补弹。
- **接续范围（只按已定条件）：**
  - 新对象 AlliedSupersonicBomber_Buildable：1500 / 10 秒，只需机场；
  - 模型、外观、武器保持精准轰炸机原样；
  - JetAIUpdate、LocomotorSet、ReturnToProducer、命令集照 AlliedAntiGroundAircraft（或 96FIX 的袋狸结构）迁移；
  - 盟军机场命令集照 SDK 整套复制后，加入 Command_Construct；
  - 按钮和头像用 Button_PlayerPower_PrecisionStrike；
  - 不加入 AI 建造表。
- **军衔（已定原版一级）：**
  - 新建 AlliedSupersonicBomber_BuildableExperienceLevel_1，值照 SDK ExperienceLevels L221–226：inheritFrom ExperienceLevel_AlliedRank1，Required 1，Award 10000，Target 改为新 ID。
  - 写法照 ExperienceLevels_Badger：父 include 用 instance，Mod 用 all 加载。不需要用户再批。
- **取消规则保留：** park、起飞、攻击、回机场补弹，任一项实测不过就整项取消，不做替代。
- 以上是静态判断，编译和实测都没做。
