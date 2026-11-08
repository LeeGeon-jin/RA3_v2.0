# BATCH96_AUDIT — ra3v2_phase1_batch96（袋狸，静态独审，编译/运行未证，非最终验收）
包：355763 B，sha256 ffc1667d9a4adb0f4495bba0bb204aa08bec7f921901c405c3b603c9a1a8b008，与报告一致。已存为 batch96.tar.gz，解包到 /workspace/b96/data。
147 个 XML；Mod.xml 142 条 all + 3 条 reference。
与 95FIX2 相比：新增 SovietSupportBomber_Buildable.xml、ExperienceLevels_Badger.xml；修改 Mod.xml、LogicCommand、LogicCommandSet 三个文件；其余 142 个逐字节相同。5 个文件均能被 ElementTree 正常解析。

## 结论：硬 FAIL（1 项）

### F1（FAIL）：建造命令使用了 schema 中不存在的元素
- LogicCommand L252–256：`Command_ConstructSovietSupportBomber_Buildable` 写的是 `<UnitBuild>SovietSupportBomber_Buildable</UnitBuild>`。
- AssetTypeLogicCommand.xsd L52–55 只定义了 SpecialPower / Upgrade / **Object** / AISpecialPowerInfo，没有 UnitBuild。全 SDK 也找不到 `<UnitBuild>`。包内其余 39 条建造命令都用 `<Object>`。
- 后果：schema 校验失败，或者命令没有绑定单位，按钮无法建造。
- **最小修正：** 改为 `<Object>SovietSupportBomber_Buildable</Object>`（不自修）。

## 其余部分：静态合规
- **与包内世纪轰炸机 AlliedBomberAircraft.xml 逐元素对比**（去掉空白后），差异只有以下几处：
  - id、EditorName、Name / Desc / Type 键改为 SovietSupportBomber_Buildable；Side 改为 Soviet。
  - RequiredObject 由 AlliedTechStructure 改为 SovietTechStructure（作战实验室）。
  - 图标与头像用 Button_PlayerPower_DesolatorBomb1（SDK ButtonStateDataCommon L814 的现存 Image），不是伪造的引用。
  - 删除了 UnitIntro="Allied_CenturyBomber_UnitIntro"。这是安全的减法，没有虚构新 intro，但与“其余全保留”有偏差：苏军单位用盟军介绍本就不合适，记录在案，由用户知悉。
  - Draw：世纪的两个 ScriptedModelDraw（主体与 FX，含 USER_2 升级模型、PRK / HVRA / MOVA 动画）整体换成 SDK BaseSovietSupportBomber L49–118 的袋狸 Draw，逐行一致：模型 SUSupportBomber，ExtraPublicBone 与 WeaponLaunchBone 都是 SUSUPPORTBOMBER，4 个尾迹 Box01–04，LOOP 动画，DAMAGED / REALLYDAMAGED 状态。
  - 删除 SubObjectsUpgrade ModuleTag_AlliedAirPower_subobject（规格允许）。
- **其余全部与世纪相同：**
  - 造价 2000，建造 20 秒；KindOf 与世纪相同，含 LIMITED_PRODUCTION_AIRCRAFT 与 AIRCRAFT_TRANSPORT_ONLY_GARRISONABLE_WHILE_PARKED，不含 SUMMONED。
  - TransportContain ContainMax 5，只装 INFANTRY；弹出能力（Untargeted）；炸弹武器 AlliedBomberAircraftBombWeapon（含 _AirPower 槽）。
  - JetAIUpdate（停机、返航补弹），TAXIING locomotor，护甲、血量、死亡；盟军 AirPower 的 include 与 StatusBits（苏军不会触发）。
  - 美术：SUSupportBomber 来自全局（Soviet.xml → BaseSovietSupportBomber 的 ART include），本文件不再 include。
- **CommandSet：** 仍是 SDK AlliedBomberAircraftCommandSet，即 Command_ActivateEjectPassengersSpecialPowerUntargeted + Command_AttackMove，弹出齐全。cloud 报告写成“return + attackmove”与实际不符，属报告错误。世纪原版本来就没有返航按钮，弹药耗尽后由 JetAI 自动返航。
- **SovietAirfieldCommandSet**（包内首次覆盖，文件内唯一）：SDK L367–372 的 4 条原命令按原顺序全部保留，新命令插在 Recall 之前，共 5 条。
- **等级表 ExperienceLevels_Badger：** 父 include 为 instance；4 个 id 唯一；inheritFrom 为 ExperienceLevel_SovietRank1–4（SDK L93–102）；前提链 1→2→3→4；Target 为新 ID；数值 1/2000、6000/4000、12000/6000、18000/8000，与世纪 AlliedBomberAircraft 完全一致；Mod.xml 以 all 加载。
- **Mod.xml：** 两条 all include，目标根都是 AssetDeclaration。
- **原对象未动：** 原召唤袋狸 SovietSupportBomber（SDK）和包内世纪文件都没有改动。
- **AI：** 包内没有任何 SkirmishAI 文件引用新 ID，所以 AI 静态上不会造；运行时未证。

## devdoc 禁令分别核对（不替用户扩展）
- “任一项不过即整项取消，不做替代”和“AI 默认不造”只出现在**精准轰炸机**条目（L644/L649–650）。袋狸条目（L887–896）里没有这两条。
- cloud 把取消规则贴到了袋狸上，是报告错误。袋狸只是不加 AI 表的最小默认做法，不是用户禁令。
- 精准轰炸机本批未做；其军衔 widget 未答，不自行造值。

## 运行时未知
1. 停机坪停放、滑行、垂直起降、攻击、返航补弹。
2. 步兵登机与弹出：SU 模型没有 BONEGARRISON 骨骼，乘员只能以 ENCLOSED 方式承载。
3. 炸弹从 SUSUPPORTBOMBER 骨骼投下。
4. 螺旋桨动画在停机时是否正常。
5. 军衔升级。
6. 图标和字符串显示（字符串待全项目翻译）。
7. AI 不造。

## 不回退
普通幻影与高级幻影 80、复制中心限额 1、93 的候选改动，以及 89–95FIX2 的全部内容，均在逐字节相同的文件里。93 的 D1 / D4 / AI 时机设计差异仍待用户批准。
