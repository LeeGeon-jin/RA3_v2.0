# BATCH88FIX AUDIT — PASS (static; not compiled, not tested in game)

## Package
- File: batch88fix.tar.gz, 347161 B, sha256 97f8f19bfc88a4bb17f102c2fc4c44f7d6a069343e8a8a6c21b47beabf74fe08 (matches).
- 139 XML, 0 non-XML files (no backups).
- Mod.xml: 136 all + 3 reference.

## Diff vs Batch88
- Only change: SkirmishAI/AIMicroManagerLibrary.xml line 458, `UpdateTime="3.0s"` added to ScoutInfantryMicroManager.
- The other 138 XML are byte-identical to Batch88.

## Effective UpdateTime, recomputed for all 119 managers
Each value is resolved through its inheritFrom chain, falling back to the schema default of 1s.

| SDK → mod (seconds) | Count |
|---|---|
| 0.5 → 2.5 | 82 |
| 2.0 → 4.0 | 12 |
| 3.0 → 5.0 | 12 |
| 0.25 → 2.25 | 5 |
| 0.2 → 2.2 | 4 |
| 1.0 → 3.0 | 2 |
| 0.1 → 2.1 | 1 |
| 2.5 → 4.5 | 1 |

- Every manager is exactly +2s: 0 deviations, no double additions.
- The two 1.0s managers:
  - VindicatorMicroManager_MEDIUM has an explicit 1.0s.
  - ScoutInfantryMicroManager uses the schema default 1s. It is the only manager that falls back to the schema default, so a claim of "2 schema-default managers" would be wrong.
- Explicit UpdateTime count: 27 (26 from before + ScoutInfantry).

## Unchanged
Batch88 already showed that, apart from UpdateTime, every attribute and child is identical to the SDK. Since this fix changes only the one line above, that still holds.

## Unproven at runtime
- Whether the global-stream load picks up the override.
- The actual in-game effect.
