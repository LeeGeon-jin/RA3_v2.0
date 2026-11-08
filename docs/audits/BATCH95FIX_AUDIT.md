# BATCH95FIX_AUDIT — ra3v2_phase1_batch95fix（静态独审，编译/运行未证，非最终验收）
包：354127 B，sha256 4cc42c782a0991e2131fa0c74b2cc7df19e07264b73826db0bf3b30197f91bc2，与报告一致。已存为 batch95fix.tar.gz，解包到 /workspace/b95f/data。
145 个 XML；Mod.xml 140 条 all + 3 条 reference。
与 95 相比恰好 4 个文件变化：AlliedAdvancedMirageTank、新增 ExperienceLevels_AdvancedMirage、LogicCommandSet、Mod.xml。其余 141 个逐字节相同。4 个文件均能被 ElementTree 正常解析。

## 结论：FAIL（军衔数值是编造的，与普通幻影不一致）

### F1（FAIL）：ExperienceLevels_AdvancedMirage 的阈值与奖励不是普通幻影的值
| 级 | SDK 普通幻影 AlliedAntiVehicleVehicleTech3（ExperienceLevels.xml L361–390） | 95FIX |
|---|---|---|
| 1 | RequiredExperience 1 / ExperienceAward 1600 | 100 / 200 |
| 2 | 4800 / 3200 | 200 / 400 |
| 3 | 8400 / 9600 | 400 / 800 |
| 4 | 14400 / 6400 | 800 / 1600 |

- 包内没有覆盖普通幻影的等级表，所以 SDK 的值就是现行值。
- 95FIX 的数值在 SDK 和 devdoc 中都找不到来源，属于编造。后果：升级速度约快 50–100 倍，被击杀时给对方的经验也与普通幻影不同。
- **最小修正：** 4 级的 RequiredExperience / ExperienceAward 改为 1/1600、4800/3200、8400/9600、14400/6400，其它保持不变（不自修）。

## 其余部分：静态合法
- **等级表的结构：**
  - 文件里有对 ExperienceLevels.xml 的 instance 父 include，与包内 ExperienceLevels_SovietSpy 的写法相同，无循环。
  - 4 个 id 唯一，inheritFrom 依次为 ExperienceLevel_AlliedRank1–4（SDK L78 起），与普通幻影相同。
  - Prerequisite 链 1→2→3→4 正确，Target 都是 AlliedAdvancedMirageTank。
  - Mod.xml L146 以 type="all" 加载，目标根是 AssetDeclaration，与 SovietSpy 等级表的加载方式相同。
  - 能否真正升级仍属运行时未证。
- **单位文件：** 编造的 UnitIntro 已删除（全文件不再出现 UnitIntro），改为从普通幻影继承 Allied_MirageTank_UnitIntro。除缩进外没有其它变化。95 的 F1 已消除。
- **LogicCommandSet：** 新命令移到 Command_ConstructAlliedAntiVehicleVehicleTech3 之后（普通幻影之后），其余 7 条原命令保持不变。
- **继承：** inheritFrom 仍是 AlliedAntiVehicleVehicleTech3，父文件用 instance include。CAMP_A08 的比对结果沿用 95 审计（95 审计中其它项均合规）。

## 累计不回退
- 普通幻影文件逐字节未动：NORMAL Speed 80.0，locomotor 为 AlliedAntiVehicleVehicleTech3Locomotor。高级幻影使用同一 locomotor，也是 80.0。
- 复制中心限额 1，以及 89–94 的内容，都在逐字节相同的文件里。93 的候选改动（加速链、坠毁 2000/112、按钮 UI）均未被修改。

## 编译 / 实测未知
FAKE / IDLZ 美术是否存在于 build 机；军衔升级的运行效果；字符串显示（全项目翻译待做）。

## 未批准事项
93 的 D1 / D4 / AI 时机设计差异仍待用户批准。
