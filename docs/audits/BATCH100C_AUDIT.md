# BATCH100C_AUDIT — 科技机场空降：机场与 UI 接线（静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 04:31（UTC+10）。基线：100B。规格：NEXT_PHASE2_FINAL.md v4 §2.3–2.10。

## 包
- 364341 B，sha256 d616fd1486d1f7e05eef93d6903ba55a4a8cc1eb2ddba25f3f03aed67f9bf92b，与报告一致。
- 已存为 /workspace/ra3xfer/batch100c.tar.gz，解包到 /workspace/b100c/data。
- 151 个 XML；Mod.xml 146 条 all + 3 条 reference（static / global / audio）。
- 与 100B 比较（diff -rq 实测）：
  - 新增 Neutral/Structures/AirportTechStructure.xml；
  - 修改 Mod、LogicCommand、LogicCommandSet、UnitAbilityButtonTemplates、AirportTechStructureBuildable 五个文件；
  - 其余 145 个逐字节相同。
- TechAirportParadrop.xml 和 SpecialPowerTemplates.xml 用 cmp 核对，与 100B **逐字节相同**。
- 6 个改动或新增文件都能被 ElementTree 正常解析。

## 结论：静态 PASS（候选），无硬错

### 中立机场：与 SDK 比较（diff --strip-trailing-cr）
只多了 3 处：
1. Includes 末尾加 `<Include type="instance" source="DATA:Neutral/Structures/TechAirportParadrop.xml"/>`；
2. 对象属性 CommandSet="TechAirportParadropCommandSet"；
3. Behaviors 末尾（LUAEventList 之后）加 3 个 OCLSpecialPower。

其余逐行与 SDK 相同：ART include、Draw 和旗帜 xi:include、BuildingDestruction、FX、Die、CreateObjectDie、2% PassiveAreaEffect（AIRCRAFT VEHICLE HUGE_VEHICLE / ALLIES / AIRBORNE_TARGET）、EngineerContain 和 Repair xi:include、LUAEventList、Body、Geometry、Audio、Vision、Buildability、文件内的 Die_OCL。唯一的格式差异是换行符（SDK 为 CRLF），不影响内容。

### 可建造机场
- 只改 AlliedAirportTechStructureBuildable 一段：同样的 instance include、CommandSet 和 3 个模块（放在 LUAEventList 之后、</Behaviors> 之前）。
- 苏 / 日两段逐字未改，继续继承 Allied；苏联段的 Behaviors 只追加了 StructureUnpackUpdate，不会覆盖新模块。
- 2% 治疗保留。

### OCLSpecialPower ×3（两个机场相同）
- SpecialPowerTemplate、OCL 按阵营一一对应。
- DestinationOCL="OCL_PrecisionStrikeBeacon"（SDK ObjectCreationLists L1085，由全局 reference 提供），CreateLocation="CREATE_AT_EDGE_NEAR_SOURCE"。
- 与 CAMP_PowerStore 先例同构。
- 模块 id ModuleTag_TechAirportParadrop_* 在每个对象内唯一，与基类没有冲突。

### 依赖链（逐跳核实）
1. 按钮 ButtonTechAirportParadrop_X → LogicCommand="Command_TechAirportParadrop_X"
2. 命令（Type SPECIAL_POWER、Options NEED_TARGET_POS、没有 AISpecialPowerInfo）→ SpecialPower_TechAirportParadrop_X（100B）
3. 模板 → 机场上同模板的 OCLSpecialPower → OCL_TechAirportParadrop_X → TechAirportParadropBomber_X（100A）
4. 飞机 → SpecialPower_EjectPassengers、RunOffMap

三个阵营各自对应正确，命令集 TechAirportParadropCommandSet 含 3 条命令。

