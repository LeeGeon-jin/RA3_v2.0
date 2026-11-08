# 精准轰炸机实施：最小最新基线（2026-11-09 08:59 UTC+10，基线 Batch101；只是源码候选，不是承诺）
- refs 包：/workspace/ra3xfer/precision_b101_refs.tar.gz（110641 B，sha256 85c77b66066d88770b8675caf0ca13778acaf0a293b1b9873531cee6732107b0）。共 16 个文件，附 MANIFEST.tsv；解包后已按哈希全部校验通过。
  - sdk/ 下：AlliedSupersonicBomber、AlliedAntiGroundAircraft、AlliedBomberAircraft、ExperienceLevels、LogicCommandSet、LogicCommand、Weapon、Locomotor、ButtonStateDataCommon、SkirmishAI/States/AlliedBaseStates；
  - b101/ 下：Mod、LogicCommand、LogicCommandSet、Weapon、ExperienceLevels_Badger、SovietSupportBomber_Buildable。
- NEXT_BOMBERS.md 中以 95FIX2 为准的行号已过期，**以本文件为准**。

## 已定要求（按用户条件，不扩范围）
1. 新对象 **AlliedSupersonicBomber_Buildable**：1500 / 10 秒，只需机场。
   - 模型、外观、武器保持精准轰炸机原样：ART:AUSupersonicBomber.w3x；武器 AlliedPrecisionBomb，ClipSize 1、AutoReloadsClip NONE，适合回机场补弹。
   - 机场机的模块照 AlliedAntiGroundAircraft 迁移：JetAIUpdate、两套 LocomotorSet（含 BasicHelicopterTaxiLocomotor）、ReturnToProducerSpecialPower。
   - 结构参照包内 b101 的 SovietSupportBomber_Buildable（272 行，以 BaseVehicle 为基类的完整对象）。
   - 去掉 SUMMONED、EmptyCommandSet、ParabolicCurveUpdate。
   - 按钮和头像用 Button_PlayerPower_PrecisionStrike。
2. **原召唤机 AlliedSupersonicBomber 不改**，它的经验表 AlliedSupersonicBomberExperienceLevel_1 也不改。
3. **军衔：原版一级。** 新建 AlliedSupersonicBomber_BuildableExperienceLevel_1：
   - inheritFrom ExperienceLevel_AlliedRank1，RequiredExperience 1，ExperienceAward 10000，Target 为新 ID（值照 SDK ExperienceLevels L221–226）；
   - 写法照 ExperienceLevels_Badger：父文件用 instance include，Mod 用 all 加载（参照 b101 Mod L149 / L152）。
4. **命令：**
   - 新增 Command_ConstructAlliedSupersonicBomber_Buildable，类型 UNIT_BUILD。
   - 包内现在**没有** AlliedAirfieldCommandSet。照 SDK 原版整套 5 条命令（AntiGround、Fighter、Support、Bomber、RecallAll）复制后，加入这一条新命令。
   - **SovietAirfieldCommandSet（b101 L231–237，含袋狸）保持原样**。
5. **AI：** 不加入 AlliedBaseStates 的建造表（SDK 的空军 BuildEntry 参照 L493 附近）。AI 实际会不会造，要实测才知道。
6. **取消规则：** 停机、起飞、攻击、回机场补弹，任一项实测不过就**整项取消，不做替代**。
7. **必须保留：** Batch101 的全部内容，包括基洛夫还原（DamagePerSecond 100.0）、坠毁 2000 / 112、机场链、95–100 的既定改动。
8. **流程（用户 08:56 已定）：** 第二批源码复核全部完成后，先把代码和最新 md 上传到公开 GitHub 仓库 RA3_v2.0，上传核验通过后才编译测试。**在那之前不编译。**
