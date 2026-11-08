# BATCH96FIX_AUDIT — ra3v2_phase1_batch96fix（静态独审，编译/运行未证，非最终验收）
包：355759 B，sha256 2751c06a93ca08211bca88e0e1b29b60b1cf5ac1129120de7791395afeff0a9b，与报告一致。已存为 batch96fix.tar.gz，解包到 /workspace/b96f/data。
147 个 XML；Mod.xml 142 条 all + 3 条 reference。

## 结论：静态 PASS（候选）
- **改动范围：** 与 96 相比只有 GlobalData/LogicCommand.xml 的 L255 一行变化，其余 146 个文件逐字节相同。
- **96 的 F1 已消除：** 该行由 `<UnitBuild>` 改为 `<Object>SovietSupportBomber_Buildable</Object>`。
  - 合 schema：AssetTypeLogicCommand.xsd L54，Object 的类型为 GameObjectRef。
  - 与 SDK 和包内其余 39 条建造命令写法相同；Type 为 UNIT_BUILD，指向新 ID。
  - 全文件已无 `<UnitBuild>`，ElementTree 能正常解析。
- **96 其余审计结论全部沿用**（96 审计中其它项均合规）。

## 累计不回退
普通幻影与高级幻影 80、复制中心限额 1、93 候选改动，以及 89–96 的内容，均在逐字节相同的文件里。

## 未编译 / 未实测
沿用 96 审计列出的全部运行时未知项：停机、登机与弹出、投弹骨骼、动画、军衔、图标与字符串、AI 不造。

## 待批准
- 93 的 D1 / D4 / AI 时机设计差异仍待用户批准。
- 精准轰炸机军衔未答，暂不实施。
