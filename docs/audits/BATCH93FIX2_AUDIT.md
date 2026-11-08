# BATCH93FIX2_AUDIT — RA3_V2.0_Batch93FIX2_KirovBoost（静态独审，运行时未证，非最终验收）
包：352315 B，sha256 ec52db0a44a47d5ad52853b33fedacc2b975c5239bf010df287caa1134d5b699，与指令一致。已存为 batch93fix2.tar.gz，解包到 /workspace/b93f2/data。
143 个 XML；Mod.xml 138 条 all + 3 条 reference。

## A. 技术静态：可接受候选
- **对 93FIX：** 只有 LogicCommand、UI/ButtonStateDataCommon 两个文件变化，其余 141 个逐字节相同。
- **对 93：** 有 3 个文件变化（SovietBomberAircraft 去掉 SwitchLocomotorUpdate，加上两个 UI 文件），其余 140 个相同。
  - 指令说“对 93 四文件差、其余 139 同”，实测是 3 个。原因是 LogicCommand 已经回到与 93 逐字节相同，并非缺漏。
- **ButtonStateToggleAfterburners（同 SDK id 覆盖，文件内唯一）：** Image=SUA_Kirov_Afterburners，Title=NAME:ToggleAfterburners，Description=DESC:ToggleAfterburners，三个值与 SDK ButtonStateDataCommon L1076–1080 完全一致。93FIX 的缺陷 F1 已消除。
- **引用链：** SDK SovietBomberAircraftCommandSet（LCS L606）→ Command_ToggleAfterburners（包内覆盖）→ ButtonToggleAfterburners（包内同 id 覆盖，`<SpecialPower StateData>`，合 schema）→ ButtonStateToggleAfterburners。链条完整。两个 UI 文件都在 Mod.xml L10–11 中以 all 方式包含。两个改动文件均能被 ElementTree 正常解析。
- **LogicCommand：** 只剩 Heuristic=SPEED_BOOST 和 Manager=MICRO_MANAGER，与 93 相同，SPEED_BOOST 在 AssetTypeAISpecialPower.xsd L21 中合法。
- **不回退：** 10s 持续 / 30s 冷却 / 无掉血 / 30→55 / 坠毁 2000/112 / TaperOff 200 / 冲击波与 50% 友伤 / 炸弹 400 / 幻影坦克 80 / 复制中心限额 1 / 91 与 92 的内容，全部未变（未触及的文件逐字节相同）。

## B. 用户未批准的差异（不是技术缺陷，也不算设计通过）
- **D1：** 加速结束时无声，原 SOV_Kirov_CastroBurnersOff 已丢失。
- **D4：** 低血量限制已不再生效：
  - 原 SwitchLocomotorUpdate 的 MinimumHealth 10%，即 6000 HP 的 600 以下不能加速；
  - 原 AI 提示 NeverUseWhenHealthIsBelow 2000。
- **AI 时机：**
  - 原 toggle 的提示是：OnlyUseWhenHaveTarget、离目标超过 1000 不用、近于 50 不用、血量低于 2000 不用。这些都写在 ToggleState 的 SkirmishAiInfo 里，随 toggle 模块一起删掉了。
  - 现在只有 SPEED_BOOST / MICRO_MANAGER，没有保留目标、距离和血量限制。
  - cloud 称 schema 中没有对应字段。该判断没有被本审计证伪，需要用户决策。
  - 删掉 RETREAT 状态，**不能**证明 AI 不会在撤退时使用；SPEED_BOOST 的实际使用时机属运行时未证。
- 以上三项都要等用户在 widget 中作答；未作答前，93 不算最终验收。

## C. 运行时必测
1. 按钮显示原图标、原文本和快捷键。
2. 冷却显示。
3. 10 秒加速后回到 30，冷却 30 秒。
4. 加速期间全图可见。
5. 开启音效正常播放。
6. AI 使用时机。
7. 坠毁伤害 2000、半径 112。
