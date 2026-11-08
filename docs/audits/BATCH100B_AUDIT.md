# BATCH100B_AUDIT — 科技机场空降：OCL 与能力模板（静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 04:22（UTC+10）。基线：100A。规格：NEXT_PHASE2_FINAL.md v4 §2.2 A2、§2.6。

## 包
- 363833 B，sha256 494d35d7b510c43a11b86028faa5aec477f011ee2e2521b8bc20935106d6e39c，与报告一致。
- 已存为 /workspace/ra3xfer/batch100b.tar.gz，解包到 /workspace/b100b/data。
- 150 个 XML。
- 与 100A 比较（diff -rq 实测）：只改了 TechAirportParadrop.xml 和 GlobalData/SpecialPowerTemplates.xml，其余 148 个逐字节相同。Mod.xml 没有改。
- 两个文件都能被 ElementTree 正常解析。

## 结论：静态 PASS（候选），无硬错
- **D1 已修：** L5 改为 type="instance"。三架飞机对象本身的 diff 为 0，没有其它改动。
- **3 个 OCL（OCL_TechAirportParadrop_Allied / _Soviet / _Japan）：**
  - 结构与 SDK OCL_CAMPAlliedBomberDrop1 同构（CreateObject 属性 → Offset → 子 CreateObject）；
  - Options 为 "IGNORE_ALL_OBJECTS DONT_SET_PRODUCER ISSUE_MOVE_AFTER_CREATION FIRE_SPECIAL_POWER"，**没有** CREATE_AT_TARGET，也没有 MOVE_TARGET_USES_OFFSET；
  - Disposition LIKE_EXISTING，FireSpecialPowerTemplate SpecialPower_EjectPassengers，Offset 0/0/190；
  - 每个 OCL 1 架，并且各自对应正确阵营的飞机。
  - 与 v4 A2 逐字一致。OCL 写在对象文件里，有 SDK 先例（CAMP_Infantry_1、中立机场文件内的 Die_OCL）。
- **3 个 SpecialPowerTemplate：**
  - ReloadTime 540s、TargetType LOCATION、RadiusCursorRadius 100；
  - EvaEventToPlayWhenSelectingTarget SelectSpecialPowerTargetArea，全局存在：Sounds/Eva.xml L1896，经 MasterAudioEvents 以 all 载入；
  - Flags 为 IS_PLAYER_POWER PATHABLE_ONLY NOT_CLIFF_CELL NO_FORBIDDEN_OBJECTS SHARED_SYNC，都是 schema 枚举值；
  - RequiredPlayerTech 分别为 PlayerTech_Allied / _Soviet / _Japan，定义在 SDK System/PlayerTechs.xml（包内没有覆盖）；
  - ForbiddenObjectFilter 与 SpecialPowerParadropLvl1 逐字相同（ExcludeThing NanoSwarmHiveEffect 定义在 SDK Japan/Props）；
  - 没有 GameDependency / ForbiddenPlayerTech 等战役字段，没有 AI 字段；
  - 插在文件末尾 SpecialPower_AlliedCommandoSprint 之后、</AssetDeclaration> 之前，位置合法。
- 新 ID 在包和 SDK 中各只出现 1 次。
- **依赖闭合：** OCL → 飞机（100A）→ SpecialPower_EjectPassengers（包内覆盖文件中存在）；模板 → PlayerTech / Eva / NanoSwarmHiveEffect，全部存在。

## 加载风险（不能因为“还没接线”就说没有影响）
- 新资产在构建时**会被编译和载入**（新文件由 Mod L123 以 all 载入；SpecialPowerTemplates 已在 Mod 中）。即使还没接线，悬空引用和重复 ID 也会在编译时报错。本批静态上没有发现这两类问题，但是否编译成功仍待验证。
- 三个模板目前没有任何 OCLSpecialPower 引用，属于设计上的分阶段状态，不是缺陷。
- RequiredPlayerTech 用阵营根科技做门控，没有 SDK 先例。SHARED_SYNC 共享计时、AI 不使用（没有 AI 字段只代表没有给 AI 提示）都**未证**。

## 回归
以下内容所在的文件全部逐字节等于 100A，均保留：
- 三架飞机对象（D1 那一行除外）；
- 原袋狸、世纪轰炸机；
- 头像直接建造、97 ART include；
- 98 建造范围；
- 96 袋狸、95 军衔表、93 候选改动、86 兵营；
- 复制中心限额 1、幻影坦克速度 80。

## 运行未证
- 编译。
- 边缘出生、航线、到点逐个跳伞、飞离地图。
- 540 秒共享计时。
- 根科技门控下按钮隐藏还是变灰。
- AI 不使用。
- 击落时弹出剩余乘员，以及他们是否生还。

## 100C 接续摘要（机场和 UI，v4 §2.3–2.8）
1. 新建 Neutral/Structures/AirportTechStructure.xml，逐字复制 SDK，只增加以下几处：
   - CommandSet="TechAirportParadropCommandSet"；
   - Behaviors 末尾 3 个 OCLSpecialPower：
     `<OCLSpecialPower id="ModuleTag_TechAirportParadrop_X" SpecialPowerTemplate="SpecialPower_TechAirportParadrop_X" OCL="OCL_TechAirportParadrop_X" DestinationOCL="OCL_PrecisionStrikeBeacon" CreateLocation="CREATE_AT_EDGE_NEAR_SOURCE"/>`
   - Includes 加 `<Include type="instance" source="DATA:Neutral/Structures/TechAirportParadrop.xml"/>`；
   - 2% 治疗保留。
2. 包内 AirportTechStructureBuildable.xml：只改 AlliedAirportTechStructureBuildable，加同样的 CommandSet、3 个模块和这条 instance include。苏 / 日继承，不要分写。
3. LogicCommand 加 3 条：Type SPECIAL_POWER、Options NEED_TARGET_POS、指向对应的 SpecialPower，没有 AISpecialPowerInfo。LogicCommandSet 新建 TechAirportParadropCommandSet，含这 3 条。
4. UnitAbilityButtonTemplates 加 3 个 ButtonTechAirportParadrop_X：
   - TargetedSpecialPower，RadiusCursor="Target_Allied_Paradrop"；
   - StateData="ButtonStateAbilityEjectPassengersUntargetted"，ValidTargetCursor="TargetAbility"；
   - 不新建 ButtonState，也不新建字符串。
5. Mod.xml 只新增中立机场的 all include，其它文件不重复加；不得把 xi 片段写成 all。
6. 审计时比较：中立机场与 SDK 逐元素只差上述 3 项；可建造机场只有 Allied 段有改动；飞机、OCL、模板逐字节不变。

## 对验证 md 的更正
- L197 写“No AISpecialPowerInfo: AI will NOT use this ability”，**说法过头**。没有 AI 字段，只能说明没有给 AI 提示；AI 是否真的不用，属运行时未证。
- L315 写“Verified against SDK schema ✅”只是静态结构核对，不是编译验证。
- L302 写 SpecialPower_EjectPassengers “exists in SDK/base game”，正确（包内覆盖的 SpecialPowerTemplates.xml 也有）。
