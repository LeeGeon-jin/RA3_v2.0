# BATCH87 AUDIT — PASS (static; runtime unproven)

## Package
- 342991 B, sha256 7d2dd042f7fd3ddb6d06ba86871a483e1572bcad5e37517080f2df38dae89c5a. 138 XML.
- vs Batch86: only the 3 refineries differ, by exactly 1 line each: Amount 2000 → 5000. The other 135 XML are byte-identical.

## Refineries vs SDK
- **Allied refinery:** BuildTime 20 → 18.
- **Soviet refinery:** unpack Define 20s → 18s.
- **Japan refinery:** UnpackTime 20s → 18s.
- **Infiltration module, all three:**
  - The SDK `xi:include InfiltratorContainEconomic.xml` (STEAL_MONEY, Amount 2000, **BlockedDuration 30s**) is replaced by a single inline module with the same id: STEAL_MONEY, **Amount 5000**, **BlockedDuration 0s**.
  - There are no duplicate ids and no other changes.

## Blocking chain
- **SDK evidence:**
  - Schema Modules/InfiltratorContain.xsd: `BlockedDuration` is a Time, default 2s.
  - SDK original value: 30s.
  - devdoc L518: "BlockedDuration 改 0s 即『立马进下一个』".
  - The 0s value has been in place since Batch3 (BATCH3_REFINED/BATCH12 audits). Batch87 only changes the amount.
- **Other gates:** `InfiltratedStatusFilter` (default DESTROYED UNDER_CONSTRUCTION SOLD UNPACKING) is a state filter, not a cooldown. No other cooldown attribute is set.
- **Not static-provable:** whether the engine adds any hidden cooldown, so a second spy entering immediately is runtime-unproven. Fixed amount 5000 applies (the "half the money" idea isn't implemented).
- **Correction:** my progress doc wrongly said "2000, same as SDK, only the form changed". In fact BlockedDuration was 30s → 0s.
