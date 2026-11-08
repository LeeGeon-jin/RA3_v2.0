# BATCH88 AUDIT — FAIL (one omission)

## Package
- 347156 B, sha256 fbd77a82d5e4a13870afb9cb6c47582f54fe2c7d025acbd4333a3d89ff753d14.
- 139 XML. Mod.xml: 136 all + 3 reference, as expected.
- vs Batch87:
  - Mod.xml has +1 line at L53: `<Include type="all" source="DATA:SkirmishAI/AIMicroManagerLibrary.xml" />`, the same route as the existing CoopBasePersonality override at L52;
  - plus the new SkirmishAI/AIMicroManagerLibrary.xml.
  - The other 137 XML are byte-identical.

## AIMicroManagerLibrary vs SDK
- Same 119 AIMicroManagerData, in the same order. The root is equal.
- **Apart from UpdateTime, there are zero differences:** all other attributes and all children (whitespace-normalised) are identical. That includes DodgeThreats, reaction times, UseSpecialPowers, SpecialPowerDelay, targets and retreat.
- No AIData, personality, state or economy file was touched.
- **Explicit UpdateTime:** 26 in the SDK, 26 in the mod. Each explicit value is +2s.
- **Effective UpdateTime**, resolved through the inheritFrom chain:

| Original → current | Count |
|---|---|
| 0.5 → 2.5 | 82 |
| 2.0 → 4.0 | 12 |
| 3.0 → 5.0 | 12 |
| 0.25 → 2.25 | 5 |
| 0.2 → 2.2 | 4 |
| 1.0 → 3.0 | 1 |
| 0.1 → 2.1 | 1 |
| 2.5 → 4.5 | 1 |

- **No double add:** inherited managers receive +2 only through their parent.
- Coverage: every difficulty (_EASY / _MEDIUM / unsuffixed) and every campaign A/S/J/KLF manager. These are all defined in this one library; no other AIMicroManagerData exists anywhere in the SDK XML.

## FAIL
- **What's wrong:** `ScoutInfantryMicroManager` has no inheritFrom and no UpdateTime, so it uses the schema default `UpdateTime` 1s (AssetTypeAIMicroManager.xsd L33). It is unchanged in the mod: still 1s.
- **It is actually used:** SkirmishAI/States/SovietAirMarshallStates.xml L18 and States/AIStateLibrary.xml L960.
- **Minimal fix:** add `UpdateTime="3s"` to ScoutInfantryMicroManager. Not applied.

## Runtime (unproven)
- Whether the global-stream override takes effect is unproven.
- The in-game effect is unproven.
- Production and build timing are unaffected by static evidence only (no macro fields changed).
