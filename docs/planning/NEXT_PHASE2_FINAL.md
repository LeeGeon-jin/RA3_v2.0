# NEXT_PHASE2_FINAL v4（2026-11-09 04:05 UTC+10） — 最后三项（只读规格；基线 Batch97，sha 60e92383…，静态 PASS 候选；v2 基线为 96FIX）
图例：【定】= devdoc 或用户已定；【推】= 技术推断；【缺】= 真正缺参（需本人定）。一切编译和运行时行为均未证。
v2 更正（重要）：
- v1 称“现有苏/盟 Rushmore 头像 KindOf 缺 FS_BASE_DEFENSE”是**错误的**，已撤回。
  - 证据：SDK BaseObjects/BaseMountRushmoreHead.xml L80 的 KindOf 已含 FS_BASE_DEFENSE；MR_LaserMtRushmore_Lincoln_Ready 没有覆盖 KindOf；包内 Soviet/AlliedRushmoreLaserHead 用的是增量写法 "+POWERED +SCORE -UNATTACKABLE -NOT_AUTOACQUIRABLE"（SDK 增量 KindOf 先例：OD_Castle01 L18）。
  - 所以有效 KindOf = 基类集合 + POWERED SCORE − UNATTACKABLE NOT_AUTOACQUIRABLE，**FS_BASE_DEFENSE 已在其中**，满足 devdoc L788 “KindOf 加 FS_BASE_DEFENSE、POWERED、SCORE，去掉 UNATTACKABLE / NOT_AUTOACQUIRABLE”。
  - 不是漏项，不需要修。
- v1 写的“PackTime 25s”也是错的。日本“展开时间”指的是展开后对象的 StructureUnpackUpdate UnpackTime，不是蛋的 PackTime，详见 1.2。

## 1. 日本 Rushmore 头像（JapanRushmoreLaserHead）
> **已被取代：** 用户 03:54 取消了核心 + 展开，改为与盟军相同的直接建造（2000 / 30 秒，前提 JapanTechStructure，其它既定值不变）。Batch99 硬 FAIL（命令类型）；99FIX 已改为 CONSTRUCTION_YARD_CONSTRUCT，静态 PASS（候选），见 BATCH99FIX_AUDIT.md。下面 1.1–1.5 只作历史记录。
### 1.1 用户既定（devdoc L785 / L788 / L1610 原文）
- 三军都可建造，数值三方相同：造价 2000、建造 30 秒、血量 2000、射程 1150、视野 1250、耗电 -75。【定】
- 帝国做法：JapanRushmoreLaserHead + 核心车 JapanRushmoreLaserHeadEgg，参照 JapanBaseDefenseAdvancedEgg（原版核心 BuildTime 5）；“核心时间 + 展开时间合计 30 秒，拆分待定，如核心 5 秒 + 展开 25 秒”。【定：总 30】【推：5 + 25】
- 前提：帝国纳米电脑主机 JapanTechStructure（本人已确认）。不加 JapanPowerPlant，与原版波能炮核心不同。【定】
- KindOf 加 FS_BASE_DEFENSE、POWERED、SCORE，去 UNATTACKABLE、NOT_AUTOACQUIRABLE；删掉 MaxDeflection 15d，转速 360；不做底座，悬空可接受。【定】
- 射程 1150 的新武器复用包内 SovietRushmoreLaserHeadWeapon（MR_LaserMtRushmore_Lincoln_Ready.xml L314–360，AttackRange 1150）；三方共用模型和武器。【定】
- AI 默认不加入建造表。【定】
- 头像（devdoc：原版已有 Portrait_HeadLincoln_robot）：沿用包内盟/苏版本，SelectPortrait Portrait_HeadLincoln_robot / ButtonImage Button_HeadLincoln_robot，继承自 Ready L16–17。【定 / 推】
- 限额：devdoc 未规定，不加。【定】

