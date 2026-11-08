# BATCH102_AUDIT — 可建造精准轰炸机（静态独审；编译和实测都没做）
审计时间：2026-11-09 09:10（UTC+10）。基线：101。规范：NEXT_PRECISION_B101.md。对照文件：SDK 的 AlliedSupersonicBomber、AlliedAntiGroundAircraft、AlliedBomberAircraft，以及包内 b101 的 SovietSupportBomber_Buildable。
使用真实包和验证 md，没有使用节选附件。

## 包
- 365822 B，sha256 7c8911e992c1a007fba926ca2dfef2308a14622d744e735c1de52abe364d9cac，与报告一致。
- 153 个 XML；Mod.xml 148 条 all + 3 条 reference。
- 相对 101：新增 AlliedSupersonicBomber_Buildable.xml 和 ExperienceLevels_PrecisionBuildable.xml 两个文件；修改 Mod、LogicCommand、LogicCommandSet、Weapon 四个文件；其余 147 个逐字节相同。6 个文件都能被 ElementTree 正常解析。

## 结论：**硬 FAIL**（新对象 3 处硬伤，另有 3 处偏离规范；其余部分通过）

### 通过的部分
- **武器** AlliedPrecisionBomb_Buildable：inheritFrom AlliedPrecisionBomb，只改 AutoReloadsClip="RETURN_TO_BASE"（与 SDK 世纪轰炸机 Weapon L1663 同一枚举值）。ClipSize 1、射程 150、ClipReloadTime 0.1s、弹体和弹头都继承原版，没有虚构资源。父模板在同一个包内 Weapon.xml 中。
- **经验** AlliedSupersonicBomber_BuildableExperienceLevel_1：inheritFrom ExperienceLevel_AlliedRank1，Required 1，Award 10000，Target 为新 ID，父文件用 instance include，Mod 用 all 加载。与 SDK L221–226 和袋狸的写法一致。
- **命令和命令集：** Command_ConstructAlliedSupersonicBomber_Buildable 类型为 UNIT_BUILD。AlliedAirfieldCommandSet 保留 SDK 原版全部 5 项（4 种机型加 RecallAll），新项插在 RecallAll 之前。AlliedAirfield.xml 引用了这个命令集。SovietAirfieldCommandSet（含袋狸）与 101 逐字相同。
- **对象基本属性：** 1500 / 10 秒；没有 RequiredObject 或协议门槛；运动器 TAXIING 10 加 NORMAL AlliedSupersonicBomberLocomotor 400；HP 2000；ArmorSet 用原版装甲。
- **召唤属性已全部撤除：** SUMMONED、IGNORES_SELECT_ALL、SKIRMISH_AI_DONT_CONSIDER_THREAT、IsTrainable=false、EmptyCommandSet、ParabolicCurveUpdate、AIUpdate、StancesBehavior Remove 都没有了。
- **机场机模块：** JetAIUpdate 与维和轰炸机逐字相同；ReturnToProducerSpecialPower 和 CommandSet AlliedAntiGroundAircraftCommandSet（含返航按钮）都在；空中力量协议的 include 和 StatusBitsUpgrade 都在。
- **AI：** SkirmishAI 里没有引用新 ID，即没有加入建造表。这**不等于 AI 不会造**，要实测。
- **回归：** 101 的基洛夫（DamagePerSecond 100.0）、坠毁 2000 / 112、100C 机场链所在文件全部逐字节等于 101。

### 硬伤（必须修）
- **F1 虚构音效：** 下列音效在 SDK XML、Sounds/Voice.xml、static / global manifest 里都不存在，全部是编造的：
  - AudioArrayVoice 的 9 条 ALL_PrecisionBomber_Voice*；
  - AudioArraySound 的 ALL_PrecisionBomber_MoveStart / MoveLoop；
  - SlowDeath 里的 ALL_PrecisionBomber_VoiceDie。

  SDK 中与精准轰炸机相关的音效只有 ALL_SurgicalStrike_* 和 ALL_PrecisionBomb_BombExplosion，原机只有 `soundAmbient ALL_SurgicalStrike_FlyByLoop`。
  - **修法：** AudioArraySound 恢复原版的 `<AudioEntry Sound="ALL_SurgicalStrike_FlyByLoop" AudioType="soundAmbient"/>`。原机没有语音，AudioArrayVoice 按迁移模板照抄 SDK 维和轰炸机的 8 条 ALL_Vindicator_*（6 条 AudioEntry 加 2 条 NamedEntry），逐字复制，不自造。
