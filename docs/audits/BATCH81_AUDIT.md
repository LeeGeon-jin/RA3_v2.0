# BATCH81 AUDIT — SOURCE PASS (source candidate)
No full XSD check, no compile, no in-game test. This does not mean Phase 1 is complete.

## Package
- `batch81.tar.gz`: 321313 B, sha256 48b60db2…2a6f (matches).
- 130 XML files; Mod.xml unchanged (128 "all").
- `diff -r` against Batch80 shows **only** `GlobalData/Weapon.xml` changed, as a pure 10-line insertion after L760. The other 129 files are byte-identical.
- All other Weapon.xml content is unchanged.

## The new nugget (inside SovietCommandoSniperRifle, after the LineDamageNugget)
`DamageNugget Damage=999999 Radius=0 DamageType=GRENADE DamageFXType=SOVIET_SNIPERRIFLE DeathType=DETONATED` + `SpecialObjectFilter Rule="NONE" Include="VEHICLE"`

### Filter semantics (checked as evidence, not taken from the report)
- **Schema:** ObjectFilter.xsd L4-9 enum ObjectFilterRule = ALL / ANY / NONE. The xsd has **no documentation text** for what each rule means.
- **Strongest evidence — the same weapon:**
  - its own SDK-original LineDamageNugget uses `Rule="NONE" Include="INFANTRY"`, and this is the shipped sniper behaviour (it kills infantry only);
  - the SDK's commented-out predecessor uses `Rule="ALL" … Exclude="VEHICLE STRUCTURE…"`.
- **Pattern:** "NONE = start from nothing, add Include"; "ALL = everything minus Exclude". The SDK has 21 uses of `Rule="NONE" Include="INFANTRY"` on infantry-only weapons.
- So `NONE + Include=VEHICLE` should be **vehicle only, not an inverted selection**. This is still inference from precedent: the engine source is not available.
- **Correction to my R81 note:** Tanya's C4 (AlliedCommandoDetonationWeapon) uses **`Rule="ANY"`** (Include STRUCTURE VEHICLE VALID_TARGET_FOR_C4, Exclude WALL_PIECE, StatusBitFlagsExclude AIRBORNE_TARGET), **not NONE**. PilotSnipe also uses `Rule="ANY" Relationship=ENEMIES Include=VEHICLE`.
- **SDK precedent for the exact combination `NONE` + `VEHICLE`:** 2 occurrences (`Include="VEHICLE"` after Rule NONE).
- **Verdict:** not a FAIL.
- **Optional, more conservative equivalent (not required):** `Rule="ANY" Include="VEHICLE"`, mirroring PilotSnipe.

### Other fields
- **Enums:** GRENADE (DamageDef.xsd L32), SOVIET_SNIPERRIFLE (DamageFX.xsd L62) and DETONATED (Death.xsd L16) are all valid.
- **SDK combinations:** DETONATED is used 4× in the SDK and SOVIET_SNIPERRIFLE 2× (both on the rifle). GRENADE + DETONATED is the C4 precedent. The FX type SOVIET_SNIPERRIFLE with GRENADE is a new pairing; it is only a visual lookup (runtime only).
- **Radius 0:** direct primary-target damage, like the SDK's commented DamageNugget (Radius 0) and the C4. Splash does not apply.
- **No double hit on infantry:** an infantry target is excluded by the VEHICLE filter. Structures are not VEHICLE, so they are excluded too.
- **Unchanged:** the LineDamage 1000 SNIPER / INFANTRY nugget.

## Unchanged weapon / slot facts
- **Rifle stats:** range 300, ATTACK_NEEDS_LINE_OF_SIGHT, clip 1, PreAttack 0.25 / Firing 1.5 / Reload 0.25, RequiredAntiMask `ANTI_GROUND ANTI_WATER` (no airborne or submerged mask added), RadiusDamageAffects ENEMIES, FireFX unchanged.
- **No WeaponAIHint / TargetFilter** in the weapon or in Natasha's WeaponSetUpdate. Targeting is limited only by the anti-mask, so vehicles can already be targeted.
- **Slot:** Hardpoint ID1 is PRIMARY rifle / SECONDARY CallBombingRun (300) / TERTIARY CallBombingRunStructure (450), all unchanged. WeaponChoiceCriteria default is PREFER_MOST_DAMAGE (WeaponSetUpdate.xsd L49). Which weapon is chosen is **runtime, unproven**.
- **PilotSnipe:** the SovietCommandoPilotSnipeWeapon special ability is unchanged.

## Shared users of the weapon
- `SovietCommandoSniperRifle` is referenced only by Soviet/Units/SovietCommandoTech1.xml.
- AlliedBaseDefense / AlliedAntiAirVehicleTech1 use **separate** templates `ABD_SovietCommandoSniperRifle` / `AAAVT1_SovietCommandoSniperRifle` (they only matched a substring search). Those are unaffected: Natasha inside an IFV or multigunner turret does not get the vehicle kill.
- There is no inheritance of this WeaponTemplate.

## Targets
- **Ships:** VEHICLE (AlliedAntiAirShip VEHICLE SHIP; Soviet ships AMPHIBIOUS VEHICLE; JapanNavyScoutShip VEHICLE SUBMARINE). A sub that is submerged stays untargetable: there is no ANTI_SUBMERGED mask.
- **Flying aircraft:** untargetable (no airborne mask).
- **Landed aircraft:** they are VEHICLE, so they could be hit. This is a design note only.
- **Bridges and dual-KindOf objects** (e.g. VEHICLE+STRUCTURE): not checked, and not guessed.

## Damage is not a guaranteed kill
- Vehicle armors don't list GRENADE, so ArmorTemplate Default applies, which is 100 (xsd default). Static damage is not 0 for normal armors.
- **Exceptions that do give 0:**
  - InvulnerableArmor and ProjectileArmor (Default 0);
  - Iron Curtain / invulnerable states;
  - any runtime damage immunity or shield.
- CryoBeamFrozenArmor (90000) and ShrinkRay (200) only increase damage.
- So this is a "should one-shot normal vehicles" source candidate, **not a guaranteed kill**.

## Runtime only
- Whether the AI and auto-choice pick the rifle over the bombing run against vehicles.
- Whether both nuggets resolve on one shot.
- How DETONATED death looks, and what happens to passengers and garrisons.
- Landed aircraft behaviour.

## Open design question (unchanged from R81)
- The user's L737 wording "对付载具、舰船改为用狙击枪" vs the 300 bombing run that stays against vehicles. The batch keeps both, following the 17:46 decision.