### 1.2 时间拆分（技术推断，按 SDK 实际字段）
- SDK 先例：JapanBaseDefenseAdvancedEgg 的 BuildTime 为 5（核心），蛋的 ReplaceSelf PackTime 为 3.0s（L227）。展开后对象 JapanBaseDefenseAdvanced 的 StructureUnpackUpdate UnpackTime 为 40s（L963），包内已减半为 20s（devdoc L215 “波能炮展开 40→20，核心 5 秒不变”）。
- 所以 devdoc 所说的“展开时间” = 展开后对象的 **UnpackTime**；PackTime 3s 是各个日本蛋共有的替换动作，devdoc 计时时没有算它。
- 包内三门炮先例相同：蛋 BuildTime 3 + PackTime 3.0s，JapanWaveForceTripleCannon（FI_FloatingFortressMainGun.xml L338 起）UnpackTime 18s。
- **头像：** 蛋 BuildTime="5"，蛋 PackTime="3.0s"（照先例不改），本体覆盖 `<StructureUnpackUpdate id="StructureUnpackUpdate" xai:joinAction="Replace" UnpackTime="25s"/>`，与包内 SovietRushmoreLaserHead L381–384 的写法完全相同（基类 BaseMountRushmoreHead L121–123 的 id 是 "StructureUnpackUpdate"，UnpackTime 1.5s）。必须覆盖，否则展开只要 1.5 秒。
- 【需告知用户】实际墙钟时间 = 5 + 3（替换动作）+ 25 = 约 33 秒，与 devdoc 计算波能炮时的口径一致。如果用户要求墙钟严格 30 秒，可以改成 PackTime 0 或展开 22 秒，属于设计口径问题，待用户定。

### 1.3 最小完整实现
1. **蛋：** 新文件 Japan/Eggs/JapanRushmoreLaserHeadEgg.xml，逐元素复制包内 Japan/Eggs/JapanWaveForceTripleCannonEgg.xml（它本身是 SDK JapanBaseDefenseAdvancedEgg 的副本），只改以下各项：
   - id / EditorName：JapanRushmoreLaserHeadEgg。
   - SelectPortrait / ButtonImage：Portrait_HeadLincoln_robot / Button_HeadLincoln_robot。
   - Description / TypeDescription / DisplayName：新键 Desc: / Type: / Name:JapanRushmoreLaserHead（字符串待全项目翻译）。
   - BuildTime 3 → 5。
   - GameDependency：删掉 RequiredObject JapanPowerPlant，只留 JapanTechStructure。
   - BuildCost 2500 → 2000。
   - CommandSet 新建 JapanRushmoreLaserHeadEggCommandSet，内容为 Command_UnPackJapanBaseDefenseAdvancedEgg（SDK LC L177，SpecialPower_UnpackReplaceSelf）。也可以直接复用 JapanWaveForceTripleCannonEggCommandSet，两者内容相同；复用的改动更小【推】。
   - ReplacementTemplate：JapanRushmoreLaserHead。
   - 其它（JUEgg Draw、KindOf =$BASE_DEFENSE_EGG_KINDOFS、Side Japan、GenericUnpackPower include）原样保留。
2. **本体：** 加在包内 MR_LaserMtRushmore_Lincoln_Ready.xml 的末尾，结构照 AlliedRushmoreLaserHead（L417–465）逐元素复制：
   - id JapanRushmoreLaserHead，inheritFrom MR_LaserMtRushmore_Lincoln_Ready，Side="Japan"。
   - KindOf 同盟/苏版本的增量写法。
   - EnergyProduction -75。
   - VisionInfo 1250/1250。
   - WeaponSetUpdate Replace（SovietRushmoreLaserHeadWeapon，TurretTurnRate 360，不写 MaxDeflection）。
   - ActiveBody MaxHealth 2000。
   - StructureUnpackUpdate id="StructureUnpackUpdate" Replace UnpackTime 25s（照苏军版 L381–384，见 1.2）。
   - **不写** BuildCost / BuildTime / GameDependency：造价和前提在蛋上；日本可展开防御的本体按包内三门炮先例写了 BuildCost 2500，那只用于退款和计分，本体照写 2000【推】。
3. **命令：** LogicCommand 新增 Command_ConstructJapanRushmoreLaserHeadEgg（Type UNIT_BUILD，`<Object>JapanRushmoreLaserHeadEgg</Object>`，必须用 Object 元素，见 96 的 F1）。加入 JapanConstructionYardCommandSet（包内 LogicCommandSet L97 起，放在 Command_ConstructJapanWaveForceTripleCannonEgg 之后）。
4. **Mod.xml：** 新增一条 `<Include type="all" source="DATA:Japan/Eggs/JapanRushmoreLaserHeadEgg.xml"/>`。本体所在的 MR 文件已在 Mod L107。
5. **不做：** AI BuildEntry；等级表（devdoc 未要求，防御建筑本来也没有）；新图片和新字符串文件。

