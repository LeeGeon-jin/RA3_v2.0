# PHASE1_REMAINING_R82 (rev 2) — against the Batch81 package (read-only)
Static only. Not a coverage proof, not compiled or tested, and not Phase 1 complete.

## Scope (per the parent's check of the original session)
- The user said "开工第一阶段". The scope given explicitly includes 工程师即时占领 / 碾压不停顿 / 最低画质.
- The first cloud task: 第一批 numbers and mechanisms (≈82 items). Items spanning batches 1/2 → only the explicit 第一批 numbers. New units, complex model / weapon additions and campaign scripts come later.
- Mirage move-fire is 第二批 → parked.

## Corrections to my earlier reports
1. **R82 v1:** "Phase 1 = 第一批 + 第二批" — withdrawn (that was a guess).
2. **R82 v1:** "vehicle bombing 300 = user decision / open conflict" — withdrawn. It was the parent's technical limit; user 17:46 confirmed only the structure 1.5×; L737 rifle stands.
3. **R82 v1:** internal batch / R numbers equated with user batches — withdrawn.
4. **R82 v1:** default lowest quality / classic mouse "not implemented":
   - classic mouse = **B72** (source candidate);
   - music 0% = **B71**;
   - lowest quality has **no** batch (B71 / B72 were music / mouse only).
5. **R82 v2:** proposed asking whether the "test-first" call still holds — withdrawn. R65 "test-first" was an internal technical note, not a user revocation; it creates no user blocker.
6. **R81 note:** "Tanya C4 uses NONE" — wrong, it uses `Rule="ANY"` (see BATCH81_AUDIT).
7. **R49:** front / back armor "dropped (L29)" — wrong. L29 is about campaign building copies; armor done in **B69**.

## Three real 第一批 gaps (no implementing field in the package, no batch)
| Gap | Package evidence | Next |
|---|---|---|
| **Crush without stopping** (L206-212) | 13 package files 80% + 1 at 50% (same as SDK); BaseVehicle / BaseEgg / JapanAVVT1 / SovietAVVT1 / SovietAVVT2 absent; CrushKillDelay 1.5s only in SDK BaseVehicle L41 | **NEXT_R83 §A — recommended next source batch** (19 files, value-only) |
| **Instant capture** CaptureWaitTime (L185-186) | no System/ folder in the package | NEXT_R83 §B — single-file candidate, **global-stream route unproven** (global.xml L50; FAQ #36 MapMetaData note); after A |
| **Default lowest quality** (L194-199, L1570) | no GameLOD / GraphicsHardware in the package | NEXT_R83 §C — global stream + Options.ini first-run detection only; not pushed |

## Rest of 第一批 — source candidates, blocked only by native compile / test (PC access forbidden)
- ore / miner;
- base build times, super reactor 24 / airfield 15, Battle Lab 2000/30, tech 1000/15 (academy 1500);
- MCV 3000/30 / speed 60;
- permits kept / not unlocking + RequiredObject prereqs;
- KillPassengersOnDeath (aircraft "需实测");
- Premature discharge removed (**B60**);
- coastal gun homing;
- AI ResourceMultiplierCheat 100%;
- front / back armor (**B69**);
- music 0% (**B71**);
- classic mouse (**B72**);
- Japan PP turbine 300/10 (**B28/29**);
- Kirov 2000/20 (**B16_FIX**);
- other timing batches 59-72 (per R72 / R73 lists).
- **Caveat:** these come from earlier PASS audits; this round re-checked only the fields named above.

## Not in this phase (do not start)
- 第二批 items such as mirage move-fire (NEXT_R82, parked), advanced mirage, Tesla tank unlock, precision bomber, Badger, Soviet spy, paratroopers, Kirov boost.
- 第三批, 末阶段 / Uprising.
