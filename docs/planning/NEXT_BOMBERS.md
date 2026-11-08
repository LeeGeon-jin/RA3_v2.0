# NEXT: two hidden aircraft. Base now Batch95FIX2 (sha c2ca369e…; static PASS 23:5x). Read-only spec, 2026-11-08 UTC+10
Both are new objects. **The original summoned aircraft are not modified**: the protocol / support powers keep spawning them through ParabolicCurve OCLs.

## A. 精准轰炸机 (precision bomber): AlliedSupersonicBomber → new AlliedSupersonicBomber_Buildable
### devdoc wording (L640/L643/L644/L649/L650)
- User decided 1500 / 10s, **no protocol needed, airfield is enough**. "精准轰炸机是最高机密协议里的飞机，如果你造不了就不要拿别的飞机改".
- Only the original aircraft: same model AUSupersonicBomber, same bomb, Speed 400, MaxHealth 2000.
- "待测（任一项不过即整项取消，不做替代）": park / take off / attack / return to reload; it must not fly off and vanish; AI must not build it (not added to the AI build list).
### SDK facts (static)
- The original is loaded globally: Allied.xml L33 includes it, with ART AUSupersonicBomber.w3x included `all` in the file.
- Original object:
  - IsTrainable false; CommandSet EmptyCommandSet.
  - KindOf has SUMMONED IGNORES_SELECT_ALL SKIRMISH_AI_DONT_CONSIDER_THREAT and no SELECTABLE.
  - **No SelectPortrait / ButtonImage / BuildCost / BuildTime.**
  - LocomotorSet AlliedSupersonicBomberLocomotor Speed 400 (Surfaces AIR, MinTurnSpeed 0%). No TAXIING.
  - Weapon slot AlliedPrecisionBomb: ClipSize 1, AutoReloadsClip NONE, range 150, ANTI_WATER/GROUND/STRUCTURE.
  - Behaviors include ParabolicCurveUpdate (ModuleTag_ParabolicCurve) and DestroyDie ModuleTag_DeathFaded.
  - AI is a plain AIUpdate (ModuleTag_AIUpdate).
- Production building = **AlliedAirfield**: ProductionUpdate Type AIRCRAFT; ParkingPlaceBehavior 2×2, LimitedProductionAircraftSpots 4; CanParkHereFilter Exclude SUMMONED + ExcludeThing AlliedSupportAircraft. So the new object must not have SUMMONED and must have LIMITED_PRODUCTION_AIRCRAFT to take a pad.
- Template aircraft AlliedAntiGroundAircraft (维和轰炸机):
  - TAXIING BasicHelicopterTaxiLocomotor Speed 10;
  - JetAIUpdate (NeedsRunway false, KeepsParkingSpaceWhenAirborne true, OutOfAmmoDamagePerSecond 1.5, CirclesForAttack, ReturnToBaseWhenVictimDead, JetAIStateMachine);
  - ReturnToProducerSpecialPower (SpecialPowerReturnToProducer, AttributeModifier_ReturnToBase, USER_1 30s);
  - CommandSet AlliedAntiGroundAircraftCommandSet (Command_AlliedAntiGroundAircraftReturnToAirfield + Command_AttackMove);
  - its own Draw has no Animation entries.
