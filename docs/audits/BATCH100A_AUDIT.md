# BATCH100A_AUDIT — 科技机场空降：飞机阶段（静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 04:15（UTC+10）。基线：99FIX。规格：NEXT_PHASE2_FINAL.md v4 §2.2 A1。

## 包
- 363601 B，sha256 e992a3b8f12f9788e890b4ab9a13fa2109602b42cdd4ca67a25f493d5f97ca0c，与报告一致。
- 已存为 /workspace/ra3xfer/batch100a.tar.gz，解包到 /workspace/b100a/data。
- 150 个 XML。
- 与 99FIX 比较（diff -rq 实测）：
  - 新增 Neutral/Structures/TechAirportParadrop.xml；
  - Mod.xml 只在 L123 加了一条 all include；
  - 其余 148 个逐字节相同。
- Mod.xml：<Include> 元素 148 → 149（其中 all 144 → 145、reference 3，另有 1 个是 Includes 容器标签被计入）。cloud 报的“148→149”是按 <Include 字样计数的，数字吻合，但不等于“149 条 all”。
- 新文件能被 ElementTree 正常解析。

## 结论：静态 PASS（候选），附 1 项非阻断缺陷 D1

### 逐项核对（三架飞机结构相同，只有 id、Side、InitialPayload 不同）
- **继承：** inheritFrom="SovietSupportBomber_Buildable"（包内 96FIX，Badger Draw）。父文件没有改动，原袋狸、世纪轰炸机文件也没有改动。
- **KindOf：** 增量写法 -AIRCRAFT_TRANSPORT_ONLY_GARRISONABLE_WHILE_PARKED -LIMITED_PRODUCTION_AIRCRAFT +SUMMONED +IGNORES_SELECT_ALL +NO_COLLIDE -SELECTABLE。被去掉的两项父类确实有（父类 KindOf L22）；SELECTABLE 也被去掉。与规格一致。
- **其它属性：** IsTrainable="false"、EditorSorting="UNIT"。Side 分别为 Allies / Soviet / Japan。
- **TransportContain：**
  - id 与父类相同（ModuleTag_Contain），用 xai:joinAction="Replace" 整段替换；
  - 属性和子元素与父类 L175–200 逐项相同，只把 KillPassengersOnDeath 改为 "false"，并显式写 EjectPassengersOnDeath="true"（OpenContain.xsd L46–47）；
  - 子元素顺序 PassengerFilter → DieMuxData → PassengerData（OpenContain 基础序列）→ InitialPayload（TransportContain 扩展序列，maxOccurs 4），合法；
  - 载荷：盟 3 AlliedAntiInfantryInfantry + 2 AlliedAntiVehicleInfantry，苏 3 Soviet… + 2 Soviet…，帝 3 Japan… + 2 Japan…。6 个 ID 都存在。
- **死亡处理：** 没有 OCL、FireWeaponWhenDead 或任何生成对象的模块。死亡时只会弹出此刻还在机上的乘员，不新造兵，不会复制已投下的步兵。【静态推理】
- **SpecialPower 和 EjectPassengersSpecialAbilityUpdate：**
  - 都用 Replace，与父类 id 相同（L202 / L206）；
  - 字段逐字照 CAMP_Infantry_2；
  - StartAbilityRange 在 SpecialAbilityUpdate.xsd L63 合法；
  - SpecialPower_EjectPassengers 在包内覆盖的 SpecialPowerTemplates.xml 中存在。
- **RunOffMapBehavior：** 用 Replace，与 BaseVehicle L125–129 的同 id 模块对应，没有重复 id。FlyingOffMap 和 RequiresSpecificTrigger 照 CAMP。
- **WeaponSetUpdate：**
  - 用 Remove，与父类 L129 的 id 相同；SDK 先例 CAMP_Infantry_2 L101–103。
  - 副作用：飞机没有武器。继承来的 StatusBitsUpgrade（WEAPON_UPGRADED_01）和 AlliedAirPower AttributeModifierUpgrade 仍在，但对弹出和飞离没有影响（按规格不改）。JetAIUpdate 的 OutOfAmmoDamagePerSecond 在没有武器时如何表现，属运行时项。
