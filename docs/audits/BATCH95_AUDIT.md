# BATCH95_AUDIT — RA3_V2.0_Batch95_AdvancedMirage（静态独审，运行时/编译未证，非最终验收）
包：353896 B，sha256 cfd320410d174fe1aa5410dfe4d1bd693466eb13f6d7e2337419f0163e89c99b，与指令一致。已存为 batch95.tar.gz，解包到 /workspace/b95/data。未使用 host 片段。
144 个 XML；Mod.xml 139 条 all + 3 条 reference。
与 94 相比：新增 Allied/Units/AlliedAdvancedMirageTank.xml，修改 Mod.xml、LogicCommand、LogicCommandSet 三个文件，其余 140 个逐字节相同。
四个文件的根都是 AssetDeclaration，ElementTree 均能正常解析。

## 结论：静态 FAIL（1 项硬缺陷）

### F1（FAIL）：UnitIntro 指向不存在的资产
- 新文件 L22 写的是 `UnitIntro="Allied_AdvancedMirage_UnitIntro"`。
- schema 中该属性类型为 UnitIntroRef（AssetTypeGameObject.xsd L518），属强引用。
- 全 SDK（GlobalData/UnitIntros.xml）和包内都没有这个 id，只有普通幻影用的 Allied_MirageTank_UnitIntro（UnitIntros L172）。
- CAMP_A08 没有这个属性，我的规格 NEXT_ADVANCED_MIRAGE 也没有要求，这是 cloud 自行编造的。
- **最小修正：** 删除该属性，从父类继承 Allied_MirageTank_UnitIntro；或者直接写 Allied_MirageTank_UnitIntro（不自修）。

## 与 SDK CAMP_A08_SpecialMirageTank.xml 逐元素对比（去掉空白和注释后）
差异只有以下几处，均符合 NEXT_ADVANCED_MIRAGE 规格：
- id 和 EditorName 改为 AlliedAdvancedMirageTank；EditorSorting 改为 UNIT；新增 Side="Allies"。
- KindOf 加 T3_UNIT，保留 MOVE_FOR_NOONE。
- 按钮和头像复用普通幻影：Button_AlliedAntiVehicleVehicleTech3_on / Portrait_AlliedAntiVehicleVehicleTech3。
- 新增 BuildTime 15、造价 1500、RequiredObject AlliedTechStructure（国防局）。
- LocomotorSet 用同一 locomotor AlliedAntiVehicleVehicleTech3Locomotor，Speed 从 20 改为 80.0，与包内普通幻影的 80.0 相同。
- InvisibilityBroadcastUpdate 的 UpdatePeriod 从 0.01s 改为 0.2s（规格项）。
- Include 变化：FAKE 和 IDLZ 两个模型从 instance 改为 all（规格项，有包内快速生产中心先例）；EX_Headlights 和 EXCloakingField 两条去掉，二者均为全局资产（规格项）。
- 新增 F1 中的 UnitIntro（缺陷）。

**其余内容全部与 CAMP_A08 相同：**
- MaxHealth 2000，视野 200/200；
- 幻影场 BroadcastRange 225，使用 A08 隐身模板（SDK GlobalData/InvisibilityTemplates.xml L23，经 Static.xml 全局加载）；
- 场开关 ToggleStatus，A08 音效；
- FAKE / 斗篷场 Draw；
- 碾压参数和 AI 状态机。

**继承自父类（包内普通幻影）的部分：** 武器（含 R89 移动射击）、死亡、其它技能。新文件没有改动这些。
devdoc 没有规定限额，新文件也没有设限，未自行扩展。

## 命令
- LogicCommand：新增 Command_ConstructAlliedAdvancedMirageTank（UNIT_BUILD，Object 为新单位），id 唯一。
- LogicCommandSet：AlliedWarFactoryCommandSet 在包内首次覆盖，文件内唯一。与 SDK LCS L185–196 相比：
  - 7 条原命令按原顺序全部保留；
  - 新命令插在 Tech3（普通幻影）之前；规格写的是“紧跟普通幻影之后”，顺序偏差只影响按钮位置，不影响合法性；
  - SDK 中的 RepairBay 升级命令原本就是注释状态，不算遗漏。
- AlliedWarFactory.xml 仍引用 AlliedWarFactoryCommandSet。
- Mod.xml 新增一条 type="all" include，目标是 AssetDeclaration 根。

## 风险 / 未证（非本批硬 FAIL，但必须列明）
- **R1 等级（老兵）表：**
  - ExperienceLevelTemplate 的 Target 是按 ID 匹配的弱引用；SDK 中只有 AlliedAntiVehicleVehicleTech3 有等级表，A08 本来就没有。新 ID 没有出现在任何 Target 里。
  - 静态反证线索：SDK 实际可造的 AlliedAntiInfantryVehicle_Ground 继承 AlliedAntiInfantryVehicle，同样没有自己的 Target。但这条“继承即可升级”的证据不能视为已证（此前已定：IFV 先例不得称为已证）。
  - 所以新单位能否升级是未证项。cloud 测试清单写了 veterancy progression，却没有提供等级表。
  - 如需确保，应按 ExperienceLevels_SovietSpy 的先例，为 AlliedAdvancedMirageTank 补 4 级等级表（Target 写新 ID，数值照抄 SDK ExperienceLevels L362–390）。是否要求升级由用户决定。
- **R2 字符串：**
  - Name:/Desc:/Type:AlliedAdvancedMirageTank 是新键，包内没有字符串文件，不能说显示已证。
  - devdoc L589⑥ 规定了文字内容，属于全项目翻译、字符串批的待完成项。
  - SDK 有可复用的战役键 Name:MeerageTank / DESC:MeerageTank / TYPE:MeerageTank（CAMP_A08 原用，static.manifest 中有相应的 Portrait 和 Button），但那是战役文字，与 devdoc 规定的文字不同，不建议用来替代。
- **R3 美术：** FAKE 和 IDLZ 的 w3x 只在本机 bibber/Art 提取树中存在，build 机的 ART 路径里是否有它们，只能编译时验证。
- **R4 运行时：** FAKE 模型叠加效果、幻影场、速度 80、建造前置条件。

## 不回退
- 普通幻影 AlliedAntiVehicleVehicleTech3.xml 逐字节未动（Speed 80，造价 1500）。
- 复制中心限额 1，以及 89–94 的全部内容，均在逐字节相同的文件里。
- 93 的 D1 / D4 / AI 时机仍待用户批准，不因本批而改变。
