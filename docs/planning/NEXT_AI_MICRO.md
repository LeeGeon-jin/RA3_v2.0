# NEXT_AI_MICRO — Slow AI micro without slowing production / build / strategy (read-only research)
2026-11-08 21:24 (UTC+10). No source, PC or compile actions. Refs: refs_ai_micro.tar.gz (23390 B, sha256 6a4917d9b9727bb36848e5c28a49de2af1a1dc5678a050953f21e3dcea209d1c), full SDK files + schemas.

## 1. What devdoc already approved (第一批, 3.3 table, L117-120 + batch table L1578)
- Item "放慢 AI 决策与微操节奏 / 一次做一件事，减少神微操", rated 中等.
- Approved direction text: "可把凶残难度的微操管理器换成更慢的 UpdateTime、关闭 DodgeThreats".
- **No concrete numbers** given (no target seconds). So the seconds must be proposed; user decision needed only on the number (see 5).
- Separate items (NOT micro):
  - 决策 (macro) cited fields AIData TeamSeconds=10, StructureSeconds, RebuildDelaySeconds=30, BasePersonality EnemyResortingTime=15s, SecondsTillTargetsExpire=5 — also no numbers.
  - "一次只打一波" = remove harassment StrategicStates (ACVHarrassment, FighterAircraftFlankAttack, AlliedScout…) keep one main attack — no concrete list approved beyond examples.
- Cancelled (11-02): 克制权重 / 固定建造配方 — do NOT touch UnitBuilder*/SkirmishAIInformation/OpeningMoves recipe.
- User 21:23 (pt383u): "ai微操间隔调慢几秒不就行了" → consistent with the micro UpdateTime route; parent promised micro-only fields.

