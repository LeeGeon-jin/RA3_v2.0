# BATCH97_AUDIT — ra3v2_phase2_batch97（日本 Rushmore 头像，静态独审，编译/运行未证，非最终验收）
包：356234 B，sha256 60e92383b3864ff45563bba9fbdc63113a71389edbb023d7984ace13b502bf7e，与报告一致。已存为 batch97.tar.gz，解包到 /workspace/b97/data。
148 个 XML；Mod.xml 143 条 all + 3 条 reference。
与 96FIX 相比：新增 Japan/Eggs/JapanRushmoreLaserHeadEgg.xml；修改 MR_LaserMtRushmore_Lincoln_Ready、LogicCommand、LogicCommandSet、Mod.xml 四个文件；其余 143 个逐字节相同。5 个文件均能被 ElementTree 正常解析，新 id 唯一。

## 结论：静态 PASS（候选）
- **核心车（与包内三门炮蛋逐元素对比）：** 差异只有以下几项：
  - id / EditorName。
  - 图标 Portrait_HeadLincoln_robot / Button_HeadLincoln_robot（Ready 原有，非伪造）。
  - Desc / Type / Name 新键（字符串待全项目翻译）。
  - BuildTime 3 → 5。
  - 删去 RequiredObject JapanPowerPlant，只留 JapanTechStructure。
  - 造价 2500 → 2000。
  - ReplacementTemplate 改为 JapanRushmoreLaserHead。
  
  标准 PackTime 3.0s 保留；CommandSet 复用 JapanWaveForceTripleCannonEggCommandSet（内容为 Command_UnPackJapanBaseDefenseAdvancedEgg，合法的最小复用）；JUEgg Draw、KindOf 和 include 原样保留。
- **本体 JapanRushmoreLaserHead：**
  - inheritFrom MR_LaserMtRushmore_Lincoln_Ready，Side Japan。
  - KindOf 采用与盟/苏相同的增量写法，从 BaseMountRushmoreHead L80 继承 FS_BASE_DEFENSE。
  - EnergyProduction -75；BuildCost 2000（仅用于退款和计分）；不写 BuildTime 和 GameDependency。
  - VisionInfo 1250/1250。
  - `StructureUnpackUpdate id="StructureUnpackUpdate" Replace UnpackTime="25s"`，与基类 id 相同，写法与苏军版一致。
  - WeaponSetUpdate Replace：SovietRushmoreLaserHeadWeapon（AttackRange 1150），TurretTurnRate 360，不写 MaxDeflection。
  - ActiveBody 2000。
  - Draw 和其余 behaviors 继承自 Ready 与 Base，没有改动。
- **原有对象未篡改：** 逐块抽取后比对，MR_LaserMtRushmore_Lincoln_Ready、SovietRushmoreLaserHead、AlliedRushmoreLaserHead 三个块与 96FIX 完全一致。diff 中出现的盟军块只是对齐假象。
- **Ready 文件新增 2 条 ART include：** `ART:MR_LaserMtRushmore_Lincoln.W3X`、`ART:MR_LaserMtRushmore_Lincoln_COL.W3X`，type all。
  - 路径和大小写与 SDK 原版 Ready L7–8 逐字相同，恢复的是 SDK 原写法。
  - 全包只有这一处引用，没有重复 include。
  - 盟/苏/日三版头像都受益（devdoc L788 风险①）。
- **命令：**
  - Command_ConstructJapanRushmoreLaserHeadEgg 为 UNIT_BUILD，用 `<Object>`，合 schema。
  - 加入 JapanConstructionYardCommandSet，紧跟在三门炮蛋之后，原有按钮全部保留。
  - Mod.xml 新增核心车 include，type all，目标根为 AssetDeclaration。
- **AI、限额、军衔：** 均未添加（符合 devdoc）。

## 更正此前说法
- 本机 bibber/Art 下的 w3x（mr_lasermtrushmore_lincoln* 以及此前 95 审计提到的 auantivehiclevehicletech3_fake / _idlz）都**只是 75 字节的空 AssetDeclaration 占位文件**，不是真模型。
- 所以“源文件存在于本机”只能证明名称存在，不能证明模型可用。build 机的 ART 路径里是否有真模型，只能在编译时验证。

## 未编译 / 未实测
1. 墙钟时间约 5 + 3 + 25 = 33 秒，是否严格要 30 秒待用户确认口径。
2. 模型显示：三版头像的 ART include 能否在 build 机解析。
3. 激光射程 1150，可以朝背后开火。
4. 低电时停火。
5. 退款金额。
6. 按钮和字符串显示。
7. 新加的 ART all include 是否与全局流中的资源重名冲突。

## 不回退
复制中心限额 1、幻影 80、95 的军衔表、96 的袋狸、93 的候选改动，均在逐字节相同的文件里。93 的 D1 / D4 / AI 时机设计差异仍待用户批准。
