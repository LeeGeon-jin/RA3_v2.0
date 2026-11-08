# BATCH78 AUDIT — FAIL (static defects; FIX required). No full XSD / compile / in-game test; not Phase1 complete.

## Package
- 302189 B, sha256 5258ef36…3b2a8c match. All entries under data/. 124 XML parse. Mod: 3 reference / 122 all.
- vs 77: 3 new objects (143/146/143 lines) + AttributeModifier / LogicCommand / LogicCommandSet / Mod changed; the other 117 XML are byte-identical.
- No cloudstore BATCH78_REPORT was found; the audit is based on the tar only.
- **AttributeModifier:** `AttributeModifier_QuickProduction` Category NONE (valid enum), Duration 1.0s, PRODUCTION 200%. Valid.
- **LogicCommand:** 3 × CONSTRUCTION_YARD_CONSTRUCT → correct ids. Valid.
- **CommandSet:** +1 Cmd each in AlliedConstructionYardCommandSetBase, JapanConstructionYardCommandSet and SovietConstructionYardCommandSet.
- **Mod:** +3 all includes.

## Objects
- Full copy of SDK AM_AlliedFutureTechHQ (119 lines).
  - `diff` against the SDK shows nothing removed except one comment: model / Draw / 20 contact bones / BuildingDestruction / FX / collapse OCL / DestroyDie / armor / geometry / audio / ART + collapse + debris includes all kept.
  - Changes: id/side/strings, cost/time/power/limit/queue, prereq, aura, HP 2000/2000.
- Soviet: BuildTime 0.0 + StructureUnpackUpdate. Japan: BuildTime 28, direct placement (matches the decision).
- Prereqs AlliedTechStructure / SovietTechStructure / JapanTechStructure correct.

## STATIC DEFECTS (must fix)
1. **`BuildCost="2000"` is not a GameObject attribute.** In the schema, BuildCost is an element in ObjectResourceInfo (AssetTypeGameObject.xsd L379); the package precedent (Guard02 L20-22) uses `<ObjectResourceInfo><BuildCost Account="=$ACCOUNT_ORE" Amount="2000"/></ObjectResourceInfo>`. As written, the cost is invalid/ignored. All 3 files.
2. **`StartsActive="true"` on AttributeModifierAuraUpdate is not in its schema.** It exists only on AutoAbilityBehavior and CostModifierUpgrade; the aura schema and UpgradeModuleData lack it. Remove it (InitiallyActive="true" is the valid switch). All 3 files.
3. **Soviet `UnpackTime="28"` violates the Time type** (Base.xsd L131 requires an `s`/`ms` suffix) → must be `28s`.
4. **No `BuildPlacementTypeFlag`** (default INVALID, AssetTypeGameObject.xsd L504), while ProductionQueueType is OTHER_STRUCTURE. Previous buildables set both (Guard02 L19 OTHER_STRUCTURE; the tech structures use MAIN_STRUCTURE for both). Add the flag matching the queue. All 3 files.
5. **Wrong parent for a faction building: BaseCivilianStructureNoGarrisonDestructible.** Its KindOf fully replaces the base list: CIVILIAN_BUILDING, NOT_AUTOACQUIRABLE, ALWAYS_VISIBLE_IN_RADAR, no CAPTURABLE. Its chain (BaseCivilianStructureNoGarrison → BaseObject) has none of the BaseStructure modules: **no StructureSellUpdate** (BaseStructure.xml L40), no construction / sell audio, no catalyst etc.
   - The user requirement that the effect ends on **sell** therefore has no sell path. Engineer capture / repair on a civilian-classified object is also unestablished.
   - Minimal fix: inherit like the tech structures:
     - Allied/Japan `BaseStructure` (AlliedTechStructure L19, JapanTechStructure L33);
     - Soviet `BaseSovietStructure` (SovietTechStructure L35; adds +ACTIVATE_AFTER_UNPACK).
   - Change the base include, keep the copied Draw/geometry/death/collapse modules, and drop the civilian KindOf baggage.
6. **Soviet aura can run during the 28s unpack.** The object lacks ACTIVATE_AFTER_UNPACK (which BaseSovietStructure provides; all Japan/Soviet unpacking buildings carry it). Fix 5 covers this. Whether ACTIVATE_AFTER_UNPACK actually gates the aura is runtime-unproven.

## Recommended consistency (not strictly required)
- The previous buildables were also added to AlliedCraneCommandSet / SovietCraneCommandSet (5 lists); this batch has only 3 CY sets. Add both crane sets for consistency.
- Strings Name / Type / Desc:QuickProductionCenter do not exist in SDK strings → missing-string text (cosmetic).

## Aura (static review)
- Schema-valid: InitiallyActive, Range SageReal 99999, RefreshDelay 0.5s, AttributeModifierName.
- ObjectFilter `Rule="ANY" Relationship="SAME_PLAYER" Include="FS_FACTORY" Exclude="CONSTRUCTION_YARD"`: all enums are valid. Rule must be ANY (default NONE).
- **Coverage, checked per SDK file:**
  - FS_FACTORY: Allied/Soviet/Japan Barracks, WarFactory, NavalYard; Allied/Soviet Airfield.
  - Excluded via CONSTRUCTION_YARD: all CYs + AlliedCrane / SovietCrane, so structures and Japan cores are not sped up.
  - Also matched: MCVs and SovietSurveyor (VEHICLE FS_FACTORY), harmless (no unit queue).
  - The center itself is not FS_FACTORY, so there is no self-effect.
  - Package full copies of the Soviet factories keep their KindOf.
- **Not proven:**
  - 200% = half time, and whether it applies to in-progress items;
  - re-applying the same modifier refreshes rather than multiplies (no SDK statement);
  - two centers via capture stacking;
  - interaction with cryo / garrison categories;
  - Range 99999 covering every map (not infinite);
  - lapse time after death / sell / capture — "≤1.5s" is theory only (RunWhileDead unset; owner change on capture is engine-side);
  - low power.
