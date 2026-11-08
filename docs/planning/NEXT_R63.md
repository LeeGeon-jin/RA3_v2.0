# Next (R63): Iron Curtain 60 s ×1.5 radius + Chronosphere ×1.5 radius — decided (phase 一), not implemented
Refs: `ironcurtain_chrono_sdk_refs.tar.gz` (9 SDK files: AttributeModifier, SpecialPowerTemplates, Weapon, Soviet/Props/IronCurtainEffect, Soviet/Soviet.xml, AlliedSuperWeapon, A09_IronCurtainEffect, AlliedBomberAircraft, CampaignOverrides).

## Requirement
- **5.1 #13, L236 (user):** "现在铁幕生效时间多久？能不能改成一分钟？还有，铁幕应用范围能不能改为1.5倍？超时空应用范围改为1.5倍？" Difficulty 容易, phase 一.
- **L239-240 (plan):**
  - Iron Curtain: 20 s → 60 s; the three radii 100 → 150 together (aura, cursor, infantry kill).
  - Chronosphere: select radius 100 → 150 (store radius + both cursors).
  - Sphere FX models are fixed-size (display only).

## Package state b97 — nothing done yet
| # | Where (package unless noted) | Now | Target |
|---|---|---|---|
| 1 | GlobalData/AttributeModifier.xml `AttributeModifier_IronCurtain` (L129) Duration, **L136** | 20s | **60s** |
| 2 | GlobalData/SpecialPowerTemplates.xml `SpecialPowerIronCurtain` (L93) RadiusCursorRadius, **L101** | 100 | **150** |
| 3 | GlobalData/Weapon.xml `IronCurtainInfantryDeathWeapon` (L5257) DamageNugget Radius | 100.0 | **150.0** |
| 4 | **Soviet/Props/IronCurtainEffect.xml — not in package** (SDK, 92 lines) AttributeModifierAuraUpdate Range, SDK **L61** | 100 | **150** |
| 5 | Allied/Structures/AlliedSuperWeapon.xml `StoreObjectsSpecialPower` Radius, **L465** | 100 | **150** |
| 6 | SpecialPowerTemplates `SpecialPowerChronosphereObjectSelect` RadiusCursorRadius, **L499** | 100 | **150** |
| 7 | SpecialPowerTemplates `SpecialPowerChronosphereObjectSpawn` RadiusCursorRadius, **L523** | 100 | **150** |

## Dependencies
- IronCurtainEffect is loaded by SDK Soviet.xml L90 (`props/IronCurtainEffect.xml`) and created by OCL_IronCurtain. Its includes are ART:FXIronCurtainSphere.w3x and GlobalDefines.
  - Package convention: full SDK copy at `data/Soviet/Props/IronCurtainEffect.xml`, Mod +1 `type="all"`, ART include kept (unit convention, Batch57/58).
- **Campaign:**
  - A09_IronCurtainEffect (Range 750) uses the same modifier, so it also becomes 60 s. The doc accepts this.
  - The A03 Heidelberg overrides live in map files (radius 825/750) → untouched.
  - CampaignOverrides has no Iron Curtain/Chrono entry.
- No other user of IronCurtainInfantryDeathWeapon.
- Other `Duration="20s"` lines (AttributeModifier L15/375/657) belong to other modifiers → **do not touch**.

## Minimal Batch 63
- Text edits:
  - AttributeModifier.xml: 1 line;
  - SpecialPowerTemplates.xml: 3 lines;
  - Weapon.xml: 1 line;
  - AlliedSuperWeapon.xml: 1 line.
- New full SDK copy of IronCurtainEffect.xml with 1 line changed; Mod +1.
- **Expected:** 112 XML, Mod 111 all; total value changes = 7 lines; no command change.
- **Native test:** 60 s expiry, infantry kill at 150, Chronosphere 150 mass teleport (possible stutter), FX smaller than the area.

## Second ready candidate (small)
- **Century Bomber "投弹速度加倍"**, L622 (phase 一); plan L625.
- Package Weapon.xml `AlliedBomberAircraftBombWeapon` FiringDuration Min/Max **.25s (L1661-1662) → .125s**.
- `_AirPower` (L1681) inherits it, so it doubles too (same bomber). CampaignOverrides L1035 only overrides ClipReloadTime.
- Weapon.xml 2 lines.

## Checked and not candidates
- **Assault Destroyer land speed:** L638 says 90/90, but L679 says "本人指定 65，取代前一条的 60". The package has 65. **Doc conflict → ask.**
- **Soviet AA gun ground fire (L779) / Twinblade AA (L833):** both are **phase 二** (not phase 1).
  - The AA gun can only hit ground with a pitch change (MinimumPitch 45d). The −10d is a plan value, and the plan also leaves DamageType vs infantry "待本人定".
  - Twinblade: the plan does not say which weapons, slot or bones.
  - Not implementation-only choices: they change aiming/visuals and values.
- **Confirmed done in b97:** riot shield SPEED 70%; Vindicator 3/4; IFV tesla 0.375; Tanya C4 0.5; Akula/Stingray/Yari; Kirov/Twinblade; Dreadnought; Shogun; Japan miner; wave gun; Yuriko; Bullfrog mask.
