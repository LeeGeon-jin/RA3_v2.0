# BATCH76 AUDIT — SOURCE CANDIDATE PASS (logic) with a PRESENTATION DEFECT to fix
No full XSD, compile or in-game test. Phase 1 not complete.

## Package
- 299819 B, sha256 a08b6ab4…339f2a2e4 match. All entries under `data/`. 121 XML parse.
- Mod: 3 reference / 119 all.
- vs 75: only Weapon.xml and SovietCommandoTech1.xml differ; the other 119 XML are byte-identical.

## Diff
- **Weapon.xml:**
  - L813 the original SovietCommandoCallBombingRun mask `ANTI_WATER ANTI_GROUND ANTI_STRUCTURE` → `ANTI_WATER ANTI_GROUND`;
  - new L854-858 `SovietCommandoCallBombingRunStructure` inheritFrom it, `AttackRange="450.0"`, `RequiredAntiMask="ANTI_STRUCTURE"`.
  - Range 300, MinimumAttackRange 50, delays 0.5/1.0, AI hint and all nuggets (laser / SpecialPowerNugget SpecialPowerBombingRun with filter VEHICLE STRUCTURE VALID_TARGET_FOR_C4 / tint / inform) are unchanged and inherited by the new template.
- **SovietCommandoTech1.xml:**
  - WeaponSlotHardpoint ID 1 re-indented (whitespace only) + new `<Weapon Ordering="TERTIARY_WEAPON" Template="SovietCommandoCallBombingRunStructure" />`;
  - sniper rifle PRIMARY, bombing SECONDARY, Pilot Snipe (StartAbilityRange 500), VisionRange 325, CommandSet unchanged.
  - Natasha has a single WeaponSetUpdate / slot (no water/state-specific slots), so all states are covered.

## Mask semantics (static evidence only)
- **Schema:** WpnAntiT lists ANTI_GROUND and ANTI_STRUCTURE as **separate** enum values (AssetTypeWeaponTemplate.xsd L112-130); default mask = "ANTI_GROUND ANTI_WATER ANTI_STRUCTURE". This implies structure is not implied by ground.
- **SDK usage:**
  - weapons meant for infantry/units only use ANTI_GROUND ANTI_WATER without ANTI_STRUCTURE (SovietCommandoSniperRifle, AlliedCommandoDesertEagles, AAGA_PistolWeapon, Scout maul, ShrinkRay…);
  - Tanya's C4 AttachWeapon adds ANTI_STRUCTURE explicitly;
  - "…ForBridges" weapons exist solely to add ANTI_STRUCTURE.
  - This is consistent with ANTI_GROUND **not** covering structures. Not a runtime proof.
- **Inheritance:** a child attribute replaces the parent's (the same as ForBridges, e.g. JapanNavalScoutShipMiniTorpedoLauncherForBridges overriding RequiredAntiMask). No merge semantics for attributes.
- No static contradiction:
  - the 450 weapon cannot pick vehicles (mask ANTI_STRUCTURE only; vehicles are ground/water);
  - the 300 weapon no longer lists structures.

## Command / AI
- The CommandSet has no weapon-slot-specific command (only Pilot Snipe, MoveToPositionAndCollect, AttackMove). There is nothing restricting bombing to SECONDARY.
- WeaponAiHintInfo is per weapon (inherited). Slot defaults AutoChooseWeapon true / PREFER_MOST_DAMAGE.

## Presentation defect (static, real)
Draw bones and animation/sound are keyed to SECONDARY only:
- ScriptedModelDraw default state L83-89 `WeaponFireFXBone` / `WeaponLaunchBone` WeaponSlotType SECONDARY_WEAPON → FX_Laser (none for TERTIARY);
- AnimationStates L548 `FIRING_OR_PREATTACK_B OVER_WATER` and L654 `FIRING_OR_PREATTACK_B`;
- the paint sound L1160 `RequiredFlags="FIRING_B"`.

Because **all structure bombing now goes through TERTIARY** (the C conditions), structure targets would likely lose the laser origin bone, the aiming animation and the paint sound. Bombing logic is unaffected.

**Minimal fix (same file only):**
1. Add `WeaponFireFXBone` + `WeaponLaunchBone` with `WeaponSlotID="1" WeaponSlotType="TERTIARY_WEAPON" BoneName="FX_Laser"` beside L83-89.
2. Add AnimationStates duplicating L548 / L654 with `FIRING_OR_PREATTACK_C` (same animation as the B states).
3. Add a ModelConditionSound with `RequiredFlags="FIRING_C"` like L1160.

Native test after the fix:
- TERTIARY selection at 300–450;
- ANTI_GROUND not hitting structures;
- vision 325 vs 450.