### 1.4 美术 / 全局依赖
- 头像模型 MR_LaserMtRushmore_Lincoln(.W3X / _COL)：SDK 版 Ready 文件 L7–8 以 all 方式 include，**包内版已去掉这两条**（包内 L1–9），盟/苏头像从早先批次起就这样。
- devdoc L788 风险①：民用资源原版只由 WorldBuilder.xml 包含，mod 必须一并包含，否则可能隐形或报错。本机 manifest 无法判断这些模型是否在全局流中（连已知全局模型也查不到），所以属于**编译和实测前提**，是三方头像共同的现存风险，不是本批新增。
- ~~w3x 源文件在本机 bibber/Art/mr 下。~~【更正】本机 bibber/Art 下的这些 w3x 只是 75 字节的空 AssetDeclaration 占位文件，不能证明真模型存在。真模型是否存在，要等编译时验证（见 BATCH97_AUDIT L38）。
- 激光 FX：BaseMountRushmoreHead 以 instance 方式 include ART:FXPrisimLaser01 / 01b / FXRailDistort；Ready 文件 include ART:FXLaserStandard.xml。随继承链一起编译。
- 核心模型 JUEgg：原版日本蛋共用。

### 1.5 运行时必测
1. 核心 5 秒，替换后 25 秒展开（墙钟约 33 秒）。
2. 模型显示（不隐形），悬空可接受。
3. 激光射程 1150，可以朝背后开火，头像大概率不转。
4. 血量 2000，能被攻击，敌人会自动索敌。
5. 低电时停火（POWERED）。
6. 按钮和字符串显示。

## 2. 科技机场空降（方案 B，v4：基线 Batch99FIX（与 99 只差头像命令类型，与机场无关），可直接交 cloud 实现；静态规格，编译 / 运行未证）
图例：【定】用户 / devdoc 已定；【推】技术推断；【未证】运行时待测。

### 2.1 用户既定
- 倒计时 9 分钟 → ReloadTime="540s"，每个玩家共用一个倒计时（SHARED_SYNC）。【定】
- 点地面目标，TargetType="LOCATION"。【定】
- 每阵营 5 名步兵：盟 3 AlliedAntiInfantryInfantry + 2 AlliedAntiVehicleInfantry；苏 3 SovietAntiInfantryInfantry + 2 SovietAntiVehicleInfantry；帝 3 JapanAntiInfantryInfantry + 2 JapanAntiVehicleInfantry。【定】
- 袋狸模型，从地图边缘入场。【定】
- 方案 B：按钮在机场上，丢了机场就不能用；占领的中立机场和建造的三方机场都适用。【定】
- **用户 03:55 新决定：** 飞机被击落时，**尝试弹出机上剩余的乘员**，实际能否生还待测。此决定**覆盖**原来“随机死亡”的要求。随机方案的研究移到附录 R，不作为实施要求。【定】
- 保留原 2% 空中治疗；遭遇战 AI 不用（不写 AISpecialPowerInfo）。【定】

### 2.2 新文件 A：Neutral/Structures/TechAirportParadrop.xml（新文件，Mod 加 1 条 all）
内容为 3 架飞机、3 个 OCL。SpecialPowerTemplate 不放这里，改写进包内 GlobalData/SpecialPowerTemplates.xml，见 2.6。

**A1. 飞机 ×3**：TechAirportParadropBomber_Allied / _Soviet / _Japan
- `inheritFrom="SovietSupportBomber_Buildable"`，即包内 96FIX 的袋狸：Draw 是 Badger，TransportContain id 为 ModuleTag_Contain，ContainMax 5，已有 EjectPassengers 模块。
- Includes：`<Include type="instance" source="DATA:Soviet/Units/SovietSupportBomber_Buildable.xml"/>` 和 `<Include type="all" source="DATA:GlobalData/GlobalDefines.xml"/>`，照包内各文件惯例。
- 对象属性：
  - KindOf 增量 `"-AIRCRAFT_TRANSPORT_ONLY_GARRISONABLE_WHILE_PARKED -LIMITED_PRODUCTION_AIRCRAFT +SUMMONED +IGNORES_SELECT_ALL +NO_COLLIDE -SELECTABLE"`。照 CAMP_AlliedBomberAircraft_Infantry_2 L11；多去掉的 LIMITED_PRODUCTION_AIRCRAFT 是【推】，免得召唤物计入停机位。
  - `IsTrainable="false"`（照 CAMP）。
  - Side：_Allied 为 "Allies"，_Soviet 继承 Soviet，_Japan 为 "Japan"。
  - EditorSorting="UNIT"。BuildCost / GameDependency 继承后无害【推】，因为召唤物不经生产。
