# 第二批剩余范围核对（2026-11-08 22:15 UTC+10）
依据：devdoc（最新修订说明优先）+ 88FIX 实包（139 XML）。只读，不改源码、不访问 PC、不编译。单位按真实 ID 核对，不按俗名。

## 俗名纠正
- **将军刽子手 = JapanMechaKing**（devdoc L209/L1059）。之前的进度文档误写成“鬼王”。
- **红鬼王 = JapanEmperorMecha**（L1050/L1053，天皇的机甲）。之前误写成“帝国巨型机甲”。
- **袋狸轰炸机 = SovietSupportBomber**（L890）。
- **精准轰炸机 = AlliedSupersonicBomber**（L643/L644）。
- **磁能坦克 = SovietAntiVehicleVehicleTech2**（L885）。
- **先进幻影坦克**：来源是 CAMP_A08_SpecialMirageTank，新对象 id 为 AlliedAdvancedMirageTank（L14/L589）。

## A. 已在 88FIX 实包内（不要重做；只需实测，进度文档以后改名纠正）
| 项 | devdoc | 实包证据 |
|---|---|---|
| 将军刽子手 | L1056/L1059：核心 4000 / 5 秒，在战车工厂生产，展开 30 秒，速度 ×1.5，不限数量 | JapanMechaKingCore 4000 / BuildTime 5 / PackTime 30.0s / ReplacementTemplate JapanMechaKing；速度 45 → 67.5；命令 Command_ConstructJapanMechaKingCore 在 LogicCommandSet L88 |
| 红鬼王 | L1050/L1053：2200，时间 8 秒不改，前提纳米电脑主机 | JapanEmperorMecha 2200 / 8 / RequiredObject JapanTechStructure；命令在 LogicCommandSet L86 |
| 电厂升级（盟军、帝国） | L478/L482/L942/L946：300、10 秒、1.5 倍、仅一次 | 涡轮升级 500 → 300；EnergyBonus 改动（B 早期批）；两个 Command_Upgrade*PowerPlantTurbine 命令在命令集 L18/L23。“1.5 倍”的实际电量待实测 |
| 特殊炮台 360 度 | L32/L33/L200–L204 | AlliedCoastalGun、JapanWaveForceTripleCannon、Soviet/Allied RushmoreLaserHead 都用 Replace 方式重写了 TurretSettings，里面没有 MaxDeflection；乌克兰炮 SovietArtilleryDomeMissle AcceptableAimDelta 25d。穿模、头像不转动属于实测项（L1605） |
| 谭雅冲刺、科技建筑可建造、快速生产中心、复制中心、地标、帝国装饰 | L1581 | 已在包内 |
| 天启移动开火 | L821/L825 | 原版主炮已经可以边走边打；鱼叉、对空导弹在实包里也是 CanFireWhileMoving=true。不需要改源码，只需实测 |
| 多辆天启鱼叉同一建筑 | L825 | XML 里没有限制，只需实测，不需要改源码 |

