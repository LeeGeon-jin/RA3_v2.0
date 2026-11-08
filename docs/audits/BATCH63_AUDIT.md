# BATCH63 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete. The cloud's "independent audit passed" is only its own self-check and was not used.

## Package
- Source: `<handoff>/batch63_ironcurtain_chrono.tar.gz`, readable. 286302 B, sha256 c2d2e94e…c42d6 match.
- All entries under `data/`. 112 XML parse; Mod 111 all + 3 ref.
- **Mod:** +1 line L28 `<Include type="all" source="DATA:Soviet/Props/IronCurtainEffect.xml" />` (type verified in the real file).
- vs 62: the 4 files below, Mod, and the new file changed. The other 106 files are byte-identical, including LogicCommand and LogicCommandSet.

## Diffs (real)
| File | Line | Inside | Change |
|---|---|---|---|
| AttributeModifier.xml | L136 | `AttributeModifier_IronCurtain` (L129) | Duration 20s → 60s |
| SpecialPowerTemplates.xml | L101 | SpecialPowerIronCurtain | RadiusCursorRadius 100 → 150 |
| SpecialPowerTemplates.xml | L499 | SpecialPowerChronosphereObjectSelect | 100 → 150 |
| SpecialPowerTemplates.xml | L523 | SpecialPowerChronosphereObjectSpawn | 100 → 150 |
| Weapon.xml | L5265 | IronCurtainInfantryDeathWeapon (L5257) | DamageNugget Radius 100.0 → 150.0 |
| AlliedSuperWeapon.xml | L465 | StoreObjectsSpecialPower | Radius 100 → 150 |
| **new** Soviet/Props/IronCurtainEffect.xml | L61 | AttributeModifierAuraUpdate | Range 100 → 150 |

- The new file is 92 lines, same as SDK, and differs only at L61.
- It keeps the ART:FXIronCurtainSphere include, GlobalDefines, Draw, LifetimeUpdate 3.0s, FireWeaponUpdate (death weapon, FireDelay 0.1s), the aura filter and RefreshDelay.
- Each of the 4 old files differs from 62 only in the listed lines, so earlier changes are kept. Other Duration="20s" modifiers are untouched.

## Dependency chain
- **Iron Curtain:** SpecialPowerIronCurtain → OCL_IronCurtain (SDK ObjectCreationLists L272) → IronCurtainEffect.
  - The effect object lives 3 s. Its aura (refresh 0.1 s) applies AttributeModifier_IronCurtain, and the duration comes from the modifier: the aura schema has only Range, no duration (AttributeModifierAuraUpdate.xsd L23).
  - So 60 s should come from the modifier, as the original 20 s did. **Not proven:** whether the engine removes the modifier when the aura object dies or the unit leaves → native test.
  - Infantry kill at 150 via the one-shot weapon.
- **Chronosphere:** StoreObjectsSpecialPower Radius (selection) 150, plus both cursors 150.
  - TeleportStoredObjectsSpecialPower / TeleportStoredObjectsUpdate (L472-500) have no radius of their own: they teleport the stored set.
  - OCL_Chronosphere / Persistent create effects only.
- **Campaign:** A09_IronCurtainEffect shares the modifier, so it becomes 60 s (accepted in doc L239). Heidelberg map overrides are untouched.