- Behaviors（module id 与父类相同时用 xai:joinAction 合并；新 id 直接追加）：
  1. `<TransportContain id="ModuleTag_Contain" xai:joinAction="Replace" …>`：
     - **用 Replace 整段重写，不用 Append。** CAMP 用 Append 只追加 InitialPayload；本项要改 KillPassengersOnDeath 属性，Append 能否覆盖属性无证据，所以整段替换。
     - 内容逐字复制父类 SovietSupportBomber_Buildable L175–200 的全部属性和子元素（ObjectStatusOfContained UNSELECTABLE ENCLOSED、ContainMax 5、Allow*、ShowPips、Enter/ExitSound、ConditionForEntry INVALID、ExtendedExitContainerChecks、PassengerFilter、DieMuxData ALL、PassengerData BONEGARRISON），只改：
       - `KillPassengersOnDeath="false"`（父类为 true）；
       - 显式写 `EjectPassengersOnDeath="true"`。OpenContain.xsd L46–47，默认值本来就是 true，显式写出便于审计；
       - 末尾加 `<InitialPayload Name="…AntiInfantryInfantry" Count="3"/>` 和 `<InitialPayload Name="…AntiVehicleInfantry" Count="2"/>`（按阵营）。
     - **为什么只弹出剩余乘员、不会复制：** 死亡时弹出的是此刻容器里的对象，已经跳下去的不在容器里。没有新生成任何对象（不用 OCL 或 FireWeaponWhenDead）。【静态推理；实测确认】
  2. `<SpecialPower id="ModuleTag_EjectPassengers" xai:joinAction="Replace" SpecialPowerTemplate="SpecialPower_EjectPassengers" UpdateModuleStartsAttack="true"/>`（照 CAMP L82–86）。
  3. `<EjectPassengersSpecialAbilityUpdate id="ModuleTag_EjectPassengersUpdate" xai:joinAction="Replace" SpecialPowerTemplate="SpecialPower_EjectPassengers" Height="150.0" StartAbilityRange="0.0" TimePerPassenger=".5s" Radius="0" RunOffMapWhenDone="true" IgnoreTargetLocation="true" Options="RECONSTITUTE_STORED_COMMAND DO_NOT_DO_AI_SPECIAL_POWER"/>`（照 CAMP L87–97 逐字）。
  4. `<RunOffMapBehavior id="ModuleTag_RunOffMapBehavior" xai:joinAction="Replace" FlyingOffMap="true" RequiresSpecificTrigger="true"/>`：
     - **必须用 Replace**，照 CAMP L98–100 逐字。
     - 已核：BaseVehicle.xml L125–129 已有同 id 模块（RequiresSpecificTrigger true、RunOffMapWaypointName="RunOffMap"，没有 FlyingOffMap）。如果不写 Replace 而直接追加，会出现重复 id。
  5. `<WeaponSetUpdate id="ModuleTag_WeaponSetUpdate" xai:joinAction="Remove"/>`（照 CAMP L101–103），不投弹。
  6. 继承下来但**不改**的模块：
     - AlliedAirPowerUpgrade include（ModuleTag_AirPowerUpgrade，AttributeModifierUpgrade，由 Upgrade_AlliedAirPower 触发）；
     - ModuleTag_UpgradeWeapon（StatusBitsUpgrade）。
     
     只有盟军玩家有此升级时，属性加成才会作用到盟军版飞机上；武器槽已删，StatusBits 不起作用。这不影响弹出和飞离，**判定不干扰**。如果要零差异，可加两条 Remove，属可逆技术项。
- 原袋狸、世纪轰炸机，以及包内 SovietSupportBomber_Buildable 文件本身**都不改**。死亡弹出只在 3 架机场专用机上生效。

**A2. OCL ×3**：OCL_TechAirportParadrop_Allied / _Soviet / _Japan
- 照 OCL_CAMPAlliedBomberDrop1（CAMP_Infantry_1.xml）。这个先例的出生点由 OCLSpecialPower 的 CREATE_AT_EDGE_NEAR_SOURCE 决定，所以 Options 里**不加** CREATE_AT_TARGET（OCL_ParaDropLvl1 有它，是因为那是从目标点出生的玩家技能）。
- 每个 1 架：

  `<CreateObject Options="IGNORE_ALL_OBJECTS DONT_SET_PRODUCER ISSUE_MOVE_AFTER_CREATION FIRE_SPECIAL_POWER" Disposition="LIKE_EXISTING" FireSpecialPowerTemplate="SpecialPower_EjectPassengers"><Offset x="0" y="0" z="190"/><CreateObject>TechAirportParadropBomber_X</CreateObject></CreateObject>`
  
  只有 1 架，所以不需要 MOVE_TARGET_USES_OFFSET【推】。
- 航线：从离机场最近的地图边缘出生（CREATE_AT_EDGE_NEAR_SOURCE）→ 移动到目标（ISSUE_MOVE_AFTER_CREATION）→ 到达后执行 SpecialPower_EjectPassengers，逐个跳伞（FIRE_SPECIAL_POWER）→ RunOffMapWhenDone 飞离地图。【SDK 先例；未证】