### UI 引用
- StateData ButtonStateAbilityEjectPassengersUntargetted、RadiusCursor Target_Allied_Paradrop、ValidTargetCursor TargetAbility（GlobalData/MouseCursors）都是 SDK 全局 ID，包内文件没有重新定义它们。
- 能否解析，依赖 Mod.xml 对 static.xml / global.xml 的 reference。包内 ButtonStateDataCommon 只有 2 个条目，UnitAbilityButtonTemplates 只有 7 个条目，一直靠这个机制取得其余原版 ID（与 93、Yari 冲刺等先例相同）。这是**编译时项**。
- 按钮模板的 schema 类型为 TargetedSpecialPower，与 SDK ButtonEjectPassengers 同构。插在文件内 ButtonToggleAfterburners 之后，位置合法。

### 其它
- 所有新 ID 在包和 SDK 中唯一。
- Mod.xml 只新增中立机场一条 all include，没有把片段误写成 all。
- SkirmishAI 没有引用任何新 ID；LogicCommand 没有 AI 字段。这只说明没给 AI 提示，**不能说成 AI 一定不用**。

## 回归
以下内容所在的文件全部逐字节等于 100B，均保留：
- 飞机、OCL、模板；
- 原袋狸、世纪轰炸机；
- 帝国头像直接建造、97 ART include；
- 98 建造范围（盟军建筑文件没有改动）；
- 96、95、93 候选改动、86 兵营；
- 复制中心限额 1、幻影坦克速度 80。

## 运行时必测（静态审计不能替代）
1. 编译，包括中立机场覆盖后是否与 static 流里的原版定义冲突，以及 UI ID 能否通过 reference 解析。
2. 按钮按阵营出现；根科技门控下按钮是隐藏、变灰，还是三个都显示。
3. 540 秒计时在多座机场之间共享，机场易主后的表现。
4. 飞机从最近的地图边缘入场，飞到目标，逐个跳伞，然后飞离；目标信标显示正常。
5. 击落时剩余乘员是否被弹出，空中弹出后是否生还、有没有伞。
6. 2% 空中治疗仍然有效。
7. AI 不使用。
8. 丢失机场后不能再用。
9. 袋狸美术是否存在（本机 w3x 是 75 B 占位文件）。

## 第二批剩余范围交叉核对
依据：PHASE2_SCOPE（22:15）B / C 表、NEXT_BOMBERS、进度文档、各批审计。
- 已有静态 PASS 候选（都还要编译和实测）：
  - 幻影移动开火（89）、防空炮对地（90，伤害类型按默认保持 FLAK）、磁能坦克（91）、苏军间谍（92FIX2）；
  - 基洛夫（93FIX2，有待决项）、维修无人机（94）、先进幻影（95FIX2，力场刷新 0.2s 已在包内）；
  - 袋狸（96FIX）、总统山头像（99FIX，直接建造）、盟军建造范围（98）、机场空降（100A–100C）。
- **剩余：**
  1. **精准轰炸机（AlliedSupersonicBomber_Buildable）：没有做。** 1500 / 10 秒 / 只需机场 / 照维和轰炸机等数值 devdoc 已定；**唯一缺的是军衔表**（候选：照维和轰炸机 4 级，或不加），由用户定。devdoc 另有取消规则：任一测试项不过，整项取消，不做替代。
  2. **93 基洛夫：** D1（关闭音效丢失）、D4（低血量限制被删）、AI 使用时机，三项待用户批准或修改。
- 以下不是待决项（口径校正 04:32）：
  - 无苏联同类的盟军建筑，此前已定不扩范围；
  - 头像继承 1.5 秒展开，属于和盟军相同的默认，不需另批；
  - 字符串本地化是技术收尾，后续按真实 string key 核对处理，不自造。
- 编译、实测全部未做。
- 没有发现已授权但遗漏未做的项。精准轰炸机必须等军衔决定后才能排批；如果用户同意先“不加军衔表”，可以单独一批实现。

## 对 cloud 验证文档的措辞核对
- AI、编译、按钮显示逻辑都已标为 runtime unverified，口径正确。
- L157 写“Both factions receive full paradrop functionality via inheritance”：静态继承属实，但“full functionality”是运行时结论，应改为“statically inherit the wiring; runtime unverified”。L37 / L488 的“verified”同理，只能指静态核对。
