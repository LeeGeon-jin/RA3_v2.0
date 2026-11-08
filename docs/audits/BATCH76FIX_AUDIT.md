# BATCH76FIX AUDIT — SOURCE PASS (no full XSD / compile / in-game test; not Phase1 complete)

## Package
- 300017 B; sha256 2888ec84…8d45d26 match.
- All entries under data/. 121 XML parse. Mod: 3 reference / 119 all.
- vs 76: only Soviet/Units/SovietCommandoTech1.xml differs. The other 120 XML are byte-identical, so Weapon.xml (bombing 300 ground/water + Structure 450 ANTI_STRUCTURE), rifle, Pilot Snipe 500 / timing 1s and vision 325 are untouched.

## Changes (the element tree of old vs new is compared, namespace + all attributes + text)
- **Additions only**, 9 elements; every old element, attribute and text is preserved in its original order.
- The 31 reformatted line pairs are whitespace-only:
  - `diff -w` shows nothing besides the additions;
  - the element-level diff shows no '-' items, so no merged attribute tokens.
1. Default ModelConditionState: TERTIARY_WEAPON SlotID 1 `WeaponFireFXBone` + `WeaponLaunchBone` → FX_Laser, directly after the SECONDARY pair (same element types/order).
2. AnimationState `FIRING_OR_PREATTACK_C OVER_WATER` placed right after the B over-water state. It is an exact mirror: Flags RESTART_ANIM_WHEN_COMPLETE, StateName STATE_OverWater, SUCommando_WPNTA ONCE blend 7, ParticleSysBone SmallShipWakeIdle + AUScoutInfantrySplash (None / FollowBone false).
3. AnimationState `FIRING_OR_PREATTACK_C` right after the B land state: SUCommando_PNTA ONCE blend 7, same flags.
4. `ModelConditionSound SOV_Commando_PaintMS RequiredFlags FIRING_C ExcludedFlags DYING` after the B sound.

## Structure / conditions
- The new elements sit inside the same parents and next to the same sibling types as the B versions, so sequence validity matches the existing B elements.
- The over-water C state precedes the land C state, the same relative order as B, so water selection precedence is mirrored.
- No claim that A/B/C firing are mutually exclusive at runtime; that is not provable from XML.
- **Duplicate StateName `STATE_OverWater`** now exists on the B and C states. This is a static note; its effect on transitions is a native test item.

## Still native-test only
- the FX_Laser bone and laser origin for TERTIARY;
- animation and sound playback on C;
- automatic weapon choice 300 vs 450 and ANTI_GROUND not hitting structures;
- the vision 325 < 450 acquisition;
- resource/asset loading.

The cloud's claims "no resource risk / runtime proven" are not accepted.

## Next
NEXT_R77.md + r77_sdk_refs.tar.gz stand. Nothing new found, so no further research.