### 2.3 中立机场：Neutral/Structures/AirportTechStructure.xml（整文件复制 SDK，Mod 加 1 条 all）
- 逐字复制 SDK 文件，包括 ART include、文件内的 NUAirportTechStructure_Die_OCL、PassiveAreaEffect 2% 治疗（L102 起）。
- 只增加：
  - 对象属性 `CommandSet="TechAirportParadropCommandSet"`（原本继承 BaseTechStructure L23 的 EmptyCommandSet）；
  - Behaviors 末尾加 3 个 OCLSpecialPower（见 2.5）；
  - Includes 加 `<Include type="instance" source="DATA:Neutral/Structures/TechAirportParadrop.xml"/>`。

### 2.4 可建造机场：包内 Neutral/Structures/AirportTechStructureBuildable.xml（修改）
- 只改 AlliedAirportTechStructureBuildable（L12）：
  - 加 `CommandSet="TechAirportParadropCommandSet"`；
  - Behaviors 末尾加同样 3 个 OCLSpecialPower；
  - Includes 加上面那条 instance include。
- Soviet（L191）和 Japan（L204）继承自 Allied。Soviet 的 Behaviors 只追加了 ModuleTag_StructureUnpackUpdate，不会覆盖新模块，所以**三方同源继承，不要分写三遍**。
- PassiveAreaEffect 2% 原样保留。

### 2.5 OCLSpecialPower ×3（中立机场和可建造盟军机场各一组，内容相同）
- `<OCLSpecialPower id="ModuleTag_TechAirportParadrop_Allied" SpecialPowerTemplate="SpecialPower_TechAirportParadrop_Allied" OCL="OCL_TechAirportParadrop_Allied" DestinationOCL="OCL_PrecisionStrikeBeacon" CreateLocation="CREATE_AT_EDGE_NEAR_SOURCE"/>`
- _Soviet、_Japan 同构。
- 照 CAMP_PowerStore_AlliedBomberDrop L35–46。OCL_PrecisionStrikeBeacon 定义在 SDK GlobalData/ObjectCreationLists.xml L1085，是全局对象。

### 2.6 SpecialPowerTemplate ×3：写入包内 GlobalData/SpecialPowerTemplates.xml（93 起已覆盖此文件）
```
<SpecialPowerTemplate id="SpecialPower_TechAirportParadrop_Allied"
  ReloadTime="540s" TargetType="LOCATION" RadiusCursorRadius="100"
  EvaEventToPlayWhenSelectingTarget="SelectSpecialPowerTargetArea"
  Flags="IS_PLAYER_POWER PATHABLE_ONLY NOT_CLIFF_CELL NO_FORBIDDEN_OBJECTS SHARED_SYNC"
  RequiredPlayerTech="PlayerTech_Allied" WaypointModeTerminal="false">
  <ForbiddenObjectFilter Rule="ANY" Include="STRUCTURE CRUSHABLE_OBSTACLE AIRCRAFT" Exclude="BRIDGE_ENDCAP BRIDGE_SEGMENT">
    <ExcludeThing>NanoSwarmHiveEffect</ExcludeThing>
  </ForbiddenObjectFilter>
</SpecialPowerTemplate>
```
- _Soviet / _Japan 只改 id 和 RequiredPlayerTech（PlayerTech_Soviet / PlayerTech_Japan，见 System/PlayerTechs.xml L6/9/12）。
- 字段来源：
  - Flags 和 ForbiddenObjectFilter、半径 100、Eva 来自 SpecialPowerParadropLvl1（CampaignOverrides L142–162），再加上 CAMP 掉落先例的 SHARED_SYNC（SpecialPowers L1617）；
  - **不抄** GameDependency 和 ForbiddenPlayerTech，那是战役军衔用的。
- RequiredPlayerTech 在 schema 中合法（AssetTypeSpecialPowerTemplate.xsd L120）。但用阵营根科技做门控**没有 SDK 先例**【推】；按钮隐藏还是变灰【未证】。
- SHARED_SYNC 的语义是“同一玩家所有同模板实例共享计时”【先例：推】。每阵营一个模板，所以同一玩家的多座机场共用一个 540s 计时。
- 不写 AISpecialPowerInfo，AI 不用。

### 2.7 命令 / 命令集 / 按钮（全部用新 ID，复用既有图）
- 包内 GlobalData/LogicCommand.xml 加 3 条：
  - `<LogicCommand Type="SPECIAL_POWER" id="Command_TechAirportParadrop_Allied" Options="NEED_TARGET_POS"><SpecialPower>SpecialPower_TechAirportParadrop_Allied</SpecialPower></LogicCommand>`；
  - _Soviet、_Japan 同构；
  - NEED_TARGET_POS 是合法值（AssetTypeLogicCommand.xsd L38）；**不写 AISpecialPowerInfo**。
