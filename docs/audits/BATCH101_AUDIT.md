# BATCH101_AUDIT — 基洛夫还原原版双模式并把掉血减半（静态独审；编译和实测都没做，不是最终验收）
审计时间：2026-11-09 08:59（UTC+10）。基线：100C 和 b92f2，对照 SDK 原文。
本次审计使用真实包和验证 md，没有使用 501 B 的节选附件。

## 包
- 364412 B，sha256 5a1a47996881719c08e7ad710a6bda1fa5604e34ef80e1616a39fc352a193940，与报告一致。
- 151 个 XML。
- 与 100C 比较（diff -rq）：只有 5 个文件变化，即 SovietBomberAircraft、SpecialPowerTemplates、LogicCommand、ButtonStateDataCommon、UnitAbilityButtonTemplates；其余 146 个逐字节相同。
- Mod.xml、机场链的所有文件、Weapon.xml 都逐字节相同。
- 5 个改动文件都能被 ElementTree 正常解析。

## 结论：静态 PASS（候选），无缺陷

### SovietBomberAircraft
- 与 b92f2 做 diff -w -B（忽略缩进）：**唯一差异是 DamagePerSecond "200.0" → "100.0"**。缩进比 b92f2 和 SDK 少一级 tab，不影响内容。
- 四个模块逐元素恢复：
  - SpecialPower；
  - ToggleStatusSpecialAbilityUpdate：RECONSTITUTE_STORED_COMMAND；关闭音效 CastroBurnersOff 和开启音效 CastroBurnersOn；GENERIC_TOGGLE_STATE 与 SHROUD_REVEAL_TO_ALL；LOCOMOTOR_NORMAL_UPGRADED；SkirmishAiInfo 为 TOGGLE_DEFAULT / TOGGLE_ALWAYS、OnlyUseWhenHaveTarget、距离 1000 / 50、NeverUseWhenHealthIsBelow 2000；两个 Module 引用；
  - SwitchLocomotorUpdate：NORMAL_UPGRADED，1.0 秒，MinimumHealth 10%；
  - LoseHealthUpdate：HealthTrigger 0%，DamagePerSecond 100.0，要求状态 GENERIC_TOGGLE_STATE。
- 运动器速度 10 / 30 / 55（L46 / 51 / 55）、2000 / 20 秒均保留。
- 93 的 MovementSpecialPower ModuleTag_AfterburnersBoost 已删除，全包已没有残留。

### 定时框架撤除
相对 100C 只有删除，没有任何新增行：
- SpecialPowerTemplates：删除 L754–755 的 ReloadTime 30s 和 InitiateSound，模板回到 SDK 原样。
- LogicCommand：删除 L35–43 的 Command_ToggleAfterburners。
- ButtonStateDataCommon：删除 L10–17。
- UnitAbilityButtonTemplates：删除 L31–39。

这 4 个文件与 b92f2 的全部差异，都只是 95–100C 的既定新增（先进幻影、袋狸、头像命令，机场的 3 条命令、3 个模板、3 个按钮），没有遗漏也没有多余。
原定义由 static 引用接管，回到 b92f2 的状态：
- Command_ToggleAfterburners（SDK LogicCommand L1481，Heuristic TOGGLE）；
- ButtonToggleAfterburners（SDK Mouse L733，ToggleSpecialPower，含 Toggle 和 Off 两个状态）；
- ButtonStateToggleAfterburners / Off（SDK L1076 / L1084）。

包内没有重复或悬空的 Afterburners ID。AttributeModifier_KirovAfterburnersDummy 本来就是 SDK 原有的。

### 保留项
- Weapon 坠毁 Damage 2000.0 / Radius 112.0（L4515–4516）与 100C 逐字节相同。
- 100C 机场链及 95–100C 的全部既定改动保持不变。

## 运行时必测
- 编译。
- 开关加速、两种音效、速度 30 → 55。
- 加速时实际掉血速率（DamagePerSecond 100.0 实际如何扣血未证）。
- 血量低于 10% 时自动退出加速。
- AI 的 2000 血门控。
- 坠毁伤害和半径。
- 100C 机场空降全部运行时项。

## cloud 验证 md
- 已改用 DamagePerSecond 字段名的写法，没有发现越界措辞。
