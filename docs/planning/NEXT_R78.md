# Next (R78): Quick Production Center — decided facts + a technically reliable minimal chain
Refs: `r78_sdk_refs.tar.gz` (20 SDK files: the HQ model object + collapse/debris/base, tech structures, AttributeModifier, aura precedents, PlayerSpellBook/SpecialPowerTemplates, schemas). Batch77 package: no quick production object exists yet (no "FutureTechHQ" in data/).

## Decided (devdoc; latest wins)
| Item | Value | Source |
|---|---|---|
| Effect | "单位生产时间减半"; if destroyed "立马恢复原状"; "类似电量不足的逻辑" | L260 user |
| Lost by | destroyed, sold, captured by enemy engineers → restore immediately (≤2s accepted by user later) | L263 / your brief |
| Sides | all three | L263 |
| Build time | 28s all; Allied BuildTime 28; Soviet unpack 28 (BuildTime 0 pattern); Japan **direct placement** (CONSTRUCTION_YARD_CONSTRUCT, BuildTime 28, no core) | L29, L224, L260, L263 |
| Cost / power | 2000 / -75 (= tech structures -75) | L260, L263 |
| Limit | one per player, no stacking (MaxSimultaneousOfType 1) | L34, L263 |
| Prereq | each side's tech structure: AlliedTechStructure / SovietTechStructure / JapanTechStructure | L218, L263 |
| Model | small HQ AM_AlliedFutureTechHQ (no animation, BOX 30×30×40, collapse + YU_HotelDebris); new id | L36, L263-264 |
| HP | 2000 (your brief: = battle lab; SovietTechStructure MaxHealth 2000 at L435 in SDK refs) | brief |
| Campaign | new id; campaign overrides not synced (global rule L29) | L29, L263 |

## Mechanism research (SDK)
- **A. GiveProductionBonusSpecialPower** (BuildTimeBonus / Allies, PlayerSpellBook, protocol precedent):
  - player-wide but a one-shot permanent grant;
  - no SDK removal path found → cannot satisfy "restore on loss". **Rejected.**
- **B. AttributeModifierAuraUpdate + Modifier Type PRODUCTION (recommended):**
  - The schema (AttributeModifierAuraUpdate.xsd) has AttributeModifierName, RefreshDelay, Range, InitiallyActive (default **false** → must set true), ObjectFilter (Relationship enum ALLIES / ENEMIES / NEUTRAL / **SAME_PLAYER**, Include / Exclude KindOf).
  - PRODUCTION is a valid AttributeModifier type (AssetTypeAttributeModifier.xsd L42).
  - **SDK precedent that a PRODUCTION modifier on a structure changes its production:** BaseStructure.xml L55 applies cryo modifiers AttributeModifer_CryoBeam_02..10 (PRODUCTION 80%…0.01%) to buildings via SecondaryDamageTracker. A >100% value is an inference (test).
  - Expiry precedent: AttributeModifier_Garrisoned Duration 1.0s + aura RefreshDelay 0.5s (BaseCivilianStructure.xml L72-82). On loss (death / sell) refresh stops → the modifier lapses in ~≤1.5s (theory; meets ≤2s if confirmed).
  - On capture, the aura owner changes, so SAME_PLAYER now refers to the captor; the original owner lapses the same way.
- **C. Player upgrade + AttributeModifierUpgrade** (CaptureAndGiveUpgrade precedent): revoking on loss is unproven. Not chosen.

## Minimal chain (technical choices, no user questions)
1. New `GlobalData/AttributeModifier` entry, e.g. `AttributeModifier_QuickProduction`: `Category` like Garrisoned, `Duration="1.0s"`, `<Modifier Type="PRODUCTION" Value="200%"/>`.
   - "Half time" = double rate. That 200% means double the rate is an inference from the cryo direction; test.
2. **New Allied object** (full copy of AM_AlliedFutureTechHQ, new id): Side Allied; BuildCost 2000; BuildTime 28; EnergyProduction -75; MaxHealth 2000 (+ InitialHealth); MaxSimultaneousOfType 1; GameDependency RequiredObject AlliedTechStructure; MAIN/OTHER structure queue/placement as for previous buildables.
   - Add `AttributeModifierAuraUpdate InitiallyActive="true" AttributeModifierName=… RefreshDelay="0.5s" Range=<large, map-wide>` with `ObjectFilter Rule="ANY" Relationship="SAME_PLAYER" Include="FS_FACTORY" Exclude="CONSTRUCTION_YARD"`.
   - FS_FACTORY is verified on barracks / war factory / naval yard / airfield (Allied/Soviet airfield, Japan barracks).
   - CY is excluded because the effect is for units and Japan CY builds structure cores. Japan factories: check each has FS_FACTORY.
3. Soviet and Japan versions: same pattern.
   - Soviet: unpack 28 with BuildTime 0, inheriting the Allied object or a full copy per the package convention.
   - Japan: direct CONSTRUCTION_YARD_CONSTRUCT, BuildTime 28 (doc L1610 test).
4. LogicCommand ×3 + the CY CommandSets; Mod +includes; add the HQ model/collapse/debris asset includes (they are only loaded by WorldBuilder originally, L264 risk).

## Runtime test items (not design)
- PRODUCTION 200% halves time on queued and in-progress items;
- range / map-wide behaviour (Range -1 unproven → use a large number);
- lapse ≤2s on destroy / sell / capture;
- no effect on allies or enemies;
- low power interaction (not required by the user; just observe);
- capture → captor may own 2 (limit);
- the model W3X is complete.

## Clone center (later)
Decided 2500 / 30 / 100 power / battle-lab prereq / VIP bunker model / HP 2000 / "只要是兵就能复制". Mechanism already noted (CaptureAndGiveUpgrade → GiveUpgradeToProduced → ObjectCreationUpgrade). Not researched further this round.