- 包内 GlobalData/LogicCommandSet.xml 新建 `<LogicCommandSet id="TechAirportParadropCommandSet">`，含这 3 条 Cmd。
- 包内 UI/Mouse/UnitAbilityButtonTemplates.xml（93 起已覆盖）加 3 个：
  - `<UnitAbilityButtonTemplate id="ButtonTechAirportParadrop_Allied" LogicCommand="Command_TechAirportParadrop_Allied"><Data><TargetedSpecialPower RadiusCursor="Target_Allied_Paradrop" StateData="ButtonStateAbilityEjectPassengersUntargetted" ValidTargetCursor="TargetAbility"/></Data></UnitAbilityButtonTemplate>`；
  - 照 SDK ButtonEjectPassengers L569–577 的 TargetedSpecialPower 写法（schema：TargetedSpecialPowerUnitAbilityButtonTemplateData.xsd）；
  - StateData 复用全局现有的 ButtonStateAbilityEjectPassengersUntargetted（UI/ButtonStateDataCommon L914–920，Image AUA_Dropoff_Passengers，NAME/DESC:AbilityParadrop），所以**不需要新的 ButtonState，也不需要新字符串**；
  - RadiusCursor Target_Allied_Paradrop（UI/RadiusCursors L471，全局）三方共用（可逆技术项）。

### 2.8 Mod.xml
- 新增 2 条 all include：
  - `<Include type="all" source="DATA:Neutral/Structures/AirportTechStructure.xml"/>`（完整的 AssetDeclaration 根文件）；
  - `<Include type="all" source="DATA:Neutral/Structures/TechAirportParadrop.xml"/>`（同上）。
- SpecialPowerTemplates / LogicCommand / LogicCommandSet / UnitAbilityButtonTemplates / AirportTechStructureBuildable 已经在 Mod 里，不重复加。
- **不要**把 xi:include 片段（如 AlliedAirPowerUpgrade.xml）写成 all（见 92 / 92FIX 的教训）。
- **不复制** CampaignOverrides、CAMP_* 文件：所需字段已在新 ID 中重写，不引用任何战役专用 ID。

### 2.9 丢失、占领与停用
- 模块挂在建筑上：机场被摧毁、卖掉或被占领后，原主人失去按钮。【定 B；未证】
- 占领者按自己阵营的根科技显示对应按钮。【推；未证】
- 易主或摧毁后，SHARED_SYNC 计时的表现【未证】。

### 2.10 审计清单（cloud 交付后核对）
- 新 ID 全局唯一：
  - 3 架飞机 TechAirportParadropBomber_*；
  - 3 个 OCL_TechAirportParadrop_*；
  - 3 个 SpecialPower_TechAirportParadrop_*；
  - 3 条 Command_TechAirportParadrop_*；
  - TechAirportParadropCommandSet；
  - 3 个 ButtonTechAirportParadrop_*；
  - 6 个 ModuleTag_TechAirportParadrop_*（每个机场对象 3 个）。
- 中立机场与 SDK 逐元素比较，只差 CommandSet、3 个模块、1 条 include；2% 治疗不变。
- 可建造机场只改 Allied 一段，苏 / 日段落不变。
- SovietSupportBomber_Buildable、原袋狸、世纪轰炸机文件逐字节不变。
- SkirmishAI 中 grep 新 ID 为 0；LogicCommand 没有 AISpecialPowerInfo。
- 回归项：复制中心 1、幻影 80、86 兵营、93 / 95 / 96 / 97–99FIX、98 建造范围。

### 2.11 运行时必测（不得宣称已证）
1. 按钮按阵营出现；门控不满足时隐藏还是变灰。
2. 540s 计时三机场共享，易主后的表现。
3. 飞机从最近的地图边缘入场，飞到目标，逐个跳伞，然后飞离。
4. 跳伞落地正常。
5. 击落时剩余乘员是否被弹出，空中弹出后是生还还是摔死，有没有伞。**被弹出≠一定生还**。
6. 投放完毕后击落：机上已空，不应凭空生成步兵。
7. 2% 空中治疗仍然有效。
8. AI 不使用。
9. 袋狸模型显示正常（真实美术是否存在待编译；本机 w3x 是 75 B 占位文件）。
10. 盟军升级 AirPower 的加成对盟军版飞机无副作用。

## 3. 盟军 RA2 式建造范围（复制苏联同类半径）
- 元素：`<ProjectedBuildabilityInfo Radius=".." [RadiusY=".."] BuildPlacementTypes="MAIN_STRUCTURE OTHER_STRUCTURE" />`。
- 位置：GameObject 序列中 VisionInfo / CrusherInfo 之后、DisplayUpgrade 之前（AssetTypeGameObject.xsd L420–423，maxOccurs unbounded）。

