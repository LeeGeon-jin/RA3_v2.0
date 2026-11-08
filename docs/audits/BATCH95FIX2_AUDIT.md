# BATCH95FIX2_AUDIT — ra3v2_phase1_batch95fix2（静态独审，编译/运行未证，非最终验收）
包：354183 B，sha256 c2ca369ef20e1382c7f747d6c8ffaece4ae168dfc00e0747e5e1646b14365215，与报告一致。已存为 batch95fix2.tar.gz，解包到 /workspace/b95f2/data。
145 个 XML；Mod.xml 140 条 all + 3 条 reference。

## 结论：静态 PASS（候选）
- **与 95FIX 的差异：** 只有 ExperienceLevels_AdvancedMirage.xml 的 8 个值改变，其余 144 个 XML 逐字节相同。该文件能被 ElementTree 正常解析。
- **8 个值逐项比对：** 1/1600、4800/3200、8400/9600、14400/6400，与 SDK 普通幻影（ExperienceLevels.xml L361–390）完全一致。95FIX 的 F1 已消除。
- **结构保留：** 父 include（instance）、4 个唯一 id、inheritFrom 为 ExperienceLevel_AlliedRank1–4、Prerequisite 链 1→2→3→4、Target 为 AlliedAdvancedMirageTank、Mod.xml L146 以 all 加载，都没有变化。
- **95 系列其它修复保持：** 编造的 UnitIntro 已删除（继承普通幻影的）；按钮在普通幻影之后；war factory 的 7 条原命令保留。

## 累计不回退（逐字节）
- 普通幻影和高级幻影都是 Speed 80.0，使用同一 locomotor AlliedAntiVehicleVehicleTech3Locomotor。
- 复制中心限额 1。
- 89–94 的内容，以及 93 的候选改动，均未变。

## 硬缺陷
无。

## 待编译 / 实测
1. FAKE / IDLZ 美术是否存在于 build 机。
2. 军衔升级的实际效果。
3. FAKE 模型叠加、幻影场、速度、前置条件。
4. 字符串显示（全项目翻译待做）。

## 未批准事项
93 的 D1 / D4 / AI 时机设计差异仍待用户批准。
