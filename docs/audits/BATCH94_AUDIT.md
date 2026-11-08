# BATCH94_AUDIT — RA3_V2.0_Batch94_SovietRepairDrones（静态独审，运行时未证，非最终验收）
包：352649 B，sha256 531e767118a5cd8ee63718717fee16f8a44a783b84b149da75ececc8cfedd610，与指令一致。已存为 batch94.tar.gz，解包到 /workspace/b94/data。未使用 host 片段。
143 个 XML；Mod.xml 138 条 all + 3 条 reference。与 93FIX2 相比只有 SovietWarFactory、SovietNavalYard 两个文件变化，其余 141 个逐字节相同。

## 结论：静态 PASS（候选）
1. **逐字复制 SDK：** 两个文件各新增 2 个模块，内容与 SDK SovietCrane.xml L464–480 逐属性一致，只有缩进不同：
   - `AssignSlavesTargetObjectSpecialPower id=ModuleTag_SpecialPowerRepairVehicle SpecialPowerTemplate=SpecialPower_TargetedRepairVehicle`；
   - `SpawnBehavior id=ModuleTag_SpawnRepairDrones`：SpawnNumberData 3、InitialBurst 3、SpawnReplaceDelayData 10s、SpawnedRequireSpawner、KillSpawnsOnCaptured、SpawnInsideBuilding、KillSpawnsOnDisabled、SpawnOnUnpack 都为 true；`Die DeathTypes=ALL`；SpawnTemplate 为 SovietRepairDrone。
2. **ID 与插入位置：** 两个文件内 ModuleTag 都没有重复 id。新模块插在 `<Behaviors>` 的开头（WarFactory L520、NavalYard L484）；Behaviors 是 choice 结构，顺序无约束，合 schema。
3. **其余内容不丢：** 与 93FIX2 的 diff 只有这 17 行新增，Includes、Draw、生产、死亡、xi:include 和 CommandSet 全部原样保留。两个文件均能被 ElementTree 正常解析。
4. **无人机加载与能力链：**
   - SovietRepairDrone 由 SDK Soviet/Soviet.xml L14 全局加载，并出现在 static.manifest 中。SovietCrane 本身也不 include 它，同样按名称引用，属同一机制。
   - SpecialPower_TargetedRepairVehicle 定义在 SDK SpecialPowerTemplates L69（筛选条件：VEHICLE HUGE_VEHICLE，排除 AIRCRAFT，MaxCastRange 200）。包内覆盖的 SpecialPowerTemplates 含这个 id。
   - 与 SDK 起重机一致：CommandSet 中没有对应按钮，无人机靠自身 AI 修理。
5. **苏联舰船 KindOf（静态满足）：**
   - 无人机的修理筛选为 Rule=ANY，Include="VEHICLE AIRCRAFT HUGE_VEHICLE"，Relationship=ALLIES。
   - 包内现行的苏联舰船 KindOf 都含 VEHICLE：
     - SovietAntiAirShip（Bullfrog）：VEHICLE AMPHIBIOUS
     - SovietAntiNavyShipTech1（Stingray）：VEHICLE AMPHIBIOUS
     - SovietAntiNavyShipTech2（Akula）：VEHICLE SUBMARINE
     - SovietAntiStructureShip（Dreadnought）：VEHICLE SHIP
     - SovietMCV 与 SovietMiner：VEHICLE AMPHIBIOUS
   - 包内唯一新增的苏联单位 SovietInfiltrationInfantry 是 INFANTRY，本来就不在修理范围内。
   - 静态筛选满足。但实际是否修理，仍属运行时：水上路径、潜艇下潜时能否修、船只修理、展开后生成都未测。
6. **不回退：** 复制中心限额 1、普通幻影 80、93 坠毁 2000/112（Weapon 中 3 处 Damage="2000.0"，与 93 一致）、93 加速链，以及 91 与 92 的内容，都在逐字节相同的文件里。

## 未批准事项（不受本批 PASS 影响）
93 的 D1（结束无声）、D4（低血限制不再生效）和 AI 时机差异仍待用户批准；93 依然未最终验收。

## 运行时必测
1. 战车工厂和船厂展开后各出 3 架无人机，10 秒补充。
2. 无人机修理载具和舰船（含潜艇）。
3. 建筑被占领、被禁用或被摧毁时无人机消失。
