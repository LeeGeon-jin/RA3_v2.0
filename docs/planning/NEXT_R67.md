# Next (R67): Proton Collider shots ×2
Refs: `proton_r67_sdk_refs.tar.gz` (64755 B, sha256 9ec864e5…7d75):
- ObjectCreationLists, Weapon, AlliedSuperWeaponAdvanced, AlliedSuperWeaponAdvancedEffect, SpecialPowerTemplates;
- global.xml, Static.xml;
- AssetTypeObjectCreationList.xsd, CnC3Types.xsd.

## Requirement
- **devdoc L242 (user):** "盟军超级武器zhizi撞击炮是打几发？炮弹量加一倍吧". Marked easy, phase 一.
  - The **user decision is only "shots ×2" (5→10).**
- **The rest comes from the plan (L245-246), not from the user:**
  - add 5 identical FlingObjects at InitialDelay 5–9 s;
  - angles 0,36…324;
  - per-shot damage, radius and interval unchanged.
- **Technical choices within "×2, nothing else changed":**
  - keeping the 1 s spacing is the only choice that does not change the interval;
  - the angle spread is placement only.

## Chain (SDK, package)
1. AlliedSuperWeaponAdvanced L446-448: `SpecialWeapon="ParticleCannonWeapon"`. Not in the package.
2. **ParticleCannonWeapon** (package Weapon.xml L1320; text same as SDK):
   - `WeaponOCLNugget OCL_ParticleCannonProjectiles` + `OCLParticleCannon` (shroud revealer);
   - AiHint ParticleAcceleratorFinalWeapon.
3. **OCL_ParticleCannonProjectiles** (SDK ObjectCreationLists L442-543) has 5 FlingObjects. Each is:
   - CreateObject ParticleCannonProjectile, Count 1, Speed 100, Height 0;
   - InitialDelay 0/1/2/3/4s, UsePrimaryObjectForOffsets;
   - Offset z500, DistanceFromTarget 75/75, AngleAroundTarget 0/72/144/216/288, DistanceAtTarget 50/50.
4. **ParticleCannonProjectile** (AlliedSuperWeaponAdvancedEffect.xml L11-67): FireWeaponWhenDead → ParticleAcceleratorFinalWeapon (400 / taper 200 / r250 EXPLOSIVE).
5. Only reference to the OCL: Weapon.xml. No campaign override.

## Package state
- **ObjectCreationLists.xml is NOT in the package.** It is loaded from `global.xml` L74, which the package Mod includes as `type="reference"`.
- Package precedent: new OCLs are placed inside the package object files under **unique new ids** (neutral buildings, statues) to avoid colliding with the reference ids.
- There is no package precedent for redefining a global OCL with the same id.

## Minimal batch (technical route chosen: new id, no full 4076-line OCL copy)
1. **New OCL `OCL_ParticleCannonProjectiles_x2`:**
   - 10 FlingObjects, each a verbatim copy of the SDK FlingObject except InitialDelay 0…9s and AngleAroundTarget Low=High 0,36,…,324;
   - every other attribute exactly as SDK.
   - **Location:** put it in a small new data file, e.g. `GlobalData/ObjectCreationLists_ProtonX2.xml` with an AssetDeclaration in the default namespace, Mod +1 all.
   - **Alternative:** a full copy of AlliedSuperWeaponAdvancedEffect.xml. Not needed.
2. **Weapon.xml ParticleCannonWeapon:** 1 line, WeaponOCL → `OCL_ParticleCannonProjectiles_x2`. OCLParticleCannon, the AiHint and everything else stay.
3. **Expected:**
   - 114 XML; Mod 113 all;
   - Weapon 1 line; other 112 files byte-identical;
   - commands unchanged.

## Shared side effects / risks
- **Total damage roughly doubles.** This is inherent to "×2"; per-shot values are unchanged.
- **Visual/info only, not changed (would expand scope):**
  - the 5 s beacon (OCL_ProtonCollider_Generic5SecondBeacon, building L518) and its audio are unchanged;
  - the effect file has a LifetimeUpdate 8s (AlliedSuperWeaponAdvancedEffect.xml L102-105, in the second GameObject after the projectile at L69+; likely the shroud revealer — verify), so the last shots may land after the reveal ends.
- AI hint and SpecialPower reload 360 s are unchanged.

## Native test
- All 10 spawn and hit; the actual spacing and total duration (~10 s is theory).
- Frame rate.
- Whether a weapon-owned OCL in a mod file resolves against the reference global.xml load.
