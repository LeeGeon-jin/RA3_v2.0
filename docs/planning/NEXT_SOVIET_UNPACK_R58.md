# Next (R58): Soviet base-building unpack times — decided, not implemented (minimal batch)
Refs: `soviet_unpack_sdk_refs.tar.gz` (8 files: 6 SDK structures + Soviet.xml + StructureUnpackUpdate.xsd).

## Requirement (latest, 2026-11-06)
- **L218 (user):** "三军普通发电厂建造时间改为8秒…兵营改为8秒…矿场改为18秒…战车工厂改为18秒…船厂改为18秒…苏联超级反应堆改为24秒、机场改为15秒、作战实验室改为2000块、30秒" (also L30 revision note, 11-06).
- **L221 (plan):** Soviet structures have BuildTime 0.0; the unpack time *is* the build time. PP 10→8, barracks 10→8, refinery 20→18, WF 20→18, naval 20→18, super reactor 30→24, airfield 30→15, Battle Lab 3000→2000 / 60→30.
- **L218 also:** campaign overrides building copies "这个不改了"; the Soviet crane/repair bay "不做". Both excluded.

## Already in package b92 (no repeat)
| Item | Value in b92 |
|---|---|
| Allied PP / barracks | BuildTime 8 |
| Allied refinery / WF / naval yard | BuildTime 18 |
| Japan PP unpack | 8 s |
| Japan refinery unpack | 18 s |
| Soviet super reactor unpack | 24 s |
| Soviet Battle Lab | 30 s / 2000 |

## Missing (real files)
| Object | Current | Line | Target |
|---|---|---|---|
| SovietPowerPlant.xml (not in package) | `SOVIET_POWERPLANT_LOCAL_UNPACK_TIME` 10s | SDK L40 | **8s** |
| SovietBarracks.xml (not in package) | `SOVIET_BARRACKS_LOCAL_UNPACK_TIME` 10s | L28 | **8s** |
| **SovietRefinery.xml (already in package for spy STEAL_MONEY)** | `SOVIET_REFINERY_LOCAL_UNPACK_TIME` still **20s** | package L13 | **18s** |
| SovietWarFactory.xml (not in package) | 20s | L82 | **18s** |
| SovietNavalYard.xml (not in package) | 20s | L58 | **18s** |
| SovietAirfield.xml (not in package) | 30s | L64 | **15s** |

- Each Define is used only by its own `StructureUnpackUpdate UnpackTime="=$…"`.
- Unpack animations use `AnimationMode="MATCH_UNPACKING"`, so they scale with the time.
- Refinery: the comment "keep initialdelay = UnpackTime+0.5s" is stale. The SpawnBehavior uses `SpawnOnUnpack="true"` and has no InitialDelay attribute, so there is nothing else to change.
- CampaignOverrides.xml has no entries for these 5 objects.

## Minimal Batch 58
- **Five new full SDK copies** at the same paths `data/Soviet/Structures/Soviet{PowerPlant,Barracks,WarFactory,NavalYard,Airfield}.xml`:
  - edit only the one Define value each;
  - keep the ART includes as-is (Batch57 / Batch49 convention).
- Mod `type="all"` +5.
- **SovietRefinery.xml:** one-line text edit of the package file, L13 `20s` → `18s`. No other change.
- **Expected checks:**
  - `diff -w` vs SDK = 1 line per new file;
  - refinery vs b92 = 1 line;
  - Mod +5; commands unchanged; 110 XML.
- **Test natively:** build timings, miner spawn on unpack, airfield aircraft slots.

## AA follow-up check (doc only)
- No further decision exists in devdoc: only L821 and L825 mention it (searched "鱼叉"/"发射点"/later 天启 lines).
- Harpoon mode, aim/turret and launch bone remain **user decisions**. NEXT_APOC_AA_R58.md stays pending.
- Move-and-fire is already true for the cannon; that is not proof for the harpoon.