| 盟军 ID | 对应苏联 ID | Radius / RadiusY | 包内是否已有盟军文件 |
|---|---|---|---|
| AlliedPowerPlant | SovietPowerPlant | 180 | 有 |
| AlliedBarracks | SovietBarracks | 195 | 有 |
| AlliedRefinery | SovietRefinery | 180 / 195 | 有 |
| AlliedWarFactory | SovietWarFactory | 240 | 有 |
| AlliedNavalYard | SovietNavalYard | 240 / 255 | 有 |
| AlliedAirfield | SovietAirfield | 270 | **无，需整文件复制 SDK** |
| AlliedTechStructure | SovietTechStructure | 210 | 有 |
| AlliedSuperWeapon | SovietSuperWeapon | 180 / 165 | 有 |
| AlliedSuperWeaponAdvanced | SovietSuperWeaponAdvanced | 180 / 165 | **无，需整文件复制 SDK** |
| AlliedBaseDefense / Advanced | Soviet 防御 = 0 | 不加（0 等同无） | 【推】 |

- **不动**：AlliedConstructionYard 600（含第二条海军船坞 AllowedObjectFilter 条目）、AlliedOutPost 390、全部日本半径（CY 600/585 等）、包内已有半径的中立可建科技建筑。
- AlliedCrane：SDK 中不可建，跳过【推】。
- **【缺】**
  - 包内新增的盟军建筑（AlliedQuickProductionCenter、AlliedStatueOfLiberty、地标、Rushmore 头像）在 SDK 中无苏联对应半径。
  - 苏联对应物（SovietQuickProductionCenter 等）包内也无 ProjectedBuildabilityInfo。
  - 按“复制苏联”的规则，这些建筑应为不加；如需扩展，由本人定。
- 性能注意：见 devdoc L1565。

## 待本人定（v4）
1. 新增的盟军非标准建筑是否也给建造范围（见 3）。
2. 帝国头像直接建造会继承 1.5 秒展开（与盟军版相同）；如果要严格 0 秒，需另外决定。
（机场击落：用户已定为尝试弹出，不再待定。）

## 附录 R：随机乘员伤亡研究（历史，**不作为实施要求**）
### R.1 击落时乘员随机伤亡：**未解决**（2026-11-09 00:31 UTC+10 修订，静态，全部未验证）
- **结论更正：** 上一版说“可以实现，只差 P”，这个结论**撤回**。目前**没有**确定可行的方案，所以不设 P，也不请用户接受“生成新兵代替生还者”。
- **真正的问题：** 有没有一种可靠方案，能让**机上剩余的真实乘员**按随机比例死亡或生还，同时不复制已经投下的步兵？要满足这一点，必须能做到以下之一：
  - 读到动态剩余人数和兵种计数；
  - 识别“部分已投放”的状态；
  - 让伤亡处理只在开始投放之前生效。
- **候选 C1（降级为未验证候选，非方案）：** KillPassengersOnDeath + 5 个 FireWeaponWhenDead（WeaponFireProbability ChancePercentage）+ WeaponOCLNugget 生成替身。
  - 先例：Includes/SovietTerrorDroneSpawnUpgradePlayerPower.xml；Weapon.xml L5369 TerrorDroneEggsPlayerPowerWeapon；FireWeaponWhenDeadBehavior.xsd；AssetTypeWeaponTemplate.xsd L464；DieMux.xsd L7–8；SovietAntiGroundAircraft L272 的 CONTAINER_OCCUPIED。
  - 缺陷：
    1. 生成的是新对象，**不是真实乘员生还**。
    2. 生成数量固定按 5 人算，不知道机上还剩几人、各是什么兵种。投放到一半被击落时，会凭空多出士兵，已投下的步兵等于被复制。
    3. CONTAINER_OCCUPIED 是否随清空而解除，以及 RequiredStatus 门控是否有效，都未证。
    4. 多个模块是否各自独立掷骰，未证。
