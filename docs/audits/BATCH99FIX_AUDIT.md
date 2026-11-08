# BATCH99FIX_AUDIT — 帝国头像直接建造命令修正（静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 04:07（UTC+10）

## 包
- 362713 B，sha256 b1fbd9f148028715935e22a2b119f6860fb42e0763099fc37984b4c3294c1b55，与报告一致。
- 已存为 /workspace/ra3xfer/batch99fix.tar.gz，解包到 /workspace/b99f/data。
- 149 个 XML。
- 与 99 比较（diff -rq 实测）：只改了 GlobalData/LogicCommand.xml 一行（L259：Type UNIT_BUILD → CONSTRUCTION_YARD_CONSTRUCT），其余 148 个逐字节相同。
- LogicCommand.xml 能被 ElementTree 正常解析。

## 结论：静态 PASS（候选）
- **99 的 F1 已修正。** 新的 Type 是 schema 枚举中的合法值。现在 Command_ConstructJapanRushmoreLaserHead 与以下命令写法同构：
  - 盟军头像（LC L86–88）、苏联头像（L80–82）；
  - 帝国在建造场直接放置的建筑：装饰 L93–99、快速生产中心 L229–231、可建造机场 L196–198。
- 帝国建造场有 SDK 原样的 MAIN / OTHER_STRUCTURE ProductionUpdate。
- 全包 grep 旧核心 ID：0 残留。
- 以下内容所在的文件与 99 逐字节相同，均保留：
  - 头像参数：2000 / 30 秒 / 前提 JapanTechStructure、HP2000、射程1150、视野1250、耗电-75、转速360、无 MaxDeflection、无限额、AI 未加；
  - Ready 文件 L7–8 的两条 ART include；
  - 盟、苏头像段落；
  - 98 建造范围；
  - 96 袋狸、95 军衔表、93 候选改动、86 兵营；
  - 复制中心限额 1、幻影坦克速度 80。

## 1.5 秒展开
- 帝国头像继承 BaseMountRushmoreHead L121–123 的 StructureUnpackUpdate 1.5s，与盟军头像相同。
- 静态上**不是 0 秒**。这是与盟军版相同的继承机制，不算新偏差。实际表现待测。

## 运行未证
- 编译。
- 放置流程，悬空表现。
- 1.5 秒展开期间能否开火、能否被攻击。
- 低电时停火。
- 按钮和新字符串键的显示。
- 真实美术是否存在（本机 w3x 是 75 B 占位文件）。