### Spec (devdoc ①–⑥, via inheritFrom; module removal uses the SDK pattern `xai:joinAction="Remove"` on the same id, e.g. MR_LaserMtRushmore_Roosevelt_Ready L135–137)
1. New file Allied/Units/AlliedSupersonicBomber_Buildable.xml:
   - Include instance `DATA:Allied/Units/AlliedSupersonicBomber.xml`.
   - `inheritFrom="AlliedSupersonicBomber"`, EditorSorting UNIT.
   - KindOf full replacement: `CAN_CAST_REFLECTIONS CAN_ATTACK SELECTABLE SCORE AIRCRAFT VEHICLE ASSAULT_AIRCRAFT NO_COLLIDE LIMITED_PRODUCTION_AIRCRAFT`. That is: removes SUMMONED / IGNORES_SELECT_ALL / SKIRMISH_AI_DONT_CONSIDER_THREAT, adds SELECTABLE / ASSAULT_AIRCRAFT / LIMITED_PRODUCTION_AIRCRAFT. NO_COLLIDE is kept from the original; devdoc doesn't mention it.
   - IsTrainable true; BuildTime 10; BuildCost 1500.
   - **No GameDependency.** Checked: SDK AlliedAntiGroundAircraft has none, because being in the airfield command set already means "有机场即可". The airfield is the production building, not a prerequisite entry.
   - CommandSet AlliedAntiGroundAircraftCommandSet (reused; it has the return-to-airfield and attack-move commands).
   - Add a TAXIING LocomotorSet: BasicHelicopterTaxiLocomotor Speed 10.
   - Behaviors:
     - Remove ModuleTag_ParabolicCurve.
     - Replace the WeaponSetUpdate slot with the new weapon.
     - Add ReturnToProducerSpecialPower copied from the template.
     - DestroyDie FADED stays; it only fires on FADED.
   - AI: Remove ModuleTag_AIUpdate, add JetAIUpdate copied from AlliedAntiGroundAircraft L268–281.
   - Draw: inherited unchanged.
2. Weapon.xml: `AlliedPrecisionBomb_Buildable` inheritFrom AlliedPrecisionBomb with AutoReloadsClip="RETURN_TO_BASE" (same pattern as R90).
3. LogicCommand: new Command_ConstructAlliedSupersonicBomber_Buildable (UNIT_BUILD).
4. LogicCommandSet:
   - The package has **no AlliedAirfieldCommandSet**. Add the full SDK L67–73 set plus the new command before the Recall command.
   - Button budget: 5 → 6 commands.
5. Mod.xml +1 all.
6. **Not fixed by devdoc** ("补字符串和头像", without saying which image). The original has no portrait. The candidate existing global image is `Button_PlayerPower_PrecisionStrike` (UI/ButtonStateDataCommon L146). That would be my inference; confirm it or let the user pick. Name / Desc string keys are new (same unresolved string issue as the other new units).

## B. 袋狸轰炸机 (Badger bomber): SovietSupportBomber → new buildable copy (ID not given in devdoc; inferred `SovietSupportBomber_Buildable`)
### devdoc wording (L887/L890/L891/L893/L896)
- Buildable. "能装与实际支援轰炸机相同数量的伞兵，并能像世纪轰炸机一样投弹（可理解为换皮的世纪轰炸机）".
- 2000 / 20s, **prerequisite SovietTechStructure (作战实验室), produced at the Soviet airfield** (SovietAirfieldCommandSet button).
- Route (L891): **copy the Century bomber AlliedBomberAircraft**, switch it to the Soviet side, use the Badger model, and replace its 国防局 prerequisite with SovietTechStructure.
- Capacity: 5, "待实测".
### SDK facts (static)
- Badger: Soviet.xml L35 global. SovietSupportBomber inheritFrom BaseSovietSupportBomber (instance include, ART SUSupportBomber.w3x `all`), so the model is in the global stream.
  - Base: SUMMONED, IsTrainable false, placeholder SelectPortrait / ButtonImage **Portrait_GDIOrca**, CommandSet AlliedBomberAircraftCommandSet, Speed 300.
  - The skirmish object carries the Desolator bomb + ParabolicCurve.
  - The transport variant is the campaign-only SovietSupportBomber_S07.
- Badger Draw (Base L49–118):
  - Model SUSupportBomber, ExtraPublicBone + WeaponLaunchBone SUSUPPORTBOMBER, 4 ParticleSysBone Box01–04;
  - a looping AnimationState "SUSupportBomber";
  - DAMAGED / REALLYDAMAGED states.
  - **No PRK / HVRA / MOVA parking or hover animations.**
- Century bomber (package b92fix2 = SDK + RequiredObject AlliedTechStructure):
  - Cost 2000, BuildTime 20;
  - KindOf includes LIMITED_PRODUCTION_AIRCRAFT and **AIRCRAFT_TRANSPORT_ONLY_GARRISONABLE_WHILE_PARKED** plus TRANSPORT;
  - TransportContain ContainMax 5, PassengerFilter INFANTRY, PassengerData BonePrefix BONEGARRISON;
  - ConditionForEntry="INVALID". The xsd type is a ModelConditionFlagType, so INVALID means no model condition is required. **It does not mean "can't board"**, which corrects devdoc L891. Infantry board while it is parked; that's what the KindOf says.
  - Eject: SpecialPower_EjectPassengersUntargeted, TimePerPassenger .25s, Height 150.
  - Weapons: AlliedBomberAircraftBombWeapon (+ _AirPower).
  - JetAIUpdate; TAXIING locomotor; AlliedAirPower xi:include / StatusBits / SubObjectsUpgrade (Allied protocol only).
  - CommandSet AlliedBomberAircraftCommandSet (eject + attack move).
