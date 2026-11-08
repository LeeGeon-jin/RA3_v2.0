# Next item research: Clone Center vs Quick Production Center (read-only)
Package state (b80 = 48_FIX): **neither implemented**. No VIPBunker/FutureTech/Clone/QuickProduction object, command, upgrade or Mod include (grep). SovietBarracks.xml and Soviet infantry for cloning are partly absent (package has SovietEngineer, SovietAntiVehicleInfantry, SovietHeavyAntiVehicleInfantry, SovietCommandoTech1 only; no barracks).

## A. Soviet Infantry Clone Center — devdoc L803 (request), **L806** (decision + mechanism), L34 (7.能复制，只要是兵就能复制), L1571 (risks)
Decided (L806): cost 2500; Soviet unpack `UnpackTime="30s"`; `EnergyProduction="-100"`; prerequisite SovietTechStructure; `MaxSimultaneousOfType="1"`, not stacking; model GE_SovietVIPBunkerSubStructure (Name:SovietVIPBunker, LOOP animation); all barracks infantry cloned incl. engineer, war bear, spy, Natasha.
**Not decided:** health. L806 only states "原血量 7500" (description); no "沿用原版" decision as for landmarks → ask user (7500 original vs other). Armor not stated (source inherits StructureArmor; keep = no change).
Mechanism (SDK-verified):
- `Neutral/Structures/VeterancyTechStructure.xml` L52-58 CaptureAndGiveUpgradeBehavior UpgradeMap OwnershipAmount→PLAYER upgrade (only 2 uses in SDK; whether it fires for self-built buildings = test item per L806; fallback GrantUpgradeCreate `Allied/Structures/AlliedConstructionYard.xml` L501 + removal on loss, unresolved).
- `GlobalData/upgrade.xml` L46-49 template pattern (Type PLAYER, DO_NOT_TRANSFER) → new `Upgrade_SovietCloning_1` (PLAYER) + `Upgrade_CloneMe_1` (OBJECT).
- `Soviet/Structures/SovietBarracks.xml` L427-447 ProductionUpdate GiveUpgradeToProduced → add UpgradeTranslate Cloning_1→CloneMe_1 (needs full barracks copy into mod).
- `Soviet/Units/SovietAntiVehicleVehicleTech1.xml` L1411-1415 ObjectCreationUpgrade ThingToSpawn/TriggeredBy → add to every barracks infantry (list must be enumerated from SovietBarracks CommandSet, not guessed).
Size: large (building + 2 upgrades + barracks + N infantry). Footprint ~136×88, height 125.
Minimal first slice (if user gives health): building only = copy GE_SovietVIPBunkerSubStructure (Includes L5-8: NoGarrisonDestructible, ART W3X, YU_HotelDebris, `Civilian/Geneva_GE/Props/GE_SovietVIPBunkerSubStructure_Collapse.xml`), new id, Side Soviet, BuildTime 0 + StructureUnpackUpdate 30s, -100, GameDependency SovietTechStructure, Max 1, OTHER_STRUCTURE, CaptureAndGiveUpgrade + upgrade templates; barracks/infantry in a later batch.
Attach: Civilian/Geneva_GE/Buildings/GE_SovietVIPBunkerSubStructure.xml; Civilian/Geneva_GE/Props/GE_SovietVIPBunkerSubStructure_Collapse.xml; Civilian/Yucatan_YU/Props/YU_HotelDebris.xml; Neutral/Structures/VeterancyTechStructure.xml; GlobalData/upgrade.xml; Soviet/Structures/SovietBarracks.xml; Soviet/Units/SovietAntiVehicleVehicleTech1.xml; Allied/Structures/AlliedConstructionYard.xml; package Soviet/Structures/SovietTechStructure.xml (GameDependency syntax) and SovietGreatKremlinPalace.xml (unpack template).

## B. Quick Production Center — devdoc L260 (request), **L263** (decision), L264 (evidence/mechanism), L29/L34/L36, L1610 (test)
Decided: all three sides; cost 2000; 28 s (Allied BuildTime 28, Soviet unpack 28 s, Japan direct place BuildTime 28 CONSTRUCTION_YARD_CONSTRUCT); prerequisite AlliedTechStructure / SovietTechStructure / JapanTechStructure; -75 power; limit 1 per player; owning one = production time halved, lost/sold/captured → restored immediately; look AM_AlliedFutureTechHQ (30×30×40).
**Not decided:** health — L263 "新对象按正常建筑设定血量（待定）" (original 50000, armor AlliedConYardArmor). Ask user.
**Mechanism not yet resolved:** L264 ④ proposes a player-level multiplier "like low power" (UnitAISettings MinLowEnergyProductionSpeed) — that is an AI/power setting, not a per-building switch. Needs SDK research for an XML player production-speed modifier (candidates to check next: AttributeModifier `PRODUCTION`-type category, PlayerUpgrade + ProductionSpeed modifiers). Not settled → not implementable yet.
Attach: Civilian/Amsterdam_AM/Buildings/AM_AlliedFutureTechHQ.xml (+ its _Collapse in Amsterdam_AM/Props), Civilian/Yucatan_YU/Props/YU_HotelDebris.xml, Allied|Soviet|Japan/Structures/*TechStructure.xml.

## Recommendation
Clone center is better specified (all numbers but health, mechanism has SDK precedents). Ask user ONE question: clone center health (original 7500?) and quick-prod health. Meanwhile research the production-speed modifier. Guard02 health still undecided.

## Coverage gap
Full coverage list still missing; this only covers L263/L806. A doc-wide item sweep vs package is still owed.
