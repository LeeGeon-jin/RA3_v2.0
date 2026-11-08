# BATCH93FIX_AUDIT — RA3_V2.0_Batch93FIX_KirovBoost（静态独审，运行时未证）
包：352310 B，sha256 ac3db65cae77211c1e33d20bb166fe9e99097d70c056388e905e8d56b651b3b6，与指令一致。已存为 batch93fix.tar.gz，解包到 /workspace/b93f/data。
143 个 XML；Mod.xml 138 条 all + 3 条 reference。与 93 相比只有 4 个文件变化，其余 139 个逐字节相同。

## 结论：技术静态 FAIL（1 项缺陷）；另有 D1、D4 两项设计差异未获批准（与 FAIL 分开列）

### F1（FAIL）：ButtonState 覆盖改了原图标和文本
包内 UI/ButtonStateDataCommon.xml 新增的 `ButtonStateToggleAfterburners` 与原版不一致：

| 字段 | SDK 原值（ButtonStateDataCommon L1076–1080） | 93FIX |
|---|---|---|
| Image | SUA_Kirov_Afterburners | **SUA_Afterburners**（全 SDK 和 static.manifest 都没有这张图，会缺图） |
| Title | NAME:ToggleAfterburners | **NAME:AbilityToggleAfterburners**（全 SDK XML 中无此键，属新键；字符串表无法静态核对） |
| Description | DESC:ToggleAfterburners | **DESC:AbilityToggleAfterburners**（同上） |

- 快捷键来自 NAME 字符串，换了键就可能丢失快捷键。
- 所以 cloud 称“保原 icon/文本/快捷键”与包内实际不符。
- 另外，这个 id 并不是“新 ID”，而是与 SDK 同 id 的重定义（同 id 覆盖本身有包内先例，可以接受）。
- **最小修正：** 把这三个值恢复为 SDK 原值，id 保持不变（不自修）。

## 其余三项改动：静态合法
1. **SovietBomberAircraft：** 删除 SwitchLocomotorUpdate 共 5 行。全包已无 ModuleTag_Afterburners 的引用，不留孤儿。93 审计中的 D3 就此消除。
2. **UnitAbilityButtonTemplates：** 同 id 重定义 ButtonToggleAfterburners → `<SpecialPower StateData=…/>`。
   - Schema 依据：AssetTypeUnitAbilityButtonTemplate.xsd L28 和 SpecialPowerUnitAbilityButtonTemplateData.xsd，StateData 类型为 ButtonSingleStateDataRef。
   - 写法与 SDK 冲刺先例 ButtonJapanEngineerSprint（L975）相同。
   - 引用链：CommandSet（SDK LCS L606）→ Command_ToggleAfterburners → 按钮 → ButtonState，完整；包内这两个 UI 文件都已在 Mod.xml L10–11 中以 all 方式包含。
   - 冷却显示：已有设置条件，即 SpecialPower 类按钮配合模板 ReloadTime 30s，与工程师冲刺同构。是否真的显示冷却，运行时未证。
   - 非目标 UI 条目与 93 逐字节相同。
3. **LogicCommand：** 加入 UseInMicroManagerState="RETREAT COMBAT CLEANUP" 和 UseNearTacticalTarget="true"。
   - 属性在 AssetTypeAISpecialPower.xsd L260–261 中合法，与 SDK Command_JapanEngineerSprint（L1624–1628）完全相同。
   - **但与原版 AI 时机不等价：**
     - 原 toggle 的 AI 提示是：OnlyUseWhenHaveTarget、离目标超过 1000 不用、近于 50 不用、自身血量低于 2000 不用。
     - 新版额外允许在撤退（RETREAT）时使用，并且不再有距离和血量限制。
   - 这是技术新增，等于扩大了 AI 使用时机，需要用户确认，不能视为与原版等价。

## 93 沿用（本包未触及，复核未变）
- 10s / 30s / 不掉血 / 坠毁 2000 / 112 / 正常 30 加速 55 / 炸弹 400 都保留。
- 幻影坦克 80 与复制中心限额 1 均未变。

## 未批准的设计差异（不是技术缺陷，也不能自动接受）
- **D1：** 加速结束时无声。原版熄火音效 SOV_Kirov_CastroBurnersOff 已丢失。
- **D4：** 原版对低血量的限制已不再生效：
  - 原 SwitchLocomotorUpdate 的 MinimumHealth="10%"，即基洛夫 MaxHealth 6000 的 600 HP 以下不能加速；
  - 原 AI 提示 NeverUseWhenHealthIsBelow="2000"（约 33%）。
  - 现在任何血量都能用。
- 以上按实际字段记录，不采用 cloud 的因果解说。

## 运行时必测
按钮图标和文本、冷却显示、快捷键，10 秒加速后回到 30，AI 使用时机。
