# Doc-wide coverage + mechanism research (read-only, after 48_FIX)
Basis: devdoc.txt (1735 lines, item headers = number line + request line), package b80 (=48_FIX, 94 XML), SDK XMLFiles. Status legend: **DONE** field seen in package diff vs SDK · **PART** partly · **MISS** no package file/field · **NC** no change needed (SDK already within cap) · **NONXML** Lua/map/options/script, outside current XML batches · **USER** needs user value · **TEST** in-game test only · **?** not verified this round (do not count as done).
Per-item "DONE" = field present; values were audited in earlier batches only where noted. Not a full coverage proof.

## Decision conflicts checked
| Topic | Earlier | Latest (wins) | Evidence |
|---|---|---|---|
| Quick-prod build time | 2026-11-02 memory: Allies/Soviet 30 s, Empire core 3 s + unpack 25 s | **2026-11-06: all three 28 s, Empire placed directly (no core)** | doc L29 user quote "3.三军造快速生产中心都是28秒"; L263; L36; shared memory 2026-11-06 "takes 28 s for all three factions" |
| Quick-prod model | Kremlin | AM_AlliedFutureTechHQ | L35/L36/L263, memory 11-06 |
| Quick-prod build effect | — | no build animation/dust, appears when placed | memory 11-06 |
| Quick-prod health | — | **still undecided** ("新对象按正常建筑设定血量（待定）" L263); no later user value in doc or memory | |
| Clone center health | — | **never decided**: L806 only describes "原血量 7500"; memory 11-06 lists 2500/30 s/power 100/Battle Lab/RA2 effect, no health | |
Other chat transcripts: not readable from this run (no session id), so only doc + shared memory were checked.