## 2. Macro vs micro — which field does what (SDK evidence)
| Layer | Field | File | Original | Unit | Affects |
|---|---|---|---|---|---|
| Micro (per team's units) | AIMicroManagerData `UpdateTime` | SkirmishAI/AIMicroManagerLibrary.xml | Base 0.5s | Time (xsd `type="Time"`, schema default 1s) | how often a team's micromanager re-evaluates targets/dodge/specials/pullback |
| Micro | `DodgeThreats` / `DodgeThreatsReactionTimeMin/Max` | same | true / 0.5s / 0.5s | bool / Time | dodging incoming fire (the "神微操") |
| Micro | `UseSpecialPowers`, `SpecialPowerDelayMinimum/Maximum` | same | true / unset (schema 0s) | Time | delay before AI unit uses abilities |
| Micro | `TimeToKeepTargetMin/Max` | same | unset (0s) on HARD | Time | target switching (focus-fire jumps) |
| Macro | AIData `TeamSeconds`, `StructureSeconds` | SkirmishAI/AIData.xml (global.xml stream) | 10 / 0.0 | seconds (SageReal; comment "every N seconds") | production/build rhythm — **do not touch** for this task |
| Macro | `RebuildDelaySeconds` | AIData | 30 | s | rebuilding — don't touch |
| Macro | `EnemyResortingTime`, `SecondsTillTargetsExpire` | BasePersonality | 15s / 5 | Time / s | strategic target choice — don't touch |
| Frames/ints (avoid) | `GuardChaseUnitFrames` 15000, `GuardEnemyScanRate` 500 / `ReturnScanRate` 1000 | AIData | — | frames / SageUnsignedInt (unit unclear) | guard behaviour; unit not seconds → no guesses |

## 3. How difficulty maps to micromanagers (evidence)
- Personalities pick StrategicStates by Difficulty, e.g. AlliedBalanced L57/62/67: `BalancedAttackGround` = HARD BRUTAL, `_MEDIUM` = MEDIUM, `_EASY` = EASY.
- States' TeamTemplates name a MicroManager (BalancedStates: StandardMicroManager / DefenseMicroManager …). HARD/BRUTAL states use the unsuffixed managers.
- Inheritance (120 AIMicroManagerData resolved):
  - ~95 inherit `UpdateTime` 0.5s from **BaseMicroManager**: Standard, Defense, Expansion, Fearless, Harrassment, Fighter/Bomber/Kirov/Twinblade, Commando/Tanya, Capture*, **HarvesterMicroManager**, and ~40 campaign A/S/J managers.
  - Own override (unaffected by Base change): Scout / BurstDroneHarassment / StealthDetector / Vindicator / FearlessVindicator 0.25s; campaign S01/S02 0.1–0.2s; all `_MEDIUM` 2.0s (Fighter_MEDIUM 3.0s, Vindicator_MEDIUM 1.0s); all `_EASY` 3.0s (Vindicator_EASY 2.0s, S03 2.5s).
- Official SDK precedent range: 0.1s–3.0s. MEDIUM = 2.0s, dodge reaction 6–14s, special delay 2–8s. EASY = 3.0s, DodgeThreats false, UseSpecialPowers false.
- **Shared by unit category:** one manager serves all unit types in a team (infantry/vehicle/air mixed). There is no separate per-category interval except dedicated ones (Vindicator, Kirov, Twinblade, Harvester…).

## 4. Minimal implementable candidates (micro only)
**Candidate A (minimal, 1 attribute):** override `BaseMicroManager UpdateTime 0.5s → 2.0s`, i.e. the official MEDIUM value.
- Effect: all unsuffixed (HARD/BRUTAL) managers and inherited campaign managers.
- Risks:
  - affects campaign AI too (≈40 A/S/J managers inherit Base);
  - affects HarvesterMicroManager (harvest re-orders). That is micro, not production, but it could slightly slow economy reaction — test.
- Doesn't touch the 0.25s explicit ones.

**Candidate B (A + reaction, still micro):** in BaseMicroManager also set `DodgeThreatsReactionTimeMin/Max 0.5s → 6s/14s` (MEDIUM precedent), and `SpecialPowerDelayMinimum/Maximum` unset → 2s/8s.
- Because the Base sets dodge 0.5s, unsuffixed inheritors pick it up. `_EASY` keeps its own values.

**Candidate C (scope-tight, skirmish-only):** leave Base; override only the unsuffixed skirmish-used managers (Standard, Defense, Expansion, Fearless, FearlessDefense, Harrassment, ReactiveDefense, EmergencyDefense, GrowingAttacks, Focused, FirstAssault, SpecialForces, HeavyArmor, ShockSpecialist, AirMarshall, FleetCommand, AmbushDivision, Capture*, Fighter/Bomber/Kirov/Twinblade/Vindicator/Scout…) with UpdateTime 2.0s.
- Campaign untouched, but many more edits.
- Optional add-on to any candidate: DodgeThreats="false" (= EASY behaviour; matches devdoc wording "关闭 DodgeThreats", but is stronger than just slowing down).

Not recommended: AIData TeamSeconds / StructureSeconds / RebuildDelay, EnemyResortingTime, personality StrategicState lists (that's the separate "一波" item), UnitBuilder (cancelled).

## 5. Decisions the parent should ask the user (no devdoc numbers exist)
1. Interval: 2.0s (= official MEDIUM, conservative) / 3.0s (= EASY) / other? The SDK range is 0.1–3.0s; going above 3s has no SDK precedent → test.
2. Also slow dodge (6–14s) and skill delay (2–8s)? Or turn dodging fully off (devdoc wording)?
3. Include campaign AI (Candidate A/B) or skirmish only (C)?

## 6. Loading / runtime evidence
- AIMicroManagerLibrary is included via SkirmishAIIncludes.xml (L22), which global.xml L75 loads. The Batch85 Mod.xml already overrides a SkirmishAI file the same way (L52 `DATA:SkirmishAI/Personalities/CoopBasePersonality.xml` type all). That route is unproven at runtime (same caveat as 71/72/83/85 global-stream overrides).
- Need a native compile plus a test: BRUTAL AI vs player, observe dodging/ability spam; compare production timing unchanged.
- The xai partial override of a single AIMicroManagerData by id (full copy of file vs one element) follows the package convention: full-copy file with one attribute changed.
