# Next (R73): Hammer tank fire interval −⅓ — one value pair; bunker item closed
Refs: `r73_sdk_refs.tar.gz` (56102 B, sha256 9e0b6d52bf65154e…): Weapon, SovietAntiVehicleVehicleTech1, Tutorial_SovietTech1Tank, SovietEngineer, SovietBunker, SpecialPowerTemplates.

## 1. Hammer (devdoc L767, phase 一)
- **User:** "铁锤坦克开炮间隔减三分之一". No later revision mentions Hammer (searched 铁锤 / 三分之一 / SovietAntiVehicleVehicleTech1).
- **Plan L771:** "FiringDuration 0.2s + ClipReloadTime 0.6s（约 0.8 秒一发）→ ClipReloadTime 约 0.33s（间隔约 0.53 秒）".
  - **The plan read only the Min.** Real SDK = package (b107 Weapon.xml L6302-6318, identical to SDK):
    - ClipSize 1, AutoReloadsClip AUTO;
    - FiringDuration 0.2/0.2s;
    - **ClipReloadTime Min 0.6s / Max 1.0s**.
  - → interval ≈ 0.8–1.2 s.
- **"减三分之一" = interval × 2/3.** This is arithmetic on the user's own instruction, the same reading as the plan (0.8→0.53), not a new design value.
  - Applied to the whole range: 0.533–0.8 s.
  - **Technical route** (same as the plan): keep FiringDuration 0.2 and shorten reload only. Min 0.6→**0.333s**, Max 1.0→**0.6s**.
  - The alternative (scaling FiringDuration too) gives the same interval but alters the fire cycle → not chosen.
  - **Parent check:** if the parent considers the Max an unauthorised extension, the only open question is "apply ⅓ to the random range's upper end too?". Arithmetic says yes.
- **Shared effects:**
  - `Leech_SovietTankCannon` (L7093-7096) inheritFrom it, with no timing override → also faster. It is used when a Hammer leeches another Hammer (SovietAntiVehicleVehicleTech1 L888) — consistent with "Hammer fire interval".
  - Campaign `Tutorial_SovietTech1Tank` (Units_Campaign L262) uses the same weapon. The doc's global rule applies to campaign too.
  - No CampaignOverrides entry. Damage, warhead, range 150, ScatterableWeapon parent and leech beam are unchanged.
- **Minimal batch 73:**
  - Weapon.xml L6317-6318 only: `MinSeconds="0.333s" MaxSeconds="0.6s"`.
  - → 118 XML, Mod 116; 1 file, 2 values; other 117 byte-identical.
- **Native test:** the real interval, and ScatterableWeapon/AutoReload interplay.

## 2. Bunker (L725 "修碉堡速度减半") — do NOT implement
- **Real chain** (for the record):
  - SovietEngineer `AssembleStructureSpecialAbilityUpdate NewObjectAssemblyTime="10s"` (SovietEngineer.xml L905-913);
  - SovietBunker `StructureUnpackUpdate UnpackTime="10s"` (L268-270, BuildTime 0.0);
  - SpecialPower_ConstructSovietBunker ReloadTime 120s / Money −500.
- **Superseded:** the latest 11-06 revision (L31 / L212, "好的不改了…围墙、碉堡不减半") keeps the bunker time unchanged at 10 s. Not a candidate.
- The pistol PreAttackDelay part was done in b59.

## Remaining (no artificial blockers)
- **User design:**
  - health values (Guard02 / clone / quick-production) and immediate restore;
  - Apocalypse AA, paradrop, oil derrick;
  - sentry conscript count;
  - Natasha one-shot scope/death type and bombing range;
  - MCV/miner MG.
- **Native test only:** all implemented timing/override batches (59–72); aircraft passenger survival; instant capture; crush.
