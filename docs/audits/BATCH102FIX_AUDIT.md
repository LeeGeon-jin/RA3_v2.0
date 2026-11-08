# BATCH102FIX_AUDIT — 可建造精准轰炸机修复（静态独审；编译和实测都没做，任何游戏功能都没有验收）
审计时间：2026-11-09 09:17（UTC+10）。基线：102。对照：SDK 原文。
使用真实包和验证 md，没有使用节选附件。

## 包
- 365841 B，sha256 053c6b498c5e28b82e31eaa312229221cc48a1a16d8ba15cc61f4f0df077bdca，与报告一致。
- 153 个 XML。
- 与 102 比较（diff -rq）：只有 AlliedSupersonicBomber_Buildable.xml 一个文件变化，其余 152 个逐字节相同。
- 新文件能被 ElementTree 正常解析。

## 结论：静态 PASS（候选），F1–F6 全部修复
- **F1 音效：** AudioArrayVoice 为 SDK 维和轰炸机的 8 条 ALL_Vindicator_*（6 条 AudioEntry 加 2 条 NamedEntry），与 SDK 逐字相同；AudioArraySound 恢复原版的 ALL_SurgicalStrike_FlyByLoop soundAmbient。全文件不再有 ALL_PrecisionBomber_*，所有音效 ID 都能在 SDK Voice.xml 和 manifest 中查到。
- **F2 死法：**
  - 两个 CreateObjectDie：AUBomberAircraft_Dying_OCL（ExemptStatus PARKED_AT_AIRFIELD）和 AUBomberAircraft_Die_OCL（RequiredStatus PARKED_AT_AIRFIELD），两个 OCL 都在 SDK ObjectCreationLists 中；
  - DestroyDie ModuleTag_Die，DeathTypes ALL；
  - FXListBehavior 的 FX 为 FX_ALL_VindicatorDie（SDK 中存在）；
  - SlowDeathBehavior 已删除。与世纪轰炸机、袋狸的写法同构。
- **F3 Draw：** Draws 段与 SDK AlliedSupersonicBomber 做 diff -w，**完全为空**（去掉 CR 后比较）。WeaponLaunchBone FXCON02、FireHawkConTrail、DAMAGED 和 REALLYDAMAGED 两个状态都已恢复，虚构的 AnimationState 已删除。
- **F4：** DynamicsUpdate ModuleTag_DefaultDynamicsUpdate xai:joinAction="Remove" 已加上。
- **F5：** ProductionUpdate 已删除。
- **F6：** Geometry 改为 10 / 5 / 5，与原机相同，只多了维和轰炸机的 ContactPointGeneration="VEHICLE"；SubGroupPriority 605。

## 追加核查
- **WEAPON_UPGRADED_01：** StatusBitsUpgrade 只设置这个状态。武器槽里只有 AlliedPrecisionBomb_Buildable 一把武器，而且没有 ObjectStatus 或 ForbiddenObjectStatus 过滤，所以买空中力量协议后不会切换到别的武器。AlliedAirPowerUpgrade.xml 只挂载 AttributeMod_AlliedAirPowerAttribute。没有误变换。
- **兼容边界（静态无法证明，都是运行时项）：**
  - 原机模型 AUSupersonicBomber 只有 DEFAULT / DAMAGED / REALLYDAMAGED 三个状态，没有 TAXIING、PARKED、USER_1（返航）的专用外观，停机和滑行时显示默认模型；
  - 残骸 OCL 用的是世纪轰炸机的残骸（袋狸也一样），外观可能不匹配；
  - JetAI 对一个没有起落动画的模型的起飞和降落表现未知。
- **KindOf：** 与维和轰炸机相同，另保留原机的 NO_COLLIDE；没有 SUMMONED、IGNORES_SELECT_ALL。
- **原召唤机：** 包内没有 AlliedSupersonicBomber.xml 的覆盖，SDK 原版不变；它的经验表也不变。
- **102 已通过的部分：** 武器、经验、命令、两个机场命令集、Mod，以及 101 / 100C 和全部累计改动，所在文件都逐字节等于 102。

## 运行时必测
编译；停机、起飞、攻击、回机场补弹（任一项不过，整项取消）；炸弹从 FXCON02 投出；空中和停机两种死法；空中力量协议；AI 是否会造；模型在停机和滑行状态下的表现。

## 对 cloud 验证 md 的纠正
- L474 写“公开 GitHub 上传：用户操作”，不对。用户 08:56 只定了顺序，上传由主协调负责执行，不是用户自己操作。
