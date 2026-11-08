# BATCH99_AUDIT — ra3v2_phase2_batch99（帝国总统山头像改为直接建造；静态独审，编译和实测都没做，不是最终验收）
审计时间：2026-11-09 04:02（UTC+10）

## 包
- 362707 B，sha256 0698683768a162cd13ab9b2869e6ccadb904bb00abbea4bbf0e2b0bee35ba43b，与报告一致。
- 已存为 /workspace/ra3xfer/batch99.tar.gz，解包到 /workspace/b99/data。
- 149 个 XML；Mod.xml 144 条 all。4 个改动文件都能被 ElementTree 正常解析。
- 与 98 比较（diff -rq 实测）：
  - 删除 Japan/Eggs/JapanRushmoreLaserHeadEgg.xml；
  - 修改 Mod.xml、LogicCommand、LogicCommandSet、MR_LaserMtRushmore_Lincoln_Ready 四个文件；
  - 其余 145 个逐字节相同。

## 结论：**硬 FAIL（F1）**

### F1：建造命令类型错误，不是直接建造
- Command_ConstructJapanRushmoreLaserHead 的 **Type="UNIT_BUILD"**，只是把命令 id 和 Object 换成了头像。
- 包内所有在建造场直接放置的建筑都用 **Type="CONSTRUCTION_YARD_CONSTRUCT"**：
  - 盟军头像（LC L86–88）、苏联头像（L80–82）；
  - 帝国装饰 JapanImperialAdminBuilding / EmperorFlagpoleStatue（L93–99）；
  - JapanQuickProductionCenter（L229–231）；
  - JapanAirportTechStructureBuildable（L196–198）。
  
  SDK 中这种类型共 38 处。
- 帝国建造场（与 SDK 相同）有 ProductionUpdate MAIN_STRUCTURE / OTHER_STRUCTURE 和 QueueProductionExitUpdate，后者用于蛋这类 UNIT_BUILD 出厂的单位。
- 用 UNIT_BUILD 会把建筑当作单位排队，从出生点出厂，没有放置流程。这与用户 03:54 要求的“类似盟军直接建造”不符。
- **修法（只指出，不改）：** 把 Type 改为 CONSTRUCTION_YARD_CONSTRUCT，与盟军头像命令逐字同构；其它不动。

### 静态通过的项
- 核心文件已删，Mod 中的 core include 已删，全包 grep JapanRushmoreLaserHeadEgg 为 **0 残留**。
- LogicCommandSet 中 JapanConstructionYardCommandSet 的条目已换成新命令，位置不变。
- 共享的展开命令保留：
  - JapanWaveForceTripleCannonEggCommandSet 仍在（LCS 中 2 处引用，三门炮蛋 1 处）；
  - Command_UnPackJapanBaseDefenseAdvancedEgg 来自 SDK LogicCommand，未被删。
- 帝国头像现在与盟军头像逐元素同构，只差 id、Side=Japan、RequiredObject JapanTechStructure：
  - BuildTime 30.0、造价 2000、前提 JapanTechStructure；
  - KindOf +POWERED +SCORE −UNATTACKABLE −NOT_AUTOACQUIRABLE（FS_BASE_DEFENSE 由基类继承）；
  - 耗电 -75、视野 1250/1250、HP 2000；
  - 武器 SovietRushmoreLaserHeadWeapon（射程 1150）、转速 360、没有 MaxDeflection；
  - 无限额，没有加入 SkirmishAI（grep 0 命中）。
- Ready 文件 L7–8 的两条 ART all include 保留。
- 盟军、苏联头像所在段落没有改动；diff 只涉及帝国段落。
- PlacementViewAngle 225d 继承自 BaseMountRushmoreHead L83，与盟军头像相同。

## 关于默认的 1.5 秒展开（不能说成 0 秒）
- 删掉 25s 覆盖后，帝国头像会继承 BaseMountRushmoreHead L121–123 的 **StructureUnpackUpdate UnpackTime="1.5s"**。
- 盟军头像本来就没有覆盖，同样继承 1.5s。苏联头像覆盖为 30s，这是旧批次的写法，这里不评价。
- cloud 说“没有等待”**没有证据**：静态上存在 1.5 秒展开。
- 这是与盟军版完全相同的继承机制，不算新的设计偏差。但实际体验是“30 秒建造 + 约 1.5 秒展开”，而且 1.5 秒内能否开火、能否被攻击，都是**运行时待测**。用户如果要求严格 0 秒，需另外决定。

## 回归
以下内容所在的文件全部逐字节等于 98，均保留：
- 98 建造范围；
- 97 ART include；
- 96 袋狸；
- 95 军衔表；
- 93 候选改动；
- 86 兵营；
- 复制中心限额 1；
- 幻影坦克速度 80。

## 未证
- 没有编译，也没有实测。
- 修正 F1 后仍需实测：放置、悬空表现、1.5 秒展开、低电停火、按钮和字符串（Name:JapanRushmoreLaserHead 等新键需要翻译）。

## 已登记的用户决定（03:55）
- 机场空降飞机被击落时，**尝试弹出剩余乘员**，以此覆盖原来的“随机”要求；实际能否生还待测。
- 研究文档稍后同步。