## 5.1 Global (L163–L283)
| # | Req (short) | Status | Evidence |
|---|---|---|---|
|1|ore ×2|DONE|BaseOreNode MaximumGatheredValue 60000|
|2|miner load ×2, speed 1.5|DONE/PART|BaseMiner DeliveryCapacity 500; miners Speed 75 (A/S/J)|
|3|passengers survive|PART|KillPassengersOnDeath=false on several vehicles; full list ?|
|4|instant capture|?|no engineer capture field seen|
|5|global: buildable in campaign|NONXML/?|overrides/maps|
|6|default lowest quality|NONXML|options.ini|
|7|360° turrets|DONE?|coastal gun/ArtilleryDome/FI gun rewritten (B-batches)|
|8|crush without stopping|?|locomotor; not found|
|9|defences halved|DONE|A/S/J BaseDefense(Advanced) times|
|10|PP 8, barracks 8, refinery 18, WF 18…|PART|Allied barracks/PP/WF/naval/refinery, Japan PP/refinery, Soviet PP adv; Soviet barracks/WF/PP basic ?|
|11|tech buildings 1000/15, academy 1500/15|PART|AlliedTechStructure 1000/15 — **caution: AlliedTechStructure is Defense Bureau, check intent**; neutral tech buildings MISS|
|12|SW ≤30 s, ≤3500|DONE/NC|JapanSuperWeaponAdvanced 3500; others ≤30 s in SDK|
|13|Iron Curtain 60 s, ×1.5 radius; Chrono ×1.5|?|SpecialPowerTemplates/Weapon changed; per-item ?|
|14|Proton shots ×2|?||
|15|Vacuum duration ×2|?||
|**16**|**MCV ≤3000 / ≤30 s (3 sides)**|**MISS**|SDK Allied/Soviet/Japan MCV 5000/60; no MCV file in package; doc L257-258 decided "全部改为 3000 / 30 秒", campaign has no MCV override|
|17|quick-prod center|MISS / USER health|see below|
|18|no facing damage|dropped (L29 "这个不改了")|
|19|music off default|NONXML|
|20|left-click command|NONXML|
|21|Uprising import|**excluded by user**|
## 5.2 Tech buildings (L367–L421)
1–10 oil/hospital/garage/drydock/airport/paratroop/academy/outpost/shop/bank: **MISS** (no Neutral/Structures files in package). Values partly user-decided (L224); needs per-item read before batching.
## 5.3 AI (L434–L440): CoopBasePersonality changed (BRUTAL 100%) = PART; "acts like human" NONXML/approx.
## 5.4 Allied (L453–L693)
|#|Req|Status|
|---|---|---|
|1–2|no T1/T2 permits|?|
|3|RA2 build radius|MISS (ProjectedBuildabilityInfo not in package)|
|4|multi-gunner turret passengers survive|DONE (AlliedBaseDefense KillPassengersOnDeath=false)|
|5|PP upgrade 300, 1.5×, 10 s|DONE (upgrade.xml 300/10s, EnergyBonus 50)|
|6–7|coastal gun 2000/15 s, homing|PART: package BuildTime=30 — **doc L483 says 15 s → re-check** |
|8|peacekeeper shield speed 35|?|
|9|javelin cooldown in IFV|?|
|10|engineer tent ×1.5|DONE (150)|
|11|spy bribe ×2, cd 15, steal half|DONE/PART (DominateRadius 130, STEAL_MONEY)|
|12|engineers 8 s, heroes need Battle Lab|DONE 8 s; hero prereq ?|
|13–14|Tanya 20 s, sprint, C4 1.5 s|DONE/PART (sprint module, 20 s)|
|15|surveyor unpack 15 s, ×1.5|DONE (OutPost 15s)|
|16–17|miner 12, ACV 8, IFV 8, dolphin 8, fortress 10|DONE (12/8/8/8); fortress = new unit MISS|
|18|Riptide clip ×2|? (Weapon.xml)|
|19|IFV survive|DONE|
|20|Guardian 1 s|? (Weapon.xml)|
|21|Athena ×1.5, focus 0.5|PART (Speed 75)|
|22|Mirage/Athena ≤1500/15|PART|
|23|low-profile Soviet tank (AntiVehicleVehicleTech3)|PART (1500 set)|
|24|mirage fire on move|?|
|**25**|**MCV speed 1.2× (50→60) + MG**|**MISS** (speed batch 1, MG batch 2: L601-602)|
|26–31|bomber shots, Apollo AG, cryo heli, Century, hydrofoil, assault destroyer|PART/?|
|32–33|precision bomber, vindicator 1000/10|PART (AntiGroundAircraft 1000/10)|
|34–37|spy in IFV 1 s, Battle Fortress, GI, Heavy GI|MISS (new units)|
|38–40|destroyer 15, carrier 20, drones|DONE (15/20, drone speed 337.5)|
|41|Statue of Liberty|DONE (48_FIX)|
## 5.5 Soviet (L706–L928)
|#|Req|Status|
|---|---|---|
|1|sentry gun conscript survive / spawn|?|
|2|Battle Lab 30 s|DONE (unpack 30s, 2000)|
|3|flak mines on crush|?|
|4|combat engineer|?|
|5|Tesla trooper charge ½, ×1.5, 500|PART (500/8 s)|
|6|Natasha|PART (20 s)|
|7|miner MG, ×1.5|PART (speed)|
|8–9|vehicle times, Stingray 8|DONE (8 s)|
|10|Bullfrog AG|? (Weapon.xml)|
|11|Hammer rate|?|
|12|Tesla coil ≤15|DONE|
|13|flak cannon AG|?|
|14–15|Rushmore/Moai|DONE|
|16|Ukraine cannon|DONE|
|17|clone center|MISS / USER health|
|18|Kremlin, Heroes statue|DONE|
|19|V4 ≤1500/15, Apoc ≤20, V4 speed ≥70|NC cost/time (SDK 1200/15, 20 s); V4 speed ?|
|20|Apoc ×1.5, AA, harpoon|MISS|
|**21**|**MCV speed 1.2× (50→60) + MG**|**MISS** (L829-830 "同盟军基地车")|
|22–25|Twinblade AA, MiG AG, Kirov, Stingray|PART (Kirov 2000/20)|
|26–29|sub 15, dreadnought 20, Tesla charge|DONE times; rest ?|
|30|Tesla tank (memory: 1500/15, super reactor, speed 70)|MISS|
|31–32|Grinder/Bear bomber|PART|
|33–38|engineers, spy, demo truck, Crazy Ivan|PART (engineer 8 s); new units MISS|
## 5.6 Empire (L941–L1091)
PP upgrade DONE; permits ?; Shinobi/tank buster/VX/Tengu/Jet AG mostly ? (Weapon.xml changes not mapped); Yuriko unlimited ?; miner 12/×1.5 DONE; Tengu 8 DONE; **#15 Japan MCV MG MISS (batch 2)**; wave gun no pre-fire ?; King Oni / Shogun / Wave cannon DONE (eggs + mecha); ship times DONE; Yari sprint DONE; Shogun sprint DONE; **#25 decorations DONE except Guard02 (USER health) and Rushmore Japan core/unpack split (USER)**; #26 CY build range MISS.
## 5.7 Campaign (L1104–L1200): all **NONXML** (map scripts / Lua / starting money) — not in package.

