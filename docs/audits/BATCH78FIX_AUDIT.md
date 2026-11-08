# BATCH78FIX AUDIT — FAIL (1 static schema-order defect; everything else fixed)
No full XSD / compile / in-game test. Not Phase1 complete.

## Package
- `<agent-asset>` → `/workspace/ra3xfer/batch78fix.tar.gz`.
- 302173 B, sha256 1c2b5016…6a2cf4f match. Cumulative, data/ root. 124 XML parse. Mod: 3 reference / 122 all (unchanged vs 78).
- **vs 78: exactly 4 files differ** — the 3 centers + LogicCommandSet. The other 120 are byte-identical; Mod, AttributeModifier and LogicCommand are unchanged vs 78.
- vs 77: the 7 Batch78 files (3 new + AttributeModifier / LogicCommand / LogicCommandSet / Mod); the other 117 are identical.
- (The cloud's "7 changed" describes the cumulative change against 77, not against 78.)

## The 6 Batch78 defects
1. **BuildCost:** now `<ObjectResourceInfo><BuildCost Account="=$ACCOUNT_ORE" Amount="2000"/>`; the attribute is removed. Fixed (but see the order defect).
2. **StartsActive:** removed; InitiallyActive="true" remains. Fixed.
3. **Soviet UnpackTime:** `28s`. Fixed.
4. **BuildPlacementTypeFlag:** OTHER_STRUCTURE = ProductionQueueType OTHER_STRUCTURE in all 3. Fixed.
5. **Parent:**
   - Allied/Japan include + inheritFrom `BaseStructure`, Soviet `BaseSovietStructure` (include and inheritFrom are in sync).
   - Object `KindOf="+AIRCRAFT_PATH_AROUND"` is additive. The resulting flags were computed layer by layer:
     - BaseStructure: STRUCTURE SELECTABLE IMMOBILE CAN_CAST_REFLECTIONS NOT_AUTOACQUIRABLE AUTO_ACQUIRABLE_BY_AI COVER SCORE CAN_BUILD_ON_WATER CAN_BUILD_ON_DEEP_WATER (+ Soviet ACTIVATE_AFTER_UNPACK CRUSHABLE_BUILDING) + AIRCRAFT_PATH_AROUND.
     - This is the same set as AlliedTechStructure / JapanTechStructure (+FS_TECHNOLOGY) and SovietTechStructure.
     - CAPTURABLE is not on any SDK faction structure; engineer capture comes from GenericEngineerContain, now included.
     - The civilian flags (CIVILIAN_BUILDING, ALWAYS_VISIBLE_IN_RADAR, KEEP_CLASSIFIED…) are gone.
   - Sell: BaseStructure ModuleTag_StructureSellUpdate.
   - Added in Behaviors (xi namespace declared on the root): `xi:include DATA:Includes/GenericBuildingRepair.xml` (ModuleTag_RepairUpdate) and `GenericEngineerContain.xml` (ModuleTag_EngineerContain). This is the same pattern as AlliedTechStructure L411/L413. The InfiltratorContain spy include was not added (not required).
   - **Module ids:**
     - the object's Draw / Physics / Aura / BuildingDestruction / FXList / CreateObjectDie / DestroyDie / Body do not collide with BaseStructure / BaseObject ids (SellUpdate, DieSound, SecondaryDamageTracker, CatalystDeathWeapon, Sold, ConstructionAudio, IronCurtain, AttributeModifierPool);
     - Soviet ModuleTag_Physics re-declares BaseSovietStructure's — SDK precedent SovietSuperWeapon / SovietConstructionYard / SovietWallPiece;
     - ModuleTag_FXList `xai:joinAction="Replace"` with no parent counterpart — SDK precedent BaseStructure ModuleTag_DieSound (Replace over BaseObject, which lacks it);
     - Body is a single choice slot, and the child ActiveBody 2000/2000 replaces DefaultBody.
   - **Death:** the HQ has no SlowDeath (DestroyDie + CreateObjectDie collapse + BuildingDestruction + FXList); the parent adds the DieSound FX and the catalyst weapon. No duplicate death module.
6. **Soviet:** inherits +ACTIVATE_AFTER_UNPACK (BaseSovietStructure L12). Whether that holds back the InitiallyActive aura during the 28s unpack is runtime only.

## Commands
- The 5 entry lists now have the Cmd: AlliedConstructionYardCommandSetBase, AlliedCraneCommandSet (new), JapanConstructionYardCommandSet, SovietConstructionYardCommandSet, SovietCraneCommandSet (new).
- Ids exist in LogicCommand (CONSTRUCTION_YARD_CONSTRUCT); text insert, old order kept, asset namespace.

## Values
HP 2000/2000; cost 2000; Allied/Japan BuildTime 28 / Soviet 0 + unpack 28s; power -75; MaxSimultaneousOfType 1; prereqs Allied/Soviet/Japan TechStructure; aura and modifier unchanged from 78.

## STATIC DEFECT (FAIL)
**GameObject element order.** AssetTypeGameObject.xsd defines GameObject as an `xs:sequence` (L383+): DisplayName, DisplayNameTransformed, **GameDependency, ObjectResourceInfo**, ArmorSet, … The SDK AlliedTechStructure follows this order.
- All 3 new files have `<ObjectResourceInfo>` **before** `<GameDependency>` (Allied L30-35 order: DisplayName → ObjectResourceInfo → GameDependency). This is a schema sequence violation that the asset builder may reject.
- **Minimal fix:** in each of the 3 centers, move the `<GameDependency>…</GameDependency>` block above `<ObjectResourceInfo>`. No other change.

## Runtime only (source mechanism otherwise acceptable)
- 200% = half time and its effect on in-progress items;
- refresh vs multiply; stacking via capture;
- Range 99999 map coverage;
- lapse ≤2s on death / sell / capture;
- the Soviet aura during unpack;
- no build-up / unpack animation (visual);
- missing strings (cosmetic);
- the model W3X loading in skirmish.

Clone research is deferred until source passes.