## B. 待做（值已确认，可直接排批）
| # | 项 | devdoc 行 | 确认值 / 做法 | 依赖与风险 |
|---|---|---|---|---|
| 1 | 幻影坦克移动开火 | L10/L592/L595/L596 | PrismCannon 和 _Veteran 的 AcceptableAimDelta 10d → 180d；_Veteran 的 CanFireWhileMoving false → true | 只改 Weapon.xml，见 NEXT_R89 |
| 2 | 苏联防空炮可以对地 | L779/L782/L783 | 首选方案：新建武器 SovietBaseDefenseAirFlakCannonGround（inheritFrom 原武器，RequiredAntiMask = ANTI_GROUND ANTI_STRUCTURE ANTI_WATER），作为同一炮塔的 SECONDARY；MinimumPitch 45d → -10d | 是否换 DamageType 用户“待定”，默认保持 FLAK（打步兵只有 10%）。需要补 SECONDARY 的开火骨骼。见下方“第二小批” |
| 3 | 磁能坦克 | L881/L884/L885 | 1500 / 15 秒 / 前提超级反应堆；速度 62.5 → 70；加入 SovietWarFactoryCommandSet | S08 的覆盖保持不动 |
| 4 | 苏军间谍 | L899/L902/L903（L909 是复制做法） | 复制盟军间谍：1000 / 8 秒 / RequiredObject SovietWarFactory，加入苏联兵营命令集 | 复制时必须去掉 Upgrade_AlliedTech2。名字和简介字符串的做法待查 |
| 5 | 袋狸轰炸机 | L887/L890/L891/L893/L896 | 复制世纪轰炸机，改成苏联阵营、换成袋狸模型；2000 / 20 秒 / 作战实验室；在苏联机场生产；载员 5 | 载员数待实测 |
| 6 | 精准轰炸机 | L640/L643/L644/L649/L650 | 新建 AlliedSupersonicBomber_Buildable：1500 / 10 秒，只需机场；JetAIUpdate、TAXIING、命令集、回机场装弹的武器都照维和轰炸机（AlliedAntiGroundAircraft）抄 | 模块较多，单独一批 |
| 7 | 基洛夫加速 | L845/L849 | 改成限时 10 秒、冷却 30 秒、不掉血（删除 LoseHealthUpdate 200）；被击落时威力 / 范围相当于 5 颗炸弹 | 坠毁武器名“待查”，5 颗炸弹的具体数值要先查 SDK，不能编 |
| 8 | 苏联战车工厂 / 船厂维修无人机 | L29/L30/L222/L1560/L1609 | 照抄盟军 / 帝国工厂原版模块：SpecialPower_TargetedRepairVehicle + 3 架维修无人机 | 船厂无人机能否修船要实测 |
| 9 | 先进幻影坦克 | L10–L14/L586–L590 | 新 id AlliedAdvancedMirageTank，inheritFrom CAMP_A08；速度 80 / 1500 / 15 秒 / 国防局；T3_UNIT；按钮和头像用幻影坦克的；力场刷新 0.01 → 0.2 秒；保留 A08 音效 | FAKE 模型原版只在战役加载，ART 必须进全局，这和包内“剥离 ART”的惯例冲突，要先研究。新字符串、简介的做法待定。#1 完成后它自动继承移动开火 |

## C. 需要先补参数或做决定（不得猜）
- **帝国版总统山头像**（L788）：前提纳米电脑主机已确认；“核心时间 + 展开时间 = 30 秒”的拆分待定（建议核心 5 秒 + 展开 25 秒）。另外 L1581 说帝国新建筑改为直接放置，所以要问用户：直接放置 30 秒，还是核心 + 展开？
- **科技机场伞兵**（L398/L401/L402/L1601）：
  - 已定：9 分钟冷却；空投 5 名步兵（盟军 3 维和 + 2 标枪 / 苏联 3 征召兵 + 2 防空兵 / 帝国 3 武士 + 2 坦克杀手）；默认从地图边缘飞入。
  - 未定：按钮放在协议栏还是科技机场上（devdoc 说实测后再定，建议先按方案 B）；用哪架飞机（原文是袋狸）。
- **盟军红警 2 式建造范围**（L466–L470）：做法是给盟军各建筑加 ProjectedBuildabilityInfo，但每个建筑用多大半径没有给值（苏联先例：电厂 180、兵营 195）。需要用户确认：照搬苏联同类建筑的值，还是统一一个值。
- **基洛夫坠毁威力**：先查 SDK 的坠毁 OCL 和炸弹武器，再算“5 颗炸弹”的值。

## D. 已取消（不做）
- 苏军起重机 / 回收站（L29）
- 任务 overrides 里的建筑副本同步（L29）

## 安全小批次顺序（建议）
1. **R89**：幻影坦克移动开火（只改 Weapon.xml，3 个属性）
2. **R90**：苏联防空炮对地（1 个新武器 + 1 个建筑文件）
3. **R91**：磁能坦克
4. **R92**：苏军间谍
5. **R93**：苏联工厂维修无人机
6. **R94**：基洛夫加速（先查清坠毁数值）
7. **R95**：袋狸轰炸机
8. **R96**：精准轰炸机
9. **R97**：先进幻影坦克（先研究 ART 打包）
10. **R98**：帝国总统山头像、伞兵、盟军建造范围（拿到决定后再做）

每批都按“只改一处 → 审计 → 下一批”推进。
