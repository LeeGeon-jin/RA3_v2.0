# BATCH58 AUDIT — SOURCE PASS (native-compile candidate)
**No full XSD, compile or in-game test.** I don't claim it runs correctly, and a missing resource is not guaranteed to be cosmetic only. Phase 1 not complete.

## Package
- 282399 B, sha256 ace5f484…7e91e3c match. All entries under `data/`. 110 XML parse; Mod 109 all + 3 ref.
- vs 57:
  - +5 files: SovietPowerPlant, SovietBarracks, SovietWarFactory, SovietNavalYard, SovietAirfield.
  - SovietRefinery changed.
  - Mod +5 `type="all"` lines (L109-113), nothing else.
  - The other 103 files are byte-identical, including LogicCommand and LogicCommandSet: no new commands.

## Diff of all six files vs SDK / package
| File | Lines (pkg/SDK) | Only change | Define use |
|---|---|---|---|
| SovietPowerPlant | 540/540 | L40 10s→8s | only L483 StructureUnpackUpdate |
| SovietBarracks | 529/529 | L28 10s→8s | only L461 |
| SovietWarFactory | 716/716 | L82 20s→18s | only L604 |
| SovietNavalYard | 669/669 | L58 20s→18s | only L560 |
| SovietAirfield | 1298/1298 | L64 30s→15s | only L1201 |
| SovietRefinery vs 57 | — | L13 20s→18s | only L683 |

- **The five new files are full SDK copies:**
  - same ids, every ART/DATA include, xi, Draw/bones (unpack states `MATCH_UNPACKING` scale with the time), behaviors, geometry, AI, health/armor, prerequisites;
  - BuildTime 0.0 kept;
  - trailing bytes identical;
  - not thin patches.
- **Refinery:**
  - the spy STEAL_MONEY 2000 InfiltratorContain is unchanged;
  - SpawnBehavior unchanged (SpawnOnUnpack, no invented delay);
  - free miner untouched.
- Campaign copies are untouched. No neutral "no animation" rule was applied.