- **F2 虚构特效和错误死法：** FX_ALL_AntiGroundAircraftDie 不存在（SDK 维和轰炸机用的是 FX_ALL_VindicatorDie）。死法改成了 SlowDeathBehavior（下沉 3 秒、9 秒后销毁），SDK 的飞机没有这样写的，而且删掉了原有的 CreateObjectDie 和 DestroyDie。
  - **修法：** 删除 ModuleTag_Death SlowDeathBehavior，照 SDK 世纪轰炸机 L239–260 和袋狸 L145–166 改为：
    - CreateObjectDie ModuleTag_CreateObjectDie，CreationList AUBomberAircraft_Dying_OCL，ExemptStatus PARKED_AT_AIRFIELD；
    - CreateObjectDie ModuleTag_CreateObjectDieAtAirfield，CreationList AUBomberAircraft_Die_OCL，RequiredStatus PARKED_AT_AIRFIELD；
    - DestroyDie ModuleTag_Die，DeathTypes ALL；
    - FXListBehavior 的 FX 改为 FX_ALL_VindicatorDie。
  - **纠正 cloud：** 它把“没有 DestroyDie ALL”说成“攻击后不会自动消失”，这是错的。DestroyDie 只在死亡时移除对象，与召唤机飞离消失无关；召唤机消失靠的是 ParabolicCurve / 脚本。去掉 DestroyDie 的真实风险是死亡后对象的移除和残骸不按 SDK 方式处理。
- **F3 Draw 与原版不符：** 与 SDK AlliedSupersonicBomber 的 Draws（L44–147）比较：
  - 丢了 **WeaponLaunchBone WeaponSlotID 1 PRIMARY BoneName FXCON02**，炸弹的发射骨骼没了；
  - 丢了 FXCon01 / FXCon02 的 FireHawkConTrail；
  - 丢了 DAMAGED 状态；
  - REALLYDAMAGED 状态的骨骼和粒子被改了（变成 NONE / AircraftDamage*）；
  - 新加了一个 AnimationState AUSupersonicBomber，而 ART include 只有 w3x 模型，原版也没有这个动画，属于虚构资源。
  - **修法：** 整段 Draws 逐字照抄 SDK L44–147。

### 偏离规范（应修）
- **F4：** 缺少 `<DynamicsUpdate id="ModuleTag_DefaultDynamicsUpdate" xai:joinAction="Remove"/>`。BaseVehicle L43 有这个模块，SDK 原机、维和轰炸机、世纪轰炸机、袋狸都把它移除了。要补上。
- **F5：** 多了 ProductionUpdate ModuleTag_Production（Type AIRCRAFT），所有参照对象都没有，是凭空加的。要删除。
- **F6：** 其它自造数值：
  - Geometry 20 / 30 / 10：原机是 10 / 5 / 5，维和轰炸机是 20 / 15 / 20。改回原机的 10 / 5 / 5。
  - SubGroupPriority 615：维和轰炸机是 605，可以照抄 605。
  - DamageFX AircraftDamageFX、VisionRange 150 / STANDARD 与维和轰炸机相同，属于迁移模板值，可以接受。

## 修复后要复审的内容
- 只改上述 6 处，其余不动。
- 复审时，Draws 与 SDK 做 diff -w 应为空；音效和特效 ID 要能在 SDK 中查到。

## 运行时必测
编译；停机、起飞、攻击、回机场补弹（任一项不过，整项取消）；投弹的发射骨骼；空中和停机时的死法；空中力量协议；AI 是否会造。

## 对 cloud 报告的纠正
- “与其他 5 机型”应为：原版 4 种机型（维和、阿波罗、冷冻直升机、世纪）加新的 1 种；命令集里第 5 项是 RecallAll，不是机型。
- 关于“没有 DestroyDie ALL”的说法，见 F2。
