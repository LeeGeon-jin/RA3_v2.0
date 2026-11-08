# Next (R59): Tesla coil charge ½ + combat-engineer pistol aim 0 — decided, not implemented
Refs: `tesla_engineer_sdk_refs.tar.gz` (SDK Weapon.xml + users).

## Japan structures: nothing left to do
Every Japan structure value in L221 (11-06) is already in the package, or the user decided it doesn't change:
- PP unpack 8 and refinery 18 are in the package;
- barracks (4+8) and naval yard (4+18) already match in the original;
- war factory is decided unchanged.
The open "does Japan BuildTime count?" question is a test item, not a split to guess. → skip.

## Package checks for the other simple rows (already done in b93, not repeated)
- Riptide chaingun clip 10.
- Guardian ClipReload 0.8.
- Athena speed 75 / targeter 0.5.
- Dreadnought 20 s / reload 2.5.
- Yari / Japan engineer sprint 30 s.

## Missing — decided values
| # | Quote (devdoc) | SDK = b93 now | Target |
|---|---|---|---|
| 5.5 #12 | L875 "磁暴线圈充能时间减半"; plan L878 | Weapon.xml `SovietBaseDefenseAdvancedTeslaGun` PreAttackDelay Min/Max 2.5s (b93 L4121-4123) | **1.25s / 1.25s** |
| 5.5 #4 | L725 "战斗工兵手枪瞄准速度归零"; plan L729 | `SovietEngineerPistol` PreAttackDelay Min/Max 0.5s (b93 L5198-5200) | **0.0s / 0.0s** |

## Dependencies
- **TeslaGun:**
  - used by SovietBaseDefenseAdvanced.xml L365 (package);
  - inherited by EI_EasterIslandHeadDefenseTeslaGun, which **overrides** PreAttackDelay 3.0s, so it is unaffected;
  - also used by the campaign SovietTeslaWallHub, which follows under the global "campaign too" rule.
  - The comment says the delay is "needed for NotifyWhenAttackingBehavior (hackish)" → test: assist/charge animation still fires.
  - Not the TeslaLinkGun (overcharge); unchanged.
- **EngineerPistol:** only SovietEngineer.xml L828. Bunker "修碉堡减半" has an unknown parameter location (L729 "待核") → **excluded**.

## Excluded (not guessed)
- **Hammer "开炮间隔减三分之一"** (L767): the SDK ClipReloadTime is **Min 0.6 / Max 1.0**. The plan gives only "约0.33s" for Min; there's no decision for Max → needs confirmation.

## Minimal Batch 59
- Text edit of package `data/GlobalData/Weapon.xml` only:
  - L4122-4123 `2.5s` → `1.25s`;
  - L5199-5200 `0.5s` → `0.0s`.
- Expected diff vs 58: exactly 4 lines. No Mod or command change; 110 XML.
- **Native test:**
  - Tesla coil assist behaviour.
  - Pistol behaviour.
- SDK precedent for `PreAttackDelay 0.0s/0.0s`: Weapon.xml L5748-5750 and L8451-8453.