- **投放 / 飞离链的公共依赖静态完整：**
  - SpecialPower_EjectPassengers 存在；
  - RunOffMap（FlyingOffMap）存在；
  - 6 个步兵 ID 存在；
  - GlobalDefines 存在。
  
  OCL、能力、机场接线按设计留到 100B / 100C，本批不判为缺项。

### D1（非阻断缺陷，建议在 100B 顺带改）：父文件用 all 方式引用
- 新文件 L5 写的是 `<Include type="all" source="DATA:Soviet/Units/SovietSupportBomber_Buildable.xml"/>`，规格 v4 写的是 **instance**。
- 包内唯一一处“对象文件 all 引用另一个对象文件”就是这里。SDK 中的继承父文件一律用 instance（如 CAMP_Infantry_2 引用 AlliedBomberAircraft）。
- 不判硬 FAIL 的理由：
  - SDK 有同一文件被多个文件 all 引用的先例（CCBuildingDebris_02 被 9 处 all 引用）；
  - Mod.xml L148 本来就 all 加载了这个父文件，因此不会悬空。
- 风险：重复流入构建流，是否会造成重复定义或包体膨胀，只能编译验证。
- **修法：** 只把这一行的 type="all" 改为 type="instance"，其它不动。

## 回归
以下内容所在的文件全部逐字节等于 99FIX，均保留：
- 头像直接建造（CONSTRUCTION_YARD_CONSTRUCT）、97 ART include；
- 98 建造范围；
- 96 袋狸、95 军衔表、93 候选改动、86 兵营；
- 复制中心限额 1、幻影坦克速度 80。

## 运行未证
- 编译，包括 D1 的重复 all 引用。
- 召唤后能否被选中。
- 投放流程（目前还没接线）。
- 击落后剩余乘员是否被弹出、空中弹出后是否生还、有没有伞。
- 没有武器时 JetAI 的表现。
- 袋狸美术是否存在（本机 w3x 是 75 B 占位文件）。

## 100B 最小接续建议（只做能力 / OCL；机场 UI 和模块留给 100C）
1. 改 D1：TechAirportParadrop.xml L5 改为 type="instance"。
2. 在同一个新文件里加 3 个 ObjectCreationList：OCL_TechAirportParadrop_Allied / _Soviet / _Japan，按 v4 §2.2 A2。
   - 每个 1 个 CreateObject：Options "IGNORE_ALL_OBJECTS DONT_SET_PRODUCER ISSUE_MOVE_AFTER_CREATION FIRE_SPECIAL_POWER"，Disposition LIKE_EXISTING，FireSpecialPowerTemplate SpecialPower_EjectPassengers，Offset 0/0/190。
   - **不加** CREATE_AT_TARGET。
3. 在包内 GlobalData/SpecialPowerTemplates.xml 加 3 个 SpecialPower_TechAirportParadrop_*，按 v4 §2.6 逐字：
   - 540s、LOCATION、半径 100、Eva；
   - Flags 含 SHARED_SYNC；
   - ForbiddenObjectFilter；
   - RequiredPlayerTech 为对应阵营的根科技；
   - 没有 AI 字段。
4. **100B 不要动：**
   - 机场文件、OCLSpecialPower 模块、LogicCommand、LogicCommandSet、按钮；
   - 中立机场整文件复制；
   - Mod.xml。新文件已经被 all 加载；SpecialPowerTemplates 也已在 Mod 中。
5. 100C 再做：中立机场整文件复制，可建造盟军机场加 CommandSet 和 3 个 OCLSpecialPower 模块，3 条命令、命令集、3 个按钮，Mod 加中立机场的 all include（v4 §2.3–2.8）。