- **候选 C2（未验证）：** 多个 SlowDeath 变体（SlowDeath.xsd L65 ProbabilityModifier 按权重随机选一个），各在 INITIAL 阶段用 Weapon（L39/58）发射 DamageContainedNugget（AssetTypeWeaponTemplate.xsd L586，MaxUnitsToDamage = k），再配合 EjectPassengersOnDeath="true"、KillPassengersOnDeath="false" 弹出剩下的人。
  - 优点：理论上作用于**真实剩余乘员**，最多伤 k 人；剩余不足 k 人时，自然只伤现有的人，不会复制。
  - 关键未证点：
    1. 乘员是在死亡瞬间（onDie）就被弹出或杀死，还是等 SlowDeath 武器打完后才处理？时序决定这个方案能否成立。
    2. DamageContainedNugget 的 SDK 先例（Weapon.xml 莫洛托夫弹头约 L3979、辐射场约 L8708）都是打**范围内被驻守的建筑**，打不打得到发射者自身的乘员，没有先例。
    3. 伤到哪几名乘员、是否随机，未知。
    4. 被弹出的步兵在空中落地是生还还是摔死，有没有伞，未证（步兵有 ParachuteDraw 包含，见 Includes/ParachuteDraw*.xml，但只证明有伞的外观）。
    5. RA3 schema（Schemas/xsd）中**没有 JetSlowDeath 模块**（检索 0 命中，只有 SlowDeath / HelicopterSlowDeath / ShipSlowDeath / ClearanceTestingSlowDeath）。包内 SovietSupportBomber_Buildable 本体没有直接写 SlowDeath（来自 BaseVehicle 或 include），C2 要先查清实际生效的死亡模块。
  - 静态无法确认，只能实测。
- **C3（确定性，不满足“随机”）：** EjectPassengersOnDeath + OpenContain DamagePercentToUnits（OpenContain.xsd），所有乘员受同等比例伤害，SDK 无使用先例。
- **按乘员数量分档的机制（有限检索结果）：**
  - schema 中没有找到“按当前乘员人数分档”的条件。
  - RIDER1–8、PASSENGER_VARIATION_1–5、WEAPONSET_PASSENGER_TYPE_* 只表示乘员类型或外观变体，没有逐项证实，不能当作人数计数。
  - HitPassengerPercentage（AssetTypeWeaponTemplate.xsd L968）是外部武器攻击驻军时命中乘员的比例，与自身死亡无关。
  - TransportContain 的 DestroyRidersWhoAreNotFreeToExit / ShouldThrowOutPassengers（TransportContain.xsd L28/L38）都没有随机或分档参数。
  - 没有找到“死亡时逐个乘员掷骰”的原生字段。
- **当前状态：** 没有确定可行方案，**不实施、不设 P**。真正可选的是：①全死（原版 KillPassengersOnDeath，默认继承）；②尝试弹出（可加 C3 的固定伤害）；③批准对 C2 做实测研究。这属于设计决定，交用户定。
- **公开核查（2026-11-09 00:36 UTC+10，按 unblock-research：3 次搜索 + 2 页 WebFetch，未超限）：**
  - 记忆：没有现成方法，只有一条记录显示“载具被毁乘员存活”在你的 RA2 化愿望清单里。
  - 搜索 1（web，带 "Grok Bot" OR "@bot"）：命中的是 RA2 / Ares。
  - 搜索 2（web，RA3 SDK 关键词）：命中 BFME2 SAGE 参考、ModDB RA3 XML 索引教程、红警 DIY 论坛的残骸模型帖，**都没有 RA3 随机乘员存活的实现**。
  - 搜索 3（X 公开帖，"Grok Bot"/@bot + RA3 + passengers/transport/eject）：0 条结果。
  - 实际读过的页面：
    1. https://deathfishatease.github.io/Ares-docs/new/survivors.html ——Ares（RA2 / YR 的 ini 扩展）的 Survivor.PassengerChance 正好是“每名乘员独立概率生还、空中载具也适用”。这是 RA2 引擎扩展，**不能作为 RA3 证据**，只说明这种需求在 RA2 系是靠引擎扩展实现的。
    2. http://rcmod.the3rdage.net/wiki/class_s_a_g_e_1_1_transport_contain.html ——BFME2 / ROTWK（同为 SAGE 引擎，但不是 RA3）的 TransportContain 说明：DamagePercentToUnits 是“本体受到伤害的这一百分比转给乘员”，EjectPassengersOnDeath 是死亡时释放乘员，KillPassengersOnDeath 是死亡时杀死乘员，**没有随机参数**。RA3 的同名字段语义是否一致未证。
      - 由此只得到一个**未验证**的思路：DamagePercentToUnits 传伤 + 死亡弹出，不同兵种血量不同，可能只活下部分人。但这是确定性的，不是随机，同兵种结果相同。
  - **结论：** 没有找到公开、可验证的 RA3 原生随机乘员伤亡实现。这**不等于**引擎做不到。
  - 真实选项：
    - ①等原生编译后，实测 C2 / DamagePercentToUnits 再研究；
    - ②用户接受全死；
    - ③用户接受尝试弹出。
  - 不自行选择，不改变 devdoc 的“随机”要求。
- 研究范围：本机 SDK XML 和 schema，加上述有限公开核查；不承诺可行。