- Production building = **SovietAirfield**: ParkingPlaceBehavior 2×2, LimitedProductionAircraftSpots 4; CanParkHereFilter Exclude SUMMONED + ExcludeThing AlliedSupportAircraft / SovietAntiGroundAircraft / SovietBomberAircraft. The new object (no SUMMONED, LIMITED_PRODUCTION_AIRCRAFT) can take a pad, shared with the MiGs.
### Spec
1. New file Soviet/Units/SovietSupportBomber_Buildable.xml = **full copy of package Allied/Units/AlliedBomberAircraft.xml**. Change:
   - id / EditorName / names → SovietSupportBomber_Buildable; Side Soviet.
   - RequiredObject AlliedTechStructure → SovietTechStructure.
   - Draw: **replace** the Century ScriptedModelDraw (AUBomberAircraft models + PRK / HVRA / MOVA animation states) with the Badger Draw from BaseSovietSupportBomber L49–118, verbatim. Its ART include is `ART:SUSupportBomber.w3x`, already global; keeping or stripping it follows package convention.
   - Keep everything else: cost 2000, time 20, KindOf, TransportContain 5, eject, Century bomb weapon, JetAIUpdate, TAXIING, CommandSet AlliedBomberAircraftCommandSet, armor, body.
   - Allied-only AirPower modules (xi:include AlliedAirPowerUpgrade, StatusBitsUpgrade, SubObjectsUpgrade Upgrade_01, the _AirPower weapon) never trigger for the Soviets. Keeping them is the smaller diff, but SubObjectsUpgrade "Upgrade_01" refers to a sub-object that the SU model doesn't have. **Technical choice: drop SubObjectsUpgrade only; keep the rest.** Inferred.
2. LogicCommand: Command_ConstructSovietSupportBomber_Buildable.
3. LogicCommandSet: the package has **no SovietAirfieldCommandSet**. Add the full SDK L367–372 set plus the new command before Command_SovietRecallAllAircraft (4 → 5).
4. Mod.xml +1 all.
5. ExperienceLevels: SDK has SovietSupportBomber_Experience targeting only the summoned ID. The Century bomber's own levels target AlliedBomberAircraft. For full parity, add rank templates for the new ID (same method as R92, with the parents included as an instance). Inferred; required for parity.
6. **Not fixed by devdoc:** portrait / button. The SDK placeholder is Portrait_GDIOrca (a C&C3 leftover; whether the image exists in RA3 is unproven). An existing global candidate is `Button_PlayerPower_DesolatorBomb1` (UI/ButtonStateDataCommon L814). **Choose or confirm before implementing.**

## Static vs runtime
| | Statically provable | Runtime / airfield test |
|---|---|---|
| Both | Object / command / set IDs exist, single definitions; production building and pad filter accept the new objects; models are in the global stream; schema patterns (inheritFrom + Remove, inherited weapon) | Pad parking, vertical take-off/landing, taxi, attack and RTB reload; no fade-out; AI not building; button/portrait show |
| Precision | Weapon reload type | It doesn't "fly off and vanish" (devdoc: any failure = whole item cancelled, no substitute) |
| Badger | Capacity 5, boarding allowed while parked (KindOf + ConditionForEntry semantics) | Infantry actually boarding / ejecting; the bone-less SU model holding passengers (BONEGARRISON bones are absent; passengers are ENCLOSED); looping prop animation while parked; bomb drop from the SUSUPPORTBOMBER launch bone |

Refs: bombers_sdk_refs.tar.gz