## Smallest next items not blocked by health
1. **MCV cost/time (5.1 #16)** — Allied/Soviet/Japan MCV `BuildCost 5000→3000`, `BuildTime 60→30`; unpack untouched (L257). Attach: Allied/Units/AlliedMCV.xml, Soviet/Units/SovietMCV.xml, Japan/Units/JapanMCV.xml.
2. **Allied + Soviet MCV speed 50→60** (5.4 #25, 5.5 #21; L601 "速度一批"). Each file has a second LocomotorSet after L79/L58 → read and decide whether it is a water/other condition before changing (do not change blindly). Japan MCV speed not requested.
3. Re-check **coastal gun BuildTime 30 vs doc L483 "15秒"** (possible later override L785 "2000，30秒" — L785 says "盟军巨炮造价2000，30秒，需要国防局" → 30 s is the newer text; record as resolved by L785).
4. MCV machine guns = batch 2 (needs weapon + fire bone; L602).

## Mechanism research
### Quick-production center: "halve production while owned, restore immediately"
- Engine supports a production-speed attribute: `AssetTypeAttributeModifier.xsd` L42 `PRODUCTION`; used by `GlobalData/AttributeModifier.xml` L912-945 (CryoBeam: PRODUCTION 80…0.01% slows frozen factories) → value is a rate multiplier; **200% = double rate = half time** (inference from <100% slowing; TEST).
- Distribution: `AttributeModifierAuraUpdate` (schema `Modules/AttributeModifierAuraUpdate.xsd`: Range, RefreshDelay, ObjectFilter, InitiallyActive, RunWhileDead…). Precedent `Civilian/Tokyo_Harbor_TH/Buildings/TH_EmperorFlagpoleStatue.xml` L31-43 (RefreshDelay 0.75s, Range 400, ObjectFilter Relationship) with modifier `AttributeModifer_EmperorsStatue` Duration="2s" (AttributeModifier.xml L583-585).
- Plan: center has AttributeModifierAuraUpdate, `AttributeModifierName` new `AttributeModifier_RapidProduction` (Category NONE, Duration 2s, `<Modifier Type="PRODUCTION" Value="200%"/>`), RefreshDelay 0.75s, Range map-wide (large value), ObjectFilter `Rule="ANY" Include="FS_FACTORY" Relationship="SAME_PLAYER"` (FS_FACTORY on barracks/war factory etc., e.g. SovietBarracks L41).
- Restore: aura stops when the center dies/is sold (RunWhileDead default false); captured → owner changes, SAME_PLAYER now targets the captor; modifier expires ≤2 s. Matches "立即恢复" within ~2 s (TEST). Non-stacking: limit 1 + same modifier name.
- Note user's 11-02 wish "global like low power, not range aura": map-wide Range gives global effect; no XML player-level production multiplier exists (UnitAISettings LowEnergy values are global engine constants, not switchable per building). TEST: whether Japan cores/egg production counts.
- Alternative (rejected as primary): CaptureAndGiveUpgrade → PLAYER upgrade → `AttributeModifierUpgrade` on each factory (precedent TH_ImperialHarborBuilding L153-157): upgrade removal on loss is not guaranteed for AttributeModifierUpgrade.
### Clone center
- Owner → player upgrade: `CaptureAndGiveUpgradeBehavior` (schema only UpgradeMap OwnershipAmount/ProvidedUpgrade; precedent VeterancyTechStructure L52-58). Ownership-count based → should work for built buildings and drop on loss (TEST).
- Barracks translate: SovietBarracks L427-447 `GiveUpgradeToProduced/UpgradeTranslate` RequiredUpgrade=PLAYER upgrade → ProvidedUpgrade=OBJECT upgrade. Barracks needs ProductionUpdate merge (copy with xai merge of id ModuleTag_06).
- Spawn: `ObjectCreationUpgrade` (ThingToSpawn, TriggeredBy) per infantry; precedent SovietAntiVehicleVehicleTech1 L1411-1415. Clone spawned by OCU is not barracks-produced → no CloneMe → no loop.
- Infantry list (SDK SovietBarracksCommandSet): SovietScoutInfantry (war bear), SovietAntiInfantryInfantry, SovietAntiVehicleInfantry, SovietEngineer, SovietHeavyAntiVehicleInfantry, SovietCommandoTech1 (Natasha). Soviet spy = new mod unit (5.5 #34) not yet existing → add later. Package already holds 4 of 6 (Engineer, AntiVehicleInf, HeavyAntiVehicleInf, CommandoTech1); missing SovietScoutInfantry, SovietAntiInfantryInfantry, SovietBarracks.
- Upgrade templates: GlobalData/upgrade.xml L46-49 pattern (Type PLAYER, Options DO_NOT_TRANSFER) + OBJECT type for CloneMe.
- Remaining TEST: Natasha MaxSimultaneousOfType 1 vs OCU, rally point, veterancy.

## Minimal user questions (not sent)
1. Clone center health (no value ever given).
2. Quick-production center health (L263 "待定").
3. (existing) Guard02 health; Japan Rushmore core/unpack split.
