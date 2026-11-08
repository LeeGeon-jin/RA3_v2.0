# Next (R68): Natasha — unlimited + Pilot Snipe cooldown 10 s (decided numeric part only)
Refs: `r68_sdk_refs.tar.gz` (64145 B, sha256 57fee674…0b724518):
- SovietCommandoTech1, SpecialPowerTemplates, LogicCommand, Weapon;
- CampaignOverrides, Armor, Static.xml.

## How this was found
I scanned all 72 phase 一 / 一/二 entries in devdoc against b102 by diffing the actual object/weapon values. Already done in package:
- coastal gun homing;
- spy/Tanya/Javelin/Guardian/Athena/Riptide;
- Tesla trooper, short-circuit range 75;
- Bullfrog/ACV/IFV/turret passengers survive;
- Dreadnought;
- outpost 15 s, miners 75;
- Yuriko/Tanya unlimited;
- sprint 30 s;
- destroyer 65/15 s, etc.

## Requirement
- **devdoc L737 (user):** "娜塔莎：……特殊能力狙击驾驶冷却时间改为10秒，启动时瞄准时间缩短1秒。训练时间20秒。可造无限个". Phase 一/二.
- **Plan L741:**
  - BuildTime 30→20;
  - MaxSimultaneousOfType 1 → 取消;
  - SpecialPower_PilotSnipe ReloadTime 60s → 10s;
  - "瞄准时间参数待核";
  - sniper vs vehicles / bombing range to be designed.

## Package b102
- **Soviet/Units/SovietCommandoTech1.xml:**
  - BuildTime 20 is **done**;
  - L34 `MaxSimultaneousOfType="1"` is **still there**;
  - GameDependency RequiredObject SovietTechStructure (L39-42) is already the battle-lab prerequisite.
- **GlobalData/SpecialPowerTemplates.xml** L914-915: SpecialPower_PilotSnipe `ReloadTime="60s"` is **unchanged**.
  - The template is used only by Natasha (SovietCommandoTech1 L1083-1089) and Command_ActivatePilotSnipeSpecialPower.
  - No CampaignOverrides entry.
- **Precedents:**
  - Tanya (b102 AlliedCommandoTech1) and Yuriko have `MaxSimultaneousOfType` deleted.
  - Natasha should follow the same: delete the attribute, keep `UnitIntro` etc.

## Minimal Batch 68
1. SovietCommandoTech1.xml: delete L34 `MaxSimultaneousOfType="1"` only. All other lines kept.
2. SpecialPowerTemplates.xml L915: `ReloadTime="60s"` → `"10s"`.
3. Expected:
   - 114 XML, Mod 113 all, commands unchanged;
   - 2 files change (−1 line / 1 value); the other 112 files byte-identical.
4. **Native test:**
   - multiple Natashas are buildable;
   - the cooldown is 10 s;
   - AI/stat behaviour with several heroes (doc L1565 performance note).

## Excluded (genuinely undecided)
- **"瞄准时间缩短1秒":**
  - SovietCommandoPilotSnipeWeapon (Weapon L686) timing still needs to be located, so it is not in this batch.
  - The plan marks it 待核. Next research: read that weapon's PreAttackDelay/FiringDuration before deciding.
- **Sniper one-shots vehicles/ships, and the safe-distance bombing range:** these need new damage/range values the user did not give.

## Other decided, unimplemented candidates found (for later batches)
- **L266 (user) — remove front/back damage difference:**
  - Armor.xml (Static.xml L28, not in package).
  - Set Side/RearDamageScalar of the 10 non-100 templates to 100% (30 non-100 attribute lines among 15 templates — recount the exact 10 before implementing).
  - Needs a full Armor.xml copy.
- **L272 — default music 0%:** Sounds/AudioSettings.xml DefaultMusicVolume 50%→0% (audio.xml reference; packaging path to verify).
- **L278 — default classic mouse:** UIComponentOptionsSettingsGeneral DefaultAlternateMouse false→true.
- **L272/L278 caveat:** a profile's Options.ini overrides the default (doc limitation).

## Still truly blocked (user decision)
- Guard02 / clone center / quick production center health; quick-production immediate restore.
- Apocalypse AA design; paradrop button; oil derrick.
- Sentry gun conscript count (L708 "数量待定"); aircraft passenger survival (L179 需实测).
- Hammer ⅓; bunker repair parameter; Natasha anti-vehicle/bombing values.