---
## 补充（22:58 指令）
### A. “AI 不造”的实际实现依据（静态证据，运行时未证）
- AI 只会生产在以下三处被显式点名的 ID：
  1. `SkirmishAI/States/*BaseStates.xml` 的 `AIBuildStateDefinition` → `<BuildEntry Build="ID">`（例：AlliedBaseStates.xml L881–888 AlliedAntiGroundAircraftBuildState 只列 AlliedSupportAircraft / AlliedAntiGroundAircraft / AlliedBomberAircraft）；
  2. OpeningMoves `<Order Build="ID">`；
  3. Personality `SpecificUnitCap`。
- ArmyDef 不含单位清单。
- **实现方式 = 不做任何改动**：AlliedSupersonicBomber_Buildable、SovietSupportBomber_Buildable 不写入以上任何文件。审计项：grep 这两个 ID，在 SkirmishAI/ 下必须 0 命中。
- 是否真不造属于运行时项，未证。
### B. 袋狸 AI 禁造：原文核查
- devdoc 精确轰炸机条目有 “③AI 默认不会造（不加入 AI 建造表）”，属于**测试项**。
- 袋狸条目（L887–896、L40）**未找到**用户明确的 AI 禁造表述。
- “不加入建造表”只是最小改动的默认做法，**不得写成用户禁令**。如需 AI 造袋狸，需本人另定。
### C. UI 图标/头像（低风险技术项，未测）
- 精确轰炸机：ButtonImage / SelectPortrait 均用 `Button_PlayerPower_PrecisionStrike`（UI/ButtonStateDataCommon L146）。
- 袋狸：均用 `Button_PlayerPower_DesolatorBomb1`（L814）。禁用 SDK 占位 Portrait_GDIOrca。
- 不加载 C&C3 图片。不改既定外观与武器。
### D. 精确轰炸机取消规则（按 devdoc 原文记录）
- 任一测试项不过，即**整项取消，不做替代**。
- 本规格目前只是**源码候选**，不是最终承诺。

---
## 补充 E（23:5x 一致性复核，基线改为 95FIX2）
- **基线：** 本规格引用的包内文件与 95FIX2 的对应关系：
  - AlliedBomberAircraft.xml、AlliedAntiGroundAircraft.xml 与 b92fix2 逐字节相同，规格内对它们的引用仍然有效。
  - LogicCommand、LogicCommandSet、Weapon、Mod.xml 在 93 / 95 中有变化：LogicCommand 多了 Kirov 与高级幻影条目，LogicCommandSet 多了 AlliedWarFactoryCommandSet，Weapon 改了 Kirov 坠毁值。所以**行号以 95FIX2 为准**，refs tar 已换成 pkg_b95fix2。
  - 95FIX2 中仍**没有** AlliedAirfieldCommandSet / SovietAirfieldCommandSet，“整套照抄 SDK 再加新命令”的做法不变。
- **图标核实：** Button_PlayerPower_PrecisionStrike / Button_PlayerPower_DesolatorBomb1 是 SDK ButtonStateDataCommon L146 / L814 的 State Image 值，属全局现存图。新对象的 ButtonImage / SelectPortrait 直接写这两个 Image 名。显示效果未测。
- **军衔表（缺参，需用户决定，不得自造）：**
  - SDK 原召唤机：AlliedSupersonicBomberExperienceLevel_1 与 SovietSupportBomber_Experience 都只有 1 级（Required 1 / Award 10000）。照抄会让敌人击杀一架就得 10000 经验，不适合可建造单位。
  - 袋狸：规格写的是“照世纪轰炸机”，即 AlliedBomberAircraft 的 4 级：1/2000、6000/4000、12000/6000、18000/8000，inheritFrom 改为 ExperienceLevel_SovietRank1–4（推断）。
  - 精准轰炸机：devdoc 未定。候选是照维和轰炸机 AlliedAntiGroundAircraft 的 4 级（1/1200、3600/2400、7200/3600、10800/4800），**需用户确认**。或者不加等级表（是否可继承未证）。
  - 写法照 ExperienceLevels_SovietSpy / _AdvancedMirage 的先例：父 include 用 instance，Mod 以 all 加载。
- **AI 白名单依据文件：** 已把 SDK SkirmishAI/States/AlliedBaseStates.xml、SovietBaseStates.xml 放进 refs（Allied L881–888；Soviet L872 / L880 的空军 BuildEntry）。
