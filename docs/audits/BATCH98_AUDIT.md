# BATCH98_AUDIT — ra3v2_phase2_batch98（盟军 RA2 式建造范围，静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 00:34（UTC+10）

## 包
- 362972 B，sha256 28a6689595527c16ba009a01e5b71db72ed7fac3e93ba41843049529d6b567a4，与报告一致。
- 已存为 /workspace/ra3xfer/batch98.tar.gz，解包到 /workspace/b98/data。
- 150 个 XML；Mod.xml 145 条 all + 3 条 reference，没有重复的 source。
- 与 97 比较（diff -rq 实测）：
  - 修改 8 个文件：7 个盟军建筑 + Mod.xml；
  - 新增 2 个：AlliedAirfield、AlliedSuperWeaponAdvanced；
  - 合计 10 个，其余 **140** 个逐字节相同。
  - 【更正报告口径】报告写“138 个相同”，实际是 140（150 − 10）。不影响结论。

## 结论：静态 PASS（候选）
### 1. 七个原有盟军建筑：只追加了范围
每个文件的 diff 都只有新增的 ProjectedBuildabilityInfo，数值逐项与 SDK 苏联对应建筑相同：

| 盟军 | Radius / RadiusY | BuildPlacementTypes | SDK 苏联对应 |
|---|---|---|---|
| PowerPlant | 180 | MAIN_STRUCTURE OTHER_STRUCTURE | SovietPowerPlant 180 ✓ |
| Barracks | 195 | 同上 | 195 ✓ |
| Refinery | 180 / 195 | 同上 | 180 / 195 ✓ |
| WarFactory | 240 | 同上 | 240 ✓ |
| NavalYard | 240 / 255 | 同上 | 240 / 255 ✓ |
| TechStructure | 210 | 同上 | 210 ✓ |
| SuperWeapon | 180 / 165 | 同上 | 180 / 165 ✓ |

### 2. 两个新增文件：与 SDK 逐行 diff，只差范围一项
| 文件 | 新增 | SDK 苏联对应 |
|---|---|---|
| AlliedAirfield | 270 | SovietAirfield 270 ✓ |
| AlliedSuperWeaponAdvanced | 180 / 165 | SovietSuperWeaponAdvanced 180 / 165 ✓ |

- Draw、死亡、includes、生产、ART include 与 SDK 原样相同。保留 ART all include，与包内整文件复制的 SovietAirfield（16 条 ART）惯例一致。
- 两个文件的 DATA: 依赖都能在 SDK 或包内找到。
- Mod.xml 新增两条 all include，位置分别在 L24 和 L40。

### 3. Schema 顺序与唯一性
- 9 个对象都只有 1 个 ProjectedBuildabilityInfo。
- 都位于 VisionInfo 之后、GameObject 末尾，这里在它之后没有其它子元素。AssetTypeGameObject.xsd 的顺序是 VisionInfo → CrusherInfo → ProjectedBuildabilityInfo → DisplayUpgrade …，合法。
- 9 个文件都能被 ElementTree 正常解析。

### 4. 命令集
- 新 AlliedAirfield 的 CommandSet="AlliedAirfieldCommandSet"，对应包内 LogicCommandSet L67 的覆盖版本（未改），引用的命令在 SDK LogicCommand 中存在。
- 96 加到 SovietAirfieldCommandSet 的袋狸建造命令在未改文件中，仍然有效。

### 5. 不应扩展的部分：均未改
- 盟军建造场：包内没有覆盖，沿用 SDK 600（含船坞 filter）。
- AlliedOutPost 390：文件逐字节未改。
- 苏联、日本的所有文件，以及没有苏联对应物的新建筑（QuickProductionCenter、StatueOfLiberty、地标、头像）：都没加范围，文件未改。

### 6. 回归
以下内容所在的文件全部逐字节等于 97，均保留：
- 86 兵营：完整重建，8 秒，复制升级；
- 97 头像、核心和 ART include；
- 96 袋狸；
- 95 军衔表；
- 93 候选改动；
- 复制中心限额 1；
- 幻影坦克速度 80。

## 未证 / 边界
- 没有原生编译，也没有实测。
- 未证的运行表现：范围叠加后的实际建造区域；AI 摆放；性能（devdoc L1565）。
- 两个新文件的 ART 是否存在要等编译验证。本机 w3x 只是 75 B 占位文件，不能作证。
- 盟军建筑被覆盖后，与 SDK 静态加载流是否会重复定义，属编译时项。
- 仍待用户决定：
  - 93 的 D1、D4 和 AI 时机；
  - 精准轰炸机的军衔 widget；
  - 机场空降被击落后的乘员处理（随机方案未证，见 NEXT_PHASE2_FINAL 2.5）；
  - 头像墙钟时间 33 秒还是 30 秒；
  - 无苏联对应物的盟军新建筑是否给范围。
